from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response, status

from app.db.init import database
from app.db.model import Auth, Token
from app.lib.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)

router = APIRouter()

ACCESS_COOKIE_NAME = "access_token"
REFRESH_COOKIE_NAME = "refresh_token"

COOKIE_SECURE = False
COOKIE_SAMESITE = "lax"


async def get_current_uid(request: Request) -> int:
    token = request.cookies.get(ACCESS_COOKIE_NAME)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return decode_token(token, expected_type="access")


def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    response.set_cookie(
        key=ACCESS_COOKIE_NAME,
        value=access_token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        max_age=7 * 24 * 60 * 60,
    )


def clear_auth_cookies(response: Response) -> None:
    response.delete_cookie(ACCESS_COOKIE_NAME)
    response.delete_cookie(REFRESH_COOKIE_NAME)


@router.post("/signup")
async def signup(data: dict = Body(...)):
    email: Optional[str] = data.get("email")
    username: Optional[str] = data.get("username")
    password: Optional[str] = data.get("password")
    print(email)
    return 
    if not email or not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email, username, and password are required.",
        )

    existing = await database.fetch_one(
        Auth.__table__.select().where(Auth.email == email)
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered.",
        )

    hashed = hash_password(password)

    query = Auth.__table__.insert().values(
        email=email,
        username=username,
        password=hashed,
        create_time=datetime.utcnow(),
    )
    await database.execute(query)

    return {"status": "ok", "message": "Signup successful."}


@router.post("/signin")
async def signin(response: Response, data: dict = Body(...)):
    email: Optional[str] = data.get("email")
    password: Optional[str] = data.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required.",
        )

    user = await database.fetch_one(
        Auth.__table__.select().where(Auth.email == email)
    )
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    uid = int(user["uid"])
    access_token = create_access_token(uid)
    refresh_token = create_refresh_token(uid)

    existing_token = await database.fetch_one(
        Token.__table__.select().where(Token.uid == uid)
    )
    expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    if existing_token:
        query = (
            Token.__table__
            .update()
            .where(Token.uid == uid)
            .values(
                access_token=access_token,
                refresh_token=refresh_token,
                created_at=datetime.utcnow(),
                expires_at=expires_at,
            )
        )
    else:
        query = Token.__table__.insert().values(
            uid=uid,
            access_token=access_token,
            refresh_token=refresh_token,
            created_at=datetime.utcnow(),
            expires_at=expires_at,
        )
    await database.execute(query)

    set_auth_cookies(response, access_token, refresh_token)

    return {"status": "ok", "email": user["email"], "username": user["username"]}


@router.post("/signout")
async def signout(request: Request, response: Response):
    access_token = request.cookies.get(ACCESS_COOKIE_NAME)
    uid: Optional[int] = None
    if access_token:
        try:
            uid = decode_token(access_token, expected_type="access")
        except HTTPException:
            uid = None

    if uid is not None:
        delete_q = Token.__table__.delete().where(Token.uid == uid)
        await database.execute(delete_q)

    clear_auth_cookies(response)
    return {"status": "ok", "message": "Signed out."}


@router.get("/me")
async def me(uid: int = Depends(get_current_uid)):
    user = await database.fetch_one(
        Auth.__table__.select().where(Auth.uid == uid)
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return {
        "uid": user["uid"],
        "email": user["email"],
        "username": user["username"],
        "is_active": user["is_active"],
    }
