from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base

# We will use alembic for migrations, but we can also create tables on startup for dev
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Nexora AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api import auth, profile, research

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(profile.router, prefix="/api/profile", tags=["profile"])
app.include_router(research.router, prefix="/api/research", tags=["research"])

@app.get("/")
def root():
    return {"message": "Welcome to Nexora AI Backend"}
