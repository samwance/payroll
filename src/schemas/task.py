from datetime import datetime
from pydantic import BaseModel
from typing import TYPE_CHECKING, Optional, List


if TYPE_CHECKING:
    from schemas.user import UserSimpleResponse


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    priority: Optional[int] = None
    deadline: Optional[datetime] = None
    assignee_id: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None
    deadline: Optional[datetime] = None


class TaskResponseSimple(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: Optional[int]
    deadline: Optional[datetime] = None
    creator_id: int
    assignee_id: int


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: Optional[int]
    deadline: Optional[datetime] = None
    creator_id: int
    assignee_id: int
    assignee: Optional["UserSimpleResponse"]

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    tasks: Optional[List[TaskResponse]] = []
