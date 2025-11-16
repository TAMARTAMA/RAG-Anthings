# app/auth/tokens.py
import base64, hmac, hashlib, json, time
from typing import Optional
from app.config import cfg
from fastapi import Header, HTTPException, Depends


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


def verify_token(authorization: str = Header(...)) -> Optional[str]:
    try:
        if not authorization.startswith("Bearer "):
            raise HTTPException(401, "Invalid authorization header")

        token = authorization.split(" ")[1]

        body, sig = token.split(".")
        expected = _b64(hmac.new(SECRET.encode(), body.encode(), hashlib.sha256).digest())
        if not hmac.compare_digest(sig, expected):
            raise HTTPException(403, "Invalid signature")

        payload = json.loads(_unb64(body))
        if int(time.time()) > int(payload.get("exp", 0)):
            raise HTTPException(403, "Token expired")

        return payload.get("sub")

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(400, "Malformed token")

