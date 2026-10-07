"""
Configuração do GUARA - Configurações prontas para produção com padrões de segurança rígidos.
Utiliza pydantic-settings para configuração tipada e validada.
"""

import os
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações da aplicação com padrões de segurança e endurecimento.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
        validate_assignment=True,
        revalidate_instances="always",
    )

    # Aplicação
    app_name: str = "GUARA"
    app_version: str = "0.1.0"
    debug: bool = False

    # Banco de Dados
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./guara.db")
    database_pool_size: int = 10
    database_max_overflow: int = 20
    database_echo: bool = False

    # Segurança
    security_secret_key: str = (
        os.getenv("SECRET_KEY", "chave-secreta-alterar-em-producao-com-no-minimo-32-bytes")
    )
    security_algorithm: str = "HS256"
    security_access_token_expire_minutes: int = 30
    security_refresh_token_expire_minutes: int = 604800  # 7 dias

    # Fator de custo do bcrypt - mínimo 12 para segurança em produção
    security_bcrypt_cost: int = 12

    # CORS (modo estrito - permite apenas origens específicas)
    cors_origins: List[str] = ["http://localhost:3000", "https://localhost:8000", "https://guara.example.com"]

    # API ORCID (Requisito HTTPS para redirecionamento OAuth 2.0)
    orcid_client_id: str = os.getenv("ORCID_CLIENT_ID", "")
    orcid_client_secret: str = os.getenv("ORCID_CLIENT_SECRET", "")
    orcid_redirect_uri: str = os.getenv("ORCID_REDIRECT_URI", "https://localhost:8000/api/auth/orcid/callback")
    orcid_scopes: List[str] = [
        "read_delimited_output",
        "read_publications",
        "read_works",
        "read_works_extended",
    ]

    # Limitação de taxa (Rate limiting)
    rate_limit_requests: int = 100
    rate_limit_period_seconds: int = 60

    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Validação de senhas
    password_min_length: int = 12
    password_require_uppercase: bool = True
    password_require_lowercase: bool = True
    password_require_numbers: bool = True
    password_require_special: bool = True

    @property
    def is_production(self) -> bool:
        """Verifica se está executando em modo de produção."""
        return not self.debug and self.database_echo is False

    @property
    def is_development(self) -> bool:
        """Verifica se está executando em modo de desenvolvimento."""
        return self.debug

    @property
    def allowed_origins(self) -> List[str]:
        """Obtém origens CORS validadas."""
        return [origin.strip() for origin in self.cors_origins if origin]


@lru_cache()
def get_settings() -> Settings:
    """Obtém instância de configurações em cache."""
    return Settings()


# Instância singleton para acesso direto
settings: Settings = get_settings()
