from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.db import get_db

router = APIRouter(tags=["health"])


@router.get("/healthz")
def healthz(session: Session = Depends(get_db)) -> dict[str, str]:
    """Liveness + DB ping (DESIGN.md §22.1)."""
    try:
        session.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "degraded", "db": "unreachable"},
        ) from None
    return {"status": "ok", "db": "ok"}
