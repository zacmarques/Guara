"""
ORCID Authentication Endpoints for FastAPI.
"""

from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, status, Request, Depends
from sqlmodel import Session
from src.services.orcid_service import ORCIDService
from src.services.user_service import UserService
from src.services.auth_service import AuthService
from src.api.deps import get_session, get_current_user
from src.models.user import User
from src.config.settings import settings
import secrets
import uuid

router = APIRouter(prefix="/auth/orcid", tags=["ORCID Authentication"])

state_tokens = {}


@router.get("/login")
async def orcid_login(request: Request):
    """
    Initiate ORCID OAuth 2.0 authentication flow.
    """
    state = secrets.token_urlsafe(32)
    state_tokens[state] = {
        'timestamp': uuid.uuid4().hex,
        'redirect_url': request.query_params.get('redirect_url', '/dashboard')
    }
    orcid_service = ORCIDService()
    auth_url = orcid_service.get_orcid_auth_url(state)
    return {"auth_url": auth_url}


@router.get("/callback")
async def orcid_callback(
    request: Request,
    session: Session = Depends(get_session)
):
    """
    Handle ORCID OAuth 2.0 callback.
    """
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    if not state or state not in state_tokens:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or missing state parameter"
        )

    del state_tokens[state]

    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization code not provided"
        )

    try:
        orcid_service = ORCIDService(session=session)
        token_response = await orcid_service.exchange_code_for_token(code)

        access_token = token_response.get("access_token")
        refresh_token = token_response.get("refresh_token")
        orcid_id = token_response.get("orcid")

        if not access_token or not orcid_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve token or ORCID ID"
            )

        user_service = UserService(session)
        user = user_service.get_by_orcid_id(orcid_id)
        if not user:
            user = user_service.create_user(
                email=f"{orcid_id}@orcid.user",
                password=f"OrcidUser123!_{orcid_id}",
                orcid_id=orcid_id,
            )

        user_service.set_orcid_tokens(
            user_id=user.id,
            orcid_id=orcid_id,
            access_token=access_token,
            refresh_token=refresh_token
        )

        auth_service = AuthService(session)
        jwt_token = auth_service.create_access_token({"sub": user.id})

        return {
            "message": "ORCID authentication successful",
            "access_token": jwt_token,
            "token_type": "bearer",
            "user_id": user.id,
            "orcid_id": orcid_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error during ORCID authentication: {str(e)}"
        )


@router.get("/logout")
async def orcid_logout():
    """Logout from ORCID session."""
    return {"message": "ORCID logout successful", "status": "success"}


@router.get("/test")
async def orcid_test():
    """Test endpoint for ORCID configuration status."""
    return {"message": "ORCID service is working", "configured": bool(settings.orcid_client_id)}
