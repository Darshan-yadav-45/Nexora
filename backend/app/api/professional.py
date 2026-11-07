from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from app.database.connection import get_db
from app.models.user import User
from app.models.profile import UserProfile
from app.api.auth import get_current_user

router = APIRouter(prefix="/professional", tags=["professional"])

class ProfessionalProfileRequest(BaseModel):
    name: str
    preferred_name: Optional[str] = None
    profession: Optional[str] = None
    organization: Optional[str] = None
    skills: Optional[List[str]] = None
    interests: Optional[List[str]] = None
    career_goals: Optional[str] = None
    preferred_language: Optional[str] = "English"
    enabled_modules: Optional[List[str]] = None

@router.get("/profile")
async def get_professional_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(UserProfile).filter(UserProfile.user_id == current_user.id))
    profile = result.scalars().first()
    if not profile:
        profile = UserProfile(
            user_id=current_user.id,
            name=current_user.email.split("@")[0].capitalize(),
            profession="Senior Technology Specialist",
            organization="Nexora Global Systems",
            career_skills=["System Architecture", "AI Engineering", "PostgreSQL Administration"],
            research_interests=["Cloud Native Security", "Applied LLM Architectures"],
            enabled_modules=["study", "career", "research", "creator", "planner", "knowledge_base"]
        )
        db.add(profile)
        await db.commit()
        await db.refresh(profile)

    return {
        "name": profile.name,
        "preferred_name": profile.preferred_name,
        "profession": profile.profession or "Technology Professional",
        "organization": profile.organization or "Enterprise",
        "skills": profile.career_skills or [],
        "interests": profile.research_interests or [],
        "career_goals": profile.learning_goal or "Advance enterprise AI solutions",
        "preferred_language": profile.native_language or "English",
        "enabled_modules": profile.enabled_modules or ["study", "career", "research", "creator", "planner", "knowledge_base"]
    }

@router.post("/profile")
async def update_professional_profile(
    req: ProfessionalProfileRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(UserProfile).filter(UserProfile.user_id == current_user.id))
    profile = result.scalars().first()
    if not profile:
        profile = UserProfile(user_id=current_user.id, name=req.name)
        db.add(profile)

    profile.name = req.name
    profile.preferred_name = req.preferred_name or req.name
    profile.profession = req.profession
    profile.organization = req.organization
    if req.skills is not None:
        profile.career_skills = req.skills
    if req.interests is not None:
        profile.research_interests = req.interests
    if req.career_goals is not None:
        profile.learning_goal = req.career_goals
    if req.preferred_language is not None:
        profile.native_language = req.preferred_language
    if req.enabled_modules is not None:
        profile.enabled_modules = req.enabled_modules

    current_user.profile_completed = True
    await db.commit()
    await db.refresh(profile)
    return {"message": "Professional profile updated successfully", "profile": profile.name}
