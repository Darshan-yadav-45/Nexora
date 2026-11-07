import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database.connection import Base

class PlannerTask(Base):
    __tablename__ = "planner_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=True)
    priority = Column(String(50), default="Medium") # Low, Medium, High, Urgent
    status = Column(String(50), default="Todo") # Todo, In Progress, Completed
    source_module = Column(String(50), default="manual") # research, career, manual
    source_id = Column(UUID(as_uuid=True), nullable=True) # ID of research_task or career_topic
    tags = Column(JSONB, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class KnowledgeBaseItem(Base):
    __tablename__ = "knowledge_base_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(500), nullable=False, index=True)
    category = Column(String(100), default="General") # Research, Career, Methodology, Paper, Notes
    tags = Column(JSONB, default=list)
    content = Column(Text, nullable=False)
    source_type = Column(String(50), default="manual") # research_paper, research_doc, career_note, manual
    source_id = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

