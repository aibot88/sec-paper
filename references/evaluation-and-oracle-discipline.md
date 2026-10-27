# Evaluation, Oracle & Deduplication Discipline for Security Papers

This reference codifies the empirical standards required during `sec-idea-creator` Phase 5 pilots and `experiment-bridge` / `sec-paper-writing` full evaluations. It integrates lessons from **Klees et al. (*Evaluating Fuzz Testing*, ACM CCS 2018)**, modern Web fuzzing/scanning evaluations (**Atropos, USENIX Security 2024**; **Enemy of the State, USENIX Security 2012**), and security engineering practice.

---

## 1. The Oracle Rule: What Counts as Ground Truth?

A vulnerability or defense evaluation is only as credible as its **oracle** (the mechanism that decides whether a security property was violated).

### Valid Oracles
1. **Differential Policy / State Oracle**:
   - Execute action $a$ on resource $r$ owned by `Victim B` using credentials of `Attacker A`.
   - Verify violation via **authoritative backend state diff or ground-truth policy matrix** (e.g., database row mutation, unauthorized secret retrieval), not HTTP status code alone.
2. **Patch / Minimal-Fix Oracle (Klees et al., CCS'18)**:
   - On historical or known-bug corpora, group inputs by the **minimal conceptual patch** that causes the violation to disappear.
3. **Execution-Layer Sanitizer / Fault-Escalation Oracle**:
   - Observe concrete sink execution (e.g., SQL AST structural change, OS command invocation, file path escape, DOM JS execution in a real browser context) rather than regex matching on HTTP responses.
4. **Manual Root-Cause Triage with Reproducible PoC**:
   - For newly discovered vulnerabilities in real applications, every counted bug must have a minimized PoC, root-cause location, and disclosure record.

### Invalid / Circular Oracles (Strictly Forbidden)
- **HTTP 200 = Vulnerability**: custom error pages, soft redirects, and public fields routinely return `200 OK`.
- **Scanner Consensus = Ground Truth**: taking the union or intersection of Tool A and Tool B without root-cause verification only measures agreement between heuristics.
- **Unverified LLM Judge = Ground Truth**: an LLM labeling its own or another agent's output as "exploitable" without execution or state verification is circular.
- **Coverage or Unique Crashes = Bug Count**: Klees et al. (CCS'18) showed that 57,142 AFL coverage-"unique" crashing inputs on `cxxfilt` mapped to only **9 distinct patches**, and stack hashes both overcounted (≈46 hashes per bug) and dropped real bugs via hash collisions (≈16%).

---

## 2. Deduplication & Experimental Unit

Always declare the **experimental unit** before reporting numbers:

| Claim Type | Correct Experimental Unit | Wrong Unit (Inflated) |
|------------|---------------------------|-----------------------|
| Vulnerability discovery | **Distinct root-cause bugs / minimal fixes** across distinct applications | Raw crashing requests, alert count, or identical vulnerable plugin deployed across 50 sites |
| Access-control testing | **Distinct broken authorization rules / state transitions** | Number of parameter permutations hitting the same unprotected handler |
| Web measurement | **Independent origins / organizations / codebases** (with clustering documented) | Mirror domains, CDN aliases, or version clones treated as independent i.i.d. samples |

---

## 3. Budget Matching, Seeds, and Timeouts

When comparing Method A against Baseline B:

1. **Match the initial state and seed corpus**:
   - In Web testing, "seed" means **authentication state, pre-populated database records, role accounts, and starting crawl/API spec**.
   - If Method A receives valid login tokens + OpenAPI specs while Baseline B runs unauthenticated from `/`, the comparison is invalid.
2. **Report performance over time/budget, not a single arbitrary cutoff**:
   - Klees et al. demonstrated that algorithm rankings can **reverse** between short (e.g., 6h) and longer (e.g., 24h) runs.
   - Plot or tabulate progress across budget checkpoints (e.g., request budget or wall-clock time).
3. **Multiple trials for stochastic methods**:
   - Any method involving randomness (fuzzing mutations, LLM sampling, randomized scheduling) must run multiple trials and report **median + IQR / confidence intervals + non-parametric statistical tests (e.g., Mann-Whitney U)** rather than a single lucky run.
4. **One moving piece per ablation**:
   - When a system has multiple coupled components (e.g., state snapshot + key-value inference + bug oracle), disable one component at a time on identical targets to prove each component's necessity.
