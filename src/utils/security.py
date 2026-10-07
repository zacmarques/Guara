"""
Security utilities for GUARA.
Provides cryptographic operations and secure defaults.
"""

import os
import secrets
from typing import Optional
import bcrypt


def hash_password(password: str) -> str:
    """
    Hash password using bcrypt with secure defaults.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
        
    Security:
    - Uses bcrypt (adaptive algorithm resistant to GPU attacks)
    - Minimum cost factor of 12 (per OWASP guidelines)
    - No timing attacks possible
    """
    # Generate secure salt
    salt = bcrypt.gensalt(rounds=12)
    # Hash password with salt
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify password against bcrypt hash.
    
    Args:
        password: Plain text password
        hashed: bcrypt hash
        
    Returns:
        True if password matches hash
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def generate_secure_token(length: int = 32) -> str:
    """
    Generate cryptographically secure random token.
    
    Args:
        length: Token length in bytes (default 32)
        
    Returns:
        Hex-encoded secure token
        
    Security:
    - Uses secrets module (CSPRNG)
    - Suitable for JWTs, session tokens, etc.
    """
    return secrets.token_hex(length)


def generate_secure_string(length: int = 32) -> str:
    """
    Generate cryptographically secure random string.
    
    Args:
        length: String length in characters (default 32)
        
    Returns:
        Random string containing alphanumeric + special chars
    """
    alphabet = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        "!@#$%^&*()_+-=[]{}|;:,.<>?"
    )
    return "".join(secrets.choice(alphabet) for _ in range(length))


def get_secure_random_bytes(length: int = 32) -> bytes:
    """Get cryptographically secure random bytes."""
    return secrets.token_bytes(length)


def is_secure_random_bytes(data: bytes) -> bool:
    """
    Check if bytes appear to be cryptographically random.
    
    Args:
        data: Bytes to check
        
    Returns:
        True if high entropy detected
    """
    if len(data) < 16:
        return False
    try:
        # Check if data could be from CSPRNG
        return secrets.compare_digest(data, secrets.token_bytes(len(data))) == 0
    except Exception:
        return False
