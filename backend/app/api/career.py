import os
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import Response, PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database.connection import get_db
from app.models.user import User
from app.api.auth import get_current_user
from app.models.career import (
    CareerPath, CareerModule, CareerTopic, CareerSubtopic, TopicLearningContent,
    UserCareerEnrollment, UserTopicProgress, UserTopicNote, UserStudyTimetable, CustomRoadmap
)
from app.schemas.career import (
    CareerPathResponse, ModuleResponse, TopicBriefResponse, TopicLearningContentResponse,
    TopicProgressUpdateRequest, TopicNoteRequest, GenerateTimetableRequest,
    GenerateAiRoadmapRequest, ConfirmCustomRoadmapRequest
)
from app.services.text_extractor import DocumentTextExtractor
from app.services.ai_roadmap_service import AiRoadmapService
from app.services.career_seed import build_topic_content

router = APIRouter(prefix="/career", tags=["career"])

# -------------------------------------------------------------
# 1. Career Paths & Roadmaps Retrieval
# -------------------------------------------------------------

@router.get("/paths", response_model=List[CareerPathResponse])
async def get_career_paths(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns the three complete standard career paths plus any custom roadmaps
    created by the authenticated user.
    """
    stmt = (
        select(CareerPath)
        .filter((CareerPath.is_custom == False) | (CareerPath.user_id == current_user.id))
        .options(
            selectinload(CareerPath.modules).selectinload(CareerModule.topics).selectinload(CareerTopic.subtopics)
        )
        .order_by(CareerPath.is_custom, CareerPath.title)
    )
    result = await db.execute(stmt)
    paths = result.scalars().all()
    return paths

@router.get("/paths/{path_slug_or_id}", response_model=CareerPathResponse)
async def get_career_path_details(
    path_slug_or_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Retrieves full career path hierarchy: path -> modules -> topics -> subtopics."""
    try:
        path_uuid = uuid.UUID(path_slug_or_id)
        filter_clause = (CareerPath.id == path_uuid)
    except ValueError:
        filter_clause = (CareerPath.slug == path_slug_or_id)

    stmt = (
        select(CareerPath)
        .filter(filter_clause)
        .options(
            selectinload(CareerPath.modules).selectinload(CareerModule.topics).selectinload(CareerTopic.subtopics)
        )
    )
    result = await db.execute(stmt)
    path = result.scalars().first()
    if not path:
        raise HTTPException(status_code=404, detail="Career path not found")
    return path

# -------------------------------------------------------------
# 2. Comprehensive 17-Item Learning Content
# -------------------------------------------------------------

@router.get("/topics/{topic_id}/content", response_model=TopicLearningContentResponse)
async def get_topic_learning_content(
    topic_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves complete 17-component learning content for a topic.
    If not yet generated (e.g. For custom roadmap), generates it dynamically.
    """
    stmt = select(TopicLearningContent).filter(TopicLearningContent.career_topic_id == topic_id)
    result = await db.execute(stmt)
    content = result.scalars().first()

    if not content:
        # Fetch topic to generate dynamic content
        top_res = await db.execute(
            select(CareerTopic).filter(CareerTopic.id == topic_id).options(selectinload(CareerTopic.module))
        )
        topic = top_res.scalars().first()
        if not topic:
            raise HTTPException(status_code=404, detail="Topic not found")

        payload = build_topic_content(
            topic_name=topic.title,
            module_name=topic.module.title if topic.module else "Core Engineering",
            career_name="Custom Track",
            level=topic.level,
            primary_language="Python",
            key_terms=[f"{topic.title} Architecture", "Modular Synthesis", "State Integrity"],
            code_snippet=f"# Production Implementation for {topic.title}\ndef execute():\n    return 'Success'",
            output_snippet="Success"
        )
        content = TopicLearningContent(career_topic_id=topic_id, **payload)
        db.add(content)
        await db.commit()
        await db.refresh(content)

    return content

# -------------------------------------------------------------
# 3. User Enrollment & Career Switching
# -------------------------------------------------------------

@router.post("/enroll/{path_id}")
async def enroll_career_path(
    path_id: uuid.UUID,
    daily_study_hours: float = 2.0,
    weekly_target_hours: float = 10.0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Enrolls user in career path or changes active path without deleting previous progress.
    """
    # Check if enrollment exists
    stmt = select(UserCareerEnrollment).filter_by(user_id=current_user.id, career_path_id=path_id)
    result = await db.execute(stmt)
    enrollment = result.scalars().first()

    if not enrollment:
        target_date = datetime.utcnow() + timedelta(weeks=16)
        enrollment = UserCareerEnrollment(
            user_id=current_user.id,
            career_path_id=path_id,
            status="In Progress",
            daily_study_hours=daily_study_hours,
            weekly_target_hours=weekly_target_hours,
            target_completion_date=target_date,
            enrolled_at=datetime.utcnow()
        )
        db.add(enrollment)
    else:
        enrollment.status = "In Progress"
        enrollment.daily_study_hours = daily_study_hours
        enrollment.weekly_target_hours = weekly_target_hours
        enrollment.last_activity_at = datetime.utcnow()

    await db.commit()
    await db.refresh(enrollment)
    return {"message": "Enrolled successfully", "enrollment_id": enrollment.id, "status": enrollment.status}

@router.post("/enrollment/{path_id}/status")
async def update_enrollment_status(
    path_id: uuid.UUID,
    status_value: str, # "In Progress", "Paused", "Completed"
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(UserCareerEnrollment).filter_by(user_id=current_user.id, career_path_id=path_id)
    res = await db.execute(stmt)
    enrollment = res.scalars().first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    enrollment.status = status_value
    enrollment.last_activity_at = datetime.utcnow()
    await db.commit()
    return {"message": f"Career path status updated to {status_value}"}

# -------------------------------------------------------------
# 4. Progress, Quizzes & Personal Notes Tracking
# -------------------------------------------------------------

@router.get("/progress/{path_id}")
async def get_path_progress(
    path_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns user's progress records across all topics in a career path,
    calculating completion percentage, weak topics, and recommendation.
    """
    # Fetch all topics in path
    stmt = (
        select(CareerTopic)
        .join(CareerModule, CareerTopic.career_module_id == CareerModule.id)
        .filter(CareerModule.career_path_id == path_id)
        .order_by(CareerModule.order_index, CareerTopic.order_index)
    )
    res = await db.execute(stmt)
    topics = res.scalars().all()
    topic_ids = [t.id for t in topics]

    # Fetch user topic progress
    p_stmt = select(UserTopicProgress).filter(
        UserTopicProgress.user_id == current_user.id,
        UserTopicProgress.career_topic_id.in_(topic_ids)
    )
    p_res = await db.execute(p_stmt)
    progress_records = {p.career_topic_id: p for p in p_res.scalars().all()}

    # Fetch notes & bookmarks
    n_stmt = select(UserTopicNote).filter(
        UserTopicNote.user_id == current_user.id,
        UserTopicNote.career_topic_id.in_(topic_ids)
    )
    n_res = await db.execute(n_stmt)
    notes_records = {n.career_topic_id: n for n in n_res.scalars().all()}

    total_topics = len(topics)
    completed_topics = 0
    weak_topics = []
    next_recommended_topic = None

    topic_stats = []
    for t in topics:
        p = progress_records.get(t.id)
        n = notes_records.get(t.id)

        t_status = p.status if p else "Not Started"
        quiz_score = p.quiz_score if p else 0.0

        if t_status == "Completed":
            completed_topics += 1
        elif not next_recommended_topic and t_status in ["Not Started", "In Progress"]:
            next_recommended_topic = {"id": str(t.id), "title": t.title, "level": t.level}

        if t_status == "Needs Revision" or (p and p.quiz_score < 70.0 and t_status == "Completed"):
            weak_topics.append({"id": str(t.id), "title": t.title, "score": quiz_score, "reason": "Low assessment score or flagged for revision"})

        topic_stats.append({
            "topic_id": str(t.id),
            "title": t.title,
            "status": t_status,
            "quiz_score": quiz_score,
            "project_completed": p.project_completed if p else False,
            "time_spent_minutes": p.time_spent_minutes if p else 0,
            "is_bookmarked": n.is_bookmarked if n else False,
            "has_notes": bool(n and n.notes.strip()) if n else False
        })

    completion_percentage = (completed_topics / total_topics * 100.0) if total_topics > 0 else 0.0

    # Update enrollment completion percentage
    enr_stmt = select(UserCareerEnrollment).filter_by(user_id=current_user.id, career_path_id=path_id)
    enr_res = await db.execute(enr_stmt)
    enrollment = enr_res.scalars().first()
    if enrollment:
        enrollment.completion_percentage = round(completion_percentage, 1)
        if next_recommended_topic:
            enrollment.current_topic_id = uuid.UUID(next_recommended_topic["id"])
        await db.commit()

    return {
        "path_id": str(path_id),
        "total_topics": total_topics,
        "completed_topics": completed_topics,
        "completion_percentage": round(completion_percentage, 1),
        "next_recommended_topic": next_recommended_topic,
        "weak_topics": weak_topics,
        "topics": topic_stats
    }

@router.post("/topics/{topic_id}/progress")
async def update_topic_progress(
    topic_id: uuid.UUID,
    data: TopicProgressUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Updates progress, assessment score, and completion status for a topic."""
    stmt = select(UserTopicProgress).filter_by(user_id=current_user.id, career_topic_id=topic_id)
    res = await db.execute(stmt)
    progress = res.scalars().first()

    if not progress:
        progress = UserTopicProgress(
            user_id=current_user.id,
            career_topic_id=topic_id,
            status=data.status,
            quiz_score=data.quiz_score or 0.0,
            quiz_answers=data.quiz_answers or {},
            exercise_submissions=data.exercise_submissions or {},
            project_completed=data.project_completed or False,
            time_spent_minutes=data.time_spent_minutes or 0,
            completed_at=datetime.utcnow() if data.status == "Completed" else None
        )
        db.add(progress)
    else:
        progress.status = data.status
        if data.quiz_score is not None:
            progress.quiz_score = data.quiz_score
        if data.quiz_answers is not None:
            progress.quiz_answers = data.quiz_answers
        if data.exercise_submissions is not None:
            progress.exercise_submissions = data.exercise_submissions
        if data.project_completed is not None:
            progress.project_completed = data.project_completed
        if data.time_spent_minutes is not None:
            progress.time_spent_minutes += data.time_spent_minutes
        if data.status == "Completed" and not progress.completed_at:
            progress.completed_at = datetime.utcnow()

    await db.commit()
    return {"message": "Topic progress updated", "status": progress.status, "quiz_score": progress.quiz_score}

@router.get("/topics/{topic_id}/note")
async def get_topic_note(
    topic_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(UserTopicNote).filter_by(user_id=current_user.id, career_topic_id=topic_id)
    res = await db.execute(stmt)
    note = res.scalars().first()
    return {
        "topic_id": str(topic_id),
        "notes": note.notes if note else "",
        "is_bookmarked": note.is_bookmarked if note else False
    }

@router.post("/topics/{topic_id}/note")
async def save_topic_note(
    topic_id: uuid.UUID,
    data: TopicNoteRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(UserTopicNote).filter_by(user_id=current_user.id, career_topic_id=topic_id)
    res = await db.execute(stmt)
    note = res.scalars().first()

    if not note:
        note = UserTopicNote(
            user_id=current_user.id,
            career_topic_id=topic_id,
            notes=data.notes,
            is_bookmarked=data.is_bookmarked if data.is_bookmarked is not None else False
        )
        db.add(note)
    else:
        note.notes = data.notes
        if data.is_bookmarked is not None:
            note.is_bookmarked = data.is_bookmarked

    await db.commit()
    return {"message": "Note saved successfully", "is_bookmarked": note.is_bookmarked}

# -------------------------------------------------------------
# 5. Timetable Generator & Study Targets
# -------------------------------------------------------------

@router.post("/timetable/generate")
async def generate_study_timetable(
    data: GenerateTimetableRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generates a realistic day-by-day study schedule based on available daily hours
    and topic estimated learning times.
    """
    stmt = (
        select(CareerTopic)
        .join(CareerModule, CareerTopic.career_module_id == CareerModule.id)
        .filter(CareerModule.career_path_id == data.career_path_id)
        .order_by(CareerModule.order_index, CareerTopic.order_index)
    )
    res = await db.execute(stmt)
    topics = res.scalars().all()

    start_date = data.start_date or datetime.utcnow()
    current_date = start_date
    schedule = []
    
    daily_available_minutes = data.daily_study_hours * 60
    current_day_minutes_used = 0

    for topic in topics:
        topic_time = topic.estimated_minutes or 90
        
        while current_date.weekday() >= data.days_per_week:
            # Skip weekend days based on days_per_week
            current_date += timedelta(days=1)

        schedule.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "day_name": current_date.strftime("%A"),
            "topic_id": str(topic.id),
            "topic_title": topic.title,
            "estimated_minutes": topic_time,
            "level": topic.level
        })

        current_day_minutes_used += topic_time
        if current_day_minutes_used >= daily_available_minutes:
            current_date += timedelta(days=1)
            current_day_minutes_used = 0

    # Save to user_study_timetables
    tt_stmt = select(UserStudyTimetable).filter_by(user_id=current_user.id, career_path_id=data.career_path_id)
    tt_res = await db.execute(tt_stmt)
    existing_tt = tt_res.scalars().first()

    hours_dist = {"monday": data.daily_study_hours, "tuesday": data.daily_study_hours, "wednesday": data.daily_study_hours, "thursday": data.daily_study_hours, "friday": data.daily_study_hours}
    if existing_tt:
        existing_tt.available_hours_per_day = hours_dist
        existing_tt.schedule_items = schedule
    else:
        new_tt = UserStudyTimetable(
            user_id=current_user.id,
            career_path_id=data.career_path_id,
            available_hours_per_day=hours_dist,
            schedule_items=schedule
        )
        db.add(new_tt)

    await db.commit()
    return {
        "career_path_id": str(data.career_path_id),
        "total_days_scheduled": len(set(s["date"] for s in schedule)),
        "schedule": schedule
    }

# -------------------------------------------------------------
# 6. Custom Roadmap Upload & AI Roadmap Generator
# -------------------------------------------------------------

@router.post("/upload")
async def upload_custom_roadmap(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Master Requirement 1.D:
    Upload user's roadmap (PDF, DOC, DOCX, TXT, image) -> Extract text & structure ->
    Identify modules, topics, subtopics, prerequisites -> Identify missing/unclear topics ->
    Return extracted roadmap for user review before confirmation. Never automatically overwrite.
    """
    file_bytes = await file.read()
    filename = file.filename or "roadmap.txt"
    
    # 1. Extract text
    extracted_data = DocumentTextExtractor.extract(file_bytes, filename)
    raw_text = extracted_data.get("text", "")

    # 2. Parse modules and topics
    parsed_result = AiRoadmapService.parse_uploaded_roadmap_text(raw_text, filename)

    # 3. Store draft in custom_roadmaps table
    custom_record = CustomRoadmap(
        user_id=current_user.id,
        title=parsed_result["title"],
        source_filename=filename,
        extracted_raw_text=raw_text[:50000], # Cap preview text
        parsed_structure=parsed_result,
        missing_or_unclear_topics=parsed_result["missing_or_unclear_topics"],
        status="reviewed"
    )
    db.add(custom_record)
    await db.commit()
    await db.refresh(custom_record)

    return {
        "custom_roadmap_id": str(custom_record.id),
        "title": parsed_result["title"],
        "modules": parsed_result["modules"],
        "missing_or_unclear_topics": parsed_result["missing_or_unclear_topics"],
        "total_topics_count": parsed_result["total_topics_count"],
        "message": "Roadmap parsed successfully. Review and edit topics before confirming."
    }

@router.post("/generate-ai")
async def generate_ai_roadmap(
    data: GenerateAiRoadmapRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Master Requirement 1.E:
    AI-generated step-by-step roadmap from career goal, knowledge level, skills, preferences, and hours.
    """
    generated = AiRoadmapService.generate_personalized_roadmap(
        career_goal=data.career_goal,
        current_knowledge_level=data.current_knowledge_level,
        existing_skills=data.existing_skills,
        preferred_technologies=data.preferred_technologies,
        daily_study_hours=data.daily_study_hours,
        weekly_study_hours=data.weekly_study_hours,
        target_completion_weeks=data.target_completion_weeks,
        learning_preferences=data.learning_preferences,
        existing_roadmap_notes=data.existing_roadmap_notes or ""
    )

    # Save as custom roadmap draft for review
    custom_record = CustomRoadmap(
        user_id=current_user.id,
        title=generated["title"],
        source_filename="AI_Generator",
        extracted_raw_text=f"AI Roadmap for {data.career_goal}",
        parsed_structure=generated,
        status="reviewed"
    )
    db.add(custom_record)
    await db.commit()
    await db.refresh(custom_record)

    return {
        "custom_roadmap_id": str(custom_record.id),
        "roadmap": generated
    }

@router.post("/confirm")
async def confirm_custom_roadmap(
    data: ConfirmCustomRoadmapRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Saves the user-reviewed/edited roadmap permanently as a playable career path
    with complete modules, topics, subtopics, and comprehensive learning contents.
    Never overwrites existing roadmaps.
    """
    slug = f"user-{uuid.uuid4().hex[:8]}"
    
    career_path = CareerPath(
        slug=slug,
        title=data.title,
        description=f"Personalized roadmap confirmed by {current_user.email}",
        icon="Compass",
        estimated_weeks=16,
        total_hours=100,
        is_custom=True,
        user_id=current_user.id
    )
    db.add(career_path)
    await db.flush()

    for mod_idx, mod in enumerate(data.modules):
        module = CareerModule(
            career_path_id=career_path.id,
            title=mod.get("title", f"Module {mod_idx + 1}"),
            description=mod.get("description", "Structured learning phase"),
            order_index=mod_idx,
            difficulty_level=mod.get("difficulty", "Intermediate"),
            estimated_hours=mod.get("estimated_hours", 20)
        )
        db.add(module)
        await db.flush()

        for top_idx, top in enumerate(mod.get("topics", [])):
            top_title = top.get("title", f"Topic {top_idx + 1}")
            top_slug = top_title.lower().replace(" ", "-")[:80]
            
            topic = CareerTopic(
                career_module_id=module.id,
                title=top_title,
                slug=f"{top_slug}-{uuid.uuid4().hex[:4]}",
                summary=f"In-depth mastery of {top_title}",
                order_index=top_idx,
                prerequisites=top.get("prerequisites", ["Core basics"]),
                estimated_minutes=top.get("estimated_minutes", 90),
                level=top.get("level", "Intermediate")
            )
            db.add(topic)
            await db.flush()

            # Create subtopics
            for sub_idx, sub_title in enumerate(top.get("subtopics", ["Core Concepts", "Implementation"])):
                db.add(CareerSubtopic(
                    career_topic_id=topic.id,
                    title=sub_title,
                    order_index=sub_idx,
                    content_summary=f"Key technical details of {sub_title}"
                ))

            # Create 17-item learning content
            content_payload = build_topic_content(
                topic_name=top_title,
                module_name=module.title,
                career_name=data.title,
                level=topic.level,
                primary_language="Python",
                key_terms=[f"{top_title} Concepts", "Design Patterns", "Reliability"],
                code_snippet=f"# Practical Implementation for {top_title}\ndef run():\n    return 'Execution OK'",
                output_snippet="Execution OK"
            )
            db.add(TopicLearningContent(career_topic_id=topic.id, **content_payload))

    # Auto enroll user in their confirmed custom path
    enrollment = UserCareerEnrollment(
        user_id=current_user.id,
        career_path_id=career_path.id,
        status="In Progress",
        daily_study_hours=2.0,
        weekly_target_hours=10.0,
        enrolled_at=datetime.utcnow()
    )
    db.add(enrollment)

    # Update custom roadmap draft status
    draft_stmt = select(CustomRoadmap).filter_by(id=data.custom_roadmap_id, user_id=current_user.id)
    draft_res = await db.execute(draft_stmt)
    draft = draft_res.scalars().first()
    if draft:
        draft.status = "confirmed"
        draft.career_path_id = career_path.id

    await db.commit()
    return {
        "message": "Custom roadmap successfully created and enrolled!",
        "career_path_id": str(career_path.id),
        "slug": career_path.slug
    }

# -------------------------------------------------------------
# 7. Downloadable Progress Report
# -------------------------------------------------------------

@router.get("/report/{path_id}")
async def download_progress_report(
    path_id: uuid.UUID,
    format: str = "markdown", # markdown or json
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generates a downloadable career roadmap progress report.
    """
    path_res = await db.execute(select(CareerPath).filter_by(id=path_id))
    path = path_res.scalars().first()
    if not path:
        raise HTTPException(status_code=404, detail="Career path not found")

    progress_data = await get_path_progress(path_id, current_user, db)

    if format == "json":
        import json
        return Response(
            content=json.dumps(progress_data, indent=2),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=progress_report_{path.slug}.json"}
        )

    # Markdown format
    md_lines = [
        f"# Nexora AI — Career Roadmap Progress Report",
        f"**Candidate**: {current_user.email}",
        f"**Career Path**: {path.title}",
        f"**Generated At**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"**Overall Completion**: {progress_data['completion_percentage']}%",
        f"**Completed Topics**: {progress_data['completed_topics']} / {progress_data['total_topics']}",
        "",
        "## Summary of Performance",
        f"- **Next Recommended Topic**: {progress_data['next_recommended_topic']['title'] if progress_data['next_recommended_topic'] else 'All Topics Completed!'}",
        f"- **Weak Topics Requiring Revision**: {len(progress_data['weak_topics'])}",
        "",
        "## Detailed Topic Progress",
        "| Topic Name | Status | Quiz Score | Project Completed | Bookmarked |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]

    for t in progress_data["topics"]:
        score_str = f"{t['quiz_score']}%" if t['quiz_score'] > 0 else "N/A"
        proj_str = "Yes" if t["project_completed"] else "No"
        bm_str = "Yes" if t["is_bookmarked"] else "No"
        md_lines.append(f"| {t['title']} | {t['status']} | {score_str} | {proj_str} | {bm_str} |")

    if progress_data["weak_topics"]:
        md_lines.extend([
            "",
            "## Recommended Revision Areas",
            *[f"- **{w['title']}**: {w['reason']}" for w in progress_data["weak_topics"]]
        ])

    md_report = "\n".join(md_lines)
    return PlainTextResponse(
        content=md_report,
        headers={"Content-Disposition": f"attachment; filename=progress_report_{path.slug}.md"}
    )

