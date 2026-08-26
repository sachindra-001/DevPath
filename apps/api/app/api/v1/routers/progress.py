"""Progress tracking router (DESIGN.md §21, §22.1, §22.2)."""

import uuid
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.core.deps import get_current_user
from app.models.enums import ProgressStatus
from app.models.user import User
from app.schemas.progress import ProgressItem, ProgressUpsertRequest, ProgressUpsertResponse

router = APIRouter(prefix="/progress", tags=["Progress"])


@router.get("", response_model=list[ProgressItem], summary="Get learner progress for a roadmap")
def get_progress(
    roadmap_id: Annotated[uuid.UUID, Query(description="Target roadmap ID")],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[ProgressItem]:
    # Contract stub fixture
    now = datetime.now(UTC)
    return [
        ProgressItem(
            topic_id=uuid.UUID("33333333-3333-3333-3333-333333333333"),
            status=ProgressStatus.completed,
            completed_at=now,
            updated_at=now,
        ),
        ProgressItem(
            topic_id=uuid.UUID("44444444-4444-4444-4444-444444444444"),
            status=ProgressStatus.in_progress,
            completed_at=None,
            updated_at=now,
        ),
    ]


@router.put("", response_model=ProgressUpsertResponse, summary="Upsert topic completion status")
def update_progress(
    req: ProgressUpsertRequest,
    current_user: Annotated[User, Depends(get_current_user)],
) -> ProgressUpsertResponse:
    now = datetime.now(UTC)
    item = ProgressItem(
        topic_id=req.topic_id,
        status=req.status,
        completed_at=now if req.status == ProgressStatus.completed else None,
        updated_at=now,
    )
    return ProgressUpsertResponse(
        progress=item,
        roadmap_pct=33.3,
        section_pct=50.0,
    )
