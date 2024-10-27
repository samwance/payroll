import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from crud.user import crud_user
from models.user import User
from schemas.user import UserCreateDB
from utils.password import hash_password

@pytest_asyncio.fixture
async def user_fixture(async_session: AsyncSession) -> User:
    
    schema = UserCreateDB(
        name='name',
        second_name="User",
        surname='Another',
        phone='12345678',
        position='jun',
        password=hash_password("password123"),
        random_password='password123',
        salary=0,
    )
    
    new_user = await crud_user.create(db=async_session, create_schema=schema)
    return new_user

@pytest_asyncio.fixture
async def user_fixture_2(async_session: AsyncSession) -> User:
    schema = UserCreateDB(
        name="Another_user",
        second_name="User",
        surname='Another',
        phone="12345679",
        position='jun',
        password=hash_password("password123"),
        random_password='password123',
        salary=0,
    )
    
    new_user = await crud_user.create(db=async_session, create_schema=schema)
    return new_user
