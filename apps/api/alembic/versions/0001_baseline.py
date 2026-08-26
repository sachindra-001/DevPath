"""Baseline schema — all §12 tables, enums, indexes.

Revision ID: 0001_baseline
Revises:
Create Date: 2026-08-26

Forward-only policy (§12.3). Built from Base.metadata so models and schema
cannot drift; later migrations use autogenerate against this baseline.
"""

from collections.abc import Sequence

from sqlalchemy import text

from alembic import op
from app.models import Base

revision: str = "0001_baseline"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    # extensions are also created by database/init on first compose boot;
    # re-assert for non-compose environments (managed Postgres)
    bind.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    bind.execute(text("CREATE EXTENSION IF NOT EXISTS citext"))
    bind.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto"))
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    pass
