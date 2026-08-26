"""users table (FR-01..04, DESIGN.md §12.2)."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, CITEXT, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import ExperienceLevel, UserRole, pg_enum

if TYPE_CHECKING:
    from app.models.progress import UserProgress


class User(TimestampMixin, Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("weekly_hours BETWEEN 0 AND 80", name="ck_users_weekly_hours"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(CITEXT(), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        pg_enum(UserRole, "user_role"), default=UserRole.user, nullable=False
    )

    # Light personalization inputs (§21)
    experience_level: Mapped[ExperienceLevel | None] = mapped_column(
        pg_enum(ExperienceLevel, "experience_level"), nullable=True
    )
    interests: Mapped[list[str]] = mapped_column(ARRAY(Text), default=list, nullable=False)
    weekly_hours: Mapped[int | None] = mapped_column(Integer, nullable=True)
    target_role: Mapped[str | None] = mapped_column(String(120), nullable=True)

    # Single active refresh session: opaque rotating token, stored hashed (§23.2)
    refresh_token_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)

    progress_items: Mapped[list["UserProgress"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
