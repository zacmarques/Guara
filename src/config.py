import os
import logging
from typing import Optional

# Configuration settings
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./guara.db")
SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-32-bytes-minimum")
ORCID_CLIENT_ID: str = os.getenv("ORCID_CLIENT_ID", "")
ORCID_CLIENT_SECRET: str = os.getenv("ORCID_CLIENT_SECRET", "")
ORCID_REDIRECT_URI: str = os.getenv("ORCID_REDIRECT_URI", "http://localhost:8000/auth/orcid/callback")

# Security constants
JWT_ALGORITHM: str = "HS256"
JWT_EXPIRE_MINUTES: int = 30
BCRYPT_COST: int = 12

# Logging configuration
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

def setup_logging():
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

setup_logging()
logger = logging.getLogger("guara")
