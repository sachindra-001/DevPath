"""Resource scoring, deduplication, and ranking interfaces (DESIGN.md §17, §18)."""

from typing import Protocol


class ResourceRanker(Protocol):
    def score_candidate(self, evaluation: dict, url: str) -> float: ...
