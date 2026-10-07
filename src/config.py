import os
from typing import Optional

# Variáveis de ambiente
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./guara.db")
SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
ORCID_CLIENT_ID: str = os.getenv("ORCID_CLIENT_ID", "")
ORCID_CLIENT_SECRET: str = os.getenv("ORCID_CLIENT_SECRET", "")

# Constantes de segurança
JWT_ALGORITHM: str = "HS256"
JWT_EXPIRE_MINUTES: int = 30

# Níveis de logging
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")