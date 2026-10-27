---
name: "sec-experiment-plan"
description: "Turn a refined security proposal into a claim-driven, oracle-first experiment roadmap: A1/A2/A3 attacker tiers, matched-budget baselines, ablation matrix, statistical protocol, ethics checkpoints, and artifact-ready run order for Big-Four submission. Use after sec-research-refine, or when the user asks for a detailed security experiment plan, ablation matrix, or evaluation protocol."
argument-hint: "[refined-proposal-or-path] [— venue: USENIX_SEC | IEEE_SP | ACM_CCS | NDSS]"
---

# Security Experiment Plan: Claim-Driven, Oracle-First Validation (`sec-experiment-plan`)

Refine and concretize: **$ARGUMENTS**

---

## Overview

Use this skill after `sec-research-refine` stabilizes the method, when the question becomes: **what exact experiments, in what order, defend this security paper?** The output is a `claim → evidence → run order` roadmap — not a benchmark wishlist.

Security adaptation of `experiment-plan`: every experiment block must declare its **ground-truth oracle** and **experimental unit** up front, defenses must include an **A3 adaptive-attacker** block, and stochastic methods must declare their **trial-count and statistics protocol** before any run starts.

---

## Constants

- **MAX_CORE_EXPERIMENTS = 4** — Cap on headline result blocks (RQ1–RQ4).
- **TRIAL_PLAN = evidence-driven** — Plan independent trials using pilot variance, effect of interest, confidence/precision/power and budget. Ten trials may be a starting estimate, never a sufficiency guarantee. Deterministic PoCs may run once but are existence evidence, not comparative superiority.
- **OUTPUT = `refine-logs/EXPERIMENT_PLAN.md` + `refine-logs/EXPERIMENT_TRACKER.md`**.

---

## Workflow

### Phase 0: Extract Claims & Anchors

From `refine-logs/FINAL_PROPOSAL.md` (or the provided proposal), extract:
- The ≤2 core claims, each phrased as a falsifiable statement (`Under threat model T, mechanism M enforces/breaks property P with measurable effect E`).
- The frozen Threat-Model Anchor and Security Problem Anchor.
- Any claim-migration entries — the experiments must test the *revised* claim, not the original.

### Phase 1: Claim → Evidence Matrix

For each claim, define exactly what evidence convinces a skeptical PC member:

| Claim | Required Evidence | Ground-Truth Oracle | Experimental Unit | Baseline & Matched Budget |
|-------|-------------------|---------------------|-------------------|---------------------------|
| C1 | ... | State diff / patch SHA / sanitizer sink / audited sample | Root-cause bug / broken rule / independent origin | Strongest prior tool under identical seed state, auth roles, request/time budget |

**Oracle rule (non-negotiable):** an experiment whose oracle is HTTP status codes, unverified scanner/LLM judgments, coverage edges, or stack hashes is **rejected at planning time** — redesign it before scheduling.

### Phase 2: Research Questions → Experiment Blocks

Structure the evaluation as RQ1–RQ4, ordered by dependency:

| RQ | Block | Purpose | Minimum Bar |
|----|-------|---------|-------------|
| RQ1 | **Ground-Truth Effectiveness** | Does the mechanism work on verified positives/negatives? | Precision & recall (or block rate) against an oracle-verified corpus, not synthetic labels from another heuristic |
| RQ2 | **Real-World / Zero-Day Discovery** | Does it find or stop things baselines miss? | Every counted finding has a minimized PoC + root cause + dedup unit; report raw alerts → deduped TP → FP separately |
| RQ3 | **Adaptive Attacker (A3) Resilience** *(mandatory for defense/detection)* | What survives a white-box adversary? | A1 static payloads → A2 workflow-aware matched-budget → A3 adaptive tailored to the mechanism; report the degradation curve and characterize the residual channel honestly |
| RQ4 | **Overhead & Ablation** | What does it cost, and is every component load-bearing? | Runtime/memory/deployment overhead (median + IQR); one-component-at-a-time ablation proving each piece is necessary |

### Phase 3: Ablation & Budget Matrix

- **One moving piece per ablation.** Disable exactly one component on identical targets; never ablate two things at once.
- **Budget matching table:** for every comparison, pin seed state (auth tokens, pre-populated DB, crawl spec), request budget, wall-clock window, and hardware.
- **Timeout discipline (Klees et al., CCS'18):** report results at ≥2 budget checkpoints (e.g., 6h and 24h) — rankings can invert; a single cutoff is cherry-picking.
- **Statistics protocol:** predeclare the independent experimental unit, justified trial/sample count, uncertainty and a test appropriate to pairing/clustering/distribution (Mann-Whitney U only when its assumptions fit). Report effect sizes and confidence intervals; correct multiple comparisons where applicable. Single runs are smoke tests, never comparative claims.

### Phase 4: Ethics, Environment & Disclosure Checkpoints

- **Environment plan:** exact container images, app versions, 40-char commit SHAs, role accounts; verify authorization scope for every target (local/containerized only unless consent documented).
- **Live-system rule:** if any experiment touches shared/public infrastructure, it gets an explicit consent + rate-limit + non-mutating justification — otherwise redesign to local reproduction.
- **Disclosure trigger:** define the applicable vendor/venue disclosure process and embargo for a confirmed finding; a 90-day example is not a universal policy.

### Phase 5: Run Order, Tracker & Artifact Readiness

1. Order experiments by *information gain per unit effort*: oracle validation → RQ1 → RQ2 → RQ3 → RQ4. Smoke-test the harness on 1–2 targets before any sweep.
2. Write `EXPERIMENT_TRACKER.md`: one row per run — `hypothesis | command | target@SHA | oracle | trials | status | raw → deduped result | verdict`.
3. **Artifact readiness:** name the reproduction scripts now (`./reproduce-table-1.sh`, `./reproduce-figure-3.sh`) so every planned run already knows which paper artifact it feeds.
4. **Negative-result protocol:** a failed experiment lands in `REFUTED` / `UNDERPOWERED_OR_BLIND` / `BLOCKED_ETHICS_OR_ENV` with its evidence — never silently dropped; publishable negative findings are kept.

### Phase 6: Output

Write `refine-logs/EXPERIMENT_PLAN.md` containing: claims → evidence matrix, RQ blocks, ablation matrix, budget-matching table, statistics protocol, ethics/disclosure checkpoints, run order, and the artifact mapping. Update `EXPERIMENT_TRACKER.md` skeleton.
