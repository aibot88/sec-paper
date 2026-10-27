---
name: "sec-ablation-planner"
description: "Design the ablation matrix for a security paper after main results pass sec-result-to-claim (supported or partial). Covers the four security ablation axes — component deletability, attacker tier (A1→A3), oracle coverage, and target-family diversity — with one moving piece per run. Use when user says \"安全消融\", \"ablation design\", or main results are positive."
argument-hint: "[RESULT_TO_CLAIM.md-or-FINAL_PROPOSAL.md] [— max runs: N]"
---

# Security Ablation Planner (`sec-ablation-planner`)

Design the ablation study for: **$ARGUMENTS**

Follow shared-references/workflow-contract.md. Gemini reviews the ablation matrix against audited claim status; Codex checks feasibility and executes. After the wave, re-audit evidence and re-route claims. Use tools/jobs.py queue/status/wait (owned local backend), never require generic ARIS run/queue Skills.

---

## When to Run

After `sec-result-to-claim` returns `claim_supported` or `partial`. If claims are `contradicted`, the right move is pivot/negative-finding, not ablation.

---

## The Four Security Ablation Axes

ML ablations vary one component. Security papers get attacked on **four** axes — plan runs for each applicable axis, **one moving piece per run, identical targets**:

### Axis 1 — Component Deletability (all tracks)
Disable exactly one harness component per run on identical targets (state snapshot off, structure inference off, custom oracle replaced by generic). Goal: prove every load-bearing component is necessary — the direct answer to "which module is decoration?" The number of runs equals the number of deletable components; components failing this test should have been cut in `sec-research-refine`, so a failure here is a design signal, not a paper detail.

### Axis 2 — Attacker Tier (attack & defense tracks)
- For **detection/defense**: sweep the same evaluation under A1 (static payloads) → A2 (workflow-aware, matched budget) → A3 (adaptive, knows the mechanism). The degradation curve *is* the ablation result — it isolates what the mechanism robustly buys vs. what only holds against ignorant attackers.
- For **attack/discovery**: vary attacker *preconditions* (authentication level, schema visibility, request budget) to map where the attack's boundary actually lies.

### Axis 3 — Oracle Coverage (all tracks)
Vary which oracles are active (e.g., state-diff only vs. + sink detection vs. + patch-SHA check). Reveals blind spots: a finding family that only one oracle catches is both a contribution detail and a limitation statement.

### Axis 4 — Target-Family Diversity (measurement & attack tracks)
Hold the method constant, vary the target corpus: framework family, version era, app size, authentication model. Distinguishes "works on tested targets" from "works where the invariant exists" — this is the evidence for the generality claim.

---

## Workflow

1. **Read** `RESULT_TO_CLAIM.md` (claim status), `FINAL_PROPOSAL.md` (deletability rationale — it predicts which components should survive ablation), and `EXPERIMENT_PLAN.md` Phase 3.
2. **Emit the ablation matrix** into `refine-logs/ABLATION_PLAN.md`:

| Run | Axis | Disabled/Varied | Held Constant | Hypothesis | Oracle + Unit | Budget |
|-----|------|-----------------|---------------|------------|---------------|--------|
| ABL-1 | Component | -state snapshot | all else | reach of deep states drops ≥X% | state-diff, root-cause | identical |

3. **Rules**: one moving piece per run; identical seed state/auth/budget across variants; stochastic variants keep the planned trial count; each run names its hypothesis *before* execution so the result is interpretable either way.
4. **Execution**: run the matrix via bundled tools/jobs.py queue with wave dependencies. Fold results into EXPERIMENT_RESULTS.md, re-audit the new evidence and rerun sec-result-to-claim for every completed wave, not only surprising results.

## Output

`refine-logs/ABLATION_PLAN.md` + updated tracker rows. Ablations that surprise (component removal *doesn't* hurt → decoration; A3 fully bypasses → residual channel finding) get explicitly written into the results narrative — they are findings, not embarrassments.
