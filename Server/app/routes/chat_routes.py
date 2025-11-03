from fastapi import APIRouter, Query
from app.models.types_chat import MessageRateRequest, MessageAddRequest
from app.services.process_question import process_asking
from app.services.chat_history import update_rate, add_chat
import time
router = APIRouter()

@router.post("/add")
def ask(req: MessageAddRequest):
    time_started = time.time()
    ans,keywords_list = process_asking(req.request)
    ans = ans["text"]
    print(f" Answer generated: {ans} running time: {time.time() - time_started} seconds")

    id = add_chat(req.request, ans,keywords_list)
    return {"answer": ans, "messegeId": id}

@router.post("/rate")
def rate(req: MessageRateRequest):
    update_rate(req.messageId, req.rating)
    return {"status": "ok"}
@router.post("/add_test")
def ask(req: MessageAddRequest):

    ans,keywords_list,search_results = process_asking(req.request)
    ans = ans["text"]
    id = add_chat(req.request, ans,keywords_list)
    return {"answer": ans, "messegeId": id ,"keywords": keywords_list ,"search_results": search_results}



