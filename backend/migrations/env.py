import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.database.connection import Base, DATABASE_URL
from app.models.user import User
from app.models.profile import UserProfile, LearningProfile
from app.models.character import Character
from app.models.career import CareerPath, CareerModule, CareerTopic, CareerSubtopic, TopicLearningContent, UserCareerEnrollment, UserTopicProgress, UserTopicNote, UserStudyTimetable, CustomRoadmap
from app.models.research import (
    ResearchProject, ResearchProjectMember, ResearchTopic, ResearchQuestion, ResearchObjective,
    ResearchPaper, ResearchPaperAuthor, ResearchPaperFile, ResearchPaperText, ResearchPaperPage,
    ResearchKeyword, ResearchPaperKeyword, ResearchProjectPaper, LiteratureReview, LiteratureReviewEntry,
    ResearchGapAnalysis, ResearchMethodology, ResearchVariable, ResearchDataset, ResearchExperiment,
    ResearchExperimentStep, ResearchResult, ResearchObservation, ResearchNote, ResearchHighlight,
    ResearchCitation, ResearchReference, ResearchDocument, ResearchDocumentVersion, ResearchTask,
    ResearchMeeting, ResearchFeedback, ResearchAiGeneration, ResearchConversation, ResearchConversationMessage,
    ResearchActivityLog
)
from app.models.integration import PlannerTask, KnowledgeBaseItem

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    # Use our database URL instead of the alembic.ini one
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = DATABASE_URL
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
