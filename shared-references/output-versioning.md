# Output Versioning Protocol

When writing an output file that would overwrite an existing file, use a
timestamped filename plus a fixed-name latest copy:

1. Write output to the timestamped file:
   `{FILENAME}_{YYYYMMDD_HHmmss}.md` (or `.json`, `.tex` as appropriate),
   in the same directory as the fixed-name file.
2. Copy the same content to the fixed-name file (`{FILENAME}.md`), overwriting
   the previous latest copy.
3. Downstream skills and `review.py --input` always read the fixed-name file —
   they do not need to know about timestamps.

## Interaction with receipts (important)

`review.py` receipts pin SHA-256 snapshots of reviewed inputs. Overwriting a
reviewed artifact **invalidates its receipt** (`STALE`) — versioning never
hides that; it preserves the superseded copy for audit and rollback while the
new content must be re-reviewed before acceptance.

- Apply timestamping to **drafts and regenerated reports** (IDEA_REPORT,
  FINAL_PROPOSAL, EXPERIMENT_PLAN, EXPERIMENT_RESULTS, NARRATIVE_REPORT,
  round-N-refinement, section rewrites).
- Do NOT timestamp raw evidence under `results/<job_id>/` (immutable by
  contract — jobs.py already refuses reuse), receipts under `.aris/traces/`
  (already unique), or MANIFEST.md / REVIEW_STATE.json / ACQUITTAL_LOG.jsonl
  (append-only or overwrite-in-place state).
- When reverting, copy a timestamped version back onto the fixed name; the
  receipt bound to that content then validates again only if hashes match.
