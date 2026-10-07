"""
GUARA Configuration - Production-ready settings with strict security defaults.
Uses pydantic-settings for type-safe, validated configuration.
"""

import os
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings with strict defaults and security hardening.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
        validate_assignment=True,
        revalidate_instances="always",
    )

    # Application
    app_name: str = "GUARA"
    app_version: str = "0.1.0"
    debug: bool = False

    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./guara.db")
    database_pool_size: int = 10
    database_max_overflow: int = 20
    database_echo: bool = False

    # Security
    security_secret_key: str = (
        os.getenv("SECRET_KEY", "your-secret-key-change-in-production-use-32-bytes-minimum")
    )
    security_algorithm: str = "HS256"
    security_access_token_expire_minutes: int = 30
    security_refresh_token_expire_minutes: int = 604800  # 7 days

    # bcrypt cost factor - minimum 12 for production security
    security_bcrypt_cost: int = 12

    # CORS (strict mode - only allow specific origins)
    cors_origins: List[str] = ["http://localhost:3000", "https://localhost:8000", "https://guara.example.com"]

    # ORCID API (HTTPS requirement for OAuth 2.0 redirect)
    orcid_client_id: str = os.getenv("ORCID_CLIENT_ID", "")
    orcid_client_secret: str = os.getenv("ORCID_CLIENT_SECRET", "")
    orcid_redirect_uri: str = os.getenv("ORCID_REDIRECT_URI", "https://localhost:8000/api/auth/orcid/callback")
    orcid_scopes: List[str] = [
        "read_delimited_output",
        "read_publications",
        "read_works",
        "read_works_extended",
    ]

    # Rate limiting
    rate_limit_requests: int = 100
    rate_limit_period_seconds: int = 60

    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Password hashing
    password_min_length: int = 12
    password_require_uppercase: bool = True
    password_require_lowercase: bool = True
    password_require_numbers: bool = True
    password_require_special: bool = True

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.debug and self.database_echo is False

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.debug

    @property
    def allowed_origins(self) -> List[str]:
        """Get validated CORS origins."""
        return [origin.strip() for origin in self.cors_origins if origin]


@lru_cache()
def get_settings() -> Settings:
    """Cached settings getter."""
    return Settings()


# Singleton instance for direct access
settings: Settings = get_settings()
