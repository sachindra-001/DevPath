"""API v1 master router incorporating all sub-routers (DESIGN.md §22.1)."""

from fastapi import APIRouter

from app.api.v1.routers import (
    admin_candidates,
    admin_resources,
    admin_runs,
    auth,
    health,
    progress,
    roadmaps,
    topics,
    users,
)

api_v1_router = APIRouter()
api_v1_router.include_router(health.router)
api_v1_router.include_router(auth.router)
api_v1_router.include_router(users.router)
api_v1_router.include_router(roadmaps.router)
api_v1_router.include_router(topics.router)
api_v1_router.include_router(progress.router)
api_v1_router.include_router(admin_runs.router)
api_v1_router.include_router(admin_candidates.router)
api_v1_router.include_router(admin_resources.router)
