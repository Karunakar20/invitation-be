from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic import model_validator


class UserBase(BaseModel):
    user_name: Optional[str] = None
    email: EmailStr
    profile_pic: Optional[str] = None

class UserCreate(UserBase):
    password: str  # required for local signup

class UserGoogleAuth(BaseModel):
    email: EmailStr
    user_name: Optional[str] = None
    oauth_id: str   # Google "sub"
    profile_pic: Optional[str] = None

class UserResponse(UserBase):
    id: int
    auth_provider: str
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True  # for SQLAlchemy (ORM mode in v2)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserAuth(BaseModel):
    email: EmailStr
    password: Optional[str] = None
    oauth_id: Optional[str] = None

    @model_validator(mode="after")
    def check_auth(cls, values):
        if not values.password and not values.oauth_id:
            raise ValueError("Either password or oauth_id required")
        return values