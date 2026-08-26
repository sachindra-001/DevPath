"""Stub endpoints and contract fixture tests (DESIGN.md §22, §33.2)."""

import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password
from app.models.enums import UserRole
from app.models.user import User
from database.seeder import seed_roadmap


def test_public_roadmaps_and_topics(client: TestClient, db_session: Session) -> None:
    # Seed data
    fe_data = {
        "slug": "frontend-developer",
        "title": "Frontend Developer",
        "description": "Frontend roadmap",
        "difficulty": "beginner",
        "is_published": True,
        "sections": [
            {
                "title": "Basics",
                "order": 1,
                "topics": [
                    {
                        "slug": "html",
                        "title": "HTML",
                        "difficulty": "beginner",
                        "learning_objectives": ["Tags"],
                        "depends_on": [],
                    }
                ],
            }
        ],
    }
    da_data = {
        "slug": "data-analyst",
        "title": "Data Analyst",
        "description": "Data roadmap",
        "difficulty": "beginner",
        "is_published": True,
        "sections": [
            {
                "title": "SQL",
                "order": 1,
                "topics": [
                    {
                        "slug": "sql-basics",
                        "title": "SQL Basics",
                        "difficulty": "beginner",
                        "learning_objectives": ["Select"],
                        "depends_on": [],
                    }
                ],
            }
        ],
    }
    seed_roadmap(db_session, fe_data)
    seed_roadmap(db_session, da_data)

    # 1. GET /roadmaps
    res = client.get("/api/v1/roadmaps")
    assert res.status_code == 200
    roadmaps = res.json()
    assert len(roadmaps) >= 2
    slugs = [r["slug"] for r in roadmaps]
    assert "frontend-developer" in slugs
    assert "data-analyst" in slugs

    # 2. GET /roadmaps/{slug}
    res_detail = client.get("/api/v1/roadmaps/frontend-developer")
    assert res_detail.status_code == 200
    detail = res_detail.json()
    assert detail["slug"] == "frontend-developer"
    assert len(detail["sections"]) > 0

    # 3. GET /topics/by-slug/{roadmap_slug}/{topic_slug}
    res_topic = client.get("/api/v1/topics/by-slug/frontend-developer/html")
    assert res_topic.status_code == 200
    topic_data = res_topic.json()
    assert topic_data["slug"] == "html"


def test_progress_endpoints(client: TestClient, db_session: Session) -> None:
    user = User(
        email="learner_progress@example.com",
        password_hash=hash_password("Pass123!"),
        name="Progress Learner",
        role=UserRole.user,
    )
    db_session.add(user)
    db_session.commit()
    token, _ = create_access_token(user.id, user.role.value)

    roadmap_id = uuid.uuid4()
    # GET /progress
    res = client.get(
        f"/api/v1/progress?roadmap_id={roadmap_id}",
        cookies={"cpgs_access_token": token},
    )
    assert res.status_code == 200

    # PUT /progress
    topic_id = uuid.uuid4()
    put_res = client.put(
        "/api/v1/progress",
        json={"topic_id": str(topic_id), "status": "completed"},
        cookies={"cpgs_access_token": token},
        headers={"X-Requested-With": "fetch"},
    )
    assert put_res.status_code == 200
    assert put_res.json()["progress"]["status"] == "completed"
