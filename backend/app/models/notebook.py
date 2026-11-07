import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database.connection import Base

class ResearchNotebook(Base):
    __tablename__ = "research_notebooks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(500), nullable=False) # e.g. "Artificial Intelligence in Healthcare"
    description = Column(Text, nullable=True)
    domain_area = Column(String(255), nullable=True)
    keywords = Column(JSONB, default=list)
    category = Column(String(100), default="General")
    is_pinned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="research_notebooks")
    sources = relationship("ResearchNotebookSource", back_populates="notebook", cascade="all, delete-orphan")
    generated_contents = relationship("ResearchGeneratedContent", back_populates="notebook", cascade="all, delete-orphan")
    chunks = relationship("ResearchDocumentChunk", back_populates="notebook", cascade="all, delete-orphan")
    exports = relationship("ResearchExport", back_populates="notebook", cascade="all, delete-orphan")


class ResearchNotebookSource(Base):
    __tablename__ = "research_notebook_sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    notebook_id = Column(UUID(as_uuid=True), ForeignKey("research_notebooks.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=True)
    source_type = Column(String(50), default="pdf") # pdf, docx, txt, pasted_text, url, youtube, audio
    file_path = Column(String(1000), nullable=True)
    source_url = Column(String(1000), nullable=True)
    processing_status = Column(String(50), default="completed") # queued, processing, completed, failed
    processing_progress = Column(Integer, default=100) # 0 to 100
    overview = Column(Text, nullable=True)
    key_points = Column(JSONB, default=list)
    headings = Column(JSONB, default=list)
    extracted_text = Column(Text, nullable=True)
    page_count = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    notebook = relationship("ResearchNotebook", back_populates="sources")
    pages = relationship("ResearchSourcePage", back_populates="source", cascade="all, delete-orphan")
    chunks = relationship("ResearchDocumentChunk", back_populates="source", cascade="all, delete-orphan")
    file_record = relationship("ResearchSourceFile", back_populates="source", uselist=False, cascade="all, delete-orphan")


class ResearchSourceFile(Base):
    __tablename__ = "research_source_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("research_notebook_sources.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    file_hash = Column(String(64), nullable=True)
    file_size_bytes = Column(Integer, default=0)
    mime_type = Column(String(100), nullable=True)
    storage_path = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    source = relationship("ResearchNotebookSource", back_populates="file_record")


class ResearchSourcePage(Base):
    __tablename__ = "research_source_pages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("research_notebook_sources.id", ondelete="CASCADE"), nullable=False, index=True)
    page_number = Column(Integer, nullable=False)
    page_text = Column(Text, nullable=False)
    word_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    source = relationship("ResearchNotebookSource", back_populates="pages")


class ResearchDocumentChunk(Base):
    __tablename__ = "research_document_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("research_notebook_sources.id", ondelete="CASCADE"), nullable=False, index=True)
    notebook_id = Column(UUID(as_uuid=True), ForeignKey("research_notebooks.id", ondelete="CASCADE"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    page_number = Column(Integer, nullable=True)
    chunk_text = Column(Text, nullable=False)
    token_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    source = relationship("ResearchNotebookSource", back_populates="chunks")
    notebook = relationship("ResearchNotebook", back_populates="chunks")
    embedding = relationship("ResearchEmbedding", back_populates="chunk", uselist=False, cascade="all, delete-orphan")


class ResearchEmbedding(Base):
    __tablename__ = "research_embeddings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chunk_id = Column(UUID(as_uuid=True), ForeignKey("research_document_chunks.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    embedding_vector = Column(JSONB, default=list) # Vector data
    model_name = Column(String(100), default="text-embedding-004")
    created_at = Column(DateTime, default=datetime.utcnow)

    chunk = relationship("ResearchDocumentChunk", back_populates="embedding")


class ResearchGeneratedContent(Base):
    __tablename__ = "research_generated_content"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    notebook_id = Column(UUID(as_uuid=True), ForeignKey("research_notebooks.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    content_type = Column(String(100), nullable=False) # 20 generators
    title = Column(String(255), nullable=False)
    data = Column(JSONB, default=dict)
    is_saved_as_note = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    notebook = relationship("ResearchNotebook", back_populates="generated_contents")


class ResearchPaperComparison(Base):
    __tablename__ = "research_paper_comparisons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    notebook_id = Column(UUID(as_uuid=True), ForeignKey("research_notebooks.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    matrix_data = Column(JSONB, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)


class ResearchHumanizeDraft(Base):
    __tablename__ = "research_humanize_drafts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    notebook_id = Column(UUID(as_uuid=True), ForeignKey("research_notebooks.id", ondelete="SET NULL"), nullable=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    original_text = Column(Text, nullable=False)
    revised_text = Column(Text, nullable=False)
    mode = Column(String(50), default="natural_human") # natural_human, academic_formal, simple_english, concise, expand, bullet_to_para, para_to_notes
    changes_summary = Column(JSONB, default=list)
    status = Column(String(50), default="draft") # draft, accepted, rejected
    created_at = Column(DateTime, default=datetime.utcnow)


class ResearchExport(Base):
    __tablename__ = "research_exports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    notebook_id = Column(UUID(as_uuid=True), ForeignKey("research_notebooks.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    export_type = Column(String(50), default="markdown") # markdown, csv, json, text
    file_path = Column(String(1000), nullable=True)
    content_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    notebook = relationship("ResearchNotebook", back_populates="exports")
