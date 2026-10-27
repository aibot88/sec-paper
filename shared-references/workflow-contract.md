# Standalone workflow contract (authoritative across sec-* Skills)

This is an agent-executed pipeline, not a claim that Markdown is a running
scheduler. All commands below use `$SEC_PAPER/tools/`, where SEC_PAPER is
`.aris/sec-paper.json:repo_root` or the resolved installed Skill's repository.
No ARIS checkout or generic ARIS Skill is required. Python 3.9+, POSIX are
the baseline. External Docker/TeX/PDF/search capabilities are real prerequisites,
not bundled services. Older vendored references do not override this contract.

## Bootstrap, roles and shared parameters

1. `python3 "$SEC_PAPER/tools/project.py" init --project "$PROJECT"`.
2. `python3 "$SEC_PAPER/tools/project.py" doctor --project "$PROJECT" --live`.
3. Record exact executor identity, actual returned Gemini identity, direction,
   track, authorization scope, user-approved resources, AUTO_PROCEED,
   AUTO_WRITE, VENUE/CYCLE, REF_PAPER, COMPACT, pilot time/request/trial budgets
   in `.aris/context.json`; forward the resolved values to every child.
4. Generation, coding, experiment execution and prose are Codex's work. Gemini
   alone reviews. Never delegate brainstorming to the reviewer backend.
5. A missing reviewer blocks semantic acceptance. Missing TeX blocks writing
   assurance only; lack of a search source must be recorded, not fabricated.

## Run namespaces and completion

Outer run ID: `<direction>-<date>-<unique-suffix>`. Discovery child:
`<outer>-ideas`; use `--parent-run-id <outer>`. Never use the same ID for two
different phase lists. On reuse `run_state.py start` rejects mismatched lists.

```text
outer: sec-idea-discovery,sec-experiment-bridge,sec-experiment-audit,sec-auto-review-loop,summary,sec-paper-writing
child: sec-research-lit,sec-idea-creator,sec-novelty-check,sec-research-review,sec-research-refine-pipeline
```

Start both with `--executor <actual-codex-model>`, not
`--provisional-advances`. Outer uses `--auto-write` only when requested.
`run_state.py set ROOT RUN PHASE running` on entry;
`... set ROOT RUN PHASE done --artifact PATH` after output exists.
Execution-only research-lit, bridge and summary can complete with nonempty
artifacts. All other phases require a real positive Gemini receipt:

```bash
python3 "$SEC_PAPER/tools/run_state.py" accept "$PROJECT" "$RUN" "$PHASE" \
  --verdict-id .aris/traces/REAL_UUID/receipt.json --reviewer ACTUAL_GEMINI_MODEL
```

Final receipts use fresh sessions; `accept` rejects unavailable, negative,
same-family, wrong-run and stale inputs. Resume checks freshness, not status
labels alone. Re-entering an accepted phase invalidates later acceptances.
`skipped` is legal only for disabled optional writing. An old run with weaker
receipts must be revalidated, never silently upgraded.

## S1: constraints -> literature -> ideas -> novelty -> review -> refine+plan

Keep a shared IDEA_REPORT; each child updates only its owned sections and
preserves earlier sections and failed candidates. No child may overwrite the
whole report. Candidate IDs survive ranking changes. `Ranked Ideas` may
contain nested candidate headings; the gate parses heading levels correctly.
Review inputs can be `path.md#heading-slug`: snapshot includes the full owned
section and its subsections. First fold all findings into that section, then
obtain its acceptance receipt; never edit the sealed section afterwards.
This lets later phases append their own sections without invalidating earlier
receipts. Include dependent candidate sections and original raw evidence in
the input list too. A scope/candidate change requires renewed relevant reviews.

The creator's seven actions remain mandatory: Codex generation -> invariant
dedup/resource/authorization screening -> fresh Gemini ranking ->
sec-novelty-check on the shortlist -> local pilot launch -> monitor/collect ->
Codex evidence re-ranking with fresh Gemini validation. Store internal
novelty/triage receipts by candidate ID. The outer novelty stage reviews the
final post-pilot claim; reuse search evidence only when scope/claim unchanged,
but its phase/run receipt is distinct. NO clean pilot means an explicitly
UNVALIDATED candidate, not a validated recommendation.

Refinement may use warm objection continuity, followed by a fresh final
Gemini review on FINAL_PROPOSAL + EXPERIMENT_PLAN + TRACKER + REVIEW_SUMMARY.
REVISE may produce a draft plan, never a validated handoff. Gate completion
requires these nonempty artifacts and four positive phase receipts (creator,
novelty, external review, refinement). For outer discovery acceptance obtain
a fresh aggregate review of the child state, final report, plan and evidence.

## S1.5/S2: experiment evidence and repair loops

Ordered loop: implement -> fresh code review -> sanity/oracle controls -> main
jobs -> collect -> sec-experiment-audit -> sec-result-to-claim ->
sec-ablation-planner (if supported/partial) -> run ablations -> new audit +
claim routing -> final results. Initial claims may be provisional engineering
notes only; unaudited data never becomes a paper claim.

Every changed evidence batch invalidates older AUDIT_PASS and claim judgments.
Auto-review repair rounds must re-run audit/routing before re-review. The
final fresh Gemini verdict must read the latest audited snapshot. Repeated
failure routes to pivot; MAX_ROUNDS is NOT a positive verdict. You may always
write a status/negative-results report, but no submission-ready claim follows
without a valid final acceptance. A partial claim cannot be labeled supported
until missing evidence is supplied or a logged scope revision is revalidated.

Use `review-stage/REVIEW_STATE.json` after each boundary: schema_version,
run_id, parent_run_id, round, status, current_phase, executor_model,
reviewer_route, requested_model, reported_model, thread_id, pending_jobs,
evidence_inputs, receipt, weaknesses, next_action. Keep run_id unchanged.
Append one row per returned review to `review-stage/ACQUITTAL_LOG.jsonl`
(run_id, round, phase, raw_trace, receipt, decision, accepted); never replace
old rows. A crash resumes from the first unfinished action; it never reruns
an already-running job under a new ID.

## Standalone run/monitor/queue lifecycle

`tools/jobs.py` is the owned local backend, not an optional ARIS alias.
Start a spec with argv command, id, target, target_revision, isolation_key,
seed, timeout_seconds. Output is `results/ID/config.json`, stdout/stderr,
job.json and application oracle artifacts. Job completion means process
completion, not a true vulnerability. Oracle evidence is still mandatory.

```bash
python3 "$SEC_PAPER/tools/jobs.py" start --project "$PROJECT" --spec job.json
python3 "$SEC_PAPER/tools/jobs.py" status --project "$PROJECT" --id pilot-1
python3 "$SEC_PAPER/tools/jobs.py" wait --project "$PROJECT" --id pilot-1
python3 "$SEC_PAPER/tools/jobs.py" cancel --project "$PROJECT" --id pilot-1
python3 "$SEC_PAPER/tools/jobs.py" queue --project "$PROJECT" --spec jobs.json --parallel 3
```

Queue all N jobs uniformly (no 6–9 gap). `after` dependencies enforce waves.
Spec IDs are immutable; failed jobs require a new ID. Workers enforce deadlines,
cancel groups and clean descendants. An interrupted/killed worker is not
auto-retried or assumed safe: inspect orphan/target state, then allocate a new
instance/key. The isolation key prevents accidental concurrent scheduling,
not arbitrary network traffic; authorization and endpoint confinement remain
harness/testbed obligations. SSH/GPU backends are explicitly unsupported until
an adapter implementing this same lifecycle is installed; never silently fall
back from a requested backend. Total worker/request budgets constrain the
queue and child harnesses; don't launch beyond the inherited budget.

## Summary and W3 submission assurance

Freeze final evidence -> final RESULT_TO_CLAIM -> NARRATIVE_REPORT + FACT_PACK
(each fact points to raw file/unit/denominator) -> outline -> figures -> LaTeX
-> compile -> polish -> independent final audits -> PDF and bundle gate.
No edits after final audits; edits require renewed affected audits.

Use sec-paper-audit (five fresh Gemini calls: claims, citations, adversarial,
proof-or-justified-N/A, artifact reproduction). These replace mandatory ARIS
assurance functions locally; they are not optional host dependencies. A six-item
security checklist supplements rather than replaces these audits.

Capture the actual venue cycle's official CFP and rules in
paper/official-cfp.md + venue-policy.json. The 2026 reference is only a starting
point. No universal 90-day disclosure mandate, mandatory CVE assignment or
fixed trial count substitutes for actual scope/ethics/power decisions.

Assemble `.aris/submission.json` from the template BEFORE final audits.
Final source/PDF/BibTeX, FACT_PACK, research contract, raw evidence, venue
policy and anonymized artifact directory must be covered by every final
audit snapshot. Run `paper_check.py`, then `submission_gate.py`. Only a fresh
PASS permits submission-ready. Submission to a venue itself is a separate
human-confirmed action, not an automatic final click. AUTO_WRITE=false stops
at an honest research handoff, not a claim that a paper exists.
