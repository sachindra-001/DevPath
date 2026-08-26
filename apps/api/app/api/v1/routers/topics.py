"""Topics and resources public router (DESIGN.md §22.1, §22.2)."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.deps import get_optional_current_user
from app.models.user import User
from app.schemas.topic import TopicDetail
from app.services.topic_service import TopicService

router = APIRouter(prefix="/topics", tags=["Topics"])


@router.get("/{id}", response_model=TopicDetail, summary="Get topic detail with ordered resources")
def get_topic(
    id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User | None, Depends(get_optional_current_user)] = None,
) -> TopicDetail:
    service = TopicService(db)
    topic = service.get_topic_by_id(id, user=current_user)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "not_found", "message": f"Topic '{id}' not found."},
        )
    return topic


@router.get("/by-slug/{roadmap_slug}/{topic_slug}", response_model=TopicDetail, summary="Get topic detail by slugs")
def get_topic_by_slug(
    roadmap_slug: str,
    topic_slug: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User | None, Depends(get_optional_current_user)] = None,
) -> TopicDetail:
    service = TopicService(db)
    topic = service.get_topic_by_slugs(roadmap_slug, topic_slug, user=current_user)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "not_found", "message": f"Topic '{topic_slug}' in roadmap '{roadmap_slug}' not found."},
        )
    return topic
