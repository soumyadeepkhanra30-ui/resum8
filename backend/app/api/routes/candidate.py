"""
Candidate API routes.
Handles resume upload, job matching, and gap analysis for job seekers.
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.parser import parse_resume, extract_email, extract_phone, extract_name_heuristic
from app.services.embeddings import generate_embedding
from app.services.matcher import match_resume_to_jobs
from app.services.gap_analysis import generate_gap_analysis
from app.core.config import settings
from app.core.security import sanitize_filename

router = APIRouter(prefix="/api/candidate", tags=["Candidate"])

# ─── Request/Response Models ───────────────────────────────────────────────


class ParsedResumeResponse(BaseModel):
    """Response from the resume upload endpoint."""
    resume_text: str
    extracted_name: Optional[str] = None
    extracted_email: Optional[str] = None
    extracted_phone: Optional[str] = None
    word_count: int
    char_count: int
    message: str = "Resume parsed successfully"


class JobMatchResult(BaseModel):
    """A single job match result."""
    job_id: int
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
    match_score: float
    cosine_similarity: float
    rank: int


class MatchJobsResponse(BaseModel):
    """Response from the job matching endpoint."""
    matches: List[JobMatchResult]
    total_jobs_compared: int
    message: str


class GapAnalysisRequest(BaseModel):
    """Request body for gap analysis."""
    resume_text: str
    job_id: int
    match_score: float


class GapAnalysisResponse(BaseModel):
    """Response from the gap analysis endpoint."""
    job_id: int
    job_title: str
    match_score: float
    matching_skills: List[str]
    missing_skills: List[str]
    improvement_tips: List[str]
    summary: str


# ─── Routes ────────────────────────────────────────────────────────────────


@router.post("/upload-resume", response_model=ParsedResumeResponse)
async def upload_resume(
    file: UploadFile = File(..., description="PDF or DOCX resume file"),
):
    """
    Parse an uploaded resume and extract text.

    Supports .pdf and .docx formats. Returns extracted text and basic
    personal info for use in the matching and gap analysis endpoints.
    """
    # Validate file type
    allowed_types = ["application/pdf",
                     "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    if file.content_type not in allowed_types and not (
        file.filename.lower().endswith(".pdf") or file.filename.lower().endswith(".docx")
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and DOCX files are supported."
        )

    # Validate file size
    max_size = settings.max_upload_size_mb * 1024 * 1024
    contents = await file.read()
    if len(contents) > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds {settings.max_upload_size_mb}MB limit."
        )

    safe_filename = sanitize_filename(file.filename)

    try:
        resume_text = parse_resume(contents, safe_filename)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    return ParsedResumeResponse(
        resume_text=resume_text,
        extracted_name=extract_name_heuristic(resume_text),
        extracted_email=extract_email(resume_text),
        extracted_phone=extract_phone(resume_text),
        word_count=len(resume_text.split()),
        char_count=len(resume_text),
    )


@router.post("/match-jobs", response_model=MatchJobsResponse)
async def match_jobs(
    resume_text: str = Form(..., description="Extracted resume text"),
    db: AsyncSession = Depends(get_db),
):
    """
    Match a resume against all jobs in the database.

    Uses semantic embeddings (Google Gemini) and cosine similarity to find
    the top 5 most relevant job matches. This goes BEYOND keyword matching —
    'MERN Stack' will match 'Full Stack Developer' roles correctly.
    """
    if len(resume_text.strip()) < 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume text is too short. Please upload a complete resume."
        )

    try:
        matches = await match_resume_to_jobs(resume_text, db, top_k=5)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

    if not matches:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No jobs found in the database. Please seed the database first via POST /api/jobs/seed"
        )

    # Count total jobs in DB for informational purposes
    from sqlalchemy import func, select
    from app.models.job import Job
    total_result = await db.execute(select(func.count(Job.id)))
    total_jobs = total_result.scalar() or 0

    job_matches = []
    for m in matches:
        job = m["job"]
        job_matches.append(JobMatchResult(
            job_id=job.id,
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
            match_score=m["match_score"],
            cosine_similarity=m["cosine_similarity"],
            rank=m["rank"],
        ))

    return MatchJobsResponse(
        matches=job_matches,
        total_jobs_compared=total_jobs,
        message=f"Found {len(job_matches)} top matches from {total_jobs} jobs"
    )


@router.post("/gap-analysis", response_model=GapAnalysisResponse)
async def get_gap_analysis(
    payload: GapAnalysisRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Get AI-powered gap analysis for a specific job match.

    Uses Google Gemini to identify:
    - Skills the candidate already has that match
    - Skills/experience they're missing
    - Specific, actionable improvement tips
    """
    from sqlalchemy import select
    from app.models.job import Job

    # Fetch the job
    result = await db.execute(select(Job).where(Job.id == payload.job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    try:
        analysis = await generate_gap_analysis(
            resume_text=payload.resume_text,
            job_title=job.title,
            job_description=job.description,
            required_skills=job.required_skills or [],
            match_score=payload.match_score,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

    return GapAnalysisResponse(
        job_id=job.id,
        job_title=job.title,
        match_score=payload.match_score,
        matching_skills=analysis.get("matching_skills", []),
        missing_skills=analysis.get("missing_skills", []),
        improvement_tips=analysis.get("improvement_tips", []),
        summary=analysis.get("summary", ""),
    )
