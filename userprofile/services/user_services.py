from sqlalchemy.orm import Session
from ..schemas.user_schemas import UserRegistrationSchema, UserProfileViewSchema, UserLoginSchema
from ..schemas.auth_schemas import Token
from ..repositories import user_repo
from ..core.utils import get_password_hash, verify_password, create_jwt_token

def user_registration(session: Session, user: UserRegistrationSchema):
    user.password = get_password_hash(user.password)
    req_data = user.model_dump()
    user_repo.user_registration(session, req_data)

def user_profile_view(session: Session, user: UserLoginSchema) -> UserProfileViewSchema:
    user_profile = user_repo.user_profile(session, user.model_dump())
    return UserProfileViewSchema(**user_profile)

def user_login(session: Session, credentials: UserLoginSchema):
    user = user_repo.get_user(session, email=credentials.email)
    payload = {'id': user.id}
    if verify_password(credentials.password, user.password):
        access_token = create_jwt_token(payload)

    return Token(access_token=access_token, token_type='bearer')