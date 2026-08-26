"""Stub endpoints and contract fixture tests (DESIGN.md §22, §33.2)."""

import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password
from app.models.enums import UserRole
from app.models.user import User


def test_public_roadmaps_and_topics(client: TestClient) -> None:
    # 1. GET /roadmaps
    res = client.get("/api/v1/roadmaps")
    assert res.status_code == 200
    roadmaps = res.json()
    assert len(roadmaps) >= 2
    assert roadmaps[0]["slug"] == "frontend-developer"

    # 2. GET /roadmaps/{slug}
    res_detail = client.get("/api/v1/roadmaps/frontend-developer")
    assert res_detail.status_code == 200
    detail = res_detail.json()
    assert detail["slug"] == "frontend-developer"
    assert len(detail["sections"]) > 0

    # 3. GET /topics/{id}
    topic_id = uuid.uuid4()
    res_topic = client.get(f"/api/v1/topics/{topic_id}")
    assert res_topic.status_code == 200
    topic_data = res_topic.json()
    assert len(topic_data["resources"]) > 0


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
