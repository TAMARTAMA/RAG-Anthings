from app.models.types_chat import MessageRateRequest, MessageAddRequest,AddIndexRequest
from app.services.process_question import process_asking
from app.services.chat_history import update_rate, add_chat
from app.services.search_service import add_documents_to_index
from fastapi import APIRouter, Response
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
def add_index(req: AddIndexRequest):
    """
    Route שמקבל בקשה מהמשתמש ליצירת אינדקס חדש:
    1. מוסיף את המסמכים לאינדקס החדש ב־OpenSearch.
    2. מריץ תהליך אינדוקס (אם יש צורך).
    3. מעדכן את רשימת האינדקסים של המשתמש במסד הנתונים.
    """
    try:
        # שלב 1: יצירת אינדקס והוספת מסמכים
        add_documents_to_index(req.index_name, req.documents)

        # שלב 2: (אופציונלי) הרצת תהליך עיבוד נוסף - embeddings, metadata וכו’
        # run_indexing_job(req.index_name)

        # שלב 3: (בעתיד) עדכון משתמש במסד הנתונים
        # add_index_to_user(req.user_id, req.index_name)

        return {
            "status": "success",
            "message": f"Index '{req.index_name}' created and documents added successfully.",
            "document_count": len(req.documents),
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
