"""
Base model for all GUARA models.
Provides common fields and security constraints.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel, table=True):
    """Base model with common fields and security constraints."""

    # Security: UUIDs prevent enumeration attacks
    id: Optional[str] = Field(
        default=None,
        primary_key=True,
        index=True,
        sa_column=Field(
            name="id",
            type_=str,
            nullable=False,
            default=lambda: str(__import__("uuid").uuid4()),
        ),
    )

    # Audit fields with proper timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Field(
            name="created_at",
            type_=datetime,
            nullable=False,
            server_default="CURRENT_TIMESTAMP",
        ),
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Field(
            name="updated_at",
            type_=datetime,
            nullable=False,
            server_default="CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
        ),
    )

    # Soft delete for data retention
    is_deleted: bool = Field(
        default=False,
        index=True,
        sa_column=Field(
            name="is_deleted",
            type_=bool,
            nullable=False,
            default=False,
        ),
    )

    def is_active(self) -> bool:
        """Check if the record is not soft-deleted."""
        return not self.is_deleted

    def update_timestamp(self) -> None:
        """Update the last modified timestamp."""
        self.updated_at = datetime.utcnow()
