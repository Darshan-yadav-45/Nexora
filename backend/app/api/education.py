import uuid
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from pydantic import BaseModel

from app.database.connection import get_db
from app.models.user import User
from app.models.profile import UserProfile
from app.models.education import (
    StudentProfile, EducationRecord, UserSubject, Syllabus,
    StudyMaterial, LearningPreferences, CareerProfile, Skill, UserSkill,
    Resume, ResumeSection
)
from app.api.auth import get_current_user
from app.services.text_extractor import DocumentTextExtractor
from app.services.resume_parser import ResumeParserService

router = APIRouter(prefix="/education", tags=["education"])

# --- Schemas ---

class PersonalInfoRequest(BaseModel):
    name: str
    preferred_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[str] = None
    country: Optional[str] = "India"
    state: Optional[str] = None
    city: Optional[str] = None
    preferred_language: Optional[str] = "English"

class EducationRecordCreate(BaseModel):
    level: str # SSLC, PUC, Diploma, UG, PG, PhD, Other
    status: str # Completed, Currently studying, Not started
    institution_name: Optional[str] = None
    board_or_university: Optional[str] = None
    stream: Optional[str] = None
    degree_name: Optional[str] = None
    specialization: Optional[str] = None
    course_duration: Optional[str] = None
    admission_year: Optional[int] = None
    passing_year: Optional[int] = None
    expected_completion_year: Optional[int] = None
    current_class_or_year: Optional[str] = None
    current_semester: Optional[str] = None
    result_percentage_cgpa: Optional[str] = None
    research_title: Optional[str] = None
    research_guide: Optional[str] = None
    research_status: Optional[str] = None
    chronological_order: Optional[int] = 1
    extra_metadata: Optional[Dict[str, Any]] = None

class UserSubjectCreate(BaseModel):
    name: str
    code: Optional[str] = None
    credits: Optional[int] = None
    description: Optional[str] = None
    education_record_id: Optional[str] = None

class SyllabusTextCreate(BaseModel):
    title: str
    content_text: str

class StudyMaterialCreate(BaseModel):
    title: str
    material_type: str # lecture_notes, assignments, question_papers, lab_manuals, reference_urls, teacher_notes
    url: Optional[str] = None
    content_text: Optional[str] = None

class LearningPreferencesRequest(BaseModel):
    explanation_language: Optional[str] = "English"
    difficulty_level: Optional[str] = "Beginner" # Beginner, Intermediate, Advanced
    explanation_depth: Optional[str] = "detailed" # simple, detailed
    code_examples_required: Optional[bool] = True
    visual_explanations_required: Optional[bool] = True
    practice_questions_required: Optional[bool] = True
    mcqs_required: Optional[bool] = True
    viva_prep_required: Optional[bool] = False
    exam_prep_required: Optional[bool] = True

class CareerInfoRequest(BaseModel):
    career_goal: Optional[str] = None
    current_skills: Optional[List[str]] = None
    technologies_interested: Optional[List[str]] = None
    preferred_career_path: Optional[str] = "Python Full Stack Development"
    daily_learning_time_minutes: Optional[int] = 60
    target_completion_weeks: Optional[int] = 12

class ResumeConfirmRequest(BaseModel):
    resume_id: str
    education: Optional[List[Dict[str, Any]]] = None
    skills: Optional[List[Dict[str, Any]]] = None
    projects: Optional[List[Dict[str, Any]]] = None
    internships: Optional[List[Dict[str, Any]]] = None
    work_experience: Optional[List[Dict[str, Any]]] = None
    certifications: Optional[List[Dict[str, Any]]] = None
    achievements: Optional[List[str]] = None

# --- Step 1: Personal Information ---

@router.get("/personal-info")
async def get_personal_info(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(UserProfile).filter(UserProfile.user_id == current_user.id))
    profile = result.scalars().first()
    if not profile:
        profile = UserProfile(
            user_id=current_user.id,
            name=current_user.email.split("@")[0].capitalize(),
            preferred_name=current_user.email.split("@")[0].capitalize(),
            native_language="English",
            english_level="Intermediate"
        )
        db.add(profile)
        await db.commit()
        await db.refresh(profile)

    return {
        "full_name": profile.name,
        "preferred_name": profile.preferred_name,
        "email": current_user.email,
        "phone_number": profile.phone_number,
        "date_of_birth": profile.date_of_birth,
        "country": profile.country or "India",
        "state": profile.state,
        "city": profile.city,
        "preferred_language": profile.native_language or "English",
        "avatar_url": profile.avatar_url
    }

@router.post("/personal-info")
async def save_personal_info(
    req: PersonalInfoRequest,
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
    profile.phone_number = req.phone_number
    profile.date_of_birth = req.date_of_birth
    profile.country = req.country
    profile.state = req.state
    profile.city = req.city
    profile.native_language = req.preferred_language or "English"

    await db.commit()
    await db.refresh(profile)
    return {"message": "Personal information updated successfully", "profile": profile.name}

# --- Step 2: Education Records (SSLC, PUC, Diploma, UG, PG, PhD, Other) ---

@router.get("/records")
async def get_education_records(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(EducationRecord)
        .filter(EducationRecord.user_id == current_user.id)
        .order_by(EducationRecord.chronological_order.asc(), EducationRecord.created_at.asc())
    )
    records = result.scalars().all()
    return records

@router.post("/records")
async def create_education_record(
    req: EducationRecordCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    record = EducationRecord(
        user_id=current_user.id,
        level=req.level,
        status=req.status,
        institution_name=req.institution_name,
        board_or_university=req.board_or_university,
        stream=req.stream,
        degree_name=req.degree_name,
        specialization=req.specialization,
        course_duration=req.course_duration,
        admission_year=req.admission_year,
        passing_year=req.passing_year,
        expected_completion_year=req.expected_completion_year,
        current_class_or_year=req.current_class_or_year,
        current_semester=req.current_semester,
        result_percentage_cgpa=req.result_percentage_cgpa,
        research_title=req.research_title,
        research_guide=req.research_guide,
        research_status=req.research_status,
        chronological_order=req.chronological_order or 1,
        extra_metadata=req.extra_metadata or {}
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record

@router.delete("/records/{record_id}")
async def delete_education_record(
    record_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        rec_uuid = uuid.UUID(record_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid record ID")

    result = await db.execute(
        select(EducationRecord).filter(
            EducationRecord.id == rec_uuid,
            EducationRecord.user_id == current_user.id
        )
    )
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail="Education record not found")

    await db.delete(record)
    await db.commit()
    return {"message": "Record deleted successfully"}

# --- Step 3: Subjects & Syllabi Management ---

@router.get("/subjects")
async def get_user_subjects(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserSubject)
        .filter(UserSubject.user_id == current_user.id, UserSubject.is_active == True)
        .order_by(UserSubject.created_at.asc())
    )
    subjects = result.scalars().all()
    
    # Enrich with syllabi and materials counts
    enriched = []
    for s in subjects:
        syl_res = await db.execute(select(Syllabus).filter(Syllabus.user_subject_id == s.id))
        mat_res = await db.execute(select(StudyMaterial).filter(StudyMaterial.user_subject_id == s.id))
        syllabi = syl_res.scalars().all()
        materials = mat_res.scalars().all()
        enriched.append({
            "id": str(s.id),
            "name": s.name,
            "code": s.code,
            "credits": s.credits,
            "description": s.description,
            "education_record_id": str(s.education_record_id) if s.education_record_id else None,
            "syllabi_count": len(syllabi),
            "materials_count": len(materials),
            "syllabi": [{"id": str(sy.id), "title": sy.title, "source_type": sy.source_type} for sy in syllabi]
        })
    return enriched

@router.post("/subjects")
async def create_user_subject(
    req: UserSubjectCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    rec_id = None
    if req.education_record_id:
        try:
            rec_id = uuid.UUID(req.education_record_id)
        except ValueError:
            pass

    subject = UserSubject(
        user_id=current_user.id,
        education_record_id=rec_id,
        name=req.name,
        code=req.code,
        credits=req.credits,
        description=req.description,
        is_active=True
    )
    db.add(subject)
    await db.commit()
    await db.refresh(subject)
    return subject

@router.delete("/subjects/{subject_id}")
async def delete_user_subject(
    subject_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        sub_uuid = uuid.UUID(subject_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid subject ID")

    result = await db.execute(
        select(UserSubject).filter(
            UserSubject.id == sub_uuid,
            UserSubject.user_id == current_user.id
        )
    )
    subject = result.scalars().first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    await db.delete(subject)
    await db.commit()
    return {"message": "Subject removed successfully"}

@router.post("/subjects/{subject_id}/syllabus-file")
async def upload_subject_syllabus_file(
    subject_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        sub_uuid = uuid.UUID(subject_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid subject ID")

    # Check subject ownership
    sub_res = await db.execute(select(UserSubject).filter(UserSubject.id == sub_uuid, UserSubject.user_id == current_user.id))
    subject = sub_res.scalars().first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    file_bytes = await file.read()
    extracted = DocumentTextExtractor.extract(file_bytes, file.filename)

    syllabus = Syllabus(
        user_subject_id=subject.id,
        user_id=current_user.id,
        title=f"Syllabus: {file.filename}",
        source_type="file_upload",
        file_name=file.filename,
        content_text=extracted.get("text", "")
    )
    db.add(syllabus)
    await db.commit()
    await db.refresh(syllabus)
    return {"message": "Syllabus file uploaded and text extracted", "syllabus_id": str(syllabus.id)}

@router.post("/subjects/{subject_id}/syllabus-text")
async def paste_subject_syllabus_text(
    subject_id: str,
    req: SyllabusTextCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        sub_uuid = uuid.UUID(subject_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid subject ID")

    sub_res = await db.execute(select(UserSubject).filter(UserSubject.id == sub_uuid, UserSubject.user_id == current_user.id))
    subject = sub_res.scalars().first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    syllabus = Syllabus(
        user_subject_id=subject.id,
        user_id=current_user.id,
        title=req.title or f"Syllabus for {subject.name}",
        source_type="pasted_text",
        content_text=req.content_text
    )
    db.add(syllabus)
    await db.commit()
    await db.refresh(syllabus)
    return {"message": "Syllabus text saved", "syllabus_id": str(syllabus.id)}

@router.post("/subjects/{subject_id}/materials")
async def add_study_material(
    subject_id: str,
    req: StudyMaterialCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        sub_uuid = uuid.UUID(subject_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid subject ID")

    sub_res = await db.execute(select(UserSubject).filter(UserSubject.id == sub_uuid, UserSubject.user_id == current_user.id))
    subject = sub_res.scalars().first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    material = StudyMaterial(
        user_subject_id=subject.id,
        user_id=current_user.id,
        title=req.title,
        material_type=req.material_type,
        url=req.url,
        content_text=req.content_text
    )
    db.add(material)
    await db.commit()
    await db.refresh(material)
    return material

# --- Step 4: Learning Preferences ---

@router.get("/learning-preferences")
async def get_learning_preferences(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(LearningPreferences).filter(LearningPreferences.user_id == current_user.id))
    pref = result.scalars().first()
    if not pref:
        pref = LearningPreferences(user_id=current_user.id)
        db.add(pref)
        await db.commit()
        await db.refresh(pref)
    return pref

@router.post("/learning-preferences")
async def save_learning_preferences(
    req: LearningPreferencesRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(LearningPreferences).filter(LearningPreferences.user_id == current_user.id))
    pref = result.scalars().first()
    if not pref:
        pref = LearningPreferences(user_id=current_user.id)
        db.add(pref)

    pref.explanation_language = req.explanation_language or "English"
    pref.difficulty_level = req.difficulty_level or "Beginner"
    pref.explanation_depth = req.explanation_depth or "detailed"
    pref.code_examples_required = req.code_examples_required
    pref.visual_explanations_required = req.visual_explanations_required
    pref.practice_questions_required = req.practice_questions_required
    pref.mcqs_required = req.mcqs_required
    pref.viva_prep_required = req.viva_prep_required
    pref.exam_prep_required = req.exam_prep_required

    await db.commit()
    await db.refresh(pref)
    return pref

# --- Step 5: Career Information ---

@router.get("/career-info")
async def get_career_info(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(CareerProfile).filter(CareerProfile.user_id == current_user.id))
    profile = result.scalars().first()
    if not profile:
        profile = CareerProfile(
            user_id=current_user.id,
            career_goal="Full Stack AI Engineer",
            preferred_career_path="Python Full Stack Development",
            current_skills=["Python", "SQL", "Git"],
            technologies_interested=["FastAPI", "React", "PostgreSQL", "Docker"]
        )
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
    return profile

@router.post("/career-info")
async def save_career_info(
    req: CareerInfoRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(CareerProfile).filter(CareerProfile.user_id == current_user.id))
    profile = result.scalars().first()
    if not profile:
        profile = CareerProfile(user_id=current_user.id)
        db.add(profile)

    if req.career_goal is not None:
        profile.career_goal = req.career_goal
    if req.current_skills is not None:
        profile.current_skills = req.current_skills
    if req.technologies_interested is not None:
        profile.technologies_interested = req.technologies_interested
    if req.preferred_career_path is not None:
        profile.preferred_career_path = req.preferred_career_path
    if req.daily_learning_time_minutes is not None:
        profile.daily_learning_time_minutes = req.daily_learning_time_minutes
    if req.target_completion_weeks is not None:
        profile.target_completion_weeks = req.target_completion_weeks

    await db.commit()
    await db.refresh(profile)
    return profile

# --- Step 6: Resume Upload & Extraction Flow ---

@router.post("/resume/upload")
async def upload_and_parse_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    file_bytes = await file.read()
    extracted = DocumentTextExtractor.extract(file_bytes, file.filename)
    raw_text = extracted.get("text", "")

    # Parse sections intelligently
    parsed_sections = ResumeParserService.parse_resume_text(raw_text)

    # Save Resume record
    resume = Resume(
        user_id=current_user.id,
        file_name=file.filename,
        extracted_text=raw_text,
        status="parsed"
    )
    db.add(resume)
    await db.flush()

    # Save ResumeSection entries for granular user review
    for sec_name, sec_data in parsed_sections.items():
        if sec_name == "raw_word_count":
            continue
        sec = ResumeSection(
            resume_id=resume.id,
            user_id=current_user.id,
            section_name=sec_name,
            content_data=sec_data if isinstance(sec_data, list) else [sec_data],
            is_confirmed=False
        )
        db.add(sec)

    await db.commit()
    await db.refresh(resume)

    return {
        "message": "Resume successfully uploaded and parsed for user review.",
        "resume_id": str(resume.id),
        "file_name": file.filename,
        "parsed_sections": parsed_sections,
        "requires_user_confirmation": True
    }

@router.post("/resume/confirm")
async def confirm_resume_sections(
    req: ResumeConfirmRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        res_uuid = uuid.UUID(req.resume_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid resume ID")

    res_record = await db.execute(select(Resume).filter(Resume.id == res_uuid, Resume.user_id == current_user.id))
    resume = res_record.scalars().first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Update resume status
    resume.status = "confirmed"

    # Merge confirmed skills into user_skills
    if req.skills:
        for sk in req.skills:
            skill_name = sk.get("name") if isinstance(sk, dict) else str(sk)
            if skill_name:
                db_skill = UserSkill(
                    user_id=current_user.id,
                    skill_name=skill_name,
                    category=sk.get("category", "General") if isinstance(sk, dict) else "General",
                    proficiency="Intermediate",
                    source="resume"
                )
                db.add(db_skill)

    # Merge confirmed education records
    if req.education:
        for ed in req.education:
            ed_rec = EducationRecord(
                user_id=current_user.id,
                level=ed.get("level", "Undergraduate (UG)"),
                status=ed.get("status", "Completed"),
                institution_name=ed.get("institution_name"),
                degree_name=ed.get("degree_name"),
                specialization=ed.get("specialization"),
                chronological_order=2
            )
            db.add(ed_rec)

    await db.commit()
    return {"message": "Resume details confirmed and merged into profile successfully."}

# --- Step 7: Education Timeline & Profile Completion ---

@router.get("/timeline")
async def get_education_timeline(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    standard_stages = [
        {"key": "sslc", "label": "SSLC / 10th", "level_match": "SSLC"},
        {"key": "puc", "label": "PUC / 12th", "level_match": "PUC"},
        {"key": "diploma_ug", "label": "Diploma / Undergraduate (UG)", "level_match": ["Diploma", "Undergraduate (UG)"]},
        {"key": "pg", "label": "Postgraduate (PG)", "level_match": "Postgraduate (PG)"},
        {"key": "phd_other", "label": "PhD / Other", "level_match": ["PhD", "Other"]}
    ]

    result = await db.execute(select(EducationRecord).filter(EducationRecord.user_id == current_user.id))
    records = result.scalars().all()

    timeline = []
    for stage in standard_stages:
        matches = []
        for r in records:
            if isinstance(stage["level_match"], list):
                if any(m.lower() in r.level.lower() for m in stage["level_match"]):
                    matches.append(r)
            else:
                if stage["level_match"].lower() in r.level.lower():
                    matches.append(r)

        if matches:
            first = matches[0]
            timeline.append({
                "stage": stage["label"],
                "status": first.status, # Completed, Currently studying
                "institution": first.institution_name,
                "degree": first.degree_name or first.level,
                "record_id": str(first.id),
                "has_entry": True
            })
        else:
            timeline.append({
                "stage": stage["label"],
                "status": "Not Added",
                "institution": None,
                "degree": None,
                "record_id": None,
                "has_entry": False
            })

    return {
        "timeline": timeline,
        "completed_count": sum(1 for t in timeline if t["status"] == "Completed"),
        "ongoing_count": sum(1 for t in timeline if t["status"] == "Currently studying"),
        "total_stages": len(timeline)
    }

@router.post("/complete")
async def mark_education_profile_complete(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    current_user.profile_completed = True
    current_user.first_time_login = False
    await db.commit()
    await db.refresh(current_user)
    return {
        "message": "Education journey completed! Profile marked active.",
        "profile_completed": True,
        "redirect_to": "/dashboard"
    }
