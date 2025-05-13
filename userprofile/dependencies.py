from .config.db import DBConnection
from .core.utils import decode_jwt_token
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends, HTTPException, status
from .repositories import user_repo
from jwt.exceptions import InvalidTokenError
from .schemas.user_schemas import AuthenticatedUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")  

def get_db():
    mydb = DBConnection()
    session = mydb.create_session()
    yield session

    session.close()

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    payload = decode_jwt_token(token)
    email = payload.get('email')
    user_repo.get_user(email)
    return email

def get_authenticated_user(token: Annotated[str, Depends(oauth2_scheme)]) -> AuthenticatedUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_jwt_token(token)
        user_id = payload.get('id')
        if not user_id:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    rawuser = user_repo.get_user(id=user_id)
    user = AuthenticatedUser(id=rawuser.id, email=rawuser.email)
    return user
