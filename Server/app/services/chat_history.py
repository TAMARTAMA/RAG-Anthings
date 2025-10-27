import jsonlines
from pathlib import Path
from app.config import cfg

BASE_DIR = Path(__file__).resolve().parents[2]
CHAT_FILE = (BASE_DIR / Path(cfg["chat_dir"])).with_suffix(".jsonl")

def add_chat(question: str, answer: str,titles=[]):
    chat_entry = {
        "id": sum(1 for _ in open(CHAT_FILE, "r", encoding="utf-8")) + 1 if CHAT_FILE.exists() else 1,
        "question": question,
        "answer": answer,
        "rate": None,
        "titles": titles
    }
    with jsonlines.open(CHAT_FILE, mode='a') as writer:
        writer.write(chat_entry)
    print(f" Chat {chat_entry['id']} added")
    return chat_entry["id"]

def update_rate(chat_id: int, rate: str):
    chats = []
    updated = False
    with jsonlines.open(CHAT_FILE, mode='r') as reader:
        for chat in reader:
            if chat["id"] == chat_id:
                chat["rate"] = rate
                updated = True
            chats.append(chat)
    with jsonlines.open(CHAT_FILE, mode='w') as writer:
        writer.write_all(chats)
    print(f" Updated rate for chat {chat_id}") if updated else print(f" Not found")

def get_all_chats():
    with jsonlines.open(CHAT_FILE, mode='r') as reader:
        return list(reader)
