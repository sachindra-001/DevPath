#!/usr/bin/env python
"""Database Seeder for CPGS Roadmaps (DESIGN.md §12, §20.3).

Validates roadmap seed JSON schemas, performs DAG topological cycle checks over
prerequisites, and performs idempotent upserts into PostgreSQL.
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

# Add apps/api to path so imports resolve cleanly
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root / "apps" / "api"))

from app.core.db import SessionLocal  # noqa: E402
from app.models.enums import DifficultyLevel  # noqa: E402
from app.models.roadmap import (  # noqa: E402
    Roadmap,
    RoadmapSection,
    RoadmapTopic,
    TopicDependency,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("seeder")


def validate_seed_data(data: dict[str, Any], filename: str) -> list[str]:
    """Validate seed JSON structure and ensure no circular dependencies."""
    errors: list[str] = []

    for field in ["slug", "title", "difficulty", "sections"]:
        if field not in data:
            errors.append(f"{filename}: missing required top-level field '{field}'")

    if not isinstance(data.get("sections"), list) or len(data.get("sections", [])) == 0:
        errors.append(f"{filename}: 'sections' must be a non-empty list")
        return errors

    topic_slugs: set[str] = set()
    dependencies_map: dict[str, list[str]] = {}

    for sec_idx, section in enumerate(data.get("sections", [])):
        if "title" not in section or "order" not in section:
            errors.append(f"{filename} Section {sec_idx}: missing 'title' or 'order'")

        topics = section.get("topics", [])
        if not isinstance(topics, list):
            errors.append(f"{filename} Section '{section.get('title')}': 'topics' must be a list")
            continue

        for top_idx, topic in enumerate(topics):
            slug = topic.get("slug")
            title = topic.get("title")
            if not slug or not title:
                errors.append(
                    f"{filename} Topic {top_idx} in Section {sec_idx}: missing 'slug' or 'title'"
                )
                continue

            if slug in topic_slugs:
                errors.append(f"{filename}: duplicate topic slug '{slug}'")
            topic_slugs.add(slug)

            deps = topic.get("depends_on", [])
            if not isinstance(deps, list):
                errors.append(f"{filename} Topic '{slug}': 'depends_on' must be a list of slugs")
            else:
                dependencies_map[slug] = deps

    # Check that all dependencies reference existing topics in this roadmap
    for slug, deps in dependencies_map.items():
        for dep in deps:
            if dep not in topic_slugs:
                errors.append(f"{filename} Topic '{slug}' depends on unknown topic '{dep}'")

    # DAG Cycle detection
    visited: dict[str, int] = {node: 0 for node in topic_slugs}  # 0: unvisited, 1: visiting, 2: visited

    def has_cycle(node: str) -> bool:
        visited[node] = 1
        for neighbor in dependencies_map.get(node, []):
            if neighbor not in dependencies_map:
                continue
            if visited.get(neighbor) == 1:
                return True
            if visited.get(neighbor) == 0 and has_cycle(neighbor):
                return True
        visited[node] = 2
        return False

    for node in topic_slugs:
        if visited[node] == 0 and has_cycle(node):
            errors.append(f"{filename}: circular dependency detected involving topic '{node}'")
            break

    return errors


def seed_roadmap(session: Session, seed_data: dict[str, Any], dry_run: bool = False) -> Roadmap:
    """Idempotently seed or update a roadmap, its sections, topics, and dependencies."""
    slug = seed_data["slug"]
    title = seed_data["title"]
    description = seed_data.get("description")
    difficulty = DifficultyLevel(seed_data.get("difficulty", "beginner"))
    seed_version = seed_data.get("seed_version", 1)
    is_published = seed_data.get("is_published", True)

    # 1. Fetch or create Roadmap
    stmt = select(Roadmap).where(Roadmap.slug == slug)
    roadmap = session.execute(stmt).scalar_one_or_none()

    if roadmap is None:
        roadmap = Roadmap(
            slug=slug,
            title=title,
            description=description,
            difficulty=difficulty,
            is_published=is_published,
            seed_version=seed_version,
        )
        session.add(roadmap)
        session.flush()
        logger.info(f"Created new roadmap: {roadmap.title} ({roadmap.slug})")
    else:
        roadmap.title = title
        roadmap.description = description
        roadmap.difficulty = difficulty
        roadmap.is_published = is_published
        roadmap.seed_version = seed_version
        logger.info(f"Updated existing roadmap: {roadmap.title} ({roadmap.slug})")

    # 2. Existing sections map
    existing_sections = {sec.title: sec for sec in roadmap.sections}
    active_section_ids = set()

    # Existing topics map for this roadmap
    stmt_topics = select(RoadmapTopic).where(RoadmapTopic.roadmap_id == roadmap.id)
    existing_topics = {t.slug: t for t in session.execute(stmt_topics).scalars().all()}
    active_topic_slugs = set()

    # Track dependencies to link after all topics exist
    pending_dependencies: list[tuple[RoadmapTopic, list[str]]] = []

    # 3. Process Sections and Topics
    for sec_data in seed_data.get("sections", []):
        sec_title = sec_data["title"]
        sec_order = sec_data["order"]
        sec_desc = sec_data.get("description")

        section = existing_sections.get(sec_title)
        if section is None:
            section = RoadmapSection(
                roadmap_id=roadmap.id,
                title=sec_title,
                description=sec_desc,
                order_index=sec_order,
            )
            session.add(section)
            session.flush()
        else:
            section.order_index = sec_order
            section.description = sec_desc

        active_section_ids.add(section.id)

        for top_idx, top_data in enumerate(sec_data.get("topics", [])):
            top_slug = top_data["slug"]
            top_title = top_data["title"]
            top_desc = top_data.get("description")
            top_diff = DifficultyLevel(top_data.get("difficulty", "beginner"))
            top_hours = top_data.get("estimated_hours", 4)
            top_objectives = top_data.get("learning_objectives", [])
            top_order = top_idx + 1

            topic = existing_topics.get(top_slug)
            if topic is None:
                topic = RoadmapTopic(
                    roadmap_id=roadmap.id,
                    section_id=section.id,
                    slug=top_slug,
                    title=top_title,
                    description=top_desc,
                    difficulty=top_diff,
                    estimated_hours=top_hours,
                    learning_objectives=top_objectives,
                    order_index=top_order,
                )
                session.add(topic)
                session.flush()
                existing_topics[top_slug] = topic
            else:
                topic.section_id = section.id
                topic.title = top_title
                topic.description = top_desc
                topic.difficulty = top_diff
                topic.estimated_hours = top_hours
                topic.learning_objectives = top_objectives
                topic.order_index = top_order

            active_topic_slugs.add(top_slug)
            pending_dependencies.append((topic, top_data.get("depends_on", [])))

    # 4. Reconcile dependencies
    # Delete existing dependencies for this roadmap's topics first
    topic_ids = [t.id for t in existing_topics.values()]
    if topic_ids:
        session.execute(
            delete(TopicDependency).where(TopicDependency.topic_id.in_(topic_ids))
        )
        session.flush()

    for topic, dep_slugs in pending_dependencies:
        for dep_slug in dep_slugs:
            dep_topic = existing_topics.get(dep_slug)
            if dep_topic and dep_topic.id != topic.id:
                dep = TopicDependency(topic_id=topic.id, depends_on_topic_id=dep_topic.id)
                session.add(dep)

    # 5. Soft-orphan topics that are no longer in the seed (preserve user progress)
    for old_slug, old_topic in existing_topics.items():
        if old_slug not in active_topic_slugs:
            old_topic.section_id = None
            logger.warning(
                f"Topic '{old_slug}' is no longer in seed. Unlinked from section (preserved for user progress)."
            )

    if dry_run:
        session.rollback()
        logger.info(f"[DRY-RUN] Seeding completed without committing changes for {slug}.")
    else:
        session.commit()
        session.refresh(roadmap)
        logger.info(f"Successfully seeded roadmap '{slug}'.")

    return roadmap


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest roadmap seed JSON files into database.")
    parser.add_argument("--roadmap", type=str, help="Specific roadmap slug to seed (e.g. frontend-developer)")
    parser.add_argument("--all", action="store_true", help="Seed all roadmaps found in database/seeds/")
    parser.add_argument("--dry-run", action="store_true", help="Validate and simulate seeding without committing")
    args = parser.parse_args()

    seeds_dir = repo_root / "database" / "seeds"
    if not seeds_dir.exists():
        logger.error(f"Seeds directory not found at {seeds_dir}")
        sys.exit(1)

    if args.roadmap:
        target_file = seeds_dir / f"{args.roadmap}.json"
        if not target_file.exists():
            logger.error(f"Seed file for '{args.roadmap}' not found: {target_file}")
            sys.exit(1)
        seed_files = [target_file]
    else:
        seed_files = sorted(seeds_dir.glob("*.json"))

    if not seed_files:
        logger.warning("No seed JSON files found.")
        sys.exit(0)

    # 1. Validation pass
    logger.info(f"Validating {len(seed_files)} seed file(s)...")
    has_errors = False
    parsed_seeds: list[dict[str, Any]] = []

    for sfile in seed_files:
        try:
            with open(sfile, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            logger.error(f"Failed to parse JSON from {sfile.name}: {e}")
            has_errors = True
            continue

        errs = validate_seed_data(data, sfile.name)
        if errs:
            has_errors = True
            for err in errs:
                logger.error(f"Validation error: {err}")
        else:
            parsed_seeds.append(data)

    if has_errors:
        logger.error("Seed validation failed. Halting before database execution.")
        sys.exit(1)

    # 2. Database seeding pass
    logger.info("Connecting to database for seeding...")
    with SessionLocal() as session:
        for seed_data in parsed_seeds:
            seed_roadmap(session, seed_data, dry_run=args.dry_run)

    logger.info("All roadmap seeds processed successfully.")


if __name__ == "__main__":
    main()
