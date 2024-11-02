from datetime import datetime, timedelta, UTC
from httpx import AsyncClient
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from models.task import Task
from models.user import User
from schemas.task import TaskCreate
from crud.task import crud_task


@pytest_asyncio.fixture
async def task_fixture(
    http_client: AsyncClient, user_fixture: User, async_session: AsyncSession
) -> Task:
    new_task_data = TaskCreate(
        title="Sample Task",
        description="This is a sample task.",
        status="pending",
        priority=1,
        deadline=datetime.now(UTC) + timedelta(days=7),
        assignee_id=user_fixture.id,
    )

    created_task = await crud_task.create(
        db=async_session,
        create_schema=new_task_data,
        creator_id=user_fixture.id,
    )

    return created_task
