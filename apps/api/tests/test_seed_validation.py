"""Tests for seed validation, DAG cycle detection, and idempotent database seeding."""

import sys
from pathlib import Path

from sqlalchemy import func, select

from app.models.roadmap import Roadmap, RoadmapSection, RoadmapTopic, TopicDependency
from database.seeder import seed_roadmap, validate_seed_data


def test_valid_seed_validation():
    valid_data = {
        "slug": "test-roadmap",
        "title": "Test Roadmap",
        "difficulty": "beginner",
        "sections": [
            {
                "title": "Section 1",
                "order": 1,
                "topics": [
                    {
                        "slug": "topic-1",
                        "title": "Topic 1",
                        "difficulty": "beginner",
                        "estimated_hours": 2,
                        "learning_objectives": ["Obj 1"],
                        "depends_on": [],
                    },
                    {
                        "slug": "topic-2",
                        "title": "Topic 2",
                        "difficulty": "intermediate",
                        "estimated_hours": 4,
                        "learning_objectives": ["Obj 2"],
                        "depends_on": ["topic-1"],
                    },
                ],
            }
        ],
    }
    errors = validate_seed_data(valid_data, "test.json")
    assert errors == []


def test_circular_dependency_detected():
    cyclic_data = {
        "slug": "test-cyclic",
        "title": "Cyclic Roadmap",
        "difficulty": "beginner",
        "sections": [
            {
                "title": "Section 1",
                "order": 1,
                "topics": [
                    {
                        "slug": "topic-a",
                        "title": "Topic A",
                        "difficulty": "beginner",
                        "learning_objectives": [],
                        "depends_on": ["topic-b"],
                    },
                    {
                        "slug": "topic-b",
                        "title": "Topic B",
                        "difficulty": "beginner",
                        "learning_objectives": [],
                        "depends_on": ["topic-a"],
                    },
                ],
            }
        ],
    }
    errors = validate_seed_data(cyclic_data, "cyclic.json")
    assert len(errors) > 0
    assert any("circular dependency detected" in err for err in errors)


def test_unknown_dependency_detected():
    bad_dep_data = {
        "slug": "test-bad-dep",
        "title": "Bad Dep Roadmap",
        "difficulty": "beginner",
        "sections": [
            {
                "title": "Section 1",
                "order": 1,
                "topics": [
                    {
                        "slug": "topic-x",
                        "title": "Topic X",
                        "difficulty": "beginner",
                        "learning_objectives": [],
                        "depends_on": ["non-existent-topic"],
                    }
                ],
            }
        ],
    }
    errors = validate_seed_data(bad_dep_data, "baddep.json")
    assert len(errors) > 0
    assert any("unknown topic" in err for err in errors)


def test_idempotent_database_seeding(db_session):
    seed_data = {
        "slug": "web-basics",
        "title": "Web Basics",
        "description": "Learn fundamentals of web dev",
        "difficulty": "beginner",
        "seed_version": 1,
        "sections": [
            {
                "title": "Foundations",
                "order": 1,
                "topics": [
                    {
                        "slug": "html",
                        "title": "HTML",
                        "difficulty": "beginner",
                        "estimated_hours": 3,
                        "learning_objectives": ["Structure page"],
                        "depends_on": [],
                    },
                    {
                        "slug": "css",
                        "title": "CSS",
                        "difficulty": "beginner",
                        "estimated_hours": 5,
                        "learning_objectives": ["Style page"],
                        "depends_on": ["html"],
                    },
                ],
            }
        ],
    }

    # First run
    rm1 = seed_roadmap(db_session, seed_data)
    assert rm1.slug == "web-basics"
    assert db_session.scalar(select(func.count(Roadmap.id))) == 1
    assert db_session.scalar(select(func.count(RoadmapSection.id))) == 1
    assert db_session.scalar(select(func.count(RoadmapTopic.id))) == 2
    assert db_session.scalar(select(func.count(TopicDependency.topic_id))) == 1

    # Second run with same data
    rm2 = seed_roadmap(db_session, seed_data)
    assert rm2.id == rm1.id
    assert db_session.scalar(select(func.count(Roadmap.id))) == 1
    assert db_session.scalar(select(func.count(RoadmapSection.id))) == 1
    assert db_session.scalar(select(func.count(RoadmapTopic.id))) == 2
    assert db_session.scalar(select(func.count(TopicDependency.topic_id))) == 1
