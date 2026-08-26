#!/usr/bin/env python
"""Seed the initial platform administrator idempotently (FR-04, DESIGN.md §23, §31)."""

import sys
from pathlib import Path

# Ensure apps/api is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "apps" / "api"))

from app.core.config import get_settings  # noqa: E402
from app.core.db import SessionLocal  # noqa: E402
from app.core.security import hash_password  # noqa: E402
from app.models.enums import UserRole  # noqa: E402
from app.repositories.user_repo import UserRepository  # noqa: E402


def seed_admin() -> None:
    settings = get_settings()
    session = SessionLocal()
    try:
        repo = UserRepository(session)
        existing = repo.get_by_email(settings.admin_email)
        if existing:
            if existing.role != UserRole.admin:
                existing.role = UserRole.admin
                session.commit()
                role_val = UserRole.admin.value
                print(f"[OK] Updated user '{settings.admin_email}' to role '{role_val}'.")
            else:
                print(f"[OK] Admin user '{settings.admin_email}' already exists. No action needed.")
            return

        admin_user = repo.create(
            email=settings.admin_email,
            password_hash=hash_password(settings.admin_password),
            name=settings.admin_name,
            role=UserRole.admin,
        )
        print(f"[OK] Successfully seeded admin user '{admin_user.email}' (ID: {admin_user.id}).")
    finally:
        session.close()


if __name__ == "__main__":
    seed_admin()
