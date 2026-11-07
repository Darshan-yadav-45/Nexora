from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    name: Optional[str] = None
    password: str
    confirm_password: Optional[str] = None

class UserResponse(UserBase):
    id: UUID
    account_type: Optional[str] = None
    is_verified: bool = True
    profile_completed: bool = False
    first_time_login: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: Optional[UserResponse] = None

class TokenData(BaseModel):
    email: Optional[str] = None

class SelectAccountTypeRequest(BaseModel):
    account_type: str # "student", "teacher", "professional"

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    confirm_password: Optional[str] = None
