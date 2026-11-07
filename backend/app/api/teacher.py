from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from app.database.connection import get_db
from app.models.user import User
from app.models.education import TeacherProfile
from app.api.auth import get_current_user
from app.services.teacher_service import TeacherAIService

router = APIRouter(prefix="/teacher", tags=["teacher"])

class TeacherProfileRequest(BaseModel):
    institution: Optional[str] = None
    teaching_position: Optional[str] = None
    department: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    teaching_experience_years: Optional[float] = 0.0
    subjects_taught: Optional[List[str]] = None
    current_classes_semesters: Optional[List[str]] = None

class TeacherAIAssistRequest(BaseModel):
    tool_type: str # lesson_plan, lecture_notes, mcqs, assignments, viva_questions, revision_material
    subject_name: str
    topic: str
    grade_or_sem: Optional[str] = "Semester 5"

@router.get("/profile")
async def get_teacher_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(TeacherProfile).filter(TeacherProfile.user_id == current_user.id))
    profile = result.scalars().first()
    if not profile:
        profile = TeacherProfile(
            user_id=current_user.id,
            institution="National Institute of Technology",
            teaching_position="Assistant Professor",
            department="Computer Science & Engineering",
            qualification="M.Tech, Ph.D",
            specialization="Distributed Computing & AI",
            teaching_experience_years=5.0,
            subjects_taught=["Data Structures & Algorithms", "Database Management Systems", "Artificial Intelligence"],
            current_classes_semesters=["B.Tech 3rd Sem", "B.Tech 5th Sem"]
        )
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
    return profile

@router.post("/profile")
async def update_teacher_profile(
    req: TeacherProfileRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(TeacherProfile).filter(TeacherProfile.user_id == current_user.id))
    profile = result.scalars().first()
    if not profile:
        profile = TeacherProfile(user_id=current_user.id)
        db.add(profile)

    if req.institution is not None:
        profile.institution = req.institution
    if req.teaching_position is not None:
        profile.teaching_position = req.teaching_position
    if req.department is not None:
        profile.department = req.department
    if req.qualification is not None:
        profile.qualification = req.qualification
    if req.specialization is not None:
        profile.specialization = req.specialization
    if req.teaching_experience_years is not None:
        profile.teaching_experience_years = req.teaching_experience_years
    if req.subjects_taught is not None:
        profile.subjects_taught = req.subjects_taught
    if req.current_classes_semesters is not None:
        profile.current_classes_semesters = req.current_classes_semesters

    current_user.profile_completed = True
    await db.commit()
    await db.refresh(profile)
    return profile

@router.post("/ai-assist")
async def generate_teaching_materials(
    req: TeacherAIAssistRequest,
    current_user: User = Depends(get_current_user)
):
    output = TeacherAIService.generate_pedagogical_material(
        tool_type=req.tool_type,
        subject_name=req.subject_name,
        topic=req.topic,
        grade_or_sem=req.grade_or_sem or "Class / Semester"
    )
    return output
