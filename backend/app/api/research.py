import os
import uuid
import shutil
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.api.dependencies import get_current_user
from app.models.research import ResearchProject, ResearchPaper, PaperNote, LiteratureReview
from app.schemas.research import (
    ResearchProjectCreate, ResearchProjectUpdate, ResearchProjectResponse,
    ResearchPaperCreate, ResearchPaperUpdate, ResearchPaperResponse,
    PaperNoteCreate, PaperNoteUpdate, PaperNoteResponse,
    LiteratureReviewCreate, LiteratureReviewUpdate, LiteratureReviewResponse
)

router = APIRouter()

UPLOAD_DIR = "uploads/papers"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ----------------- Research Projects -----------------

@router.get("/projects", response_model=List[ResearchProjectResponse])
def get_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    projects = db.query(ResearchProject).filter(ResearchProject.user_id == current_user.id).all()
    return projects

@router.post("/projects", response_model=ResearchProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project_in: ResearchProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_project = ResearchProject(**project_in.model_dump(), user_id=current_user.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    # Initialize empty literature review for the project
    lit_review = LiteratureReview(project_id=new_project.id, content="")
    db.add(lit_review)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.get("/projects/{project_id}", response_model=ResearchProjectResponse)
def get_project(project_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id, ResearchProject.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/projects/{project_id}", response_model=ResearchProjectResponse)
def update_project(project_id: uuid.UUID, project_in: ResearchProjectUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id, ResearchProject.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_data = project_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)
    
    db.commit()
    db.refresh(project)
    return project

@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id, ResearchProject.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    return None

# ----------------- Research Papers -----------------

@router.post("/projects/{project_id}/papers", response_model=ResearchPaperResponse, status_code=status.HTTP_201_CREATED)
def upload_paper(
    project_id: uuid.UUID,
    title: str = Form(...),
    authors: str = Form(None),
    publication_year: str = Form(None),
    abstract: str = Form(None),
    doi: str = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id, ResearchProject.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    file_url = None
    if file:
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_url = f"/uploads/papers/{unique_filename}"
        
    paper = ResearchPaper(
        project_id=project_id,
        title=title,
        authors=authors,
        publication_year=publication_year,
        abstract=abstract,
        doi=doi,
        file_url=file_url
    )
    db.add(paper)
    db.commit()
    db.refresh(paper)
    return paper

@router.delete("/papers/{paper_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_paper(paper_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    paper = db.query(ResearchPaper).join(ResearchProject).filter(ResearchPaper.id == paper_id, ResearchProject.user_id == current_user.id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    if paper.file_url:
        try:
            os.remove(paper.file_url.lstrip('/'))
        except FileNotFoundError:
            pass
            
    db.delete(paper)
    db.commit()
    return None

# ----------------- Paper Notes -----------------

@router.post("/papers/{paper_id}/notes", response_model=PaperNoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(paper_id: uuid.UUID, note_in: PaperNoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    paper = db.query(ResearchPaper).join(ResearchProject).filter(ResearchPaper.id == paper_id, ResearchProject.user_id == current_user.id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    note = PaperNote(**note_in.model_dump(), paper_id=paper_id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = db.query(PaperNote).join(ResearchPaper).join(ResearchProject).filter(PaperNote.id == note_id, ResearchProject.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(note)
    db.commit()
    return None

# ----------------- Literature Review -----------------

@router.put("/projects/{project_id}/literature-review", response_model=LiteratureReviewResponse)
def update_literature_review(project_id: uuid.UUID, review_in: LiteratureReviewUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    review = db.query(LiteratureReview).join(ResearchProject).filter(LiteratureReview.project_id == project_id, ResearchProject.user_id == current_user.id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Literature review not found")
    
    review.content = review_in.content
    db.commit()
    db.refresh(review)
    return review
