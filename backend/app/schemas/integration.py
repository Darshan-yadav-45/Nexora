from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class PlannerTaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = "Medium"
    status: Optional[str] = "Todo"
    source_module: Optional[str] = "manual" # research, career, manual
    source_id: Optional[UUID] = None
    tags: Optional[List[str]] = []

class PlannerTaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[List[str]] = None

class PlannerTaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: str
    status: str
    source_module: str
    source_id: Optional[UUID] = None
    tags: List[str] = []
    created_at: datetime
    updated_at: datetime

class KnowledgeBaseItemCreate(BaseModel):
    title: str
    category: Optional[str] = "General"
    tags: Optional[List[str]] = []
    content: str
    source_type: Optional[str] = "manual"
    source_id: Optional[UUID] = None

class KnowledgeBaseItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    title: str
    category: str
    tags: List[str] = []
    content: str
    source_type: str
    source_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

class ConnectCareerSkillRequest(BaseModel):
    skill_name: str
    domain: Optional[str] = "Software Engineering"
    proficiency: Optional[str] = "Intermediate"

