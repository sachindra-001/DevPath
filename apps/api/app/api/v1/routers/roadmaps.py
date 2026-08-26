"""Roadmaps public catalog router (DESIGN.md §20, §22.1)."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.deps import get_optional_current_user
from app.models.user import User
from app.schemas.roadmap import RoadmapDetail, RoadmapSummary
from app.services.roadmap_service import RoadmapService

router = APIRouter(prefix="/roadmaps", tags=["Roadmaps"])


@router.get("", response_model=list[RoadmapSummary], summary="List published roadmaps")
def list_roadmaps(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User | None, Depends(get_optional_current_user)] = None,
) -> list[RoadmapSummary]:
    service = RoadmapService(db)
    return service.list_roadmaps(user=current_user)


@router.get("/{slug}", response_model=RoadmapDetail, summary="Get full roadmap structure by slug")
def get_roadmap(
    slug: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User | None, Depends(get_optional_current_user)] = None,
) -> RoadmapDetail:
    service = RoadmapService(db)
    roadmap = service.get_roadmap_by_slug(slug, user=current_user)
    if not roadmap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "not_found", "message": f"Roadmap '{slug}' not found."},
        )
    return roadmap
