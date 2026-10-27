# Security Research Contract Template (`idea-stage/docs/research_contract.md`)

The claims source of truth for the whole pipeline. Created by `sec-experiment-bridge` Phase 1 (if absent), read by `sec-result-to-claim`, `sec-experiment-audit`, `sec-auto-review-loop`, and `sec-paper-writing`. **Claims here are falsifiable statements — ambitions and descriptions are not claims.**

---

## Frozen Anchors

**Security Problem Anchor** (verbatim from `FINAL_PROPOSAL.md`):
> [Broken/enforced invariant · trust boundary · must-solve bottleneck · non-goals]

**Threat-Model Anchor** (verbatim):
> Adversary class: [W1–W6] · Starting privileges: [...] · In scope: [...] · Out of scope: [...] · TCB: [...] · Authorization: [local-only / consented-scope]

## Core Claims (≤2)

| # | Falsifiable Claim (Under T, M enforces/breaks P with effect E) | Required Evidence (from EXPERIMENT_PLAN) | Oracle | Unit | Baseline (matched budget) |
|---|--------------------------------------------------------------|------------------------------------------|--------|------|---------------------------|
| C1 | ... | RQ1 + RQ2 | [state-diff / patch-SHA / sink / audited sample] | [root cause / broken rule / origin] | [tool @ version @ SHA] |

## Claim-Migration Log (append-only)

| Date | Original Claim | Revised Claim / Precondition | Reason | Approved By (review verdict / user) |
|------|----------------|------------------------------|--------|--------------------------------------|

## Forbidden-Claim Seed (for FACT_PACK + writing gate)

- [ ] No unbounded "novel/first" claims until novelty lock
- [ ] No unbounded FP claims — scope-bounded rewrites only
- [ ] No comparative claims from single short runs
- [ ] No "unified framework" phrasing for coupled mechanisms
