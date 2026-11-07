from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.connection import get_db
from app.models.user import User
from app.models.profile import UserProfile, LearningProfile
from app.schemas.profile import UserProfileCreate, UserProfileResponse, LearningProfileResponse
from app.api.auth import get_current_user

router = APIRouter(prefix="/profile", tags=["profile"])

@router.post("/", response_model=UserProfileResponse)
async def create_profile(
    profile: UserProfileCreate, 
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    # Check if profile already exists
    result = await db.execute(select(UserProfile).filter(UserProfile.user_id == current_user.id))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Profile already exists for this user")
    
    # Create UserProfile
    db_profile = UserProfile(
        user_id=current_user.id,
        name=profile.name,
        preferred_name=profile.preferred_name,
        native_language=profile.native_language,
        english_level=profile.english_level,
        learning_goal=profile.learning_goal,
        timezone=profile.timezone
    )
    db.add(db_profile)
    
    # Create empty LearningProfile
    db_learning = LearningProfile(user_id=current_user.id)
    db.add(db_learning)
    
    await db.commit()
    await db.refresh(db_profile)
    
    return db_profile

@router.get("/", response_model=UserProfileResponse)
async def get_profile(
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(UserProfile).filter(UserProfile.user_id == current_user.id))
    profile = result.scalars().first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.get("/learning", response_model=LearningProfileResponse)
async def get_learning_profile(
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(LearningProfile).filter(LearningProfile.user_id == current_user.id))
    learning_profile = result.scalars().first()
    if not learning_profile:
        raise HTTPException(status_code=404, detail="Learning profile not found")
    return learning_profile
