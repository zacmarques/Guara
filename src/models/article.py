"""
Article model for academic publications.
Supports ORCID integration and DOI lookup.
"""

from typing import Optional
from sqlmodel import Field, SQLModel


class Article(SQLModel, table=True):
    """
    Academic article model with ORCID integration.
    
    Fields based on central_producoes_historicas.xlsx:
    - Basic bibliographic data
    - ORCID synchronization
    - DOI resolution
    - User associations
    """

    # Basic bibliographic data
    title: str = Field(
        max_length=1000,
        sa_column=Field(
            name="title",
            type_=str,
            nullable=False,
        ),
    )
    doi: Optional[str] = Field(
        max_length=100,
        index=True,
        sa_column=Field(
            name="doi",
            type_=str,
            nullable=True,
            index=True,
        ),
    )
    doi_resolved: Optional[str] = Field(
        sa_column=Field(
            name="doi_resolved",
            type_=str,
            nullable=True,
        ),
    )
    doi_last_checked: Optional[str] = Field(
        sa_column=Field(
            name="doi_last_checked",
            type_=str,
            nullable=True,
        ),
    )

    # Publication data
    publication_type: Optional[str] = Field(
        max_length=100,
        sa_column=Field(
            name="publication_type",
            type_=str,
            nullable=True,
        ),
    )
    publication_date: Optional[str] = Field(
        max_length=50,
        sa_column=Field(
            name="publication_date",
            type_=str,
            nullable=True,
        ),
    )
    volume: Optional[str] = Field(
        max_length=50,
        sa_column=Field(
            name="volume",
            type_=str,
            nullable=True,
        ),
    )
    issue: Optional[str] = Field(
        max_length=50,
        sa_column=Field(
            name="issue",
            type_=str,
            nullable=True,
        ),
    )
    pages: Optional[str] = Field(
        max_length=100,
        sa_column=Field(
            name="pages",
            type_=str,
            nullable=True,
        ),
    )
    e_issn: Optional[str] = Field(
        max_length=50,
        sa_column=Field(
            name="e_issn",
            type_=str,
            nullable=True,
        ),
    )
    p_issn: Optional[str] = Field(
        max_length=50,
        sa_column=Field(
            name="p_issn",
            type_=str,
            nullable=True,
        ),
    )

    # Content
    abstract: Optional[str] = Field(
        max_length=4000,
        sa_column=Field(
            name="abstract",
            type_=str,
            nullable=True,
        ),
    )
    keywords: Optional[str] = Field(
        max_length=2000,
        sa_column=Field(
            name="keywords",
            type_=str,
            nullable=True,
        ),
    )
    url: Optional[str] = Field(
        max_length=500,
        sa_column=Field(
            name="url",
            type_=str,
            nullable=True,
        ),
    )
    publisher: Optional[str] = Field(
        max_length=255,
        sa_column=Field(
            name="publisher",
            type_=str,
            nullable=True,
        ),
    )
    language: Optional[str] = Field(
        max_length=50,
        sa_column=Field(
            name="language",
            type_=str,
            nullable=True,
        ),
    )

    # Author data (JSON format for flexibility)
    authors: Optional[str] = Field(
        sa_column=Field(
            name="authors",
            type_=str,
            nullable=True,
        ),
    )

    # ORCID synchronization
    orcid_synchronized: bool = Field(
        default=False,
        index=True,
        sa_column=Field(
            name="orcid_synchronized",
            type_=bool,
            nullable=False,
            default=False,
            index=True,
        ),
    )
    orcid_sync_last_attempt: Optional[str] = Field(
        sa_column=Field(
            name="orcid_sync_last_attempt",
            type_=str,
            nullable=True,
        ),
    )
    orcid_sync_status: Optional[str] = Field(
        max_length=50,
        sa_column=Field(
            name="orcid_sync_status",
            type_=str,
            nullable=True,
        ),
    )

    # User associations
    user_id: Optional[str] = Field(
        sa_column=Field(
            name="user_id",
            type_=str,
            nullable=True,
        ),
    )
    is_owner: bool = Field(
        default=False,
        sa_column=Field(
            name="is_owner",
            type_=bool,
            nullable=False,
            default=False,
        ),
    )

    # Status and metadata
    status: str = Field(
        default="draft",
        sa_column=Field(
            name="status",
            type_=str,
            nullable=False,
            default="draft",
        ),
    )
    tags: Optional[str] = Field(
        max_length=500,
        sa_column=Field(
            name="tags",
            type_=str,
            nullable=True,
        ),
    )
    notes: Optional[str] = Field(
        max_length=2000,
        sa_column=Field(
            name="notes",
            type_=str,
            nullable=True,
        ),
    )
    is_public: bool = Field(
        default=False,
        sa_column=Field(
            name="is_public",
            type_=bool,
            nullable=False,
            default=False,
        ),
    )

    def update_timestamp(self) -> None:
        """Update the last modified timestamp."""
        from src.models.base import BaseModel

        BaseModel.update_timestamp(self)
