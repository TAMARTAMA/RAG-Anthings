from typing import Optional
from fastapi import APIRouter, Response, Header, Query, UploadFile, File, Form, HTTPException, Depends
from app.models.types_chat import MessageRateRequest, MessageAddRequest, RemoveIndexRequest
from app.services.process_question import process_asking
from app.services.chat_history import (
    update_rate, create_new_chat, add_message_to_chat,
    get_chat_by_id, delete_chat_by_id, get_chats_by_user
)
from app.services.search_service import add_documents_to_index, create_index_if_not_exists, delete_index
from app.services.user_service import add_index_to_user, remove_index_from_user
from app.auth.tokens import verify_token
from PyPDF2 import PdfReader
from docx import Document
from io import BytesIO
import os
import time

router = APIRouter()


@router.post("/add")
def ask(req: MessageAddRequest):
    """Handle a new user message: process question, get answer, and save chat."""
    time_started = time.time()
    print(req)

    answer_obj, keywords_list, search_res = process_asking(req.request, req.index)
    if not isinstance(answer_obj, dict) or "text" not in answer_obj:
        print("LLM ERROR →", answer_obj)
        return {"answer": "answer_obj", "chatId": req.chatId, "links": []}

    answer_text = answer_obj["text"]
    print(answer_obj)

    links = []
    hits = search_res.get("results", search_res) if isinstance(search_res, dict) else search_res
    for hit in hits:
        if isinstance(hit, dict):
            links.append({"title": hit.get("title", "No Title"), "url": hit.get("url", "#")})
        else:
            links.append({"title": hit, "url": hit})

    print("REQUEST CHAT ID:", req.chatId)
    chat_id = create_new_chat(req.request, answer_text, req.userId, keywords_list, links) if not req.chatId else \
              add_message_to_chat(req.chatId, req.request, answer_text, links)

    return {"answer": answer_text, "chatId": chat_id, "links": links}


@router.get("/history")
def get_user_history(userId: str = Query(...), authorization: str = Header(None)):
    """Return all chats for a given user."""
    chats = get_chats_by_user(userId)
    return {"userId": userId, "chats": chats}


@router.post("/rate")
def rate(req: MessageRateRequest):
    """Update message rating."""
    update_rate(req.messageId, req.rating)
    return {"status": "ok"}


@router.options("/{path:path}")
def options_handler(path: str):
    """Handle CORS preflight requests."""
    return Response(status_code=200)


@router.post("/add_index")
async def add_index(
    user_id: str = Form(...),
    index_name: str = Form(...),
    files: Optional[list[UploadFile]] = File(None)
):
    """Create a new OpenSearch index and link it to the user."""
    documents = []
    if files is None:
        files = []

    try:
        for file in files:
            ext = os.path.splitext(file.filename)[1].lower()
            title = os.path.splitext(file.filename)[0]
            text = ""

            if ext == ".txt":
                text = (await file.read()).decode("utf-8", errors="ignore")
            elif ext == ".pdf":
                reader = PdfReader(BytesIO(await file.read()))
                text = "\n".join(page.extract_text() or "" for page in reader.pages)
            elif ext == ".docx":
                doc = Document(BytesIO(await file.read()))
                text = "\n".join(p.text for p in doc.paragraphs)
            else:
                print(f"Skipping unsupported file type: {file.filename}")
                continue

            if text.strip():
                documents.append({"title": title, "text": text})

        try:
            if documents:
                add_documents_to_index(index_name, documents)
            else:
                create_index_if_not_exists(index_name)
        except Exception as es_err:
            print(f"❌ OpenSearch error while creating index '{index_name}': {es_err}")
            raise HTTPException(status_code=500, detail=f"Failed to create index '{index_name}': {str(es_err)}")

        user_data = add_index_to_user(user_id, index_name)
        return {
            "status": "success",
            "message": f"Index '{index_name}' created ({len(documents)} documents added).",
            "document_count": len(documents),
            "user": user_data
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ General error in add_index: {type(e).__name__} - {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error while creating index '{index_name}': {str(e)}")


@router.post("/remove_index")
async def remove_index(data: RemoveIndexRequest):
    """Delete an OpenSearch index and unlink it from the user."""
    index_name = data.index
    user_id = data.UserId

    try:
        deleted = delete_index(index_name)
        if deleted is not True:
            raise Exception(f"Index '{index_name}' could not be deleted.")

        user = remove_index_from_user(user_id, index_name)
        return {
            "status": "success",
            "message": f"Index '{index_name}' removed successfully.",
            "user": user
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove index '{index_name}': {str(e)}")


@router.get("/chat/{chat_id}")
def get_chat(chat_id: str):
    """Return a single chat by ID."""
    chat = get_chat_by_id(chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.delete("/{chat_id}")
def delete_chat(chat_id: str, current: str = Depends(verify_token)):
    """Delete a chat (only if owned by current user)."""
    chat = get_chat_by_id(chat_id)
    if not chat:
        raise HTTPException(404, "Chat not found")

    if chat["userId"] != current:
        raise HTTPException(403, "Not allowed")

    if delete_chat_by_id(chat_id):
        return {"status": "deleted", "chatId": chat_id}

    raise HTTPException(500, "Failed to delete chat")