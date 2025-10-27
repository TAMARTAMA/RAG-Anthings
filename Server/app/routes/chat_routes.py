from fastapi import APIRouter, Query
from app.models.types_chat import MessageRateRequest, MessageAddRequest
from app.services.process_question import process_asking
from app.services.chat_history import update_rate, add_chat, get_all_chats
import time
router = APIRouter()

@router.post("/add")
def ask(req: MessageAddRequest):
    ans,keywords_list = process_asking(req.request)
    ans = ans["text"]
    print(f" Answer generated: {ans} time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

    id = add_chat(req.request, ans,keywords_list)
    return {"answer": ans, "messegeId": id}

@router.post("/rate")
def rate(req: MessageRateRequest):
    success = update_rate(req.messageId, req.rating)
    if success:
        return {"status": "ok"}
    return {"status": "error", "message": "id not found"}

@router.get("/history")
def get_history_route(userId: str = Query(..., description="Chat ID")):
    return get_all_chats()
