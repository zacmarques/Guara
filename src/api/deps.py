"""
Dependency injection and security middleware for GUARA API.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session
from src.config.settings import settings
from src.models.user import User
from src.services.user_service import UserService


# Security: Never expose real secrets in error messages
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    auto_error=False,
)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token with secure defaults.
    
    Args:
        data: Token payload
        expires_delta: Token expiration (default 30 minutes)
        
    Returns:
        JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.security_access_token_expire_minutes)
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    
    # Use secure algorithm (HS256)
    encoded_jwt = jwt.encode(
        to_encode,
        settings.security_secret_key,
        algorithm=settings.security_algorithm,
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Create JWT refresh token with longer expiration (7 days).
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.security_refresh_token_expire_minutes)
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    
    return jwt.encode(
        to_encode,
        settings.security_secret_key,
        algorithm=settings.security_algorithm,
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> Optional[User]:
    """
    Get current authenticated user from JWT token.
    
    Fails securely - no stack traces exposed.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token,
            settings.security_secret_key,
            algorithms=[settings.security_algorithm],
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = UserService(Session()).get_user(user_id)
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get current active (non-deleted) user."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return current_user
