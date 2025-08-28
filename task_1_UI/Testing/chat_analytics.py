
import json
from dataclasses import dataclass
from typing import List, Optional, Tuple
from datetime import datetime, timedelta, timezone

import pandas as pd
import matplotlib.pyplot as plt

@dataclass
class Message:
    id: str
    role: str
    content: str
    timestamp: str
    rating: Optional[str] = None
    replyTo: Optional[str] = None

@dataclass
class Chat:
    id: str
    title: str
    messages: List[Message]
    createdAt: str
    updatedAt: str

def parse_iso(s: str) -> datetime:
    try:
        if s.endswith("Z"):
            return datetime.fromisoformat(s.replace("Z", "+00:00"))
        return datetime.fromisoformat(s)
    except Exception:
        return datetime.fromisoformat(s + "+00:00")

def today_bounds(tz: timezone = timezone.utc) -> Tuple[datetime, datetime]:
    now = datetime.now(tz)
    start = datetime(now.year, now.month, now.day, tzinfo=tz)
    end = start + timedelta(days=1)
    return start, end

def load_dataframe(json_path: str) -> pd.DataFrame:
    raw = json.loads(open(json_path, "r", encoding="utf-8").read())
    recs = []
    for c in raw:
        chat_id = c.get("id", c.get("userId", ""))
        chat_title = c.get("title", f"Chat {chat_id}")
        chat_createdAt = c.get("createdAt", "")
        chat_updatedAt = c.get("updatedAt", "")
        for m in c["messages"]:
            recs.append({
                "chat_id": chat_id,
                "chat_title": chat_title,
                "chat_createdAt": chat_createdAt,
                "chat_updatedAt": chat_updatedAt,
                "message_id": m["id"],
                "role": m["role"],
                "content": m["content"],
                "timestamp": m["timestamp"],
                "rating": m.get("rating"),
                "replyTo": m.get("replyTo"),
                "timestamp_dt": parse_iso(m["timestamp"]),
            })
    df = pd.DataFrame.from_records(recs).sort_values("timestamp_dt")
    df["date"] = df["timestamp_dt"].dt.date
    return df

def query_messages_today(df: pd.DataFrame, tz: timezone = timezone.utc) -> pd.DataFrame:
    start, end = today_bounds(tz)
    return df[(df["timestamp_dt"] >= start) & (df["timestamp_dt"] < end)]

def ratings_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    return df["rating"].value_counts(dropna=False).rename_axis("rating").reset_index(name="count")

def messages_per_chat(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("chat_title")["message_id"].count().reset_index(name="message_count")

def messages_by_role(df: pd.DataFrame) -> pd.DataFrame:
    vc = df["role"].value_counts().reset_index()
    vc.columns = ["role", "count"]
    return vc

def daily_activity(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("date")["message_id"].count().reset_index(name="messages")

def per_chat_ratings(df: pd.DataFrame) -> pd.DataFrame:
    tmp = df.assign(is_like=(df["rating"] == "like").astype(int),
                    is_dislike=(df["rating"] == "dislike").astype(int))
    return tmp.groupby("chat_title")[["is_like", "is_dislike"]].sum().reset_index()

def response_times(df: pd.DataFrame) -> list:
    times = []
    for chat_id, sub in df.groupby("chat_id"):
        sub = sub.sort_values("timestamp_dt")
        last_user = None
        for _, row in sub.iterrows():
            if row["role"] == "user":
                last_user = row["timestamp_dt"]
            elif row["role"] == "assistant" and last_user is not None:
                times.append((row["timestamp_dt"] - last_user).total_seconds())
                last_user = None
    return times

def plot_overall_ratings(df: pd.DataFrame, out_path: str):
    counts = df["rating"].value_counts()
    plt.figure()
    plt.bar(counts.index.astype(str), counts.values)
    plt.title("Overall Ratings Count")
    plt.xlabel("Rating")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(out_path)

import os

if __name__ == "__main__":
    # Use absolute path relative to this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "chats.json")
    if not os.path.exists(json_path):
        json_path = os.path.join(base_dir, "..", "project", "chats.json")
    df = load_dataframe(json_path)
    today = query_messages_today(df)
    print("Messages today:", len(today))
    print("Likes:", (df["rating"] == "like").sum(), "Dislikes:", (df["rating"] == "dislike").sum())
    plot_overall_ratings(df, "overall_ratings.png")
    print("Saved overall_ratings.png")
