"""
SQLAlchemy model for job listings.
Stores job title, description, required skills, and embedding vector.
"""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.sql import func
from app.db.database import Base


class Job(Base):
    """Represents a job listing in the database."""
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    company = Column(String(200), nullable=False)
    location = Column(String(200), default="Remote")
    job_type = Column(String(50), default="Full-time")  # Full-time, Part-time, Contract
    experience_level = Column(String(50), default="Mid-level")  # Entry, Mid, Senior, Lead

    # Job description and requirements
    description = Column(Text, nullable=False)
    required_skills = Column(JSON, default=list)   # List of required skill strings
    preferred_skills = Column(JSON, default=list)  # List of nice-to-have skills
    salary_range = Column(String(100), default="")

    # Category for grouping (e.g., "Engineering", "Data Science", "Product")
    category = Column(String(100), default="Engineering")

    # Pre-computed embedding vector stored as JSON array
    # This is generated once and reused for all matching operations
    embedding = Column(JSON, default=None)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Job id={self.id} title='{self.title}' company='{self.company}'>"
