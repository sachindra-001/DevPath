"""Topic service layer (DESIGN.md §12, §22.2)."""

import uuid
from sqlalchemy.orm import Session

from app.models.roadmap import Roadmap
from app.models.user import User
from app.repositories.topic_repo import TopicRepository
from app.schemas.topic import ResourceSummary, TopicDetail


class TopicService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = TopicRepository(db)

    def get_topic_by_id(self, topic_id: uuid.UUID, user: User | None = None) -> TopicDetail | None:
        """Fetch topic detail with prerequisites and resources."""
        topic = self.repo.get_by_id(topic_id)
        if not topic:
            return None

        # Fetch roadmap slug
        roadmap = self.db.get(Roadmap, topic.roadmap_id)
        roadmap_slug = roadmap.slug if roadmap else ""

        prereq_slugs = self.repo.get_prerequisite_slugs(topic.id)
        topic_resources = self.repo.get_resources_for_topic(topic.id)

        resources_out: list[ResourceSummary] = []
        for tr, res in topic_resources:
            resources_out.append(
                ResourceSummary(
                    id=res.id,
                    title=res.title,
                    url=res.url,
                    resource_type=res.resource_type,
                    access_type=res.access_type,
                    difficulty=res.difficulty or topic.difficulty,
                    source_domain=res.source_domain or "",
                    summary=res.description,
                    is_recommended=tr.is_recommended,
                    display_order=tr.display_order,
                )
            )

        return TopicDetail(
            id=topic.id,
            roadmap_slug=roadmap_slug,
            section_id=topic.section_id or uuid.UUID(int=0),
            slug=topic.slug,
            title=topic.title,
            description=topic.description,
            difficulty=topic.difficulty,
            estimated_hours=topic.estimated_hours or 4,
            learning_objectives=topic.learning_objectives or [],
            prerequisites=prereq_slugs,
            resources=resources_out,
            status=None,
            is_suggested_next=False,
        )

    def get_topic_by_slugs(
        self, roadmap_slug: str, topic_slug: str, user: User | None = None
    ) -> TopicDetail | None:
        """Fetch topic detail by roadmap slug and topic slug."""
        topic = self.repo.get_by_slugs(roadmap_slug, topic_slug)
        if not topic:
            return None
        return self.get_topic_by_id(topic.id, user=user)
