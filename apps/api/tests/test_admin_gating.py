"""Role-based authorization and admin route gating tests (DESIGN.md §22.3, §23.2)."""

import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password
from app.models.enums import UserRole
from app.models.user import User


def test_admin_gating(client: TestClient, db_session: Session) -> None:
    # 1. Normal learner user
    learner = User(
        id=uuid.uuid4(),
        email="learner_user@example.com",
        password_hash=hash_password("Pass123!"),
        name="Learner",
        role=UserRole.user,
    )
    # 2. Admin user
    admin = User(
        id=uuid.uuid4(),
        email="admin_user@example.com",
        password_hash=hash_password("AdminPass123!"),
        name="Admin",
        role=UserRole.admin,
    )
    db_session.add_all([learner, admin])
    db_session.commit()

    learner_token, _ = create_access_token(learner.id, learner.role.value)
    admin_token, _ = create_access_token(admin.id, admin.role.value)

    # 3. Unauthenticated -> 401
    unauth_res = client.get("/api/v1/admin/search-runs")
    assert unauth_res.status_code == 401

    # 4. Authenticated as non-admin -> 403 Forbidden
    forbidden_res = client.get(
        "/api/v1/admin/search-runs",
        cookies={"cpgs_access_token": learner_token},
    )
    assert forbidden_res.status_code == 403
    assert forbidden_res.json()["detail"]["code"] == "forbidden"

    # 5. Authenticated as Admin -> 200 OK
    admin_res = client.get(
        "/api/v1/admin/search-runs",
        cookies={"cpgs_access_token": admin_token},
    )
    assert admin_res.status_code == 200
    data = admin_res.json()
    assert isinstance(data, list)
