from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Literal
from datetime import datetime
app = FastAPI()

# לאפשר גישה מ־React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # או רק ['http://localhost:3000']
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- מבנה נתונים מדומה לשמירת הודעות ---
chat_history = {}
# --- מודלים של בקשות ---

class AddMessageRequest(BaseModel):
    requset: str  # שימי לב: זה עם טעות כתיב כמו ב-frontend שלך
    userId: str

class RateMessageRequest(BaseModel):
    userId: str
    messageId: str
    rating: Optional[Literal["like", "dislike", None]] = None

class Message(BaseModel):
    id: str
    role: str
    content: str
    timestamp: str
    rating: Optional[str] = None
    replyTo: Optional[str] = None


# --- POST /api/message/add ---
@app.post("/api/message/add")
async def add_message(req: AddMessageRequest):
    """מקבל הודעה חדשה מהלקוח ומחזיר תגובה מדומה"""
    user_id = req.userId
    text = req.requset

    # צור מבנה הודעה חדשה
    new_message = Message(
        id=f"msg-{int(datetime.now().timestamp())}",
        role="user",
        content=text,
        timestamp=datetime.now().isoformat(),
    )

    # שמירה בזיכרון
    chat_history.setdefault(user_id, []).append(new_message.dict())

    # תגובה מדומה
    reply_message = Message(
        id=f"msg-{int(datetime.now().timestamp())}-bot",
        role="assistant",
        content=f"Echo: {text}",  # כאן תוכלי לשלב את הלוגיקה האמיתית שלך
        timestamp=datetime.now().isoformat(),
    )
    chat_history[user_id].append(reply_message.dict())

    return {
        "message": reply_message.dict(),
        "chatHistory": {"messages": chat_history[user_id]},
    }


# --- GET /api/message/history ---
@app.get("/api/message/history")
async def get_history(userId: str = Query(...)):
    """מחזיר את ההיסטוריה של המשתמש"""
    messages = chat_history.get(userId, [])
    return {"userId": userId, "messages": messages}


# --- POST /api/message/rate ---
@app.post("/api/message/rate")
async def rate_message(req: RateMessageRequest):
    """עדכון דירוג של הודעה"""
    user_id = req.userId
    message_id = req.messageId
    rating = req.rating

    user_msgs = chat_history.get(user_id, [])
    for msg in user_msgs:
        if msg["id"] == message_id:
            msg["rating"] = rating
            return {"success": True}

    return {"error": "Message not found"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)