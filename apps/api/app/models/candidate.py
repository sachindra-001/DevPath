"""search_runs + resource_candidates — pipeline telemetry and audit (FR-19..27, AD-9)."""

import datetime as dt
import uuid

from sqlalchemy import (
    ARRAY,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import (
    CandidateFinalStatus,
    ExtractionStatus,
    SearchRunStatus,
    pg_enum,
)


class SearchRun(TimestampMixin, Base):
    """One row per discovery execution: status protocol + cost accounting (§11.4)."""

    __tablename__ = "search_runs"
    __table_args__ = (
        # FR-19 at DB level: max 1 active run per topic
        Index(
            "uq_search_runs_topic_active",
            "topic_id",
            unique=True,
            postgresql_where=text("status IN ('queued', 'running')"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("roadmap_topics.id", ondelete="CASCADE"), nullable=False
    )
    requested_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[SearchRunStatus] = mapped_column(
        pg_enum(SearchRunStatus, "search_run_status"),
        default=SearchRunStatus.queued,
        nullable=False,
    )

    queries_generated: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)

    # Live counters polled by the admin UI (§11.4)
    candidates_found: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    evaluated_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    recommended_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    pending_review_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    llm_prompt_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    llm_completion_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    estimated_cost_usd: Mapped[float] = mapped_column(Numeric(8, 4), default=0, nullable=False)

    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    candidates: Mapped[list["ResourceCandidate"]] = relationship(
        back_populates="search_run", cascade="all, delete-orphan"
    )


class ResourceCandidate(TimestampMixin, Base):
    """Every URL the pipeline surfaced + evaluation + review fate in one row (AD-9)."""

    __tablename__ = "resource_candidates"
    __table_args__ = (
        UniqueConstraint("search_run_id", "url_hash", name="uq_candidates_run_urlhash"),
        Index("ix_candidates_topic_status", "topic_id", "final_status"),
        Index("ix_candidates_run", "search_run_id"),
        Index(
            "ix_candidates_pending_score",
            "overall_score",
            postgresql_where=text("final_status = 'pending_review'"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("roadmap_topics.id", ondelete="CASCADE"), nullable=False
    )
    search_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("search_runs.id", ondelete="CASCADE"), nullable=False
    )

    url: Mapped[str] = mapped_column(Text, nullable=False)
    url_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str | None] = mapped_column(String(300), nullable=True)
    source_domain: Mapped[str | None] = mapped_column(String(200), nullable=True)

    extraction_status: Mapped[ExtractionStatus] = mapped_column(
        pg_enum(ExtractionStatus, "extraction_status"),
        default=ExtractionStatus.pending,
        nullable=False,
    )
    content_text: Mapped[str | None] = mapped_column(Text, nullable=True)  # cleaned, truncated
    content_chars: Mapped[int | None] = mapped_column(Integer, nullable=True)

    final_status: Mapped[CandidateFinalStatus] = mapped_column(
        pg_enum(CandidateFinalStatus, "candidate_final_status"),
        default=CandidateFinalStatus.new,
        nullable=False,
    )

    relevance_score: Mapped[float | None] = mapped_column(Numeric(4, 2), nullable=True)
    quality_score: Mapped[float | None] = mapped_column(Numeric(4, 2), nullable=True)
    authority_score: Mapped[float | None] = mapped_column(Numeric(4, 2), nullable=True)
    freshness_score: Mapped[float | None] = mapped_column(Numeric(4, 2), nullable=True)
    overall_score: Mapped[float | None] = mapped_column(Numeric(4, 2), nullable=True)

    evaluation: Mapped[dict] = mapped_column(
        JSONB, default=dict, nullable=False
    )  # full LLM payload
    flags: Mapped[list[str]] = mapped_column(ARRAY(String(50)), default=list, nullable=False)
    duplicate_of_resource_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("resources.id", ondelete="SET NULL"), nullable=True
    )

    # Review audit trail (FR-32) — replaces a separate reviews table
    reviewed_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    review_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewed_at: Mapped[dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    search_run: Mapped[SearchRun] = relationship(back_populates="candidates")
