# Selectable Reviewer Contract (sec-paper edition)

> Resolved configuration for this deployment: **executor = Codex family;
> reviewer = AntiGravity (Gemini) via `tools/antigravity-exec/server.py`**.
> Because executor and reviewer are different model families, a completed,
> in-scope positive review produces **`accept`** (cross-family) receipts —
> not `provisional`.

## Resolution order (every reviewer slot)

1. **Invocation override** — `--reviewer: <backend>` / `--model:` / `--effort:` in the skill's `$ARGUMENTS` wins for that call.
2. **Project config** — `<project>/.aris/reviewer.json`:
   ```json
   {"backend": "antigravity", "model": "gemini-3.8-flash-high", "effort": "high"}
   ```
3. **Host default** — the host harness's reviewer path (e.g., Codex spawn_agent with a secondary model), which for cross-family acceptance requires the actual returned identity to differ in family from the executor.

Resolve programmatically:

```bash
python3 tools/reviewer_route.py <project-root> --host codex --tier deep
# -> {"backend": "antigravity", "model": "...", "effort": "...", "tools": {...}}
```

## Independence classes

| Where used | Topology | Receipt |
|---|---|---|
| `sec-idea-creator` Phase 4 · `sec-novelty-check` Phase C · `sec-research-review` · `sec-experiment-audit` · `sec-auto-review-loop` artifact inputs · `sec-paper-improve-loop` | **fresh-context** — new session, reads artifact paths, never the producer's summary | `accept` (cross-family) after completed positive verdict |
| `sec-research-refine` iterative rounds · `sec-auto-review-loop` objection continuity | **same-session continuity** — reviewer remembers prior objections; inputs stay cold | `accept` per round |

Rules:
- Record the **actual returned model identity** in `.aris/traces/`; never claim cross-family from config alone.
- An unavailable reviewer is `REVIEW_UNAVAILABLE` — a blocking state, never a fabricated PASS.
- Forward invocation reviewer overrides to reviewer-bearing children (`sec-idea-discovery` → `sec-novelty-check`/`sec-research-review`; `sec-research-pipeline` → all stages).

## Backend server

`tools/antigravity-exec/server.py` is the MCP/CLI bridge to the local logged-in `agy` binary. See `tools/antigravity-exec/README.md` for setup; the repo's `.aris/reviewer.example.json` shows the expected project config.
