"""
Utilitários de segurança para o GUARA.
Fornece operações criptográficas e padrões seguros.
"""

import os
import secrets
from typing import Optional
import bcrypt


def hash_password(password: str) -> str:
    """
    Gera hash da senha utilizando bcrypt com configurações seguras.
    """
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """
    Verifica a senha informada contra o hash bcrypt.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def generate_secure_token(length: int = 32) -> str:
    """
    Gera token aleatório criptograficamente seguro.
    """
    return secrets.token_hex(length)


def generate_secure_string(length: int = 32) -> str:
    """
    Gera string aleatória criptograficamente segura.
    """
    alphabet = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        "!@#$%^&*()_+-=[]{}|;:,.<>?"
    )
    return "".join(secrets.choice(alphabet) for _ in range(length))


def get_secure_random_bytes(length: int = 32) -> bytes:
    """Obtém bytes aleatórios criptograficamente seguros."""
    return secrets.token_bytes(length)


def is_secure_random_bytes(data: bytes) -> bool:
    """
    Verifica se os bytes possuem alta entropia aleatória.
    """
    if len(data) < 16:
        return False
    try:
        return secrets.compare_digest(data, secrets.token_bytes(len(data))) == 0
    except Exception:
        return False
