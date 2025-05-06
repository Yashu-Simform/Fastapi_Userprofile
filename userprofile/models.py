from pydantic import BaseModel
from sqlmodel import SQLModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

Base = declarative_base()

class UserProfile(Base):
    __tablename__ = 'user_profile'

    id = Column(Integer, primary_key=True)
    fname = Column(String(255))
    lname = Column(String(255))
    profile_img = Column()

    # for developer purpose
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())