import uuid
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Header, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.connection import get_db
from app.models.notebook import (
    ResearchNotebook, ResearchNotebookSource, ResearchSourcePage,
    ResearchGeneratedContent, ResearchHumanizeDraft
)
from app.services.notebook_service import NotebookAIService
from app.services.text_extractor import DocumentTextExtractor

router = APIRouter(prefix="/ai", tags=["ai-microservice"])

INTERNAL_SERVICE_KEY = "nexora-ai-internal-key-2026"

# Service-to-Service Security Validator
async def verify_internal_service(
    x_internal_service_key: Optional[str] = Header(None, alias="X-Internal-Service-Key"),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
    x_user_email: Optional[str] = Header(None, alias="X-User-Email")
):
    if not x_internal_service_key or x_internal_service_key != INTERNAL_SERVICE_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Invalid or missing internal service key. Direct frontend access is strictly forbidden."
        )
    if not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad Request: Missing verified user context (X-User-Id) from primary backend."
        )
    try:
        user_uuid = uuid.UUID(x_user_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request: Invalid UUID format for X-User-Id.")
    
    return {"user_id": user_uuid, "email": x_user_email}

# --- Request / Response Models ---

class GroundedChatRequest(BaseModel):
    message: str
    selected_source_ids: Optional[List[str]] = None
    tone: Optional[str] = "academic"
    humanize: Optional[bool] = False
    general_ai_mode: Optional[bool] = False
    conversation_history: Optional[List[Dict[str, str]]] = None

class HumanizeRequest(BaseModel):
    text: str
    style: Optional[str] = "student"
    tone: Optional[str] = "clear"
    mode: Optional[str] = "natural_human"

class StudioToolRequest(BaseModel):
    tool: Optional[str] = "summary"
    prompt: Optional[str] = None
    source_ids: Optional[List[str]] = None

# --- Endpoints ---

@router.get("/health")
async def ai_health(internal_auth: Dict[str, Any] = Depends(verify_internal_service)):
    return {
        "status": "healthy",
        "service": "Nexora AI Python Microservice",
        "verified_user": str(internal_auth["user_id"])
    }

@router.post("/grounded-chat")
async def grounded_chat(
    req: GroundedChatRequest,
    internal_auth: Dict[str, Any] = Depends(verify_internal_service),
    db: AsyncSession = Depends(get_db)
):
    user_id = internal_auth["user_id"]
    
    # Query sources belonging to this user
    sources_data = []
    if req.selected_source_ids:
        for sid in req.selected_source_ids:
            try:
                src_uuid = uuid.UUID(sid)
                res = await db.execute(
                    select(ResearchNotebookSource).filter(
                        ResearchNotebookSource.id == src_uuid,
                        ResearchNotebookSource.user_id == user_id
                    )
                )
                src = res.scalars().first()
                if src:
                    # Get pages for exact grounding
                    pages_res = await db.execute(
                        select(ResearchSourcePage).filter(ResearchSourcePage.source_id == src.id).order_by(ResearchSourcePage.page_number.asc())
                    )
                    pages = pages_res.scalars().all()
                    sources_data.append({
                        "title": src.title,
                        "extracted_text": src.extracted_text or "",
                        "pages": [{"page_number": p.page_number, "text": p.page_text} for p in pages]
                    })
            except Exception:
                continue

    result = NotebookAIService.grounded_chat(
        notebook_title="User Research Notebook",
        sources=sources_data,
        user_query=req.message,
        conversation_history=req.conversation_history,
        general_ai_mode=req.general_ai_mode or (len(sources_data) == 0)
    )

    if req.humanize and result.get("answer"):
        humanized = NotebookAIService.humanize_and_improve_writing(
            original_text=result["answer"],
            mode="natural_human"
        )
        result["answer"] = humanized.get("revised_text", result["answer"])
        result["humanized"] = True

    return result

@router.post("/humanize")
async def humanize_text(
    req: HumanizeRequest,
    internal_auth: Dict[str, Any] = Depends(verify_internal_service)
):
    mode = req.mode or "natural_human"
    result = NotebookAIService.humanize_and_improve_writing(
        original_text=req.text,
        mode=mode
    )
    return {
        "humanized_text": result.get("revised_text", req.text),
        "changes_summary": result.get("changes_summary", []),
        "readability_score": result.get("readability_score", 92),
        "tone_applied": req.tone or "clear"
    }

@router.post("/studio/{tool_name}")
async def studio_tool(
    tool_name: str,
    req: StudioToolRequest,
    internal_auth: Dict[str, Any] = Depends(verify_internal_service),
    db: AsyncSession = Depends(get_db)
):
    user_id = internal_auth["user_id"]
    
    sources_data = []
    if req.source_ids:
        for sid in req.source_ids:
            try:
                src_uuid = uuid.UUID(sid)
                res = await db.execute(
                    select(ResearchNotebookSource).filter(
                        ResearchNotebookSource.id == src_uuid,
                        ResearchNotebookSource.user_id == user_id
                    )
                )
                src = res.scalars().first()
                if src:
                    sources_data.append({
                        "title": src.title,
                        "extracted_text": src.extracted_text or ""
                    })
            except Exception:
                continue

    tool_output = NotebookAIService.generate_studio_tool(
        tool_name=tool_name,
        sources=sources_data,
        notebook_title="Research Workspace"
    )

    return tool_output

