---
name: "sec-experiment-audit"
description: "Independent integrity audit of security experiment EVIDENCE (not code) before results become paper claims. A fresh-context reviewer checks oracle firing, ground-truth independence, dedup honesty, phantom results, authorization compliance, and scope sufficiency. Use after sec-experiment-bridge collects results, before sec-auto-review-loop or any claim writing."
argument-hint: "[results-path-or-EXPERIMENT_RESULTS.md]"
---

# Security Experiment Integrity Audit (`sec-experiment-audit`)

> **Reviewer slot**: resolve per ARIS selectable-reviewer contract — **fresh
> context, reads artifacts directly** (result files, logs, oracle outputs,
> tracker rows), never the executor's summary. Under the configured
> AntiGravity/Gemini route this is a cross-family review; receipt = `accept`.

Audit experiment evidence integrity for: **$ARGUMENTS**

---

## Why This Is a Separate Step

`sec-experiment-bridge` Phase 2.5 reviews *code before it runs*. This skill audits *evidence after it runs* — the two failure sets barely overlap. A perfectly reviewed harness can still produce:

- **Phantom results**: numbers in `EXPERIMENT_RESULTS.md` with no corresponding run directory, truncated log, or mismatched target SHA;
- **Fake ground truth**: oracle "verdicts" copied from the tool's own output field instead of an independent check;
- **Silent oracle bypass**: the oracle module exists but logged zero invocations — every TP was labeled by heuristics;
- **Dedup fraud**: deduplicated count *exceeding* raw count, or the dedup key trivially equal to "one alert = one bug";
- **Scope inflation**: evaluation on 2 apps claimed as generality over "modern web frameworks";
- **Authorization leakage**: result logs containing traffic to hosts outside the declared scope.

Code review sees none of this; only artifact auditing does.

---

## Workflow

### Phase 0: Assemble the Audit Pack

Pass paths to the fresh reviewer:
`refine-logs/EXPERIMENT_RESULTS.md` · `refine-logs/EXPERIMENT_TRACKER.md` · `results/<run_id>/` directories · oracle module outputs · dedup outputs · `idea-stage/docs/research_contract.md` (claims source) · authorization scope recorded in Phase 0 of the pipeline.

### Phase 1: Evidence Audit (fresh reviewer)

```text
Audit this security experiment results package. You did not run these
experiments. Read the artifacts directly and check:

1. Traceability (phantom results): every headline number in
   EXPERIMENT_RESULTS.md must trace to a results/<run_id>/ directory with
   matching config, target@SHA, and non-truncated logs. Flag any number
   whose only source is the summary file itself.
2. Oracle independence (fake ground truth): for each claim's oracle,
   locate the artifact where it actually fired (state-diff output, patch
   SHA diff, sink detection log, audit sheet). If "ground truth" rows are
   identical to the tool's own alert labels, the oracle was bypassed —
   that is FATAL.
3. Dedup honesty: verify deduped_count <= raw_count for every table, and
   that the dedup key (root cause / minimal fix / broken rule / origin) is
   what the plan declared. Flag "unique crash/hash" style counting.
4. Statistical protocol: stochastic methods show >= planned trials,
   median + IQR, and the declared test. A single run labeled as comparative
   evidence is a violation; existence-smoke labeling is acceptable.
5. Authorization compliance: scan run logs for any destination outside
   the declared scope (production endpoints, third-party IPs, mutated
   remote state). Any hit is an immediate BLOCK, not a fix item.
6. Scope sufficiency: does the target corpus actually cover what the
   claim asserts (frameworks, versions, threat preconditions)? Flag
   claims whose generality exceeds the tested corpus.
7. A3 genuineness (defense/detection): does the adaptive-attacker run
   input actually encode knowledge of the defense (its rules/thresholds/
   parser), with observable evasion attempts in logs — or is it a static
   payload replay?

Return a per-check verdict (PASS / FAIL / INSUFFICIENT-EVIDENCE) with the
artifact path+line for each FAIL, then an overall gate: AUDIT_PASS /
AUDIT_FAIL (list of blocking findings).
```

### Phase 2: Verdict Routing

- **`AUDIT_PASS`** → proceed to `/sec-auto-review-loop` (or downstream claim use); record the audit trace path in `RESULT_TO_CLAIM.md`.
- **`AUDIT_FAIL`** → blocking findings go back to `sec-experiment-bridge` as *evidence fixes* (re-run with correct oracle wiring, restore missing logs, re-dedup), not prose edits. Re-audit after fix.
- **Authorization violation** → stop the pipeline, surface to the user immediately; this is a policy event, not a technical bug.

### Phase 3: Output

Write `review-stage/EXPERIMENT_AUDIT.md`: per-check verdicts with artifact citations, blocking findings, and the final gate decision. This file is cited by `SEC_AUTO_REVIEW.md` and by the paper's artifact appendix.
