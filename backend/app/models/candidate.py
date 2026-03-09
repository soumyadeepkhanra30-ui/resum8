"""
SQLAlchemy model for candidates.
Stores parsed resume data and optionally the encrypted resume text.
"""
from sqlalchemy import Column, Integer, String, Text, JSON, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.database import Base


class Candidate(Base):
    """Represents a candidate who has uploaded their resume."""
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    # Parsed personal info
    name = Column(String(200), default="")
    email = Column(String(200), default="")
    phone = Column(String(50), default="")
    location = Column(String(200), default="")

    # Extracted resume content
    resume_text = Column(Text, default="")      # Full extracted text (plain)
    skills = Column(JSON, default=list)         # Extracted skills list
    experience_years = Column(Integer, default=0)
    education = Column(JSON, default=list)      # List of education entries
    work_history = Column(JSON, default=list)   # List of work experience entries

    # Security: optional encrypted copy for data retention
    encrypted_resume = Column(Text, default=None)  # Fernet-encrypted resume text
    is_anonymized = Column(Boolean, default=False)  # Whether name/contact was masked

    # Embedding for semantic search
    embedding = Column(JSON, default=None)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # Auto-delete: candidates can be deleted after processing if save_resume_data=False
    expires_at = Column(DateTime(timezone=True), default=None)

    def __repr__(self):
        return f"<Candidate id={self.id} name='{self.name}'>"
