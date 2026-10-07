"""
Article model for academic publications.
Supports ORCID integration and DOI lookup.
"""

from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.user import User


class Article(BaseModel, table=True):
    """
    Academic article model with ORCID integration.
    """

    title: str = Field(
        max_length=1000,
        nullable=False,
    )
    content: Optional[str] = Field(
        default=None,
        nullable=True,
    )
    doi: Optional[str] = Field(
        default=None,
        max_length=100,
        index=True,
        nullable=True,
    )
    doi_resolved: Optional[str] = Field(
        default=None,
        nullable=True,
    )
    doi_last_checked: Optional[str] = Field(
        default=None,
        nullable=True,
    )

    publication_type: Optional[str] = Field(
        default=None,
        max_length=100,
        nullable=True,
    )
    publication_date: Optional[str] = Field(
        default=None,
        max_length=50,
        nullable=True,
    )
    volume: Optional[str] = Field(
        default=None,
        max_length=50,
        nullable=True,
    )
    issue: Optional[str] = Field(
        default=None,
        max_length=50,
        nullable=True,
    )
    pages: Optional[str] = Field(
        default=None,
        max_length=100,
        nullable=True,
    )
    e_issn: Optional[str] = Field(
        default=None,
        max_length=50,
        nullable=True,
    )
    p_issn: Optional[str] = Field(
        default=None,
        max_length=50,
        nullable=True,
    )

    abstract: Optional[str] = Field(
        default=None,
        max_length=4000,
        nullable=True,
    )
    keywords: Optional[str] = Field(
        default=None,
        max_length=2000,
        nullable=True,
    )
    url: Optional[str] = Field(
        default=None,
        max_length=500,
        nullable=True,
    )
    publisher: Optional[str] = Field(
        default=None,
        max_length=255,
        nullable=True,
    )
    language: Optional[str] = Field(
        default=None,
        max_length=50,
        nullable=True,
    )

    authors: Optional[str] = Field(
        default=None,
        nullable=True,
    )

    orcid_synchronized: bool = Field(
        default=False,
        index=True,
        nullable=False,
    )
    orcid_sync_last_attempt: Optional[str] = Field(
        default=None,
        nullable=True,
    )
    orcid_sync_status: Optional[str] = Field(
        default=None,
        max_length=50,
        nullable=True,
    )

    user_id: Optional[str] = Field(
        default=None,
        foreign_key="user.id",
        nullable=True,
    )
    user: Optional["User"] = Relationship(back_populates="articles")

    is_owner: bool = Field(
        default=False,
        nullable=False,
    )

    status: str = Field(
        default="draft",
        nullable=False,
    )
    tags: Optional[str] = Field(
        default=None,
        max_length=500,
        nullable=True,
    )
    notes: Optional[str] = Field(
        default=None,
        max_length=2000,
        nullable=True,
    )
    is_public: bool = Field(
        default=False,
        nullable=False,
    )
