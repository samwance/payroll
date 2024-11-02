from typing import AsyncGenerator
from fastapi import Depends, HTTPException, Security, status
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import SessionLocal
from fastapi_jwt import JwtAuthorizationCredentials
from models.user import User
from schemas.user import TokenPayload
from crud.user import crud_user
from utils.tokens import access_security

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def get_current_user(
    credentials: JwtAuthorizationCredentials = Security(access_security),
    db: AsyncSession = Depends(get_db),
) -> User:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    try:
        token_user = TokenPayload(**credentials.subject)
    except (JWTError, ValidationError) as ex:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from ex
    return await crud_user.get_user(db=db, user_id=token_user.id)
