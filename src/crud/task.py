from typing import Generic, Optional, TypeVar
from sqlalchemy import insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from models.task import Task

CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")
ModelType = TypeVar("ModelType")

class CRUDTask(Generic[CreateSchemaType, ModelType]):
    def __init__(self, model):
        self.model = model

    async def create(
        self,
        db: AsyncSession,
        *,
        create_schema: CreateSchemaType,
        creator_id: int,
        commit: bool = True,
    ) -> ModelType:
        data = create_schema.model_dump(exclude_unset=True)
        data['creator_id'] = creator_id
        if not data['assignee_id']:
            data['assignee_id'] = creator_id
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
        task_id: int,
        update_schema: UpdateSchemaType,
        commit: bool = True,
    ) -> ModelType:
        existing_task = await self.get_task(db, task_id)
        if not existing_task:
            return None
        
        update_data = update_schema.model_dump(exclude_unset=True)
        
        stmt = (
            update(self.model)
            .where(self.model.id == task_id)
            .values(**update_data)
            .returning(self.model)
        )
        res = await db.execute(stmt)
        obj = res.scalars().first()

        if commit:
            await db.commit()
            await db.refresh(obj)

        return obj

    async def get_task(self, db: AsyncSession, task_id: int) -> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.id == task_id))
        return result.scalar_one_or_none()

    async def get_tasks(self, db: AsyncSession):
        result = await db.execute(select(self.model).options(selectinload(Task.assignee)))
        return result.scalars().all()

    async def delete(self, db: AsyncSession, task_id: int) -> bool:
        stmt = delete(self.model).where(self.model.id == task_id)
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount > 0
    
crud_task = CRUDTask(Task)
