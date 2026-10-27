# ARIS parity and independent implementation boundary

Baseline audit: sec-paper `62c4c87`; upstream checkout inspected at
`18bceb3c71c638bef58096274e1c9a6d323dbc0a`. This is not an ARIS fork/update
mechanism. See THIRD_PARTY_NOTICES for the earlier unpinned import history.

| ARIS responsibility | Independent sec-paper implementation |
|---|---|
| research-pipeline five-stage spine | sec-research-pipeline; isolated parent/child IDs; optional writing remains optional |
| idea-discovery brief/reference/lit/creator/novelty/review/refinement | all sec-* equivalents; shared context/parameter ownership and real Gemini receipts |
| creator generation/dedup/resources/rank/novelty/pilot/monitor/rerank | Codex generation and execution, owned sec-novelty-check, jobs.py lifecycle and fresh Gemini validation |
| native selectable reviewer | Gemini-only route, bundled agy bridge, project.py init/doctor and review.py CLI; no Codex self-review fallback |
| run state, deterministic evidence gate | explicit execution/review types, real trace freshness, owned Markdown sections, four refinement outputs and namespaces |
| run/monitor/queue Skills | local POSIX jobs.py start/status/wait/cancel/queue, immutable configs, target isolation keys, timeouts and dependency waves |
| experiment integrity -> result-to-claim -> ablations | audit before adjudication, then ablation wave, then re-audit/re-route on new evidence |
| review state, reviewer memory and acquittal ledger | REVIEW_STATE.json, append-only ACQUITTAL_LOG; warm repair checks are not called cold; final acceptance is fresh Gemini |
| narrative/claims/writing handoff | final evidence/claims snapshot, NARRATIVE_REPORT and fact pack; unresolved/max-round work is status only |
| plan/figure/write/compile/improve | owned agent-executed W3 specification; real latexmk and PDF inspectors, no generic ARIS Skill dependency |
| mandatory submission audits and freshness verifier | sec-paper-audit: five fresh Gemini audits; paper_check.py + submission_gate.py on the unchanged final bundle |
| deterministic evidence existence pre-check | tools/evidence_check.py (vendored, unmodified) wired into sec-result-to-claim + sec-experiment-audit + workflow contract |
| output manifest / language / versioning / composition | shared-references/output-{manifest,language,versioning,composition}.md, wired via workflow-contract.md §Output protocols |
| review tracing | review-tracing.md maps onto review.py raw.json + receipt.json per call (full prompt/response, hash-bound) |
| injection hygiene | workflow-contract.md §Output protocols + sec-idea-creator: threat_scan.py --scope strict on every re-ingested non-executor text |
| watchdog + iteration stall log | vendored tools, wired in sec-research-pipeline Stage 0 + contract §Loop maintenance |
| reviewer memory across rounds | REVIEWER_MEMORY.md in sec-auto-review-loop (all modes) + contract §S1.5/S2 — durable objection ledger vs. ephemeral warm threads |
| wiki/helper resolution | wiki-helper-resolution.md: resolve repo via .aris/sec-paper.json or real skill path; wiki non-blocking, scanned content blocking |
| integration contract (engineered handoffs) | integration-contract.md — artifact + shape check + deterministic gate + failure route + version binding |
| score calibration anchors | taste-calibration.md cited by sec-research-refine (+ review-loop score gate) |
| fan-out pattern | fan-out-pattern.md — generation may shard; acceptance stays fresh-Gemini; fetched content scanned |
| release/runtime tests | unittest suite for bridge failures, local jobs, state/gates/install, stale receipts, contract coverage and real PDF compilation when tools exist |

### Deliberately not ported (scoped out, not oversights)

| Upstream contract/skill | Why out of scope |
|---|---|
| `compute-env-contract` (env spec + hash ledger + validation ladder) | Local POSIX backend only; reproducible-environment fidelity for remote/GPU targets returns with a real backend adapter. Documented as deferred, not silently absent. |
| `AGENTS.md` pipeline-status dashboard (`language:` flag, stage table) | `.aris/context.json` + `MANIFEST.md` + `REVIEW_STATE.json` carry the same state machine-readable; language flag supported via context.json. |
| Post-submission skills (`rebuttal`, `resubmit-pipeline`, `paper-talk`, posters/slides) | Intentionally left to the ARIS generic layer — out of the idea→submission scope. |
| Rendering (`render-html`), grant/patent tracks, ML-interview tooling | Optional cosmetics / different domains; never load-bearing for a security submission. |
| `verify_paper_audits.sh` name | Equivalent is `tools/submission_gate.py` (fail-closed, receipt + snapshot bound). |

## Explicit boundaries (not concealed fallbacks)

- Skills remain **agent-executed specifications**; this is not a fully coded
  research director, nor a claim that future experiments or papers already ran.
- Local POSIX jobs are supported. A requested SSH/GPU backend without a real
  lifecycle adapter is BLOCKED, not replaced silently with local work.
- Isolation keys prevent accidental concurrent use of a mutable testbed, not
  hostile network access. Harness/testbed authorization and network confinement
  are still required. Interrupted workers need target/orphan inspection.
- Python is bundled only as a dependency requirement, not a runtime image.
  agy/login, Docker for relevant targets, TeX/PDF tools and accessible literature
  sources must actually work on the host; doctor reports what is present.
- Review receipts detect absent/mismatched/stale local evidence. They are process
  records, not signed attestations against a malicious owner fabricating files,
  and not a theorem of research correctness.
- Proof checking applies only to actual guarantee/theorem claims. A justified
  Gemini NOT_APPLICABLE is recorded otherwise. No forced CVE assignment or
  universal disclosure interval is assumed.
- The final manifest covers paper source/PDF, raw results, fact pack, contract,
  actual venue policy and anonymous artifact code. Real clean reproduction and
  semantic audits remain necessary; offline fixtures never supply them.
- Rebuttal/resubmission/talks are post-submission branches. Upload and final
  submission are human-confirmed actions, not automatic side effects.

## Verification commands

```bash
python3 -m unittest discover -s tests -v
python3 tools/project.py doctor --project /path/to/project --live
python3 tools/idea_discovery_gate.py /path/to/project CHILD_RUN_ID
python3 tools/paper_check.py --project /path/to/project
python3 tools/submission_gate.py --project /path/to/project
```

The last three require genuine project artifacts and receipts. Missing inputs
must block; do not synthesize them from test fixtures just to get PASS.
