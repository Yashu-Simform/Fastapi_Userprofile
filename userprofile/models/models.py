from pydantic import BaseModel
from sqlmodel import SQLModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from typing import Optional
from email_validator import validate_email

class Base(DeclarativeBase):
    pass

class BaseModel:
    created_at: Mapped[datetime] = mapped_column(insert_default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(insert_default=datetime.now())

class UserBase(Base, BaseModel):
    __tablename__ = 'user'

    id = mapped_column(Integer, primary_key=True)
    username: Mapped[str]
    email: Mapped[str]
    fname: Mapped[Optional[str]]
    lname: Mapped[Optional[str]]
    # profile_img = Column()