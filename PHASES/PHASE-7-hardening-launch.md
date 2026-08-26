# Phase 7 — Hardening & Launch

> **Objective:** Demo-ready, deployed, monitored.
> **Weeks:** 7 (+ week 8 buffer) · **Lead:** All hands · Dev 2 ops
> **Depends on:** P6
> **Covers:** §26 Security · §29 Error handling · §30 Observability · §35 Testing (E2E/perf) · §36 Deployment · P7 exit gate

---

## Entry Criteria

- P6 exit met: full pipeline works end-to-end; golden set green.
- Both apps deployable; Sentry installed (from P1) but not yet tuned.

---

## Tasks

### Dev 1 — E2E & UX Sweep

- [ ] Playwright flow 1: fresh visitor → browse → signup → mark topic progress → dashboard reflects it (§35 E2E row)
- [ ] Playwright flow 2: admin triggers run (mock mode) → reviews → approves → resource visible on public page
- [ ] Nightly CI schedule + pre-release run for both flows
- [ ] Frontend hardening per §29: TanStack Query retry policy verified, route-level error boundaries with recovery actions, skeletons everywhere (no spinners), toasts for mutation failures
- [ ] A11y + responsive final sweep on learner surfaces (AA contrast, keyboard-complete, reduced-motion respected — §25.3)

### Dev 2 — Security, Perf, Ops

- [ ] Security pass vs §26 table line-by-line + OWASP basics:
  - headers: CSP (self + Vercel/Sentry allowances), `X-Content-Type-Options: nosniff`, `frame-ancestors 'none'`, Referrer-Policy strict-origin-cross-origin, HSTS both hosts
  - rate limits confirmed live (login/register 10/min/IP; trigger 5/hr/admin; 100/min/user)
  - CI grep for known secret key patterns green; `.env.example` complete; Dependabot alerts on; lockfiles committed
- [ ] Perf sanity: k6-lite script at modest concurrency → p95 < 200 ms reads locally (informational target, §35)
- [ ] Sentry activated both apps with release tagging + alert routing smoke-tested
- [ ] Budget guardrail live: `LLM_MONTHLY_BUDGET_USD` soft alert at 80%; admin overview shows MTD spend rollups from `search_runs.cost` (§28.2)
- [ ] Rollback drill executed once: redeploy previous image tag; confirm forward-only/additive-first migration tolerance (N-1 app on N schema) (§36)
- [ ] Smoke gate: zero 5xx across a 100-request scripted pass

### Dev 3 — Content & Prompt Hygiene

- [ ] Populate **both** roadmaps via real pipeline runs + review sessions: target 5–8 approved resources per core topic with type diversity (docs/tutorial/video mix) (FR-13)
- [ ] Weekly spot-check habit documented: sample 5 auto-rejected candidates/run; findings tune weights/thresholds by PR (§19.2)
- [ ] Prompt changelog + before/after outputs archived in `docs/`; ADR notes finalized (§31 docs/)
- [ ] Dead-link sweep run once manually over published resources (schema supports it; automation stays post-MVP, §13.14)

### All — Launch Ritual

- [ ] Demo script written + fallback recording captured (works offline via compose if vendors misbehave)
- [ ] Fresh-environment rehearsal: new clone → `compose up` → full demo path
- [ ] Tag `v0.1.0`; release notes assembled from Conventional Commits history

---

## Exit Gate (§34, verbatim)

> Fresh visitor → signup → progress flow passes E2E; admin fills a *new* topic's shelf purely via pipeline+review in <30 min; error budget: zero 5xx in a 100-request smoke; costs dashboard shows real spend; rollback procedure tested once.

---

## Verification Checklist

| Gate item | Evidence |
|---|---|
| Visitor→signup→progress E2E | Green Playwright run in CI |
| New-topic shelf via pipeline+review <30 min | Timed recorded session |
| Zero 5xx / 100 requests | Smoke log artifact |
| Real spend visible | Admin overview screenshot w/ MTD cost |
| Rollback tested | Drill notes + redeploy tag reference |
| Golden-set still green | Harness CI badge |

---

## Buffer-Week Guidance (week 8)

Cut order under pressure (least product value first):

1. Embedding dedup tier 3 → keep hash/canonical tiers only (flagged honestly).
2. YouTube/GitHub special extractors → Passthrough extractor suffices for demo.
3. Interests-based catalog boost (FR-33 partial) → level highlights + suggested-next carry personalization.

Never cut: human review gate (P5), SSRF/robots controls, auth, transactional publish.

---

## Risks & Fallbacks

| Risk | Mitigation |
|---|---|
| Content population takes longer than a week | Start populating during P6 slack; prioritize core topics of the 2 roadmaps |
| Perf misses 200 ms p95 | Informational only at MVP; documented tradeoff, cache tier is a written revisit trigger (§39) |
| Vendor outage during demo | Offline compose demo + fallback recording + curated allowlist path (§14.3) |
