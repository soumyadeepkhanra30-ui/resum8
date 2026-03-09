"""
FastAPI main application entry point.
Configures the app, CORS, routers, and startup events.
"""
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.config import settings
from app.db.database import create_tables, get_db
from app.api.routes.candidate import router as candidate_router
from app.api.routes.recruiter import router as recruiter_router
from app.models.job import Job


# ─── Lifespan (startup/shutdown) ────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup."""
    await create_tables()
    yield


# ─── App Initialization ────────────────────────────────────────────────────

app = FastAPI(
    title="ResuM8 API",
    description=(
        "AI-Powered Talent Matcher — Semantic resume-to-job matching using Google Gemini embeddings. "
        "Bridges the gap between job seekers and recruiters with intelligent match scoring."
    ),
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ─── CORS Middleware ────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:80",
        "http://frontend:80",  # Docker service name
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ───────────────────────────────────────────────────────────────

app.include_router(candidate_router)
app.include_router(recruiter_router)


# ─── Job Routes ────────────────────────────────────────────────────────────

class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    job_type: str
    experience_level: str
    category: str
    salary_range: str
    description: str
    required_skills: List[str]
    preferred_skills: List[str]


class SeedResponse(BaseModel):
    message: str
    jobs_seeded: int
    total_jobs: int


@app.get("/api/jobs", response_model=List[JobResponse], tags=["Jobs"])
async def list_jobs(db: AsyncSession = Depends(get_db)):
    """List all job listings in the database."""
    result = await db.execute(select(Job))
    jobs = result.scalars().all()
    return [
        JobResponse(
            id=job.id,
            title=job.title,
            company=job.company,
            location=job.location,
            job_type=job.job_type,
            experience_level=job.experience_level,
            category=job.category,
            salary_range=job.salary_range,
            description=job.description,
            required_skills=job.required_skills or [],
            preferred_skills=job.preferred_skills or [],
        )
        for job in jobs
    ]


@app.post("/api/jobs/seed", response_model=SeedResponse, tags=["Jobs"])
async def seed_jobs_endpoint(db: AsyncSession = Depends(get_db)):
    """
    Seed the database with 50+ dummy job listings.
    Generates embeddings for each job via the Gemini API.
    This may take 30-60 seconds depending on the API rate limits.
    """
    from app.db.seed_jobs import seed_jobs
    try:
        seeded = await seed_jobs(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to seed jobs: {str(e)}"
        )

    total_result = await db.execute(select(func.count(Job.id)))
    total = total_result.scalar() or 0

    return SeedResponse(
        message=f"Successfully seeded {seeded} new jobs",
        jobs_seeded=seeded,
        total_jobs=total,
    )


# ─── Health Check ──────────────────────────────────────────────────────────

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring and deployment readiness."""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "gemini_configured": bool(settings.gemini_api_key),
    }


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint — links to API documentation."""
    return {
        "message": f"Welcome to {settings.app_name} API",
        "docs": "/docs",
        "health": "/health",
        "version": settings.app_version,
    }
