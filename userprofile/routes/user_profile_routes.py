from fastapi import APIRouter, Depends, status, Form, Security, UploadFile, BackgroundTasks, Body
from fastapi.requests import Request
from sqlalchemy.orm import Session
from typing import Annotated, Union
from ..dependencies import get_db, get_authenticated_user, is_admin_user, get_user_email
from ..schemas.user_schemas import NotifyData, UserRegistrationSchema, UserProfileViewSchema, UserLoginSchema, AuthenticatedUser, UserLoginDocsSchema, UserProfileUpdateSchema, UserPasswordResetReqSchema
from ..schemas.auth_schemas import Token
from ..services import user_services, callback_services
from ..core.workers import send_email
from fastapi.responses import JSONResponse, FileResponse
from pydantic import HttpUrl

router = APIRouter(prefix='/user', tags=['users'])

@router.post('/registration', status_code=status.HTTP_201_CREATED)
def user_registration(session: Annotated[Session, Depends(get_db)], user: Annotated[UserRegistrationSchema, Form()]):
    return user_services.user_registration(session, user)

@router.get('/view-profile')
def user_profile_view(session: Annotated[Session, Depends(get_db)], user: Annotated[AuthenticatedUser, Security(get_authenticated_user, scopes=['user-r'])]) -> UserProfileViewSchema:
    return user_services.user_profile_view(session, user) 

@router.post('/login')
def user_login(session: Annotated[Session, Depends(get_db, use_cache=False)], credentials: Annotated[UserLoginDocsSchema, Form()]) -> Token:
    my_credentials = UserLoginSchema(email=credentials.username, password=credentials.password, scopes=credentials.scope)
    return user_services.user_login(session, my_credentials)

@router.get('/authenticate-user')
def get_auth_user(user: Annotated[AuthenticatedUser, Security(get_authenticated_user, scopes=['user-r'])]):
    # user_services
    return user

@router.patch('/update-profile', status_code=status.HTTP_200_OK)
def user_profile_update(session: Annotated[Session, Depends(get_db)], user: Annotated[AuthenticatedUser, Security(get_authenticated_user, scopes=['user-r', 'user-w'])], updated_data: Annotated[UserProfileUpdateSchema, Form()]):
    return user_services.user_profile_update(session, user, updated_data)

@router.delete('/delete-account', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(is_admin_user)])
def delete_user_account(session: Annotated[Session, Depends(get_db)], id: int):
    user_acc_deleted = user_services.delete_user_account(session, id)
    
    subject = 'Your account has been deleted!'
    recipients = [user_acc_deleted.email]
    body = """<p>You account has been Deleted!</p>"""
    send_email.delay(subject, recipients, body)

@router.patch('/account-recovery', status_code=status.HTTP_200_OK)
def user_forgot_password(email: Annotated[str, Depends(get_user_email, use_cache=True)]):
    user_services.user_forgot_password(email)

@router.post('/reset-password', name='password_reset')
def user_reset_password(session: Annotated[Session, Depends(get_db)], req_data: Annotated[UserPasswordResetReqSchema, Form()], background_task: BackgroundTasks, callback_url: Union[HttpUrl, None] = None):
    user_data = user_services.user_reset_password(session, req_data)
    if callback_url:
        background_task.add_task(callback_services.notify_user_password_change, callback_url, user_data)
    return JSONResponse(content={'status': 'success', 'message': 'Password Reset Successfully!'})

@router.get('/download-car-img')
def download_car_image():
    return FileResponse('userprofile/static/car.jpg', media_type='application/octet-stream',filename='car.jpg')

@router.post('/upload/profile-img')
def user_profile_img_upload(session: Annotated[Session, Depends(get_db)], img: UploadFile, user: Annotated[AuthenticatedUser, Security(get_authenticated_user, scopes=['user-r', 'user-w'])]):
    user_services.user_profile_img_upload(session, img, user)
    return JSONResponse(content={"data": f"Flie {img.filename} uploaded successfully!"}, status_code=status.HTTP_200_OK)

@router.get('/get-profile-img')
def get_user_profile_img(session: Annotated[Session, Depends(get_db)], user: Annotated[AuthenticatedUser, Security(get_authenticated_user, scopes=['user-r'])]):
    img_path = user_services.get_user_profile_img(session, user)
    if not img_path:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "success", "message": "No profile image uploaded!"})
    return FileResponse(img_path)

@router.post('/dummy-callback-url')
def dummy_callback_url(body: Annotated[NotifyData, Body()]):
    print(body.title)