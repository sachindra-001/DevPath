"""User repository for SQLAlchemy database access (DESIGN.md §11.1)."""

import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import UserRole
from app.models.user import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email.strip().lower())
        return self.session.scalars(stmt).first()

    def create(
        self,
        email: str,
        password_hash: str,
        name: str,
        role: UserRole = UserRole.user,
    ) -> User:
        user = User(
            email=email.strip().lower(),
            password_hash=password_hash,
            name=name.strip(),
            role=role,
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update_refresh_token_hash(self, user: User, token_hash: str | None) -> None:
        user.refresh_token_hash = token_hash
        self.session.commit()

    def update_preferences(self, user: User, update_data: dict[str, Any]) -> User:
        for field, value in update_data.items():
            if hasattr(user, field) and value is not None:
                setattr(user, field, value)
        self.session.commit()
        self.session.refresh(user)
        return user
