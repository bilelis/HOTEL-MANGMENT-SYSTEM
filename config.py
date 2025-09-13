"""
Hotel Management System - Core Configuration
Handles application settings, database configuration, and security settings.
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings configuration."""
    
    # Application Information
    app_name: str = "Hotel Management System"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Database Configuration
    database_url: str = "postgresql://postgres:password@localhost:5432/hotel_management"
    test_database_url: Optional[str] = None
    
    # Security Configuration
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS Configuration
    allowed_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    @validator("allowed_origins", pre=True)
    def assemble_cors_origins(cls, v):
        """Parse CORS origins from environment variable."""
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()

# Database URL for SQLAlchemy
SQLALCHEMY_DATABASE_URL = settings.database_url

# Security settings
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

