import json, os
from pathlib import Path

CFG_PATH = Path(__file__).with_name("config.json")
cfg = json.loads(CFG_PATH.read_text(encoding="utf-8"))

CHATS_DIR = cfg["chat_dir"]

def _load_chats():
    if CHATS_DIR.exists():
        with open(CHATS_DIR, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {"chats": []}

def _save_chats(data):
    with open(CHATS_DIR, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_chat(question: str, answer: str):
    data = _load_chats()
    next_id = len(data["chats"]) + 1
    chat_entry = {
        "id": next_id,
        "question": question,
        "answer": answer,
        "rate": None
    }
    data["chats"].append(chat_entry)
    _save_chats(data)
    print(f" נוספה שיחה חדשה עם מזהה {next_id}")


def update_rate(chat_id: int, rate: str):
    data = _load_chats()
    for chat in data["chats"]:
        if chat["id"] == chat_id:
            chat["rate"] = rate
            _save_chats(data)
            print(f" הדירוג של שיחה {chat_id} עודכן ל-{rate}")
            return
    print(f" לא נמצאה שיחה עם מזהה {chat_id}")


def get_all_chats():
    data = _load_chats()
    return data["chats"]


def delete_chat_file():
    if CHATS_DIR.exists():
        os.remove(CHATS_DIR)
        print("🗑️ הקובץ chats.json נמחק בהצלחה.")
    else:
        print("⚠️ אין קובץ למחוק.")
