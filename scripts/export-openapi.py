#!/usr/bin/env python
"""Export FastAPI OpenAPI JSON schema to shared/contracts/openapi.json (DESIGN.md §31, §33.2)."""

import json
import sys
from pathlib import Path

# Ensure apps/api is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "apps" / "api"))

from app.main import app  # noqa: E402


def export_openapi() -> None:
    openapi_data = app.openapi()
    output_path = Path(__file__).resolve().parent.parent / "shared" / "contracts" / "openapi.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(openapi_data, f, indent=2)

    count = len(openapi_data.get("paths", {}))
    print(f"[OK] Exported OpenAPI snapshot ({count} endpoints) -> {output_path}")


if __name__ == "__main__":
    export_openapi()
