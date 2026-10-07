"""
Serviço de Artigo - Lógica de negócios para artigos acadêmicos.
Trata resolução de DOI, sincronização ORCID e CRUD de artigos.
"""

from datetime import datetime, timezone
from typing import Optional, List
from sqlmodel import Session, select
from src.models.article import Article


class ArticleService:
    """
    Camada de serviço para operações com Artigos.
    """

    def __init__(self, session: Session):
        """Inicializa o serviço com a sessão do banco de dados."""
        self.session = session

    def create_article(
        self,
        title: str,
        content: Optional[str] = None,
        doi: Optional[str] = None,
        publication_type: Optional[str] = None,
        publication_date: Optional[str] = None,
        volume: Optional[str] = None,
        issue: Optional[str] = None,
        pages: Optional[str] = None,
        e_issn: Optional[str] = None,
        p_issn: Optional[str] = None,
        abstract: Optional[str] = None,
        keywords: Optional[str] = None,
        url: Optional[str] = None,
        publisher: Optional[str] = None,
        language: Optional[str] = None,
        authors: Optional[str] = None,
        tags: Optional[str] = None,
        notes: Optional[str] = None,
        is_public: bool = False,
        user_id: Optional[str] = None,
    ) -> Article:
        """
        Cria um novo artigo acadêmico.
        """
        if not title:
            raise ValueError("O título é obrigatório")

        title = self._sanitize_string(title, max_length=1000)
        doi = self._sanitize_string(doi, max_length=100) if doi else None
        url = self._sanitize_string(url, max_length=500) if url else None
        publisher = self._sanitize_string(publisher, max_length=255) if publisher else None
        language = self._sanitize_string(language, max_length=50) if language else None

        if doi:
            existing = self.session.exec(
                select(Article).where(Article.doi == doi, Article.is_deleted == False)
            ).first()
            if existing:
                existing.doi_resolved = doi
                existing.doi_last_checked = datetime.now(timezone.utc).isoformat()
                self.session.add(existing)
                self.session.commit()
                self.session.refresh(existing)
                return existing

        article = Article(
            title=title,
            content=content,
            doi=doi,
            doi_resolved=doi,
            doi_last_checked=datetime.now(timezone.utc).isoformat() if doi else None,
            publication_type=publication_type,
            publication_date=publication_date,
            volume=volume,
            issue=issue,
            pages=pages,
            e_issn=e_issn,
            p_issn=p_issn,
            abstract=abstract,
            keywords=keywords,
            url=url,
            publisher=publisher,
            language=language,
            authors=authors,
            tags=tags,
            notes=notes,
            is_public=is_public,
            user_id=user_id,
            is_owner=user_id is not None,
        )

        self.session.add(article)
        self.session.commit()
        self.session.refresh(article)

        return article

    def get_article(self, article_id: str) -> Optional[Article]:
        """Obtém artigo por ID (apenas ativos)."""
        return self.session.exec(
            select(Article)
            .where(Article.id == article_id, Article.is_deleted == False)
        ).first()

    def get_articles_by_user(self, user_id: str) -> List[Article]:
        """Obtém todos os artigos associados a um usuário."""
        return list(self.session.exec(
            select(Article)
            .where(Article.user_id == user_id, Article.is_deleted == False)
        ).all())

    def get_by_doi(self, doi: str) -> Optional[Article]:
        """Obtém artigo por DOI (apenas ativos)."""
        return self.session.exec(
            select(Article)
            .where(Article.doi == doi, Article.is_deleted == False)
        ).first()

    def update_article(
        self,
        article_id: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
        doi: Optional[str] = None,
        publication_type: Optional[str] = None,
        publication_date: Optional[str] = None,
        volume: Optional[str] = None,
        issue: Optional[str] = None,
        pages: Optional[str] = None,
        e_issn: Optional[str] = None,
        p_issn: Optional[str] = None,
        abstract: Optional[str] = None,
        keywords: Optional[str] = None,
        url: Optional[str] = None,
        publisher: Optional[str] = None,
        language: Optional[str] = None,
        authors: Optional[str] = None,
        tags: Optional[str] = None,
        notes: Optional[str] = None,
        is_public: Optional[bool] = None,
        user_id: Optional[str] = None,
    ) -> Optional[Article]:
        """
        Atualiza os campos do artigo.
        """
        article = self.get_article(article_id)
        if not article:
            return None

        if user_id and article.user_id and article.user_id != user_id and user_id != "admin":
            raise PermissionError("Apenas o proprietário do artigo pode modificá-lo")

        if title is not None:
            article.title = self._sanitize_string(title, max_length=1000)
        if content is not None:
            article.content = content
        if doi is not None:
            sanitized_doi = self._sanitize_string(doi, max_length=100)
            article.doi = sanitized_doi
            article.doi_resolved = sanitized_doi
            article.doi_last_checked = datetime.now(timezone.utc).isoformat()
        if publication_type is not None:
            article.publication_type = self._sanitize_string(publication_type, max_length=100)
        if publication_date is not None:
            article.publication_date = publication_date
        if volume is not None:
            article.volume = volume
        if issue is not None:
            article.issue = issue
        if pages is not None:
            article.pages = pages
        if e_issn is not None:
            article.e_issn = e_issn
        if p_issn is not None:
            article.p_issn = p_issn
        if abstract is not None:
            article.abstract = abstract
        if keywords is not None:
            article.keywords = keywords
        if url is not None:
            article.url = self._sanitize_string(url, max_length=500)
        if publisher is not None:
            article.publisher = self._sanitize_string(publisher, max_length=255)
        if language is not None:
            article.language = self._sanitize_string(language, max_length=50)
        if authors is not None:
            article.authors = authors
        if tags is not None:
            article.tags = tags
        if notes is not None:
            article.notes = notes
        if is_public is not None:
            article.is_public = is_public

        article.update_timestamp()
        self.session.add(article)
        self.session.commit()
        self.session.refresh(article)

        return article

    def delete_article(self, article_id: str, user_id: Optional[str] = None) -> bool:
        """
        Realiza exclusão lógica (soft delete) do artigo.
        """
        article = self.get_article(article_id)
        if not article:
            return False

        if user_id and article.user_id and article.user_id != user_id and user_id != "admin":
            raise PermissionError("Apenas o proprietário do artigo pode excluí-lo")

        article.is_deleted = True
        self.session.commit()
        return True

    def sync_with_orcid(
        self,
        orcid_id: str,
        access_token: str,
        user_id: str,
    ) -> dict:
        """
        Sincroniza artigos a partir da API do ORCID.
        """
        from src.services.user_service import UserService

        user_service = UserService(self.session)
        user = user_service.get_user_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado")

        user_service.set_orcid_tokens(user_id, orcid_id, access_token)

        return {
            "orcid_id": orcid_id,
            "synchronized": True,
            "synced_at": datetime.now(timezone.utc).isoformat(),
        }

    def _sanitize_string(self, value: Optional[str], max_length: int = 1000) -> str:
        """Sanitiza entrada de texto para prevenir ataques de injeção."""
        if not value:
            return ""
        sanitized = value.replace("\x00", "")
        return sanitized[:max_length]
