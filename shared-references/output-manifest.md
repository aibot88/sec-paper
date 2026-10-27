# Output Manifest Protocol

After writing any output file, append an entry to `MANIFEST.md` in the project
root. `MANIFEST.md` is an **agent-maintained provenance log** — one auditable
ledger of what each stage produced. Deterministic acceptance is still enforced
by the receipt/gate layer (`run_state.py`, `submission_gate.py` over
`.aris/submission.json`); the manifest is bookkeeping evidence for humans and
for reviewer prompts, not a cross-checked gate input today.

## Format

If `MANIFEST.md` does not exist, create it with this header:

```markdown
# Research Output Manifest
> Auto-maintained by sec-paper skills. Tracks all generated artifacts across
> the idea → submission lifecycle.
| Timestamp | Skill | File | Stage | Description |
|-----------|-------|------|-------|-------------|
```

Then append one row per output file:

```markdown
| 2026-10-28T10:31Z | sec-idea-creator | idea-stage/IDEA_REPORT.md | W1-ideas | Ranked candidates with pilot verdicts |
```

## Rules

- **Append-only.** Never rewrite or delete rows; a superseded file gets a new
  row and the old row stays as history (see output-versioning.md).
- **Receipt-bearing artifacts** (`IDEA_REPORT.md`, `FINAL_PROPOSAL.md`,
  `EXPERIMENT_PLAN.md`, `EXPERIMENT_RESULTS.md`, `RESULT_TO_CLAIM.md`,
  `NARRATIVE_REPORT.md`, `FACT_PACK.md`, `main.tex`, `main.pdf`,
  `submission.json`) MUST have a manifest row; other files SHOULD.
- Review traces and receipts under `.aris/traces/` are recorded by
  `review.py` itself — do not duplicate them in the manifest.
- A manifest row is provenance bookkeeping, not evidence of correctness.
