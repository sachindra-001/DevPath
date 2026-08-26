"""Users router (DESIGN.md §21, §22.1)."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.user import UserPreferencesUpdate, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile and preferences",
)
def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserResponse:
    return UserResponse.model_validate(current_user)


@router.patch(
    "/me/preferences",
    response_model=UserResponse,
    summary="Update light personalization preferences (experience, weekly hours, interests)",
)
def update_preferences(
    req: UserPreferencesUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserResponse:
    auth_service = AuthService(db)
    updated_user = auth_service.update_preferences(current_user, req)
    return UserResponse.model_validate(updated_user)
