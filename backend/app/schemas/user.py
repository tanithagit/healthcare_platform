from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.models.user import UserRole


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: UserRole

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    role: UserRole
    is_active: int
    created_at: datetime

    class Config:
        from_attributes = True

    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str
    user_id: int
    email: str

class ChangePassword(BaseModel):
    current_password: str
    new_password: str
    
