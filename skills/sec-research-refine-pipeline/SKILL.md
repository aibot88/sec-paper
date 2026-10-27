---
name: "sec-research-refine-pipeline"
description: "One-shot pipeline chaining sec-research-refine (threat-model-anchored method refinement) and sec-experiment-plan (oracle-first, A3-aware experiment roadmap). Use when the user wants the full method+experiment package in one run, or asks to \"串起来\" the security refinement chain."
argument-hint: "[security-problem | rough-approach] [— venue: USENIX_SEC | IEEE_SP | ACM_CCS | NDSS]"
---

# Security Refine Pipeline: Method + Experiment Planning in One Pass (`sec-research-refine-pipeline`)

Refine and concretize: **$ARGUMENTS**

---

## Overview

Use this skill when the user does not want to stop at a refined security method. It composes two sibling skills in order:

1. `sec-research-refine` — stabilize the threat-model-anchored mechanism through iterative reviewer rounds.
2. `sec-experiment-plan` — turn the stable mechanism into a claim-driven, oracle-first, A3-aware experiment roadmap.

**Core rule:** never plan a large experiment suite on top of an unstable mechanism or a drifting threat model. Stabilize the thesis and its anchors first; then derive experiments from the *final* claims (including any logged claim-migration), never from the pre-refinement sketch.

For stage-specific detail, read the sibling skills only when needed:
- `../sec-research-refine/SKILL.md`
- `../sec-experiment-plan/SKILL.md`

---

## Default Outputs

- `refine-logs/FINAL_PROPOSAL.md`
- `refine-logs/REVIEW_SUMMARY.md`
- `refine-logs/REFINEMENT_REPORT.md`
- `refine-logs/EXPERIMENT_PLAN.md`
- `refine-logs/EXPERIMENT_TRACKER.md`
- `refine-logs/PIPELINE_SUMMARY.md`

---

## Workflow

### Phase 0: Triage the Starting Point

- Extract the security problem, rough approach, threat-model context, authorization constraints, and target venue.
- If `refine-logs/FINAL_PROPOSAL.md` exists and still matches the request, reuse it and jump to Phase 2.
- If missing, stale, or materially different, run the full refinement stage. When in doubt, re-run `sec-research-refine` — planning experiments for the wrong threat model is the most expensive mistake in this pipeline.

### Phase 1: Method Refinement Stage

Run `sec-research-refine` with its contract intact:
- Freeze both anchors (Security Problem Anchor + Threat-Model Anchor).
- Enforce deletability on every component; reject "Unified A+B+C" stitching.
- Record any claim-migration explicitly.

Exit this stage only when these are explicit:
- the final mechanism thesis and its classic-primitive mapping (if any);
- the dominant contribution;
- the complexity deliberately rejected;
- the ≤2 core claims and must-run ablations;
- the final threat preconditions (post-migration);
- the remaining risks.

If the last verdict is still `REVISE`, proceed only with weaknesses clearly documented in `REFINEMENT_REPORT.md`.

### Phase 2: Experiment Planning Stage

Run `sec-experiment-plan` on `FINAL_PROPOSAL.md`:
- Claims → evidence matrix with declared oracles and experimental units;
- RQ1–RQ4 blocks incl. mandatory A3 adaptive-attacker evaluation for defense/detection;
- Ablation matrix (one moving piece), budget-matching table, statistics protocol (≥10 trials for stochastic methods);
- Ethics/environment/disclosure checkpoints;
- Run order + `EXPERIMENT_TRACKER.md` + artifact script mapping.

### Phase 3: Pipeline Summary

Write `refine-logs/PIPELINE_SUMMARY.md`:

```markdown
# Security Refine Pipeline Summary
- Final mechanism thesis: [1 sentence + primitive mapping]
- Threat model (final): [adversary class, privileges, scope, TCB]
- Dominant contribution: [...]
- Core claims: [C1, C2] (+ claim-migration log if any)
- Experiment run order: [RQ sequence with oracles]
- First command to run: [exact harness invocation]
- Biggest remaining risk: [...]
- Venue target & open-science notes: [...]
```
