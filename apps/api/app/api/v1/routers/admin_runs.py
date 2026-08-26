"""Admin discovery runs router (DESIGN.md §13, §22.1, §24)."""

import uuid
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.core.deps import require_admin
from app.models.enums import SearchRunStatus
from app.models.user import User
from app.schemas.admin import SearchRunCreateRequest, SearchRunCreateResponse, SearchRunSummary

router = APIRouter(prefix="/admin/search-runs", tags=["Admin Runs"])


@router.post(
    "",
    response_model=SearchRunCreateResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger background AI resource discovery for a topic",
)
def create_search_run(
    req: SearchRunCreateRequest,
    admin: Annotated[User, Depends(require_admin)],
) -> SearchRunCreateResponse:
    run_id = uuid.uuid4()
    return SearchRunCreateResponse(
        run_id=run_id,
        status=SearchRunStatus.queued,
        poll=f"/api/v1/admin/search-runs/{run_id}",
    )


@router.get(
    "",
    response_model=list[SearchRunSummary],
    summary="List discovery runs with optional filtering",
)
def list_search_runs(
    admin: Annotated[User, Depends(require_admin)],
    topic_id: Annotated[uuid.UUID | None, Query()] = None,
    limit: int = 20,
    offset: int = 0,
) -> list[SearchRunSummary]:
    now = datetime.now(UTC)
    mock_run = SearchRunSummary(
        id=uuid.UUID("88888888-8888-8888-8888-888888888888"),
        topic_id=topic_id or uuid.UUID("33333333-3333-3333-3333-333333333333"),
        status=SearchRunStatus.completed,
        current_stage="completed",
        queries_used=[
            "how the internet works tutorial beginners",
            "client server model explained mdn",
            "dns resolution step by step guide",
        ],
        candidates_found=24,
        candidates_evaluated=16,
        candidates_recommended=6,
        candidates_pending=4,
        total_tokens_used=18400,
        estimated_cost_usd=0.012,
        created_at=now,
        finished_at=now,
    )
    return [mock_run]


@router.get(
    "/{id}",
    response_model=SearchRunSummary,
    summary="Get discovery run status and telemetry",
)
def get_search_run(
    id: uuid.UUID,
    admin: Annotated[User, Depends(require_admin)],
) -> SearchRunSummary:
    now = datetime.now(UTC)
    return SearchRunSummary(
        id=id,
        topic_id=uuid.UUID("33333333-3333-3333-3333-333333333333"),
        status=SearchRunStatus.running,
        current_stage="evaluating",
        queries_used=[
            "how the internet works tutorial beginners",
            "client server model explained mdn",
        ],
        candidates_found=18,
        candidates_evaluated=10,
        candidates_recommended=4,
        candidates_pending=2,
        total_tokens_used=12500,
        estimated_cost_usd=0.008,
        created_at=now,
        finished_at=None,
    )
