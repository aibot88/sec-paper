# Evidence Pre-check (deterministic first stage)

Claim audits (`sec-result-to-claim`, `sec-experiment-audit`, the claims audit
inside `sec-paper-audit`) spend a Gemini call judging whether a claim is
supported. Before that call, run the deterministic pre-check so hallucinated
citations never reach the reviewer.

## Two-stage gate

- **Stage 1 — `tools/evidence_check.py`** (no model): for each claim's
  `(value, source)` pair, verify the cited file exists and the literal value
  appears in it. Statuses: `verified` | `path_missing` | `value_not_found` |
  `unparseable`. `verified` means only *the cited evidence exists* — never
  that the claim is correct. The numeric matcher is deliberately
  conservative: compound constructs (dates, versions, fractions, locale
  grouping, non-ASCII delimiters) fail closed to stage 2.
- **Stage 2 — Gemini semantic review** (`tools/review.py`): judges whether
  real-but-mismatched evidence actually supports the claim.

## Usage

```bash
python3 "$SEC_PAPER/tools/evidence_check.py" "$PROJECT" \
  --value "23" --source "results/pilot-1/oracle.json"
python3 "$SEC_PAPER/tools/evidence_check.py" "$PROJECT" \
  --batch claims.json --numeric-only
```

Batch input: a JSON list of `{"id": ..., "value": ..., "source": ...}`.
Exit 0 only when every checkable claim verifies; `path_missing` /
`value_not_found` entries are surfaced to the reviewer as findings, not
silently dropped.

**Use `--numeric-only` for stage-1 in sec-paper.** The non-numeric matcher is
an un-bounded substring check: short verdict tokens ("TP", "PASS") can
substring-match unrelated words ("HTTP", "PASSWORD") and be falsely
`verified`. Numeric claims keep the strict boundary logic; qualitative/
verdict claims report `skipped_non_numeric` and go to the Gemini jury
unchecked — fail-closed in the direction that can never fabricate evidence.
