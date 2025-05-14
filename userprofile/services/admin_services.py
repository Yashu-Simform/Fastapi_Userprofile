from sqlalchemy.orm import Session
from ..schemas.user_schemas import UserRegistrationSchema, UserProfileViewSchema, UserLoginSchema, AuthenticatedUser, UserProfileUpdateSchema
from ..schemas.auth_schemas import Token
from ..repositories import admin_repo
from ..core.utils import get_password_hash, verify_password, create_jwt_token
from fastapi import HTTPException, status

def create_admin_user(session: Session, user: UserRegistrationSchema):
    req_data = user.model_dump()
    admin_repo.create_admin_user(session, req_data)