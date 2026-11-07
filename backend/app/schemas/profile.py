from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any

class UserProfileBase(BaseModel):
    name: str
    preferred_name: Optional[str] = None
    native_language: str
    english_level: str
    learning_goal: Optional[str] = None
    timezone: Optional[str] = None

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileResponse(UserProfileBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LearningProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    grammar_score: int
    vocabulary_score: int
    fluency_score: int
    pronunciation_score: int
    grammar_data: Dict[str, Any]
    vocabulary_data: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
