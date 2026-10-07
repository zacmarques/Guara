"""
Serviço de Usuário - Lógica de negócios para autenticação e integração ORCID.
Implementa armazenamento seguro de senhas e fluxo OAuth 2.0.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import Session, select
from src.models.user import User
from src.utils.security import hash_password, verify_password


class UserService:
    """
    Camada de serviço para operações de Usuário.
    """

    def __init__(self, session: Session):
        """Inicializa o serviço com a sessão do banco de dados."""
        self.session = session

    def create_user(
        self,
        email: str,
        password: str,
        username: Optional[str] = None,
        full_name: Optional[str] = None,
        organization: Optional[str] = None,
        orcid_id: Optional[str] = None,
    ) -> User:
        """
        Cria uma nova conta de usuário com hash de senha seguro.
        """
        if len(password) < 12:
            raise ValueError("A senha deve ter pelo menos 12 caracteres")
        
        if not any(c.isupper() for c in password):
            raise ValueError("A senha deve conter pelo menos uma letra maiúscula")
        if not any(c.islower() for c in password):
            raise ValueError("A senha deve conter pelo menos uma letra minúscula")
        if not any(c.isdigit() for c in password):
            raise ValueError("A senha deve conter pelo menos um dígito")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            raise ValueError("A senha deve conter pelo menos um caractere especial")

        # Verifica usuário existente
        existing = self.session.exec(
            select(User).where(User.email == email.lower().strip(), User.is_deleted == False)
        ).first()
        if existing:
<<<<<<< Updated upstream
            raise ValueError("E-mail já cadastrado no sistema")
=======
            raise ValueError("Email já registrado")
>>>>>>> Stashed changes

        password_hash = hash_password(password)

        user = User(
            email=email.lower().strip(),
            username=username,
            password_hash=password_hash,
            full_name=full_name,
            organization=organization,
            orcid_id=orcid_id,
            is_active=True,
            is_verified=False,
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def register_user(
        self,
        email: str,
        password: str,
        username: Optional[str] = None,
        full_name: Optional[str] = None,
        organization: Optional[str] = None,
    ) -> User:
        """Alias para create_user por compatibilidade."""
        return self.create_user(
            email=email,
            password=password,
            username=username,
            full_name=full_name,
            organization=organization,
        )

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Autentica o usuário com e-mail e senha.
        """
        user = self.session.exec(
            select(User).where(User.email == email.lower().strip(), User.is_deleted == False)
        ).first()
        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        if not user.is_active:
            return None

        return user

    def reset_password(self, user_id: str, new_password: str) -> bool:
        """
        Redefine a senha do usuário com segurança.
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return False

        if len(new_password) < 12:
            raise ValueError("A senha deve ter pelo menos 12 caracteres")
        
        if not any(c.isupper() for c in new_password):
            raise ValueError("A senha deve conter pelo menos uma letra maiúscula")
        if not any(c.islower() for c in new_password):
            raise ValueError("A senha deve conter pelo menos uma letra minúscula")
        if not any(c.isdigit() for c in new_password):
            raise ValueError("A senha deve conter pelo menos um dígito")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in new_password):
            raise ValueError("A senha deve conter pelo menos um caractere especial")

        new_hash = hash_password(new_password)
        user.password_hash = new_hash
        user.is_verified = True
        user.update_timestamp()

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return True

    def update_user(
        self,
        user_id: str,
        email: Optional[str] = None,
        username: Optional[str] = None,
        full_name: Optional[str] = None,
        organization: Optional[str] = None,
        orcid_id: Optional[str] = None,
        orcid_access_token: Optional[str] = None,
        orcid_refresh_token: Optional[str] = None,
    ) -> Optional[User]:
        """Atualiza os campos do usuário."""
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        if email is not None:
            user.email = email.lower().strip()
        if username is not None:
            user.username = username
        if full_name is not None:
            user.full_name = full_name
        if organization is not None:
            user.organization = organization
        if orcid_id is not None:
            user.orcid_id = orcid_id
        if orcid_access_token is not None:
            user.orcid_access_token = orcid_access_token
        if orcid_refresh_token is not None:
            user.orcid_refresh_token = orcid_refresh_token

        user.update_timestamp()
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Obtém usuário por ID (apenas ativos)."""
        return self.session.exec(
            select(User).where(User.id == user_id, User.is_deleted == False)
        ).first()

    def get_user(self, user_id: str) -> Optional[User]:
        """Alias para get_user_by_id."""
        return self.get_user_by_id(user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        """Obtém usuário por e-mail (apenas ativos)."""
        return self.session.exec(
            select(User)
            .where(User.email == email.lower().strip(), User.is_deleted == False)
        ).first()

    def get_by_orcid_id(self, orcid_id: str) -> Optional[User]:
        """Obtém usuário por ORCID ID (apenas ativos)."""
        return self.session.exec(
            select(User)
            .where(User.orcid_id == orcid_id, User.is_deleted == False)
        ).first()

    def set_orcid_tokens(
        self,
        user_id: str,
        orcid_id: str,
        access_token: str,
        refresh_token: Optional[str] = None,
    ) -> None:
        """
        Armazena com segurança os tokens OAuth do ORCID.
        """
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado")

        user.orcid_id = orcid_id
        user.orcid_access_token = access_token
        if refresh_token:
            user.orcid_refresh_token = refresh_token

        user.update_timestamp()
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
