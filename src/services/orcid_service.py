"""
ORCID Service for OAuth 2.0 Authentication and API Integration.
"""

from typing import Optional, Dict, Any
from urllib.parse import urlencode
import httpx
from fastapi import HTTPException, status
from src.config.settings import settings
from src.models.user import User
from src.services.user_service import UserService

class ORCIDService:
    """
    Service for handling ORCID OAuth 2.0 authentication and API interactions.
    """

    def __init__(self):
        self.client_id = settings.orcid_client_id
        self.client_secret = settings.orcid_client_secret
        self.redirect_uri = settings.orcid_redirect_uri
        self.scopes = settings.orcid_scopes

    def get_orcid_auth_url(self, state: str) -> str:
        """
        Generate the ORCID authorization URL for OAuth 2.0 flow.
        
        Args:
            state (str): CSRF protection token
            
        Returns:
            str: Authorization URL for ORCID
        """
        if not self.client_id or not self.client_secret:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="ORCID client credentials not configured"
            )

        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': ' '.join(self.scopes),
            'state': state
        }

        # Build the authorization URL
        auth_url = f"https://orcid.org/oauth/authorize?{urlencode(params)}"
        return auth_url

    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access token.
        
        Args:
            code (str): Authorization code from ORCID
            
        Returns:
            Dict[str, Any]: Token response with access_token and refresh_token
        """
        if not self.client_id or not self.client_secret:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="ORCID client credentials not configured"
            )

        # Prepare token exchange request
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://orcid.org/oauth/token",
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to exchange ORCID code for token: {str(e)}"
            )

    async def get_user_profile(self, access_token: str) -> Dict[str, Any]:
        """
        Fetch user profile information from ORCID API.
        
        Args:
            access_token (str): Valid access token
            
        Returns:
            Dict[str, Any]: User profile data from ORCID
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://pub.orcid.org/v3.0/record",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Accept": "application/json"
                    }
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch ORCID user profile: {str(e)}"
            )

    async def get_user_by_orcid_id(self, orcid_id: str) -> Optional[User]:
        """
        Get user by ORCID ID from database.
        
        Args:
            orcid_id (str): ORCID identifier
            
        Returns:
            Optional[User]: User object if found, None otherwise
        """
        # This would need to be implemented with actual database access logic
        # For now, returning None as placeholder
        return None

    async def create_or_update_user_from_orcid(self, orcid_data: Dict[str, Any]) -> User:
        """
        Create or update user based on ORCID profile data.
        
        Args:
            orcid_data (Dict[str, Any]): ORCID profile data
            
        Returns:
            User: User object created or updated
        """
        # This would need to be implemented with actual database logic
        # For now, returning a placeholder User object
        return User(
            username="orcid_user",  # Placeholder - should extract from ORCID data
            email="orcid@example.com",  # Placeholder - should extract from ORCID data
            orcid_id="0000-0000-0000-0000"  # Placeholder - should extract from ORCID data
        )