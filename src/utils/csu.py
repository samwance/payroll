from fastapi import Depends
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from api.v1.dependencies.database import get_db
from utils.password import hash_password


async def create_admin_user(db: AsyncSession = Depends(get_db)):
    password = 'password'
    hashed_password = hash_password(password)

    admin_user = User(
        name='accountant',
        second_name='accountant',
        surname='accountant',
        position='accountant',
        email="admin@admin.com",
        salary=0,
        phone='12345678',
        password=hashed_password,
        is_admin=True
    )
    db.add(admin_user)
    await db.commit()
    await db.refresh(admin_user)
    return admin_user
