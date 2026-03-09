"""
Application configuration using pydantic-settings.
Loads all settings from environment variables or .env file.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Google Gemini API key for AI-powered features
    gemini_api_key: str = ""

    # PostgreSQL database URL (async)
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/resum8"

    # Frontend URL for CORS
    frontend_url: str = "http://localhost:5173"

    # Secret key for encryption helpers
    secret_key: str = "change-this-secret-key-in-production"

    # App settings
    app_name: str = "ResuM8"
    app_version: str = "1.0.0"
    debug: bool = False

    # Upload settings
    max_upload_size_mb: int = 10
    max_recruiter_uploads: int = 20

    # Data retention: if True, resume data is saved to DB; if False, processed in-memory only
    save_resume_data: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = False


# Singleton settings object
settings = Settings()
