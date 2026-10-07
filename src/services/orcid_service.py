"""
ORCID Service for OAuth 2.0 Authentication and API Integration.
"""

from typing import Optional, Dict, Any
from urllib.parse import urlencode
import httpx
from fastapi import HTTPException, status
from sqlmodel import Session
from src.config.settings import settings
from src.models.user import User
from src.services.user_service import UserService


class ORCIDService:
    """
    Service for handling ORCID OAuth 2.0 authentication and API interactions.
    """

    def __init__(self, session: Optional[Session] = None):
        self.session = session
        self.client_id = settings.orcid_client_id
        self.client_secret = settings.orcid_client_secret
        self.redirect_uri = settings.orcid_redirect_uri
        self.scopes = settings.orcid_scopes

    def get_authorization_url(self, state: str) -> str:
        """Alias for get_orcid_auth_url."""
        return self.get_orcid_auth_url(state)

    def get_orcid_auth_url(self, state: str) -> str:
        """
        Generate the ORCID authorization URL for OAuth 2.0 flow.
        
        Args:
            state (str): CSRF protection token
            
        Returns:
            str: Authorization URL for ORCID
        """
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': ' '.join(self.scopes),
            'state': state
        }

        auth_url = f"https://orcid.org/oauth/authorize?{urlencode(params)}"
        return auth_url

    async def exchange_token(self, code: str) -> Dict[str, Any]:
        """Alias for exchange_code_for_token."""
        return await self.exchange_code_for_token(code)

    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access token.
        
        Args:
            code (str): Authorization code from ORCID
            
        Returns:
            Dict[str, Any]: Token response with access_token and refresh_token
        """
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
                    headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to exchange ORCID code for token: {str(e)}"
            )

    async def refresh_token(self, refresh_token_val: str) -> Dict[str, Any]:
        """
        Refresh access token using refresh_token.
        """
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token_val,
            'redirect_uri': self.redirect_uri
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://orcid.org/oauth/token",
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to refresh ORCID token: {str(e)}"
            )

    async def get_user_profile(self, access_token: str, orcid_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch user profile information from ORCID API.
        
        Args:
            access_token (str): Valid access token
            orcid_id (str, optional): ORCID ID
            
        Returns:
            Dict[str, Any]: User profile data from ORCID
        """
        url = f"https://pub.orcid.org/v3.0/{orcid_id}/record" if orcid_id else "https://pub.orcid.org/v3.0/record"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
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

    async def get_user_works(self, access_token: str, orcid_id: str) -> Dict[str, Any]:
        """
        Fetch user works from ORCID API.
        """
        url = f"https://pub.orcid.org/v3.0/{orcid_id}/works"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
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
                detail=f"Failed to fetch ORCID works: {str(e)}"
            )

    async def get_user_by_orcid_id(self, orcid_id: str) -> Optional[User]:
        """
        Get user by ORCID ID from database session.
        """
        if not self.session:
            return None
        user_service = UserService(self.session)
        return user_service.get_by_orcid_id(orcid_id)

    async def create_or_update_user_from_orcid(self, orcid_data: Dict[str, Any], user_id: Optional[str] = None) -> User:
        """
        Create or update user based on ORCID profile data.
        """
        if not self.session:
            raise ValueError("Database session is required")

        user_service = UserService(self.session)
        orcid_id = orcid_data.get("orcid-identifier", {}).get("path") or orcid_data.get("orcid")

        if user_id:
            user = user_service.get_user_by_id(user_id)
            if user:
                if orcid_id:
                    user.orcid_id = orcid_id
                self.session.add(user)
                self.session.commit()
                self.session.refresh(user)
                return user

        if orcid_id:
            user = user_service.get_by_orcid_id(orcid_id)
            if user:
                return user

        email = f"{orcid_id}@orcid.user" if orcid_id else "orcid_user@example.com"
        dummy_password = f"OrcidUser123!_{orcid_id}"
        return user_service.create_user(
            email=email,
            password=dummy_password,
            username=orcid_id,
            orcid_id=orcid_id,
        )
