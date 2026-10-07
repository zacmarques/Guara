"""
API Router for Users, Articles, and Authentication.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlmodel import Session

from src.api.deps import get_session, get_current_user
from src.models.user import User
from src.models.article import Article
from src.services.user_service import UserService
from src.services.article_service import ArticleService
from src.services.auth_service import AuthService

router = APIRouter()


# --- Schemas ---

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None
    full_name: Optional[str] = None
    organization: Optional[str] = None


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class ArticleCreateRequest(BaseModel):
    title: str
    content: Optional[str] = None
    doi: Optional[str] = None
    publication_type: Optional[str] = None
    publication_date: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    e_issn: Optional[str] = None
    p_issn: Optional[str] = None
    abstract: Optional[str] = None
    keywords: Optional[str] = None
    url: Optional[str] = None
    publisher: Optional[str] = None
    language: Optional[str] = None
    authors: Optional[str] = None
    tags: Optional[str] = None
    notes: Optional[str] = None
    is_public: bool = False


class ArticleUpdateRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    doi: Optional[str] = None
    publication_type: Optional[str] = None
    publication_date: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    e_issn: Optional[str] = None
    p_issn: Optional[str] = None
    abstract: Optional[str] = None
    keywords: Optional[str] = None
    url: Optional[str] = None
    publisher: Optional[str] = None
    language: Optional[str] = None
    authors: Optional[str] = None
    tags: Optional[str] = None
    notes: Optional[str] = None
    is_public: Optional[bool] = None


# --- Auth & User Endpoints ---

@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register_user(
    data: UserRegisterRequest,
    session: Session = Depends(get_session)
):
    """Register a new user."""
    user_service = UserService(session)
    try:
        user = user_service.create_user(
            email=data.email,
            password=data.password,
            username=data.username,
            full_name=data.full_name,
            organization=data.organization,
        )
        return {"id": user.id, "email": user.email, "message": "User registered successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/auth/login")
def login_user(
    data: UserLoginRequest,
    session: Session = Depends(get_session)
):
    """Authenticate user and return JWT access token."""
    auth_service = AuthService(session)
    user = auth_service.authenticate_user(data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = auth_service.create_access_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer", "user_id": user.id}


@router.get("/users/me")
def get_me(current_user: User = Depends(get_current_user)):
    """Get profile of authenticated user."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "organization": current_user.organization,
        "orcid_id": current_user.orcid_id,
    }


# --- Article CRUD Endpoints ---

@router.post("/articles", status_code=status.HTTP_201_CREATED)
def create_article(
    data: ArticleCreateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Create a new academic article."""
    article_service = ArticleService(session)
    try:
        article = article_service.create_article(
            title=data.title,
            content=data.content,
            doi=data.doi,
            publication_type=data.publication_type,
            publication_date=data.publication_date,
            volume=data.volume,
            issue=data.issue,
            pages=data.pages,
            e_issn=data.e_issn,
            p_issn=data.p_issn,
            abstract=data.abstract,
            keywords=data.keywords,
            url=data.url,
            publisher=data.publisher,
            language=data.language,
            authors=data.authors,
            tags=data.tags,
            notes=data.notes,
            is_public=data.is_public,
            user_id=current_user.id,
        )
        return article
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/articles")
def list_articles(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """List all articles owned by authenticated user."""
    article_service = ArticleService(session)
    return article_service.get_articles_by_user(current_user.id)


@router.get("/articles/{article_id}")
def get_article(
    article_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Get single article by ID."""
    article_service = ArticleService(session)
    article = article_service.get_article(article_id)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    if not article.is_public and article.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return article


@router.put("/articles/{article_id}")
def update_article(
    article_id: str,
    data: ArticleUpdateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Update existing article."""
    article_service = ArticleService(session)
    try:
        updated = article_service.update_article(
            article_id=article_id,
            user_id=current_user.id,
            **data.dict(exclude_unset=True)
        )
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
        return updated
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.delete("/articles/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(
    article_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Soft delete an article."""
    article_service = ArticleService(session)
    try:
        success = article_service.delete_article(article_id, user_id=current_user.id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
        return None
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
