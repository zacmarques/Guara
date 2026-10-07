"""
Main API router for GUARA.
Organizes routes by domain and applies security middleware.
"""

from fastapi import APIRouter
from src.api.orcid_auth import router as orcid_auth_router
from src.api.router import router as api_router

# Create main router
main_router = APIRouter()

# Include ORCID authentication routes
main_router.include_router(orcid_auth_router)

# Include core API routes
main_router.include_router(api_router)
