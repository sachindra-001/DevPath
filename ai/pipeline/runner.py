"""Pipeline orchestrator and runner interfaces (DESIGN.md §11.1, §33.2)."""

import uuid
from typing import Protocol


class PipelineRunner(Protocol):
    """BE <-> AI seam protocol (DESIGN.md §33.2)."""

    def run_topic_discovery(
        self,
        topic_id: uuid.UUID,
        requested_by: uuid.UUID | None = None,
    ) -> uuid.UUID:
        """Trigger discovery pipeline for topic and return search_run_id."""
        ...


class MockPipelineRunner:
    """Mock runner for offline development and testing without spending external API tokens."""

    def __init__(self, session_factory=None) -> None:
        self.session_factory = session_factory

    def run_topic_discovery(
        self,
        topic_id: uuid.UUID,
        requested_by: uuid.UUID | None = None,
    ) -> uuid.UUID:
        search_run_id = uuid.uuid4()
        # Returns a mock run id
        return search_run_id
