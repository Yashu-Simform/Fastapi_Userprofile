from fastapi import APIRouter, Depends, status, Form
from sqlalchemy.orm import Session
from typing import Annotated
from ..dependencies import get_db, get_authenticated_user, is_admin_user
from ..schemas.user_schemas import UserRegistrationSchema, UserProfileViewSchema, UserLoginSchema, AuthenticatedUser, UserLoginDocsSchema, UserProfileUpdateSchema
from ..schemas.auth_schemas import Token
from ..services import user_services

router = APIRouter(prefix='/user', tags=['users'])

@router.post('/registration', status_code=status.HTTP_201_CREATED)
def user_registration(session: Annotated[Session, Depends(get_db)], user: Annotated[UserRegistrationSchema, Form()]):
    return user_services.user_registration(session, user)

@router.get('/view-profile')
def user_profile_view(session: Annotated[Session, Depends(get_db)], user: Annotated[AuthenticatedUser, Depends(get_authenticated_user)]) -> UserProfileViewSchema:
    return user_services.user_profile_view(session, user) 

@router.post('/login')
def user_login(session: Annotated[Session, Depends(get_db, use_cache=False)], credentials: Annotated[UserLoginDocsSchema, Form()]) -> Token:
    
    my_credentials = UserLoginSchema(email=credentials.username, password=credentials.password)
    return user_services.user_login(session, my_credentials)

@router.patch('/update-profile', status_code=status.HTTP_200_OK)
def user_profile_update(session: Annotated[Session, Depends(get_db)], user: Annotated[AuthenticatedUser, Depends(get_authenticated_user)], updated_data: Annotated[UserProfileUpdateSchema, Form()]):
    return user_services.user_profile_update(session, user, updated_data)

@router.delete('/delete-account', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(is_admin_user)])
def delete_user_account(session: Annotated[Session, Depends(get_db)], id: int):
    return user_services.delete_user_account(session, id)