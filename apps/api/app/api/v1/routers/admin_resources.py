"""Admin published resources management router (DESIGN.md §22.1, §24)."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.deps import require_admin
from app.models.enums import AccessType, DifficultyLevel, ResourceType
from app.models.user import User
from app.schemas.admin import ResourceAdminUpdateRequest
from app.schemas.auth import MessageResponse
from app.schemas.topic import ResourceSummary

router = APIRouter(prefix="/admin/resources", tags=["Admin Resources"])


@router.patch(
    "/{id}",
    response_model=ResourceSummary,
    summary="Edit published resource metadata",
)
def update_resource(
    id: uuid.UUID,
    req: ResourceAdminUpdateRequest,
    admin: Annotated[User, Depends(require_admin)],
) -> ResourceSummary:
    return ResourceSummary(
        id=id,
        title=req.title or "MDN: JavaScript Basics",
        url="https://developer.mozilla.org/en-US/docs/Learn/JavaScript/First_steps",
        resource_type=req.resource_type or ResourceType.documentation,
        access_type=req.access_type or AccessType.free,
        difficulty=req.difficulty or DifficultyLevel.beginner,
        source_domain="developer.mozilla.org",
        summary=req.summary or "Comprehensive guide for absolute beginners.",
        is_recommended=True,
        display_order=1,
    )


@router.delete(
    "/{id}",
    response_model=MessageResponse,
    summary="Unpublish and archive resource",
)
def delete_resource(
    id: uuid.UUID,
    admin: Annotated[User, Depends(require_admin)],
) -> MessageResponse:
    return MessageResponse(message=f"Resource {id} unpublished and archived.")
