from pydantic import BaseModel, EmailStr, SecretStr, field_validator, Field, model_validator, FilePath
from typing import Annotated, ClassVar
from ..core import validators
from ..core.utils import get_password_hash, validate_and_hash


class UserBaseSchema(BaseModel):
    email: EmailStr
    password: str


# Request Schemas
class UserBaseReqSchema(UserBaseSchema):
    @field_validator('password', check_fields=False)
    @classmethod
    def validate_password(cls, value: str):
        return validators.validate_password(value)
    
class UserProfileReqSchema(UserBaseReqSchema):
    fname: str | None = None
    lname: str | None = None
    mobile_number: str | None = None
    
    @field_validator('fname')
    @classmethod
    def validate_fname(cls, value: str):
        return validators.validate_fname(value)
    
    @field_validator('lname')
    @classmethod
    def validate_lname(cls, value: str):
        return validators.validate_lname(value)

    @field_validator('mobile_number')
    @classmethod
    def validate_mobile_number(cls, value: str):
        return validators.validate_mobile_number(value)

class UserRegistrationSchema(UserProfileReqSchema):
    pass

class UserLoginDocsSchema(UserBaseReqSchema):
    username: EmailStr
    email: ClassVar[str] = Field(default= 'user@example.com', exclude=True)
    scope: str = ''

class UserLoginSchema(UserBaseReqSchema):
    scopes: str = ''

class UserProfileUpdateSchema(UserProfileReqSchema):
    email: EmailStr | None = None
    password: str | None = None

class UserPasswordResetReqSchema(UserBaseReqSchema):
    confirm_password: str

    @model_validator(mode='after')
    def validate_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match.')
        
        return self

class UserProfileImgPath(BaseModel):
    img_path: FilePath


# Response Schema
class UserProfileResSchema(UserBaseSchema):
    fname: str | None = None
    lname: str | None = None
    mobile_number: str | None = None

class UserProfileViewSchema(UserProfileResSchema):
    password: SecretStr

class UserObjResSchema(UserProfileResSchema):
    id: int

class AuthenticatedUser(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool

class UserAccountDeleteResSchema(UserProfileResSchema):
    password: ClassVar[str]


# Callback url schema

class NotifyData(BaseModel):
    title: str = None
    user: dict = None