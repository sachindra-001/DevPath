"""resources + topic_resources tables (FR-10..14, §12.2)."""

import datetime as dt
import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Boolean,
    Date,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin
from app.models.enums import (
    AccessType,
    DifficultyLevel,
    DiscoveryMethod,
    ResourceStatus,
    ResourceType,
    pg_enum,
)

EMBEDDING_DIM = 1536  # text-embedding-3-small (AD-3)


class Resource(TimestampMixin, Base):
    """Canonical approved-resource catalog; deliberately generic (§38)."""

    __tablename__ = "resources"
    __table_args__ = (
        UniqueConstraint("url_hash", name="uq_resources_url_hash"),
        Index("ix_resources_source_domain", "source_domain"),
        Index("ix_resources_status", "status"),
        Index(
            "ix_resources_embedding_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    url_hash: Mapped[str] = mapped_column(String(64), nullable=False)  # sha256 of normalized URL

    # What it is
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    resource_type: Mapped[ResourceType] = mapped_column(
        pg_enum(ResourceType, "resource_type"), nullable=False
    )
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict, nullable=False)

    # Where it came from
    source_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    source_domain: Mapped[str | None] = mapped_column(String(200), nullable=True)
    author: Mapped[str | None] = mapped_column(String(200), nullable=True)
    language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    published_at: Mapped[dt.date | None] = mapped_column(Date, nullable=True)

    # How it got here
    discovery_method: Mapped[DiscoveryMethod] = mapped_column(
        pg_enum(DiscoveryMethod, "discovery_method"), default=DiscoveryMethod.manual, nullable=False
    )
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    status: Mapped[ResourceStatus] = mapped_column(
        pg_enum(ResourceStatus, "resource_status"), default=ResourceStatus.published, nullable=False
    )
    access_type: Mapped[AccessType] = mapped_column(
        pg_enum(AccessType, "access_type"), default=AccessType.unknown, nullable=False
    )
    difficulty: Mapped[DifficultyLevel | None] = mapped_column(
        pg_enum(DifficultyLevel, "difficulty_level"), nullable=True
    )
    quality_score: Mapped[float | None] = mapped_column(Numeric(4, 2), nullable=True)
    embedding = mapped_column(Vector(EMBEDDING_DIM), nullable=True)


class TopicResource(Base):
    """Curated many-to-many placement with ordering (§12.2)."""

    __tablename__ = "topic_resources"
    __table_args__ = (Index("ix_topic_resources_order", "topic_id", "display_order"),)

    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roadmap_topics.id", ondelete="CASCADE"),
        primary_key=True,
    )
    resource_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("resources.id", ondelete="CASCADE"),
        primary_key=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_recommended: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    added_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
