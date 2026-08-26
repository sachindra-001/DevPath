"""Web content extraction and safe fetcher interfaces (DESIGN.md §15)."""

from typing import Protocol


class Extractor(Protocol):
    def extract(self, url: str, raw_html: str) -> dict: ...
