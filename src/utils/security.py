"""Utilitários de segurança para o GUARA.
Fornece operações criptográficas e configurações seguras por padrão."""

import os
import secrets
from typing import Optional
import bcrypt


def hash_password(password: str) -> str:
    """
    Hashar senha utilizando bcrypt com configurações seguras por padrão.
    
    Args:
        password: Senha em texto simples
        
    Returns:
        Senha hash
        
    Segurança:
    - Utiliza bcrypt (algoritmo adaptativo resistente a ataques de GPU)
    - Fator de custo mínimo de 12 (conforme diretrizes OWASP)
    - Não há ataques de tempo possíveis
    """
    # Gerar sal seguro
    salt = bcrypt.gensalt(rounds=12)
    # Hashar senha com sal
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """
    Verificar senha contra o hash do bcrypt.
    
    Args:
        password: Senha em texto simples
        hashed: hash do bcrypt
        
    Returns:
        True se a senha corresponder ao hash
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def generate_secure_token(length: int = 32) -> str:
    """
    Gerar token aleatório cri
