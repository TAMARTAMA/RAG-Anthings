# app/auth/tokens.py
import base64, hmac, hashlib, json, time
from typing import Optional
from app.config import cfg

SECRET = cfg.get("auth_secret", "CHANGE_ME")

def _b64(x: bytes) -> str:
    return base64.urlsafe_b64encode(x).decode().rstrip("=")

def _unb64(s: str) -> bytes:
    pad = '=' * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)

def make_token(user_id: str, ttl_days: int = 7) -> str:
    payload = {"sub": user_id, "exp": int(time.time()) + ttl_days*24*3600}
    body = _b64(json.dumps(payload).encode())
    sig = hmac.new(SECRET.encode(), body.encode(), hashlib.sha256).digest()
    return body + "." + _b64(sig)

def verify_token(token: str) -> Optional[str]:
    try:
        body, sig = token.split(".")
        expected = _b64(hmac.new(SECRET.encode(), body.encode(), hashlib.sha256).digest())
        if not hmac.compare_digest(sig, expected):
            return None
        payload = json.loads(_unb64(body))
        if int(time.time()) > int(payload.get("exp", 0)):
            return None
        return payload.get("sub")
    except Exception:
        return None
