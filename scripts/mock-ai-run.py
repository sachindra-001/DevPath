#!/usr/bin/env python
"""Generate mock AI search runs and resource candidates for offline UI testing.

Traces to DESIGN.md §31, §33.2.
"""

import datetime as dt
import hashlib
import sys
import uuid
from pathlib import Path

# Ensure apps/api is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "apps" / "api"))

from app.core.db import SessionLocal  # noqa: E402
from app.models.candidate import ResourceCandidate, SearchRun  # noqa: E402
from app.models.enums import (  # noqa: E402
    CandidateFinalStatus,
    ExtractionStatus,
    SearchRunStatus,
)
from app.models.roadmap import RoadmapTopic  # noqa: E402


def generate_mock_run() -> None:
    session = SessionLocal()
    try:
        topic = session.query(RoadmapTopic).first()
        topic_id = topic.id if topic else uuid.uuid4()

        run = SearchRun(
            id=uuid.uuid4(),
            topic_id=topic_id,
            status=SearchRunStatus.completed,
            queries_generated=[
                "asynchronous javascript promises async await mdn",
                "javascript event loop concurrency model tutorial",
                "fetch api modern javascript guide",
            ],
            candidates_found=15,
            evaluated_count=10,
            recommended_count=4,
            pending_review_count=3,
            llm_prompt_tokens=14200,
            llm_completion_tokens=3100,
            estimated_cost_usd=0.0125,
            started_at=dt.datetime.now(dt.UTC) - dt.timedelta(minutes=2),
            finished_at=dt.datetime.now(dt.UTC),
        )
        session.add(run)

        # Mock candidates
        sample_urls = [
            (
                "MDN Web Docs — Using Promises",
                "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises",
                "developer.mozilla.org",
                0.95,
                CandidateFinalStatus.pending_review,
            ),
            (
                "JavaScript.info — Promise Basics",
                "https://javascript.info/promise-basics",
                "javascript.info",
                0.91,
                CandidateFinalStatus.pending_review,
            ),
            (
                "freeCodeCamp — Async/Await Explained",
                "https://www.freecodecamp.org/news/async-await-javascript/",
                "freecodecamp.org",
                0.86,
                CandidateFinalStatus.pending_review,
            ),
            (
                "Outdated Blog — Callback Hell 2014",
                "https://example.com/blog/callbacks-2014",
                "example.com",
                0.42,
                CandidateFinalStatus.low_score,
            ),
        ]

        for title, url, domain, score, status in sample_urls:
            url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()
            candidate = ResourceCandidate(
                id=uuid.uuid4(),
                topic_id=topic_id,
                search_run_id=run.id,
                url=url,
                url_hash=url_hash,
                title=title,
                source_domain=domain,
                extraction_status=ExtractionStatus.extracted,
                content_text="Guide explaining Promise states, chaining, and error handling...",
                content_chars=4200,
                final_status=status,
                relevance_score=score,
                quality_score=score,
                authority_score=score,
                freshness_score=0.90,
                overall_score=score,
                evaluation={
                    "relevance_score": score,
                    "quality_score": score,
                    "authority_signals": score,
                    "difficulty": "intermediate",
                    "resource_type": "documentation" if "mdn" in domain else "article",
                    "access_type": "free",
                    "summary": f"Comprehensive guide to asynchronous concepts from {domain}.",
                    "recommended": score >= 0.75,
                },
                flags=[],
            )
            session.add(candidate)

        try:
            session.commit()
            print(f"[OK] Inserted mock SearchRun {run.id} with {len(sample_urls)} candidates.")
        except Exception as e:
            session.rollback()
            print(f"[INFO] Skipping DB insertion (DB may not be online yet): {e}")

    finally:
        session.close()


if __name__ == "__main__":
    generate_mock_run()
