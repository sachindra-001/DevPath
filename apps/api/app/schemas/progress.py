"""User progress tracking schemas (DESIGN.md §21, §22.2)."""

import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.enums import ProgressStatus


class ProgressItem(BaseModel):
    topic_id: uuid.UUID
    status: ProgressStatus
    completed_at: datetime | None = None
    updated_at: datetime


class ProgressUpsertRequest(BaseModel):
    topic_id: uuid.UUID
    status: ProgressStatus


class ProgressUpsertResponse(BaseModel):
    progress: ProgressItem
    roadmap_pct: float
    section_pct: float
