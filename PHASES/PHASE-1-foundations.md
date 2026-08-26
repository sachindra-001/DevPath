# Phase 1 — Foundations

> **Objective:** Skeleton runs locally + deploys hello-world.
> **Weeks:** 1 · **Lead:** Dev 2 (Backend & Data) · **Support:** Dev 1, Dev 3
> **Depends on:** — (first phase)
> **Covers:** FR-01..04 · AD-6 (self-hosted JWT) · §11 backend skeleton · §12 schema baseline · §23 auth · §32 workflow setup

---

## Entry Criteria

- DESIGN.md approved as written; repo + platform accounts provisioned day one (GitHub org/repo, Vercel, Render/Railway, managed Postgres w/ pgvector, Sentry).
- `.env` secrets available locally: DB URL, JWT secret, admin seed credentials.

---

## Tasks

### Dev 2 — Backend, DB, Auth, CI/CD

**Monorepo & infra**
- [ ] Init monorepo per §31 layout: `apps/api`, `apps/web`, `ai/`, `database/`, `shared/contracts/`, `scripts/`, `docs/`, `.github/workflows/`
- [ ] `docker-compose.yml`: postgres:16 + pgvector image; `database/init/01-extensions.sql` runs `CREATE EXTENSION vector;`
- [ ] FastAPI app skeleton with layering rules enforced (routers → services → repositories; routers never touch DB) — §11.1
- [ ] `core/config.py` via pydantic-settings; `.env.example` documents every var incl. pipeline tunables (`MAX_CANDIDATES_PER_RUN=30`, `RUN_CONCURRENCY=2`, `DISABLE_AI_PIPELINE=false`, …) — §11.3
- [ ] README.md: 15-minute local setup guide (§31)

**Database baseline**
- [ ] SQLAlchemy 2 models for **all** §12 tables: users, roadmaps, roadmap_sections, roadmap_topics, topic_dependencies, resources, topic_resources, resource_candidates, search_runs, user_progress
- [ ] Alembic baseline migration; forward-only policy noted in PR template (§12.3)
- [ ] Partial unique index on `search_runs.topic_id WHERE status IN ('queued','running')` (FR-19 groundwork)

**Auth (FR-01..04, §23)**
- [ ] Argon2id hashing via passlib; JWT HS256 access token (15 min, claims `{sub, role, jti}`); opaque rotating refresh (7 days, hashed in users row, single active session)
- [ ] httpOnly cookie helpers (`Secure; SameSite=Lax`; refresh scoped to `/api/v1/auth`); no tokens in localStorage ever
- [ ] Routers: POST `/auth/register|login|refresh|logout`, GET `/users/me`; DI deps `get_current_user`, `require_admin`
- [ ] CSRF middleware: require `X-Requested-With: fetch` on state-changing routes (§23.3)
- [ ] First admin seeded via environment config (FR-04)

**API surface**
- [ ] GET `/healthz` — liveness + DB ping (§22.1)
- [ ] **Stub routers returning fixture data** for all remaining §22 endpoints (contract-first, §33.2 FE↔BE seam)
- [ ] Export `shared/contracts/openapi.json` snapshot from FastAPI

### Dev 1 — Frontend Skeleton

- [ ] Next.js 15 App Router scaffold: TypeScript, Tailwind v4, shadcn/ui init, TanStack Query provider — §9
- [ ] `scripts/generate-types.ts` → `src/types/api.d.ts`; CI fails if snapshot stale (§10.5)
- [ ] `AuthUserContext` fed by GET `/users/me` (§10.3)
- [ ] `/login`, `/register` pages against real auth endpoints; establish error pattern (toast + inline field errors) — §29
- [ ] Placeholder routes for full §10.2 route map

### Dev 3 — AI Package Skeleton

- [ ] `ai/` package dirs: `pipeline/ discovery/ extraction/ evaluation/ ranking/` — interfaces only, no logic yet
- [ ] `PipelineRunner` protocol: `run_topic_discovery(topic_id, requested_by) -> search_run_id` (BE↔AI seam, §33.2)
- [ ] `scripts/mock-ai-run.py`: inserts fake search_run + candidate rows (fixture source for P4)
- [ ] pytest scaffolding; pick cassette approach for external Tavily/OpenAI adapters (§35)

### CI/CD (Dev 2 drives, all support)

- [ ] `ci.yml` required gates: lint (ruff/eslint), typecheck (mypy/tsc), tests, build — §32.2
- [ ] Branching live: `main` protected, `feature/*`, squash-merge, Conventional Commits, ≥1 approval, author never merges own PR
- [ ] Vercel project wired (preview deploy per PR); Render/Railway container with release command `alembic upgrade head`
- [ ] Managed Postgres provisioned; daily backups verified (§36)
- [ ] Sentry SDK installed both apps (activation tuning in P7)
- [ ] Seed JSON schema validator `scripts/validate-seeds.py` running in CI (§33.2 Seeds↔all)

---

## Exit Criteria (§34, verbatim)

> Fresh clone → `compose up` → register/login works; CI green; previews live.

---

## Verification

```bash
git clone <repo> && docker compose up -d   # api + db healthy
curl localhost:8000/api/v1/healthz          # 200 {"status":"ok"}
# register → login → GET /users/me round trip returns profile
alembic upgrade head                        # idempotent: run twice, second is no-op
python scripts/validate-seeds.py bad-seed.json   # exits non-zero (negative test)
```

- Sample PR shows all CI checks green; Vercel preview URL renders placeholder page.
- Non-admin receives 403 on an admin stub route (parametrized dependency test).

---

## Risks & Fallbacks

| Risk | Mitigation |
|---|---|
| Platform/account provisioning stalls the week | Create all accounts day 1; develop against compose only if needed |
| FE/BE contract drift | openapi.json committed + CI staleness check (§10.5) |
| Schema churn later | All §12 tables migrated now, even if unused until P4–P6 |
