from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator, SecretStr
from starlette import status


class Role(str, Enum):
    user = "user"
    admin = "admin"
    super_user = "super_user"
    teacher = "teacher"


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    password: SecretStr
    _role: Role = Role.user

    @validator('password', pre=True)
    def password_length(cls, v):
        if len(v) < 8:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail='password must be at least 8 characters')
        return SecretStr(v)

    @validator('email', pre=True)
    def email_format(cls, v):
        if not v:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail='email cannot be blank')
        try:
            EmailStr.validate(v)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail='invalid email format')
        return v

    @property
    def role(self):
        return self._role


class UserDisplay(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    role: Role
    is_active: bool
    is_blocked: bool
    registered_at: datetime
    last_activity: datetime

    @validator('email', pre=True)
    def email_format(cls, v):
        try:
            EmailStr.validate(v)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail='invalid email format')
        return v

    class Config:
        orm_mode = True
