# Output Composition Protocol

When a skill runs **inside an orchestrating pipeline** (`sec-idea-discovery`,
`sec-research-pipeline`, `sec-research-refine-pipeline`), its intermediate
findings fold into the pipeline's single canonical deliverable instead of each
sub-skill scattering overlapping files. When the same skill runs **standalone**
it writes its own documented outputs unchanged.

## The two states

- **composed** — the caller declares the owned section(s). The child writes
  ONLY its owned sections of the shared deliverable (e.g.
  `idea-stage/IDEA_REPORT.md#ranked-ideas`), plus any contract-named artifact
  it is the sole producer of (`refine-logs/EXPERIMENT_PLAN.md`, `MANIFEST.md`
  row, job results). It never rewrites or truncates other sections, and never
  deletes earlier candidates — failed candidates stay as recorded findings.
- **standalone** (default when no caller context is given) — the skill writes
  every output its own documentation names.

## Signal

The orchestrator passes the shared deliverable path and the owned-section list
in the invocation context. Absence of that context = standalone, never
"half-composed". Section-level receipts (`review.py --input file.md#section`)
bind each owned section to its producer's review phase.
