from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    Security,
    status,
)
from fastapi.responses import JSONResponse
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.dependencies.database import get_db
from schemas.user import Token, UserCreateSimple, UserLogin
from utils.auth import (
    ACCESS_TOKEN_COOKIE_KEY,
    REFRESH_TOKEN_COOKIE_KEY,
    access_security,
    authenticate_username,
    set_tokens_to_cookie,
)
from crud.user import crud_user
from utils.auth import create_tokens
from utils.redis import redis_client

router = APIRouter()


@router.post(
    "/register/",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_create: UserCreateSimple, db: AsyncSession = Depends(get_db)
):
    existing_user = await crud_user.get_by_username(db, user_create.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists.",
        )

    new_user = await crud_user.create_easy(db=db, create_schema=user_create)

    tokens = await create_tokens(subject={"id": str(new_user.id)})
    response = JSONResponse(content=tokens.model_dump())
    return await set_tokens_to_cookie(response=response, tokens=tokens)


@router.post("/login/", response_model=Token)
async def login_for_access_token(
    user_login: UserLogin, db: AsyncSession = Depends(get_db)
):
    user = await authenticate_username(
        db, user_login.username, user_login.password
    )
    if isinstance(user, str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=user,
            headers={"WWW-Authenticate": "Bearer"},
        )
    tokens = await create_tokens(subject={"id": str(user.id)})
    response = JSONResponse(content=tokens.model_dump())
    return await set_tokens_to_cookie(response=response, tokens=tokens)


@router.delete("/logout/", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    user_id = credentials.subject.get("id")
    response = Response()
    response.delete_cookie(ACCESS_TOKEN_COOKIE_KEY)
    response.delete_cookie(REFRESH_TOKEN_COOKIE_KEY)
    redis_client.delete_refresh_token(user_id)
