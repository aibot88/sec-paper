# Security Idea Card Template (6-Field Standard)

Use this card for every candidate evaluated in `sec-idea-creator`.

---

## Candidate #[N]: [Short Descriptive Title]

### 1. Security Property & Track
- **Track**: `Attack / Discovery` | `Defense / Detection` | `Measurement / Diagnostic`
- **Broken or Enforced Property**: [One sentence naming the exact C / I / A / Authorization / Tenant-Isolation invariant]

### 2. Trust Boundary & Threat Preconditions
- **Adversary Class**: [e.g., W2 Authenticated Low-Privilege Cross-Tenant User / W4 Differential Parser Attacker]
- **Starting Capabilities & Budget**: [accounts, network vantage point, request budget]
- **In Scope**: [...]
- **Out of Scope**: [...]
- **Trusted Computing Base (TCB)**: [...]

### 3. Core Claim, Classic Primitive Mapping & Closest Prior Work
- **What We Actually Do (2–4 plain steps)**:
  1. [...]
  2. [...]
  3. [...]
- **Classic Systems/Security Primitive Mapped (if applicable)**: [e.g., CFI / IFC / Least Privilege / State-Machine Inference → Web/API/Agent surface]
- **Closest Prior Work**: [Paper / RFC / CVE / Commit SHA]
- **Exact Differentiation**: [Which assumption in prior work breaks here?]
- **Deletability Check**: [For each component, state what fails if it is removed]

### 4. Minimal Evidence, Oracle & Deduplication Unit
- **Ground-Truth Oracle**: [Backend state diff / Minimal patch SHA / Sanitizer sink / Audited subset]
- **Deduplication / Experimental Unit**: [Distinct root cause / patch / broken rule / independent origin]
- **Baseline & Matched Budget**: [Strongest realistic baseline under identical seed state, auth, and request/time budget]
- **Adaptive Attacker Probe (A3, required for Defense/Detection)**: [How an attacker who knows our mechanism tries to evade it]

### 5. Budget & Primary Unknown
- **Pilot Harness**: [Containerized apps / benchmark / trace corpus]
- **Wall-Clock & Trial Plan**: [e.g., 2h deterministic PoC or 10 trials × 4h stochastic run]
- **Primary Unknown to Resolve**: [The single highest-value question this pilot answers]

### 6. Pilot Verdict & Claim Provenance
- **Verdict**: `SUPPORTED` | `REFUTED` | `UNDERPOWERED_OR_BLIND` | `BLOCKED_ETHICS_OR_ENV`
- **Observed Signal**: [Concrete reproduction or measurement summary]
- **Explicit Claim Revision Log (if any)**:
  - *Original Claim*: [...]
  - *Revised Claim & Threat Precondition*: [...]
  - *Why This Is Not Stealth Scope-Shrinking*: [...]
