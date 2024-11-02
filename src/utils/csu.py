import asyncio
from getpass import getpass
from models.user import User
from utils.password import hash_password
from api.v1.dependencies.database import get_db


async def console_manager() -> None:
    while True:
        username = input("Input username: ")
        if username.strip():
            break
        print("username shouldn't be empty string, try again.")  # noqa: T201

    password = getpass("Input password: ")

    await save_admin_user(username, password)
    print("Admin successfully created.")  # noqa: T201


async def save_admin_user(username: str, password: str) -> None:
    """Save cleaned data to db"""
    hashed_password = hash_password(password)
    admin_user = User(
        username=username, password=hashed_password, is_admin=True
    )
    async for db in get_db():
        db.add(admin_user)
        await db.commit()
        await db.refresh(admin_user)


if __name__ == "__main__":
    asyncio.run(console_manager())
