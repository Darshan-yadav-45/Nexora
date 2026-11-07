import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database.connection import Base

class CareerPath(Base):
    __tablename__ = "career_paths"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(50), default="Code")
    estimated_weeks = Column(Integer, default=16)
    total_hours = Column(Integer, default=120)
    is_custom = Column(Boolean, default=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    modules = relationship("CareerModule", back_populates="career_path", cascade="all, delete-orphan", order_by="CareerModule.order_index")
    enrollments = relationship("UserCareerEnrollment", back_populates="career_path", cascade="all, delete-orphan")


class CareerModule(Base):
    __tablename__ = "career_modules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    career_path_id = Column(UUID(as_uuid=True), ForeignKey("career_paths.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)
    difficulty_level = Column(String(50), default="Beginner") # Beginner, Intermediate, Advanced
    estimated_hours = Column(Integer, default=10)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    career_path = relationship("CareerPath", back_populates="modules")
    topics = relationship("CareerTopic", back_populates="module", cascade="all, delete-orphan", order_by="CareerTopic.order_index")


class CareerTopic(Base):
    __tablename__ = "career_topics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    career_module_id = Column(UUID(as_uuid=True), ForeignKey("career_modules.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False)
    summary = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)
    prerequisites = Column(JSONB, default=list) # List of prerequisite topics/skills
    estimated_minutes = Column(Integer, default=90)
    level = Column(String(50), default="Beginner") # Beginner, Intermediate, Advanced
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    module = relationship("CareerModule", back_populates="topics")
    subtopics = relationship("CareerSubtopic", back_populates="topic", cascade="all, delete-orphan", order_by="CareerSubtopic.order_index")
    learning_content = relationship("TopicLearningContent", back_populates="topic", uselist=False, cascade="all, delete-orphan")
    progress_records = relationship("UserTopicProgress", back_populates="topic", cascade="all, delete-orphan")
    notes = relationship("UserTopicNote", back_populates="topic", cascade="all, delete-orphan")


class CareerSubtopic(Base):
    __tablename__ = "career_subtopics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    career_topic_id = Column(UUID(as_uuid=True), ForeignKey("career_topics.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    order_index = Column(Integer, default=0)
    content_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    topic = relationship("CareerTopic", back_populates="subtopics")


class TopicLearningContent(Base):
    """
    Complete learning content for every topic, covering all 17 master requirements:
    1. Topic name and learning objectives
    2. Prerequisites
    3. Beginner-friendly explanation
    4. Detailed technical notes
    5. Important definitions and concepts
    6. Syntax and examples where applicable
    7. Practical coding examples with explanations
    8. Real-world applications
    9. Common mistakes and how to avoid them
    10. Interview questions with answers
    11. MCQs with answers and explanations
    12. Coding exercises or practical tasks
    13. Mini-projects and project assignments
    14. Revision notes and key takeaways
    15. Additional learning resources
    16. Estimated learning time
    17. Topic completion assessment
    """
    __tablename__ = "topic_learning_contents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    career_topic_id = Column(UUID(as_uuid=True), ForeignKey("career_topics.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    topic_name = Column(String(255), nullable=False)
    learning_objectives = Column(JSONB, default=list) # List of objectives
    prerequisites = Column(JSONB, default=list) # List of prerequisite items
    beginner_explanation = Column(Text, nullable=False)
    detailed_technical_notes = Column(Text, nullable=False)
    important_definitions = Column(JSONB, default=list) # [{term: str, definition: str, key_concept: str}]
    syntax_and_examples = Column(JSONB, default=list) # [{title: str, language: str, syntax: str, example: str, explanation: str}]
    practical_coding_examples = Column(JSONB, default=list) # [{title: str, code: str, language: str, explanation: str, output: str}]
    real_world_applications = Column(JSONB, default=list) # [{domain: str, use_case: str, real_example: str}]
    common_mistakes = Column(JSONB, default=list) # [{mistake: str, why_wrong: str, how_to_fix: str, corrected_code: str}]
    interview_questions = Column(JSONB, default=list) # [{question: str, answer: str, difficulty: str, tip: str}]
    mcqs = Column(JSONB, default=list) # [{id: int, question: str, options: list[str], correct_option: int, explanation: str}]
    coding_exercises = Column(JSONB, default=list) # [{id: int, title: str, description: str, starter_code: str, solution_code: str, test_cases: list}]
    mini_projects = Column(JSONB, default=list) # [{title: str, description: str, requirements: list[str], steps: list[str], deliverables: str}]
    revision_notes = Column(Text, nullable=False)
    key_takeaways = Column(JSONB, default=list) # List of strings
    additional_learning_resources = Column(JSONB, default=list) # [{title: str, url: str, type: str, note: str}]
    estimated_learning_time_minutes = Column(Integer, default=90)
    topic_completion_assessment = Column(JSONB, default=dict) # Assessment criteria, rubric, and passing score
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    topic = relationship("CareerTopic", back_populates="learning_content")


class UserCareerEnrollment(Base):
    __tablename__ = "user_career_enrollments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    career_path_id = Column(UUID(as_uuid=True), ForeignKey("career_paths.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="In Progress") # Not Started, In Progress, Paused, Completed
    current_topic_id = Column(UUID(as_uuid=True), ForeignKey("career_topics.id", ondelete="SET NULL"), nullable=True)
    completion_percentage = Column(Float, default=0.0)
    daily_study_hours = Column(Float, default=2.0)
    weekly_target_hours = Column(Float, default=10.0)
    target_completion_date = Column(DateTime, nullable=True)
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    last_activity_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    career_path = relationship("CareerPath", back_populates="enrollments")


class UserTopicProgress(Base):
    __tablename__ = "user_topic_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    career_topic_id = Column(UUID(as_uuid=True), ForeignKey("career_topics.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="Not Started") # Not Started, In Progress, Completed, Needs Revision
    quiz_score = Column(Float, default=0.0)
    quiz_answers = Column(JSONB, default=dict)
    exercise_submissions = Column(JSONB, default=dict)
    project_completed = Column(Boolean, default=False)
    time_spent_minutes = Column(Integer, default=0)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    topic = relationship("CareerTopic", back_populates="progress_records")


class UserTopicNote(Base):
    __tablename__ = "user_topic_notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    career_topic_id = Column(UUID(as_uuid=True), ForeignKey("career_topics.id", ondelete="CASCADE"), nullable=False)
    notes = Column(Text, default="")
    is_bookmarked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    topic = relationship("CareerTopic", back_populates="notes")


class UserStudyTimetable(Base):
    __tablename__ = "user_study_timetables"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    career_path_id = Column(UUID(as_uuid=True), ForeignKey("career_paths.id", ondelete="CASCADE"), nullable=False)
    available_hours_per_day = Column(JSONB, default=dict) # {"monday": 2, "tuesday": 2, ...}
    schedule_items = Column(JSONB, default=list) # [{date: str, topic_id: str, topic_title: str, hours: float, completed: bool}]
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CustomRoadmap(Base):
    __tablename__ = "custom_roadmaps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    source_filename = Column(String(255), nullable=True)
    extracted_raw_text = Column(Text, nullable=True)
    parsed_structure = Column(JSONB, default=dict) # Modules, topics, subtopics, prerequisites, milestones
    missing_or_unclear_topics = Column(JSONB, default=list)
    status = Column(String(50), default="reviewed") # uploaded, reviewed, confirmed, saved
    career_path_id = Column(UUID(as_uuid=True), ForeignKey("career_paths.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

