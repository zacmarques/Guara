"""
Roteador Principal da API do GUARA.
Organiza as rotas por domínio e aplica configurações de segurança.
"""

from fastapi import APIRouter
from src.api.orcid_auth import router as orcid_auth_router
from src.api.router import router as api_router

# Cria roteador principal
main_router = APIRouter()

# Inclui rotas de autenticação ORCID
main_router.include_router(orcid_auth_router)

# Inclui rotas principais da API
main_router.include_router(api_router)
