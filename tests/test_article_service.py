"""
Tests for ArticleService.
"""

import pytest
from sqlmodel import Session, create_engine, SQLModel
from src.services.user_service import UserService
from src.services.article_service import ArticleService


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_create_and_get_article(session: Session):
    user_service = UserService(session)
    user = user_service.create_user(email="author@example.com", password="AuthorPassword123!")

    article_service = ArticleService(session)
    article = article_service.create_article(
        title="Quantum Computing Advancement",
        doi="10.1000/182",
        user_id=user.id,
    )
    assert article.id is not None
    assert article.title == "Quantum Computing Advancement"
    assert article.doi == "10.1000/182"

    fetched = article_service.get_article(article.id)
    assert fetched is not None
    assert fetched.title == "Quantum Computing Advancement"


def test_update_and_delete_article(session: Session):
    user_service = UserService(session)
    user = user_service.create_user(email="author2@example.com", password="AuthorPassword123!")

    article_service = ArticleService(session)
    article = article_service.create_article(
        title="Initial Title",
        user_id=user.id,
    )

    updated = article_service.update_article(
        article_id=article.id,
        title="Updated Title",
        user_id=user.id,
    )
    assert updated is not None
    assert updated.title == "Updated Title"

    deleted = article_service.delete_article(article.id, user_id=user.id)
    assert deleted is True
    assert article_service.get_article(article.id) is None


def test_sync_with_orcid(session: Session):
    user_service = UserService(session)
    user = user_service.create_user(email="orciduser@example.com", password="AuthorPassword123!")

    article_service = ArticleService(session)
    result = article_service.sync_with_orcid(
        orcid_id="0000-0002-1825-0097",
        access_token="token123",
        user_id=user.id,
    )
    assert result["synchronized"] is True
    assert result["orcid_id"] == "0000-0002-1825-0097"
