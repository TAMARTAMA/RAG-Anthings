from datetime import datetime
import jsonlines
import json
import uuid
import os
from pathlib import Path
from app.config import CHATS_FILE, RATINGS_FILE

def create_new_chat(question, answer, userId, titles=None, links=None):
    chat_id = str(uuid.uuid4())

    chat = {
        "id": chat_id,
        "userId": userId,
        "title": question[:30] + ("..." if len(question) > 30 else ""),
        "messages": [
            {
                "id": str(uuid.uuid4()),
                "role": "user",
                "content": question,
                "replyTo": None,
                "timestamp": None
            },
            {
                "id": str(uuid.uuid4()),
                "role": "assistant",
                "content": answer,
                "replyTo": None,
                "timestamp": None,
                "links": links or []
            }
        ],
        "createdAt": None,
        "updatedAt": None
    }

    with jsonlines.open(CHATS_FILE, 'a') as writer:
        writer.write(chat)

    return chat_id

def add_message_to_chat(chat_id, question, answer, links=None):

    chats = []
    with jsonlines.open(CHATS_FILE, "r") as reader:
        for c in reader:
            chats.append(c)

    for c in chats:
        if c["id"] == chat_id:
            user_msg = {
                "id": str(uuid.uuid4()),
                "role": "user",
                "content": question,
                "timestamp": None,
                "replyTo": None
            }
            bot_msg = {
                "id": str(uuid.uuid4()),
                "role": "assistant",
                "content": answer,
                "timestamp": None,
                "replyTo": user_msg["id"],
                "links": links or []
            }

            c["messages"].append(user_msg)
            c["messages"].append(bot_msg)
            c["updatedAt"] = None
            break

    with jsonlines.open(CHATS_FILE, "w") as writer:
        for c in chats:
            writer.write(c)

    return chat_id



def update_rate(chat_id: int, rate: str):
    with open(RATINGS_FILE, 'a+', encoding='utf-8') as f:
        f.seek(0)
        content = f.read().strip()
        data = json.loads(content) if content else {}

    data[str(chat_id)] = rate

    with open(RATINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f" Updated rate for chat {chat_id} → {rate}")

def get_chats_by_user(user_id: str):
    chats = []

    if user_id == "NoUser":
        return chats

    with jsonlines.open(CHATS_FILE, "r") as reader:
        for c in reader:
            if c.get("userId") == user_id:
                chats.append(c)

    return chats
def get_chat_by_id(chat_id: str):
    with jsonlines.open(CHATS_FILE, "r") as reader:
        for c in reader:
            if c.get("id") == chat_id:
                return c
    return None

def delete_chat_by_id(chat_id: str) -> bool:

    chats = []
    deleted = False

    with jsonlines.open(CHATS_FILE, "r") as reader:
        for c in reader:
            if c.get("id") == chat_id:
                deleted = True  
            else:
                chats.append(c)

    with jsonlines.open(CHATS_FILE, "w") as writer:
        for c in chats:
            writer.write(c)

    return deleted
