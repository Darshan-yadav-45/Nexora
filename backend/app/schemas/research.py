from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List

# Paper Note Schemas
class PaperNoteBase(BaseModel):
    content: str
    page_number: Optional[str] = None

class PaperNoteCreate(PaperNoteBase):
    pass

class PaperNoteUpdate(BaseModel):
    content: Optional[str] = None
    page_number: Optional[str] = None

class PaperNoteResponse(PaperNoteBase):
    id: UUID
    paper_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Research Paper Schemas
class ResearchPaperBase(BaseModel):
    title: str
    authors: Optional[str] = None
    publication_year: Optional[str] = None
    abstract: Optional[str] = None
    doi: Optional[str] = None
    file_url: Optional[str] = None

class ResearchPaperCreate(ResearchPaperBase):
    pass

class ResearchPaperUpdate(BaseModel):
    title: Optional[str] = None
    authors: Optional[str] = None
    publication_year: Optional[str] = None
    abstract: Optional[str] = None
    doi: Optional[str] = None

class ResearchPaperResponse(ResearchPaperBase):
    id: UUID
    project_id: UUID
    created_at: datetime
    notes: List[PaperNoteResponse] = []

    class Config:
        from_attributes = True

# Literature Review Schemas
class LiteratureReviewBase(BaseModel):
    content: Optional[str] = None

class LiteratureReviewCreate(LiteratureReviewBase):
    pass

class LiteratureReviewUpdate(LiteratureReviewBase):
    pass

class LiteratureReviewResponse(LiteratureReviewBase):
    id: UUID
    project_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Research Project Schemas
class ResearchProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    research_question: Optional[str] = None
    status: Optional[str] = "planning"

class ResearchProjectCreate(ResearchProjectBase):
    pass

class ResearchProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    research_question: Optional[str] = None
    status: Optional[str] = None

class ResearchProjectResponse(ResearchProjectBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    papers: List[ResearchPaperResponse] = []
    literature_review: Optional[LiteratureReviewResponse] = None

    class Config:
        from_attributes = True
