---
name: "sec-auto-review-loop"
description: "Workflow S2: Autonomous multi-round security review loop — a fresh-context Big-Four reviewer critiques experiments/results, the executor fixes, re-runs, and re-reviews until positive assessment or max rounds. Use when user says \"auto review loop\", \"security review until it passes\", or after sec-experiment-bridge collected results."
argument-hint: "[direction-or-artifacts] [— difficulty: medium|hard|nightmare] [— human checkpoint: true] [— max rounds: N]"
---

# Workflow S2: Security Auto Review Loop (`sec-auto-review-loop`)

> **Reviewer slots**: resolve per the reviewer contract in `shared-references/reviewer-contract.md`. Each review
> final acceptance is fresh-context Gemini reading actual artifacts. Warm
> repair checks may preserve objections, but are explicitly warm and never
> count as final acceptance. Read shared-references/workflow-contract.md.

Run an autonomous review-fix loop for: **$ARGUMENTS**

---

## Overview

```
EXPERIMENT_RESULTS.md ─┐
RESULT_TO_CLAIM.md     ├─→ Round N: reviewer scores → executor fixes → re-run → re-review
harness + results/     ┘         until STOP or MAX_ROUNDS
```

Security-adapted from auto-review-loop: five hard gates make this more than a score loop. No STOP while any hard gate fails, regardless of numeric score.

---

## Constants

- **MAX_ROUNDS = 4**
- **STOP_SCORE = 6/10** — Minimum calibrated score for autonomous stop (same bar as upstream).
- **HUMAN_CHECKPOINT = false** — `true` pauses after each review for user direction.
- **REVIEWER_DIFFICULTY = medium** — `medium`: standard review. `hard`: + reviewer memory of prior weaknesses + debate protocol. `nightmare`: reviewer reads the repo/results directly + memory + debate.
- **MAX_FIX_EXPERIMENTS_PER_ROUND = 3** — A round may schedule at most 3 supplementary experiments; bigger gaps route back to `sec-experiment-plan` instead of patch-looping.
- **RESUMABLE = true** — Mandatory review-stage/REVIEW_STATE.json and append-only ACQUITTAL_LOG.jsonl, plus .aris/runs state. Persist the fields and recovery rules in shared-references/workflow-contract.md after every phase boundary; missing evidence blocks acceptance.

---

## Hard Gates (score-independent)

A `STOP` verdict is invalid while any hard gate is red:

- [ ] **Threat-model gate**: every experiment respects the frozen anchor; any capability used in eval that the threat model excludes is either removed or explicitly labeled out-of-model stress test.
- [ ] **Oracle gate**: every reported finding carries oracle-verified TP/FP; zero results rely on HTTP-status, scanner-consensus, coverage, or stack-hash counting.
- [ ] **A3 gate** (defense/detection tracks): an adaptive-attacker evaluation exists and its degradation is reported honestly — "no A3 test" is never a passing state.
- [ ] **Ethics gate**: no unconsented live-system traffic anywhere in `results/`; authorization scope violations → immediate `BLOCK`, not a fix round.
- [ ] **Pinned-artifacts gate**: versions, `CVE-YYYY-NNNNN`, 40-char SHAs resolvable for every target and baseline.

Soft dimensions scored 1–10 per round: mechanism clarity (deletability), baseline fairness (matched budgets), statistical soundness (trials/IQR/tests), characterization honesty (failure regimes stated), novelty delta vs closest work.

---

## Workflow

### Phase 0: Assemble the Review Pack

Pass **paths** to the reviewer:
`refine-logs/FINAL_PROPOSAL.md` (anchors) · `refine-logs/EXPERIMENT_PLAN.md` (claims→evidence) · `refine-logs/EXPERIMENT_RESULTS.md` · `refine-logs/RESULT_TO_CLAIM.md` · `results/` raw logs · harness diff (`git diff` or file list).

### Phase 1: Review Round

Dispatch the resolved reviewer with the security rubric:

```text
Act as a senior PC member for IEEE S&P / USENIX Security / ACM CCS / NDSS
reviewing a complete results package. Read the listed files directly.

Check the five HARD GATES first (threat-model fidelity, oracle soundness,
A3 presence for defenses, ethics scope, pinned artifacts). A failure on any
hard gate makes this round FAIL regardless of score — say so explicitly and
name the violating artifact and line.

Then score 1-10 on: mechanism clarity & deletability, baseline fairness
(matched seed/auth/budget), statistical soundness (trial count, IQR,
Mann-Whitney U where stochastic), characterization honesty, and the
verifiable novelty delta over closest prior work.

Return: hard-gate table (PASS/FAIL + evidence), overall score X/10,
verdict (STOP | CONTINUE), ranked weaknesses (FATAL/MAJOR/MINOR), and for
each the cheapest discriminating fix — bounded to at most
MAX_FIX_EXPERIMENTS_PER_ROUND new experiments.
```

### Phase 2: Fix Round

Executor implements the fixes in weakness order:
- FATAL/hard-gate failures first — these are never optional.
- Supplementary experiments go through bundled jobs.py with oracle and dedup intact. Persist pending job IDs and resume those jobs, never duplicate a running experiment. Update tracker/results, then rerun sec-experiment-audit and sec-result-to-claim on the NEW snapshot before re-review. Old acceptances do not apply to new evidence.
- If a weakness demands reframing the claim (e.g., narrower threat model), log it as an explicit **claim-migration entry** in `RESULT_TO_CLAIM.md` — never edit results to fit the old claim.
- `HUMAN_CHECKPOINT = true`: after presenting the review + planned fixes, end turn and wait.

### Phase 3: Re-Review & Iterate

Warm repair checks may use review.py --continue-from, preserving objections. Before STOP obtain a NEW-session Gemini verdict on the final audited results/claims; only this fresh positive receipt accepts the phase. Append actual raw trace and receipt to ACQUITTAL_LOG and persist REVIEW_STATE. Repeat until:
- `STOP` with all hard gates green and score ≥ `STOP_SCORE` → write verdict, exit.
- `MAX_ROUNDS` reached → write the final assessment **with unresolved weaknesses listed** — never report a timed-out loop as "passed".
- The same weakness recurs for 2 consecutive rounds → escalate to `pivot` recommendation instead of a fifth identical fix.

### Phase 4: Output

Write `review-stage/SEC_AUTO_REVIEW.md`:
- Per-round: hard-gate table, score, weaknesses, fixes applied, new results.
- Final: verdict (`STOP`/`MAX_ROUNDS`), claim status after all rounds, claim-migration log, remaining limitations for the paper's Discussion section, and the figure/table inventory the results now support.

An unsuccessful loop may hand off an honest research STATUS report, not validated writing. Submission assurance remains BLOCKED after MAX_ROUNDS, pivot, unavailable review, unresolved hard gates or stale evidence. A positive final receipt plus current claims routing is required for validated writing.
