import uuid
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.connection import get_db
from app.models.user import User
from app.api.auth import get_current_user
from app.models.profile import UserProfile
from app.models.research import ResearchProject, ResearchTask, ResearchDocument, ResearchPaper
from app.models.integration import PlannerTask, KnowledgeBaseItem
from app.schemas.integration import (
    PlannerTaskCreate, PlannerTaskUpdate, PlannerTaskResponse,
    KnowledgeBaseItemCreate, KnowledgeBaseItemResponse, ConnectCareerSkillRequest
)

router = APIRouter(prefix="/integration", tags=["integration"])

# -------------------------------------------------------------
# 1. Planner Tasks Integration
# -------------------------------------------------------------

@router.get("/planner/tasks", response_model=List[PlannerTaskResponse])
async def list_planner_tasks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(PlannerTask).filter(PlannerTask.user_id == current_user.id).order_by(PlannerTask.due_date.asc().nulls_last(), PlannerTask.created_at.desc())
    res = await db.execute(stmt)
    return res.scalars().all()

@router.post("/planner/tasks", response_model=PlannerTaskResponse)
async def create_planner_task(
    data: PlannerTaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    task = PlannerTask(
        user_id=current_user.id,
        title=data.title,
        description=data.description,
        due_date=data.due_date,
        priority=data.priority or "Medium",
        status=data.status or "Todo",
        source_module=data.source_module or "manual",
        source_id=data.source_id,
        tags=data.tags or []
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

@router.post("/planner/convert-research-task/{task_id}", response_model=PlannerTaskResponse)
async def convert_research_task_to_planner(
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Master Requirement 3:
    Converts a research task directly into a Planner task.
    """
    stmt = select(ResearchTask).filter_by(id=task_id, user_id=current_user.id)
    res = await db.execute(stmt)
    rt = res.scalars().first()
    if not rt:
        raise HTTPException(status_code=404, detail="Research task not found")

    planner_task = PlannerTask(
        user_id=current_user.id,
        title=f"[Research] {rt.title}",
        description=rt.description,
        due_date=rt.deadline,
        priority=rt.priority,
        status="Todo",
        source_module="research",
        source_id=rt.id,
        tags=["research", "project"]
    )
    db.add(planner_task)
    await db.flush()

    rt.converted_to_planner_id = planner_task.id
    await db.commit()
    await db.refresh(planner_task)
    return planner_task

@router.put("/planner/tasks/{task_id}", response_model=PlannerTaskResponse)
async def update_planner_task(
    task_id: uuid.UUID,
    data: PlannerTaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(PlannerTask).filter_by(id=task_id, user_id=current_user.id)
    res = await db.execute(stmt)
    task = res.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Planner task not found")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(task, k, v)
    task.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(task)
    return task

@router.delete("/planner/tasks/{task_id}")
async def delete_planner_task(
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(PlannerTask).filter_by(id=task_id, user_id=current_user.id)
    res = await db.execute(stmt)
    task = res.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Planner task not found")

    await db.delete(task)
    await db.commit()
    return {"message": "Planner task deleted"}

# -------------------------------------------------------------
# 2. Personal Knowledge Base Integration
# -------------------------------------------------------------

@router.get("/knowledge-base/items", response_model=List[KnowledgeBaseItemResponse])
async def list_knowledge_base_items(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(KnowledgeBaseItem).filter_by(user_id=current_user.id).order_by(KnowledgeBaseItem.created_at.desc())
    res = await db.execute(stmt)
    return res.scalars().all()

@router.post("/knowledge-base/items", response_model=KnowledgeBaseItemResponse)
async def create_knowledge_base_item(
    data: KnowledgeBaseItemCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    item = KnowledgeBaseItem(
        user_id=current_user.id,
        title=data.title,
        category=data.category or "General",
        tags=data.tags or [],
        content=data.content,
        source_type=data.source_type or "manual",
        source_id=data.source_id
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

@router.post("/knowledge-base/save-paper/{paper_id}", response_model=KnowledgeBaseItemResponse)
async def save_paper_to_knowledge_base(
    paper_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Saves a research paper summary to Personal Knowledge Base."""
    stmt = select(ResearchPaper).filter_by(id=paper_id, user_id=current_user.id)
    res = await db.execute(stmt)
    paper = res.scalars().first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    content = f"### {paper.title}\n\n**Year**: {paper.publication_year}\n**Journal/Conference**: {paper.journal_or_conference}\n\n#### Abstract\n{paper.abstract}\n\n#### Notes\n{paper.user_notes or 'No notes added.'}"
    item = KnowledgeBaseItem(
        user_id=current_user.id,
        title=f"Paper: {paper.title}",
        category="Research Papers",
        tags=["research", "literature"],
        content=content,
        source_type="research_paper",
        source_id=paper.id
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

# -------------------------------------------------------------
# 3. Career Profile Skills & Research Cross-Connection
# -------------------------------------------------------------

@router.post("/profile/add-skill")
async def add_skill_to_career_profile(
    data: ConnectCareerSkillRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Master Requirement 3:
    Allow users to add research-related skills to their Career profile.
    """
    stmt = select(UserProfile).filter_by(user_id=current_user.id)
    res = await db.execute(stmt)
    profile = res.scalars().first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found. Please complete onboarding.")

    current_skills = list(profile.career_skills or [])
    # Check if skill exists
    if not any(s.get("name", "").lower() == data.skill_name.lower() for s in current_skills):
        current_skills.append({
            "name": data.skill_name,
            "domain": data.domain,
            "proficiency": data.proficiency,
            "added_at": datetime.utcnow().strftime("%Y-%m-%d")
        })
        profile.career_skills = current_skills
        await db.commit()

    return {"message": f"Skill '{data.skill_name}' added to Career profile", "skills": profile.career_skills}

@router.get("/profile/skills")
async def get_career_skills(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(UserProfile).filter_by(user_id=current_user.id)
    res = await db.execute(stmt)
    profile = res.scalars().first()
    return {"career_skills": profile.career_skills if profile else []}

# -------------------------------------------------------------
# 4. Project Documentation & Presentation Generation
# -------------------------------------------------------------

@router.post("/projects/{project_id}/generate-documentation")
async def generate_project_documentation(
    project_id: uuid.UUID,
    doc_type: str = "Technical Report", # Technical Report, Presentation Slides, Executive Summary
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Master Requirement 3:
    Generates structured project documentation or presentation slides from approved research data.
    """
    stmt = select(ResearchProject).filter_by(id=project_id, user_id=current_user.id)
    res = await db.execute(stmt)
    project = res.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Research project not found")

    if doc_type == "Presentation Slides":
        content = (
            f"# {project.title}\n"
            f"### Research Presentation & Findings\n"
            f"**Author**: {current_user.email} | **Domain**: {project.domain_area or 'Computer Science'}\n\n"
            f"---\n\n"
            f"## Slide 1: Problem & Motivation\n"
            f"- **Problem Statement**: {project.problem_statement or 'Investigating core architectural challenges.'}\n"
            f"- **Background**: {project.background_context or 'Recent advancements demand scalable solutions.'}\n\n"
            f"---\n\n"
            f"## Slide 2: Methodology & Objectives\n"
            f"- **Type**: {project.research_type}\n"
            f"- **Methodology**: {project.methodology_overview or 'Empirical quantitative evaluation.'}\n\n"
            f"---\n\n"
            f"## Slide 3: Expected Outcomes & Impact\n"
            f"- {project.expected_outcomes or 'Statistically significant improvements over established baselines.'}\n"
            f"- Industrial translation to production microservices."
        )
    else:
        content = (
            f"# Technical Project Report: {project.title}\n"
            f"**Domain**: {project.domain_area} | **Status**: {project.status}\n\n"
            f"## 1. Abstract\n{project.abstract or 'Abstract in progress.'}\n\n"
            f"## 2. Problem Statement\n{project.problem_statement or 'Problem statement details.'}\n\n"
            f"## 3. Background & Literature Context\n{project.background_context or 'Background context.'}\n\n"
            f"## 4. Methodology & Scope\n{project.methodology_overview or 'Methodological framework.'}\n\n"
            f"## 5. Scope & Limitations\n{project.scope_and_limitations or 'Scope definitions.'}\n\n"
            f"## 6. Expected Outcomes\n{project.expected_outcomes or 'Outcome projections.'}"
        )

    # Save to research_documents
    doc = ResearchDocument(
        research_project_id=project.id,
        user_id=current_user.id,
        document_title=f"{project.title} - {doc_type}",
        document_type=doc_type,
        content_markdown=content,
        status="Approved"
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)

    return {
        "document_id": str(doc.id),
        "title": doc.document_title,
        "content_markdown": doc.content_markdown
    }

