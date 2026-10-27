# Selectable Reviewer Contract (sec-paper edition)

> Resolved configuration for this deployment: **executor = Codex family;
> reviewer = AntiGravity (Gemini) via `tools/antigravity-exec/server.py`**.
> Because executor and reviewer are different model families, a completed,
> in-scope positive review produces **`accept`** (cross-family) receipts —
> not `provisional`.

## Resolution order (every reviewer slot)

1. **Invocation override** — model/effort may be overridden for AntiGravity/Gemini only. Another backend is rejected, not a fallback.
2. **Project config** — `<project>/.aris/reviewer.json`:
   ```json
   {"backend": "antigravity", "model": "gemini-3.8-flash-high", "effort": "high"}
   ```
3. **Project-independent default** — AntiGravity, `gemini-3.8-flash-high`, effort high. Missing CLI/login or failed model identity/probe is BLOCKED. Codex never takes the reviewer role.

Resolve programmatically:

```bash
python3 tools/reviewer_route.py --project <project-root> --host codex --tier deep
python3 tools/review.py probe --project <project-root>
python3 tools/review.py run --project <project-root> --phase sec-novelty-check \
  --run-id <child-run-id> --executor <actual-codex-model> \
  --input idea-stage/IDEA_REPORT.md --input results \
  --prompt-file <novelty-review-prompt.md>
```

## Independence classes

| Where used | Topology | Receipt |
|---|---|---|
| Candidate triage, novelty, external review, evidence audit, final refinement acceptance, final review-loop acceptance, all final paper audits | **fresh-context** — omit --continue-from; reviewer reads primary artifacts, not the producer's self-assessment | accept only a completed, in-scope positive receipt |
| Refinement and repair-verification rounds | **warm** — explicit --continue-from receipt; objections may persist; never call this cold | intermediate repair feedback, not final acceptance |

Rules:
- Record the **actual returned model identity** in `.aris/traces/`; never claim cross-family from config alone.
- An unavailable reviewer is `REVIEW_UNAVAILABLE` — a blocking state, never a fabricated PASS.
- Forward invocation reviewer overrides to reviewer-bearing children (`sec-idea-discovery` → `sec-novelty-check`/`sec-research-review`; `sec-research-pipeline` → all stages).
- `review.py` saves raw bridge events/response plus a JSON receipt under `<project>/.aris/traces/<uuid>/`. It binds actual Gemini model/thread, phase, run ID, raw trace digest and input snapshot. A non-positive verdict is saved but never accepted. Logs are process evidence, not cryptographic truth guarantees.
- In review prompts map task verdicts to the JSON decision vocabulary: ACCEPT/AUDIT_PASS/READY -> PASS; failure -> REVISE/BLOCK/ABANDON; retain original reasoning in findings. Never convert a negative verdict to positive just to advance state.
- Use the receipt path, NOT a made-up session label, as `run_state.py accept --verdict-id`. Artifacts changing invalidate receipts; rerun independent audits after the final edit.

## Backend server

`tools/antigravity-exec/server.py` is the MCP/CLI bridge to the local logged-in `agy` binary. See `tools/antigravity-exec/README.md` for setup; the repo's `.aris/reviewer.example.json` shows the expected project config.
