from fastapi import APIRouter, Query
from app.models.models import MessageAddRequest, MessageRateRequest
from app.services.message_service import add_message, get_history, rate_message

router = APIRouter(prefix="/api/message", tags=["Messages"])


@router.post("/add")
def add_message_route(req: MessageAddRequest):
    """מקבל הודעה מהלקוח ושולח אותה לעיבוד"""
    return add_message(req)


@router.get("/history")
def get_history_route(userId: str = Query(..., description="Chat ID")):
    """מחזיר את היסטוריית ההודעות של המשתמש/צ'אט"""
    return get_history(userId)


@router.post("/rate")
def rate_message_route(req: MessageRateRequest):
    """מקבל דירוג (לייק/דיסלייק) להודעה"""
    return rate_message(req)
