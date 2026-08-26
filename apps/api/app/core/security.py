"""Security primitives: Argon2id password hashing, JWT access tokens,
and refresh token helpers (DESIGN.md §23).
"""

import hashlib
import secrets
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from passlib.context import CryptContext

from app.core.config import get_settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plaintext password with Argon2id."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against an Argon2id hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: str | uuid.UUID,
    role: str,
    expires_delta: timedelta | None = None,
) -> tuple[str, str]:
    """Create a signed JWT access token with {sub, role, jti} claims.

    Returns:
        (token_str, jti)
    """
    settings = get_settings()
    now = datetime.now(UTC)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.access_token_expire_minutes)

    jti = str(uuid.uuid4())
    payload: dict[str, Any] = {
        "sub": str(subject),
        "role": str(role),
        "jti": jti,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    encoded = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return encoded, jti


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT access token."""
    settings = get_settings()
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])


def generate_refresh_token() -> str:
    """Generate an opaque cryptographically secure refresh token string."""
    return secrets.token_urlsafe(64)


def hash_refresh_token(refresh_token: str) -> str:
    """Hash an opaque refresh token using SHA-256 for persistent database storage."""
    return hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()


def verify_refresh_token(refresh_token: str, stored_hash: str) -> bool:
    """Verify an opaque refresh token against a stored SHA-256 hash."""
    computed_hash = hash_refresh_token(refresh_token)
    return secrets.compare_digest(computed_hash, stored_hash)
