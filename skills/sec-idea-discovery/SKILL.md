---
name: "sec-idea-discovery"
description: "Workflow S1: Full security idea discovery pipeline — from a broad Web/systems-security direction to validated, pilot-tested, refined ideas with an experiment roadmap. Chains sec-research-lit → sec-idea-creator → sec-novelty-check → sec-research-review → sec-research-refine-pipeline. Use when user says \"网安全流程找idea\", \"security idea discovery pipeline\", \"从方向到选题全跑完\"."
argument-hint: "[security-direction] [— ref paper: <path-or-url>] [— auto proceed: false] [— compact: true]"
---

# Workflow S1: Security Idea Discovery Pipeline (`sec-idea-discovery`)

> **Before each reviewer slot**, follow the reviewer contract in `shared-references/reviewer-contract.md`:
> resolve invocation → `.aris/reviewer.json` → host default with
> `reviewer_route.py`. Save the route and actual returned identity; unavailable
> selections are `REVIEW_UNAVAILABLE`. `sec-novelty-check` and
> `sec-research-review` are the two **reviewer-bearing phases** — classify
> acceptance from actual model families (same-family = provisional only).

Orchestrate the complete security idea discovery workflow for: **$ARGUMENTS**

---

## Overview

```
/sec-research-lit → /sec-idea-creator → /sec-novelty-check → /sec-research-review → /sec-research-refine-pipeline
  (spec+paper        (brainstorm +        (root-cause       (Big-Four PC          (anchored method +
   landscape)         oracle pilots)       novelty verdict)   adversarial review)   experiment roadmap)
```

Final deliverables:
- `idea-stage/IDEA_REPORT.md` — validated report with ranked, oracle-piloted security candidates;
- `refine-logs/FINAL_PROPOSAL.md` — threat-model-anchored proposal for the top idea;
- `refine-logs/EXPERIMENT_PLAN.md` — claim-driven, A3-aware experiment roadmap.

---

## Constants

- **PILOT_MAX_WALLCLOCK_HOURS = 4** — Skip any single pilot estimated beyond this; flag as `BLOCKED_ENV` and record `DEFERRED_BUDGET`. (Security pilots run on CPU/containers/browser harnesses — no GPU requirement. Override upward for fuzzing-style campaigns that legitimately need ≥24h.)
- **PILOT_TIMEOUT_HOURS = 6** — Hard kill; collect partial artifacts and record `UNDERPOWERED_OR_BLIND`, never a fabricated negative.
- **MAX_PILOT_IDEAS = 3** — Parallel pilots at most; extra feasible ideas recorded `DEFERRED_BUDGET`.
- **MAX_TOTAL_COMPUTE_HOURS = 12** — Total container/worker wall-clock budget across pilots.
- **AUTO_PROCEED = true** — Checkpoints are informational; continue in the same turn. `false` = ask and end turn.
- **COMPACT = false** — Also write `idea-stage/IDEA_CANDIDATES.md` short-form candidate list.
- **OUTPUT_DIR = `idea-stage/`** — All idea-stage artifacts.
- **REF_PAPER = false** — Optional local PDF / URL to seed idea generation.
- **RENDER_HTML = true** — Render `IDEA_REPORT.md` via `/render-html --no-review` at the end.
- **RESUMABLE = true** — Stage evidence under `.aris/runs/<run_id>.json` + deterministic gate before declaring completion.
- **AUTHORIZATION = `local-only`** — Default stance: pilots only on owned/local/containerized targets. `consented-scope` allows explicitly authorized external targets documented in Phase 0.

> Override via argument: `/sec-idea-discovery "multi-tenant GraphQL BOLA" — authorization: local-only, auto proceed: false`.

---

## Checkpoint Execution Rule (identical to `/idea-discovery`)

Resolve `AUTO_PROCEED` once before Phase 0 and keep it for the whole run.

- **`true` (non-blocking):** a checkpoint is a progress update — state the result and the auto-selected next action, continue **in the same turn**. Never "ask, then continue if no response": once a turn ends, silence cannot resume the workflow.
- **`false` (blocking):** present options, ask, end turn; resume only on explicit reply.

---

## Per-Stage Evidence Gate (`RESUMABLE = true`)

Resolve `run_state.py` and `idea_discovery_gate.py` in this order:
1. `<sec-paper-repo>/tools/run_state.py` (vendored copy — this repo ships it)
2. `tools/run_state.py` in the project directory
3. `tools/run_state.py` under a configured ARIS repo, if present

Same order for `idea_discovery_gate.py` (the vendored edition defaults to
the `sec-*` stage names and accepts `--phases`/`--review-phases` overrides).
If neither helper is resolvable the final report is `BLOCKED` — never
silently continue without a state record.

For a new run, derive `<run_id>` from direction slug + date, then start the ordered record with `--executor <actual-model> --provisional-advances`:

```text
sec-research-lit,sec-idea-creator,sec-novelty-check,sec-research-review,sec-research-refine-pipeline
```

Artifact locators (the gate checks the canonical report, not scratch files):

| Phase | Artifact locator |
|---|---|
| `sec-research-lit` | `idea-stage/IDEA_REPORT.md#literature-landscape` |
| `sec-idea-creator` | `idea-stage/IDEA_REPORT.md#ranked-ideas` |
| `sec-novelty-check` | `idea-stage/IDEA_REPORT.md#novelty-verification` |
| `sec-research-review` | `idea-stage/IDEA_REPORT.md#external-critical-review` |
| `sec-research-refine-pipeline` | `refine-logs/FINAL_PROPOSAL.md` |

The two **reviewer-bearing phases** require review receipts after `done`:
- Same-family reviewer → `mark-provisional` with actual reviewer model + verdict/trace id.
- Verified different-family reviewer (e.g., Claude/Gemini reviewing a Codex run) → `accept` with real identity.
- `sec-novelty-check`: `PROCEED` and `PROCEED WITH CAUTION` are positive; `ABANDON` is negative — no receipt, pick the next surviving candidate and re-run the phase.
- Never invent ids; never mark provisional without the positive verdict in hand.

At the end run:

```text
python3 <resolved-idea_discovery_gate.py> . <run_id> --report idea-stage/IDEA_REPORT.md
```

(The vendored gate already defaults to the `sec-*` phase list; pass
`--phases`/`--review-phases` only for a differently-named chain.)

On non-zero exit the gate writes `BLOCKED: <stage> evidence missing` — do not present the workflow as complete. On `— resume <run_id>`, start from the first non-terminal phase and re-run the gate.

---

## Pipeline

### Phase 0: Load Research Constraints & Authorization Context

1. Read `RESEARCH_BRIEF.md` (or the brief path in `$ARGUMENTS`): target domain, venue goal, budget, timeline.
2. **Extract authorization scope explicitly** (security addition — this replaces generic "compute constraints"):
   - Allowed targets: local containers / open-source apps / owned infrastructure / documented consented scope.
   - Forbidden during pilots: unconsented production traffic, real user data, state-mutating requests to third-party services.
3. If `REF_PAPER` is set, summarize it now (mechanism, threat model, oracle, limitations) and use it as generation context.
4. Initialize `idea-stage/` and the run state.

### Phase 1: Literature & Specification Landscape — `/sec-research-lit`

```text
/sec-research-lit "<direction>" — composed: idea-stage/IDEA_REPORT.md
```

Requires the output to contain: mechanism-decomposed neighbor map, assumption friction matrix, genuine-vs-fake gap table, verified BibTeX/RFC/CVE anchors. Gate: `#literature-landscape` non-empty in `IDEA_REPORT.md`.

### Phase 2: Candidate Generation + Oracle Pilots — `/sec-idea-creator`

```text
/sec-idea-creator "<direction>" — context: Phase 1 landscape, authorization scope from Phase 0
```

Enforce the sec contract: 8–12 candidates across Attack/Defense/Measurement tracks → Phase-3 three-way status gate (`FEASIBLE_NOW` / `EXPERIMENT_BLOCKED` / `HYPOTHESIS_REFUTED_OR_DUPLICATE`) → fresh-thread triage shortlist → Phase-5 pilots via `/run-experiment` + `/monitor-experiment` under the locked pilot contract (oracle, dedup unit, matched budget) → four-state verdicts + evidence re-ranking.

Checkpoint (per `AUTO_PROCEED`): report pilot verdict table + re-ranked candidates. Gate: `#ranked-ideas` present with verdicts.

### Phase 3: Root-Cause Novelty — `/sec-novelty-check`

```text
/sec-novelty-check "<top candidate claim set>" — composed: idea-stage/IDEA_REPORT.md
```

Run on the top-ranked `SUPPORTED` candidate (or the highest-ranked candidate if none piloted cleanly). Verify mechanism + trust-boundary novelty against Big-Four proceedings, RFCs, advisories. Record the review receipt (`accept`/`mark-provisional`) per the run-state contract. On `ABANDON`: take the next surviving candidate and re-run — do not proceed to Phase 4 with an `ABANDON` verdict.

### Phase 4: Big-Four Adversarial Review — `/sec-research-review`

```text
/sec-research-review "idea-stage/IDEA_REPORT.md (+ pilot artifacts)" — composed: idea-stage/IDEA_REPORT.md
```

Pass **file paths**, not summaries. The reviewer audits threat-model sanity, deletability, oracle validity, A3 resilience, ethics. Record the receipt. If the review's fatal objection is resolvable by an explicit claim/threat-model revision, run Step 3 of `sec-research-review` (same-session ruling) and log the migration.

### Phase 5: Anchored Refinement + Experiment Plan — `/sec-research-refine-pipeline`

```text
/sec-research-refine-pipeline "<top candidate problem | approach> — venue: <target>"
```

Chains `sec-research-refine` (anchors + deletability + iterative reviewer rounds → `FINAL_PROPOSAL.md`) and `sec-experiment-plan` (claims→evidence matrix, RQ1–RQ4 with A3, ablation matrix, statistics protocol, ethics checkpoints → `EXPERIMENT_PLAN.md` + `EXPERIMENT_TRACKER.md` + `PIPELINE_SUMMARY.md`).

Gate: `refine-logs/FINAL_PROPOSAL.md` exists. Then run the final `idea_discovery_gate.py`.

### Phase 6: Final Report & Optional Render

1. Ensure `idea-stage/IDEA_REPORT.md` contains all five anchored sections plus the security additions:
   - `## Literature Landscape` (#literature-landscape)
   - `## Ranked Ideas` (#ranked-ideas) — with pilot verdicts + re-ranking
   - `## Novelty Verification` (#novelty-verification)
   - `## External Critical Review` (#external-critical-review)
   - `## Recommended Next Steps` — pointer to `refine-logs/` artifacts
   - `## Forbidden-Claim & Ethics Seed` — disclosure trigger, forbidden claims
   - `## Dead-End & Blocked Register` — REFUTED / BLOCKED / DEFERRED candidates with exact reasons (anti-repetition memory)
2. If `research-wiki/` exists, upsert recommended + archived candidates.
3. If `RENDER_HTML` and `/render-html` is available, run `/render-html idea-stage/IDEA_REPORT.md --no-review`; otherwise skip silently (rendering is cosmetic).
4. Final checkpoint message: top candidate, threat model, pilot verdict, novelty verdict, review verdict, first experiment command.
