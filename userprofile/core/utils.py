from datetime import datetime, timedelta
import pytz
import jwt
from passlib.context import CryptContext
import os
from typing import Callable
import requests
from ..schemas.auth_schemas import PayloadSchema
from ..config.env_init import EnvConfig

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
env_config = EnvConfig()

def datetime_now(tz_name = 'Asia/Kolkata'):
    tz = pytz.timezone(tz_name)
    return datetime.now(tz)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(payload: PayloadSchema) -> str:
    SECRET_KEY = env_config.get_envvar('SECRET_KEY')
    JWT_HASHING_ALGORITHM = env_config.get_envvar('JWT_HASHING_ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES = env_config.get_envvar('ACCESS_TOKEN_EXPIRE_MINUTES')
    
    token_exp = datetime_now() + timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))

    payload_with_token_exp = payload.model_dump()
    payload_with_token_exp.update({'exp': token_exp})
    token = jwt.encode(payload_with_token_exp, SECRET_KEY, JWT_HASHING_ALGORITHM)

    return token

def decode_jwt_token(token: str) -> dict:
    SECRET_KEY = env_config.get_envvar('SECRET_KEY')
    JWT_HASHING_ALGORITHM = env_config.get_envvar('JWT_HASHING_ALGORITHM')
    payload = jwt.decode(token, SECRET_KEY, JWT_HASHING_ALGORITHM)
    return payload

def validate_and_hash(value, validator: Callable) -> str:
    validated_value = validator(value)
    return pwd_context.hash(validated_value)

def get_random_password():
    api_url = 'https://password.ninja/api/password'
    response = requests.get(api_url)
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)