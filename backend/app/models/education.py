import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database.connection import Base

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    current_education_level = Column(String(100), nullable=True) # SSLC, PUC, Diploma, UG, PG, PhD, Other
    current_institution = Column(String(255), nullable=True)
    current_degree = Column(String(255), nullable=True)
    current_semester = Column(String(50), nullable=True)
    extra_info = Column(JSONB, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="student_profile")


class TeacherProfile(Base):
    __tablename__ = "teacher_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    institution = Column(String(255), nullable=True)
    teaching_position = Column(String(255), nullable=True) # Professor, Asst Prof, Lecturer, Instructor
    department = Column(String(255), nullable=True)
    qualification = Column(String(255), nullable=True) # MTech, PhD, MSc, etc.
    specialization = Column(String(255), nullable=True)
    teaching_experience_years = Column(Float, default=0.0)
    subjects_taught = Column(JSONB, default=list) # List of subject names
    current_classes_semesters = Column(JSONB, default=list) # List of classes/semesters
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="teacher_profile")


class EducationRecord(Base):
    __tablename__ = "education_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    level = Column(String(50), nullable=False) # SSLC, PUC, Diploma, UG, PG, PhD, Other
    status = Column(String(50), nullable=False, default="Completed") # Completed, Currently studying, Not started
    institution_name = Column(String(255), nullable=True) # School, College, University
    board_or_university = Column(String(255), nullable=True) # CBSE, ICSE, State Board, VTU, etc.
    stream = Column(String(100), nullable=True) # Science, Commerce, Arts, Other
    degree_name = Column(String(100), nullable=True) # BCA, BSc, BE/BTech, MCA, etc.
    specialization = Column(String(255), nullable=True) # Computer Science, AI, Mechanical, etc.
    course_duration = Column(String(50), nullable=True) # 3 years, 4 years
    admission_year = Column(Integer, nullable=True)
    passing_year = Column(Integer, nullable=True)
    expected_completion_year = Column(Integer, nullable=True)
    current_class_or_year = Column(String(50), nullable=True) # e.g. "Class 10", "3rd Year"
    current_semester = Column(String(50), nullable=True) # e.g. "5th Semester"
    result_percentage_cgpa = Column(String(50), nullable=True) # e.g. "9.2 CGPA" or "88.5%"
    research_title = Column(String(500), nullable=True) # For PhD
    research_guide = Column(String(255), nullable=True) # For PhD
    research_status = Column(String(100), nullable=True) # For PhD
    chronological_order = Column(Integer, default=1)
    extra_metadata = Column(JSONB, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="education_records")


class UserSubject(Base):
    __tablename__ = "user_subjects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    education_record_id = Column(UUID(as_uuid=True), ForeignKey("education_records.id", ondelete="SET NULL"), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=True)
    credits = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="subjects")
    syllabi = relationship("Syllabus", back_populates="subject", cascade="all, delete-orphan")
    materials = relationship("StudyMaterial", back_populates="subject", cascade="all, delete-orphan")


class Syllabus(Base):
    __tablename__ = "syllabi"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_subject_id = Column(UUID(as_uuid=True), ForeignKey("user_subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    source_type = Column(String(50), default="file_upload") # file_upload, pasted_text
    file_name = Column(String(255), nullable=True)
    file_path = Column(String(500), nullable=True)
    content_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subject = relationship("UserSubject", back_populates="syllabi")
    user = relationship("User")


class StudyMaterial(Base):
    __tablename__ = "study_materials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_subject_id = Column(UUID(as_uuid=True), ForeignKey("user_subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    material_type = Column(String(100), default="lecture_notes") # lecture_notes, assignments, question_papers, lab_manuals, reference_urls, teacher_notes
    file_name = Column(String(255), nullable=True)
    file_path = Column(String(500), nullable=True)
    url = Column(String(1000), nullable=True)
    content_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subject = relationship("UserSubject", back_populates="materials")
    user = relationship("User")


class LearningPreferences(Base):
    __tablename__ = "learning_preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    explanation_language = Column(String(50), default="English")
    difficulty_level = Column(String(50), default="Beginner") # Beginner, Intermediate, Advanced
    explanation_depth = Column(String(50), default="detailed") # simple, detailed
    code_examples_required = Column(Boolean, default=True)
    visual_explanations_required = Column(Boolean, default=True)
    practice_questions_required = Column(Boolean, default=True)
    mcqs_required = Column(Boolean, default=True)
    viva_prep_required = Column(Boolean, default=False)
    exam_prep_required = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="learning_preferences")


class CareerProfile(Base):
    __tablename__ = "career_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    career_goal = Column(String(255), nullable=True)
    current_skills = Column(JSONB, default=list) # List of skill strings
    technologies_interested = Column(JSONB, default=list) # List of tech strings
    preferred_career_path = Column(String(100), default="Python Full Stack Development") # Java Full Stack, Python Full Stack, Data Analysis, AI/ML, Cloud/DevOps, Web Development, Other
    daily_learning_time_minutes = Column(Integer, default=60)
    target_completion_weeks = Column(Integer, default=12)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="career_profile")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), unique=True, nullable=False, index=True)
    category = Column(String(100), nullable=True) # Programming, Database, Framework, Tool, Soft Skill
    description = Column(Text, nullable=True)


class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_name = Column(String(150), nullable=False)
    category = Column(String(100), nullable=True)
    proficiency = Column(String(50), default="Intermediate") # Beginner, Intermediate, Advanced
    source = Column(String(50), default="manual") # manual, resume, career_roadmap, research
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="user_skills")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=True)
    extracted_text = Column(Text, nullable=True)
    status = Column(String(50), default="uploaded") # uploaded, parsed, confirmed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="resumes")
    sections = relationship("ResumeSection", back_populates="resume", cascade="all, delete-orphan")


class ResumeSection(Base):
    __tablename__ = "resume_sections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    section_name = Column(String(100), nullable=False) # education, skills, projects, internships, work_experience, certifications, achievements
    content_data = Column(JSONB, default=list) # Parsed structured records
    is_confirmed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    resume = relationship("Resume", back_populates="sections")
