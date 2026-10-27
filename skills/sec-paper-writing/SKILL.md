---
name: "sec-paper-writing"
description: "Draft and audit cybersecurity, Web application security, and systems security papers for IEEE S&P, USENIX Security, ACM CCS, NDSS, PETS, and ACSAC. Enforces threat-model tables, adaptive-attacker evaluation, single fact-pack provenance, CVE/commit pinning, and mandatory Ethics + Open Science appendices."
argument-hint: "[narrative-report-or-repo-path] [— venue: USENIX_SEC | IEEE_SP | ACM_CCS | NDSS]"
---

# Security & Systems Paper Writing (`sec-paper-writing`)

> *"A security paper without a threat model is a wish, not a result."*  
> Adapted for Web application security, software/systems security, and AI-system security manuscripts targeting **IEEE S&P (Oakland), USENIX Security, ACM CCS, NDSS, PETS, ACSAC, AsiaCCS, and RAID**.

Draft and audit a publication-ready security manuscript for: **$ARGUMENTS**

---

## Core Writing Philosophy

1. **Write a characterization paper, not a "we win" brochure.** Explicitly state the regimes where your attack, detector, or defense succeeds and where it degrades or fails. Security PC members trust bounded claims and hunt down unbounded boasts.
2. **One centerpiece contribution; subordinate supporting engineering.** Engineering components (crawlers, state snapshots, parsers, DSLs) exist to make the core security insight work — present them as necessary coupling, not competing headline contributions.
3. **Single Fact Pack + Forbidden-Claim Table.** Every numeral (bug count, false-positive rate, overhead, trial count, p-value), CVE ID, and commit SHA in the prose, tables, and abstract must trace to `FACT_PACK.md`. Anything unverified stays `[TBD]` or `[CITATION NEEDED]`.
4. **Trust direct measurement over multi-agent consensus.** Reviewer agents may agree on a plausible-sounding root cause or speedup explanation that is empirically false. Never write a causal explanation into the paper unless an isolated experiment verified it.

---

## Nine Non-Negotiable Iron Rules

1. **No fabricated or memory-typed citations.** Verify every paper across at least two sources (DBLP + venue proceedings / USENIX page / NDSS page / DOI / ePrint) and fetch BibTeX programmatically.
2. **No security claim without an explicit Threat Model section and Adversary Capability Table.** State Who, Goal (C / I / A / Authorization / Isolation), In-Scope vs. Out-of-Scope, and TCB before the Design section.
3. **No defense or detector evaluation without an Adaptive Attacker (A3).** Evaluate what happens when the adversary knows your mechanism, rules, thresholds, or parser and deliberately crafts inputs/states to evade it.
4. **No raw crash/alert counts masquerading as vulnerability counts.** Always report the ground-truth oracle and deduplication unit (independent root cause / minimal patch / broken invariant).
5. **Pin every CVE and code artifact.** Cite vulnerabilities as `CVE-YYYY-NNNNN` (verified via NVD) and public PoC/fix commits with full 40-character Git SHAs.
6. **Strict double-blind anonymity.** Self-citations in third person; strip author names, grants, non-anonymized GitHub URLs, and identifying hostnames from text, figures, and scripts.
7. **Mandatory Ethics & Responsible Disclosure before submission.** Follow stakeholder analysis and the actual venue/vendor disclosure policy; record dates and any embargo. A 90-day window is an example, not a universal requirement. Local-only work still documents stakeholders/risks. No CVE assignment is required for a legitimate unassigned finding; record its real advisory status.
8. **Mandatory Open Science / Artifact Readiness.** For USENIX Security ('26 policy) and peer venues, prepare anonymized artifact links and per-table/figure reproduction scripts (`./reproduce-table-1.sh`) at submission time, not after acceptance.
9. **Zero reviewer-simulator leakage.** Never paste internal review prompts, scores, or simulated rebuttal prose into the manuscript body.

---

## Internal Orchestration (W3 Sub-Chain)

This is a standalone W3 workflow. Codex performs the following stages directly; no ARIS Skills are required. Read shared-references/workflow-contract.md and preserve its actual-Gemini/freshness rules. All produced artifacts get MANIFEST.md rows (output-manifest.md); regenerated drafts keep timestamped copies (output-versioning.md); report prose follows output-language.md while venue LaTeX stays in the venue language:

```text
NARRATIVE_REPORT + FACT_PACK + final claim/evidence receipts
  -> cycle-specific official CFP + venue policy capture
  -> PAPER_PLAN with claim->figure/table->evidence mapping
  -> figures (matplotlib/TikZ/SVG, all numbers from verified evidence)
  -> LaTeX sources + BibTeX + explicit output inventory
  -> latexmk compilation and text-layer polish
  -> sec-paper-audit: five mandatory independent fresh Gemini audits
  -> paper_check.py + submission_gate.py on the FINAL unchanged bundle
```

Deliver paper/main.tex, main.pdf, .bib, figures and reproducible code/data in artifact/, plus final audit receipts, paper/.aris/pdf-check.json and .aris/submission-gate.json. Missing TeX/PDF tooling blocks submission assurance. No TBD, invented citation or unsupported number may remain in the final bundle. A general-purpose host helper may assist, but cannot replace the mandatory independent audits or owned verifier.

---

1. **Abstract (5–6 sentences)**:
   - Target system/boundary and why its security property matters;
   - Why prior defenses/scanners/analyses fail (the broken assumption);
   - Our core insight and mechanism in plain technical terms;
   - Threat model scope in one clause;
   - Headline empirical/formal result traced to `FACT_PACK.md` (with denominator and FP/overhead context).
2. **1. Introduction**:
   - Concrete motivating failure or cross-layer discrepancy;
   - Why naive fixes or prior tools miss it;
   - Core insight + how the system/method works at a high level;
   - Explicit summary of contributions (3–4 bullets, each mapped to a section and verifiable evidence);
   - Threat-model one-liner + artifact/disclosure summary.
3. **2. Background & Motivating Example**:
   - Minimal technical background needed by a non-specialist PC member;
   - One concrete, anonymized walkthrough (code snippet, HTTP/state trace, or protocol flow) showing the exact failure mode.
4. **3. Threat Model & Security Goals** *(Dedicated Section)*:
   - Adversary starting privilege, visibility, and interaction budget;
   - Security property targeted or enforced (never conflate C, I, A, and Authorization);
   - **Adversary Capability Table** (`Capability | In Scope | Out of Scope | Justification`);
   - Trusted Computing Base (TCB) and deployment assumptions.
5. **4. Design / Methodology**:
   - Architecture overview diagram matching component numbers in prose;
   - Component-by-component design tied to the broken invariant;
   - **Deletability / necessity rationale**: why each component is required for the security loop to hold;
   - Clear separation between single-party algorithms (`algorithm` env) and multi-party/cross-layer message flows (sequence diagram).
6. **5. Security Analysis / Formal Properties** *(or Implementation & Root-Cause Analysis)*:
   - What guarantee holds under the stated TCB;
   - Residual attack surface when assumptions are relaxed.
7. **6. Evaluation**:
   - Explicit **Research Questions (RQ1–RQ4)**: e.g., Effectiveness on ground-truth benchmark, Real-world/zero-day discovery & root-cause triage, Resilience to **Adaptive Attacker (A3)**, Runtime/deployment overhead & ablation;
   - **Oracle & Deduplication Declaration**: how true positives and false positives were verified;
   - Multi-trial distribution & statistical tests (e.g., Mann-Whitney U / median + IQR) for any stochastic component.
8. **7. Discussion & Limitations**:
   - Honest failure regimes, manual effort required, and out-of-scope threats.
9. **8. Related Work**:
   - Grouped by mechanism and assumption boundary (never a laundry list of "Paper X did Y").
10. **9. Conclusion**.
11. **Required Appendices (Venue-Specific)**:
     - **USENIX Security**: Ethical Considerations and Open Science as required by the target cycle; retrieve current official CFP for names, placement and page rules instead of applying the 2026 example blindly.
    - **IEEE S&P / ACM CCS / NDSS**: integrate Ethics & Data/Artifact Availability per current CFP placement rules.

---

## Pre-Submission Audit Gate

Before compiling the final PDF, run this 6-point check against `FACT_PACK.md` and the forbidden-claim source (`idea-stage/FORBIDDEN_CLAIMS.md` if materialized, else the `Forbidden-Claim & Ethics Pre-Flight Seed` section of `IDEA_REPORT.md` + `research_contract.md`):

This checklist is a SECURITY SUPPLEMENT, not submission acceptance. After the final compile/polish, sec-paper-audit must independently check raw-result-to-paper claims, citation existence/metadata/context, the strongest rejection case, applicable proofs (or justified N/A), and clean anonymous artifact reproduction. All five fresh Gemini receipts must cover the current final inputs, then paper_check.py and submission_gate.py must PASS. Any later edit reopens affected audits. A failed MAX_ROUNDS cannot be relabeled READY.

- [ ] **Numeral Parity**: Every number in Abstract, Intro, Tables, and Conclusion matches `FACT_PACK.md` verbatim.
- [ ] **Forbidden-Claim Clean**: Zero occurrences of banned overclaims (`novel` without citation proof, `0% FP` without scope bound, `provably secure` without formal theorem + assumption list).
- [ ] **Threat-Model Consistency**: No evaluation experiment uses attacker capabilities excluded in Section 3 (or if it does, it is explicitly labeled as an out-of-model stress test).
- [ ] **Adaptive Attacker Present**: Defense/detection papers include a dedicated subsection testing A3 adaptive evasion.
- [ ] **Citation & SHA Integrity**: Every BibTeX key resolves; CVEs match `CVE-YYYY-NNNNN`; commits use 40-char SHAs.
- [ ] **Double-Blind & Policy Compliance**: No author-identifying paths, repo links, or self-citation phrasing (`in our prior work`); USENIX `Ethical Considerations` and `Open Science` appendices present when `venue: USENIX_SEC`.
