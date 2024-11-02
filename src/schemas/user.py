from datetime import datetime
from typing import Optional, List, Union

from pydantic import BaseModel, Field

from schemas.task import TaskListResponse, TaskResponse

class UserBase(BaseModel):
    second_name: Optional[str]
    name: Optional[str]
    surname: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    position: Optional[str]
    username: Optional[str]
    photo: Optional[str] = None

class UserCreate(UserBase):
    salary: float

    class Config:
        from_attributes = True

class UserCreateSimple(BaseModel):
    username: str
    password: str

class UserCreateDB(UserBase):
    password: str
    salary: float

class UserCreateResponse(UserBase):
    id: int
    registered_at: datetime
    updated_at: datetime
    is_admin: bool
    salary: float

class UserFullResponse(UserBase):
    id: int
    registered_at: datetime
    updated_at: datetime
    is_admin: bool
    salary: float
    assigned_tasks: Union[TaskListResponse, List[TaskResponse]]

    class Config:
        from_attributes = True

class UserSimpleResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: int
    registered_at: datetime
    updated_at: datetime
    is_admin: bool
    assigned_tasks: Union[TaskListResponse, List[TaskResponse]]

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    second_name: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    username: Optional[str] = None

class UserListResponse(BaseModel):
    users: List[UserResponse]

class UserLogin(BaseModel):
    password: str
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class TokenPayload(BaseModel):
    id: int

class TokenAccessRefresh(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str