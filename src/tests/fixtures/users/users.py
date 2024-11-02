import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from utils.password import hash_password


@pytest_asyncio.fixture
async def user_fixture(async_session: AsyncSession) -> User:
    user = User(
        name="name",
        username="test",
        second_name="User",
        surname="Another",
        phone="12345678",
        position="jun",
        password=hash_password("password123"),
        salary=0,
        email="test@test.com",
        is_admin=True,
    )

    async_session.add(user)
    await async_session.commit()

    await async_session.refresh(user)

    return user


@pytest_asyncio.fixture
async def user_fixture_2(async_session: AsyncSession) -> User:
    user = User(
        name="Another_user",
        username="test2",
        second_name="User",
        surname="Another",
        phone="12345679",
        position="jun",
        password=hash_password("password123"),
        salary=0,
        email="test2@test.com",
    )

    async_session.add(user)
    await async_session.commit()

    await async_session.refresh(user)

    return user
