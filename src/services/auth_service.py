"""
Serviço de Autenticação para gerenciamento de tokens JWT e verificação de usuários.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import jwt, JWTError
from sqlmodel import Session, select
from src.config.settings import settings
from src.models.user import User
from src.utils.security import verify_password, hash_password


class AuthService:
    """
    Serviço para autenticação de usuário, gerenciamento de senhas e tokens JWT.
    """

    def __init__(self, session: Session):
        self.session = session
        self.secret_key = settings.security_secret_key
        self.algorithm = settings.security_algorithm

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Autentica um usuário por e-mail e senha.
        """
        user = self.session.exec(
            select(User).where(User.email == email.lower().strip(), User.is_deleted == False)
        ).first()

        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        if not user.is_active:
            return None

        return user

    def create_access_token(
        self,
        data: dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Cria um token JWT de acesso.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.security_access_token_expire_minutes)

        to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_refresh_token(self, data: dict) -> str:
        """
        Cria um token JWT de renovação (refresh token).
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.security_refresh_token_expire_minutes)
        to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Decodifica e valida um token JWT.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None
