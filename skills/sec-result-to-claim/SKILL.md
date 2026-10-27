---
name: "sec-result-to-claim"
description: "Judge what security claims the experiment evidence actually supports, what it doesn't, and what's missing — then route to confirm / supplement / pivot / negative-finding. Standalone version of the routing embedded in sec-experiment-bridge; rerun after every review-loop fix round or new evidence batch."
argument-hint: "[RESULT_TO_CLAIM.md-or-results-path]"
---

# Security Result-to-Claim Routing (`sec-result-to-claim`)

Route experimental evidence to claim status for: **$ARGUMENTS**

---

## Inputs

- `idea-stage/docs/research_contract.md` — the ≤2 falsifiable core claims + frozen anchors (created by `sec-experiment-bridge` Phase 1).
- `refine-logs/EXPERIMENT_PLAN.md` — the claim→evidence matrix (what each claim *requires*).
- `refine-logs/EXPERIMENT_RESULTS.md` + `results/` — what was *observed*.
- `review-stage/EXPERIMENT_AUDIT.md` — if present, only `AUDIT_PASS` evidence is admissible.

---

## Routing Table (write/update `refine-logs/RESULT_TO_CLAIM.md`)

| Core Claim | Required Evidence | Observed (oracle-verified) | Status | Next Action |
|---|---|---|---|---|
| C1 | RQ1+RQ2 | ... | `claim_supported` / `partial` / `contradicted` | confirm / supplement / pivot |

**Status semantics:**
- **`claim_supported`**: required evidence present, oracle-verified, audit-clean → proceed to review loop / writing.
- **`partial`**: mechanism shown but evidence incomplete (missing A3 run, ablation pending, corpus narrower than claim) → route to the *cheapest missing-evidence experiment*. Do not narrow the claim silently — if narrowing is the right answer, log a claim-migration entry (`original → revised → justification`).
- **`contradicted`**: controlled evidence falsifies the claim → two honest exits only: (a) publishable negative/diagnostic finding (document and keep), or (b) pivot recommendation. **Never** launder a refuted claim into the pipeline.

**Security-specific status annotations:**
- `oracle_gap` — the claim may hold but no valid oracle was ever built; routes to harness work, not writing.
- `a3_pending` — defense/detection claim cannot reach `claim_supported` before the adaptive-attacker block runs.
- `scope_mismatch` — evidence collected under different preconditions than the claim's threat model; mark for migration or redesign.

---

## Re-run Triggers

Re-run this routing (not just on bridge completion) whenever:
- a review-loop fix round adds new experiment results;
- an ablation wave finishes (results may change `partial → supported` or expose a new `contradicted`);
- the threat model was migrated — re-check every claim against the *new* preconditions, not the old ones.

## Output

Updated `refine-logs/RESULT_TO_CLAIM.md` + a one-paragraph routing summary naming: each claim's status, the next cheapest discriminating action for non-supported claims, and which candidates become the paper's contributions.
