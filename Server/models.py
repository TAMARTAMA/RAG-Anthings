from pydantic import BaseModel
from typing import Literal, Optional

class Ask(BaseModel):
    message: str

class RateRequest(BaseModel):
    id_question: int
    rating: Optional[Literal["LIKE", "DISLIKE"]] = None