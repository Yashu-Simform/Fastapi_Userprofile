from pydantic import BaseModel
from sqlmodel import SQLModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates
from ..core.utils import datetime_now
from datetime import datetime
from typing import Optional
import email_validator
from string import punctuation
from ..core import validators
from ..core.utils import validate_and_hash

class Base(DeclarativeBase):
    pass

class BaseModel:
    deleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime_now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime_now(), onupdate=datetime_now(), nullable=False)

    def model_to_dict(self):
        if not self:
            return None 
        
        model_dict = {
            col.key: getattr(self, col.key)
            for col in inspect(self).mapper.column_attrs
        }

        return model_dict

class UserBase(Base, BaseModel):
    __tablename__ = 'user'

    id = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(
        doc="""
        Password must contain :
            minimum 8 character,
            maxmimum 64 characters,
            at least 1 lowercase character,
            at least 1 uppercase character,
            at least 1 digit,
            at least 1 special character
            """
        )
    fname: Mapped[str] = mapped_column(nullable=True)
    lname: Mapped[str] = mapped_column(nullable=True)
    mobile_number: Mapped[str] = mapped_column(nullable=True)
    profile_img: Mapped[str] = mapped_column(nullable=True)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)

    @validates('email')
    def validate_email(self, key, value: str):
        return validators.validate_email(value)
    
    @validates('fname')
    def validate_fname(self, key, value: str):
        return validators.validate_fname(value)
    
    @validates('lname')
    def validate_lname(self, key, value: str):
        return validators.validate_lname(value)

    @validates('password')
    def validate_password(self, key, value: str):
        return validate_and_hash(value, validators.validate_password)
    
    @validates('mobile_number')
    def validate_mobile_number(self, key, value: str):
        return validators.validate_mobile_number(value)