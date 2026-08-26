#!/usr/bin/env python
"""Validate roadmap seed JSON schemas and check for circular or broken topic dependencies.

Traces to DESIGN.md §20, §33.2.
"""

import json
import sys
from pathlib import Path


def validate_seed_file(file_path: Path) -> list[str]:
    errors: list[str] = []
    if not file_path.exists():
        return [f"File not found: {file_path}"]

    try:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return [f"JSON syntax error in {file_path.name}: {e}"]

    # Required top-level fields
    for field in ["slug", "title", "difficulty", "sections"]:
        if field not in data:
            errors.append(f"{file_path.name}: missing required top-level field '{field}'")

    if not isinstance(data.get("sections"), list) or len(data.get("sections", [])) == 0:
        errors.append(f"{file_path.name}: 'sections' must be a non-empty list")
        return errors

    topic_slugs: set[str] = set()
    dependencies_map: dict[str, list[str]] = {}

    for sec_idx, section in enumerate(data.get("sections", [])):
        if "title" not in section or "order" not in section:
            errors.append(f"{file_path.name} Section {sec_idx}: missing 'title' or 'order'")

        topics = section.get("topics", [])
        if not isinstance(topics, list):
            sec_title = section.get("title")
            errors.append(f"{file_path.name} Section '{sec_title}': 'topics' must be a list")
            continue

        for top_idx, topic in enumerate(topics):
            slug = topic.get("slug")
            title = topic.get("title")
            if not slug or not title:
                err_msg = (
                    f"{file_path.name} Topic {top_idx} in Section {sec_idx}: "
                    "missing 'slug' or 'title'"
                )
                errors.append(err_msg)
                continue

            if slug in topic_slugs:
                errors.append(f"{file_path.name}: duplicate topic slug '{slug}'")
            topic_slugs.add(slug)

            deps = topic.get("depends_on", [])
            if not isinstance(deps, list):
                errors.append(
                    f"{file_path.name} Topic '{slug}': 'depends_on' must be a list of slugs"
                )
            else:
                dependencies_map[slug] = deps

    # Verify all dependencies exist and check for cycles
    for slug, deps in dependencies_map.items():
        for dep in deps:
            if dep not in topic_slugs:
                errors.append(f"{file_path.name} Topic '{slug}' depends on unknown topic '{dep}'")

    # Cycle detection (DFS)
    visited: dict[str, int] = {}  # 0: unvisited, 1: visiting, 2: visited

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
        visited[node] = 0

    for node in topic_slugs:
        if visited[node] == 0 and has_cycle(node):
            errors.append(
                f"{file_path.name}: circular dependency detected involving topic '{node}'"
            )
            break

    return errors


def main() -> None:
    if len(sys.argv) < 2:
        # Default to database/seeds/*.json
        seed_dir = Path(__file__).resolve().parent.parent / "database" / "seeds"
        files = list(seed_dir.glob("*.json"))
    else:
        files = [Path(p) for p in sys.argv[1:]]

    all_valid = True
    for f in files:
        errs = validate_seed_file(f)
        if errs:
            all_valid = False
            print(f"[FAIL] {f.name}:")
            for err in errs:
                print(f"   - {err}")
        else:
            print(f"[PASS] {f.name} validated successfully.")

    if not all_valid:
        sys.exit(1)


if __name__ == "__main__":
    main()
