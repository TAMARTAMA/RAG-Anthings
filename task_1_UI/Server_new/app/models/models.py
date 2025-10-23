from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

class Ask(BaseModel):
    message: str

class RateRequest(BaseModel):
    id_question: int
    rating: Optional[Literal["LIKE", "DISLIKE"]] = None



class ChatMessage(BaseModel):
    id: str
    role: str
    content: str
    timestamp: datetime
    rating: Optional[Literal["like", "dislike", None]] = None
    replyTo: Optional[str] = None


class MessageAddRequest(BaseModel):
    request: str  # שימי לב לשגיאת כתיב אם זו באמת המילה בפרונט
    userId: str


class MessageRateRequest(BaseModel):
    userId: str
    messageId: str
    rating: Optional[Literal["like", "dislike", None]]
