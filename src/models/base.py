"""
Modelo base para todos os modelos do GUARA.
Fornece campos comuns e restrições de segurança.
"""

from datetime import datetime, timezone
import uuid
from typing import Optional
from sqlmodel import Field, SQLModel


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


class BaseModel(SQLModel):
    """Modelo base com campos comuns e auditoria."""

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
        """Verifica se o registro não está marcado como excluído."""
        return not self.is_deleted

    def update_timestamp(self) -> None:
        """Atualiza a data/hora da última modificação."""
        self.updated_at = datetime.now(timezone.utc)
