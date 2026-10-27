---
name: "sec-research-pipeline"
description: "Workflow S0: Full end-to-end security research pipeline — broad direction → idea discovery → experiment bridge → auto review loop → narrative summary → optional paper writing. Use when user says \"网安全流程\", \"从找idea到投稿\", \"security end-to-end research\", or wants the complete autonomous security research lifecycle."
argument-hint: "[security-direction] [— auto proceed: false] [— auto write: true] [— venue: USENIX_SEC|IEEE_SP|ACM_CCS|NDSS] [— authorization: local-only]"
---

# Full Security Research Pipeline: Direction → Experiments → Submission (`sec-research-pipeline`)

> **Reviewer slots**: resolve per the reviewer contract in `shared-references/reviewer-contract.md` throughout;
> forward invocation reviewer/model/effort overrides to reviewer-bearing
> children. Codex generates/executes; only AntiGravity/Gemini reviews.
> Follow shared-references/workflow-contract.md for owned tools, phase kinds,
> parent/child run IDs, receipt freshness and final submission assurance.

End-to-end autonomous security research workflow for: **$ARGUMENTS**

---

## Overview

```
/sec-idea-discovery → /sec-experiment-bridge → /sec-experiment-audit → /sec-auto-review-loop → summary → /sec-paper-writing (optional)
├─ Workflow S1 ──────┤├─ Workflow S1.5 ────────┤├─ evidence gate ──────┤├── Workflow S2 ───────┤           ├── W3 ────────────┤
```

Owned support: sec-result-to-claim, sec-ablation-planner, sec-paper-audit, tools/jobs.py, review.py, paper_check.py and submission_gate.py. Rendering is optional; no ARIS launcher/writer/auditor is a runtime requirement.

---

## Constants

- **AUTO_PROCEED = true** — Checkpoints informational; `false` blocks at gates.
- **HUMAN_CHECKPOINT = false** — Passed to `/sec-auto-review-loop` (pause after each round).
- **REVIEWER_DIFFICULTY = medium** — `medium | hard | nightmare`, passed to `/sec-auto-review-loop`.
- **CODE_REVIEW = true** — Fresh-context security code review before deploy, passed to `/sec-experiment-bridge`.
- **BASE_REPO = false** — Optional repo URL to build the harness on.
- **COMPACT = false** — Compact candidate/result files for short-context sessions.
- **AUTO_WRITE = false** — `true` auto-invokes `/sec-paper-writing` after Stage 4. Missing venue defers writing; never blocks Stages 1–4.
- **VENUE = (unset)** — `USENIX_SEC | IEEE_SP | ACM_CCS | NDSS | PETS | ACSAC`. Bound only when Stage 5 begins; never guessed.
- **RENDER_HTML = true** — Render `NARRATIVE_REPORT.md` via `/render-html --no-review` at Stage 4.
- **AUTHORIZATION = `local-only`** — Inherited by every stage. `consented-scope` requires the documented scope to be re-stated in each stage's environment section.
- **RESUMABLE = true** — Per-stage state under `.aris/runs/<run_id>`; resume from first non-terminal stage.

> Override: `/sec-research-pipeline "direction" — AUTO_PROCEED: false, venue: USENIX_SEC, authorization: local-only`.

## Checkpoint Execution Rule

Identical to `/sec-idea-discovery`: resolve `AUTO_PROCEED` once, keep for the whole pipeline; `true` = report-and-continue in the same turn, `false` = ask-and-end-turn. Never "ask then continue on silence".

## Resumable Runs

Resolve this repository from .aris/sec-paper.json or the real installed Skill path. All helpers are owned under tools/; unresolved tools block, never require ARIS. Use a unique outer ID and a different <outer>-ideas child ID. Stage list:

```text
sec-idea-discovery,sec-experiment-bridge,sec-experiment-audit,sec-auto-review-loop,summary,sec-paper-writing
```

| Stage | Terminal record |
|---|---|
| `sec-idea-discovery` | child gate PASS + fresh aggregate Gemini receipt -> accepted |
| `sec-experiment-bridge` | execution-only done + nonempty results; semantic evidence audit is separate |
| `sec-experiment-audit` | `AUDIT_PASS` verdict with trace → `accepted`; `AUDIT_FAIL` keeps the stage open |
| `sec-auto-review-loop` | fresh Gemini STOP with all gates green -> accepted; MAX_ROUNDS does not pass |
| `summary` | execution-only done + nonempty narrative/fact pack; no scientific acceptance inferred |
| `sec-paper-writing` | submission_gate PASS + final Gemini aggregate receipt; skipped only if AUTO_WRITE=false |

---

## Pipeline

### Stage 0: Initialize

1. Run tools/project.py init and doctor --live for the target project, record capability/resource checks and .aris/context.json. Create run state with actual Codex identity and --auto-write only if requested. Missing owned state tools or reviewer blocks, never warn-and-skip.
2. Extract direction, authorization scope, venue hint, and any `RESEARCH_BRIEF.md`.
3. Record the authorization scope where every downstream stage can read it — it is a **pipeline-wide invariant**, not per-stage decoration.
4. Register the run with `tools/watchdog.py --register '{"name":"<run>","type":"loop","state_file":".aris/runs/<run>.json","stale_after_seconds":1800}'` (loop tasks require state_file + stale_after_seconds) and `--unregister` on completion; after each stage boundary append `tools/iteration_log.py note <project> <run> <stage> <new-finding-count>` — stall verdicts escalate to a real pivot/human decision, never a blind retry. See `shared-references/workflow-contract.md` §Loop maintenance.
5. Maintain `MANIFEST.md` per `shared-references/output-manifest.md` — every stage output gets a row.

### Stage 1: Idea Discovery — `/sec-idea-discovery`

```text
/sec-idea-discovery "$ARGUMENTS" — AUTO_PROCEED: $AUTO_PROCEED, authorization: $AUTHORIZATION
```

Runs internally: Phase 0 constraints+authorization → `sec-research-lit` → `sec-idea-creator` (incl. pilots) → `sec-novelty-check` → `sec-research-review` → `sec-research-refine-pipeline`. Output: `idea-stage/IDEA_REPORT.md` + `refine-logs/FINAL_PROPOSAL.md` + `refine-logs/EXPERIMENT_PLAN.md`.

🚦 **Gate 1 — Idea Selection** (respects `AUTO_PROCEED`):

```
📋 Sec Idea Discovery complete. Top candidates:
1. [Title] — Track: Attack — Pilot: SUPPORTED (1 oracle-verified PoC) — Novelty: PROCEED
2. [Title] — Track: Defense — Pilot: SUPPORTED, A3 probe pending — Novelty: PROCEED WITH CAUTION
3. [Title] — Pilot: REFUTED (archived as diagnostic finding)
AUTO_PROCEED: selected Candidate 1. Continuing to Stage 2.
```

`AUTO_PROCEED=false`: present ranking, ask, end turn. User may approve / request changes (re-run Stage 1 with refined constraints) / reject all / stop.

### Stage 2: Experiment Bridge — `/sec-experiment-bridge`

```text
/sec-experiment-bridge "$CHOSEN_CANDIDATE" — code review: $CODE_REVIEW, base repo: $BASE_REPO, compact: $COMPACT
```

Implements harness/oracle/dedup/A3 -> fresh Gemini code review -> sanity -> bundled jobs.py queue -> collected evidence -> evidence audit -> claims -> ablations -> new audit/claims.

Output: results, updated tracker and current RESULT_TO_CLAIM.md. Monitor jobs.py by real job ID. Contradicted claims route to negative findings/pivot, not a forced positive Stage 3. Supported/partial claims permit applicable sec-ablation-planner axes.

### Stage 2.5: Experiment Integrity Audit — `/sec-experiment-audit`

```text
/sec-experiment-audit "refine-logs/EXPERIMENT_RESULTS.md + results/"
```

Independent fresh-context audit of the **evidence layer** before any result becomes a claim: phantom results, oracle bypass, dedup honesty, statistical protocol, authorization compliance, A3 genuineness. `AUDIT_FAIL` → back to bridge for evidence fixes; authorization violation → stop the pipeline and surface to the user. `AUDIT_PASS` → Stage 3.

### Stage 3: Auto Review Loop — `/sec-auto-review-loop`

```text
/sec-auto-review-loop "$ARGUMENTS — [chosen candidate]" — difficulty: $REVIEWER_DIFFICULTY, human checkpoint: $HUMAN_CHECKPOINT
```

Up to 4 hard-gated review/fix rounds. Final STOP requires a fresh positive Gemini receipt on current audited evidence. MAX_ROUNDS/pivot may produce a status summary but blocks validated writing/submission. Output review-stage/SEC_AUTO_REVIEW.md plus resumable state and append-only real review receipts.

### Stage 4: Research Summary & Writing Handoff

Assemble `NARRATIVE_REPORT.md` from: `IDEA_REPORT.md` (chosen candidate, threat model, novelty justification), `FINAL_PROPOSAL.md` (anchors, mechanism), `EXPERIMENT_RESULTS.md` + `RESULT_TO_CLAIM.md` (claims→evidence), `SEC_AUTO_REVIEW.md` (weaknesses fixed, remaining limitations), `EXPERIMENT_AUDIT.md` (evidence-integrity verdict).

**Also seed `FACT_PACK.md`** from `templates/FACT_PACK_AND_FORBIDDEN_CLAIMS_TEMPLATE.md` — populate benchmark provenance, the verified vulnerability/result ledger, and headline metrics from oracle-verified results; carry over the forbidden-claim rows from `research_contract.md` and `IDEA_REPORT.md`. Stage 5 cannot begin without it — `sec-paper-writing` treats it as the write-lock.

The report **must** contain (security additions marked ★):
- Problem statement + core claim(s) as finally refined (with claim-migration log);
- ★ Frozen threat model table (adversary class, scope, TCB);
- Method summary with deletability rationale;
- Key results **with oracle + dedup breakdown per claim** (`raw → deduped → TP/FP`);
- ★ A3 evaluation summary (for defense/detection);
- Figure/table inventory + which reproduction scripts back each;
- ★ Ethics & disclosure status (findings under coordinated disclosure, CVE status);
- Limitations and remaining follow-ups.

Then the pipeline report:

```markdown
# Security Research Pipeline Report
**Direction**: $ARGUMENTS   **Chosen Candidate**: [title]   **Track**: [Attack/Defense/Measurement]
**Pipeline**: sec-idea-discovery → sec-experiment-bridge → sec-auto-review-loop

## Journey
- Candidates: X generated → Y feasible → Z piloted → 1 selected
- Harness: [what was built; oracle type; dedup unit]
- Experiments: [runs, wall-clock, trial counts]
- Review: N/4 rounds, final score X/10, hard gates [all green / list]

## Writing Handoff
- NARRATIVE_REPORT.md: ✅   - Venue: [VENUE or "unset — run /sec-paper-writing manually"]
- FACT_PACK.md seeded: [yes/no]  - Disclosure pending: [CVE-... / none]
```

Render HTML if `RENDER_HTML` and `/render-html` is available (optional, non-blocking).

### Stage 5: Paper Writing — `/sec-paper-writing` (optional)

Skip if `AUTO_WRITE=false` — print the manual command instead:

```text
📝 Research complete. To write the paper:
/sec-paper-writing "NARRATIVE_REPORT.md" — venue: <VENUE>
```

If AUTO_WRITE=true and actual VENUE/CYCLE are set, and the final research review is positive: run sec-paper-writing, optional sec-paper-improve-loop, then mandatory sec-paper-audit on the LAST revision. The six-point security checklist supplements rather than replaces five independent final Gemini audits. Only tools/submission_gate.py PASS permits submission-ready. Missing venue defers writing; missing audits/tools block assurance, not a fabricated pass. Never automatically click a venue's final submission button.

> **Post-submission branches** (out of scope for this pipeline): `/rebuttal`, `/resubmit-pipeline`, `/paper-talk` remain generic ARIS skills — invoke manually when a venue response arrives.
