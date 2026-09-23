from pydantic import BaseModel, HttpUrl, Field
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List

class UserProfileBase(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    preferred_name: Optional[str] = None
    profile_photo_url: Optional[str] = None
    date_of_birth: Optional[date] = None
    bio: Optional[str] = None
    timezone: Optional[str] = None

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    preferred_name: Optional[str] = None
    profile_photo_url: Optional[str] = None
    date_of_birth: Optional[date] = None
    bio: Optional[str] = None
    timezone: Optional[str] = None

class UserProfileResponse(UserProfileBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EducationBase(BaseModel):
    education_level: str
    degree: str
    university: str
    college: Optional[str] = None
    department: Optional[str] = None
    semester: Optional[str] = None
    academic_year: Optional[str] = None
    graduation_year: Optional[int] = None

class EducationCreate(EducationBase):
    pass

class EducationUpdate(BaseModel):
    education_level: Optional[str] = None
    degree: Optional[str] = None
    university: Optional[str] = None
    college: Optional[str] = None
    department: Optional[str] = None
    semester: Optional[str] = None
    academic_year: Optional[str] = None
    graduation_year: Optional[int] = None

class EducationResponse(EducationBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SkillBase(BaseModel):
    name: str

class SkillResponse(SkillBase):
    id: UUID
    class Config:
        from_attributes = True

class UserSkillBase(BaseModel):
    skill_level: Optional[str] = None
    experience_months: Optional[int] = None

class UserSkillCreate(UserSkillBase):
    skill_name: str # Frontend will pass string, backend will resolve to id

class UserSkillUpdate(UserSkillBase):
    pass

class UserSkillResponse(UserSkillBase):
    id: UUID
    user_id: UUID
    skill_id: UUID
    skill: SkillResponse

    class Config:
        from_attributes = True


class InternshipBase(BaseModel):
    company: str
    role: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    internship_type: Optional[str] = None
    description: Optional[str] = None
    technologies: Optional[str] = None
    certificate_url: Optional[str] = None

class InternshipCreate(InternshipBase):
    pass

class InternshipUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    internship_type: Optional[str] = None
    description: Optional[str] = None
    technologies: Optional[str] = None
    certificate_url: Optional[str] = None

class InternshipResponse(InternshipBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    technologies: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    technologies: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CertificationBase(BaseModel):
    name: str
    organization: str
    issue_date: Optional[date] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None
    certificate_file_url: Optional[str] = None

class CertificationCreate(CertificationBase):
    pass

class CertificationUpdate(BaseModel):
    name: Optional[str] = None
    organization: Optional[str] = None
    issue_date: Optional[date] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None
    certificate_file_url: Optional[str] = None

class CertificationResponse(CertificationBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class ResearchProfileBase(BaseModel):
    research_interests: Optional[str] = None
    research_skills: Optional[str] = None
    preferred_research_areas: Optional[str] = None

class ResearchProfileCreate(ResearchProfileBase):
    pass

class ResearchProfileUpdate(ResearchProfileBase):
    pass

class ResearchProfileResponse(ResearchProfileBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreatorProfileBase(BaseModel):
    channel_name: Optional[str] = None
    channel_url: Optional[str] = None
    content_category: Optional[str] = None
    preferred_language: Optional[str] = None
    content_style: Optional[str] = None
    target_audience: Optional[str] = None

class CreatorProfileCreate(CreatorProfileBase):
    pass

class CreatorProfileUpdate(CreatorProfileBase):
    pass

class CreatorProfileResponse(CreatorProfileBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserSettingsBase(BaseModel):
    theme: Optional[str] = "light"
    language: Optional[str] = "en"
    ai_response_style: Optional[str] = "normal"
    timezone: Optional[str] = None
    email_notifications: Optional[bool] = True
    reminder_notifications: Optional[bool] = True

class UserSettingsCreate(UserSettingsBase):
    pass

class UserSettingsUpdate(UserSettingsBase):
    pass

class UserSettingsResponse(UserSettingsBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
