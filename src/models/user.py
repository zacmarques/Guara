"""
Modelo de usuário com restrições rígidas de segurança.
Implementa autenticação e autorização seguras.
"""

from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship
from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.article import Article


class User(BaseModel, table=True):
    """
    Modelo de Usuário do sistema GUARA.
    """

    email: str = Field(
        max_length=255,
        index=True,
        unique=True,
        nullable=False,
    )
    username: Optional[str] = Field(
        default=None,
        max_length=50,
        nullable=True,
    )

    password_hash: str = Field(
        max_length=255,
        nullable=False,
    )

    orcid_id: Optional[str] = Field(
        default=None,
        max_length=20,
        index=True,
        unique=True,
        nullable=True,
    )
    orcid_access_token: Optional[str] = Field(
        default=None,
        nullable=True,
    )
    orcid_refresh_token: Optional[str] = Field(
        default=None,
        nullable=True,
    )

    is_active: bool = Field(
        default=True,
        index=True,
        nullable=False,
    )
    is_verified: bool = Field(
        default=False,
        nullable=False,
    )

    full_name: Optional[str] = Field(
        default=None,
        max_length=255,
        nullable=True,
    )
    organization: Optional[str] = Field(
        default=None,
        max_length=255,
        nullable=True,
    )

    # Relacionamento com Artigos
    articles: List["Article"] = Relationship(back_populates="user")
