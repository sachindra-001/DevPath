"""Roadmap database repository (DESIGN.md §20, §22.1)."""

import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.roadmap import Roadmap, RoadmapSection, RoadmapTopic, TopicDependency


class RoadmapRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_roadmaps(self, include_drafts: bool = False) -> list[Roadmap]:
        """List all roadmaps (optionally filtering drafts)."""
        stmt = select(Roadmap).order_by(Roadmap.title)
        if not include_drafts:
            stmt = stmt.where(Roadmap.is_published.is_(True))
        return list(self.session.execute(stmt).scalars().all())

    def get_by_slug(self, slug: str, include_drafts: bool = False) -> Roadmap | None:
        """Fetch full roadmap tree by slug with sections and topics eagerly loaded."""
        stmt = (
            select(Roadmap)
            .where(Roadmap.slug == slug)
            .options(
                selectinload(Roadmap.sections).selectinload(RoadmapSection.topics).selectinload(RoadmapTopic.dependencies)
            )
        )
        if not include_drafts:
            stmt = stmt.where(Roadmap.is_published.is_(True))
        return self.session.execute(stmt).scalar_one_or_none()

    def get_by_id(self, roadmap_id: uuid.UUID) -> Roadmap | None:
        """Fetch a roadmap by UUID."""
        return self.session.get(Roadmap, roadmap_id)
