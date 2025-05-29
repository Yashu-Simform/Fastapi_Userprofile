from .config.db import DBConnection
from .core.utils import decode_jwt_token
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends, HTTPException, status, Form
from .repositories import user_repo
from jwt.exceptions import InvalidTokenError
from .schemas.user_schemas import AuthenticatedUser
from sqlalchemy.orm import Session
from pydantic import EmailStr
from .models.user_models import UserBase
from fastapi.security import SecurityScopes

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="user/login",
    scopes={"user-r": "Read permission for user.", 'user-w': "Write permission for user."}
    )  

def get_db():
    mydb = DBConnection()
    session = mydb.create_session()
    yield session

    session.close()

def get_authenticated_user(session: Annotated[Session, Depends(get_db)], security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]) -> AuthenticatedUser:
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
    
    req_scopes = payload.get('scopes', [])

    # Security permission check
    for scope in security_scopes.scopes:
        if scope not in req_scopes:
            raise  HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions.",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    rawuser = user_repo.get_user(session, id=user_id)
    user = AuthenticatedUser(id=rawuser.id, email=rawuser.email, is_admin=rawuser.is_admin)
    return user

def check_permissions(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decode_jwt_token(token)
    
    req_scopes = payload.get('scopes', [])

    # Security permission check
    for scope in security_scopes.scopes:
        if scope not in req_scopes:
            raise  HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions.",
                headers={"WWW-Authenticate": "Bearer"},
            )

def is_admin_user(user: Annotated[AuthenticatedUser, Depends(get_authenticated_user)]):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not an Admin user!")
    
def get_user_email(session: Annotated[Session, Depends(get_db)], email: Annotated[EmailStr, Form()]):
    user:UserBase = user_repo.get_user(session, email=email)
    return user.email