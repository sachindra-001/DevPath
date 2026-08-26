"""LLM evaluation wrapper and prompts (DESIGN.md §16)."""

from typing import Protocol


class ResourceEvaluator(Protocol):
    def evaluate(self, candidate_content: str, topic_context: dict) -> dict: ...
