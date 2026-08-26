"""Tests for real database-backed Roadmap and Topic endpoints (DESIGN.md §20, §22.1)."""

import pytest

from app.core.security import create_access_token, hash_password
from app.models.enums import UserRole
from app.models.user import User
from database.seeder import seed_roadmap


@pytest.fixture
def seed_test_data(db_session):
    fe_data = {
        "slug": "frontend-dev",
        "title": "Frontend Developer",
        "description": "Frontend roadmap description",
        "difficulty": "beginner",
        "is_published": True,
        "seed_version": 1,
        "sections": [
            {
                "title": "Web Foundations",
                "order": 1,
                "topics": [
                    {
                        "slug": "html-intro",
                        "title": "HTML Intro",
                        "difficulty": "beginner",
                        "estimated_hours": 3,
                        "learning_objectives": ["Understand HTML tags", "Build semantic structure"],
                        "depends_on": [],
                    },
                    {
                        "slug": "css-intro",
                        "title": "CSS Intro",
                        "difficulty": "beginner",
                        "estimated_hours": 4,
                        "learning_objectives": ["Understand selectors", "Use flexbox"],
                        "depends_on": ["html-intro"],
                    },
                ],
            }
        ],
    }

    draft_data = {
        "slug": "internal-ai-roadmap",
        "title": "Internal AI Engineering",
        "description": "Draft roadmap only for staff",
        "difficulty": "advanced",
        "is_published": False,
        "seed_version": 1,
        "sections": [
            {
                "title": "LLM Fundamentals",
                "order": 1,
                "topics": [
                    {
                        "slug": "transformers",
                        "title": "Transformers",
                        "difficulty": "advanced",
                        "estimated_hours": 10,
                        "learning_objectives": ["Attention mechanism"],
                        "depends_on": [],
                    }
                ],
            }
        ],
    }

    rm_fe = seed_roadmap(db_session, fe_data)
    rm_draft = seed_roadmap(db_session, draft_data)
    return {"fe": rm_fe, "draft": rm_draft}


def test_anonymous_list_roadmaps(client, seed_test_data):
    response = client.get("/api/v1/roadmaps")
    assert response.status_code == 200
    data = response.json()
    slugs = [r["slug"] for r in data]
    assert "frontend-dev" in slugs
    # Draft must be hidden from anonymous visitor
    assert "internal-ai-roadmap" not in slugs


def test_anonymous_get_roadmap_detail(client, seed_test_data):
    response = client.get("/api/v1/roadmaps/frontend-dev")
    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == "frontend-dev"
    assert len(data["sections"]) == 1
    assert data["sections"][0]["title"] == "Web Foundations"
    assert len(data["sections"][0]["topics"]) == 2

    # Check dependency resolution
    css_topic = next(t for t in data["sections"][0]["topics"] if t["slug"] == "css-intro")
    assert css_topic["depends_on"] == ["html-intro"]


def test_anonymous_cannot_view_draft_roadmap(client, seed_test_data):
    response = client.get("/api/v1/roadmaps/internal-ai-roadmap")
    assert response.status_code == 404


def test_admin_can_view_draft_roadmap(client, db_session, seed_test_data):
    admin = User(
        email="admin@example.com",
        password_hash=hash_password("AdminPass123!"),
        name="Admin User",
        role=UserRole.admin,
    )
    db_session.add(admin)
    db_session.commit()

    token, _ = create_access_token(admin.id, role=admin.role.value)
    client.cookies.set("cpgs_access_token", token)

    # Admin list includes draft
    response = client.get("/api/v1/roadmaps")
    assert response.status_code == 200
    slugs = [r["slug"] for r in response.json()]
    assert "frontend-dev" in slugs
    assert "internal-ai-roadmap" in slugs

    # Admin can view draft detail
    detail_res = client.get("/api/v1/roadmaps/internal-ai-roadmap")
    assert detail_res.status_code == 200
    assert detail_res.json()["slug"] == "internal-ai-roadmap"


def test_get_topic_detail(client, seed_test_data):
    # Find topic ID from roadmap detail
    rm_res = client.get("/api/v1/roadmaps/frontend-dev")
    topic = rm_res.json()["sections"][0]["topics"][1]  # css-intro
    topic_id = topic["id"]

    # Test by ID
    res = client.get(f"/api/v1/topics/{topic_id}")
    assert res.status_code == 200
    data = res.json()
    assert data["slug"] == "css-intro"
    assert data["prerequisites"] == ["html-intro"]
    assert "Use flexbox" in data["learning_objectives"]

    # Test by Slug
    slug_res = client.get("/api/v1/topics/by-slug/frontend-dev/css-intro")
    assert slug_res.status_code == 200
    assert slug_res.json()["id"] == topic_id


def test_not_found_errors(client):
    assert client.get("/api/v1/roadmaps/does-not-exist").status_code == 404
    assert client.get("/api/v1/topics/00000000-0000-0000-0000-000000000000").status_code == 404
