import uuid
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from pydantic import BaseModel

from app.database.connection import get_db
from app.models.user import User
from app.models.social import SocialAccount, SocialConnectionLog
from app.models.education import CareerProfile
from app.api.auth import get_current_user
from app.services.social_service import SocialService

router = APIRouter(prefix="/social", tags=["social"])

class ConnectGithubRequest(BaseModel):
    username: str

class AddProfileLinkRequest(BaseModel):
    platform: str # linkedin, instagram, twitter, youtube, other
    profile_url: str
    username: Optional[str] = None
    display_name: Optional[str] = None
    custom_platform_name: Optional[str] = None

class SyncGithubToCareerRequest(BaseModel):
    account_id: str
    selected_repo_names: List[str]

@router.get("/accounts")
async def get_connected_accounts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(SocialAccount)
        .filter(SocialAccount.user_id == current_user.id)
        .order_by(SocialAccount.created_at.asc())
    )
    accounts = result.scalars().all()
    return accounts

@router.post("/connect-github")
async def connect_github_account(
    req: ConnectGithubRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    github_data = await SocialService.fetch_github_profile(req.username)

    # Check if existing github account
    existing = await db.execute(
        select(SocialAccount).filter(
            SocialAccount.user_id == current_user.id,
            SocialAccount.platform == "github"
        )
    )
    account = existing.scalars().first()
    if not account:
        account = SocialAccount(
            user_id=current_user.id,
            platform="github"
        )
        db.add(account)

    account.username = github_data["username"]
    account.profile_url = github_data["profile_url"]
    account.display_name = github_data["display_name"]
    account.avatar_url = github_data["avatar_url"]
    account.public_repos = github_data["public_repos"]
    account.connection_type = "oauth"
    account.is_connected = True
    account.show_on_public_profile = True
    account.platform_metadata = {"bio": github_data["bio"]}

    log = SocialConnectionLog(
        user_id=current_user.id,
        platform="github",
        action="connect",
        status="success",
        details={"repo_count": len(github_data["public_repos"])}
    )
    db.add(log)

    await db.commit()
    await db.refresh(account)

    return {
        "message": f"GitHub account @{account.username} connected successfully.",
        "account": account
    }

@router.post("/add-profile-link")
async def add_social_profile_link(
    req: AddProfileLinkRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    valid_platforms = ["linkedin", "instagram", "twitter", "youtube", "other"]
    platform = req.platform.lower()
    if platform not in valid_platforms:
        platform = "other"

    display_platform = req.custom_platform_name if platform == "other" and req.custom_platform_name else platform.capitalize()

    account = SocialAccount(
        user_id=current_user.id,
        platform=platform,
        username=req.username or req.profile_url.split("/")[-1] or "user",
        profile_url=req.profile_url,
        display_name=req.display_name or f"{display_platform} Profile",
        connection_type="profile_link",
        is_connected=False, # Distinguished from OAuth connected
        show_on_public_profile=True,
        platform_metadata={"custom_name": req.custom_platform_name}
    )
    db.add(account)

    log = SocialConnectionLog(
        user_id=current_user.id,
        platform=platform,
        action="add_profile_link",
        status="success",
        details={"url": req.profile_url}
    )
    db.add(log)

    await db.commit()
    await db.refresh(account)

    return {
        "message": f"{display_platform} profile link added.",
        "account": account
    }

@router.delete("/disconnect/{account_id}")
async def disconnect_social_account(
    account_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        acc_uuid = uuid.UUID(account_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid account ID")

    result = await db.execute(
        select(SocialAccount).filter(
            SocialAccount.id == acc_uuid,
            SocialAccount.user_id == current_user.id
        )
    )
    account = result.scalars().first()
    if not account:
        raise HTTPException(status_code=404, detail="Social account not found")

    platform = account.platform
    await db.delete(account)

    log = SocialConnectionLog(
        user_id=current_user.id,
        platform=platform,
        action="disconnect",
        status="success"
    )
    db.add(log)

    await db.commit()
    return {"message": f"{platform.capitalize()} connection severed successfully."}

@router.put("/visibility/{account_id}")
async def toggle_social_visibility(
    account_id: str,
    show: bool,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        acc_uuid = uuid.UUID(account_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid account ID")

    result = await db.execute(
        select(SocialAccount).filter(
            SocialAccount.id == acc_uuid,
            SocialAccount.user_id == current_user.id
        )
    )
    account = result.scalars().first()
    if not account:
        raise HTTPException(status_code=404, detail="Social account not found")

    account.show_on_public_profile = show
    await db.commit()
    return {"message": f"Public profile visibility set to {show}", "show_on_public_profile": show}

@router.post("/sync-github-to-career")
async def sync_github_repos_to_career(
    req: SyncGithubToCareerRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        acc_uuid = uuid.UUID(req.account_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid account ID")

    acc_res = await db.execute(select(SocialAccount).filter(SocialAccount.id == acc_uuid, SocialAccount.user_id == current_user.id))
    account = acc_res.scalars().first()
    if not account or account.platform != "github":
        raise HTTPException(status_code=404, detail="Connected GitHub account not found")

    # Find CareerProfile
    cp_res = await db.execute(select(CareerProfile).filter(CareerProfile.user_id == current_user.id))
    career_profile = cp_res.scalars().first()
    if not career_profile:
        career_profile = CareerProfile(user_id=current_user.id)
        db.add(career_profile)

    current_skills = set(career_profile.current_skills or [])
    for repo in account.public_repos or []:
        if repo.get("name") in req.selected_repo_names:
            lang = repo.get("language")
            if lang:
                current_skills.add(lang)

    career_profile.current_skills = list(current_skills)
    await db.commit()

    return {
        "message": f"Synced {len(req.selected_repo_names)} GitHub repositories to Career profile.",
        "updated_skills": career_profile.current_skills
    }
