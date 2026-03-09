"""
Summarizer service.
Generates AI-powered executive summaries for candidates using Google Gemini.
Used by recruiters to quickly understand a candidate's profile.
"""
from google import genai

from app.core.config import settings


async def generate_executive_summary(
    resume_text: str,
    candidate_name: str = "The candidate",
    job_title: str = "",
) -> str:
    """
    Generate a concise executive summary for a candidate.

    The summary highlights:
    - Total years of experience
    - Key technical skills and expertise
    - Notable achievements or projects
    - Any obvious strengths or gaps relative to the role

    Args:
        resume_text: Full text of the candidate's resume.
        candidate_name: Candidate's name (may be masked for privacy).
        job_title: Optional job title to tailor the summary.

    Returns:
        2-3 sentence executive summary string.
    """
    if not settings.gemini_api_key:
        return _fallback_summary(candidate_name)

    context = f"for the role of {job_title}" if job_title else ""

    prompt = f"""You are a senior HR analyst writing a concise executive summary 
for a recruiter {context}.

CANDIDATE: {candidate_name}

RESUME:
{resume_text[:4000]}

Write a 2-3 sentence executive summary that covers:
1. Total years of experience and primary domain
2. Core technical skills or expertise 
3. One notable strength OR one significant gap

Format: Plain text only. No bullet points. No headers. Be specific and factual.
Example: "8 years of full-stack development with expertise in Python, Django, and React. 
Strong background in e-commerce systems and microservices architecture. 
Lacks formal cloud certification (AWS/GCP) but has hands-on deployment experience."

Write the summary now:"""

    try:
        client = genai.Client(api_key=settings.gemini_api_key)
        response = await client.aio.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
        )
        return response.text.strip()
    except Exception:
        return _fallback_summary(candidate_name)


def _fallback_summary(candidate_name: str) -> str:
    """Fallback summary when AI is unavailable."""
    return (
        f"{candidate_name} has submitted their resume for consideration. "
        "Please review the full resume for detailed skills and experience. "
        "AI-powered summary generation is currently unavailable — check your GEMINI_API_KEY."
    )
