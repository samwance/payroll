from fastapi_storages.integrations.sqlalchemy import FileType
from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, DateTime, Integer, Numeric, String
from sqlalchemy.sql import expression, func

from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    second_name: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=True)
    phone: Mapped[str] = mapped_column(String, unique=True, index=True)
    photo: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    position: Mapped[str] = mapped_column(String, nullable=False)
    salary: Mapped[float] = mapped_column(Numeric(10, 2))
    random_password: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_admin: Mapped[bool] = mapped_column(Boolean, server_default=expression.false())
