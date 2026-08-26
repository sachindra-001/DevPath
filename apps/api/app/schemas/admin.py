"""Admin search runs and candidate review schemas (DESIGN.md §13, §22.2, §24)."""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.models.enums import (
    AccessType,
    CandidateFinalStatus,
    DifficultyLevel,
    ResourceType,
    SearchRunStatus,
)


class SearchRunCreateRequest(BaseModel):
    topic_id: uuid.UUID


class SearchRunSummary(BaseModel):
    id: uuid.UUID
    topic_id: uuid.UUID
    status: SearchRunStatus
    current_stage: str = "queued"
    queries_used: list[str] = Field(default_factory=list)
    candidates_found: int = 0
    candidates_evaluated: int = 0
    candidates_recommended: int = 0
    candidates_pending: int = 0
    total_tokens_used: int = 0
    estimated_cost_usd: float = 0.0
    created_at: datetime
    finished_at: datetime | None = None


class SearchRunCreateResponse(BaseModel):
    run_id: uuid.UUID
    status: SearchRunStatus
    poll: str


class CandidateEvaluationPayload(BaseModel):
    relevance_score: float = 0.95
    quality_score: float = 0.90
    authority_signals: float = 0.95
    freshness_score: float | None = 0.90
    difficulty: DifficultyLevel = DifficultyLevel.intermediate
    resource_type: ResourceType = ResourceType.documentation
    access_type: AccessType = AccessType.free
    topics_covered: list[str] = Field(default_factory=list)
    missing_topics: list[str] = Field(default_factory=list)
    summary: str = "Clear and comprehensive tutorial with interactive examples."
    flags: list[str] = Field(default_factory=list)


class CandidateSummary(BaseModel):
    id: uuid.UUID
    search_run_id: uuid.UUID
    topic_id: uuid.UUID
    url: str
    source_domain: str
    title: str | None = None
    status: CandidateFinalStatus
    overall_score: float | None = None
    rank_position: int | None = None
    evaluation_payload: dict[str, Any] | None = None
    created_at: datetime


class CandidateApproveRequest(BaseModel):
    display_order: int | None = None
    metadata_edits: dict[str, Any] | None = None


class CandidateRejectRequest(BaseModel):
    reason: str | None = None


class CandidateUpdateRequest(BaseModel):
    title: str | None = None
    difficulty: DifficultyLevel | None = None
    resource_type: ResourceType | None = None
    access_type: AccessType | None = None
    summary: str | None = None
    reassign_topic_id: uuid.UUID | None = None


class ResourceAdminUpdateRequest(BaseModel):
    title: str | None = None
    difficulty: DifficultyLevel | None = None
    resource_type: ResourceType | None = None
    access_type: AccessType | None = None
    summary: str | None = None
    is_active: bool | None = None
