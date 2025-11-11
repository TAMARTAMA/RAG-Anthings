from app.models.types_chat import MessageRateRequest, MessageAddRequest,AddIndexRequest
from app.services.process_question import process_asking
from app.services.chat_history import update_rate, add_chat
from app.services.search_service import add_documents_to_index,create_index_if_not_exists
from app.services.user_service import add_index_to_user
from fastapi import APIRouter, Response
from fastapi import APIRouter, UploadFile, File, Form
import os
from io import BytesIO
from PyPDF2 import PdfReader
from docx import Document
import time
router = APIRouter()

@router.post("/add")
def ask(req: MessageAddRequest):
    time_started = time.time()
    ans,keywords_list,search_res = process_asking(req.request,req.index)
    ans = ans["text"]
    print(f" Answer generated: {ans} running time: {time.time() - time_started} seconds")
    id = add_chat(req.request, ans,keywords_list)
    linksForMessage = [
        {"title": hit.get("title", "No Title"), "url": hit.get("url", "#")}
        for hit in search_res
    ]
    return {"answer": ans, "messegeId": id, "links": linksForMessage}

@router.post("/rate")
def rate(req: MessageRateRequest):
    update_rate(req.messageId, req.rating)
    return {"status": "ok"}

@router.post("/addtest")
def ask(req: MessageAddRequest):
    ans,keywords_list, search_results = process_asking(req.request)
    id = add_chat(req.request, ans,keywords_list)
    return {"answer": ans, "messegeId": id ,"keywords": keywords_list ,"search_results": search_results}

@router.options("/{path:path}")
def options_handler(path: str):
    return Response(status_code=200)


@router.post("/add_index")
async def add_index(
    user_id: str = Form(...),
    index_name: str = Form(...),
    files: list[UploadFile] = File(...)
):
    """
    Receives files (txt, pdf, docx), reads their content, converts them to {title, text},
    and adds the documents to an OpenSearch index.
    """
    documents = []

    for file in files:
        file_ext = os.path.splitext(file.filename)[1].lower()
        title = os.path.splitext(file.filename)[0]
        text = ""

        try:
            if file_ext == ".txt":
                text = (await file.read()).decode("utf-8", errors="ignore")

            elif file_ext == ".pdf":
                reader = PdfReader(BytesIO(await file.read()))
                text = "\n".join(page.extract_text() or "" for page in reader.pages)

            elif file_ext == ".docx":
                doc = Document(BytesIO(await file.read()))
                text = "\n".join(p.text for p in doc.paragraphs)

            else:
                print(f"Skipping unsupported file type: {file.filename}")
                continue

            if text.strip():
                documents.append({"title": title, "text": text})

        except Exception as e:
            print(f"Error reading {file.filename}: {e}")

    # Add documents to index or create an empty one if none provided
    if documents:
        add_documents_to_index(index_name, documents)
    else:
        create_index_if_not_exists(index_name)

    # link the index to the user
    add_index_to_user(user_id, index_name)

    return {
        "status": "success",
        "message": f"Index '{index_name}' created ({len(documents)} documents added).",
        "document_count": len(documents),
    }
