# Phase 5 — Discovery Pipeline

> **Objective:** Real candidates reach the queue.
> **Weeks:** 4–5 · **Lead:** Dev 3 (AI) · Dev 2 (persistence APIs)
> **Depends on:** P4 (candidate schema + review queue live on fake data)
> **Covers:** FR-19..22, FR-26 · §13.1–13.7 pipeline stages 1–7 · §14 Search strategy · §15 Extraction & safe fetcher · §11.4 background execution

---

## Entry Criteria

- P4 exit met: admin can trigger runs against fake runner and review/publish candidates.
- `PipelineRunner` protocol + mock fixtures in place from P1.

---

## Tasks

### Dev 3 — Pipeline Stages (§13.0 map)

**Stage 1–2: Context + Queries**
- [ ] TopicContext builder (§13.1): assembles topic/roadmap/section/level/prerequisites/objectives deterministically from DB; if objectives missing → one cheap gpt-4o-mini expansion cached back onto the topic row (only generative step here)
- [ ] Query generation prompt (verbatim §13.2): 6–8 diverse queries; deterministic post-processing — case-insensitive dedupe, cap 8, templated fallbacks (`"{topic} tutorial for beginners"`, `"{topic} official documentation"`) guarantee ≥6; stored on `search_runs.queries_generated`

**Stage 3–4: Search + Normalization**
- [ ] Tavily adapter: `search(query, max_results=8, include_raw_content=true, search_depth="basic")`; merge across queries by normalized hash; track `query_hits` per candidate; hard cap `MAX_CANDIDATES_PER_RUN=30` (FR-21, §13.3)
- [ ] Skip logic → `skipped_known` when url_hash already published or evaluated ≤30 days (no re-crawl, no LLM cost) (FR-26); skip non-http(s) + blocked domains
- [ ] URL normalizer (§13.4): https scheme, lowercase host, strip fragment + tracking params (`utm_*`, `fbclid`, …), sort params/drop empties, collapse slashes, host canonicalization (www., mirror map), `url_hash = sha256(normalized_url)`; final-URL re-hash after redirects

**Stage 5–6: Extraction + Cleaning**
- [ ] Safe fetcher per §15.2 table: http(s) allowlist; DNS resolve → reject private/reserved CIDRs (incl. 169.254.169.254 cloud metadata) re-checked per redirect hop; ≤3 redirects; 2 MB decompressed-body cap; 5 s connect / 10 s read; descriptive UA; retry-once on 429/5xx
- [ ] robots.txt resolver with 24h cache → `skipped_robots`, never fetch disallowed (FR-22, §14.4)
- [ ] Extractors behind one interface (`Extractor.select`): Passthrough (Tavily raw_content ≥500 chars), HTML (trafilatura + meta/OG for freshness evidence), YouTube (oEmbed + Data API + best-effort transcript), GitHub REST (README ≤8k chars, stars, pushed_at); PDF → `unsupported_type` (§15.3)
- [ ] Failure taxonomy recorded verbatim on candidate rows: `failed_timeout | failed_fetch | skipped_robots | skipped_robots_meta | too_large | too_thin | unsupported_type | skipped_language` (§15.4)
- [ ] Cleaner (§13.6): whitespace collapse, <500 chars → `too_thin`, ASCII-ratio language gate → `skipped_language`, head-biased truncate to ~6,000 chars (4500+1500), strip instruction-like lines at head/tail (defense-in-depth §27)

**Stage 7: Pre-filter (zero LLM spend)**
- [ ] Deterministic pre-filter (§13.7): domain blacklist auto-reject; snippet-keyword overlap <0.15 → `low_score`; rank remainder by `(query_hits, domain_tier, snippet_overlap)`; evaluate top `MAX_EVALUATIONS_PER_RUN=18`

**Orchestration**
- [ ] `run_topic_discovery`: stage transitions update `search_runs` counters live; global semaphore `RUN_CONCURRENCY=2`; startup sweep marks orphaned `running` runs `failed(reason="process_restart")`; per-candidate failures never abort the run (§11.4, §29)
- [ ] Swap fake runner → real behind env var (§33.3 integration point)
- [ ] Cancel flag honored between stages (§24 monitor button works)

### Dev 2 — Persistence & HTTP Contract

- [ ] Candidate persistence repositories: insert candidates with extraction status, content_text/content_chars, run linkage; unique `(search_run_id, url_hash)`
- [ ] Token/cost columns populated incrementally on `search_runs` (`llm_prompt_tokens`, `llm_completion_tokens`, `estimated_cost_usd`) — consumed properly in P6
- [ ] Run history endpoint filters (`?topic_id&status&limit&offset`) for `/admin/runs`
- [ ] Integration tests with **recorded** Tavily adapters (cassette-style, no external calls in CI) — §35

---

## Exit Criteria (§34, verbatim)

> Run on 5 topics produces ≤30 extracted candidates each; SSRF/robots unit tests pass; zero unhandled exceptions.

---

## Verification

```bash
pytest tests/security/test_ssrf_matrix.py    # all §35 CIDR/scheme/redirect-hop cases blocked
pytest tests/security/test_robots.py         # disallowed domains never fetched
pytest tests/integration/test_run_lifecycle.py  # queued→running→completed counter reconciliation vs SQL
```

- Live run across 5 seeded topics: every run yields ≤30 unique candidates; counters match DB aggregates.
- Structured logs carry request-id; extraction failures visible in run detail ("silence is a bug", §15.4).
- Vendor-outage drill: point adapter at a dead endpoint → curated allowlist fallback still produces candidates (§14.3).

---

## Risks & Fallbacks

| Risk | Mitigation |
|---|---|
| Tavily outage / thin results | Curated seed allowlist queried via the same compliant fetcher (§14.3) |
| Cost surprise before evaluation even exists | Caps (30/18) + pre-filter run *before* any LLM call in this phase |
| Process restart kills in-flight run | Startup sweep marks failed; admin re-runs; accepted limitation documented (AD-5) |
