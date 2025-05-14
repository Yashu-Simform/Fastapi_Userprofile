from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Dict, Any
from ..models.user_models import UserBase
from fastapi import HTTPException, status
from ..core.utils import get_password_hash

def create_admin_user(session: Session, req_data: Dict[str, Any]):
    req_data['password'] = get_password_hash(req_data['password'])
    req_data['is_admin'] = True
    user = UserBase(**req_data)
    session.add(user)
    session.commit()