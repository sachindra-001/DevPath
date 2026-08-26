"""Roadmap service layer (DESIGN.md §20, §22.1)."""

from sqlalchemy.orm import Session

from app.models.enums import UserRole
from app.models.roadmap import Roadmap
from app.models.user import User
from app.repositories.roadmap_repo import RoadmapRepository
from app.schemas.roadmap import RoadmapDetail, RoadmapSummary, SectionSummary, TopicSummary


class RoadmapService:
    def __init__(self, db: Session) -> None:
        self.repo = RoadmapRepository(db)

    def list_roadmaps(self, user: User | None = None) -> list[RoadmapSummary]:
        """List roadmaps. Include drafts only if user is an admin."""
        include_drafts = user is not None and user.role == UserRole.admin
        roadmaps = self.repo.list_roadmaps(include_drafts=include_drafts)
        return [
            RoadmapSummary(
                id=r.id,
                slug=r.slug,
                title=r.title,
                description=r.description,
                difficulty=r.difficulty,
                is_published=r.is_published,
                seed_version=r.seed_version,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
            for r in roadmaps
        ]

    def get_roadmap_by_slug(self, slug: str, user: User | None = None) -> RoadmapDetail | None:
        """Retrieve full roadmap tree. Include draft only if user is an admin."""
        include_drafts = user is not None and user.role == UserRole.admin
        roadmap = self.repo.get_by_slug(slug, include_drafts=include_drafts)
        if not roadmap:
            return None

        # Build topic ID to slug map across roadmap for dependency resolution
        all_topics = {}
        for sec in roadmap.sections:
            for top in sec.topics:
                all_topics[top.id] = top.slug

        sections_out: list[SectionSummary] = []
        for sec in sorted(roadmap.sections, key=lambda s: s.order_index):
            topics_out: list[TopicSummary] = []
            for top in sorted(sec.topics, key=lambda t: t.order_index):
                dep_slugs = [
                    all_topics[dep.depends_on_topic_id]
                    for dep in top.dependencies
                    if dep.depends_on_topic_id in all_topics
                ]
                topics_out.append(
                    TopicSummary(
                        id=top.id,
                        slug=top.slug,
                        title=top.title,
                        difficulty=top.difficulty,
                        estimated_hours=top.estimated_hours or 4,
                        order_index=top.order_index,
                        depends_on=dep_slugs,
                    )
                )

            sections_out.append(
                SectionSummary(
                    id=sec.id,
                    title=sec.title,
                    order_index=sec.order_index,
                    topics=topics_out,
                )
            )

        return RoadmapDetail(
            id=roadmap.id,
            slug=roadmap.slug,
            title=roadmap.title,
            description=roadmap.description,
            difficulty=roadmap.difficulty,
            is_published=roadmap.is_published,
            seed_version=roadmap.seed_version,
            created_at=roadmap.created_at,
            updated_at=roadmap.updated_at,
            sections=sections_out,
        )
