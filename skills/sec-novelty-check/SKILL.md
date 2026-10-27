---
name: "sec-novelty-check"
description: "Verify root-cause, mechanism, and trust-boundary novelty for cybersecurity, Web application security, and systems security ideas against Big-Four papers, DBLP, RFCs, and public advisories/CVEs. Compatible with ARIS idea_discovery_gate.py."
argument-hint: "[security-idea-or-claim-description] [— composed: idea-stage/IDEA_REPORT.md]"
---

# Security Root-Cause & Mechanism Novelty Check (`sec-novelty-check`)

> **Before each reviewer slot**, follow the reviewer contract in `shared-references/reviewer-contract.md`:
> resolve invocation override → `.aris/reviewer.json` → host default with
> `reviewer_route.py`. Open a **fresh** reviewer session for Phase C.

Verify whether a proposed security attack, defense, or measurement idea is genuinely novel: **$ARGUMENTS**

---

## Core Security Novelty Principle

In cybersecurity and Web application security, novelty is judged at the level of **root-cause mechanism, trust-boundary interaction, or enforcement/detection principle** — never by product name alone:

- **NOT novel (Bug Report / Incremental Port)**: finding a known vulnerability class with a known technique in one more Web app or CMS, or stitching prior mechanisms A + B + C into a "Unified Framework."
- **NOVEL (Publishable Security Contribution)**:
  1. Exposing a **new class of cross-layer / state / protocol discrepancy** or a broken assumption in widely deployed defenses;
  2. Mapping a **classic systems security primitive** to a new execution surface by solving a non-trivial technical obstacle;
  3. Designing a **new ground-truth bug oracle, abstraction, or adaptive-resilient enforcement mechanism** that changes what can be detected or guaranteed;
  4. Conducting a **rigorous measurement or replication study** that refutes or bounds a widely believed security claim under a validated oracle.

---

## Workflow

### Phase A: Extract Falsifiable Security Claims

Decompose the candidate into 3–5 concrete technical claims:
1. **Broken or Enforced Invariant**: what exact property (C / I / A / Authorization / Isolation) and trust boundary are involved?
2. **Core Mechanism / Oracle**: what technical insight makes the attack, detector, defense, or measurement work?
3. **Threat Preconditions**: what privileges and visibility does the adversary have?
4. **Claimed Delta over Prior Work**: which specific assumption in prior papers/tools is relaxed, broken, or newly enforced?

---

### Phase B: Multi-Source Security & Specification Search

For each claim, search across **both academic and practitioner/specification sources**:

1. **Big-Four & Systems/Web Venues (DBLP + Scholar / S2 / WebSearch)**:
   - IEEE S&P, USENIX Security, ACM CCS, NDSS, PETS, IMC, WWW, ICSE/FSE, OSDI/SOSP (check both recent 2024–2026 proceedings and foundational papers from the last 10–15 years).
   - Use 3+ query formulations per claim (academic terminology + practitioner/bug-bounty terminology, e.g., both *"stateful authorization bypass"* and *"BOLA / IDOR state machine"*).
2. **Standards, Advisories & Practitioner Research**:
   - IETF RFCs / W3C specs / OWASP documentation;
   - NVD (`CVE-YYYY-NNNNN`), GitHub Security Advisories, PortSwigger / Project Zero / BlackHat / DEF CON technical whitepapers (if a practitioner whitepaper already demonstrated the exact attack mechanism, the academic paper must either formalize/measure it systematically or provide a principled defense, and must cite the whitepaper honestly).

---

### Phase C: Fresh-Agent Calibrated Novelty Verdict

Invoke the configured reviewer in a **fresh session** (`reasoning_effort: xhigh` or `ultra`), passing the candidate claims, all papers/specs/advisories found in Phase B, and the verbatim verdict limits below:

```text
=== SECURITY NOVELTY VERDICT LIMITS ===
Search exhaustively; judge calibrated. Two errors waste months equally:
passing an idea that a published paper or public advisory already contains under the same threat model, and killing a viable security idea merely because the area has neighbors.

1. Proximity is information, not a veto. Another paper studying the same protocol, Web framework, or vulnerability family is expected — judge whether the broken invariant, threat precondition, oracle, or enforcement mechanism is meaningfully distinct.
2. Reject "Target-Swap" pseudo-novelty: applying an existing scanner/prompt/rule unchanged to Product Y instead of Product X is a bug report, not a research contribution, UNLESS Product Y's architecture introduces a distinct technical obstacle that the method solves.
3. Reject "Unified A+B+C" stitching: combining three prior defenses without a new coupled security property is not a novelty delta; recommend narrowing to the single sharp interaction where prior defenses fail.
4. ABANDON requires naming the specific published paper, RFC, or public technical writeup that already establishes the same mechanism under equivalent threat assumptions. No named source, no ABANDON.
5. Crowded-but-deltaed ground is PROCEED: state the verifiable delta in one sentence (e.g., "Prior work [X] requires static role tables; this candidate enforces stateful capability flow across asynchronous callbacks").
6. Thin or contested delta is PROCEED WITH CAUTION: specify the exact framing or threat-boundary adjustment needed to make the delta carry.
```

---

### Phase D: Novelty Report & Run-State Receipt

Output the structured report (and fold into `idea-stage/IDEA_REPORT.md#novelty-verification` when `— composed: idea-stage/IDEA_REPORT.md` is set):

```markdown
## Novelty Verification

### Proposed Candidate & Threat Boundary
[1-2 sentences: security property, trust boundary, and core mechanism]

### Claim-by-Claim Prior Work & Delta Audit
1. **[Claim 1]** — Closest prior work: [Paper / RFC / Advisory] — **Verifiable Delta**: [what differs in threat model, mechanism, or oracle]
2. **[Claim 2]** — Closest prior work: [...] — **Verifiable Delta**: [...]

### Closest Prior Work Matrix
| Source (Paper / RFC / CVE) | Venue / Year | Threat Model & Mechanism Overlap | Exact Technical Difference |
|----------------------------|--------------|----------------------------------|----------------------------|
| ...                        | ...          | ...                              | ...                        |

### Overall Novelty Assessment
- **Recommendation**: `PROCEED` | `PROCEED WITH CAUTION` | `ABANDON`
- **Defensible One-Sentence Delta**: [exact sentence a PC member can verify]
- **Reviewer Citation Risk**: [which papers/advisories a reviewer will immediately bring up, and how to position against them constructively]
```

**Run-state integration (when called inside `/sec-idea-discovery` with `RESUMABLE=true`)**:
- Both `PROCEED` and `PROCEED WITH CAUTION` count as positive verdicts for `run_state.py` (`accept` for verified cross-family reviewer, `mark-provisional` for same-family Codex reviewer).
- `ABANDON` is negative: do not record a positive receipt; switch to the next surviving candidate or refine the mechanism delta.
