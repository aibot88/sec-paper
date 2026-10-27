# Score Calibration Anchors (security track)

Anchored 1–10 scale for `sec-research-refine`, `sec-research-review` and the
score gate inside `sec-auto-review-loop`. Anchors prevent score drift across
rounds and reviewers.

- **9–10 (accept)**: the trust-boundary story is stated in one sentence; every
  mechanism is deletable-justified; oracles are independent of the mechanism;
  an A3 (adaptive) attacker is modeled or its non-applicability argued;
  pilot/statistics plan has a justified budget; ethics/disclosure path named.
  No hand-waved "strong defense" / "novel" claims.
- **7–8 (revise, minor)**: sound mechanism, but one or more of: oracle depends
  on the evaluated component, threat preconditions implicit, matched-budget
  baseline missing, ablation axes incomplete. Fixes are local.
- **5–6 (revise, major)**: the broken invariant is identified but the mechanism
  only re-labels the problem; evaluation plan measures the wrong unit;
  attacker tier stuck at A1; pilot is smoke-only yet claims comparative
  results.
- **3–4 (revise, deep)**: no explicit security property or trust boundary;
  oracle is self-reported by the attacker-side code; plan requires unavailable
  resources presented as available; prior art unaddressed.
- **1–2 (block)**: fabricated evidence, illegal target scope, reviewer-visible
  placeholder content, or mechanism that cannot fail (unfalsifiable).

Reviewer prompts should cite the anchor numbers; a score outside ±1 of the
anchor description must name which element justifies the deviation. An
element not evaluable from the provided inputs is a finding, not a skipped
dimension.
