import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database.connection import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    name = Column(String, nullable=False)
    preferred_name = Column(String, nullable=True)
    native_language = Column(String, nullable=True, default="English")
    english_level = Column(String, nullable=True, default="Intermediate") # A1, A2, B1, B2, C1, C2
    learning_goal = Column(String, nullable=True)
    timezone = Column(String, nullable=True)
    phone_number = Column(String(50), nullable=True)
    date_of_birth = Column(String(50), nullable=True)
    country = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    avatar_url = Column(String(1000), nullable=True)
    profession = Column(String(100), nullable=True)
    organization = Column(String(255), nullable=True)
    enabled_modules = Column(JSONB, default=lambda: ["study", "career", "research", "creator", "planner", "knowledge_base"])
    career_skills = Column(JSONB, default=list) # Skills linked from career roadmap and research
    research_interests = Column(JSONB, default=list) # Research domains and methodology skills
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", backref="profile")

class LearningProfile(Base):
    __tablename__ = "learning_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    
    grammar_score = Column(Integer, default=0)
    vocabulary_score = Column(Integer, default=0)
    fluency_score = Column(Integer, default=0)
    pronunciation_score = Column(Integer, default=0)
    
    # Store weak topics or specific metrics dynamically
    grammar_data = Column(JSONB, default=dict)
    vocabulary_data = Column(JSONB, default=dict)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", backref="learning_profile")
