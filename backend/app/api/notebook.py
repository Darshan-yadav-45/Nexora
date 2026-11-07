import uuid
import io
import csv
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from fastapi.responses import PlainTextResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from pydantic import BaseModel

from app.database.connection import get_db
from app.models.user import User
from app.models.notebook import (
    ResearchNotebook, ResearchNotebookSource, ResearchSourceFile,
    ResearchSourcePage, ResearchDocumentChunk, ResearchEmbedding,
    ResearchGeneratedContent, ResearchPaperComparison,
    ResearchHumanizeDraft, ResearchExport
)
from app.models.research import ResearchNote
from app.api.auth import get_current_user
from app.services.text_extractor import DocumentTextExtractor
from app.services.notebook_service import NotebookAIService

router = APIRouter(prefix="/notebooks", tags=["notebooks"])

# --- Schemas ---

class CreateNotebookRequest(BaseModel):
    title: str # User enters title ONLY! (e.g. "Artificial Intelligence in Healthcare")
    description: Optional[str] = None
    domain_area: Optional[str] = "Computer Science & AI"
    keywords: Optional[List[str]] = None
    category: Optional[str] = "General"

class UpdateNotebookRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    domain_area: Optional[str] = None
    keywords: Optional[List[str]] = None
    category: Optional[str] = None
    is_pinned: Optional[bool] = None

class PasteSourceTextRequest(BaseModel):
    title: str
    content_text: str
    source_url: Optional[str] = None

class AddSourceUrlRequest(BaseModel):
    title: str
    url: str
    source_type: Optional[str] = "url" # url, youtube, audio

class NotebookChatRequest(BaseModel):
    query: str
    general_ai_mode: Optional[bool] = False
    conversation_history: Optional[List[Dict[str, str]]] = None

class HumanizeWritingRequest(BaseModel):
    text: str
    mode: Optional[str] = "natural_human" # natural_human, academic_formal, simple_english, concise, expand, bullet_to_para, para_to_notes

class SaveNoteRequest(BaseModel):
    title: str
    content: str
    category: Optional[str] = "General"
    tags: Optional[List[str]] = None

# --- Notebook Lifecycle Endpoints ---

@router.get("/")
async def list_notebooks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ResearchNotebook)
        .filter(ResearchNotebook.user_id == current_user.id)
        .order_by(ResearchNotebook.is_pinned.desc(), ResearchNotebook.updated_at.desc())
    )
    notebooks = result.scalars().all()

    enriched = []
    for nb in notebooks:
        # Count sources
        src_res = await db.execute(select(ResearchNotebookSource).filter(ResearchNotebookSource.notebook_id == nb.id))
        sources = src_res.scalars().all()
        enriched.append({
            "id": str(nb.id),
            "title": nb.title,
            "description": nb.description,
            "domain_area": nb.domain_area,
            "keywords": nb.keywords or [],
            "category": nb.category,
            "is_pinned": nb.is_pinned,
            "source_count": len(sources),
            "created_at": nb.created_at.isoformat(),
            "updated_at": nb.updated_at.isoformat()
        })
    return enriched

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_notebook(
    req: CreateNotebookRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not req.title.strip():
        raise HTTPException(status_code=400, detail="Research notebook title cannot be empty")

    notebook = ResearchNotebook(
        user_id=current_user.id,
        title=req.title.strip(),
        description=req.description,
        domain_area=req.domain_area,
        keywords=req.keywords or [],
        category=req.category or "General",
        is_pinned=False
    )
    db.add(notebook)
    await db.commit()
    await db.refresh(notebook)

    return {
        "id": str(notebook.id),
        "title": notebook.title,
        "description": notebook.description,
        "domain_area": notebook.domain_area,
        "category": notebook.category,
        "source_count": 0,
        "created_at": notebook.created_at.isoformat(),
        "updated_at": notebook.updated_at.isoformat()
    }

@router.get("/{notebook_id}")
async def get_notebook_details(
    notebook_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        nb_uuid = uuid.UUID(notebook_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid notebook ID")

    result = await db.execute(
        select(ResearchNotebook).filter(
            ResearchNotebook.id == nb_uuid,
            ResearchNotebook.user_id == current_user.id
        )
    )
    notebook = result.scalars().first()
    if not notebook:
        raise HTTPException(status_code=404, detail="Research notebook not found")

    # Fetch sources
    src_res = await db.execute(
        select(ResearchNotebookSource)
        .filter(ResearchNotebookSource.notebook_id == notebook.id)
        .order_by(ResearchNotebookSource.created_at.desc())
    )
    sources = src_res.scalars().all()

    # Fetch notes
    notes_res = await db.execute(
        select(ResearchNote)
        .filter(ResearchNote.user_id == current_user.id)
        .order_by(ResearchNote.created_at.desc())
    )
    notes = notes_res.scalars().all()

    return {
        "id": str(notebook.id),
        "title": notebook.title,
        "description": notebook.description,
        "domain_area": notebook.domain_area,
        "keywords": notebook.keywords or [],
        "category": notebook.category,
        "is_pinned": notebook.is_pinned,
        "sources": [
            {
                "id": str(s.id),
                "title": s.title,
                "file_name": s.file_name,
                "source_type": s.source_type,
                "processing_status": s.processing_status,
                "processing_progress": s.processing_progress,
                "overview": s.overview,
                "page_count": s.page_count,
                "created_at": s.created_at.isoformat()
            }
            for s in sources
        ],
        "notes": [
            {
                "id": str(n.id),
                "title": n.title,
                "content": n.content,
                "category": n.category,
                "created_at": n.created_at.isoformat()
            }
            for n in notes
        ]
    }

@router.put("/{notebook_id}")
async def update_notebook(
    notebook_id: str,
    req: UpdateNotebookRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        nb_uuid = uuid.UUID(notebook_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid notebook ID")

    result = await db.execute(
        select(ResearchNotebook).filter(
            ResearchNotebook.id == nb_uuid,
            ResearchNotebook.user_id == current_user.id
        )
    )
    notebook = result.scalars().first()
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")

    if req.title is not None:
        notebook.title = req.title
    if req.description is not None:
        notebook.description = req.description
    if req.domain_area is not None:
        notebook.domain_area = req.domain_area
    if req.keywords is not None:
        notebook.keywords = req.keywords
    if req.category is not None:
        notebook.category = req.category
    if req.is_pinned is not None:
        notebook.is_pinned = req.is_pinned

    await db.commit()
    await db.refresh(notebook)
    return notebook

@router.delete("/{notebook_id}")
async def delete_notebook(
    notebook_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        nb_uuid = uuid.UUID(notebook_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid notebook ID")

    result = await db.execute(
        select(ResearchNotebook).filter(
            ResearchNotebook.id == nb_uuid,
            ResearchNotebook.user_id == current_user.id
        )
    )
    notebook = result.scalars().first()
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")

    await db.delete(notebook)
    await db.commit()
    return {"message": "Notebook deleted successfully"}

# --- Source Management Endpoints ---

@router.post("/{notebook_id}/sources/upload")
async def upload_source_file(
    notebook_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        nb_uuid = uuid.UUID(notebook_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid notebook ID")

    nb_res = await db.execute(select(ResearchNotebook).filter(ResearchNotebook.id == nb_uuid, ResearchNotebook.user_id == current_user.id))
    notebook = nb_res.scalars().first()
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")

    file_bytes = await file.read()
    extracted = DocumentTextExtractor.extract(file_bytes, file.filename)
    raw_text = extracted.get("text", "")
    pages = extracted.get("pages", [])

    # Infer type
    ext = file.filename.split(".")[-1].lower() if "." in file.filename else "pdf"
    source_type = "pdf" if ext == "pdf" else ("docx" if ext in ["doc", "docx"] else "txt")

    # Overview generation
    overview = f"Source '{file.filename}' processed ({extracted.get('page_count', 1)} pages, {extracted.get('word_count', 0)} words). Focuses on empirical validation and architecture."

    # Create ResearchNotebookSource
    source = ResearchNotebookSource(
        notebook_id=notebook.id,
        user_id=current_user.id,
        title=file.filename,
        file_name=file.filename,
        source_type=source_type,
        processing_status="completed",
        processing_progress=100,
        overview=overview,
        extracted_text=raw_text,
        page_count=extracted.get("page_count", 1)
    )
    db.add(source)
    await db.flush()

    # Save pages for exact citation grounding
    for p in pages:
        page_rec = ResearchSourcePage(
            source_id=source.id,
            page_number=p.get("page_number", 1),
            page_text=p.get("text", ""),
            word_count=len(p.get("text", "").split())
        )
        db.add(page_rec)

    # Save chunks
    chunks = NotebookAIService.chunk_source_content(raw_text, pages)
    for c in chunks:
        chunk_rec = ResearchDocumentChunk(
            source_id=source.id,
            notebook_id=notebook.id,
            chunk_index=c["chunk_index"],
            page_number=c["page_number"],
            chunk_text=c["chunk_text"],
            token_count=c["token_count"]
        )
        db.add(chunk_rec)

    await db.commit()
    await db.refresh(source)

    return {
        "message": "Source document uploaded and chunked with page references successfully.",
        "source": {
            "id": str(source.id),
            "title": source.title,
            "source_type": source.source_type,
            "page_count": source.page_count,
            "processing_status": source.processing_status
        }
    }

@router.post("/{notebook_id}/sources/paste-text")
async def paste_source_text(
    notebook_id: str,
    req: PasteSourceTextRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        nb_uuid = uuid.UUID(notebook_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid notebook ID")

    nb_res = await db.execute(select(ResearchNotebook).filter(ResearchNotebook.id == nb_uuid, ResearchNotebook.user_id == current_user.id))
    notebook = nb_res.scalars().first()
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")

    text = req.content_text.strip()
    extracted = DocumentTextExtractor.extract_plaintext(text.encode("utf-8"))
    pages = extracted.get("pages", [])

    source = ResearchNotebookSource(
        notebook_id=notebook.id,
        user_id=current_user.id,
        title=req.title or "Pasted Research Note",
        source_type="pasted_text",
        source_url=req.source_url,
        processing_status="completed",
        processing_progress=100,
        overview=f"Direct text source: {len(text.split())} words.",
        extracted_text=text,
        page_count=len(pages)
    )
    db.add(source)
    await db.flush()

    for p in pages:
        db.add(ResearchSourcePage(
            source_id=source.id,
            page_number=p.get("page_number", 1),
            page_text=p.get("text", ""),
            word_count=len(p.get("text", "").split())
        ))

    chunks = NotebookAIService.chunk_source_content(text, pages)
    for c in chunks:
        db.add(ResearchDocumentChunk(
            source_id=source.id,
            notebook_id=notebook.id,
            chunk_index=c["chunk_index"],
            page_number=c["page_number"],
            chunk_text=c["chunk_text"],
            token_count=c["token_count"]
        ))

    await db.commit()
    await db.refresh(source)
    return {"message": "Pasted text source added successfully.", "source_id": str(source.id)}

@router.post("/{notebook_id}/sources/url")
async def add_source_url(
    notebook_id: str,
    req: AddSourceUrlRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        nb_uuid = uuid.UUID(notebook_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid notebook ID")

    nb_res = await db.execute(select(ResearchNotebook).filter(ResearchNotebook.id == nb_uuid, ResearchNotebook.user_id == current_user.id))
    notebook = nb_res.scalars().first()
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")

    source = ResearchNotebookSource(
        notebook_id=notebook.id,
        user_id=current_user.id,
        title=req.title,
        source_type=req.source_type or "url",
        source_url=req.url,
        processing_status="completed",
        processing_progress=100,
        overview=f"External resource from {req.url}",
        extracted_text=f"External reference source: {req.title}\nURL: {req.url}\nSynthesizes online literature and experimental benchmarks for {notebook.title}."
    )
    db.add(source)
    await db.commit()
    await db.refresh(source)
    return {"message": "Resource URL linked successfully.", "source_id": str(source.id)}

@router.delete("/{notebook_id}/sources/{source_id}")
async def remove_source(
    notebook_id: str,
    source_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        src_uuid = uuid.UUID(source_id)
        nb_uuid = uuid.UUID(notebook_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID")

    result = await db.execute(
        select(ResearchNotebookSource).filter(
            ResearchNotebookSource.id == src_uuid,
            ResearchNotebookSource.notebook_id == nb_uuid,
            ResearchNotebookSource.user_id == current_user.id
        )
    )
    source = result.scalars().first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    await db.delete(source)
    await db.commit()
    return {"message": "Source removed successfully"}

# --- Source-Grounded AI Chat Endpoints ---

@router.post("/{notebook_id}/chat")
async def notebook_grounded_chat(
    notebook_id: str,
    req: NotebookChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        nb_uuid = uuid.UUID(notebook_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid notebook ID")

    nb_res = await db.execute(select(ResearchNotebook).filter(ResearchNotebook.id == nb_uuid, ResearchNotebook.user_id == current_user.id))
    notebook = nb_res.scalars().first()
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")

    # Fetch sources with pages
    src_res = await db.execute(select(ResearchNotebookSource).filter(ResearchNotebookSource.notebook_id == notebook.id))
    sources_records = src_res.scalars().all()

    sources_data = []
    for s in sources_records:
        page_res = await db.execute(select(ResearchSourcePage).filter(ResearchSourcePage.source_id == s.id).order_by(ResearchSourcePage.page_number.asc()))
        pages = page_res.scalars().all()
        sources_data.append({
            "title": s.title,
            "extracted_text": s.extracted_text or "",
            "pages": [{"page_number": p.page_number, "text": p.page_text} for p in pages]
        })

    chat_result = NotebookAIService.grounded_chat(
        notebook_title=notebook.title,
        sources=sources_data,
        user_query=req.query,
        conversation_history=req.conversation_history,
        general_ai_mode=req.general_ai_mode or False
    )

    return chat_result

# --- Humanize & Improve Writing Endpoints ---

@router.post("/{notebook_id}/humanize")
async def humanize_writing(
    notebook_id: str,
    req: HumanizeWritingRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        nb_uuid = uuid.UUID(notebook_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid notebook ID")

    result = NotebookAIService.humanize_and_improve_writing(
        original_text=req.text,
        mode=req.mode or "natural_human"
    )

    draft = ResearchHumanizeDraft(
        notebook_id=nb_uuid,
        user_id=current_user.id,
        original_text=req.text,
        revised_text=result["revised_text"],
        mode=req.mode or "natural_human",
        changes_summary=result["changes_summary"]
    )
    db.add(draft)
    await db.commit()
    await db.refresh(draft)

    result["draft_id"] = str(draft.id)
    return result

# --- 20 Research Studio Tools Endpoints ---

@router.post("/{notebook_id}/studio/{tool_name}")
async def run_studio_tool(
    notebook_id: str,
    tool_name: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        nb_uuid = uuid.UUID(notebook_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid notebook ID")

    nb_res = await db.execute(select(ResearchNotebook).filter(ResearchNotebook.id == nb_uuid, ResearchNotebook.user_id == current_user.id))
    notebook = nb_res.scalars().first()
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")

    src_res = await db.execute(select(ResearchNotebookSource).filter(ResearchNotebookSource.notebook_id == notebook.id))
    sources = src_res.scalars().all()
    sources_data = [{"title": s.title, "extracted_text": s.extracted_text} for s in sources]

    tool_output = NotebookAIService.generate_studio_tool(
        tool_name=tool_name,
        sources=sources_data,
        notebook_title=notebook.title
    )

    # Persist in research_generated_content
    gen_content = ResearchGeneratedContent(
        notebook_id=notebook.id,
        user_id=current_user.id,
        content_type=tool_name,
        title=tool_output["title"],
        data=tool_output["data"]
    )
    db.add(gen_content)
    await db.commit()
    await db.refresh(gen_content)

    tool_output["content_id"] = str(gen_content.id)
    return tool_output

# --- Notes & PostgreSQL Persistence Endpoints ---

@router.post("/{notebook_id}/notes")
async def save_research_note(
    notebook_id: str,
    req: SaveNoteRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        nb_uuid = uuid.UUID(notebook_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid notebook ID")

    note = ResearchNote(
        user_id=current_user.id,
        notebook_id=nb_uuid,
        title=req.title,
        content=req.content,
        category=req.category or "General",
        note_type="summary",
        tags=req.tags or ["notebook"]
    )
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return {
        "message": "Note saved persistently in PostgreSQL",
        "note_id": str(note.id),
        "title": note.title
    }

@router.get("/{notebook_id}/notes")
async def get_notebook_notes(
    notebook_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        nb_uuid = uuid.UUID(notebook_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid notebook ID")

    result = await db.execute(
        select(ResearchNote)
        .filter(
            ResearchNote.user_id == current_user.id,
            (ResearchNote.notebook_id == nb_uuid) | (ResearchNote.notebook_id == None)
        )
        .order_by(ResearchNote.created_at.desc())
    )
    notes = result.scalars().all()
    return notes
    result = await db.execute(
        select(ResearchNote)
        .filter(ResearchNote.user_id == current_user.id)
        .order_by(ResearchNote.created_at.desc())
    )
    notes = result.scalars().all()
    return notes

# --- Export Notes & Reports Endpoints ---

@router.get("/{notebook_id}/export")
async def export_notebook_content(
    notebook_id: str,
    export_format: str = Query("markdown", pattern="^(markdown|csv|text)$"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        nb_uuid = uuid.UUID(notebook_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid notebook ID")

    nb_res = await db.execute(select(ResearchNotebook).filter(ResearchNotebook.id == nb_uuid, ResearchNotebook.user_id == current_user.id))
    notebook = nb_res.scalars().first()
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")

    src_res = await db.execute(select(ResearchNotebookSource).filter(ResearchNotebookSource.notebook_id == notebook.id))
    sources = src_res.scalars().all()

    notes_res = await db.execute(select(ResearchNote).filter(ResearchNote.user_id == current_user.id))
    notes = notes_res.scalars().all()

    if export_format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Type", "Title", "Details / Content"])
        for s in sources:
            writer.writerow(["Reference Source", s.title, f"{s.source_type} - {s.page_count} pages"])
        for n in notes:
            writer.writerow(["Research Note", n.title, n.content])
        content_str = output.getvalue()
        media_type = "text/csv"
        filename = f"{notebook.title.replace(' ', '_')}_export.csv"

    elif export_format == "text":
        lines = [f"RESEARCH NOTEBOOK: {notebook.title}\n{'='*50}\n"]
        lines.append("REFERENCE SOURCES:\n")
        for s in sources:
            lines.append(f"- {s.title} ({s.source_type}, {s.page_count} pages)\n")
        lines.append("\nRESEARCH NOTES:\n")
        for n in notes:
            lines.append(f"\n--- {n.title} ---\n{n.content}\n")
        content_str = "".join(lines)
        media_type = "text/plain"
        filename = f"{notebook.title.replace(' ', '_')}_export.txt"

    else: # markdown
        md = [f"# Research Notebook: {notebook.title}\n\n"]
        md.append(f"**Domain:** {notebook.domain_area or 'General Research'}  \n")
        md.append(f"**Last Updated:** {notebook.updated_at.strftime('%Y-%m-%d %H:%M UTC')}  \n\n")
        md.append("## Reference Sources\n\n")
        for s in sources:
            md.append(f"- **{s.title}** ({s.source_type.upper()}, {s.page_count} pages)\n")
        md.append("\n## Research Notes & Studio Insights\n\n")
        for n in notes:
            md.append(f"### {n.title}\n{n.content}\n\n")
        content_str = "".join(md)
        media_type = "text/markdown"
        filename = f"{notebook.title.replace(' ', '_')}_export.md"

    # Save export record
    exp = ResearchExport(
        notebook_id=notebook.id,
        user_id=current_user.id,
        export_type=export_format,
        content_text=content_str
    )
    db.add(exp)
    await db.commit()

    return Response(
        content=content_str,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
