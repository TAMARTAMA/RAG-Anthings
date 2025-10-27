from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    id: str
    role: str
    content: str
    timestamp: datetime
    rating: Optional[Literal["like", "dislike", None]] = None
    replyTo: Optional[str] = None

class MessageAddRequest(BaseModel):
    request: str  
    userId: str

class MessageRateRequest(BaseModel):
    userId: str
    messageId: int

    rating: Optional[Literal["like", "dislike", None]] = None