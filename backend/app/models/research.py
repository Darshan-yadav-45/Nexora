import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database.connection import Base

# 1. research_projects
class ResearchProject(Base):
    __tablename__ = "research_projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    domain_area = Column(String(255), nullable=True) # e.g. "Natural Language Processing", "Bioinformatics"
    topic = Column(String(500), nullable=True)
    problem_statement = Column(Text, nullable=True)
    background_context = Column(Text, nullable=True)
    abstract = Column(Text, nullable=True)
    introduction = Column(Text, nullable=True)
    scope_and_limitations = Column(Text, nullable=True)
    research_type = Column(String(100), default="Applied Research") # Applied, Theoretical, Empirical, Exploratory
    methodology_overview = Column(Text, nullable=True)
    expected_outcomes = Column(Text, nullable=True)
    supervisor_details = Column(JSONB, default=dict) # {name, email, institution, role}
    status = Column(String(50), default="In Progress") # Planning, Literature Review, In Progress, Review, Completed, Paused
    start_date = Column(DateTime, default=datetime.utcnow)
    target_completion_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    members = relationship("ResearchProjectMember", back_populates="project", cascade="all, delete-orphan")
    topics = relationship("ResearchTopic", back_populates="project", cascade="all, delete-orphan")
    questions = relationship("ResearchQuestion", back_populates="project", cascade="all, delete-orphan")
    objectives = relationship("ResearchObjective", back_populates="project", cascade="all, delete-orphan")
    project_papers = relationship("ResearchProjectPaper", back_populates="project", cascade="all, delete-orphan")
    literature_reviews = relationship("LiteratureReview", back_populates="project", cascade="all, delete-orphan")
    gap_analyses = relationship("ResearchGapAnalysis", back_populates="project", cascade="all, delete-orphan")
    methodologies = relationship("ResearchMethodology", back_populates="project", cascade="all, delete-orphan")
    variables = relationship("ResearchVariable", back_populates="project", cascade="all, delete-orphan")
    datasets = relationship("ResearchDataset", back_populates="project", cascade="all, delete-orphan")
    experiments = relationship("ResearchExperiment", back_populates="project", cascade="all, delete-orphan")
    observations = relationship("ResearchObservation", back_populates="project", cascade="all, delete-orphan")
    notes = relationship("ResearchNote", back_populates="project", cascade="all, delete-orphan")
    citations = relationship("ResearchCitation", back_populates="project", cascade="all, delete-orphan")
    documents = relationship("ResearchDocument", back_populates="project", cascade="all, delete-orphan")
    tasks = relationship("ResearchTask", back_populates="project", cascade="all, delete-orphan")
    meetings = relationship("ResearchMeeting", back_populates="project", cascade="all, delete-orphan")
    feedback = relationship("ResearchFeedback", back_populates="project", cascade="all, delete-orphan")
    ai_generations = relationship("ResearchAiGeneration", back_populates="project", cascade="all, delete-orphan")
    conversations = relationship("ResearchConversation", back_populates="project", cascade="all, delete-orphan")
    activity_logs = relationship("ResearchActivityLog", back_populates="project", cascade="all, delete-orphan")


# 2. research_project_members
class ResearchProjectMember(Base):
    __tablename__ = "research_project_members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_project_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(50), default="Researcher") # Lead, Co-Investigator, Researcher, Supervisor, Reviewer
    permissions = Column(JSONB, default=dict)
    joined_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("ResearchProject", back_populates="members")


# 3. research_topics
class ResearchTopic(Base):
    __tablename__ = "research_topics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_project_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    domain = Column(String(255), nullable=True)
    subdomain = Column(String(255), nullable=True)
    importance_level = Column(String(50), default="High")
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("ResearchProject", back_populates="topics")


# 4. research_questions
class ResearchQuestion(Base):
    __tablename__ = "research_questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_project_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question = Column(Text, nullable=False)
    category = Column(String(50), default="Primary") # Primary, Secondary, Exploratory
    hypothesis = Column(Text, nullable=True)
    is_validated = Column(Boolean, default=False)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("ResearchProject", back_populates="questions")


# 5. research_objectives
class ResearchObjective(Base):
    __tablename__ = "research_objectives"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_project_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(50), default="High") # High, Medium, Low
    status = Column(String(50), default="Pending") # Pending, In Progress, Achieved
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("ResearchProject", back_populates="objectives")


# 6. research_papers
class ResearchPaper(Base):
    __tablename__ = "research_papers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(500), nullable=False, index=True)
    publication_year = Column(Integer, nullable=True)
    journal_or_conference = Column(String(255), nullable=True)
    doi = Column(String(100), nullable=True, index=True)
    abstract = Column(Text, nullable=True)
    publisher = Column(String(255), nullable=True)
    source_url = Column(String(1000), nullable=True)
    file_reference = Column(String(500), nullable=True)
    page_count = Column(Integer, default=0)
    processing_status = Column(String(50), default="completed") # pending, processing, completed, failed
    citation_key = Column(String(100), nullable=True)
    user_notes = Column(Text, nullable=True)
    paper_type = Column(String(50), default="Research Paper") # Research Paper, Journal Article, Conference Paper, Review
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    authors = relationship("ResearchPaperAuthor", back_populates="paper", cascade="all, delete-orphan", order_by="ResearchPaperAuthor.order_index")
    files = relationship("ResearchPaperFile", back_populates="paper", cascade="all, delete-orphan")
    text_content = relationship("ResearchPaperText", back_populates="paper", uselist=False, cascade="all, delete-orphan")
    pages = relationship("ResearchPaperPage", back_populates="paper", cascade="all, delete-orphan", order_by="ResearchPaperPage.page_number")
    paper_keywords = relationship("ResearchPaperKeyword", back_populates="paper", cascade="all, delete-orphan")
    project_associations = relationship("ResearchProjectPaper", back_populates="paper", cascade="all, delete-orphan")
    literature_review_entries = relationship("LiteratureReviewEntry", back_populates="paper", cascade="all, delete-orphan")
    highlights = relationship("ResearchHighlight", back_populates="paper", cascade="all, delete-orphan")
    citations = relationship("ResearchCitation", back_populates="paper", cascade="all, delete-orphan")
    references = relationship("ResearchReference", back_populates="paper", cascade="all, delete-orphan")


# 7. research_paper_authors
class ResearchPaperAuthor(Base):
    __tablename__ = "research_paper_authors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_paper_id = Column(UUID(as_uuid=True), ForeignKey("research_papers.id", ondelete="CASCADE"), nullable=False, index=True)
    author_name = Column(String(255), nullable=False)
    affiliation = Column(String(500), nullable=True)
    email = Column(String(255), nullable=True)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    paper = relationship("ResearchPaper", back_populates="authors")


# 8. research_paper_files
class ResearchPaperFile(Base):
    __tablename__ = "research_paper_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_paper_id = Column(UUID(as_uuid=True), ForeignKey("research_papers.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String(1000), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_size_bytes = Column(Integer, default=0)
    mime_type = Column(String(100), default="application/pdf")
    sha256_hash = Column(String(64), nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    paper = relationship("ResearchPaper", back_populates="files")


# 9. research_paper_text
class ResearchPaperText(Base):
    __tablename__ = "research_paper_text"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_paper_id = Column(UUID(as_uuid=True), ForeignKey("research_papers.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    full_text = Column(Text, nullable=False)
    chunk_count = Column(Integer, default=0)
    extracted_at = Column(DateTime, default=datetime.utcnow)

    paper = relationship("ResearchPaper", back_populates="text_content")


# 10. research_paper_pages
class ResearchPaperPage(Base):
    __tablename__ = "research_paper_pages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_paper_id = Column(UUID(as_uuid=True), ForeignKey("research_papers.id", ondelete="CASCADE"), nullable=False, index=True)
    page_number = Column(Integer, nullable=False)
    page_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    paper = relationship("ResearchPaper", back_populates="pages")


# 11. research_keywords
class ResearchKeyword(Base):
    __tablename__ = "research_keywords"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    keyword = Column(String(100), nullable=False, index=True)
    category = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    paper_keywords = relationship("ResearchPaperKeyword", back_populates="keyword_ref", cascade="all, delete-orphan")


# 12. research_paper_keywords
class ResearchPaperKeyword(Base):
    __tablename__ = "research_paper_keywords"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_paper_id = Column(UUID(as_uuid=True), ForeignKey("research_papers.id", ondelete="CASCADE"), nullable=False, index=True)
    keyword_id = Column(UUID(as_uuid=True), ForeignKey("research_keywords.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    paper = relationship("ResearchPaper", back_populates="paper_keywords")
    keyword_ref = relationship("ResearchKeyword", back_populates="paper_keywords")


# 13. research_project_papers
class ResearchProjectPaper(Base):
    __tablename__ = "research_project_papers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_project_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    research_paper_id = Column(UUID(as_uuid=True), ForeignKey("research_papers.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    relationship_type = Column(String(50), default="Foundational") # Foundational, Methodology, Baseline, Comparison, Related
    relevance_score = Column(Float, default=5.0) # 1-10 scale
    added_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("ResearchProject", back_populates="project_papers")
    paper = relationship("ResearchPaper", back_populates="project_associations")


# 14. literature_reviews
class LiteratureReview(Base):
    __tablename__ = "literature_reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_project_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    synthesis_notes = Column(Text, nullable=True)
    status = Column(String(50), default="In Progress") # In Progress, Completed, Draft
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("ResearchProject", back_populates="literature_reviews")
    entries = relationship("LiteratureReviewEntry", back_populates="review", cascade="all, delete-orphan", order_by="LiteratureReviewEntry.order_index")


# 15. literature_review_entries (The structured 12-attribute comparison table!)
class LiteratureReviewEntry(Base):
    """
    Structured comparison table attributes:
    1. Paper title
    2. Authors and year
    3. Research problem
    4. Objectives
    5. Methodology
    6. Dataset
    7. Technologies used
    8. Key findings
    9. Limitations
    10. Research gaps
    11. Relevance to the user's project
    12. Citation details
    """
    __tablename__ = "literature_review_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    literature_review_id = Column(UUID(as_uuid=True), ForeignKey("literature_reviews.id", ondelete="CASCADE"), nullable=False, index=True)
    research_paper_id = Column(UUID(as_uuid=True), ForeignKey("research_papers.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    paper_title = Column(String(500), nullable=False)
    authors_and_year = Column(String(255), nullable=False)
    research_problem = Column(Text, nullable=True)
    objectives = Column(Text, nullable=True)
    methodology = Column(Text, nullable=True)
    dataset = Column(Text, nullable=True)
    technologies_used = Column(Text, nullable=True)
    key_findings = Column(Text, nullable=True)
    limitations = Column(Text, nullable=True)
    research_gaps = Column(Text, nullable=True)
    relevance_to_project = Column(Text, nullable=True)
    citation_details = Column(Text, nullable=True)
    personal_observations = Column(Text, nullable=True) # User's personal observations
    is_ai_generated = Column(Boolean, default=True)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    review = relationship("LiteratureReview", back_populates="entries")
    paper = relationship("ResearchPaper", back_populates="literature_review_entries")


# 16. research_gap_analysis
class ResearchGapAnalysis(Base):
    __tablename__ = "research_gap_analysis"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_project_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    gap_title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    existing_approach_limitations = Column(Text, nullable=True)
    unexplored_area = Column(Text, nullable=True)
    proposed_solution_direction = Column(Text, nullable=True)
    impact_level = Column(String(50), default="High") # High, Medium, Low
    feasibility = Column(String(50), default="High")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("ResearchProject", back_populates="gap_analyses")


# 17. research_methodologies
class ResearchMethodology(Base):
    __tablename__ = "research_methodologies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_project_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    methodology_name = Column(String(255), nullable=False)
    methodology_type = Column(String(100), default="Quantitative") # Quantitative, Qualitative, Mixed, Experimental, Comparative
    rationale = Column(Text, nullable=True)
    procedure_steps = Column(JSONB, default=list) # [{step_num: int, title: str, description: str, tools: list}]
    comparison_with_alternatives = Column(Text, nullable=True)
    selected_for_project = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("ResearchProject", back_populates="methodologies")


# 18. research_variables
class ResearchVariable(Base):
    __tablename__ = "research_variables"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_project_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    variable_type = Column(String(50), default="Independent") # Independent, Dependent, Controlled, Confounding
    description = Column(Text, nullable=True)
    measurement_unit = Column(String(100), nullable=True)
    operational_definition = Column(Text, nullable=True)
    expected_relationship = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("ResearchProject", back_populates="variables")


# 19. research_datasets
class ResearchDataset(Base):
    __tablename__ = "research_datasets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_project_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    dataset_name = Column(String(255), nullable=False)
    source_url = Column(String(1000), nullable=True)
    description = Column(Text, nullable=True)
    data_type = Column(String(100), default="Tabular") # Tabular, Text, Image, Audio, Time Series, Graph
    record_count = Column(Integer, default=0)
    features_list = Column(JSONB, default=list) # List of column/feature names & descriptions
    preprocessing_steps = Column(Text, nullable=True)
    license = Column(String(100), nullable=True)
    file_reference = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("ResearchProject", back_populates="datasets")


# 20. research_experiments
class ResearchExperiment(Base):
    __tablename__ = "research_experiments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_project_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    experiment_name = Column(String(255), nullable=False)
    hypothesis = Column(Text, nullable=True)
    design_description = Column(Text, nullable=True)
    status = Column(String(50), default="Planned") # Planned, In Progress, Completed, Failed
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("ResearchProject", back_populates="experiments")
    steps = relationship("ResearchExperimentStep", back_populates="experiment", cascade="all, delete-orphan", order_by="ResearchExperimentStep.step_number")
    results = relationship("ResearchResult", back_populates="experiment", cascade="all, delete-orphan")


# 21. research_experiment_steps
class ResearchExperimentStep(Base):
    __tablename__ = "research_experiment_steps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_experiment_id = Column(UUID(as_uuid=True), ForeignKey("research_experiments.id", ondelete="CASCADE"), nullable=False, index=True)
    step_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    parameters = Column(JSONB, default=dict)
    status = Column(String(50), default="Pending") # Pending, Running, Completed, Skipped
    executed_at = Column(DateTime, nullable=True)

    experiment = relationship("ResearchExperiment", back_populates="steps")


# 22. research_results
class ResearchResult(Base):
    __tablename__ = "research_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_experiment_id = Column(UUID(as_uuid=True), ForeignKey("research_experiments.id", ondelete="CASCADE"), nullable=False, index=True)
    research_project_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    metric_name = Column(String(255), nullable=False)
    metric_value = Column(Float, nullable=False)
    baseline_value = Column(Float, nullable=True)
    unit = Column(String(50), default="")
    statistical_significance = Column(String(100), nullable=True) # e.g. "p < 0.01"
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    experiment = relationship("ResearchExperiment", back_populates="results")


# 23. research_observations
class ResearchObservation(Base):
    __tablename__ = "research_observations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_project_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    experiment_id = Column(UUID(as_uuid=True), ForeignKey("research_experiments.id", ondelete="SET NULL"), nullable=True)
    observation_text = Column(Text, nullable=False)
    chart_data = Column(JSONB, default=dict) # Structured chart config/data
    source_type = Column(String(50), default="user_hypothesis") # verified_paper, ai_suggestion, user_hypothesis
    conclusions = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("ResearchProject", back_populates="observations")


# 24. research_notes
class ResearchNote(Base):
    __tablename__ = "research_notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_project_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=True, index=True)
    notebook_id = Column(UUID(as_uuid=True), ForeignKey("research_notebooks.id", ondelete="CASCADE"), nullable=True, index=True)
    research_paper_id = Column(UUID(as_uuid=True), ForeignKey("research_papers.id", ondelete="SET NULL"), nullable=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    note_type = Column(String(50), default="personal") # personal, paper_wise, idea, summary, meeting
    category = Column(String(100), default="General")
    is_pinned = Column(Boolean, default=False)
    tags = Column(JSONB, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("ResearchProject", back_populates="notes")


# 25. research_highlights
class ResearchHighlight(Base):
    __tablename__ = "research_highlights"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_paper_id = Column(UUID(as_uuid=True), ForeignKey("research_papers.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    highlighted_text = Column(Text, nullable=False)
    page_number = Column(Integer, default=1)
    comment = Column(Text, nullable=True)
    color = Column(String(20), default="#fef08a") # Yellow default
    created_at = Column(DateTime, default=datetime.utcnow)

    paper = relationship("ResearchPaper", back_populates="highlights")


# 26. research_citations
class ResearchCitation(Base):
    __tablename__ = "research_citations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_project_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    research_paper_id = Column(UUID(as_uuid=True), ForeignKey("research_papers.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    citation_format = Column(String(50), default="APA") # APA, IEEE, Harvard, MLA, BibTeX, Chicago
    formatted_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("ResearchProject", back_populates="citations")
    paper = relationship("ResearchPaper", back_populates="citations")


# 27. research_references
class ResearchReference(Base):
    __tablename__ = "research_references"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_paper_id = Column(UUID(as_uuid=True), ForeignKey("research_papers.id", ondelete="CASCADE"), nullable=False, index=True)
    raw_reference_text = Column(Text, nullable=False)
    title = Column(String(500), nullable=True)
    authors = Column(String(500), nullable=True)
    year = Column(Integer, nullable=True)
    doi = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    paper = relationship("ResearchPaper", back_populates="references")


# 28. research_documents
class ResearchDocument(Base):
    __tablename__ = "research_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_project_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    document_title = Column(String(500), nullable=False)
    document_type = Column(String(50), default="Proposal") # Proposal, Paper Draft, Literature Review, Presentation Slides, Project Report
    content_markdown = Column(Text, nullable=False)
    status = Column(String(50), default="Draft") # Draft, In Review, Approved, Published
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("ResearchProject", back_populates="documents")
    versions = relationship("ResearchDocumentVersion", back_populates="document", cascade="all, delete-orphan", order_by="ResearchDocumentVersion.version_number")


# 29. research_document_versions
class ResearchDocumentVersion(Base):
    __tablename__ = "research_document_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_document_id = Column(UUID(as_uuid=True), ForeignKey("research_documents.id", ondelete="CASCADE"), nullable=False, index=True)
    version_number = Column(Integer, default=1)
    content_markdown = Column(Text, nullable=False)
    change_summary = Column(Text, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("ResearchDocument", back_populates="versions")


# 30. research_tasks
class ResearchTask(Base):
    __tablename__ = "research_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_project_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    deadline = Column(DateTime, nullable=True)
    priority = Column(String(50), default="Medium") # Low, Medium, High, Urgent
    status = Column(String(50), default="Todo") # Todo, In Progress, Review, Completed
    assigned_to = Column(String(255), nullable=True)
    converted_to_planner_id = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("ResearchProject", back_populates="tasks")


# 31. research_meetings
class ResearchMeeting(Base):
    __tablename__ = "research_meetings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_project_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    attendees = Column(JSONB, default=list) # List of attendee names/emails
    meeting_date = Column(DateTime, default=datetime.utcnow)
    agenda = Column(Text, nullable=True)
    meeting_notes = Column(Text, nullable=True)
    action_items = Column(JSONB, default=list) # [{item: str, owner: str, due_date: str}]
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("ResearchProject", back_populates="meetings")


# 32. research_feedback
class ResearchFeedback(Base):
    __tablename__ = "research_feedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_project_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    reviewer_name = Column(String(255), nullable=False)
    reviewer_role = Column(String(100), default="Supervisor") # Supervisor, Guide, Peer, External Reviewer
    feedback_text = Column(Text, nullable=False)
    action_taken = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("ResearchProject", back_populates="feedback")


# 33. research_ai_generations (17 AI research tools output persistence)
class ResearchAiGeneration(Base):
    __tablename__ = "research_ai_generations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_project_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tool_name = Column(String(100), nullable=False) # One of the 17 AI research tools
    input_prompt = Column(Text, nullable=False)
    generation_output = Column(JSONB, nullable=False) # Structured output or formatted response
    is_persisted_to_project = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("ResearchProject", back_populates="ai_generations")


# 34. research_conversations
class ResearchConversation(Base):
    __tablename__ = "research_conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_project_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), default="Research Assistant Chat")
    context_type = Column(String(50), default="Project") # Project, Paper, General
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("ResearchProject", back_populates="conversations")
    messages = relationship("ResearchConversationMessage", back_populates="conversation", cascade="all, delete-orphan", order_by="ResearchConversationMessage.created_at")


# 35. research_conversation_messages
class ResearchConversationMessage(Base):
    __tablename__ = "research_conversation_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_conversation_id = Column(UUID(as_uuid=True), ForeignKey("research_conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    sender_type = Column(String(20), default="user") # user, ai
    message_text = Column(Text, nullable=False)
    citations_data = Column(JSONB, default=list) # [{paper_title: str, page_number: int, quote: str}]
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("ResearchConversation", back_populates="messages")


# 36. research_activity_logs
class ResearchActivityLog(Base):
    __tablename__ = "research_activity_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_project_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    action_type = Column(String(100), nullable=False) # e.g. "paper_uploaded", "literature_review_created", "ai_tool_run"
    description = Column(Text, nullable=False)
    metadata_json = Column(JSONB, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("ResearchProject", back_populates="activity_logs")

