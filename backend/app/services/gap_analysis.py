"""
Gap Analysis service.
Uses Google Gemini to identify skill gaps between a candidate's resume
and a specific job description, then provides actionable improvement tips.
"""
import json
from typing import Dict, Any, List
from google import genai

from app.core.config import settings


async def generate_gap_analysis(
    resume_text: str,
    job_title: str,
    job_description: str,
    required_skills: List[str],
    match_score: float,
) -> Dict[str, Any]:
    """
    Generate a gap analysis for a candidate-job pair using Gemini.

    Tells the candidate:
    - What skills they already have that match
    - What skills/experience they're missing
    - Specific improvement tips

    Args:
        resume_text: Candidate's resume text.
        job_title: Title of the job.
        job_description: Full job description.
        required_skills: List of required skills for the job.
        match_score: Pre-computed match percentage (0-100).

    Returns:
        Dict with keys: matching_skills, missing_skills, improvement_tips, summary
    """
    if not settings.gemini_api_key:
        return _fallback_gap_analysis(required_skills, match_score)

    prompt = f"""You are an expert career coach and talent analyst.

A candidate has uploaded their resume and I need you to analyze the gap between 
their profile and the following job:

JOB TITLE: {job_title}
MATCH SCORE: {match_score:.1f}%

JOB DESCRIPTION:
{job_description[:2000]}

REQUIRED SKILLS: {', '.join(required_skills)}

CANDIDATE RESUME:
{resume_text[:3000]}

Please analyze and respond with a JSON object in this exact format:
{{
  "matching_skills": ["skill1", "skill2", ...],
  "missing_skills": ["skill1", "skill2", ...],
  "improvement_tips": [
    "Specific tip 1",
    "Specific tip 2",
    "Specific tip 3"
  ],
  "summary": "One paragraph summary of the gap analysis"
}}

Focus on:
1. Skills/technologies explicitly mentioned in the job but absent from the resume
2. Experience level gaps (e.g., job requires 5 years, candidate has 2)
3. Domain knowledge gaps
4. Specific, actionable improvement tips (courses, certifications, projects)

Respond ONLY with the JSON object, no other text."""

    try:
        client = genai.Client(api_key=settings.gemini_api_key)
        response = await client.aio.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
        )

        # Parse the JSON response
        raw_text = response.text.strip()
        # Remove markdown code blocks if present
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]

        result = json.loads(raw_text.strip())
        return result

    except (json.JSONDecodeError, Exception):
        # Fall back to basic analysis if AI fails
        return _fallback_gap_analysis(required_skills, match_score)


def _fallback_gap_analysis(required_skills: List[str], match_score: float) -> Dict[str, Any]:
    """
    Basic fallback gap analysis when Gemini API is unavailable.
    Returns a minimal structure with placeholder data.
    """
    return {
        "matching_skills": [],
        "missing_skills": required_skills[:5] if required_skills else [],
        "improvement_tips": [
            "Review the job description carefully and identify skills to develop.",
            "Consider taking relevant online courses on platforms like Coursera or Udemy.",
            "Build portfolio projects that demonstrate the required skills.",
        ],
        "summary": (
            f"Your profile is a {match_score:.1f}% match for this role. "
            "Review the required skills and work on filling the identified gaps "
            "through online courses, certifications, or hands-on projects."
        )
    }
