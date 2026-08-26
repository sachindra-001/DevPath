# Phase 4 — Resources + Admin Core

> **Objective:** Manual resource path works (product usable *without* AI).
> **Weeks:** 3–4 · **Lead:** Dev 2 (Backend) · Dev 1 (Admin UI)
> **Depends on:** P2 (runs parallel to P3)
> **Covers:** FR-10..14, FR-28..32 · §19 Review workflow · §24 Admin screens · AD-9 (single candidates table) · §13.13 transactional publish

---

## Entry Criteria

- P2 exit met; candidate/review schema migrated (done in P1 baseline).
- Fake runner fixtures available via `scripts/mock-ai-run.py` (built in P1).

---

## Tasks

### Dev 2 — Resource Serving & Admin HTTP Layer

- [ ] GET `/topics/{id}` now returns approved resources sorted by `display_order` with full card fields: `{id,title,url,resource_type,access_type,difficulty,source_domain,summary,is_recommended}` (FR-10..11, §22.2)
- [ ] All admin routers behind `require_admin` dependency at inclusion time — an admin route cannot exist unprotected (§23.2):
  - `admin_runs`: POST trigger, GET history, GET live status (§22.1)
  - `admin_candidates`: queue list w/ filters `?run_id&topic_id&status&min_score`, detail incl. full evaluation JSONB, approve, reject, PATCH edit/reassign (FR-28..30)
  - `admin_resources`: PATCH edit, DELETE → archive (unpublish) (§22.1)
- [ ] Manual resource CRUD for admins (fallback when AI wrong/unavailable): reuses URL normalizer + sha256 `url_hash` so manual and AI paths dedupe identically (FR-14, §12.2)
- [ ] **Transactional approve** in one DB transaction: upsert `resources` (+ embedding nullable until P6), insert `topic_resources` link at suggested order, candidate `final_status=approved`, stamp reviewer audit; double-click safe → `409 already_approved` (FR-31, §13.13)
- [ ] Reject stores optional reason; edit metadata; reassign retargets topic and marks candidate for re-evaluation against new TopicContext before any approval (FR-30, §19.2)
- [ ] Every decision stamps `reviewed_by / reviewed_at / review_note` on the candidate row (audit trail replaces separate reviews table, AD-9, FR-32)
- [ ] Trigger endpoint wired to **fake PipelineRunner** that walks a scripted run lifecycle updating counters (BE↔AI seam; real swap P5–P6 behind env var, §33.2)
- [ ] POST `/admin/search-runs` validations complete: `404 unknown_topic`, `409 run_already_active` (partial unique index), `429 rate_limited` (slowapi 5/hr/admin), `503 ai_pipeline_disabled` kill-switch (FR-19, §22.2)
- [ ] Approve triggers Next.js ISR revalidate webhook (recorded in test as a call) — §10.1

### Dev 1 — Admin Suite UI (utilitarian shadcn, §24)

- [ ] `/admin` overview: published resources total, pending queue depth, runs this week, LLM spend MTD slot, dead-link flag count slot (§24.1)
- [ ] `/admin/runs`: history table + New Run dialog (pick topic → active-run conflict pre-check) 
- [ ] `/admin/runs/[id]`: `<RunMonitor>` polls every 3s while running — status stepper + live Found / Evaluated / Recommended / Pending counters + queries viewable + Cancel button (sets cancelled flag between stages) — §11.4, §24.3
- [ ] `/admin/review`: filter bar (topic/run/status/min score); queue default = `pending_review`, sorted `overall DESC` best-first; collapsed presentation for flagged candidates (§19.2)
- [ ] `<CandidateReviewCard>` per §24 ASCII layout: rank + overall score bar, score bars (Relevance/Quality/Authority/Freshness), difficulty match indicator, Covers ✓ / Missing ○ lists, AI summary as plain text node (never rendered HTML), flag badges, original URL from pipeline metadata, actions `[Open URL ↗] [Approve] [Reject] [Edit metadata] [▾ Reassign]`
- [ ] Actions: optimistic approve with rollback-on-error; reject-with-reason inline; metadata edit modal; reassign dropdown; bulk "Approve all recommended" for trusted topics — §19.2
- [ ] Keyboard shortcuts: `a` approve focused card, `r` reject, `j/k` navigate (reviewers process dozens per sitting, §24)
- [ ] `/admin/resources`: published table — search by domain/topic, inline edit, archive, dead-link badge placeholder
- [ ] Topic page `<ResourceList>/<ResourceCard>`: type icon, domain favicon, free/paid badge, quality indicator; links open new tab with `rel="noopener noreferrer" target="_blank"` (FR-12); admin sees reorder control for `display_order`

---

## Exit Criteria (§34, verbatim)

> Admin manually populates a topic; publish revalidates page; audit fields stamped.

---

## Verification

```bash
pytest tests/integration/test_approval_transaction.py   # resource+link+candidate atomic; forced failure rolls back all
pytest tests/api/test_admin_authz.py                     # parametrized: every admin route 403 without admin role
```

- Demo script: admin adds 5 resources manually to one topic → publish → topic page shows them after ISR refresh.
- `mock-ai-run.py` populated queue approves end-to-end through the real UI.
- Every action leaves `reviewed_by/at` stamped (query check).

---

## Risks & Fallbacks

| Risk | Mitigation |
|---|---|
| Review-card UX churn eats the week | Card layout pinned to §24 spec; polish iterations deferred to P6/P7 |
| Fake runner diverges from real contract | `search_runs` row is the only status protocol; mock writes through same repository layer |
| Manual/AI URL mismatch dupes | Shared normalization module used by both paths from day one |
