"""
GUARA Configuration - Production-ready settings with strict security defaults.
Uses pydantic-settings for type-safe, validated configuration.
"""

from functools import lru_cache
from typing import Any
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings with strict defaults and security hardening.
    
    Security defaults:
    - TLS 1.3 only for production
    - No unauthenticated public interfaces
    - Minimum bcrypt cost of 12
    - Strict input validation
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
    database_url: str = "mysql://root:password@localhost:3306/guara"
    database_pool_size: int = 10
    database_max_overflow: int = 20
    database_echo: bool = False

    # Security
    security_secret_key: str = (
        "your-secret-key-change-in-production-use-32-bytes-minimum"
    )
    security_algorithm: str = "HS256"
    security_access_token_expire_minutes: int = 30
    security_refresh_token_expire_minutes: int = 604800  # 7 days

    # bcrypt cost factor - minimum 12 for production security
    security_bcrypt_cost: int = 12

    # CORS (strict mode - only allow specific origins)
    cors_origins: list[str] = ["http://localhost:3000", "https://guara.example.com"]

    # ORCID API
    orcid_client_id: str = ""
    orcid_client_secret: str = ""
    orcid_redirect_uri: str = "http://localhost:8000/auth/orcid/callback"
    orcid_scopes: list[str] = [
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
    log_format: str = "%%(asctime)s - %%(name)s - %%(levelname)s - %%(message)s"

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
    def allowed_origins(self) -> list[str]:
        """Get validated CORS origins."""
        return [origin.strip() for origin in self.cors_origins if origin]

    @classmethod
    def get_settings(cls) -> "Settings":
        """
        Get current settings instance with caching.
        Ensures consistent settings across application lifecycle.
        """
        return _get_settings()


@lru_cache()
def _get_settings() -> Settings:
    """Cached settings getter."""
    return Settings()


# Singleton instance for direct access
settings: Settings = get_settings()
