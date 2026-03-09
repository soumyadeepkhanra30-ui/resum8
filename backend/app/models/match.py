"""
SQLAlchemy model for match results.
Stores the computed match score between a candidate and a job.
"""
from sqlalchemy import Column, Integer, Float, Text, JSON, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.database import Base


class Match(Base):
    """Represents the computed match between a candidate and a job listing."""
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys linking to candidate and job
    candidate_id = Column(Integer, ForeignKey("candidates.id", ondelete="CASCADE"), index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), index=True)

    # Match score: 0.0 to 100.0 (percentage)
    match_score = Column(Float, nullable=False)

    # Raw cosine similarity: -1.0 to 1.0
    cosine_similarity = Column(Float, nullable=False)

    # Gap analysis: list of missing skills/areas
    missing_skills = Column(JSON, default=list)

    # AI-generated gap analysis text
    gap_analysis_text = Column(Text, default="")

    # AI-generated executive summary for this candidate-job pair
    executive_summary = Column(Text, default="")

    # Rank (1 = best match)
    rank = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Match candidate={self.candidate_id} job={self.job_id} score={self.match_score:.1f}%>"
