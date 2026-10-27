---
name: "sec-research-refine"
description: "Turn a validated security idea (attack, defense, or measurement) into a threat-model-anchored, minimal-mechanism, implementation-ready proposal via iterative fresh reviewer rounds. Use after sec-idea-creator/sec-idea-discovery, or when the user says \"细化安全方案\", \"refine security approach\", \"打磨攻击/防御思路\"."
argument-hint: "[security-problem | rough-approach] [— max rounds: N, threshold: S]"
---

# Security Research Refine: Threat-Model-Anchored Method Refinement (`sec-research-refine`)

> **Before each reviewer slot**, follow the reviewer contract in `shared-references/reviewer-contract.md`:
> resolve invocation override → `.aris/reviewer.json` → host default with
> `reviewer_route.py`. The reviewer session (`agent_id`) persists across rounds
> for continuity — unlike `sec-idea-creator` Phase 4, iterative refinement
> *benefits* from the reviewer remembering prior objections.

Refine and concretize: **$ARGUMENTS**

---

## Overview

Use this skill when the security problem is validated (pilot `SUPPORTED` or strong paper-level signal) but the technical route is still fuzzy. The goal is a **Problem & Threat Anchor → minimal mechanism → discriminating validation** document concrete enough to implement and sharp enough for a Big-Four PC.

Four principles dominate (security-adapted from `research-refine`):

1. **Freeze two anchors, not one.** An immutable **Security Problem Anchor** (broken invariant + trust boundary) AND an immutable **Threat-Model Anchor** (adversary class, privileges, TCB, authorization scope) are copied verbatim into every round. Revisions may narrow the threat model only through the explicit claim-migration log — never silently.
2. **The smallest adequate security mechanism wins.** Prefer the minimal mechanism that directly closes the broken invariant. Every component must pass the **Deletability Test**: removing it must break state reachability, input validity, or violation detection.
3. **One paper, one dominant contribution.** One sharp security thesis plus at most one supporting contribution (e.g., a reusable oracle or benchmark).
4. **Modern leverage is a prior, not a decoration.** LLM agents, learned oracles, and neural program analysis are welcome where they fit; they are forbidden as wrappers around logic that a deterministic check already solves.

```
Validated idea (SEC PROBLEM + rough APPROACH + pilot evidence)
  -> Phase 0: Freeze Security Problem Anchor + Threat-Model Anchor
  -> Phase 1: Scan grounding papers/advisories -> pick sharpest route -> write anchored proposal
  -> Phase 2 (fresh reviewer): Big-Four critique across 6 security dimensions
  -> Phase 3: Anchor check + deletability check -> revise -> rewrite full proposal
  -> Phase 4 (same reviewer session): re-evaluate revised proposal
  -> Repeat 3-4 until OVERALL SCORE >= THRESHOLD or MAX_ROUNDS reached
  -> Phase 5: Persist refine-logs/ + hand off to /sec-experiment-plan
```

---

## Constants

- **MAX_ROUNDS = 5** — Maximum review-revise rounds.
- **SCORE_THRESHOLD = 9** — Minimum overall score to stop.
- **OUTPUT_DIR = `refine-logs/`** — Round files, checkpoint, final proposal.
- **MAX_PRIMARY_CLAIMS = 2** — One dominant security claim + at most one supporting claim.
- **MAX_NEW_COMPONENTS = 3** — Soft cap on novel mechanisms; every component must pass deletability.

> Override via argument: `/sec-research-refine "problem | approach" — max rounds: 3, threshold: 9`.

---

## State Persistence (Checkpoint Recovery)

Identical contract to `research-refine`: persist `refine-logs/REFINE_STATE.json` after every phase boundary (`phase`, `round`, `agent_id`, `last_score`, `last_verdict`, `status`, `timestamp`). On restart: resume `in_progress` checkpoints younger than 24h; otherwise fresh start. Every `round-N-refinement.md` contains the **full anchored proposal**, never just incremental diffs.

---

## Workflow

### Phase 0: Freeze the Two Anchors

Extract and write verbatim — these may NOT be relaxed later without an explicit claim-migration entry:

**Security Problem Anchor**
- Broken or enforced invariant: which C / I / A / Authorization / Isolation property, across which trust boundary?
- Must-solve bottleneck: which specific assumption in existing defenses/tools is unacceptable?
- Non-goals: what this paper explicitly does not claim.
- Constraints: authorization scope, available targets, compute, venue, disclosure policy.

**Threat-Model Anchor**
- Adversary class (W1–W6 from `references/web-and-system-threat-models.md`) + starting privileges, knowledge, budget.
- In scope / out of scope / TCB.
- Ethics red lines: what may never be tested (unconsented live systems, real user data).

### Phase 1: Grounded Proposal Draft

Scan `idea-stage/IDEA_REPORT.md`, `LIT_LANDSCAPE.md`, and up to 15 local papers/advisories. Write `round-0-initial-proposal.md`:

```markdown
## Anchors
[verbatim Security Problem Anchor + Threat-Model Anchor]

## Mechanism (2–4 plain steps)
[What we actually build/probe/measure — named classic primitive mapping if any]

## Why Prior Work Fails Here
[The exact assumption each closest neighbor makes that this work relaxes/breaks]

## Core Claims (≤2) & Load-Bearing Components
[Each component + what breaks if it is deleted]

## Minimum Discriminating Validation
[Oracle, deduplication unit, baseline under matched budget, A3 probe if defense]
```

### Phase 2: Fresh Big-Four Reviewer Critique

Dispatch to the resolved reviewer (`ultra`/`xhigh`/`high` per route) with the file paths:

```text
Act as a senior PC member for IEEE S&P / USENIX Security / ACM CCS / NDSS.
Read the proposal file directly. Score 1-10 on:
1. Anchor fidelity — does the mechanism actually address the frozen broken
   invariant under the frozen threat model, or did it drift?
2. Threat-model sanity — circular preconditions, TCB realism, C/I/A/AuthZ clarity.
3. Mechanism sharpness — single sharp insight vs. "Unified A+B+C" stitching;
   deletability of each component.
4. Oracle & evaluation validity — non-circular ground truth, deduplication unit,
   matched baselines, A3 adaptive resilience (mandatory for defense/detection).
5. Ethics & reproducibility — authorization scope honored, pinned versions/SHAs.
6. Frontier leverage — is the mechanism the simplest adequate one, and does it
   use modern tooling (LLM agents, learned oracles) only where it genuinely fits?

Return: per-dimension scores, OVERALL SCORE, verdict (ACCEPT >= threshold |
REVISE), and the top 3 concrete weaknesses with the cheapest fix for each.
```

### Phase 3: Anchor Check + Deletability Check + Revision

Before rewriting:
- **Anchor drift check**: if the revision changes the broken invariant or threat preconditions, it must be recorded as an explicit claim-migration entry (`Original -> Revised -> Why`), or rejected.
- **Deletability sweep**: for every component, write one line stating what security property fails if it is removed. Remove components with no answer.
- Rewrite the **full** proposal into `round-N-refinement.md`.

### Phase 4: Same-Session Re-Evaluation

Query the **same** reviewer session (`agent_id` persisted) on the revised proposal. The reviewer checks whether its prior objections were actually fixed — not restated. Repeat Phases 3–4 until `OVERALL >= SCORE_THRESHOLD` or `MAX_ROUNDS`.

### Phase 5: Persist & Hand Off

Write:
- `refine-logs/FINAL_PROPOSAL.md` — the final anchored proposal (this is the artifact `sec-idea-discovery`'s evidence gate checks).
- `refine-logs/REVIEW_SUMMARY.md` — every round's scores, objections, and fixes.
- `refine-logs/REFINEMENT_REPORT.md` — what was rejected and why (incl. claim-migration log).
- `refine-logs/score-history.md`.

Then hand off to `/sec-experiment-plan` (or `/sec-research-refine-pipeline` runs it automatically).
