from sqlalchemy.orm import Session
from ..schemas.user_schemas import UserRegistrationSchema, UserProfileViewSchema, UserLoginSchema, AuthenticatedUser, UserProfileUpdateSchema
from ..schemas.auth_schemas import Token
from ..repositories import user_repo
from ..core.utils import get_password_hash, verify_password, create_jwt_token
from fastapi import HTTPException, status

def user_registration(session: Session, user: UserRegistrationSchema):
    req_data = user.model_dump()
    user_repo.user_registration(session, req_data)

def user_profile_view(session: Session, user: AuthenticatedUser) -> UserProfileViewSchema:
    user_profile = user_repo.user_profile(session, user.model_dump())
    return UserProfileViewSchema(**(user_profile.model_to_dict()))

def user_login(session: Session, credentials: UserLoginSchema) -> Token:
    user = user_repo.get_user(session, email=credentials.email)
    payload = {'id': user.id}
    if verify_password(credentials.password, user.password):
        access_token = create_jwt_token(payload)
        return Token(access_token=access_token, token_type='bearer')
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

def user_profile_update(session: Session, user: AuthenticatedUser, updated_data: UserProfileUpdateSchema):
    updated_data_dict = updated_data.model_dump()

    updated_fields_only = {k:v for k, v in updated_data_dict.items() if v}

    return user_repo.user_update_profile(session, user.id, updated_fields_only)

def delete_user_account(session: Session, id: int):
    return user_repo.delete_user_account(session, id)