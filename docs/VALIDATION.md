# Implementation validation

## Round 2 — 2026-10-28: contract-layer parity repairs

Third audit (post-`85e3c2a`) compared every upstream contract doc and helper
referenced by the idea→submission chain. Fixes applied:

- Vendored `tools/evidence_check.py` (deterministic value-in-source
  pre-check, upstream two-stage gate stage 1) and wired it into
  `sec-result-to-claim`, `sec-experiment-audit`, workflow-contract.
- Ported 10 missing shared-reference contracts: output-manifest,
  output-language, output-versioning, output-composition, review-tracing,
  wiki-helper-resolution, integration-contract, evidence-precheck,
  taste-calibration, fan-out-pattern.
- Banner-marked 4 vendored docs superseded/conflicting with the Gemini-only
  contract (reviewer-backends, resumable-runs, external-cadence,
  venue-checklists) + scoped notes on 2 normative ones.
- Wired `watchdog.py`/`iteration_log.py` into pipeline Stage 0 (were vendored
  but referenced nowhere); added REVIEWER_MEMORY.md durable objection ledger
  and REF_PAPER_SUMMARY.md canonical artifact.
- `python3 -m unittest discover -s tests`: **49 tests pass** (35 prior + 14
  contract-layer tests). `evidence_check.py` smoke: verified / value_not_found
  / path_missing / skipped_non_numeric all behave; `git diff --check` clean.
- Round-2 Gemini review: first call REVISE with 4 MAJOR findings (watchdog
  loop-register schema, evidence_check CLI syntax + substring false-positive
  risk, manifest overclaim, tautological test) — all fixed and verified by a
  fresh-session re-review **PASS** (`gemini-3.8-flash-high`, receipt
  `.aris/traces/ecf11a8bdc6a41e297b559d43c0974b0/receipt.json`, 9 bound inputs
  revalidated post-verdict). One earlier REVIEW_UNAVAILABLE (transient OAuth
  EOF) retried successfully — raw trace preserved as process evidence.

## Round 1 — 2026-10-27: runtime and assurance repairs

## Scope

Repair of the independent idea-to-submission orchestration contracts, based on
the audit of sec-paper `62c4c87`. This record is NOT a scientific result, paper
acceptance, or a claim that an actual study ran end-to-end.

## Local checks

`python3 -m unittest discover -s tests -v`: **35 tests passed** on macOS,
Python 3.9.13; no tests skipped in the final run.

- 8 offline bridge tests use an explicit fake CLI (identity, continuation,
  errors/incomplete/empty responses, long stdin and timeout).
- 7 local job tests exercise real subprocess execution: success, immutable
  IDs, logs/seeds, timeout, cancellation, isolation keys, interruption and a
  six-job dependency queue. They do not test any real security target.
- 3 PDF/policy tests include actual latexmk compilation and real
  pdfinfo/pdftotext/pdffonts inspection of a one-page test fixture, followed
  by rejection after its source changes. Fixture policy is explicitly NOT
  a real conference policy.
- 17 workflow tests cover clean installation, fixed Gemini routing, owned
  novelty invocation, nested Markdown sections, real-trace requirements,
  positive/negative/stale synthetic receipts, parent/child namespaces,
  resume, loop hard gates and final bundle freshness.

`python3 -m compileall -q tools tests` and `git diff --check`: passed.
Local relative Markdown links under shared-references/ and skills/: no
missing targets in the final check.

Calling submission_gate.py on this repository without an actual research
manifest returned **BLOCKED / submission_ready=false**, as required.

## Live AntiGravity verification (separate from fake test fixtures)

- The live probe returned SEC_PAPER_GEMINI_PROBE_OK with CLI-reported model
  `gemini-3.8-flash-high`.
- A new-session Gemini implementation review returned **PASS**, in scope,
  with no findings. Reported model: `gemini-3.8-flash-high`.
- Reviewer thread: `c2634145-c0dd-49f2-b955-e4b0a99afe9b`.
- Run: `sec-paper-repair-20261027`, phase: `implementation-review`.
- Local receipt: `.aris/traces/82181c32d88c4fd0bbc43e53128216c2/receipt.json`.
- Local raw trace SHA-256:
  `6046f3251617480e190164292c0bb9de7c6b3b423cbc02f13fd2808e06f91c64`.
- `evidence.validate_receipt` revalidated the returned positive verdict and
  current snapshot of **41 input files** after review. Raw traces remain local
  ignored runtime state, not publicly published paper evidence.

The model identity is the bridge/CLI's actual reported identity, not an
independent server attestation. Gemini's PASS is an advisory code/process
review; tests and human inspection are still needed, and it does not certify
the truth of future research or guarantee conference acceptance.

## Not validated by this change

- No real vulnerability campaign, production-target test or complete paper
  submission was executed.
- No SSH/GPU lifecycle adapter is implemented; local POSIX is the owned
  backend. Unsupported requested backends block explicitly.
- Final paper assurance still needs actual research evidence, current official
  venue rules, clean anonymous artifact reproduction and five fresh Gemini
  submission audits on the final unchanged bundle.

Architecture mapping and exact boundaries: [ARIS_PARITY.md](ARIS_PARITY.md).
