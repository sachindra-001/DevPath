"""Topics and resources public router (DESIGN.md §22.1, §22.2)."""

import uuid

from fastapi import APIRouter

from app.models.enums import AccessType, DifficultyLevel, ProgressStatus, ResourceType
from app.schemas.topic import ResourceSummary, TopicDetail

router = APIRouter(prefix="/topics", tags=["Topics"])


@router.get("/{id}", response_model=TopicDetail, summary="Get topic detail with ordered resources")
def get_topic(id: uuid.UUID) -> TopicDetail:
    mock_resources = [
        ResourceSummary(
            id=uuid.UUID("55555555-5555-5555-5555-555555555555"),
            title="MDN: How the Web works",
            url="https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/How_the_Web_works",
            resource_type=ResourceType.documentation,
            access_type=AccessType.free,
            difficulty=DifficultyLevel.beginner,
            source_domain="developer.mozilla.org",
            summary="Canonical overview covering clients, servers, DNS, HTTP, and page rendering.",
            is_recommended=True,
            display_order=1,
        ),
        ResourceSummary(
            id=uuid.UUID("66666666-6666-6666-6666-666666666666"),
            title="CS50: Internet Basics and DNS",
            url="https://www.youtube.com/watch?v=mock_video_id",
            resource_type=ResourceType.video,
            access_type=AccessType.free,
            difficulty=DifficultyLevel.beginner,
            source_domain="youtube.com",
            summary="Engaging video walkthrough of network protocols and request lifecycle.",
            is_recommended=True,
            display_order=2,
        ),
    ]

    return TopicDetail(
        id=id,
        roadmap_slug="frontend-developer",
        section_id=uuid.UUID("77777777-7777-7777-7777-777777777777"),
        slug="how-the-internet-works",
        title="How the Internet Works",
        description="Understand the fundamental infrastructure connecting computers globally.",
        difficulty=DifficultyLevel.beginner,
        estimated_hours=4,
        learning_objectives=[
            "Explain the client-server architecture",
            "Understand DNS lookup flow",
            "Describe TCP/IP packet transmission basics",
            "Differentiate HTTP vs HTTPS",
        ],
        prerequisites=[],
        resources=mock_resources,
        status=ProgressStatus.in_progress,
        is_suggested_next=True,
    )
