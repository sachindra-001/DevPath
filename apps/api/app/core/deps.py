"""FastAPI dependency injection providers and authentication guards (DESIGN.md §23)."""

import uuid
from typing import Annotated

import jwt
from fastapi import Cookie, Depends, Header, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.db import get_db
from app.core.security import decode_access_token
from app.models.enums import UserRole
from app.models.user import User

ACCESS_COOKIE_NAME = "cpgs_access_token"
REFRESH_COOKIE_NAME = "cpgs_refresh_token"


def set_auth_cookies(
    response: Response,
    access_token: str,
    refresh_token: str | None = None,
) -> None:
    """Set HttpOnly SameSite=Lax auth cookies."""
    settings = get_settings()

    response.set_cookie(
        key=ACCESS_COOKIE_NAME,
        value=access_token,
        max_age=settings.access_token_expire_minutes * 60,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite.lower(),  # type: ignore[arg-type]
        path="/",
    )

    if refresh_token is not None:
        response.set_cookie(
            key=REFRESH_COOKIE_NAME,
            value=refresh_token,
            max_age=settings.refresh_token_expire_days * 86400,
            httponly=True,
            secure=settings.cookie_secure,
            samesite=settings.cookie_samesite.lower(),  # type: ignore[arg-type]
            path="/api/v1/auth",
        )


def clear_auth_cookies(response: Response) -> None:
    """Clear access and refresh cookies on logout."""
    response.delete_cookie(key=ACCESS_COOKIE_NAME, path="/")
    response.delete_cookie(key=REFRESH_COOKIE_NAME, path="/api/v1/auth")


def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    cpgs_access_token: Annotated[str | None, Cookie()] = None,
    authorization: Annotated[str | None, Header()] = None,
) -> User:
    """Extract and validate the current authenticated user from cookie or Bearer header."""
    token: str | None = None

    if cpgs_access_token:
        token = cpgs_access_token
    elif authorization and authorization.startswith("Bearer "):
        token = authorization.removeprefix("Bearer ").strip()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "unauthorized", "message": "Authentication token missing or expired."},
        )

    try:
        payload = decode_access_token(token)
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": "unauthorized", "message": "Invalid token subject."},
            )
        user_id = uuid.UUID(user_id_str)
    except (jwt.PyJWTError, ValueError) as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "unauthorized", "message": f"Token validation error: {err}"},
        ) from err

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "unauthorized", "message": "User not found."},
        )

    return user


def require_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Require that the authenticated user has the admin role."""
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "forbidden", "message": "Admin privileges required."},
        )
    return current_user
