"""
Testes para o ORCIDService.
"""

import pytest
from src.services.orcid_service import ORCIDService


def test_get_orcid_auth_url():
    service = ORCIDService()
    state = "estado_teste_123"
    url = service.get_orcid_auth_url(state)
    assert "https://orcid.org/oauth/authorize?" in url
    assert "state=estado_teste_123" in url
    assert "response_type=code" in url
