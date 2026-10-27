# Integration Contract

When one sec-paper skill delegates work to another (or to persistent project
state), the coupling must be **engineered, not assumed**. SKILL.md prose can
*describe* an integration; it cannot *guarantee* one. Every cross-skill
handoff whose silent failure would damage the research result needs all of:

1. **A machine-checkable artifact** — the handoff is a file/record
   (`IDEA_REPORT.md#ranked-ideas`, `EXPERIMENT_PLAN.md`, job `results/`,
   receipts under `.aris/traces/`), not a chat message that evaporates.
2. **An existence + shape check at the receiver** — the consuming stage
   verifies the artifact exists, is non-empty, and carries the expected
   sections/fields before building on it (`_section_has_content`,
   `snapshot()`, manifest field checks).
3. **A deterministic gate where truth can be checked cheaply** —
   `idea_discovery_gate.py` for phase coverage, `evidence_check.py` for
   value-in-source existence, `jobs.py` terminal states for runs,
   `paper_check.py`/`submission_gate.py` for the final bundle.
4. **A failure route** — missing/degraded input names the blocking artifact
   and stops or degrades explicitly (`BLOCKED`, `UNVALIDATED`,
   `REVIEW_UNAVAILABLE`); it never fabricates the missing content.
5. **Version binding for reviewed content** — receipts pin input hashes;
   edited inputs invalidate acceptance (see output-versioning.md).

Historical motivation: assurance-gate bypass and dropped review calls in the
upstream project both traced to prose-only "MUST invoke X" steps that the
executor skipped under context pressure. Prefer one verifiable artifact over
three emphatic sentences.
