from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.database.database import get_db
from app.models.user import User, UserProfile, Education, Skill, UserSkill, Internship, Project, Certification, ResearchProfile, CreatorProfile, UserSettings
from app.schemas.profile import (
    UserProfileUpdate, UserProfileResponse,
    EducationCreate, EducationUpdate, EducationResponse,
    SkillBase, SkillResponse, UserSkillCreate, UserSkillUpdate, UserSkillResponse,
    InternshipCreate, InternshipUpdate, InternshipResponse,
    ProjectCreate, ProjectUpdate, ProjectResponse,
    CertificationCreate, CertificationUpdate, CertificationResponse,
    ResearchProfileUpdate, ResearchProfileResponse,
    CreatorProfileUpdate, CreatorProfileResponse,
    UserSettingsUpdate, UserSettingsResponse
)
from app.api.dependencies import get_current_user

router = APIRouter()

# --- User Profile ---

@router.get("/me", response_model=UserProfileResponse)
def get_my_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("/me", response_model=UserProfileResponse)
def update_my_profile(profile_data: UserProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    update_data = profile_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)
    
    db.commit()
    db.refresh(profile)
    return profile

# --- Education ---

@router.get("/education", response_model=List[EducationResponse])
def get_education(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Education).filter(Education.user_id == current_user.id).all()

@router.post("/education", response_model=EducationResponse)
def add_education(education_data: EducationCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    education = Education(**education_data.model_dump(), user_id=current_user.id)
    db.add(education)
    db.commit()
    db.refresh(education)
    return education

@router.delete("/education/{education_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_education(education_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    education = db.query(Education).filter(Education.id == education_id, Education.user_id == current_user.id).first()
    if not education:
        raise HTTPException(status_code=404, detail="Education record not found")
    db.delete(education)
    db.commit()

# --- Skills ---

@router.get("/skills", response_model=List[UserSkillResponse])
def get_skills(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(UserSkill).filter(UserSkill.user_id == current_user.id).all()

@router.post("/skills", response_model=UserSkillResponse)
def add_skill(skill_data: UserSkillCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Find or create skill in global table
    skill = db.query(Skill).filter(Skill.name.ilike(skill_data.skill_name)).first()
    if not skill:
        skill = Skill(name=skill_data.skill_name.title())
        db.add(skill)
        db.commit()
        db.refresh(skill)
    
    # Check if user already has it
    user_skill = db.query(UserSkill).filter(UserSkill.user_id == current_user.id, UserSkill.skill_id == skill.id).first()
    if user_skill:
        raise HTTPException(status_code=400, detail="Skill already added")
        
    user_skill = UserSkill(
        user_id=current_user.id, 
        skill_id=skill.id, 
        skill_level=skill_data.skill_level,
        experience_months=skill_data.experience_months
    )
    db.add(user_skill)
    db.commit()
    db.refresh(user_skill)
    return user_skill

@router.delete("/skills/{user_skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(user_skill_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_skill = db.query(UserSkill).filter(UserSkill.id == user_skill_id, UserSkill.user_id == current_user.id).first()
    if not user_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    db.delete(user_skill)
    db.commit()

# --- Internships ---

@router.get("/internships", response_model=List[InternshipResponse])
def get_internships(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Internship).filter(Internship.user_id == current_user.id).all()

@router.post("/internships", response_model=InternshipResponse)
def add_internship(internship_data: InternshipCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    internship = Internship(**internship_data.model_dump(), user_id=current_user.id)
    db.add(internship)
    db.commit()
    db.refresh(internship)
    return internship

@router.delete("/internships/{internship_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_internship(internship_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    internship = db.query(Internship).filter(Internship.id == internship_id, Internship.user_id == current_user.id).first()
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")
    db.delete(internship)
    db.commit()

# --- Projects ---

@router.get("/projects", response_model=List[ProjectResponse])
def get_projects(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Project).filter(Project.user_id == current_user.id).all()

@router.post("/projects", response_model=ProjectResponse)
def add_project(project_data: ProjectCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = Project(**project_data.model_dump(), user_id=current_user.id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()

# --- Certifications ---

@router.get("/certifications", response_model=List[CertificationResponse])
def get_certifications(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Certification).filter(Certification.user_id == current_user.id).all()

@router.post("/certifications", response_model=CertificationResponse)
def add_certification(cert_data: CertificationCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cert = Certification(**cert_data.model_dump(), user_id=current_user.id)
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert

@router.delete("/certifications/{cert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_certification(cert_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cert = db.query(Certification).filter(Certification.id == cert_id, Certification.user_id == current_user.id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found")
    db.delete(cert)
    db.commit()

# --- Singleton Profiles (Research, Creator, Settings) ---

@router.get("/research", response_model=ResearchProfileResponse)
def get_research_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(ResearchProfile).filter(ResearchProfile.user_id == current_user.id).first()
    if not profile:
        profile = ResearchProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

@router.put("/research", response_model=ResearchProfileResponse)
def update_research_profile(data: ResearchProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(ResearchProfile).filter(ResearchProfile.user_id == current_user.id).first()
    if not profile:
        profile = ResearchProfile(user_id=current_user.id)
        db.add(profile)
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)
    
    db.commit()
    db.refresh(profile)
    return profile

@router.get("/creator", response_model=CreatorProfileResponse)
def get_creator_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(CreatorProfile).filter(CreatorProfile.user_id == current_user.id).first()
    if not profile:
        profile = CreatorProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

@router.put("/creator", response_model=CreatorProfileResponse)
def update_creator_profile(data: CreatorProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(CreatorProfile).filter(CreatorProfile.user_id == current_user.id).first()
    if not profile:
        profile = CreatorProfile(user_id=current_user.id)
        db.add(profile)
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)
    
    db.commit()
    db.refresh(profile)
    return profile

@router.get("/settings", response_model=UserSettingsResponse)
def get_settings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    settings = db.query(UserSettings).filter(UserSettings.user_id == current_user.id).first()
    if not settings:
        settings = UserSettings(user_id=current_user.id)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings

@router.put("/settings", response_model=UserSettingsResponse)
def update_settings(data: UserSettingsUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    settings = db.query(UserSettings).filter(UserSettings.user_id == current_user.id).first()
    if not settings:
        settings = UserSettings(user_id=current_user.id)
        db.add(settings)
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(settings, key, value)
    
    db.commit()
    db.refresh(settings)
    return settings
