from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import engine, Base, AsyncSessionLocal
from app.database.migration import run_database_migrations
import app.models.user
import app.models.profile
import app.models.character
import app.models.career
import app.models.research
import app.models.integration
import app.models.education
import app.models.social
import app.models.notebook
from app.services.career_seed import seed_career_roadmaps

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database schema is migrated and all tables exist
    await run_database_migrations(engine)
    
    # Ensure career paths are seeded
    async with AsyncSessionLocal() as session:
        try:
            await seed_career_roadmaps(session)
        except Exception as e:
            print("Error during career seeding:", e)
    
    yield

app = FastAPI(
    title="Nexora AI Platform API",
    description="Backend API for Nexora AI Career Roadmap, Research Workspace, Planner & Knowledge Base",
    version="2.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api import auth, profile, career, research, integration, education, teacher, professional, notebook, social, ai

app.include_router(ai.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
app.include_router(career.router, prefix="/api")
app.include_router(research.router, prefix="/api")
app.include_router(integration.router, prefix="/api")
app.include_router(education.router, prefix="/api")
app.include_router(teacher.router, prefix="/api")
app.include_router(professional.router, prefix="/api")
app.include_router(notebook.router, prefix="/api")
app.include_router(social.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Nexora AI Platform API"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "platform": "Nexora AI", "version": "2.0.0"}
