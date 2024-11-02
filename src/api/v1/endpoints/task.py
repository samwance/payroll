from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.v1.dependencies.database import get_current_user, get_db
from models.task import Task
from models.user import User
from schemas.task import TaskCreate, TaskResponse, TaskListResponse, TaskResponseSimple, TaskUpdate
from crud.task import crud_task

router = APIRouter()

@router.post(
    "/",
    response_model=TaskResponseSimple,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    create_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    task = await crud_task.create(db=db, create_schema=create_data, creator_id=current_user.id)
    return task

@router.get("/", response_model=TaskListResponse)
async def list_tasks(db: AsyncSession = Depends(get_db)):
    return {"tasks": await crud_task.get_tasks(db)}

@router.get("/{task_id}/", response_model=TaskResponse)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await crud_task.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.patch("/{task_id}/", response_model=TaskResponse)
async def update_task(
    task_id: int,
    update_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    task = await crud_task.update(db=db, task_id=task_id, update_schema=update_data)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.delete("/{task_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    task = await crud_task.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if not task.creator == current_user and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You dont have right to delete this task")
    await crud_task.delete(db=db, task_id=task_id)
