from pydantic import BaseModel
from typing import Literal, Optional, List, Dict, Any
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
    index: str
    chatId: str | None = None

class MessageRateRequest(BaseModel):
    userId: str
    messageId: str

    rating: Optional[Literal["like", "dislike", None]] = None

class ProbabilityRequest(BaseModel):
    question: str
    answer: str
class RemoveIndexRequest(BaseModel):
    index: str
    UserId: str
