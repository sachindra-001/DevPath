"""Roadmaps public catalog router (DESIGN.md §20, §22.1)."""

import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, status

from app.models.enums import DifficultyLevel
from app.schemas.roadmap import RoadmapDetail, RoadmapSummary, SectionSummary, TopicSummary

router = APIRouter(prefix="/roadmaps", tags=["Roadmaps"])

MOCK_FRONTEND_ROADMAP_ID = uuid.UUID("11111111-1111-1111-1111-111111111111")
MOCK_DATA_ANALYST_ROADMAP_ID = uuid.UUID("22222222-2222-2222-2222-222222222222")

MOCK_ROADMAPS = [
    RoadmapSummary(
        id=MOCK_FRONTEND_ROADMAP_ID,
        slug="frontend-developer",
        title="Frontend Developer",
        description="Step by step guide to becoming a modern frontend developer in 2026.",
        difficulty=DifficultyLevel.beginner,
        is_published=True,
        seed_version=1,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    ),
    RoadmapSummary(
        id=MOCK_DATA_ANALYST_ROADMAP_ID,
        slug="data-analyst",
        title="Data Analyst",
        description="Master SQL, Python, data visualization, and analytical thinking.",
        difficulty=DifficultyLevel.beginner,
        is_published=True,
        seed_version=1,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    ),
]


@router.get("", response_model=list[RoadmapSummary], summary="List published roadmaps")
def list_roadmaps() -> list[RoadmapSummary]:
    return MOCK_ROADMAPS


@router.get("/{slug}", response_model=RoadmapDetail, summary="Get full roadmap structure by slug")
def get_roadmap(slug: str) -> RoadmapDetail:
    matched = next((r for r in MOCK_ROADMAPS if r.slug == slug), None)
    if not matched:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "not_found", "message": f"Roadmap '{slug}' not found."},
        )

    sec_id = uuid.uuid4()
    mock_sections = [
        SectionSummary(
            id=sec_id,
            title="Foundations & Internet",
            order_index=1,
            topics=[
                TopicSummary(
                    id=uuid.UUID("33333333-3333-3333-3333-333333333333"),
                    slug="how-the-internet-works",
                    title="How the Internet Works",
                    difficulty=DifficultyLevel.beginner,
                    estimated_hours=4,
                    order_index=1,
                    depends_on=[],
                ),
                TopicSummary(
                    id=uuid.UUID("44444444-4444-4444-4444-444444444444"),
                    slug="html-basics",
                    title="HTML Basics",
                    difficulty=DifficultyLevel.beginner,
                    estimated_hours=6,
                    order_index=2,
                    depends_on=["how-the-internet-works"],
                ),
            ],
        )
    ]

    return RoadmapDetail(
        id=matched.id,
        slug=matched.slug,
        title=matched.title,
        description=matched.description,
        difficulty=matched.difficulty,
        is_published=matched.is_published,
        seed_version=matched.seed_version,
        created_at=matched.created_at,
        updated_at=matched.updated_at,
        sections=mock_sections,
    )
