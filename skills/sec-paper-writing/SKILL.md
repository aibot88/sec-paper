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
7. **Mandatory Ethics & Responsible Disclosure before submission.** Follow the Menlo Report stakeholder analysis and document the 90-day coordinated disclosure timeline (or justify local-only testing).
8. **Mandatory Open Science / Artifact Readiness.** For USENIX Security ('26 policy) and peer venues, prepare anonymized artifact links and per-table/figure reproduction scripts (`./reproduce-table-1.sh`) at submission time, not after acceptance.
9. **Zero reviewer-simulator leakage.** Never paste internal review prompts, scores, or simulated rebuttal prose into the manuscript body.

---

## Internal Orchestration (W3 Sub-Chain)

`sec-paper-writing` composes rather than replaces ARIS's domain-neutral writing skills. The internal chain:

```text
NARRATIVE_REPORT.md
  → outline      (/paper-plan  — optional host skill; fallback: build the outline
                  directly from the section scaffold below)
  → draft        (/paper-write — optional host skill; fallback: draft sections
                  inline against the scaffold + Iron Rules)
  → figures      (/paper-figure /figure-spec — optional host skills; fallback:
                  plain matplotlib/tikz; every figure number traces to FACT_PACK.md)
  → audits       (/paper-claim-audit /citation-audit /integrity-forensics —
                  optional host skills; the 6-point security audit gate below is
                  MANDATORY and runs regardless)
  → compile      (/paper-compile — optional host skill; fallback: latexmk -pdf)
  → text-layer loop (/sec-paper-improve-loop — optional polish rounds on the draft)
```

The parts this skill itself owns — and which no external skill supplies — are the **security content contracts**: the threat-model chapter, the A3 evaluation section, the oracle/dedup declarations, the fact-pack write-lock, and the venue compliance appendices below. Structural paragraph blueprints may borrow `writing-systems-papers` patterns where they do not conflict with the threat-model-first order.

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
    - **USENIX Security**: `Ethical Considerations` (up to 1 page, stakeholder analysis per Menlo Report + disclosure timeline) and `Open Science` (up to 1 page, anonymized artifact inventory & reproduction instructions) immediately after main body, before references.
    - **IEEE S&P / ACM CCS / NDSS**: integrate Ethics & Data/Artifact Availability per current CFP placement rules.

---

## Pre-Submission Audit Gate

Before compiling the final PDF, run this 6-point check against `FACT_PACK.md` and the forbidden-claim source (`idea-stage/FORBIDDEN_CLAIMS.md` if materialized, else the `Forbidden-Claim & Ethics Pre-Flight Seed` section of `IDEA_REPORT.md` + `research_contract.md`):

- [ ] **Numeral Parity**: Every number in Abstract, Intro, Tables, and Conclusion matches `FACT_PACK.md` verbatim.
- [ ] **Forbidden-Claim Clean**: Zero occurrences of banned overclaims (`novel` without citation proof, `0% FP` without scope bound, `provably secure` without formal theorem + assumption list).
- [ ] **Threat-Model Consistency**: No evaluation experiment uses attacker capabilities excluded in Section 3 (or if it does, it is explicitly labeled as an out-of-model stress test).
- [ ] **Adaptive Attacker Present**: Defense/detection papers include a dedicated subsection testing A3 adaptive evasion.
- [ ] **Citation & SHA Integrity**: Every BibTeX key resolves; CVEs match `CVE-YYYY-NNNNN`; commits use 40-char SHAs.
- [ ] **Double-Blind & Policy Compliance**: No author-identifying paths, repo links, or self-citation phrasing (`in our prior work`); USENIX `Ethical Considerations` and `Open Science` appendices present when `venue: USENIX_SEC`.
