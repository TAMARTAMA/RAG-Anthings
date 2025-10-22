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
SERVER_MODEL_URL=cfg["remote_server"]["url_LLM"]
SERVER_SEARCH_URL=cfg["remote_server"]["url_search:"]

app = FastAPI(title="Main Server Chatbot")

def process_asking(question: str):
    keywords = send_data_to_server_LLM(SERVER_MODEL_URL, question, system_prompt_keywords)
    # send keywords to server search split the keywords string to list
    keywords_list = keywords.get("text", "").split(", ")
    if not keywords_list or keywords_list == [""]:  # if no keywords found
        return "לא נמצאו מילות מפתח מתאימות לשאלה שלך."
    
    search_results = send_data_to_server_search(SERVER_SEARCH_URL, keywords_list)
    print("Received keywords from remote server:", keywords)
    print("Sending keywords to remote server search:", keywords_list)
    print("Received search results from remote server:", search_results)
    #TODO add summury to docs before sending to LLM
    # prepare docs text
    docs_text = "\n\n".join(
        [f"[{i+1}] Title: {r['title']}" for i, r in enumerate(search_results.get("results", []))]
    )
    system_prompt_bm25_q_filled = system_prompt_bm25_q.format(docs=docs_text)
    return send_data_to_server_LLM(SERVER_MODEL_URL, question, system_prompt_bm25_q_filled)
     

def send_data_to_server_search(url: str, keywords: list):
    payload = {
        "query": keywords
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)

        try:
            return response.json()
        except ValueError:
            return response.text

    except requests.exceptions.RequestException as e:
        return {"error": f"שגיאה בשליחת הבקשה: {str(e)}"}

def send_data_to_server_LLM(url: str, question: str,system_prompt: str):
    
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
    
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)


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