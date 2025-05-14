from fastapi import APIRouter, Depends, status, Form
from sqlalchemy.orm import Session
from typing import Annotated
from ..dependencies import get_db, get_authenticated_user
from ..schemas.user_schemas import UserRegistrationSchema, UserProfileViewSchema, UserLoginSchema, AuthenticatedUser, UserLoginDocsSchema, UserProfileUpdateSchema
from ..schemas.auth_schemas import Token
from ..services import admin_services
from ..dependencies import is_admin_user

router = APIRouter(prefix='/admin', tags=['admin'])

@router.post('/create-admin-user', dependencies=[Depends(is_admin_user)])
def create_admin_user(session: Annotated[Session, Depends(get_db)], user: Annotated[UserRegistrationSchema, Form()]):
    return admin_services.create_admin_user(session, user)