from app.models.prompts import system_prompt_prob, user_prompt_prob
import requests
import re
from app.config import SERVER_MODEL_URL
def ask_prob(question: str, answer: str) -> int:
    
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt_prob},
            {"role": "user", "content": user_prompt_prob.format(question=question, answer=answer)}
        ]
    }
    r = requests.post(SERVER_MODEL_URL, json=payload, timeout=60)
    if not r.ok:
        print("SERVER ERROR BODY:", r.text)
        r.raise_for_status()
    text = r.json().get("text", "").strip()
    m = re.search(r"-?\d+", text)
    score = int(m.group(0)) if m else 0
    score = min(max(score, 0), 100)
    return score