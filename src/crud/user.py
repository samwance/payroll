from typing import Generic, Optional, TypeVar
from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models.user import User
from utils.password import hash_password

CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")
ModelType = TypeVar("ModelType")

class CRUDUser(Generic[CreateSchemaType, ModelType]):
    def __init__(self, model):
        self.model = model

    async def create(
        self,
        db: AsyncSession,
        *,
        create_schema: CreateSchemaType,
        password: str,
        commit: bool = True,
    ) -> ModelType:
        data = create_schema.model_dump(exclude_unset=True)
        data['password'] = hash_password(password)
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await db.execute(stmt)
        obj = res.scalars().first()
        if commit:
            await db.commit()
            await db.refresh(obj)
        return obj 
    
    async def create_easy(
        self,
        db: AsyncSession,
        *,
        create_schema: CreateSchemaType,
        commit: bool = True,
    ) -> ModelType:
        data = create_schema.model_dump(exclude_unset=True)
        data['password'] = hash_password(data['password'])
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await db.execute(stmt)
        obj = res.scalars().first()
        if commit:
            await db.commit()
            await db.refresh(obj)
        return obj 

    async def update(
        self,
        db: AsyncSession,
        user_id: int,
        update_schema: UpdateSchemaType,
        commit: bool = True,
    ) -> ModelType:
        existing_user = await self.get_user(db, user_id)
        if not existing_user:
            return None
        
        update_data = update_schema.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["password"] = hash_password(update_data["password"])
        
        stmt = (
            update(self.model)
            .where(self.model.id == user_id)
            .values(**update_data)
            .returning(self.model)
        )
        res = await db.execute(stmt)
        obj = res.scalars().first()

        if commit:
            await db.commit()
            await db.refresh(obj)

        return obj

    async def get_by_phone(self, db: AsyncSession, phone: str) -> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.phone == phone))
        return result.scalar_one_or_none()
    
    async def get_by_username(self, db: AsyncSession, username: str) -> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.username == username))
        return result.scalar_one_or_none()

    async def get_user(self, db: AsyncSession, user_id: int):
        result = await db.execute(
            select(User)
            .options(selectinload(User.assigned_tasks)) 
            .where(User.id == user_id)
        )
        return result.scalars().first()

    async def get_users(self, db: AsyncSession):
        result = await db.execute(select(User).options(selectinload(User.assigned_tasks)).where(User.is_admin != True))
        return result.scalars().all()

crud_user = CRUDUser(User)
