from datetime import datetime, timedelta, timezone
from typing import Optional, TypeVar
from fastapi import Response
from jose import jwt

from schemas.user import TokenAccessRefresh, TokenPayload
from utils.password import verify_password
from config.config import jwt_settings
from crud.user import crud_user
from utils.tokens import access_security, refresh_security

ResponseT = TypeVar("ResponseT", bound=Response)

ACCESS_TOKEN_COOKIE_KEY = "access_token_cookie"
REFRESH_TOKEN_COOKIE_KEY = "refresh_token_cookie"

async def create_tokens(subject: TokenPayload) -> TokenAccessRefresh:
    access_token = await create_access_token(subject)
    refresh_token = await create_refresh_token(subject)
    return TokenAccessRefresh(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )

async def create_access_token(subject: TokenPayload) -> str:
    return access_security.create_access_token(subject=subject)

async def create_refresh_token(subject: TokenPayload) -> str:
    return refresh_security.create_refresh_token(
        subject=subject,
        expires_delta=timedelta(
            minutes=jwt_settings.JWT_REFRESH_TOKEN_EXPIRES
        ),
    )

async def set_tokens_to_cookie(
    response: ResponseT, tokens: TokenAccessRefresh
) -> ResponseT:
    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE_KEY,
        value=tokens.access_token,
        secure=True,
        httponly=True,
    )
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_KEY,
        value=tokens.refresh_token,
        secure=True,
        httponly=True,
    )
    return response


async def authenticate_user(db, phone: str, password: str):
    user = await crud_user.get_by_phone(db, phone)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
    