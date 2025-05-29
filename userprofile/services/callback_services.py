from fastapi import HTTPException, status, UploadFile
from ..schemas.user_schemas import UserObjResSchema
import requests

def notify_user_password_change(callback_url, user_data: UserObjResSchema):
    body = {
        'title': 'Password Change',
        'user': user_data.model_dump(),
    }
    res = requests.post(callback_url, json=body)
    if not res.ok:
        print('Notification sending unsuccessfull!')