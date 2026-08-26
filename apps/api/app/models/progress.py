"""user_progress table (FR-15..18, §12.2)."""

import datetime as dt
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import ProgressStatus, pg_enum

if TYPE_CHECKING:
    from app.models.user import User


class UserProgress(TimestampMixin, Base):
    __tablename__ = "user_progress"
    __table_args__ = (UniqueConstraint("user_id", "topic_id", name="uq_progress_user_topic"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("roadmap_topics.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[ProgressStatus] = mapped_column(
        pg_enum(ProgressStatus, "progress_status"),
        default=ProgressStatus.not_started,
        nullable=False,
    )
    completed_at: Mapped[dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship(back_populates="progress_items")
