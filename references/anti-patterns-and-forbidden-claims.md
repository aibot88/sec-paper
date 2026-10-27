# Security Ideation & Writing Anti-Patterns (with Rewrites)

Use this checklist during `sec-idea-creator` Phase 4 triage and `sec-paper-writing` pre-submission audits.

---

## Ideation Anti-Patterns (Kill or Rewrite in `sec-idea-creator`)

### 1. The "Unified A+B+C+D Framework" Fallacy
- **Bad Idea**: *"Prior work studied sandboxing (ACE), privilege policies (Progent), and behavioral monitoring (MELON) separately. We propose a unified runtime defense framework combining sandboxing, dynamic privilege control, behavioral anomaly detection, and cross-agent isolation."*
- **Why it fails**: Combining orthogonal mechanisms from four recent papers is system integration, not a scientific contribution. It hides the lack of a single sharp insight and creates an un-ablatable monster.
- **Correct Rewrite**: Identify a **specific boundary where existing mechanisms fail even when deployed** (e.g., *"Static and per-call privilege policies fail when benign tool calls compose into an unauthorized cross-tenant state transition; we formalize stateful capability accumulation across tool chains"*).

### 2. The "Single-Module Dogma" Overcorrection
- **Bad Rejection**: *"This Web fuzzer needs state snapshotting, key-value inference, AND custom bug oracles — 3 modules means packaging, not novelty."*
- **Why it fails**: In systems security, reaching deep states and detecting non-crash logic flaws requires a closed loop. Rejecting coupled components kills legitimate systems like *Atropos* (USENIX Security'24).
- **Correct Rule**: Apply the **Deletability Test** — keep all components whose removal breaks state reachability, input validity, or violation detection; cut only decorative modules (e.g., blockchain logging, redundant LLM wrappers).

### 3. Confusing `EXPERIMENT_BLOCKED` with `HYPOTHESIS_REFUTED`
- **Bad Triage**: *"We cannot access production bank APIs or 100k real tenant sessions, so eliminate this cross-tenant authorization hypothesis."*
- **Why it fails**: An unethical or unavailable test environment blocks the *measurement design*, not the *technical hypothesis*.
- **Correct Rewrite**: Keep the hypothesis; pivot the pilot to a reproducible local multi-tenant testbed (open-source SaaS apps + seeded tenant roles) and record production prevalence as an explicit limitation.

### 4. Circular Threat Preconditions
- **Bad Idea**: *"Assume the attacker can modify the server's JWT verification middleware or read environment secrets; we then demonstrate privilege escalation."*
- **Why it fails**: If the attacker already compromises the TCB or holds admin-equivalent secrets, privilege escalation is trivial.
- **Correct Rewrite**: Restrict the attacker to realistic external or low-privilege capabilities (e.g., unauthenticated header manipulation or `Tenant A` user credentials) and keep the server runtime in the TCB.

---

## Manuscript & Evaluation Anti-Patterns (Fix in `sec-paper-writing`)

### 5. Defense Evaluation Without an Adaptive Attacker (A3)
- **Bad Prose**: *"Our prompt-flow / WAF defense reduces attack success rate from 89% to 2% on existing benchmark payloads."*
- **Why it fails**: Static benchmarks only test A1 attackers ignorant of the defense. Security reviewers immediately ask how an attacker who reads your paper bypasses your filter.
- **Rewritten**: *"We evaluate against three attacker tiers: (A1) static benchmark payloads, (A2) workflow-aware black-box probing under a $10^4$-request budget, and (A3) an adaptive white-box attacker tailored to our parser and policy thresholds. Under A3, attack success rises from 2.1% to 11.4% due to [specific residual channel], which we characterize in §6.3."*

### 6. Raw Alerts or HTTP Status Codes as Vulnerability Counts
- **Bad Prose**: *"Our scanner discovered 1,420 vulnerabilities across 50 targets, outperforming Baseline X by 4x."*
- **Why it fails**: Without root-cause deduplication and oracle verification, "1,420 vulnerabilities" usually means 1,400 false positives or 1,400 hits on the same 3 bugs.
- **Rewritten**: *"Across 50 targets, our tool generated 312 raw alerts, which deduplicated to 14 distinct root-cause vulnerabilities (verified via minimal PoC reproduction and patch diffing), with 19 false positives (precision 93.9%)."*

### 7. Conflating Confidentiality, Integrity, Authorization, and Availability
- **Bad Prose**: *"Encrypting session tokens in transit guarantees session security and prevents unauthorized actions."*
- **Why it fails**: Encryption (IND-CPA) does not provide integrity without authentication (AEAD/MAC), nor does transport confidentiality prevent server-side broken object-level authorization (BOLA).
- **Rewritten**: State the exact property: **Confidentiality**, **Integrity/Authenticity**, **Replay Resistance**, or **Object/Function-Level Authorization**, and tie each to the mechanism that enforces it.

### 8. Unpinned CVEs, Commits, and Vague Baselines
- **Bad Prose**: *"We tested on recent vulnerabilities in popular Java and PHP web frameworks."*
- **Rewritten**: Pin exact software versions, `CVE-YYYY-NNNNN` identifiers verified against NVD, and 40-character Git commit SHAs for every benchmarked vulnerability and patch.
