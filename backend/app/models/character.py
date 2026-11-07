import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.database.connection import Base

class Character(Base):
    __tablename__ = "characters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False) # e.g. "English Teacher", "Casual Friend"
    gender = Column(String, nullable=False)
    personality = Column(String, nullable=False) # e.g. "Supportive, Empathetic, Patient"
    voice_id = Column(String, nullable=True) # Reference to TTS provider voice
    avatar_url = Column(String, nullable=True)
    is_premium = Column(Boolean, default=False)
    description = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
