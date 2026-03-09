"""
Matcher service — semantic similarity scoring using cosine similarity.
Compares resume embeddings against job embeddings to find the best matches.

The key insight: cosine similarity understands that "MERN Stack" experience
matches "Full Stack Developer" roles WITHOUT keyword matching.
"""
from typing import List, Dict, Any, Optional
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.job import Job
from app.services.embeddings import generate_embedding


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Compute cosine similarity between two vectors.

    Returns a value between -1 and 1, where:
      1.0 = identical direction (perfect match)
      0.0 = orthogonal (no relation)
     -1.0 = opposite direction

    Args:
        vec_a: First embedding vector.
        vec_b: Second embedding vector.

    Returns:
        Cosine similarity score.
    """
    a = np.array(vec_a, dtype=np.float64)
    b = np.array(vec_b, dtype=np.float64)

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(np.dot(a, b) / (norm_a * norm_b))


def similarity_to_percentage(cosine_sim: float) -> float:
    """
    Convert cosine similarity (-1 to 1) to a human-readable percentage (0-100).

    We use (cosine_sim + 1) / 2 * 100 to map the full range to 0-100%.
    Practical scores for text embeddings typically range 0.5–0.95.
    """
    return round(((cosine_sim + 1) / 2) * 100, 1)


async def match_resume_to_jobs(
    resume_text: str,
    db: AsyncSession,
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Match a resume against all jobs in the database and return top-k matches.

    Process:
    1. Generate embedding for the resume text
    2. Load all job embeddings from the database
    3. Compute cosine similarity for each job
    4. Return top-k results sorted by score (descending)

    Args:
        resume_text: Extracted text from the candidate's resume.
        db: Async database session.
        top_k: Number of top matches to return (default: 5).

    Returns:
        List of match dicts sorted by match_score descending:
        [
            {
                "job": Job,
                "match_score": 87.5,
                "cosine_similarity": 0.75,
                "rank": 1
            },
            ...
        ]
    """
    # Step 1: Generate resume embedding
    resume_embedding = await generate_embedding(resume_text)

    # Step 2: Load all jobs that have pre-computed embeddings
    result = await db.execute(select(Job).where(Job.embedding.isnot(None)))
    jobs = result.scalars().all()

    if not jobs:
        return []

    # Step 3: Score each job
    scored_jobs = []
    for job in jobs:
        if not job.embedding:
            continue
        sim = cosine_similarity(resume_embedding, job.embedding)
        score = similarity_to_percentage(sim)
        scored_jobs.append({
            "job": job,
            "match_score": score,
            "cosine_similarity": sim,
        })

    # Step 4: Sort by match score (descending) and return top-k
    scored_jobs.sort(key=lambda x: x["match_score"], reverse=True)
    top_matches = scored_jobs[:top_k]

    # Add rank
    for i, match in enumerate(top_matches):
        match["rank"] = i + 1

    return top_matches


async def match_jd_to_resumes(
    job_description: str,
    resumes: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Match a job description against multiple uploaded resumes.
    Used for recruiter bulk-upload ranking.

    Args:
        job_description: The recruiter's job description text.
        resumes: List of dicts with keys: 'candidate_id', 'name', 'resume_text', 'embedding'

    Returns:
        List of match dicts sorted by match_score descending.
    """
    # Generate JD embedding
    jd_embedding = await generate_embedding(job_description)

    scored = []
    for resume in resumes:
        # Use pre-computed embedding if available, otherwise generate
        if resume.get("embedding"):
            emb = resume["embedding"]
        else:
            emb = await generate_embedding(resume["resume_text"])

        sim = cosine_similarity(jd_embedding, emb)
        score = similarity_to_percentage(sim)

        scored.append({
            **resume,
            "match_score": score,
            "cosine_similarity": sim,
        })

    # Sort by score descending
    scored.sort(key=lambda x: x["match_score"], reverse=True)

    # Add ranks
    for i, item in enumerate(scored):
        item["rank"] = i + 1

    return scored
