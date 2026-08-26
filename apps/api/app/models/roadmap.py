"""Roadmap catalog tables: roadmaps, sections, topics, prerequisite links (AD-8, §12)."""

import uuid

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import DifficultyLevel, pg_enum

difficulty = pg_enum(DifficultyLevel, "difficulty_level")


class Roadmap(TimestampMixin, Base):
    __tablename__ = "roadmaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    difficulty: Mapped[DifficultyLevel | None] = mapped_column(difficulty, nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    seed_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    sections: Mapped[list["RoadmapSection"]] = relationship(
        back_populates="roadmap",
        cascade="all, delete-orphan",
        order_by="RoadmapSection.order_index",
    )


class RoadmapSection(Base):
    __tablename__ = "roadmap_sections"
    __table_args__ = (Index("ix_sections_roadmap_order", "roadmap_id", "order_index"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    roadmap_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("roadmaps.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)

    roadmap: Mapped[Roadmap] = relationship(back_populates="sections")
    topics: Mapped[list["RoadmapTopic"]] = relationship(
        back_populates="section", order_by="RoadmapTopic.order_index"
    )


class RoadmapTopic(Base):
    __tablename__ = "roadmap_topics"
    __table_args__ = (
        UniqueConstraint("roadmap_id", "slug", name="uq_topics_roadmap_slug"),
        Index("ix_topics_roadmap", "roadmap_id"),
        Index("ix_topics_section", "section_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    roadmap_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("roadmaps.id", ondelete="CASCADE"), nullable=False
    )
    section_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("roadmap_sections.id", ondelete="SET NULL"), nullable=True
    )
    parent_topic_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("roadmap_topics.id", ondelete="CASCADE"), nullable=True
    )
    slug: Mapped[str] = mapped_column(String(120), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    difficulty: Mapped[DifficultyLevel | None] = mapped_column(difficulty, nullable=True)
    estimated_hours: Mapped[int | None] = mapped_column(Integer, nullable=True)
    learning_objectives: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    section: Mapped[RoadmapSection | None] = relationship(back_populates="topics")
    dependencies: Mapped[list["TopicDependency"]] = relationship(
        foreign_keys="TopicDependency.topic_id", cascade="all, delete-orphan"
    )
    dependents: Mapped[list["TopicDependency"]] = relationship(
        foreign_keys="TopicDependency.depends_on_topic_id", cascade="all, delete-orphan"
    )


class TopicDependency(Base):
    """Prerequisite edge: learn depends_on_topic before topic (§12.2)."""

    __tablename__ = "topic_dependencies"
    __table_args__ = (CheckConstraint("topic_id <> depends_on_topic_id", name="ck_dep_no_self"),)

    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roadmap_topics.id", ondelete="CASCADE"),
        primary_key=True,
    )
    depends_on_topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roadmap_topics.id", ondelete="CASCADE"),
        primary_key=True,
    )
