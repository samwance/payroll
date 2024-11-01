from fastapi_storages.integrations.sqlalchemy import FileType
from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, DateTime, Integer, Numeric, String
from sqlalchemy.sql import expression, func

from models.base import Base
from models.task import Task
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=True, index=True)
    second_name: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    surname: Mapped[str] = mapped_column(String, nullable=True)
    phone: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=True)
    photo: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    position: Mapped[str] = mapped_column(String, nullable=True)
    salary: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    password: Mapped[str] = mapped_column(String)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_admin: Mapped[bool] = mapped_column(Boolean, server_default=expression.false())
    created_tasks: Mapped[list["Task"]] = relationship("Task", foreign_keys="Task.creator_id", back_populates="creator")
    assigned_tasks: Mapped[list["Task"]] = relationship("Task", foreign_keys="Task.assignee_id", back_populates="assignee")
