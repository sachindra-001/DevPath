"""Shared PostgreSQL enum types (DESIGN.md §12.1)."""

import enum

from sqlalchemy import Enum


class UserRole(enum.StrEnum):
    user = "user"
    admin = "admin"


class ExperienceLevel(enum.StrEnum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class DifficultyLevel(enum.StrEnum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class ResourceType(enum.StrEnum):
    article = "article"
    blog = "blog"
    documentation = "documentation"
    video = "video"
    course = "course"
    book = "book"
    repository = "repository"
    tutorial = "tutorial"
    project = "project"
    other = "other"


class AccessType(enum.StrEnum):
    free = "free"
    freemium = "freemium"
    paid = "paid"
    unknown = "unknown"


class DiscoveryMethod(enum.StrEnum):
    ai_pipeline = "ai_pipeline"
    manual = "manual"


class ResourceStatus(enum.StrEnum):
    published = "published"
    archived = "archived"


class ExtractionStatus(enum.StrEnum):
    pending = "pending"
    extracted = "extracted"
    failed = "failed"
    skipped_robots = "skipped_robots"
    skipped_language = "skipped_language"
    too_large = "too_large"


class CandidateFinalStatus(enum.StrEnum):
    new = "new"
    pending_review = "pending_review"
    approved = "approved"
    rejected = "rejected"
    low_score = "low_score"
    duplicate_candidate = "duplicate_candidate"
    duplicate_resource = "duplicate_resource"


class SearchRunStatus(enum.StrEnum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"


class ProgressStatus(enum.StrEnum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"


def pg_enum(enum_cls: type[enum.Enum], name: str) -> Enum:
    return Enum(
        enum_cls, name=name, native_enum=True, values_callable=lambda e: [m.value for m in e]
    )
