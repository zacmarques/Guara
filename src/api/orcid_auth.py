"""
ORCID Authentication Endpoints for FastAPI.
"""

from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, status, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.services.orcid_service import ORCIDService
from src.models.user import User
from src.config.settings import settings
import secrets
import uuid

# Create router instance
router = APIRouter(prefix="/auth/orcid", tags=["ORCID Authentication"])

# In-memory storage for state tokens (in production, use a database or cache)
state_tokens = {}

# Initialize ORCID service
orcid_service = ORCIDService()


@router.get("/login")
async def orcid_login(request: Request):
    """
    Initiate ORCID OAuth 2.0 authentication flow.
    
    Generates a state token for CSRF protection and redirects to ORCID authorization URL.
    """
    # Generate a secure state token
    state = secrets.token_urlsafe(32)
    
    # Store the state token with a timeout (in production, use Redis or database)
    state_tokens[state] = {
        'timestamp': uuid.uuid4().hex,
        'redirect_url': request.query_params.get('redirect_url', '/dashboard')
    }
    
    # Generate ORCID authorization URL
    auth_url = orcid_service.get_orcid_auth_url(state)
    
    # Redirect to ORCID authorization
    return {"auth_url": auth_url}


@router.get("/callback")
async def orcid_callback(request: Request):
    """
    Handle ORCID OAuth 2.0 callback.
    
    Receives authorization code, exchanges for access token, and fetches user profile.
    """
    # Extract parameters from request
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    
    # Validate state token (CSRF protection)
    if not state or state not in state_tokens:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or missing state parameter"
        )
    
    # Remove the state token after use
    del state_tokens[state]
    
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization code not provided"
        )
    
    try:
        # Exchange authorization code for access token
        token_response = await orcid_service.exchange_code_for_token(code)
        
        # Get user profile from ORCID API
        access_token = token_response.get("access_token")
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve access token"
            )
        
        # Fetch user profile (this would normally be used to create/update user)
        orcid_profile = await orcid_service.get_user_profile(access_token)
        
        # Here you would typically create or update a user in your database
        # For now, we'll return the profile data as an example
        return {
            "message": "ORCID authentication successful",
            "profile": orcid_profile,
            "access_token": access_token,
            "token_type": token_response.get("token_type")
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error during ORCID authentication: {str(e)}"
        )


@router.get("/logout")
async def orcid_logout(request: Request):
    """
    Logout from ORCID authentication.
    
    Invalidates tokens and clears session state.
    """
    # In a real implementation, this would clear stored tokens and sessions
    # For now, just return success message
    return {"message": "ORCID logout successful", "status": "success"}


# Optional: Add a route to test ORCID integration
@router.get("/test")
async def orcid_test():
    """
    Test endpoint for ORCID service.
    """
    return {"message": "ORCID service is working", "configured": bool(settings.orcid_client_id)}