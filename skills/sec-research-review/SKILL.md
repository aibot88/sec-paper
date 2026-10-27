---
name: "sec-research-review"
description: "Deep adversarial review of cybersecurity, Web application security, and systems security ideas, pilots, or manuscripts from a Big-Four PC perspective (IEEE S&P, USENIX Security, ACM CCS, NDSS). Audits threat-model sanity, TCB realism, ground-truth oracles, A3 adaptive-attacker resilience, and minimum discriminating experiments."
argument-hint: "[idea-or-paper-scope] [— composed: idea-stage/IDEA_REPORT.md]"
---

# Security PC Adversarial Review (`sec-research-review`)

> **Before each reviewer slot**, follow the reviewer contract in `shared-references/reviewer-contract.md`:
> resolve invocation override → `.aris/reviewer.json` → host default (`--tier deep`).
> Pass **file paths only** (never executor-written summaries that hide flaws).
> Record actual model identity, family relation, and trace in `.aris/traces/`.

Run a deep, adversarial Big-Four Program Committee review for: **$ARGUMENTS**

---

## Overview

Generic ML review prompts ask about "model architecture, training curves, and NeurIPS/ICML baselines." On a security paper, that misses the actual desk-reject and PC-kill triggers:
- **Circular or unstated threat models** (adversary preconditions that already grant the goal, or conflating C / I / A / Authorization);
- **Unrealistic TCB or deployment assumptions**;
- **Circular or heuristic-only evaluation oracles** (HTTP 200 = bug, scanner consensus = truth, coverage/stack-hash = unique bug count);
- **Missing Adaptive Attacker (A3)** (evaluating a defense only against static A1 payloads);
- **Unified-Framework stitching** (combining A + B + C without isolating a core mechanism).

---

## Workflow

### Step 1: Gather Primary Artifacts (Cold Read Contract)

Identify the exact files for the reviewer to read directly (e.g., `idea-stage/IDEA_REPORT.md`, pilot scripts/logs, `refine-logs/FINAL_PROPOSAL.md`, or `paper/main.tex`). Do **not** summarize away failed pilots or negative findings.

---

### Step 2: Deep Adversarial Security Review (Round 1)

Dispatch to the resolved deep-tier reviewer (`ultra` for Codex, `high` for Antigravity/Gemini, or configured route):

```text
Please act as a senior Program Committee member for IEEE S&P, USENIX Security, ACM CCS, and NDSS.
Read the listed files directly. Start from the assumption that the security claim, threat model, or evaluation oracle is broken somewhere — your job is to find where.

Audit the work across these 6 security-critical dimensions:

1. Threat Model & Trust-Boundary Sanity:
   - Who is the adversary, what privileges/budget do they start with, and what is in the TCB?
   - Is any precondition circular (already granting the target capability) or unrealistic in real deployments?
   - Are Confidentiality, Integrity, Availability, Authorization, and Isolation distinguished cleanly?

2. Mechanism Insight vs. "Unified Framework" Bloat:
   - What is the single sharp security insight or classic primitive mapping?
   - Apply the Deletability Test: which components are load-bearing for the security loop, and which are decorative packaging that should be cut?

3. Ground-Truth Oracle & Deduplication Validity:
   - How does the work verify a true violation or successful defense?
   - Is there any circular labeling (HTTP status codes, unverified LLM judge, coverage/stack-hash overcounting)?
   - What is the experimental unit (root-cause bug / minimal fix SHA / independent app / origin)?

4. Baseline Fairness & Adaptive Attacker (A3) Resilience:
   - Are baselines run under matched seed state, authentication roles, and request/time budgets?
   - Once an A3 adaptive attacker knows this mechanism's parser, rules, or thresholds, what is the cheapest bypass?

5. Ethics, Authorization & Reproducibility:
   - Does any experiment touch live systems or sensitive data without consent when a local containerized testbed would suffice?
   - Are CVEs, software versions, and commit SHAs pinned?

6. Verdict & Cheapest Discriminating Next Experiment:
   - Bottom-line stance: `PROCEED` (or `PROCEED WITH REVISIONS`) vs. `ABANDON`
   - Score: X/10 (calibrated to S&P / USENIX / CCS / NDSS bar)
   - Top ranked weaknesses (FATAL / MAJOR / MINOR)
   - The single cheapest discriminating experiment that would resolve the biggest technical risk — without rewriting the core hypothesis into a bloated multi-module monster.
```

---

### Step 3: Iterative Follow-Up / Threat-Model Refinement (When Needed)

If the review raises a fatal threat-model objection that can be resolved by an **explicit, honest scope/precondition revision** (e.g., narrowing from unauthenticated remote to authenticated cross-tenant low-privilege user) or if the bottom-line stance (`proceed` vs. `abandon`) is ambiguous:
- Query the same reviewer session for a clear ruling on the explicit revision;
- Never infer a positive receipt from silence.

---

### Step 4: Output & Composed Folding

- **Standalone mode**: Write `RESEARCH_REVIEW.md` in the project root and save the full trace to `.aris/traces/sec-research-review/<date>_run<NN>/`.
- **Composed mode (`— composed: idea-stage/IDEA_REPORT.md`)**: Fold the structured critique, named risks, and cheapest discriminating experiment into `## External Critical Review` (`#external-critical-review` anchor required by `idea_discovery_gate.py`), and cite the `.aris/traces/...` path.
