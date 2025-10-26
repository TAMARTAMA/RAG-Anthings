from app.models.models import MessageAddRequest, MessageRateRequest, ChatMessage
from datetime import datetime
import uuid

# נניח שיש מבנה זיכרון פשוט
chat_history = {}


def add_message(req: MessageAddRequest):
    """מוסיף הודעה חדשה לצ'אט"""
    message = ChatMessage(
        id=str(uuid.uuid4()),
        role="user",
        content=req.requset,
        timestamp=datetime.utcnow(),
    )

    # מוסיפים להיסטוריה של הצ'אט
    chat_history.setdefault(req.userId, []).append(message.dict())

    # תשובה חזרה לפרונט
    return {
        "message": {
            "id": message.id,
            "role": "assistant",
            "content": f"Echo: {req.requset}",
            "timestamp": message.timestamp.isoformat(),
        },
        "chatHistory": {"messages": chat_history[req.userId]},
    }


def get_history(userId: str):
    """מחזיר את היסטוריית הצ'אט"""
    messages = chat_history.get(userId, [])
    return {"chatHistory": {"messages": messages}}


def rate_message(req: MessageRateRequest):
    """מעודכן דירוג להודעה בצ'אט"""
    chat = chat_history.get(req.userId, [])
    for msg in chat:
        if msg["id"] == req.messageId:
            msg["rating"] = req.rating
            return {"success": True}
    return {"error": "message not found"}
