from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

class UserBase(BaseModel):
    second_name: str
    name: str
    surname: str
    phone: str
    position: str
    photo: Optional[str] = None

class UserCreate(UserBase):
    salary: float

    class Config:
        from_attributes = True

class UserCreateDB(UserBase):
    password: str
    salary: float

class UserCreateResponse(UserBase):
    id: int
    registered_at: datetime
    updated_at: datetime
    is_admin: bool
    random_password: str
    salary: float

class UserFullResponse(UserBase):
    id: int
    registered_at: datetime
    updated_at: datetime
    is_admin: bool
    salary: float

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: int
    registered_at: datetime
    updated_at: datetime
    is_admin: bool

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    second_name: str = None
    name: str = None
    surname: str = None
    phone: str = None
    password: Optional[str] = None

class UserListResponse(BaseModel):
    users: List[UserResponse]

class UserLogin(BaseModel):
    phone: str
    password: str

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