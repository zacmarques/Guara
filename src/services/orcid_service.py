"""
Serviço ORCID para Autenticação OAuth 2.0 e Integração com API.
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
    Serviço para manipulação da autenticação OAuth 2.0 e requisições da API ORCID.
    """

    def __init__(self, session: Optional[Session] = None):
        self.session = session
        self.client_id = settings.orcid_client_id
        self.client_secret = settings.orcid_client_secret
        self.redirect_uri = settings.orcid_redirect_uri
        self.scopes = settings.orcid_scopes

    def get_authorization_url(self, state: str) -> str:
        """Alias para get_orcid_auth_url."""
        return self.get_orcid_auth_url(state)

    def get_orcid_auth_url(self, state: str) -> str:
        """
        Gera a URL de autorização do ORCID para o fluxo OAuth 2.0.
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
        """Alias para exchange_code_for_token."""
        return await self.exchange_code_for_token(code)

    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """
        Troca o código de autorização por um token de acesso.
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
                detail=f"Falha ao trocar código ORCID por token: {str(e)}"
            )

    async def refresh_token(self, refresh_token_val: str) -> Dict[str, Any]:
        """
        Atualiza o token de acesso utilizando o refresh_token.
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
                detail=f"Falha ao atualizar token ORCID: {str(e)}"
            )

    async def get_user_profile(self, access_token: str, orcid_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtém informações do perfil do usuário na API do ORCID.
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
                detail=f"Falha ao obter perfil do usuário no ORCID: {str(e)}"
            )

    async def get_user_works(self, access_token: str, orcid_id: str) -> Dict[str, Any]:
        """
        Obtém as obras/produções do usuário na API do ORCID.
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
                detail=f"Falha ao obter produções do ORCID: {str(e)}"
            )

    async def get_user_by_orcid_id(self, orcid_id: str) -> Optional[User]:
        """
        Obtém usuário por ORCID ID na sessão do banco de dados.
        """
        if not self.session:
            return None
        user_service = UserService(self.session)
        return user_service.get_by_orcid_id(orcid_id)

    async def create_or_update_user_from_orcid(self, orcid_data: Dict[str, Any], user_id: Optional[str] = None) -> User:
        """
        Cria ou atualiza usuário com base nos dados do perfil do ORCID.
        """
        if not self.session:
            raise ValueError("Sessão do banco de dados é necessária")

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
