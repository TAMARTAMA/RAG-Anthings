from app.services.prob_service import ask_prob
from app.models.types_chat import  ProbabilityRequest

from fastapi import APIRouter
router = APIRouter()

@router.post("/get_probalitiy")
def get_probability(req: ProbabilityRequest):
    p = ask_prob(req.question, req.answer)
    print(f" Probability calculated: {p}")
    return {"probability": p}

    