"""
Base model for all GUARA models.
Provides common fields and security constraints.
"""

from datetime import datetime, timezone
import uuid
from typing import Optional
from sqlmodel import Field, SQLModel


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


class BaseModel(SQLModel):
    """Base model with common fields and security constraints."""

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True,
    )

    created_at: datetime = Field(
        default_factory=get_utc_now,
    )
    updated_at: datetime = Field(
        default_factory=get_utc_now,
    )

    is_deleted: bool = Field(
        default=False,
        index=True,
    )

    def is_not_deleted(self) -> bool:
        """Check if the record is not soft-deleted."""
        return not self.is_deleted

    def update_timestamp(self) -> None:
        """Update the last modified timestamp."""
        self.updated_at = datetime.now(timezone.utc)
