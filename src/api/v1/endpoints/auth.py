from fastapi import APIRouter, Depends, HTTPException, Response, Security, status
from fastapi.responses import JSONResponse
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.dependencies.database import get_db
from schemas.user import Token, UserLogin
from utils.auth import ACCESS_TOKEN_COOKIE_KEY, REFRESH_TOKEN_COOKIE_KEY, access_security, authenticate_user, set_tokens_to_cookie
from crud.user import crud_user
from utils.auth import create_tokens

router = APIRouter()

@router.post("/login/", response_model=Token)
async def login_for_access_token(
    user_login: UserLogin, db: AsyncSession = Depends(get_db)
    ):
    user = await authenticate_user(db, user_login.phone, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    tokens = await create_tokens(subject={"id": str(user.id)})
    response = JSONResponse(content=tokens.model_dump())
    return await set_tokens_to_cookie(response=response, tokens=tokens)

@router.delete("/logout/", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    response = Response()
    response.delete_cookie(ACCESS_TOKEN_COOKIE_KEY)
    response.delete_cookie(REFRESH_TOKEN_COOKIE_KEY)
    return None
