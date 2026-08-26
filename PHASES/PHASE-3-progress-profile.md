# Phase 3 — Progress & Profile

> **Objective:** Learners can track progress.
> **Weeks:** 2–3 · **Lead:** Dev 1 · **Support:** Dev 2
> **Depends on:** P2
> **Covers:** FR-15..18, FR-33..35 · §21 Personalization (rule-based only) · §22.2 progress/profile endpoints

---

## Entry Criteria

- P2 exit met: both roadmaps navigable from seeds; topics resolvable by id/slug.
- Auth + `AuthUserContext` live (from P1).

---

## Tasks

### Dev 2 — Progress & Preferences API

- [ ] GET `/progress?roadmap_id=` returns caller's progress rows for that roadmap (§22.1)
- [ ] PUT `/progress` upsert `{topic_id, status}`; sets/clears `completed_at`; single round-trip response includes recomputed `{roadmap_pct, section_pct}` for the topic's roadmap (§22.2)
- [ ] Ownership enforced on every progress write; anonymous writes rejected 401 (§26 authz row)
- [ ] PATCH `/users/me/preferences`: experience_level (enum), weekly_hours (`BETWEEN 0 AND 80` CHECK), interests (tag array), target_role — FR-03 inputs of §21
- [ ] Suggested-next service: first incomplete topic whose prerequisites are all completed (FR-34); pure function + unit tests (orderings, ties, no-cycle guarantees)
- [ ] Stub→real swap for these CRUD endpoints completed (§33.3 integration point)
- [ ] Idempotent upsert behavior tested (double-submit same status = no duplicate rows)

### Dev 1 — Tracking UX & Personalization

- [ ] Topic detail: status toggle trio (not_started / in_progress / completed); anonymous click → sign-in prompt, never a dead end (FR-15, FR-18)
- [ ] Dashboard `/dashboard`:
  - continue-learning cards ("resume where you left off")
  - enrolled roadmaps = those with ≥1 progress row (no enrollment table — derived, §12.2)
  - per-roadmap ring, section %, last activity (FR-16)
- [ ] Projected finish line: "≈ N weeks at your pace" using remaining topic-hours ÷ weekly_hours, honest ±25% band shown (FR-17, FR-35, §21)
- [ ] Roadmap page personalization:
  - "For your level" highlight on topics ≤ user level; far-above-level topics visually dimmed (FR-33)
  - "Suggested next" marker on the computed next topic (roadmap page + dashboard) (FR-34)
- [ ] `/settings/profile`: level select, hours slider, interest tag input, target-role field (§25.2)
- [ ] `<ProgressBar>` family renders purely from server-computed values — deterministic math, no client-side invention (P3 principle)

---

## Exit Criteria (§34, verbatim)

> Full learner loop demoable signed-in; percentages correct vs SQL check.

---

## Verification

```bash
pytest tests/services/test_progress_math.py   # pct math vs SQL aggregate on randomized fixtures
pytest tests/services/test_suggested_next.py  # prerequisite-aware ordering cases
```

- Manual demo (Priya persona §4): set beginner + 6 hrs/wk → Foundations topics highlighted, first HTML topic marked suggested-next, header shows "≈ N weeks at your pace".
- Signed-out visitor can still browse all content; only progress actions prompt sign-in (FR-18).
- SQL cross-check script: dashboard % equals aggregate over `user_progress` for a seeded test user.

---

## Risks & Fallbacks

| Risk | Mitigation |
|---|---|
| Personalization scope creep toward ML/LLM plans | Rules only at MVP; LLM "first two weeks" narrative is a documented post-MVP idea (§21) |
| Progress write spam / races | Single upsert path, unique(user_id, topic_id), idempotency tests |
| Percent math drift between UI and DB | Server computes once; UI never recomputes; SQL parity test in CI |
