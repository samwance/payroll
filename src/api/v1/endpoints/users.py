from typing import Union
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.v1.dependencies.database import get_current_user, get_db
from models.user import User
from schemas.user import UserCreate, UserCreateResponse, UserFullResponse, UserListResponse, UserResponse, UserUpdate
from crud.user import crud_user
from utils.password import generate_random_password
from utils.email import send_password_email

router = APIRouter()

@router.post(
    "/",
    response_model=UserCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    create_data: UserCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Only admin can create new users!",
        )
    user = await crud_user.get_by_phone(db, create_data.phone)
    if user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User already exists!")
    password = generate_random_password() 
    user = await crud_user.create(db=db, create_schema=create_data, password=password)
    await send_password_email(create_data.email, password)
    return user


@router.get("/users/", response_model=UserListResponse)
async def list_users(db: AsyncSession = Depends(get_db)):
    return {"users": await crud_user.get_users(db)}

@router.get("/profile/", response_model=UserFullResponse)
async def get_user(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user = await crud_user.get_user(db, current_user.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/users/{user_id}/", response_model=Union[UserResponse, UserFullResponse])
async def get_user(user_id: int, current_user: User = Depends(get_current_user),  db: AsyncSession = Depends(get_db)):
    user = await crud_user.get_user(db, user_id)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if current_user.is_admin:
        return UserFullResponse.from_orm(user)
    else:
        return UserResponse.from_orm(user) 

@router.put("/users/", response_model=UserResponse)
async def update_user(update_data: UserUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud_user.update(db=db, user_id=current_user.id, update_schema=update_data)
