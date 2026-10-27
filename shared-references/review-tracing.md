# Review Tracing Protocol

Every reviewer call through `tools/review.py` automatically writes a full
prompt/response trace; skills must never route around it.

## What is saved per call (`.aris/traces/<uuid>/`)

- `raw.json` — the complete invocation: phase, run_id, full prompt text, input
  snapshot (SHA-256 per file/section), the raw bridge response
  (`structuredContent` incl. reported model, threadId, full content) and all
  bridge events.
- `receipt.json` — the version-bound verdict: schema_version, backend,
  executor_model, reviewer_model, thread_id, phase, run_id, inputs, snapshot,
  verdict JSON, `raw_trace` path + `raw_trace_sha256`, topology
  (fresh|warm).

## Rules

- Trace **every** reviewer call: triage, novelty, external review, refinement
  rounds, evidence audits, claim routing, ablation review, review-loop rounds,
  and all five final paper audits — fresh and warm alike.
- Never delete or edit a trace directory; failed/unavailable calls keep their
  raw evidence too (they are process records, not decorations).
- `run_state accept` takes the receipt path as `--verdict-id`; a hand-written
  verdict string is rejected.
- Traces enable reviewer-independence audit, warm-thread continuity audit, and
  meta-optimization from real review logs — keep them until the run is closed.
