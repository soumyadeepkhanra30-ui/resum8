"""
Recruiter API routes.
Handles bulk resume upload, candidate ranking, and executive summaries.
"""
from typing import List, Optional
import asyncio

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.parser import parse_resume, extract_name_heuristic, extract_email
from app.services.embeddings import generate_embedding
from app.services.matcher import match_jd_to_resumes
from app.services.summarizer import generate_executive_summary
from app.core.config import settings
from app.core.security import sanitize_filename, apply_data_masking

router = APIRouter(prefix="/api/recruiter", tags=["Recruiter"])

# ─── In-memory candidate store for recruiter session ──────────────────────
# NOTE: In production, you'd store these in PostgreSQL (Candidate model).
# For the MVP, we keep them in memory per-request for simplicity.

# ─── Request/Response Models ───────────────────────────────────────────────


class CandidateRankResult(BaseModel):
    """A single candidate result in the ranked list."""
    candidate_id: str
    name: str
    email: Optional[str] = None
    resume_text: str
    match_score: float
    cosine_similarity: float
    rank: int
    executive_summary: Optional[str] = None
    is_masked: bool = False


class RankCandidatesResponse(BaseModel):
    """Response from the rank candidates endpoint."""
    job_description: str
    candidates: List[CandidateRankResult]
    total_candidates: int
    message: str


class SummaryResponse(BaseModel):
    """Response from the summary endpoint."""
    candidate_id: str
    name: str
    summary: str


# ─── Routes ────────────────────────────────────────────────────────────────


@router.post("/upload-resumes", response_model=RankCandidatesResponse)
async def upload_resumes_and_rank(
    files: List[UploadFile] = File(..., description="Up to 20 PDF or DOCX resume files"),
    job_description: str = Form(..., description="Job description to match candidates against"),
    mask_names: bool = Form(False, description="Mask candidate names for bias-free review"),
):
    """
    Upload multiple resumes and rank them against a job description.

    Process:
    1. Parse each uploaded resume (PDF/DOCX)
    2. Generate embeddings for each resume + the job description
    3. Compute cosine similarity scores
    4. Return ranked list of candidates (highest match first)

    Supports up to 20 files per upload. Optionally masks names for bias-free screening.
    """
    if len(files) > settings.max_recruiter_uploads:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Maximum {settings.max_recruiter_uploads} files allowed per upload."
        )

    if not job_description or len(job_description.strip()) < 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description must be at least 50 characters long."
        )

    max_size = settings.max_upload_size_mb * 1024 * 1024
    parsed_resumes = []

    for i, file in enumerate(files):
        # Validate file type
        if not (file.filename.lower().endswith(".pdf") or file.filename.lower().endswith(".docx")):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File '{file.filename}' is not a PDF or DOCX. Only these formats are supported."
            )

        contents = await file.read()

        if len(contents) > max_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File '{file.filename}' exceeds {settings.max_upload_size_mb}MB limit."
            )

        safe_filename = sanitize_filename(file.filename)

        try:
            resume_text = parse_resume(contents, safe_filename)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Failed to parse '{file.filename}': {str(e)}"
            )

        name = extract_name_heuristic(resume_text) or f"Candidate {i + 1}"
        email = extract_email(resume_text)

        parsed_resumes.append({
            "candidate_id": f"candidate_{i + 1}",
            "name": name,
            "email": email,
            "resume_text": resume_text,
            "embedding": None,  # Will be generated in matcher
        })

    # Generate embeddings for all resumes concurrently
    try:
        async def embed_resume(resume_data):
            emb = await generate_embedding(resume_data["resume_text"])
            return {**resume_data, "embedding": emb}

        tasks = [embed_resume(r) for r in parsed_resumes]
        parsed_resumes = await asyncio.gather(*tasks)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

    # Rank candidates against the JD
    try:
        ranked = await match_jd_to_resumes(job_description, list(parsed_resumes))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

    # Apply masking if requested
    results = []
    for candidate in ranked:
        candidate_data = {
            "name": candidate["name"],
            "email": candidate.get("email"),
        }
        if mask_names:
            masked = apply_data_masking(candidate_data)
            display_name = masked["name"]
            display_email = masked.get("email")
        else:
            display_name = candidate_data["name"]
            display_email = candidate_data["email"]

        results.append(CandidateRankResult(
            candidate_id=candidate["candidate_id"],
            name=display_name,
            email=display_email,
            resume_text=candidate["resume_text"],
            match_score=candidate["match_score"],
            cosine_similarity=candidate["cosine_similarity"],
            rank=candidate["rank"],
            is_masked=mask_names,
        ))

    return RankCandidatesResponse(
        job_description=job_description,
        candidates=results,
        total_candidates=len(results),
        message=f"Ranked {len(results)} candidates by match score"
    )


@router.post("/summary/{candidate_id}", response_model=SummaryResponse)
async def get_candidate_summary(
    candidate_id: str,
    resume_text: str = Form(..., description="Candidate's resume text"),
    candidate_name: str = Form("The candidate", description="Candidate's name"),
    job_title: str = Form("", description="Target job title for context"),
):
    """
    Generate an AI-powered executive summary for a candidate.

    Uses Google Gemini to produce a 2-3 sentence summary covering:
    - Years of experience and primary domain
    - Core technical skills
    - Notable strength or gap

    Designed for recruiters to quickly triage candidates.
    """
    try:
        summary = await generate_executive_summary(
            resume_text=resume_text,
            candidate_name=candidate_name,
            job_title=job_title,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

    return SummaryResponse(
        candidate_id=candidate_id,
        name=candidate_name,
        summary=summary,
    )
