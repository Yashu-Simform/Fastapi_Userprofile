from sqlalchemy.orm import Session
from ..schemas.user_schemas import UserProfileImgPath, UserRegistrationSchema, UserProfileViewSchema, UserLoginSchema, AuthenticatedUser, UserProfileUpdateSchema, UserAccountDeleteResSchema, UserPasswordResetReqSchema
from ..schemas.auth_schemas import Token, PayloadSchema
from ..repositories import user_repo
from ..core.utils import get_password_hash, verify_password, create_jwt_token
from fastapi import HTTPException, status, UploadFile
from pydantic import EmailStr, FilePath
from ..models.user_models import UserBase
from ..core.workers import send_email

def user_registration(session: Session, user: UserRegistrationSchema):
    req_data = user.model_dump()
    user_repo.user_registration(session, req_data)

def user_profile_view(session: Session, user: AuthenticatedUser) -> UserProfileViewSchema:
    user_profile = user_repo.user_profile(session, user.model_dump())
    return UserProfileViewSchema(**(user_profile.model_to_dict()))

def user_login(session: Session, credentials: UserLoginSchema) -> Token:
    user = user_repo.get_user(session, email=credentials.email)
    payload = PayloadSchema(id=user.id, scopes=credentials.scopes.split(sep=' '))
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

    return user_repo.user_update_profile(session, updated_fields_only, id=user.id)

def delete_user_account(session: Session, id: int) -> UserAccountDeleteResSchema:
    user_acc_deleted = user_repo.delete_user_account(session, id)
    return user_acc_deleted

def user_forgot_password(email: str):
    pass_reset_url = 'http://127.0.0.1:8000/docs#/users/password_reset_user_reset_password_post'
    subject = 'Account Recovery!'
    recipients = [email]
    body = f'<p>Go to this url to reset password: <br><a href="{pass_reset_url}">Reset Password</a></p>'
    send_email.delay(subject, recipients, body)

def user_reset_password(session: Session, req_data: UserPasswordResetReqSchema):
    data = req_data.model_dump()
    email = data.pop('email')
    user_repo.user_update_profile(session, data, email=email)

def user_profile_img_upload(session: Session, img: UploadFile, user: AuthenticatedUser):
    
    img_path = f'data/user/profile_images/{img.filename}'

    with open(img_path, 'wb') as f:
        f.write(img.file.read())

    # Serializing and validating img file path
    user_profile_img = UserProfileImgPath(img_path=img_path)

    saved_img_path = user_repo.user_profile_img_upload(session, user_profile_img.img_path.as_posix(), user.id)

    print(saved_img_path)