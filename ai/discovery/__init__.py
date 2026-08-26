"""Topic discovery & query generation interfaces (DESIGN.md §13.2, §14)."""

import uuid
from typing import Protocol


class DiscoveryService(Protocol):
    def generate_queries(self, topic_id: uuid.UUID) -> list[str]: ...
