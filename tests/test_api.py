"""
Testes de integração para os Endpoints da API GUARA.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.pool import StaticPool
from src.main import app
from src.api.deps import get_session
from src.models import User, Article

test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)


@pytest.fixture(autouse=True)
def prepare_db():
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)


def override_get_session():
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_register_and_login_flow():
    reg_response = client.post(
        "/api/auth/register",
        json={
            "email": "apiuser@example.com",
            "password": "ApiUser123!_Pass",
            "full_name": "Usuário da API",
        },
    )
    assert reg_response.status_code == 201
    assert reg_response.json()["email"] == "apiuser@example.com"

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "apiuser@example.com",
            "password": "ApiUser123!_Pass",
        },
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    assert token is not None

    me_response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "apiuser@example.com"


def test_article_crud_flow():
    # Cadastro e Login
    client.post(
        "/api/auth/register",
        json={"email": "writer@example.com", "password": "Writer123!_Pass"},
    )
    login_res = client.post(
        "/api/auth/login",
        json={"email": "writer@example.com", "password": "Writer123!_Pass"},
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Criar Artigo
    create_res = client.post(
        "/api/articles",
        headers=headers,
        json={"title": "Novo Artigo de Pesquisa", "doi": "10.1000/182_test"},
    )
    assert create_res.status_code == 201
    article_id = create_res.json()["id"]

    # Obter Artigos
    list_res = client.get("/api/articles", headers=headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1

    # Atualizar Artigo
    update_res = client.put(
        f"/api/articles/{article_id}",
        headers=headers,
        json={"title": "Título do Artigo Atualizado"},
    )
    assert update_res.status_code == 200
    assert update_res.json()["title"] == "Título do Artigo Atualizado"

    # Excluir Artigo
    delete_res = client.delete(f"/api/articles/{article_id}", headers=headers)
    assert delete_res.status_code == 204
