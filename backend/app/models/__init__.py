"""Models package init — imports all models so SQLAlchemy discovers them."""
from app.models.job import Job
from app.models.candidate import Candidate
from app.models.match import Match

__all__ = ["Job", "Candidate", "Match"]
