"""
AuthService for GUARA authentication and JWT token management.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import jwt, JWTError
from sqlmodel import Session, select
from src.config.settings import settings
from src.models.user import User
from src.utils.security import verify_password, hash_password


class AuthService:
    """
    Service for user authentication, password management, and JWT creation/verification.
    """

    def __init__(self, session: Session):
        self.session = session
        self.secret_key = settings.security_secret_key
        self.algorithm = settings.security_algorithm

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password.
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
        Create a JWT access token.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.security_access_token_expire_minutes)

        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_refresh_token(self, data: dict) -> str:
        """
        Create a JWT refresh token.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.security_refresh_token_expire_minutes)
        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Decode and validate a JWT token.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None
