---
name: "sec-idea-creator"
description: "Generate, stress-test, and pilot-validate cybersecurity, Web application security, and systems security research ideas for top venues (IEEE S&P, USENIX Security, ACM CCS, NDSS). Use when user says \"网安找idea\", \"Web安全选题\", \"sec-idea-creator\", \"security research ideas\", or wants to explore publishable attack, defense, or measurement directions."
argument-hint: "[security-direction-or-target-boundary]"
---

# Security & Web Application Research Idea Creator (`sec-idea-creator`)

> **Before each reviewer slot**, follow ARIS's selectable-reviewer contract:
> resolve invocation override → `.aris/reviewer.json` → host default with
> `reviewer_route.py` when available. **Critical independence rule:** Phase 2
> (divergent brainstorming) and Phase 4 (adversarial triage) MUST run in
> **separate, fresh sessions/threads**. Never reuse the brainstorming
> `threadId` or agent session to rank its own ideas, and never hardcode
> `acceptance_status: accepted` in static prose.

Generate, falsify, and pilot-rank publishable security research ideas for: **$ARGUMENTS**

---

## Overview

General-purpose ML ideation skills fail on cybersecurity and Web application security papers in predictable ways:
1. They treat **paper keyword gaps** ("nobody applied X to Y in the last 2 years") as research problems, missing foundational systems/Web security work and real protocol/framework invariants.
2. They oscillate between **4-module buzzword soup** ("Unified framework combining dependency graphs + 3-layer detection + blockchain provenance + risk propagation") and a **single-module dogma** that falsely rejects coupled security systems (e.g., state snapshotting + structure inference + bug oracles).
3. They equate feasibility with **GPU hours and static datasets**, whereas Web/system security lives or dies by **authorization scope, reproducible target state, and ground-truth vulnerability oracles**.
4. They force every pilot into a **single-seed, 2-hour, metric-+X% leaderboard template**, ignoring existence proofs for new attack classes, adaptive attackers for defenses, and denominator/blind-spot calibration for measurements.

This skill replaces those assumptions with a security-first discipline grounded in Big-Four (IEEE S&P, USENIX Security, ACM CCS, NDSS) reviewing standards.

---

## Constants & Defaults

- **MAX_PILOT_IDEAS = 3** — Allocate pilot engineering budget to at most 3 surviving candidates in parallel. Keep remaining feasible candidates documented with their status, not silently discarded.
- **PILOT_WALLCLOCK_BUDGET = task-matched** — Default 30 min–4 hours for deterministic PoC or small local harness checks; longer windows (e.g., ≥24h or multi-trial runs) are explicitly flagged when stochastic fuzzing/scanning variance would make a short run misleading.
- **REQUIRE_FRESH_TRIAGE_THREAD = true** — Phase 4 critique and ranking must open a **new** reviewer thread/agent with zero brainstorming history.
- **OUTPUT_DIR = `idea-stage/`** — Canonical deliverable is `idea-stage/IDEA_REPORT.md` (plus `idea-stage/FORBIDDEN_CLAIMS.md` when preparing for downstream writing).

> 💡 Override via argument, e.g., `/sec-idea-creator "multi-tenant BOLA in GraphQL gateways" — track: attack, reviewer: antigravity`.

---

## Six Iron Rules of Security Ideation

1. **Security property & trust boundary first, engineering steps second.** Every candidate must state *who* crosses *which trust boundary* under *what privileges* to violate or protect *which security property (C / I / A / Isolation / Authorization)* before listing build steps.
2. **Classic primitive mapping > Unified-framework stitching.**
   - **Encourage:** mapping a classic systems/security invariant (Control-Flow Integrity, Information-Flow Control, Least Privilege, State-Machine Consistency, Transactional Atomicity) onto a new Web/API/Agent execution surface where naive enforcement breaks.
   - **Forbid (The Unified-Framework Fallacy):** proposing a "Comprehensive / Unified / End-to-End Framework that combines A + B + C + D" from prior papers without isolating a single broken boundary or new coupled invariant.
3. **Judge modules by deletability, not module count.** Multiple components are valid when security only holds through their coupling (e.g., state navigation + input grammar inference + differential oracle). A component is bloat if deleting it leaves the core security claim intact.
4. **Separate `HYPOTHESIS_REFUTED` from `EXPERIMENT_BLOCKED`.** Lacking authorization, production tenant traffic, or a ready-made oracle blocks *that experiment design*; it is never evidence that the vulnerability or mechanism is false.
5. **No pilot without an explicit Oracle and Deduplication Unit.** HTTP 200, scanner alerts, coverage edges, stack hashes, and unverified LLM judgements are **not** ground truth. Define what constitutes a true violation and how findings are deduplicated (by root cause / minimal fix / broken invariant, never raw alert count).
6. **Evaluate by contribution track, not a universal `+X%` table.** Attack/discovery, defense/detection, and measurement/diagnostic papers require different minimum convincing evidence.

---

## Workflow

### Phase 0: Load Research Wiki & Authorization Context

Skip the wiki step if `research-wiki/` does not exist.

1. If `research-wiki/query_pack.md` exists and passes `threat_scan.py --scope strict`, read it immediately:
   - Treat recorded **Failed Ideas** as an anti-repetition banlist.
   - Treat existing **Gaps** and **Paper nodes** as starting context.
2. Extract environment and authorization constraints from `RESEARCH_BRIEF.md` or `$ARGUMENTS`:
   - Target stack (open-source Web apps, local containers, browser/extension harness, protocol implementation, or authorized testbed).
   - Explicitly forbid unconsented live testing against third-party production services during pilots.

---

### Phase 1: Security Property & Trust-Boundary Landscape Survey

Map the technical reality before brainstorming. Do **not** limit search to the last 2 years of ML venues or the first 3 pages of PDFs.

1. **Scan local papers and artifacts first**: Check `papers/`, `literature/`, and local notes.
2. **Multi-source security retrieval**:
   - **Security & systems venues** across a **10–15 year window** for foundational mechanisms plus the **last 3 years** for active baselines: IEEE S&P, USENIX Security, ACM CCS, NDSS, PETS,IMC, OSDI/SOSP, ICSE/FSE, WWW.
   - **Normative & implementation sources**: RFCs / W3C specs, framework documentation, security advisories, NVD (`CVE-YYYY-NNNNN`), and actual fix commits (40-char git SHAs).
   - For the closest 10–15 papers, inspect **Threat Model, System Assumptions, Evaluation Setup, False Positives/Negatives, and Limitations** — never stop at the abstract.
3. **Deconstruct prior work by mechanism** (following the structured lens pattern):
   - **Problem & Broken Invariant**: what trust boundary failed?
   - **Key Insight & Primitive Mapping**: what security primitive was enforced or bypassed?
   - **Evaluation Oracle & Blind Spots**: how did they label truth, what baselines did they beat, and what did their threat model exclude?
4. **Identify genuine security gaps** (distinguishing real gaps from fake ones):
   - **Real gaps:**
     - **Cross-layer semantic differentials** (e.g., CDN / reverse proxy / API gateway / backend ORM / browser DOM parse the same request, identity, or state differently).
     - **Untested assumptions in prior defenses** (e.g., assuming honest tool metadata, static role tables, or single-step stateless requests).
     - **Classic primitive breakdown** (why existing CFI / IFC / RBAC / taint tracking fails on asynchronous, stateful, or LLM-integrated Web workflows).
     - **Diagnostic / measurement unknowns** (contradictory claims across papers or unmeasured prevalence under a defensible denominator).
   - **Fake gaps to reject immediately:**
     - "Paper X did this on PHP; nobody wrote a paper doing the exact same thing on framework Y" (unless Y's architecture introduces a distinct technical obstacle).
     - "Existing papers do A, B, and C separately; nobody combined A+B+C into a unified framework."

---

### Phase 2: Divergent Hypothesis Generation (Brainstorm Session)

Use a generation agent (or the configured reviewer backend in **brainstorm mode**) to generate **8–12 concrete candidates** across three tracks:
- **Track A — Attack / Vulnerability Discovery** (new attack class, cross-layer bypass, automated bug finding with a new oracle)
- **Track B — Defense / Runtime Enforcement / Detection** (architectural isolation, policy enforcement, low-FP detection resilient to adaptive attackers)
- **Track C — Measurement / Diagnostic / Replication** (empirical characterization, root-cause taxonomy, or refuting an assumed security property)

Prompt contract for Phase 2:

```text
You are a senior systems and Web security researcher (IEEE S&P / USENIX Security / ACM CCS / NDSS PC level).

Research direction: [user's direction]
Landscape & mechanism map from Phase 1:
[paste Phase 1 mechanism map, prior assumptions, and cross-layer friction points]

Generate 8-12 concrete research candidates spanning Attack/Discovery, Defense/Enforcement, and Measurement/Diagnostic tracks where appropriate.

For EACH candidate, provide:
1. Track: Attack / Defense / Measurement
2. Broken Invariant or Security Property: one sentence stating WHO (adversary capability/privilege) crosses WHICH trust boundary to violate or enforce WHICH property (Confidentiality, Integrity, Availability, Authorization, Isolation).
3. Core Technical Insight: what non-obvious mechanism or cross-layer interaction makes this work? (If mapping a classic systems security primitive to a new Web/application surface, name both the primitive and the non-trivial obstacle.)
4. Threat Model Snapshot:
   - Adversary capabilities & starting privilege
   - In-scope vs. Out-of-scope assumptions
   - Trusted Computing Base (TCB)
5. Minimum Discriminating Pilot:
   - Target harness (local open-source apps / synthetic differential testbed / trace corpus)
   - Ground-Truth Oracle (how a true violation or correct defense is verified without circular self-labeling)
   - Deduplication / Experimental Unit (root cause / patch / state transition / independent app)
   - What outcome SUPPORTS vs. REFUTES the hypothesis

Hard constraints on brainstorming:
- FORBID "Unified / Holistic / Comprehensive Framework combining A + B + C" ideas.
- Do NOT reject an idea for needing 2-3 coupled components if removing any component breaks the security loop (e.g., state driver + structure inference + bug oracle); DO reject decorative components (e.g., bolting on blockchain or an LLM summarizer when deterministic logic suffices).
- Do NOT assign uncalibrated probability numbers ("50-50 risk") or fake novelty scores ("8.5/10"). State the concrete technical unknown instead.
```

---

### Phase 3: Mechanical Consolidation & Three-Way Status Gate

> **Phase 3 does NOT eliminate ideas on subjective taste.** It deduplicates
> candidates, attaches prior-work/ethics notes, and classifies operational
> status cleanly.

1. **Cluster near-duplicates** that test the same underlying invariant on the same boundary.
2. **Three-way feasibility & ethics classification** (never conflate experimental blockage with falsification):
   - **`FEASIBLE_NOW`**: can be piloted in an authorized local/containerized/public-artifact environment within reasonable wall-clock and engineering effort.
   - **`EXPERIMENT_BLOCKED`**: hypothesis may be valid, but the proposed test requires unconsented live systems, unavailable proprietary tenant data, or an unbuilt oracle. **Action:** keep the hypothesis alive and either redesign the pilot around an open-source/controlled reproduction or mark as blocked pending environment setup.
   - **`HYPOTHESIS_REFUTED_OR_DUPLICATE`**: objectively covered under identical threat assumptions by a verified prior paper/spec, or contains a self-contradictory threat model (e.g., adversary already possesses the target secret/privilege in the precondition).
3. **Attach structured annotations** (do not silently drop):
   - `closest_prior_work`: verified citations/CVEs/commits and the exact assumption where this candidate differs.
   - `oracle_risk`: what could cause false positives, false negatives, or circular evaluation.
   - `deletability_check`: for multi-component ideas, what fails if each component is removed.

---

### Phase 4: Fresh-Context Adversarial Triage & Root-Cause Novelty Check

**CRITICAL:** Open a **fresh** reviewer session/thread (never reuse Phase 2's `threadId`). Pass only the consolidated candidate cards and Phase 1–3 evidence notes. Run the steps in this exact order so the fast cross-model triage gates the expensive multi-source `/novelty-check`:

1. **Step 4.1 — Fresh-context adversarial triage (Reviewer 排序初筛)**:

```text
Read the candidate set below cold. You did NOT generate these ideas.

For each candidate, audit strictly against security reviewing standards:
1. Circularity & Threat-Model Sanity:
   - Does the attacker precondition already grant the goal?
   - Are Confidentiality, Integrity, Availability, and Authorization stated precisely rather than blurred?
   - Is the TCB realistic?
2. Anti-Stitching & Deletability:
   - Is this a genuine mechanism or a "Unified A+B+C" combination of existing defenses?
   - Which component can be deleted without breaking the core claim?
3. Adaptive Attacker Test (for Defense / Detection candidates):
   - Once an A3 adaptive attacker knows this defense/detector's rules, parser, or thresholds, what is the cheapest evasion or bypass?
4. Oracle & Baseline Validity:
   - Is the proposed ground-truth oracle independent of the tool's own heuristics?
   - What is the strongest realistic baseline, and under what matched budget (requests, time, privileges, seed state) will they be compared?
5. Explicit Claim Revision (Allowed — with provenance):
   - Unlike rigid "rank; do not rewrite" rules, if a candidate fails under an overly broad precondition (e.g., unauthenticated remote) but holds under a realistic narrower threat model (e.g., authenticated low-privilege cross-tenant user), state the explicit revision:
     `Original Claim -> Revised Threat Precondition -> New Discriminating Pilot`.
   - Forbid stealth scope-shrinking that hides a refutation.

Rank all feasible candidates by expected scientific information gained per unit of pilot effort, and shortlist the top 3-4 candidates for deep root-cause novelty verification.
```

2. **Step 4.2 — Root-cause novelty check (`/novelty-check` on top shortlist)**:
   - Invoke `/novelty-check` on each shortlisted candidate from Step 4.1.
   - Verify whether the **mechanism and broken invariant** (not just the target product name) already appear in S&P/USENIX/CCS/NDSS/WWW/ICSE papers, RFCs, or public vulnerability writeups.
   - Finding a known vulnerability class in one more web app is a bug report, not a research paper — unless the candidate demonstrates a **new root-cause mechanism, a systematic cross-framework blind spot, or a generalizable detection/defense principle**.
3. **Step 4.3 — Select Pilot Slate (Top 2–3)**:
   - Combine the fresh-context reviewer ranking with `/novelty-check` verdicts and select the top `MAX_PILOT_IDEAS` (2–3) surviving candidates for Phase 5 pilots. Keep unselected feasible candidates recorded as `DEFERRED_BUDGET`.

---

### Phase 5: Minimal Discriminating Pilots (Track-Specific & Oracle-First)

Run small, controlled pilots on the top 2–3 candidates to obtain empirical or formal signal before full implementation.

> **Never skip Phase 5 merely because "no GPU is available."** Most Web and
> systems security pilots run on CPU, containers, browser automation, traffic
> replay, or static/dynamic program analysis harnesses.

#### Step 5.1 — Lock the Pilot Contract Before Running
For each selected candidate, write down:
- **Target & Environment**: exact software versions, container image / git commit SHA (`40-char SHA`), role accounts, and initial state.
- **Ground-Truth Oracle**:
  - *Differential / State Oracle*: unauthorized cross-account state mutation or data read verified against ground-truth authorization policy.
  - *Patch / Root-Cause Oracle*: input triggers violation before fix commit `<SHA>` and ceases after the minimal fix (following Klees et al., CCS'18).
  - *Formal / Property Check*: concrete counterexample trace produced by model checker / solver and replayed on the real implementation.
- **Deduplication & Experimental Unit**: count by **independent root cause / broken invariant / application**, never by raw HTTP responses, coverage edges, or stack hashes.
- **Matched Budget & Variance Control**:
  - Match request count, wall-clock window, authentication setup, and seed state across baseline and candidate.
  - If the method is stochastic (fuzzing, LLM-guided probing, randomized scheduling), run multiple trials or explicitly label a single run as **existence/mechanism smoke only** — never claim comparative superiority from a single short trial.

#### Step 5.2 — Minimum Evidence by Track

| Track | What the Pilot MUST Demonstrate | What Does NOT Count as Positive Signal |
|---|---|---|
| **Attack / Discovery** | At least **1 end-to-end reproducible violation** of the stated security property under the declared threat model, with a clear causal trace explaining *why* existing defenses/checks missed it. | Raw crash/alert counts without root-cause triage; HTTP 200 responses without authorization-policy verification; bugs requiring admin misconfiguration outside the threat model. |
| **Defense / Detection** | (1) Blocks/detects known true positives, (2) preserves benign workflows (false-positive check), (3) survives at least one **A3 adaptive bypass probe** aimed at its core mechanism, and (4) reports runtime/deployment overhead. | High F1 on a synthetic dataset where ground truth comes from another scanner; beating only a strawman baseline with no adaptive attacker test. |
| **Measurement / Diagnostic** | Well-defined sampling frame and denominator, validated measurement oracle on a manually audited subset (precision/blind-spot check), and a non-trivial finding that changes how the community understands the threat or defense. | Scraping N websites/repos and reporting unverified scanner hits as "X% of the Web is vulnerable." |

#### Step 5.3 — Deploy Parallel Pilots (`/run-experiment`)
Invoke `/run-experiment` to launch the 2–3 isolated pilot harnesses in parallel (e.g., separate Docker Compose stacks, namespaces, browser contexts, or worker nodes):

```text
/run-experiment [Pilot 1 harness command — isolated target/port/container]
/run-experiment [Pilot 2 harness command — isolated target/port/container]
/run-experiment [Pilot 3 harness command — isolated target/port/container]
```

Ensure strict state isolation between concurrent pilots (never run two stateful Web scanners against the same mutable database instance at the same time).

#### Step 5.4 — Monitor & Collect Evidence (`/monitor-experiment`)
Use `/monitor-experiment` to track pilot progress, enforce wall-clock budgets, and collect structured artifacts (state diffs, reproduction traces, false-positive logs, timing/overhead metrics):

```text
/monitor-experiment [session-or-target]
```

If a pilot exceeds its declared timeout without reaching the target state, stop it and record the truncated observation as `UNDERPOWERED_OR_BLIND` rather than silently fabricating a negative verdict.

#### Step 5.5 — Four-State Pilot Verdict & Evidence-Based Re-Ranking
1. **Assign a four-state verdict** to each completed pilot (replacing binary `POSITIVE / NEGATIVE`):
   - **`SUPPORTED`**: pilot confirms the causal mechanism and satisfies the track's minimum evidence bar.
   - **`REFUTED`**: controlled experiment falsifies the core hypothesis. Document whether this yields a **publishable negative/diagnostic finding** (e.g., proving a widely assumed attack/defense premise false under realistic conditions) or a dead end to archive.
   - **`UNDERPOWERED_OR_BLIND`**: harness failed to reach target state, sample was too small, or oracle was too noisy to decide. Only allocate one more pilot iteration if the specific blindness can be fixed cheaply.
   - **`BLOCKED_ETHICS_OR_ENV`**: cannot proceed safely/legally in the current environment; requires local reproduction or scope change.
2. **Re-rank candidates based on empirical/formal evidence**:
   - Update the candidate ranking using verified pilot outcomes and information gain.
   - A candidate with a clean, oracle-verified reproduction (`SUPPORTED`) or a high-value diagnostic refutation outranks a theoretically appealing idea whose pilot remained `UNDERPOWERED_OR_BLIND`.

---

### Phase 6: Output — Security Idea Report & Fact-Pack Seed

Write the canonical report to `idea-stage/IDEA_REPORT.md`.

**Lead every candidate with its Security Property & Threat Boundary Card**, followed by a plain-language 2–4 step description of what we actually build, instrument, or measure.

```markdown
# Security Research Idea Report

**Direction**: [user's research direction]
**Date**: [YYYY-MM-DD]
**Candidates evaluated**: X generated → Y feasible after Phase 3 → Z piloted → W recommended
**Review provenance**: Phase 2 generator = [model/session], Phase 4 fresh-context reviewer = [model/session]

## 1. Security Landscape & Broken Invariants
[Summarize key prior mechanisms, their hidden assumptions, and the exact cross-layer or primitive-mapping gaps]

## 2. Recommended Candidates (Ranked)

### Candidate 1: [Title] — [Track: Attack / Defense / Measurement]
1. **Security Property & Problem Type**: [One sentence: which C/I/A/Authorization/Isolation property breaks or is enforced, and why it matters]
2. **Trust Boundary & Threat Preconditions**:
   - **Adversary**: [privileges, knowledge, network/host position]
   - **In Scope**: [...]
   - **Out of Scope**: [...]
   - **TCB / Trust Assumptions**: [...]
3. **Core Claim, Classic Primitive Mapping & Closest Prior Work**:
   - **Mechanism (2–4 plain steps)**: [what we actually build, probe, or measure]
   - **Closest Neighbors**: [Papers / CVEs / Specs] → **Exact Differentiation**: [why prior work fails or does not cover this boundary]
   - **Deletability Check**: [why each component is necessary]
4. **Minimal Evidence, Oracle & Deduplication Unit**:
   - **Oracle**: [how true violations/defenses are verified]
   - **Experimental Unit**: [root cause / patch SHA / app / tenant flow]
   - **Adaptive Attacker Probe (if Defense/Detection)**: [how A3 tries to bypass and how we test it]
5. **Budget & Key Technical Unknown**:
   - **Pilot Setup**: [containers / apps / wall-clock / trial count]
   - **Primary Unknown**: [the #1 question the pilot resolves]
6. **Pilot Verdict & Next Step**:
   - **Verdict**: `SUPPORTED` | `REFUTED` | `UNDERPOWERED_OR_BLIND` | `BLOCKED_ETHICS_OR_ENV`
   - **Empirical / Formal Evidence**: [exact reproduction trace or numbers]
   - **Claim Revision Log (if any)**: [Original claim → Revised claim]

## 3. Pilot Comparison Table
| Candidate | Track | Target / Harness | Oracle & Unit | Adaptive / Counterexample Check | Verdict |
|-----------|-------|------------------|---------------|---------------------------------|---------|
| ...       | ...   | ...              | ...           | ...                             | ...     |

## 4. Refuted, Blocked, and Deferred Candidates (Anti-Repetition Memory)
| Candidate | Status (`REFUTED` / `BLOCKED` / `DEFERRED`) | Exact Technical or Operational Reason |
|-----------|---------------------------------------------|---------------------------------------|
| ...       | ...                                         | ...                                   |

## 5. Forbidden-Claim & Ethics Pre-Flight Seed
- **Forbidden Claims (Do NOT write in downstream paper)**:
  - [e.g., Do not claim "zero false positives in general"; bound to tested workflow classes]
  - [e.g., Do not call mechanism "novel" until DBLP + RFC + advisory cross-check is locked]
- **Responsible Disclosure & Ethics Plan**:
  - [Local-only reproduction / 90-day vendor disclosure plan / Menlo Report stakeholder notes]
```

---

### Phase 7: Write Ideas to Research Wiki (If Active)

If `research-wiki/` exists and `research_wiki.py` is available, record both recommended (`proposed`) and refuted/eliminated (`archived`) candidates via `upsert_idea` so future runs inherit the dead-end banlist and threat-model revisions.

---

## Composing with Downstream Security Workflow

```text
/sec-idea-creator "direction"      → Security-property cards + Oracle-backed pilots + Forbidden-claim seed
/experiment-bridge                 → Full benchmark / target harness implementation & multi-trial evaluation
/auto-review-loop                  → Adversarial iteration (with A3 adaptive-attacker & oracle audits)
/sec-paper-writing                 → Big-Four manuscript drafting (Threat Model table, Fact Pack, Ethics & Open Science)
```
