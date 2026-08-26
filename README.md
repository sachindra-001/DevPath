# CPGS — Career Path Guidance System

Interactive learning-roadmap platform with an **AI-powered resource discovery pipeline** (see [DESIGN.md](DESIGN.md)). Roadmaps are structured data; a background pipeline discovers, evaluates, and ranks web resources — humans approve before publish.

## Stack

| Layer | Tech |
|---|---|
| Frontend (`apps/web`) | Next.js 15 · TypeScript · Tailwind v4 · shadcn/ui · TanStack Query |
| Backend (`apps/api`) | Python 3.12 · FastAPI · SQLAlchemy 2 · Alembic · PostgreSQL 16 + pgvector |
| AI (`ai/`) | OpenAI gpt-4o-mini · Tavily · same process as API (modular monolith) |

## 15-minute local setup

### Prerequisites
- Docker Desktop
- Node 22+ / npm
- Python 3.12 + [uv](https://docs.astral.sh/uv/) (`pip install uv`)

### 1. Environment

```bash
cp .env.example .env        # then edit JWT_SECRET etc.
```

### 2. Backend + database (Docker)

```bash
docker compose up -d --build          # api on :8000, postgres(+pgvector) on :5432
curl http://localhost:8000/api/v1/healthz   # → {"status":"ok","db":"ok"}
```

API docs: http://localhost:8000/api/docs

### 3. Database migrations (host)

```bash
python -m uv sync                      # creates .venv with app + ai packages
.venv\Scripts\activate                 # Windows (source .venv/bin/activate on unix)
cd apps/api && alembic upgrade head && cd ../..
```

### 4. Seed the first admin (FR-04)

```bash
python scripts/seed-admin.py           # reads ADMIN_* from .env, idempotent
```

### 5. Frontend

```bash
cd apps/web
npm install
npm run dev                            # http://localhost:3000
```

## Repository layout (DESIGN.md §31)

```
apps/web          Next.js frontend
apps/api          FastAPI backend (routers → services → repositories)
ai/               pipeline package — same venv/process as api
database/         init SQL + roadmap seeds + seeder
shared/contracts  openapi.json snapshot (FE↔BE contract)
scripts/          dev utilities
```

## Workflow (DESIGN.md §32)

- Branches: `phase/N-*` per phase, squash-merged to `main` after exit criteria pass
- Conventional Commits; CI gates: lint · typecheck · tests · build
