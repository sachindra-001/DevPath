"""Roadmap schemas for API contracts (DESIGN.md §20, §22)."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import DifficultyLevel


class TopicSummary(BaseModel):
    id: uuid.UUID
    slug: str
    title: str
    difficulty: DifficultyLevel
    estimated_hours: int = 4
    order_index: int = 0
    depends_on: list[str] = Field(default_factory=list)


class SectionSummary(BaseModel):
    id: uuid.UUID
    title: str
    order_index: int
    topics: list[TopicSummary] = Field(default_factory=list)


class RoadmapSummary(BaseModel):
    id: uuid.UUID
    slug: str
    title: str
    description: str | None = None
    difficulty: DifficultyLevel
    is_published: bool = True
    seed_version: int = 1
    created_at: datetime
    updated_at: datetime


class RoadmapDetail(RoadmapSummary):
    sections: list[SectionSummary] = Field(default_factory=list)
