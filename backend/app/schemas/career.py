from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class SubtopicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    order_index: int
    content_summary: Optional[str] = None

class TopicLearningContentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    topic_name: str
    learning_objectives: List[str] = []
    prerequisites: List[str] = []
    beginner_explanation: str
    detailed_technical_notes: str
    important_definitions: List[Dict[str, Any]] = []
    syntax_and_examples: List[Dict[str, Any]] = []
    practical_coding_examples: List[Dict[str, Any]] = []
    real_world_applications: List[Dict[str, Any]] = []
    common_mistakes: List[Dict[str, Any]] = []
    interview_questions: List[Dict[str, Any]] = []
    mcqs: List[Dict[str, Any]] = []
    coding_exercises: List[Dict[str, Any]] = []
    mini_projects: List[Dict[str, Any]] = []
    revision_notes: str
    key_takeaways: List[str] = []
    additional_learning_resources: List[Dict[str, Any]] = []
    estimated_learning_time_minutes: int
    topic_completion_assessment: Dict[str, Any] = {}

class TopicBriefResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    career_module_id: UUID
    title: str
    slug: str
    summary: Optional[str] = None
    order_index: int
    prerequisites: List[str] = []
    estimated_minutes: int
    level: str
    subtopics: List[SubtopicResponse] = []

class ModuleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    career_path_id: UUID
    title: str
    description: Optional[str] = None
    order_index: int
    difficulty_level: str
    estimated_hours: int
    topics: List[TopicBriefResponse] = []

class CareerPathResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    slug: str
    title: str
    description: str
    icon: str
    estimated_weeks: int
    total_hours: int
    is_custom: bool
    user_id: Optional[UUID] = None
    modules: List[ModuleResponse] = []

class TopicProgressUpdateRequest(BaseModel):
    status: str # "Not Started", "In Progress", "Completed", "Needs Revision"
    quiz_score: Optional[float] = None
    quiz_answers: Optional[Dict[str, Any]] = None
    exercise_submissions: Optional[Dict[str, Any]] = None
    project_completed: Optional[bool] = None
    time_spent_minutes: Optional[int] = None

class TopicNoteRequest(BaseModel):
    notes: str
    is_bookmarked: Optional[bool] = None

class GenerateTimetableRequest(BaseModel):
    career_path_id: UUID
    daily_study_hours: float = 2.0
    days_per_week: int = 5
    start_date: Optional[datetime] = None

class GenerateAiRoadmapRequest(BaseModel):
    career_goal: str
    current_knowledge_level: str = "Beginner"
    existing_skills: List[str] = []
    preferred_technologies: List[str] = []
    daily_study_hours: float = 2.0
    weekly_study_hours: float = 14.0
    target_completion_weeks: int = 16
    learning_preferences: str = "Practical Project-Driven"
    existing_roadmap_notes: Optional[str] = ""

class ConfirmCustomRoadmapRequest(BaseModel):
    custom_roadmap_id: UUID
    title: str
    modules: List[Dict[str, Any]]

