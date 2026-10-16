from enum import Enum
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

NAME_MIN_LENGTH = 2
NAME_MAX_LENGTH = 300
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 64

class Role(str, Enum):
    user = "user"
    admin = "admin"

class UserCreate(BaseModel):
    name: str = Field(
        min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH
    )
    email: EmailStr
    password: str = Field(
        min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH
    )
    role: Role = Role.user
    is_active: bool = True

class UserUpdate(BaseModel):
    name: str = Field(
        default=None, min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH
    )
    email: EmailStr = Field(
        default=None
    )
    password: str = Field(
        default=None, min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH
    )
    role: Role = Field(
        default=None
    )
    is_active: bool = Field(
        default=None
    )

class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Role
    is_active: bool
    created_at: datetime