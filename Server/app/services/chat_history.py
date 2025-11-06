import jsonlines
import json
import uuid
import os
from pathlib import Path
from app.config import CHATS_FILE, RATINGS_FILE

def add_chat(question: str, answer: str,titles=[]):
    chat_entry = {
        "id": str(uuid.uuid4()),
        "question": question,
        "answer": answer,
        "titles": titles
    }
    with jsonlines.open(CHATS_FILE, mode='a') as writer:
        writer.write(chat_entry)
    print(f" Chat {chat_entry['id']} added")
    return chat_entry["id"]
import json
import os

def update_rate(chat_id: int, rate: str):
    with open(RATINGS_FILE, 'a+', encoding='utf-8') as f:
        f.seek(0)
        content = f.read().strip()
        data = json.loads(content) if content else {}

    data[str(chat_id)] = rate

    with open(RATINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f" Updated rate for chat {chat_id} → {rate}")
