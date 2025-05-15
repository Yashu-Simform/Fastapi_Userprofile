from celery.app import Celery
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from dotenv import load_dotenv, get_key
from typing import List
from pydantic import EmailStr
from fastapi import status
from fastapi.responses import JSONResponse
import asyncio

load_dotenv()

CELERY_BROKER_URL = get_key('.env', 'CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = get_key('.env', 'CELERY_RESULT_BACKEND')

print('\n\n---------------name: ', __name__)

celery = Celery(__name__, broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@celery.task(name="send_mail")
def send_email(subject: str, recipients: List[EmailStr], body: str) -> JSONResponse:
    
    mail_conf = ConnectionConfig(
        MAIL_USERNAME = get_key('.env', 'EMAIL_HOST_USER'),
        MAIL_FROM = get_key('.env', 'EMAIL_HOST_USER'),
        MAIL_PASSWORD = get_key('.env', 'EMAIL_HOST_PASSWORD'),
        MAIL_PORT = get_key('.env', 'EMAIL_PORT'),
        MAIL_SERVER = get_key('.env', 'EMAIL_HOST'),
        MAIL_SSL_TLS = True,
        MAIL_STARTTLS = False
    )
    
    mailer = FastMail(mail_conf)

    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=MessageType.html
    )

    asyncio.run(mailer.send_message(message))