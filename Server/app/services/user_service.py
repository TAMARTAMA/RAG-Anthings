import json, bcrypt
from pathlib import Path
from typing import Dict, Any, List
from app.config import BASE_DIR

# ----------------------------------------
# File path for user data storage
# ----------------------------------------
USERS_FILE = BASE_DIR / "data" / "users.json"
USERS_FILE.parent.mkdir(parents=True, exist_ok=True)

# ----------------------------------------
# Helper functions to load and save user data
# ----------------------------------------
def _load() -> Dict[str, Any]:
    """Load user data from JSON file."""
    if USERS_FILE.exists():
        return json.loads(USERS_FILE.read_text(encoding="utf-8"))
    return {}

def _save(d: Dict[str, Any]) -> None:
    """Save user data to JSON file."""
    USERS_FILE.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

# ----------------------------------------
# User management functions
# ----------------------------------------
def create_user(user_id: str, password: str) -> Dict[str, Any]:
    """Create a new user with hashed password."""
    d = _load()
    if user_id in d:
        raise ValueError("user exists")
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    u = {"id": user_id, "password_hash": pw_hash, "indexs": ["wikipedia"]}
    d[user_id] = u
    _save(d)
    return u

def verify_password(user_id: str, password: str) -> bool:
    """Verify user's password against stored hash."""
    u = _load().get(user_id)
    return bool(u and bcrypt.checkpw(password.encode(), u["password_hash"].encode()))

def get_user(user_id: str) -> Dict[str, Any] | None:
    """Return user data by ID, or None if not found."""
    return _load().get(user_id)

def list_user_indexes(user_id: str) -> List[str]:
    """Return list of indexes assigned to the user."""
    u = get_user(user_id)
    return (u or {}).get("indexs", ["wikipedia"])

def add_index_to_user(user_id: str, index_name: str) -> Dict[str, Any]:
    """Add an index to user's index list if not already present."""
    d = _load()
    u = d.get(user_id)
    if not u:
        raise ValueError("user not found")
    if index_name not in u["indexs"]:
        u["indexs"].append(index_name)
    d[user_id] = u
    _save(d)
    return u

def remove_index_from_user(user_id: str, index_name: str) -> Dict[str, Any]:
    """Remove an index from user's list and return updated user object."""
    d = _load()
    u = d.get(user_id)
    if not u:
        raise ValueError("user not found")

    if "indexs" not in u or not isinstance(u["indexs"], list):
        u["indexs"] = []

    u["indexs"] = [ix for ix in u["indexs"] if ix != index_name]
    d[user_id] = u
    _save(d)
    return u