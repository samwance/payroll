import sys
from typing import Callable, Generator

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from database.database import engine
from main import create_app
from models.user import User
from models.base import Base
from utils.password import hash_password
from utils.tokens import access_security

from .fixtures import * 

@pytest_asyncio.fixture
async def async_session() -> AsyncSession:
    session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with session() as s:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield s

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()

@pytest_asyncio.fixture
async def http_client(
    async_session: AsyncSession,
) -> Generator[AsyncClient, None, None]:
    test_app = create_app()
    async with (
        AsyncClient(app=test_app, base_url="http://0.0.0.0:8000") as ac,
    ):
        yield ac

@pytest_asyncio.fixture
async def get_auth_headers() -> Callable:
    async def _get_auth_headers(user: User) -> dict:
        subject = {"id": str(user.id)}
        access_token = access_security.create_access_token(subject=subject)
        headers = {"Authorization": f"Bearer {access_token}"}
        return headers

    return _get_auth_headers
