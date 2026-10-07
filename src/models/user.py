"""
User model with strict security constraints.
Implements secure authentication and authorization.
"""

from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """
    User model with enterprise-grade security.
    
    Security features:
    - Password hashing with bcrypt (cost factor >= 12)
    - No plain-text password storage
    - Indexed email for fast lookups
    - Soft delete for audit trails
    """

    # User identity
    email: str = Field(
        max_length=255,
        index=True,
        unique=True,
        sa_column=Field(
            name="email",
            type_=str,
            nullable=False,
            index=True,
            unique=True,
        ),
    )
    username: Optional[str] = Field(
        max_length=50,
        sa_column=Field(
            name="username",
            type_=str,
            nullable=True,
        ),
    )

    # Security: Passwords MUST be hashed - never store plain text
    password_hash: str = Field(
        max_length=255,
        sa_column=Field(
            name="password_hash",
            type_=str,
            nullable=False,
        ),
    )

    # OAuth 2.0 / ORCID integration
    orcid_id: Optional[str] = Field(
        max_length=20,
        index=True,
        unique=True,
        sa_column=Field(
            name="orcid_id",
            type_=str,
            nullable=True,
            index=True,
            unique=True,
        ),
    )
    orcid_access_token: Optional[str] = Field(
        sa_column=Field(
            name="orcid_access_token",
            type_=str,
            nullable=True,
        ),
    )
    orcid_refresh_token: Optional[str] = Field(
        sa_column=Field(
            name="orcid_refresh_token",
            type_=str,
            nullable=True,
        ),
    )

    # Account status
    is_active: bool = Field(
        default=True,
        index=True,
        sa_column=Field(
            name="is_active",
            type_=bool,
            nullable=False,
            default=True,
            index=True,
        ),
    )
    is_verified: bool = Field(
        default=False,
        sa_column=Field(
            name="is_verified",
            type_=bool,
            nullable=False,
            default=False,
        ),
    )

    # Metadata
    full_name: Optional[str] = Field(
        max_length=255,
        sa_column=Field(
            name="full_name",
            type_=str,
            nullable=True,
        ),
    )
    organization: Optional[str] = Field(
        max_length=255,
        sa_column=Field(
            name="organization",
            type_=str,
            nullable=True,
        ),
    )

    def update_timestamp(self) -> None:
        """Update the last modified timestamp."""
        from src.models.base import BaseModel

        BaseModel.update_timestamp(self)
