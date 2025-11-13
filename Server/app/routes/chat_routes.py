from typing import Optional
from app.models.types_chat import MessageRateRequest, MessageAddRequest,RemoveIndexRequest
from app.services.process_question import process_asking
from app.services.chat_history import update_rate, create_new_chat, add_message_to_chat,get_chat_by_id
from app.services.search_service import add_documents_to_index,create_index_if_not_exists,delete_index
from app.services.user_service import add_index_to_user,remove_index_from_user
from fastapi import APIRouter, Response, Header, Query
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from app.auth.tokens import verify_token
from app.services.chat_history import get_chats_by_user
import os
from io import BytesIO
from PyPDF2 import PdfReader
from docx import Document
import time
router = APIRouter()

@router.post("/add")
def ask(req: MessageAddRequest):
    time_started = time.time()

    answer_obj, keywords_list, search_res = process_asking(req.request, req.index)
    answer_text = answer_obj["text"]

    linksForMessage = []
    hits = search_res.get("results", search_res) if isinstance(search_res, dict) else search_res

    for hit in hits:
        if isinstance(hit, dict):
            linksForMessage.append({
                "title": hit.get("title", "No Title"),
                "url": hit.get("url", "#")
            })
        else:
            linksForMessage.append({
                "title": hit,
                "url": hit
            })
    print("REQUEST CHAT ID: ", req.chatId)

    if not req.chatId:
        chat_id = create_new_chat(req.request, answer_text, req.userId, keywords_list, linksForMessage)
    else:
        chat_id = add_message_to_chat(req.chatId, req.request, answer_text, linksForMessage)

    return {
        "answer": answer_text,
        "chatId": chat_id,
        "links": linksForMessage
    }

@router.get("/history")
def get_user_history(
    userId: str= Query(...),
    authorization: str = Header(None)
):
    # if not authorization or not authorization.startswith("Bearer "):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid token")

    # token = authorization.split("Bearer ")[1]

    # # כאן תוכל לבדוק שה-token תואם ל-userId
    # # לדוגמה:
    # if not verify_token(token, userId):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token does not match user")

    chats = get_chats_by_user(userId)
    return {"userId": userId, "chats": chats}


@router.post("/rate")
def rate(req: MessageRateRequest):
    update_rate(req.messageId, req.rating)
    return {"status": "ok"}

@router.options("/{path:path}")
def options_handler(path: str):
    return Response(status_code=200)


@router.post("/add_index")
async def add_index(
    user_id: str = Form(...),
    index_name: str = Form(...),
    files: Optional[list[UploadFile]] = File(None)
):
    """
    מקבל קבצים (txt, pdf, docx), ממיר אותם למסמכים ומנסה ליצור אינדקס חדש ב־OpenSearch.
    אם לא נוצר אינדקס בהצלחה — לא יקושר למשתמש, ותוחזר שגיאה ללקוח.
    """
    documents = []
    if files is None:
        files = []

    try:
        # קריאת קבצים
        for file in files:
            file_ext = os.path.splitext(file.filename)[1].lower()
            title = os.path.splitext(file.filename)[0]
            text = ""

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

        # ניסיון ליצור אינדקס ב־OpenSearch
        try:
            if documents:
                add_documents_to_index(index_name, documents)
            else:
                create_index_if_not_exists(index_name)

        except (Exception) as es_err:
            # הדפסה לשרת + עצירה
            print(f"❌ OpenSearch error while creating index '{index_name}': {es_err}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create index '{index_name}' in OpenSearch: {str(es_err)}"
            )

        # רק אם הצליח — קישור למשתמש
        user_data = add_index_to_user(user_id, index_name)

        return {
            "status": "success",
            "message": f"Index '{index_name}' created ({len(documents)} documents added).",
            "document_count": len(documents),
            "user": user_data
        }

    except HTTPException:
        # כבר טופלה שגיאה מ־OpenSearch — רק להעביר הלאה
        raise
    except Exception as e:
        # שגיאה כללית (למשל בעיבוד קבצים)
        print(f"❌ General error in add_index: {type(e).__name__} - {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error while creating index '{index_name}': {str(e)}"
        )


@router.post("/remove_index")
async def remove_index(data: RemoveIndexRequest):
    """
    Removes the specified index from OpenSearch and unlinks it from the user.
    Returns the updated user object so the client can setIndexes(resp.user.indexs).
    """
    index_name = data.index
    user_id = data.UserId

    try:
        # 1) מחיקת האינדקס בפועל מ-OpenSearch; אם נכשל – לזרוק חריגה
        # חשוב: delete_index צריך לזרוק חריגה אם המחיקה לא הצליחה.
        deleted = delete_index(index_name)  # אמור להחזיר True/False או לזרוק חריגה
        if deleted is not True:
            # במקרה שהפונקציה שלך מחזירה False כאשר האינדקס לא קיים – נחליט האם לעצור או להמשיך.
            # כאן נבחר לעצור ולהחזיר שגיאה מפורשת:
            raise Exception(f"Index '{index_name}' does not exist or could not be deleted.")

        # 2) עדכון המשתמש והחזרת אובייקט המשתמש המעודכן
        # ודא שהפונקציה מחזירה dict עם המפתח "indexs"
        user = remove_index_from_user(user_id, index_name)

        return {
            "status": "success",
            "message": f"Index '{index_name}' removed successfully.",
            "user": user 
        }

    except HTTPException:
        # להעביר חריגות HTTP כפי שהן
        raise
    except Exception as e:
        # להפוך כל כשל לשגיאת HTTP ברורה ללקוח
        raise HTTPException(
            status_code=500,
            detail=f"Failed to remove index '{index_name}': {str(e)}"
        )
    
@router.get("/chat/{chat_id}")
def get_chat(chat_id: str):
    chat = get_chat_by_id(chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat
   