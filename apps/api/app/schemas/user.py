"""User request and response schemas (DESIGN.md §21, §23)."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.enums import ExperienceLevel, UserRole


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr
    name: str
    role: UserRole
    experience_level: ExperienceLevel | None = None
    interests: list[str] = Field(default_factory=list)
    weekly_hours: int | None = None
    target_role: str | None = None
    created_at: datetime


class UserPreferencesUpdate(BaseModel):
    experience_level: ExperienceLevel | None = None
    interests: list[str] | None = None
    weekly_hours: int | None = Field(default=None, ge=0, le=80)
    target_role: str | None = None
