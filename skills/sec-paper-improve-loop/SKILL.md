---
name: "sec-paper-improve-loop"
description: "Post-draft autonomous improvement loop for security manuscripts: fresh-context Big-Four review → targeted LaTeX fixes → recompile → re-review, for up to N rounds. Applies the same hard gates as sec-auto-review-loop to the *text layer* (threat-model consistency, numeral parity, A3 section, forbidden claims). Use after sec-paper-writing produces a draft PDF, or when user says \"安全论文润色循环\", \"improve security paper\"."
argument-hint: "[paper-dir-or-main.tex] [— rounds: 2] [— venue: USENIX_SEC|IEEE_SP|ACM_CCS|NDSS]"
---

# Security Paper Improve Loop (`sec-paper-improve-loop`)

> **Reviewer slot**: resolve per the reviewer contract in `shared-references/reviewer-contract.md` — fresh
> context per round reading `main.tex` + `FACT_PACK.md` + appendices directly.
> Under the configured AntiGravity route, receipts are cross-family `accept`.

Improve the drafted manuscript for: **$ARGUMENTS**

---

## Overview

`sec-paper-writing` produces a draft that passed its 6-point pre-submission gate *at write time*. This loop re-verifies the draft as a **document** — the layer where different classes of bugs live: abstract-vs-table numeral drift, a threat-model table that contradicts an evaluation setup, an A3 section that summarizes but doesn't quantify, forbidden claims that crept in during section polishing.

Defaults: **2 rounds** (configurable), each = fresh review → targeted fixes → recompile → re-review.

---

## Round Structure

### Step 1 — Fresh-Context Document Review

```text
Act as a senior PC member for [VENUE]. Read main.tex and FACT_PACK.md directly.

TEXT-LAYER hard gates (a red gate fails the round regardless of polish):
1. Numeral parity — every number in Abstract/Intro/Tables/Conclusion matches
   FACT_PACK.md verbatim; flag every untraceable numeral by line.
2. Threat-model consistency — Section 3 capability table vs. what the
   evaluation actually does; any eval experiment using excluded capabilities
   must be labeled out-of-model stress test or removed.
3. A3 section presence (defense/detection) — must contain quantitative
   adaptive results, not a paragraph saying "we consider adaptive attackers".
4. Forbidden-claim scan — unbounded novelty claims, unbounded FP claims,
   "provably secure" without theorem+assumptions, unified-framework phrasing.
5. Anonymity — no author-identifying paths/links/self-citation phrasing.
6. Venue compliance — page-limit structure, required appendices present
   (Ethical Considerations + Open Science for USENIX).

Then soft-score 1-10: contribution clarity, mechanism/deletability exposition,
related-work mechanism grouping, limitation honesty.

Return: hard-gate table + score + ranked text-level issues with exact
section/line and the concrete fix for each.
```

### Step 2 — Targeted Fixes

Executor applies fixes to `.tex` only — no new experiments (evidence gaps route back to `sec-experiment-bridge`, never get papered over in prose). Maintain `FACT_PACK.md` as the write-lock: if a fix needs a number not in the fact pack, it becomes `[TBD]` or gets removed.

### Step 3 — Recompile & Re-Review

Compile via `/paper-compile` (or direct `latexmk`). Fix errors. Re-review only if the review found hard-gate reds or score < 8 — a clean round ends the loop early.

### Output

`review-stage/PAPER_IMPROVE_LOG.md`: per-round hard-gate table, score, fixes applied, final verdict (`READY` / `MAX_ROUNDS` with residual issues listed honestly).
