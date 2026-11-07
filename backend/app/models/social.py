import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database.connection import Base

class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    platform = Column(String(50), nullable=False) # github, linkedin, instagram, twitter, youtube, other
    platform_user_id = Column(String(255), nullable=True)
    username = Column(String(255), nullable=True)
    profile_url = Column(String(1000), nullable=False)
    display_name = Column(String(255), nullable=True)
    avatar_url = Column(String(1000), nullable=True)
    connection_type = Column(String(50), default="profile_link") # "oauth" or "profile_link"
    is_connected = Column(Boolean, default=False) # True if OAuth connected, False if manual profile link added
    show_on_public_profile = Column(Boolean, default=True)
    public_repos = Column(JSONB, default=list) # For GitHub: [{name, url, description, language, stars, forks}]
    platform_metadata = Column(JSONB, default=dict)
    encrypted_token = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="social_accounts")


class SocialAccountPermission(Base):
    __tablename__ = "social_account_permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    social_account_id = Column(UUID(as_uuid=True), ForeignKey("social_accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    scope = Column(String(255), nullable=False)
    granted_at = Column(DateTime, default=datetime.utcnow)

    account = relationship("SocialAccount", backref="permissions")


class SocialConnectionLog(Base):
    __tablename__ = "social_connection_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    platform = Column(String(50), nullable=False)
    action = Column(String(50), nullable=False) # connect, disconnect, sync, update_visibility
    status = Column(String(50), default="success") # success, failed
    details = Column(JSONB, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
