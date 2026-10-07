"""
Tests for UserService.
"""

import pytest
from sqlmodel import Session, create_engine, SQLModel
from src.services.user_service import UserService


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_create_user_success(session: Session):
    service = UserService(session)
    user = service.create_user(
        email="test@example.com",
        password="SecurePassword123!",
        username="testuser",
        full_name="Test User",
    )
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.is_active is True


def test_create_user_invalid_password(session: Session):
    service = UserService(session)
    with pytest.raises(ValueError, match="Password must be at least 12 characters"):
        service.create_user(email="test@example.com", password="short")


def test_authenticate_user(session: Session):
    service = UserService(session)
    service.create_user(
        email="auth@example.com",
        password="ValidPassword123!",
    )
    authenticated = service.authenticate_user("auth@example.com", "ValidPassword123!")
    assert authenticated is not None
    assert authenticated.email == "auth@example.com"

    failed = service.authenticate_user("auth@example.com", "WrongPassword123!")
    assert failed is None


def test_set_and_get_orcid_tokens(session: Session):
    service = UserService(session)
    user = service.create_user(
        email="orcid@example.com",
        password="ValidPassword123!",
    )
    service.set_orcid_tokens(
        user_id=user.id,
        orcid_id="0000-0001-2345-6789",
        access_token="access-123",
        refresh_token="refresh-456",
    )
    fetched = service.get_by_orcid_id("0000-0001-2345-6789")
    assert fetched is not None
    assert fetched.orcid_access_token == "access-123"
    assert fetched.orcid_refresh_token == "refresh-456"
