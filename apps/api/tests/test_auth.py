"""Authentication and session management tests (FR-01..04, DESIGN.md §23)."""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.enums import UserRole
from app.models.user import User


def test_register_flow(client: TestClient) -> None:
    # 1. Successful registration
    reg_payload = {
        "email": "learner@example.com",
        "password": "Password123!",
        "name": "Alex Learner",
    }
    res = client.post(
        "/api/v1/auth/register",
        json=reg_payload,
        headers={"X-Requested-With": "fetch"},
    )
    assert res.status_code == 201
    data = res.json()
    assert "access_token" in data
    assert data["user"]["email"] == "learner@example.com"
    assert data["user"]["name"] == "Alex Learner"
    assert data["user"]["role"] == "user"

    # Verify cookies
    assert "cpgs_access_token" in res.cookies
    assert "cpgs_refresh_token" in res.cookies

    # 2. Duplicate registration fails with 409
    dup_res = client.post(
        "/api/v1/auth/register",
        json=reg_payload,
        headers={"X-Requested-With": "fetch"},
    )
    assert dup_res.status_code == 409
    assert dup_res.json()["detail"]["code"] == "already_exists"


def test_login_and_logout_flow(client: TestClient, db_session: Session) -> None:
    # Seed user
    user = User(
        email="login_user@example.com",
        password_hash=hash_password("SecretPass123!"),
        name="Login User",
        role=UserRole.user,
    )
    db_session.add(user)
    db_session.commit()

    # 1. Invalid password -> 401
    bad_res = client.post(
        "/api/v1/auth/login",
        json={"email": "login_user@example.com", "password": "WrongPassword!"},
        headers={"X-Requested-With": "fetch"},
    )
    assert bad_res.status_code == 401

    # 2. Valid password -> 200 + cookies
    good_res = client.post(
        "/api/v1/auth/login",
        json={"email": "login_user@example.com", "password": "SecretPass123!"},
        headers={"X-Requested-With": "fetch"},
    )
    assert good_res.status_code == 200
    access_cookie = good_res.cookies.get("cpgs_access_token")
    assert access_cookie is not None

    # 3. GET /users/me with cookie
    me_res = client.get("/api/v1/users/me", cookies={"cpgs_access_token": access_cookie})
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "login_user@example.com"

    # 4. PATCH /users/me/preferences
    pref_res = client.patch(
        "/api/v1/users/me/preferences",
        json={
            "experience_level": "beginner",
            "weekly_hours": 10,
            "interests": ["react", "typescript"],
        },
        cookies={"cpgs_access_token": access_cookie},
        headers={"X-Requested-With": "fetch"},
    )
    assert pref_res.status_code == 200
    assert pref_res.json()["experience_level"] == "beginner"
    assert pref_res.json()["weekly_hours"] == 10

    # 5. Logout
    logout_res = client.post(
        "/api/v1/auth/logout",
        cookies={"cpgs_access_token": access_cookie},
        headers={"X-Requested-With": "fetch"},
    )
    assert logout_res.status_code == 200


def test_csrf_middleware_enforcement(client: TestClient) -> None:
    # State-changing method without X-Requested-With header when no bearer token
    res = client.post(
        "/api/v1/auth/login",
        json={"email": "anyone@example.com", "password": "Pass"},
    )
    assert res.status_code == 403
    assert res.json()["error"]["code"] == "csrf_validation_failed"
