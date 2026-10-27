---
name: "sec-research-lit"
description: "Security, Web application security, and systems security literature & specification review. Searches Big-Four security venues (IEEE S&P, USENIX Security, ACM CCS, NDSS), DBLP, RFC/W3C specs, NVD CVEs, and fix commits, decomposing prior work by trust boundary, classic primitive mapping, and evaluation oracle."
argument-hint: "[security-topic] [— sources: all | web | local | zotero | semantic-scholar | openalex] [— composed: idea-stage/IDEA_REPORT.md]"
---

# Security Literature, Specification & Advisory Review (`sec-research-lit`)

Research topic: **$ARGUMENTS**

---

## Overview

Unlike generic ML literature surveys that scan only the last 2 years of arXiv preprints or read only the first 3 pages of PDFs, `sec-research-lit` maps **both academic security mechanisms and normative/implementation reality**:
1. **Academic Security & Systems Venues (10–15 year foundational window + last 3 years active frontier)**: IEEE S&P, USENIX Security, ACM CCS, NDSS, PETS, IMC, OSDI/SOSP, ICSE/FSE, WWW.
2. **Normative Specifications & Implementation Artifacts**: IETF RFCs, W3C specs, OWASP/framework documentation, NVD (`CVE-YYYY-NNNNN`), GitHub Security Advisories, and 40-char fix commit SHAs.
3. **Deep Section Reading**: For the top 10–15 closest papers, inspect **Threat Model, System/Deployment Assumptions, Evaluation Setup, Ground-Truth Oracle, False Positives/Negatives, and Limitations** — never stop at the abstract or "Future Work" wishlist.

---

## Constants & Sources

- **PAPER_LIBRARY** — Check `papers/`, `literature/`, or path in `AGENTS.md`.
- **SOURCES = `all`** — Supports `zotero`, `obsidian`, `local`, `web`, `semantic-scholar`, `deepxiv`, `exa`, `gemini`, `openalex`, `all` (identical source detection contract to ARIS `/research-lit`).
- **COMPOSED_TARGET** — When invoked with `— composed: idea-stage/IDEA_REPORT.md`, fold output directly into the `## Literature Landscape` (`#literature-landscape`) section of `idea-stage/IDEA_REPORT.md` instead of emitting a standalone file.

---

## Workflow

### Step 1: Multi-Source Retrieval & Citation Pinning

1. **Local & Library Scan**: Check Zotero/Obsidian (if configured) and local PDFs in `papers/` or `literature/`.
2. **Academic Venue Search (DBLP + Scholar / S2 / OpenAlex / WebSearch)**:
   - Run 5+ distinct technical query formulations covering both **security mechanism terms** (e.g., *state-aware fuzzing*, *information flow control*, *capability enforcement*, *differential parsing*) and **vulnerability/surface terms** (e.g., *BOLA/IDOR*, *request smuggling*, *prompt-flow integrity*, *cross-tenant cache*).
   - Cross-check venue, year, and author list against **DBLP** (`https://dblp.org`) and official USENIX / NDSS / DOI pages. Never fabricate BibTeX from memory.
3. **Specification & Vulnerability Grounding**:
   - Locate relevant RFCs (`RFC NNNN`), W3C specifications, and representative real-world CVEs (`CVE-YYYY-NNNNN`) or patch commits (`40-char SHA`) that instantiate the failure mode.

---

### Step 2: Mechanism & Trust-Boundary Deconstruction

For each key paper or system in the top 10–15 neighbors, extract a structured 5-point card:
1. **Problem & Broken Invariant**: Which security property (C / I / A / Authorization / Isolation) fails, and across which trust boundary?
2. **Threat Model & Hidden Assumptions**: What adversary capabilities are in scope? What does the TCB silently assume (e.g., single-tenant DB, synchronous request parsing, honest tool metadata, unencrypted traffic visibility)?
3. **Classic Systems Primitive Mapping**: Does the paper adapt a classic primitive (e.g., CFI → Prompt-Flow Integrity; SELinux/Least Privilege → tool policy DSL; IFC → planner/executor separation; snapshot fuzzing → stateful Web apps)?
4. **Evaluation Oracle & Baselines**: How did they establish ground truth (state diff, patch SHA, sanitizer sink, manual audit)? Did they test an **A3 Adaptive Attacker**?
5. **Failure Regimes & Blind Spots**: Under what realistic conditions does their approach produce false positives, false negatives, or prohibitive overhead?

---

### Step 3: Build the Security Landscape & Genuine Gap Map

Synthesize findings into four structured blocks:

1. **Sub-Direction Taxonomy (by Mechanism, not Buzzword)**:
   - e.g., Architectural Isolation vs. Policy/Capability Enforcement vs. Runtime Behavioral/Differential Detection vs. Static/Symbolic Verification.
2. **Assumption Friction Matrix**:
   - Table comparing representative works across: `Target Surface | Adversary Tier (A1/A2/A3) | TCB Assumption | Oracle Type | Unresolved Blind Spot`.
3. **Genuine Research Gaps vs. Fake Gaps**:
   - **Genuine Gaps (Keep)**:
     - Cross-layer semantic discrepancies where two components parse identity, state, or privileges differently;
     - Untested assumptions that break under multi-tenant, asynchronous, or adaptive-attacker conditions;
     - Classic security primitives that fail to transfer cleanly due to a concrete technical obstacle;
     - Unmeasured real-world prevalence under a defensible denominator and validated oracle.
   - **Fake Gaps (Explicitly Reject)**:
     - *"Unified A+B+C Framework"*: combining orthogonal prior defenses without a new coupled invariant;
     - *"Same tool, new target name"*: re-running a known method on a slightly different framework without a new technical obstacle.
4. **Verified Reference & Artifact Pack**:
   - Verified BibTeX keys/URLs, RFC numbers, CVE IDs, and candidate open-source target repositories/benchmarks for pilot testing.

---

### Step 4: Output & Research Wiki Ingestion

- **Standalone mode**: Write to `LIT_LANDSCAPE.md` (or user-specified path).
- **Composed mode (`— composed: idea-stage/IDEA_REPORT.md`)**: Write/update the `## Literature Landscape` section (`#literature-landscape` anchor required by `idea_discovery_gate.py`).
- **Research Wiki (if `research-wiki/` exists)**: Ingest verified papers and genuine gaps via `research_wiki.py` so downstream `/sec-idea-creator` and `/sec-novelty-check` inherit them.
