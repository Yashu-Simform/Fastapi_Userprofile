from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Dict, Any
from ..models.user_models import UserBase
from fastapi import HTTPException, status, BackgroundTasks
from ..core.utils import get_password_hash
from ..core.workers import send_email

def user_registration(session: Session, req_data: Dict[str, Any]):
    req_data['password'] = get_password_hash(req_data['password'])
    user = UserBase(**req_data)
    session.add(user)
    session.commit()

def get_user(session: Session, email: str= None, id: int = None) -> UserBase:
    if not email and not id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="No unique identification provided to get user.")
    sql = select(UserBase).where((UserBase.email == email) if email else (UserBase.id == id))
    user = session.scalar(sql)
    if not user or (user and user.deleted):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='User not found!')
    
    return user

def user_profile(session: Session, user: Dict) -> UserBase:
    user = get_user(session,id=int(user["id"]))
    return user

def user_update_profile(session: Session, updated_data: dict, id: int | None = None, email: str | None= None):
    user = get_user(session,id=id, email=email)
    
    for k, v in updated_data.items():
        if k and v and hasattr(user, k):
            setattr(user, k, v)

    session.commit()

def delete_user_account(session: Session, id: int):
    user = get_user(session,id=id)
    
    user.deleted = True
    session.commit()

    return user