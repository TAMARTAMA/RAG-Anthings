from fastapi import FastAPI
from pathlib import Path
import json, os
import requests
from chat_history import add_chat, update_rate, get_all_chats
from models import Ask, RateRequest
from prompts_model import (
    system_prompt_keywords,
    system_prompt_guess,
    system_prompt_more_question,
    system_prompt_bm25_q,
)
CFG_PATH = Path(__file__).with_name("config.json")
cfg = json.loads(CFG_PATH.read_text(encoding="utf-8"))

PORT_SERVER = cfg["server"]["port"]
HOST_SERVER = cfg["server"]["host"]

# CHATS_DIR = cfg["chat_dir"]
SERVER_MODEL_URL=cfg["remote_server"]["url"]


app = FastAPI(title="Main Server Chatbot")

def process_asking(question: str):
    keywords = send_data_to_server(SERVER_MODEL_URL, question, system_prompt_keywords)
    print("Received keywords from remote server:", keywords)
    return keywords



def send_data_to_server(url: str, question: str,system_prompt: str):
    
    payload = {
        "messages" : [
            {
                "role": "system",
                "content": [
                    {"type": "text", "text": system_prompt}
                    ]
                },
            {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question}
                        ]
                },
        ],
        "max_new_tokens": 8,
        "temperature": 0.0001
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)

        try:
            return response.json()
        except ValueError:
            return response.text

    except requests.exceptions.RequestException as e:
        return {"error": f"שגיאה בשליחת הבקשה: {str(e)}"}


@app.post("/ask")
def ask(req: Ask):
    ans = process_asking(req.message)

    # add_chat(req.message, ans)
    return {"answer": ans}

@app.post("/rate")
def rate(req: RateRequest):
    success = update_rate(req.id_question, req.rating)
    if success:
        return {"status": "ok"}
    return {"status": "error", "message": "id not found"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST_SERVER, port=PORT_SERVER)