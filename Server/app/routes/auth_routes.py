# app/routes/auth_routes.py
from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import Optional
from app.services.user_service import (
    create_user, verify_password, get_user,
    list_user_indexes, add_index_to_user, remove_index_from_user
)
from app.auth.tokens import make_token, verify_token

router = APIRouter(prefix="/auth", tags=["auth"])

class SignupIn(BaseModel):
    userId: str
    password: str

class LoginIn(BaseModel):
    userId: str
    password: str

class IndexIn(BaseModel):
    index: str

def current_user_id(authorization: Optional[str] = Header(None)) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(401, "missing token")

    uid = verify_token(authorization)   
    if not uid:
        raise HTTPException(401, "invalid/expired token")

    return uid


@router.post("/signup")
def signup(body: SignupIn):
    uid = body.userId.strip()
    if not uid or not body.password:
        raise HTTPException(400, "userId and password required")
    try:
        user = create_user(uid, body.password)
    except ValueError:
        raise HTTPException(409, "user already exists")
    token = make_token(uid)
    return {"user": {"id": user["id"], "indexs": user["indexs"]},
            "access_token": token, "token_type": "bearer"}

@router.post("/login")
def login(body: LoginIn):
    uid = body.userId.strip()
    if not uid or not body.password:
        raise HTTPException(400, "userId and password required")
    if not verify_password(uid, body.password):
        raise HTTPException(401, "invalid credentials")
    u = get_user(uid)
    token = make_token(uid)
    return {"user": {"id": uid, "indexs": u["indexs"]},
            "access_token": token, "token_type": "bearer"}

@router.get("/indexes")
def get_indexes(current: str = Depends(current_user_id)):
    return {"userId": current, "indexs": list_user_indexes(current)}

@router.post("/indexes/add")
def add_ix(body: IndexIn, current: str = Depends(current_user_id)):
    if not body.index.strip():
        raise HTTPException(400, "index required")
    u = add_index_to_user(current, body.index.strip())
    return {"user": {"id": current, "indexs": u["indexs"]}}

@router.post("/indexes/remove")
def rm_ix(body: IndexIn, current: str = Depends(current_user_id)):
    if not body.index.strip():
        raise HTTPException(400, "index required")
    u = remove_index_from_user(current, body.index.strip())
    return {"user": {"id": current, "indexs": u["indexs"]}}
