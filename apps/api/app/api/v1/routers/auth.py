"""Authentication router (DESIGN.md §22.1, §23)."""

from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.deps import clear_auth_cookies, get_current_user, get_db, set_auth_cookies
from app.models.user import User
from app.schemas.auth import (
    AuthTokenResponse,
    MessageResponse,
    UserLoginRequest,
    UserRegisterRequest,
)
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=AuthTokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new learner account",
)
def register(
    req: UserRegisterRequest,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
) -> AuthTokenResponse:
    auth_service = AuthService(db)
    user, access_token, refresh_token = auth_service.register(req)
    set_auth_cookies(response, access_token, refresh_token)
    return AuthTokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user),
    )


@router.post(
    "/login",
    response_model=AuthTokenResponse,
    summary="Authenticate and issue JWT session cookies",
)
def login(
    req: UserLoginRequest,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
) -> AuthTokenResponse:
    auth_service = AuthService(db)
    user, access_token, refresh_token = auth_service.login(req)
    set_auth_cookies(response, access_token, refresh_token)
    return AuthTokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user),
    )


@router.post(
    "/refresh",
    response_model=AuthTokenResponse,
    summary="Rotate refresh token and issue fresh access cookie",
)
def refresh(
    response: Response,
    db: Annotated[Session, Depends(get_db)],
    cpgs_refresh_token: Annotated[str | None, Cookie()] = None,
) -> AuthTokenResponse:
    auth_service = AuthService(db)
    user, access_token, new_refresh_token = auth_service.refresh(cpgs_refresh_token)
    set_auth_cookies(response, access_token, new_refresh_token)
    return AuthTokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user),
    )


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Invalidate current session and clear cookies",
)
def logout(
    response: Response,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> MessageResponse:
    auth_service = AuthService(db)
    auth_service.logout(current_user)
    clear_auth_cookies(response)
    return MessageResponse(message="Successfully logged out.")
