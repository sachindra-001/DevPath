"""Topic database repository (DESIGN.md §12, §22.2)."""

import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.resource import Resource, TopicResource
from app.models.roadmap import Roadmap, RoadmapSection, RoadmapTopic, TopicDependency


class TopicRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, topic_id: uuid.UUID) -> RoadmapTopic | None:
        """Fetch topic by UUID with dependencies and section."""
        stmt = (
            select(RoadmapTopic)
            .where(RoadmapTopic.id == topic_id)
            .options(
                selectinload(RoadmapTopic.section),
                selectinload(RoadmapTopic.dependencies),
            )
        )
        return self.session.execute(stmt).scalar_one_or_none()

    def get_by_slugs(self, roadmap_slug: str, topic_slug: str) -> RoadmapTopic | None:
        """Fetch topic by roadmap slug and topic slug."""
        stmt = (
            select(RoadmapTopic)
            .join(Roadmap, Roadmap.id == RoadmapTopic.roadmap_id)
            .where(Roadmap.slug == roadmap_slug, RoadmapTopic.slug == topic_slug)
            .options(
                selectinload(RoadmapTopic.section),
                selectinload(RoadmapTopic.dependencies),
            )
        )
        return self.session.execute(stmt).scalar_one_or_none()

    def get_prerequisite_slugs(self, topic_id: uuid.UUID) -> list[str]:
        """Fetch list of prerequisite topic slugs for a topic."""
        stmt = (
            select(RoadmapTopic.slug)
            .join(TopicDependency, TopicDependency.depends_on_topic_id == RoadmapTopic.id)
            .where(TopicDependency.topic_id == topic_id)
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_resources_for_topic(self, topic_id: uuid.UUID) -> list[tuple[TopicResource, Resource]]:
        """Fetch published curated resources for a topic ordered by display_order."""
        stmt = (
            select(TopicResource, Resource)
            .join(Resource, Resource.id == TopicResource.resource_id)
            .where(TopicResource.topic_id == topic_id)
            .order_by(TopicResource.display_order.asc())
        )
        return list(self.session.execute(stmt).all())
