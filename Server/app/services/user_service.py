import json, bcrypt
from pathlib import Path
from typing import Dict, Any, List
from app.config import BASE_DIR

USERS_FILE = BASE_DIR / "data" / "users.json"
USERS_FILE.parent.mkdir(parents=True, exist_ok=True)

def _load() -> Dict[str, Any]:
    if USERS_FILE.exists():
        return json.loads(USERS_FILE.read_text(encoding="utf-8"))
    return {}

def _save(d: Dict[str, Any]) -> None:
    USERS_FILE.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

def create_user(user_id: str, password: str) -> Dict[str, Any]:
    d = _load()
    if user_id in d:
        raise ValueError("user exists")
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    u = {"id": user_id, "password_hash": pw_hash, "indexs": ["wikipedia"]}
    d[user_id] = u
    _save(d)
    return u

def verify_password(user_id: str, password: str) -> bool:
    u = _load().get(user_id)
    return bool(u and bcrypt.checkpw(password.encode(), u["password_hash"].encode()))

def get_user(user_id: str) -> Dict[str, Any] | None:
    return _load().get(user_id)

def list_user_indexes(user_id: str) -> List[str]:
    u = get_user(user_id)
    return (u or {}).get("indexs", ["wikipedia"])

def add_index_to_user(user_id: str, index_name: str) -> Dict[str, Any]:
    d = _load()
    u = d.get(user_id)
    if not u: raise ValueError("user not found")
    if index_name not in u["indexs"]:
        u["indexs"].append(index_name)
    d[user_id] = u
    _save(d)
    return u


def remove_index_from_user(user_id: str, index_name: str) -> Dict[str, Any]:
    """
    מסיר אינדקס מרשימת האינדקסים של המשתמש ומחזיר את אובייקט המשתמש המעודכן.
    """
    d = _load()
    u = d.get(user_id)
    if not u:
        raise ValueError("user not found")

    # וידוא שקיים מפתח indexs
    if "indexs" not in u or not isinstance(u["indexs"], list):
        u["indexs"] = []

    # הסרת האינדקס
    u["indexs"] = [ix for ix in u["indexs"] if ix != index_name]

    # עדכון ושמירה
    d[user_id] = u
    _save(d)

    # החזרה של המשתמש המעודכן
    return u
