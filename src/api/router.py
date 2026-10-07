"""
Main API router for GUARA.
Organizes routes by domain and applies security middleware.
"""

from fastapi import APIRouter
from src.api.router import router as api_router
from src.api import router as api
