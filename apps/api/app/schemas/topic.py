"""Topic and Resource schemas (DESIGN.md §12, §22.2)."""

import uuid

from pydantic import BaseModel, Field

from app.models.enums import AccessType, DifficultyLevel, ProgressStatus, ResourceType


class ResourceSummary(BaseModel):
    id: uuid.UUID
    title: str
    url: str
    resource_type: ResourceType
    access_type: AccessType
    difficulty: DifficultyLevel
    source_domain: str
    summary: str | None = None
    is_recommended: bool = True
    display_order: int = 0


class TopicDetail(BaseModel):
    id: uuid.UUID
    roadmap_slug: str
    section_id: uuid.UUID
    slug: str
    title: str
    description: str | None = None
    difficulty: DifficultyLevel
    estimated_hours: int = 4
    learning_objectives: list[str] = Field(default_factory=list)
    prerequisites: list[str] = Field(default_factory=list)
    resources: list[ResourceSummary] = Field(default_factory=list)
    status: ProgressStatus | None = None
    is_suggested_next: bool = False
