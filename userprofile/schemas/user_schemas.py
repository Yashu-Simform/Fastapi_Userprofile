from pydantic import BaseModel, EmailStr
from typing import Annotated

class UserBaseSchema(BaseModel):
    email: EmailStr
    password: str

class UserRegistrationSchema(UserBaseSchema):
    fname: str | None = None
    lname: str | None = None
    mobile_number: str | None = None

class UserProfileViewSchema(UserRegistrationSchema):
    pass

class UserLoginSchema(UserBaseSchema):
    pass

class UserLoginDocsSchema(BaseModel):
    username: EmailStr
    password: str

class AuthenticatedUser:
    id: int
    email: EmailStr