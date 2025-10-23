from fastapi import APIRouter
from app.models.models import Ask, RateRequest, MessageAddRequest
from app.utils.process_question import process_asking
from app.chat_history import update_rate

router = APIRouter()

@router.post("/add")
def ask(req: MessageAddRequest):
    print(f"Received message: {req.request}")
    ans = process_asking(req.request)
    print(f"Answer generated: {ans}")  # <--- בדקי אם זה בכלל מודפס
    return {"answer": ans["text"]}
@router.post("/rate")
def rate(req: RateRequest):
    success = update_rate(req.id_question, req.rating)
    if success:
        return {"status": "ok"}
    return {"status": "error", "message": "id not found"}
