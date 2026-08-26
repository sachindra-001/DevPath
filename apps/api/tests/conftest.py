"""Pytest fixtures for FastAPI testing with SQLite in-memory compilation rules (DESIGN.md §35)."""

import json
import sqlite3
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import ARRAY as SA_ARRAY
from sqlalchemy import create_engine, event
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from sqlalchemy.dialects.postgresql import CITEXT, JSONB, UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.deps import get_db
from app.main import app
from app.models.base import Base

# Teach sqlite3 how to adapt list and dict to JSON string
sqlite3.register_adapter(list, json.dumps)
sqlite3.register_adapter(dict, json.dumps)


# Teach SQLite dialect how to compile PostgreSQL / ARRAY specific types
@compiles(CITEXT, "sqlite")
def compile_citext(type_, compiler, **kw):
    return "TEXT"


@compiles(PG_ARRAY, "sqlite")
@compiles(SA_ARRAY, "sqlite")
def compile_array(type_, compiler, **kw):
    return "JSON"


@compiles(JSONB, "sqlite")
def compile_jsonb(type_, compiler, **kw):
    return "JSON"


@compiles(UUID, "sqlite")
def compile_uuid(type_, compiler, **kw):
    return "CHAR(36)"


try:
    from pgvector.sqlalchemy import Vector

    @compiles(Vector, "sqlite")
    def compile_vector(type_, compiler, **kw):
        return "TEXT"
except ImportError:
    pass

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Register adapters directly on raw connection
    pass


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_db() -> Generator[None, None, None]:
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
