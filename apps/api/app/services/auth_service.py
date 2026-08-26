"""Authentication service managing user registration, login, token rotation,
and sessions (DESIGN.md §23).
"""

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    generate_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
    verify_refresh_token,
)
from app.models.enums import UserRole
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.auth import UserLoginRequest, UserRegisterRequest
from app.schemas.user import UserPreferencesUpdate


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repo = UserRepository(db)

    def register(self, req: UserRegisterRequest) -> tuple[User, str, str]:
        """Register a new user, issue access + refresh tokens."""
        existing = self.user_repo.get_by_email(req.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"code": "already_exists", "message": "Email is already registered."},
            )

        hashed_pw = hash_password(req.password)
        user = self.user_repo.create(
            email=req.email,
            password_hash=hashed_pw,
            name=req.name,
            role=UserRole.user,
        )

        access_token, _ = create_access_token(user.id, user.role.value)
        raw_refresh = generate_refresh_token()
        self.user_repo.update_refresh_token_hash(user, hash_refresh_token(raw_refresh))

        return user, access_token, raw_refresh

    def login(self, req: UserLoginRequest) -> tuple[User, str, str]:
        """Authenticate credentials, rotate refresh token, issue new tokens."""
        user = self.user_repo.get_by_email(req.email)
        if not user or not verify_password(req.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": "unauthorized", "message": "Invalid email or password."},
            )

        access_token, _ = create_access_token(user.id, user.role.value)
        raw_refresh = generate_refresh_token()
        self.user_repo.update_refresh_token_hash(user, hash_refresh_token(raw_refresh))

        return user, access_token, raw_refresh

    def refresh(self, raw_refresh_token: str | None) -> tuple[User, str, str]:
        """Validate single active refresh token, rotate it, and issue new tokens."""
        if not raw_refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": "unauthorized", "message": "Refresh token missing."},
            )

        target_hash = hash_refresh_token(raw_refresh_token)
        stmt = select(User).where(User.refresh_token_hash == target_hash)
        user = self.db.scalars(stmt).first()

        if (
            not user
            or not user.refresh_token_hash
            or not verify_refresh_token(raw_refresh_token, user.refresh_token_hash)
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": "unauthorized", "message": "Invalid or expired refresh token."},
            )

        # Rotate refresh token (single active session per user)
        new_access, _ = create_access_token(user.id, user.role.value)
        new_refresh = generate_refresh_token()
        self.user_repo.update_refresh_token_hash(user, hash_refresh_token(new_refresh))

        return user, new_access, new_refresh

    def logout(self, user: User) -> None:
        """Invalidate user's stored refresh token session."""
        self.user_repo.update_refresh_token_hash(user, None)

    def update_preferences(self, user: User, req: UserPreferencesUpdate) -> User:
        """Update personalization preferences."""
        update_data = req.model_dump(exclude_unset=True)
        return self.user_repo.update_preferences(user, update_data)
