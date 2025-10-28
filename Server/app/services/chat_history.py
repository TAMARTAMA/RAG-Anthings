import jsonlines
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

def update_rate(chat_id: int, rate: str):
    found = False
    lines = []
    if os.path.exists(RATINGS_FILE):
        with jsonlines.open(RATINGS_FILE, 'r') as r:
            for chat in r and not found:
                if chat["id"] == chat_id:
                    chat["rate"] = rate
                    found = True
                lines.append(chat)
    if not found:
        lines.append({"id": chat_id, "rate": rate})
    with jsonlines.open(RATINGS_FILE, 'w') as w:
        w.write_all(lines)
