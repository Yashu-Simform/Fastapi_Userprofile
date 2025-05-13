from pydantic import BaseModel
from sqlmodel import SQLModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates
from ..core.utils import datetime_now
from datetime import datetime
from typing import Optional
import email_validator
from string import punctuation

class Base(DeclarativeBase):
    pass

class BaseModel:
    deleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime_now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime_now(), onupdate=datetime_now(), nullable=False)

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
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)

    @validates('email')
    def validate_email(self, key, value: str):
        return email_validator.validate_email(value).email
    
    @validates('fname')
    def validate_fname(self, key, value: str):

        if not value:
            return value

        if not value.isalpha():
            raise ValueError('Invalid input! Fname must only contains alphabets.')
        
        return value
    
    @validates('lname')
    def validate_lname(self, key, value: str):

        if not value:
            return value

        if not value.isalpha():
            raise ValueError('Invalid input! Lname must only contains alphabets.')
        
        return value

    @validates('password')
    def validate_password(self, key, value: str):
        if len(value) < 8:
            raise ValueError('Invalid Password! Password must contains at least 8 characters.')
        
        if len(value) > 64:
            raise ValueError('Invalid Password! Password must contains at max 64 characters.')
        
        has_lowercase = False
        has_uppercase = False
        has_digit = False
        has_special_char = False

        for c in value:
            if c.isalpha():
                if c.islower():
                    has_lowercase = True
                if c.isupper():
                    has_uppercase = True

            if c.isdigit():
                has_digit = True

            if c in punctuation:
                has_special_char = True

        if not (has_lowercase and has_uppercase and has_digit and has_special_char):
            raise ValueError('Invalid Password! Password must contain at least 1 lowercase, 1 uppercase, 1 digit and 1 special character.')
        
        return value
    
    @validates('mobile_number')
    def validate_mobile_number(self, key, value: str):

        if not value:
            return value

        if not value.isdigit():
            raise ValueError('Invalid input! Mobile number must only contain digits.')
        
        if len(value) != 10:
            raise ValueError('Invalid input. Mobile number must be of 10 digits.')
        
        return value