import json
import os
from pathlib import Path

from app.config import cfg

BASE_DIR = Path(__file__).resolve().parents[2]
CHAT_FILE = (BASE_DIR / Path(cfg["chat_dir"])).resolve()

def _load_chats():
    if CHAT_FILE.exists():
        with open(CHAT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {"chats": []}

def _save_chats(data):
    CHAT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_chat(question: str, answer: str,titels=[]):
    data = _load_chats()
    next_id = len(data["chats"]) + 1
    chat_entry = {
        "id": next_id,
        
        "question": question,
        "answer": answer,
        "rate": None
        ,"titles":[]
    }
    data["chats"].append(chat_entry)
    _save_chats(data)
    print(f" New conversation with ID added {next_id}")


def update_rate(chat_id: int, rate: str):
    data = _load_chats()
    for chat in data["chats"]:
        if chat["id"] == chat_id:
            chat["rate"] = rate
            _save_chats(data)
            print(f" The rating of a conversation {chat_id} updated to {rate}")
            return
    print(f" No conversation with ID found {chat_id}")


def get_all_chats():
    data = _load_chats()
    return data["chats"]
