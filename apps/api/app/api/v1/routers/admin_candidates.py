"""Admin candidates review queue router (DESIGN.md §19, §22.1, §24)."""

import uuid
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.core.deps import require_admin
from app.models.enums import CandidateFinalStatus
from app.models.user import User
from app.schemas.admin import (
    CandidateApproveRequest,
    CandidateRejectRequest,
    CandidateSummary,
    CandidateUpdateRequest,
)
from app.schemas.auth import MessageResponse
from app.schemas.topic import ResourceSummary

router = APIRouter(prefix="/admin/candidates", tags=["Admin Candidates"])


def _create_mock_candidate(
    cand_id: uuid.UUID,
    title: str,
    url: str,
    domain: str,
    score: float,
    status: CandidateFinalStatus = CandidateFinalStatus.pending_review,
) -> CandidateSummary:
    return CandidateSummary(
        id=cand_id,
        search_run_id=uuid.UUID("88888888-8888-8888-8888-888888888888"),
        topic_id=uuid.UUID("33333333-3333-3333-3333-333333333333"),
        url=url,
        source_domain=domain,
        title=title,
        status=status,
        overall_score=score,
        rank_position=1,
        evaluation_payload={
            "relevance_score": 0.96,
            "quality_score": 0.94,
            "authority_signals": 0.96,
            "freshness_score": 0.90,
            "difficulty": "beginner",
            "resource_type": "documentation",
            "access_type": "free",
            "topics_covered": ["Client-server model", "DNS resolution", "HTTP request flow"],
            "missing_topics": [],
            "summary": "Canonical MDN introduction with clear architectural diagrams.",
            "recommended": True,
            "flags": [],
        },
        created_at=datetime.now(UTC),
    )


@router.get(
    "",
    response_model=list[CandidateSummary],
    summary="List candidates in the review queue",
)
def list_candidates(
    admin: Annotated[User, Depends(require_admin)],
    run_id: Annotated[uuid.UUID | None, Query()] = None,
    topic_id: Annotated[uuid.UUID | None, Query()] = None,
    status: Annotated[CandidateFinalStatus | None, Query()] = None,
    min_score: Annotated[float | None, Query()] = None,
) -> list[CandidateSummary]:
    cand1 = _create_mock_candidate(
        uuid.UUID("99999999-9999-9999-9999-999999999991"),
        "MDN — How the Web Works",
        "https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/How_the_Web_works",
        "developer.mozilla.org",
        0.945,
    )
    cand2 = _create_mock_candidate(
        uuid.UUID("99999999-9999-9999-9999-999999999992"),
        "Cloudflare — What is DNS?",
        "https://www.cloudflare.com/learning/dns/what-is-dns/",
        "cloudflare.com",
        0.882,
    )
    return [cand1, cand2]


@router.get(
    "/{id}",
    response_model=CandidateSummary,
    summary="Get full candidate details with evaluation payload",
)
def get_candidate(
    id: uuid.UUID,
    admin: Annotated[User, Depends(require_admin)],
) -> CandidateSummary:
    return _create_mock_candidate(
        id,
        "MDN — How the Web Works",
        "https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/How_the_Web_works",
        "developer.mozilla.org",
        0.945,
    )


@router.post(
    "/{id}/approve",
    response_model=ResourceSummary,
    summary="Approve and publish candidate to topic shelf",
)
def approve_candidate(
    id: uuid.UUID,
    req: CandidateApproveRequest,
    admin: Annotated[User, Depends(require_admin)],
) -> ResourceSummary:
    from app.models.enums import AccessType, DifficultyLevel, ResourceType

    return ResourceSummary(
        id=uuid.uuid4(),
        title="MDN — How the Web Works",
        url="https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/How_the_Web_works",
        resource_type=ResourceType.documentation,
        access_type=AccessType.free,
        difficulty=DifficultyLevel.beginner,
        source_domain="developer.mozilla.org",
        summary="Canonical MDN introduction with clear architectural diagrams.",
        is_recommended=True,
        display_order=req.display_order or 1,
    )


@router.post(
    "/{id}/reject",
    response_model=MessageResponse,
    summary="Reject candidate with reason",
)
def reject_candidate(
    id: uuid.UUID,
    req: CandidateRejectRequest,
    admin: Annotated[User, Depends(require_admin)],
) -> MessageResponse:
    reason_text = req.reason or "No reason provided"
    return MessageResponse(message=f"Candidate {id} rejected. Reason: {reason_text}")


@router.patch(
    "/{id}",
    response_model=CandidateSummary,
    summary="Edit candidate metadata or reassign topic",
)
def update_candidate(
    id: uuid.UUID,
    req: CandidateUpdateRequest,
    admin: Annotated[User, Depends(require_admin)],
) -> CandidateSummary:
    cand = _create_mock_candidate(
        id,
        req.title or "MDN — How the Web Works (Updated)",
        "https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/How_the_Web_works",
        "developer.mozilla.org",
        0.945,
    )
    if req.reassign_topic_id:
        cand.topic_id = req.reassign_topic_id
    return cand
