---
name: "sec-experiment-bridge"
description: "Workflow S1.5: Bridge between security idea discovery and auto review. Reads EXPERIMENT_PLAN.md, implements the security harness (targets, oracles, A3 probes, baselines), deploys experiments on containerized/local infrastructure, collects oracle-verified results. Use when user says \"实现安全实验\", \"deploy security experiment plan\", or has a refine-logs/EXPERIMENT_PLAN.md ready to execute."
argument-hint: "[EXPERIMENT_PLAN.md-or-chosen-idea] [— code review: true] [— compact: true]"
---

# Workflow S1.5: Security Experiment Bridge (`sec-experiment-bridge`)

> **Reviewer slots**: resolve per ARIS selectable-reviewer contract. The Phase 2.5
> code review is a **fresh-context** reviewer — the implementer never reviews
> its own harness. Same-family results are `provisional`, never `accepted`.

Implement and deploy experiments from plan: **$ARGUMENTS**

---

## Overview

```
sec-idea-discovery output:            This skill:                     sec-auto-review-loop input:
refine-logs/EXPERIMENT_PLAN.md   →   harness impl → sanity →    →   oracle-verified results in
refine-logs/EXPERIMENT_TRACKER.md    deploy → collect → claims        EXPERIMENT_RESULTS.md
refine-logs/FINAL_PROPOSAL.md        route
```

**The defining difference from ML `experiment-bridge`:** the deliverable is not "metrics on a dataset" — it is a **working security harness whose every result line carries a verified oracle and deduplication unit**. A bridge that returns raw alert counts, unverified scanner hits, or state-corrupted runs has failed regardless of how many "findings" it produced.

---

## Constants

- **AUTO_DEPLOY = true** — Deploy after implementation + code review. `false` pauses for human review.
- **CODE_REVIEW = true** — Fresh-context security code review before any deployment.
- **SANITY_FIRST = true** — Run the smallest experiment first to validate environment + oracle wiring.
- **MAX_PARALLEL_RUNS = 4** — Parallel experiment slots; **never** two stateful runs against the same mutable target/DB instance.
- **BASE_REPO = false** — GitHub repo URL to clone as base (e.g., existing scanner/framework to extend).
- **COMPACT = false** — Prefer `idea-stage/IDEA_CANDIDATES.md`; append runs to `EXPERIMENT_LOG.md`.
- **BACKENDS = local | ssh | containers** — Security runs live on local workers, SSH hosts, and container stacks; Vast/Modal GPU paths remain available for model-heavy components but are not the default.
- **AUTHORIZATION = inherited** — Re-read the authorization scope recorded by `sec-idea-discovery` Phase 0 (`local-only` default). A plan whose environment section violates it gets redesigned or `BLOCKED_ETHICS_OR_ENV`, never silently executed.
- **RESCUE_ON_FAILURE = true** — On sanity/deploy failure, run a fresh-agent rescue review before abandoning the plan.

---

## Inputs

1. `refine-logs/EXPERIMENT_PLAN.md` — claim→evidence matrix, RQ blocks, ablation matrix, stats protocol (best input).
2. `refine-logs/EXPERIMENT_TRACKER.md` — run-by-run table to update.
3. `refine-logs/FINAL_PROPOSAL.md` — anchors + mechanism for implementation context.
4. `idea-stage/IDEA_REPORT.md` — fallback, incl. pilot harness descriptions to scale up.

If none exist, ask the user what to implement — do not guess a security experiment.

---

## Workflow

### Phase 1: Parse the Plan & Lock the Environment

Extract from `EXPERIMENT_PLAN.md`:
1. **Run order**: sanity → oracle validation → RQ1 ground-truth effectiveness → RQ2 real-world/discovery → RQ3 A3 adaptive → RQ4 overhead/ablation.
2. **Per experiment block**: target corpus (`app@version`, commit SHA, container image), compared variants/baselines, oracle, experimental unit, budget (requests/time), trial count, MUST-RUN vs NICE-TO-HAVE.
3. **Environment build sheet**: container images, role accounts, seed DB state, crawl specs, network isolation.
4. **Claims source**: create/update `idea-stage/docs/research_contract.md` from `templates/RESEARCH_CONTRACT_TEMPLATE.md` — frozen anchors + the ≤2 falsifiable claims + forbidden-claim seed; `sec-result-to-claim` (Phase 7) and downstream writing read this file.

Present the load summary (milestones, must-run count, wall-clock estimate, authorization scope confirmed).

### Phase 2: Implement the Harness

For each milestone, in run order:

1. **Reuse first**: scan project/`base_repo/` for existing scanners, fuzzers, harnesses, fixtures; extend rather than rewrite.
2. **Build the three load-bearing pieces** (these map to RQ structure):
   - **Target driver**: deployment scripts (Docker Compose / VM / browser context), seed-state loader (role accounts, pre-populated DB, tenant fixtures), teardown/reset between trials.
   - **Oracle module**: implements exactly the declared oracle — state-diff checker, patch-SHA verifier, sink/execution detector, or audited-sample harness. **The oracle must be executable code or a defined manual-audit protocol, never a comment describing intent.**
   - **Dedup module**: groups findings by declared unit (root cause / minimal fix / broken rule / independent origin); emits `raw → deduped` both.
3. **Baselines**: wrap prior tools under identical seed state, auth roles, and budget interface so comparisons share one driver.
4. **A3 harness (defense/detection tracks)**: attacker component that ingests the defense's config/rules/parser and mutates inputs to evade — implement it now, not during the review loop.
5. **Logging discipline**: every run writes `config + target@SHA + oracle verdicts + raw/deduped counts + timing` to machine-readable files (JSON/CSV) under `results/<run_id>/`.
6. **Self-review checklist**: seeds/SHAs pinned? Oracle independent of the tested mechanism? Budget knobs identical across variants? Authorization scope respected? Results parseable?

### Phase 2.5: Fresh-Agent Security Code Review (`CODE_REVIEW = true`)

Send the harness code (paths, not summaries) to a fresh reviewer. In addition to generic correctness, it must audit:

```text
1. Oracle soundness — can the oracle itself be fooled (e.g., reading the same
   state the tool mutates)? Is it truly independent of the mechanism under test?
2. Dedup correctness — does the dedup key collapse distinct root causes or
   inflate one bug into many units?
3. Contamination — do baseline and candidate share mutable state? Are seeds/
   auth/budget actually identical across variants?
4. Authorization boundary — can any code path send mutating traffic outside
   the declared local/consented scope? Flag hard-coded production endpoints.
5. A3 genuineness — does the adaptive attacker actually know the defense
   internals, or is it an A1 payload list wearing an A3 label?
```

Fix all `BLOCKER` findings before deploy; document `MAJOR` mitigations in the tracker.

### Phase 3: Sanity Stage (`SANITY_FIRST = true`)

Run the smallest block end-to-end — typically oracle validation on 1–2 targets:
- Verifies environment build, seed-state loading, oracle firing correctly on a known-positive and known-negative case.
- Up to 3 debug attempts; then `RESCUE_ON_FAILURE` fresh-agent review; then `BLOCKED_ENV` with evidence — never paper over a dead harness.

### Phase 4: Deploy Full Experiments

Auto-route by job count:
- **≤5 jobs** → `/run-experiment` per run.
- **≥10 jobs or wave dependencies** (e.g., A1→A2→A3 tiers, baseline→ablation waves) → `/experiment-queue` with OOM/crash-safe state and wave gating.

> **Standalone note (no ARIS skills installed):** `/run-experiment`,
> `/experiment-queue`, and `/monitor-experiment` are host-provided execution
> primitives. When they are absent, execute the harness commands directly —
> the **contract** is what matters, not the launcher: (a) each run lands in
> `results/<run_id>/` with config + target@SHA + oracle verdicts + timing;
> (b) stateful runs never share a mutable target instance; (c) per-trial
> seeds recorded; (d) budgets enforced and overruns marked
> `UNDERPOWERED_OR_BLIND`.

**Isolation invariants (security-specific, hard rules):**
- Never run two stateful scanners against one mutable DB/app instance concurrently — separate containers, namespaces, or DB clones.
- Reset seed state between trials of stochastic methods; record per-trial seed.
- Rate-limit any component that can emit requests; log total request budget per run.

Track via `/monitor-experiment`; update `EXPERIMENT_TRACKER.md` per run (`status | raw → deduped | oracle verdicts | wall-clock`).

### Phase 5: Collect & Verify Results

1. Parse `results/<run_id>/` into `refine-logs/EXPERIMENT_RESULTS.md` — one section per RQ block.
2. **Mandatory dedup report**: every "finding" table shows `raw alerts → deduped units → oracle-verified TP → FP`. A table missing this breakdown is incomplete.
3. **Statistics protocol check**: stochastic methods must have ≥ the planned trial count; report median + IQR + Mann-Whitney U. Short runs get labeled `existence smoke only`.
4. Timeout/infra failures → `UNDERPOWERED_OR_BLIND` or `BLOCKED_ETHICS_OR_ENV` with partial artifacts preserved.

### Phase 6: Ablation Auto-Plan (when main results support claims)

If RQ1–RQ2 are `SUPPORTED`: invoke `/sec-ablation-planner` to design the four-axis ablation matrix (component deletability / attacker tier / oracle coverage / target family) from `RESULT_TO_CLAIM.md` + `FINAL_PROPOSAL.md`, then execute the wave under the same one-moving-piece and budget-matching rules.

### Phase 7: Result-to-Claim Routing — invoke `/sec-result-to-claim`

Run `/sec-result-to-claim` against `research_contract.md` + `EXPERIMENT_RESULTS.md` to produce `refine-logs/RESULT_TO_CLAIM.md`:

- `claim_supported` → hand off to `/sec-experiment-audit` (pipeline Stage 2.5) then `/sec-auto-review-loop`.
- `partial` → route to the cheapest missing-evidence experiment (supplement, not reframe).
- `contradicted` → check for publishable negative finding; otherwise document pivot and stop — never launder a refuted claim into the paper.

Re-run `/sec-result-to-claim` after every supplementary evidence batch or ablation wave — it is a routing step, not a one-time table.

### Phase 8: Handoff Summary

Report: runs executed, oracle-verified results per RQ, A3 outcome if applicable, claims status, artifacts paths, and the exact command that resumes monitoring. Hand to `/sec-auto-review-loop` only when `EXPERIMENT_RESULTS.md` and `RESULT_TO_CLAIM.md` both exist.
