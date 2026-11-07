from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

# Research Project Schemas
class ResearchProjectCreate(BaseModel):
    title: str
    domain_area: Optional[str] = None
    topic: Optional[str] = None
    problem_statement: Optional[str] = None
    background_context: Optional[str] = None
    abstract: Optional[str] = None
    introduction: Optional[str] = None
    scope_and_limitations: Optional[str] = None
    research_type: Optional[str] = "Applied Research"
    methodology_overview: Optional[str] = None
    expected_outcomes: Optional[str] = None
    supervisor_details: Optional[Dict[str, Any]] = None
    status: Optional[str] = "In Progress"
    start_date: Optional[datetime] = None
    target_completion_date: Optional[datetime] = None

class ResearchProjectUpdate(BaseModel):
    title: Optional[str] = None
    domain_area: Optional[str] = None
    topic: Optional[str] = None
    problem_statement: Optional[str] = None
    background_context: Optional[str] = None
    abstract: Optional[str] = None
    introduction: Optional[str] = None
    scope_and_limitations: Optional[str] = None
    research_type: Optional[str] = None
    methodology_overview: Optional[str] = None
    expected_outcomes: Optional[str] = None
    supervisor_details: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    target_completion_date: Optional[datetime] = None

class ResearchProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    title: str
    domain_area: Optional[str] = None
    topic: Optional[str] = None
    problem_statement: Optional[str] = None
    background_context: Optional[str] = None
    abstract: Optional[str] = None
    introduction: Optional[str] = None
    scope_and_limitations: Optional[str] = None
    research_type: str
    methodology_overview: Optional[str] = None
    expected_outcomes: Optional[str] = None
    supervisor_details: Dict[str, Any] = {}
    status: str
    start_date: datetime
    target_completion_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

# Paper Schemas
class ResearchPaperResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    title: str
    publication_year: Optional[int] = None
    journal_or_conference: Optional[str] = None
    doi: Optional[str] = None
    abstract: Optional[str] = None
    publisher: Optional[str] = None
    source_url: Optional[str] = None
    file_reference: Optional[str] = None
    page_count: int = 0
    processing_status: str
    citation_key: Optional[str] = None
    user_notes: Optional[str] = None
    paper_type: str
    created_at: datetime
    updated_at: datetime

# Literature Review Entry Schemas (The 12 attributes)
class LiteratureReviewEntryCreate(BaseModel):
    literature_review_id: UUID
    research_paper_id: UUID
    paper_title: str
    authors_and_year: str
    research_problem: Optional[str] = None
    objectives: Optional[str] = None
    methodology: Optional[str] = None
    dataset: Optional[str] = None
    technologies_used: Optional[str] = None
    key_findings: Optional[str] = None
    limitations: Optional[str] = None
    research_gaps: Optional[str] = None
    relevance_to_project: Optional[str] = None
    citation_details: Optional[str] = None
    personal_observations: Optional[str] = None

class LiteratureReviewEntryUpdate(BaseModel):
    research_problem: Optional[str] = None
    objectives: Optional[str] = None
    methodology: Optional[str] = None
    dataset: Optional[str] = None
    technologies_used: Optional[str] = None
    key_findings: Optional[str] = None
    limitations: Optional[str] = None
    research_gaps: Optional[str] = None
    relevance_to_project: Optional[str] = None
    citation_details: Optional[str] = None
    personal_observations: Optional[str] = None

class LiteratureReviewEntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    literature_review_id: UUID
    research_paper_id: UUID
    paper_title: str
    authors_and_year: str
    research_problem: Optional[str] = None
    objectives: Optional[str] = None
    methodology: Optional[str] = None
    dataset: Optional[str] = None
    technologies_used: Optional[str] = None
    key_findings: Optional[str] = None
    limitations: Optional[str] = None
    research_gaps: Optional[str] = None
    relevance_to_project: Optional[str] = None
    citation_details: Optional[str] = None
    personal_observations: Optional[str] = None
    is_ai_generated: bool
    order_index: int
    created_at: datetime
    updated_at: datetime

class LiteratureReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    research_project_id: UUID
    user_id: UUID
    title: str
    description: Optional[str] = None
    synthesis_notes: Optional[str] = None
    status: str
    entries: List[LiteratureReviewEntryResponse] = []
    created_at: datetime
    updated_at: datetime

# Gap Analysis Schema
class ResearchGapAnalysisCreate(BaseModel):
    research_project_id: UUID
    gap_title: str
    description: str
    existing_approach_limitations: Optional[str] = None
    unexplored_area: Optional[str] = None
    proposed_solution_direction: Optional[str] = None
    impact_level: Optional[str] = "High"
    feasibility: Optional[str] = "High"

class ResearchGapAnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    research_project_id: UUID
    user_id: UUID
    gap_title: str
    description: str
    existing_approach_limitations: Optional[str] = None
    unexplored_area: Optional[str] = None
    proposed_solution_direction: Optional[str] = None
    impact_level: str
    feasibility: str
    created_at: datetime
    updated_at: datetime

# Methodology Schema
class ResearchMethodologyCreate(BaseModel):
    research_project_id: UUID
    methodology_name: str
    methodology_type: Optional[str] = "Quantitative"
    rationale: Optional[str] = None
    procedure_steps: Optional[List[Dict[str, Any]]] = None
    comparison_with_alternatives: Optional[str] = None

class ResearchMethodologyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    research_project_id: UUID
    user_id: UUID
    methodology_name: str
    methodology_type: str
    rationale: Optional[str] = None
    procedure_steps: List[Dict[str, Any]] = []
    comparison_with_alternatives: Optional[str] = None
    selected_for_project: bool
    created_at: datetime

# Variables Schema
class ResearchVariableCreate(BaseModel):
    research_project_id: UUID
    name: str
    variable_type: str = "Independent" # Independent, Dependent, Controlled, Confounding
    description: Optional[str] = None
    measurement_unit: Optional[str] = None
    operational_definition: Optional[str] = None

class ResearchVariableResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    research_project_id: UUID
    user_id: UUID
    name: str
    variable_type: str
    description: Optional[str] = None
    measurement_unit: Optional[str] = None
    operational_definition: Optional[str] = None
    created_at: datetime

# Notes Schema
class ResearchNoteCreate(BaseModel):
    research_project_id: UUID
    research_paper_id: Optional[UUID] = None
    title: str
    content: str
    note_type: Optional[str] = "personal"
    tags: Optional[List[str]] = None

class ResearchNoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    research_project_id: UUID
    research_paper_id: Optional[UUID] = None
    user_id: UUID
    title: str
    content: str
    note_type: str
    is_pinned: bool
    tags: List[str] = []
    created_at: datetime
    updated_at: datetime

# Citations Schema
class ResearchCitationCreate(BaseModel):
    research_project_id: UUID
    research_paper_id: UUID
    citation_format: str = "APA"
    formatted_text: str

class ResearchCitationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    research_project_id: UUID
    research_paper_id: UUID
    user_id: UUID
    citation_format: str
    formatted_text: str
    created_at: datetime

# Tasks Schema
class ResearchTaskCreate(BaseModel):
    research_project_id: UUID
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: Optional[str] = "Medium"
    status: Optional[str] = "Todo"
    assigned_to: Optional[str] = None

class ResearchTaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    research_project_id: UUID
    user_id: UUID
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: str
    status: str
    assigned_to: Optional[str] = None
    converted_to_planner_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

# AI Assistant Execution Request & Response
class AiToolExecutionRequest(BaseModel):
    tool_name: str # One of the 17 AI research tools
    research_project_id: Optional[UUID] = None
    research_paper_id: Optional[UUID] = None
    input_data: Dict[str, Any]
    persist_to_project: bool = True

class AiToolExecutionResponse(BaseModel):
    tool_name: str
    output: Dict[str, Any]
    saved_generation_id: Optional[UUID] = None

