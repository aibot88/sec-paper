---
name: "sec-paper-audit"
description: "Standalone mandatory submission audits: fresh Gemini claim-to-raw-results, citation existence/metadata/context, adversarial rejection, applicable proof verification, and anonymous artifact reproducibility. Emits version-bound receipts and runs the final PDF/submission gate."
---

# Security paper submission assurance

Read `shared-references/workflow-contract.md` and `reviewer-contract.md` from
the resolved sec-paper repo. Codex orchestrates; each audit is an independent
fresh AntiGravity/Gemini session. Never pass previous audit outputs, scores or
executor explanations as substitute evidence. Use original files directly.

## Inputs and freeze

Read final `paper/main.tex`, `main.pdf`, `.bib`, figures, `FACT_PACK.md`,
research_contract, raw results/formal evidence and `artifact/`. Fill
`.aris/submission.json` from SUBMISSION_TEMPLATE, including the actual run ID
and all evidence paths. Fetch and save the target cycle's official CFP in
`paper/official-cfp.md`; populate VENUE_POLICY_TEMPLATE with verified rules,
retrieval date, total-page cap and identifying tokens. The 2026 quick-reference
is not authoritative. No missing artifact may be represented by an invented
path, fake PASS, unassigned CVE or placeholder number.

## Five independent reviews (mandatory for submission assurance)

For each row invoke `tools/review.py run --project PROJECT --run-id RUN
--executor ACTUAL_CODEX_MODEL --phase paper-KIND --prompt-file PROMPT
--input paper --input FACT_PACK.md --input idea-stage/docs/research_contract.md
--input results --input artifact` (adapt formal evidence paths to manifest).
No `--continue-from`. Include all final manifest evidence in every audit;
do not edit final sources between calls. Store each returned receipt path in
`.aris/submission.json`, which lives outside the reviewed paper directory.

| KIND | Audit obligation |
|---|---|
| claims | Recompute every headline number/comparison/denominator/scope from raw results, not FACT_PACK alone. Check uncertainty, dedup, negative results and threat preconditions. Cite file/row/line or block. |
| citations | Independently resolve cited work: existence, exact authors/year/title/identifier, and whether it supports the sentence where cited. Save official/DOI/spec URLs and retrieved supporting passages. Bibliography key resolution alone is insufficient. Verify CVE applicability and commits, not just string format. |
| adversarial | Construct the strongest evidence-grounded rejection argument. Identify remaining fatal/major issues and whether bounded claims survive; no mere score-based approval. |
| proof | Verify actual security/mathematical guarantees against their assumptions and code/model. PASS for verified applicable proofs; NOT_APPLICABLE with a concrete reason if no theorem/security-proof claim exists. A model's plausibility judgment is not formal verification; state exactly what was checked. |
| artifact | Inspect anonymous reproduction scripts, pinned inputs and a clean-environment reproduction log with commands, exit codes, output hashes and omitted sensitive components. Check logs against scripts/results. Missing reproduction evidence, identifying metadata or nonfunctional scripts blocks PASS. |

All prompts require JSON decision, in_scope and findings per review.py's
contract. PASS is allowed only without unresolved blockers; proof N/A is the
only applicable exemption. Missing web retrieval blocks citation assurance.
Codex performs the controlled reproduction run; Gemini audits the resulting
evidence. Do not ask the review-only bridge to modify or deploy the artifact.

## Final deterministic checks and routing

Run `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` in paper/
before freezing the audits. Codex fixes errors, unresolved references, bad
figures and overflow. Then:

```bash
python3 "$SEC_PAPER/tools/paper_check.py" --project "$PROJECT"
python3 "$SEC_PAPER/tools/submission_gate.py" --project "$PROJECT"
```

The PDF checker requires real pdfinfo/pdftotext/pdffonts, compile logs, current
venue policy and no draft placeholders; missing tools are BLOCKED, not N/A.
The submission gate checks all five positive fresh receipts and complete
snapshots, final PDF/source/BibTeX, fact pack, raw evidence and anonymous
artifact. Any source/result/figure/artifact edit invalidates affected receipts
and the PDF check: regenerate them. Preserve failed audits and raw traces.

Output `.aris/submission-gate.json`, five receipts, `paper/.aris/pdf-check.json`
and a bounded submission-readiness report. A PASS is a process verdict, not a
claim of correctness or guaranteed acceptance. Actual venue upload/final
submission remains a separate user-confirmed action.
