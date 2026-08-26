"""Import all models so Base.metadata is complete for Alembic."""

from app.models.base import Base
from app.models.candidate import ResourceCandidate, SearchRun
from app.models.progress import UserProgress
from app.models.resource import Resource, TopicResource
from app.models.roadmap import Roadmap, RoadmapSection, RoadmapTopic, TopicDependency
from app.models.user import User

__all__ = [
    "Base",
    "ResourceCandidate",
    "Resource",
    "Roadmap",
    "RoadmapSection",
    "RoadmapTopic",
    "SearchRun",
    "TopicDependency",
    "TopicResource",
    "User",
    "UserProgress",
]
