# Phase 2 — Roadmap Engine

> **Objective:** Browsable catalog from seeds.
> **Weeks:** 1–2 · **Lead:** Dev 1 + Dev 2 (paired)
> **Depends on:** P1
> **Covers:** FR-05..09 · FR-08 (draft state) · AD-8 (seeds not editor) · §20 Roadmap Architecture · §25 UI pages

---

## Entry Criteria

- P1 exit met: compose up works, auth live, OpenAPI types generated, CI green.
- Seed JSON schema frozen (validated in CI).

---

## Tasks

### Dev 2 — Seeder & Public Endpoints

- [ ] `database/seeder.py`: validates seed JSON against schema, topological cycle check over `topic_dependencies`, upserts by slug, bumps `seed_version`, unpublishes orphans (never hard-delete — user progress must survive) — §20.3, §12.2
- [ ] Author `database/seeds/frontend-developer.json` and `data-analyst.json`:
  - ordered sections → topics → one-level subtopics (FR-06)
  - topics carry title/slug/description/difficulty/estimated_hours/**learning_objectives** (FR-07; objectives are pipeline-consumable in P5, §13.1)
  - prerequisite edges within same roadmap only (§12.2 integrity note)
- [ ] CLI flags: `--roadmap frontend-developer` and full reseed (§12.3)
- [ ] Endpoints: GET `/roadmaps` (published only; drafts visible to admins), GET `/roadmaps/{slug}` (full structure incl. sections/topics/deps), GET `/topics/{id}` (detail; resources empty at this stage) — FR-05..07, §22.1
- [ ] Draft/published toggle honored in queries (FR-08)
- [ ] Document "add a roadmap = commit JSON + reseed" in README (FR-09, no UI editor)
- [ ] Token-protected ISR revalidate endpoint contract agreed with API side (called after publishes from P4 on) — §10.1

### Dev 1 — Learner Surfaces

- [ ] Landing `/`: hero ("Learn X. Resources curated by AI, verified by humans."), featured roadmaps, CTA — §25.2
- [ ] Catalog `/roadmaps`: cards with title, topic count, difficulty, tag chips; difficulty/tag filters
- [ ] Roadmap detail `/roadmaps/[slug]`:
  - `<RoadmapOutline>` vertical sectioned outline — section headers with progress rings (empty for now), expandable `<TopicCard>` rows — §20.2, §10.4
  - Topic rows show status dot, difficulty chip, est. hours, prerequisite-met indicator; subtopics indented one level
  - Sticky section nav; overall progress bar slot
- [ ] Topic detail shell `/roadmaps/[slug]/[topicSlug]`: description, objectives checklist, prerequisites with met/unmet status, empty-resources state ("No resources yet") — §25.2
- [ ] SSR + ISR rendering for public pages; ISR revalidate wiring stubbed ready — §10.1
- [ ] Design direction applied (own identity): warm paper background, ink text, indigo→teal gradient reserved for progress/brand, Inter + JetBrains Mono — §25.3
- [ ] A11y pass: keyboard-complete outline navigation, visible focus, status = icon+text (not color alone), WCAG 2.1 AA contrast targets — §25.3
- [ ] Mobile-first stacking of the outline; admin-free pages fully responsive

---

## Exit Criteria (§34, verbatim)

> Both seeded roadmaps fully navigable, mobile-clean, Lighthouse a11y ≥ 90.

---

## Verification

```bash
python database/seeder.py --roadmap frontend-developer   # upserts cleanly
python database/seeder.py --roadmap frontend-developer   # run twice → identical row counts (idempotent)
pytest tests/test_seed_validation.py                      # circular-dependency seed rejected
```

- Anonymous visitor browses everything end-to-end with zero auth prompts (FR-18 precondition).
- Lighthouse (or equivalent) a11y score ≥ 90 on `/roadmaps/frontend-developer`.
- Draft roadmap invisible to anonymous API calls, visible to admin cookie.

---

## Risks & Fallbacks

| Risk | Mitigation |
|---|---|
| Thin learning_objectives slows P5 TopicContext quality | Write real objectives now while authors are engaged |
| Scope creep toward visual graph editor | Explicitly deferred (AD-8); optional x/y columns noted for post-MVP only (§20.2) |
| Reseed breaks progress links | Orphan topics are unpublished, never deleted (§20.3) — add regression test |
