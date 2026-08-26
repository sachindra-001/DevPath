from collections.abc import Generator

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.main import create_app


class StubResult:
    def scalar(self) -> int:
        return 1


class HealthyStubSession:
    def execute(self, *_args: object, **_kwargs: object) -> StubResult:
        return StubResult()


def override_db_ok() -> Generator[Session, None, None]:
    yield HealthyStubSession()  # type: ignore[misc]


client = TestClient(create_app())
client.app.dependency_overrides[get_db] = override_db_ok  # type: ignore[attr-defined]


def test_healthz_returns_ok_with_db_ping() -> None:
    res = client.get("/api/v1/healthz")
    assert res.status_code == 200
    assert res.json() == {"status": "ok", "db": "ok"}
