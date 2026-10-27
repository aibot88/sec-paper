# sec-paper: Cybersecurity, Web & Systems Security Research Skills

> **中文文档请参阅 [`README_CN.md`](README_CN.md)。**

`sec-paper` is a standalone, composable skill suite for **cybersecurity, Web application security, and systems security** research — covering the full arc from **hypothesis discovery and oracle-backed pilot experiments (`sec-idea-creator`)** to **Big-Four manuscript drafting and pre-submission auditing (`sec-paper-writing`)**.

Target venues: **IEEE S&P (Oakland), USENIX Security, ACM CCS, NDSS**, as well as **PETS / PoPETs, ACSAC, AsiaCCS, and RAID**.

---

## Why Generic ML Research Skills Fail on Security Papers

Standard ML ideation and paper-writing workflows break down on Web and systems security because they assume:
1. **"Paper keyword gap = research problem"** (e.g., scanning only the last 2 years of ML conferences or reading only the first 3 pages of PDFs, missing foundational systems security mechanisms, RFCs, and threat-model assumptions).
2. **Either 4-module buzzword stitching or a rigid single-module ban**:
   - Without guardrails, LLMs propose *"Unified / Holistic Frameworks combining A + B + C + D"* (e.g., dependency graphs + 3-layer detection + blockchain provenance + risk scoring).
   - Conversely, naive "one mechanism only; a second module is packaging" rules wrongly kill coupled security systems that require state snapshotting + input structure inference + bug oracles to function at all (e.g., *Atropos*, USENIX Security '24).
3. **"Feasibility = GPU hours + static dataset"**, ignoring authorization boundaries, reproducible multi-role application state, and ground-truth vulnerability oracles.
4. **"Pilot = 1 seed, 2 hours, +X% metric"** — violating established fuzzing and security evaluation principles (*Evaluating Fuzz Testing*, Klees et al., ACM CCS '18) and ignoring existence proofs, adaptive attackers (**A3**), and root-cause deduplication.

---

## Six Core Disciplines in `sec-paper`

1. **Security Property & Trust Boundary First**: Every candidate starts with *who* crosses *which boundary* under *what privilege* to violate or protect *which property (C / I / A / Authorization / Isolation)*.
2. **Classic Primitive Mapping > Unified-Framework Stitching**:
   - **Encourage:** mapping classic systems security primitives (CFI, IFC, Least Privilege, State-Machine Consistency, Transactional Isolation) onto new Web/API/Agent surfaces.
   - **Forbid:** merging prior orthogonal papers into a "Unified A+B+C Framework."
   - **Deletability Test:** judge multi-component designs by whether removing a component breaks state reachability, input validity, or violation detection — not by module count.
3. **Fresh-Context Adversarial Triage**: Brainstorming (Phase 2) and critical triage (Phase 4) never share a session/thread (`threadId`), eliminating self-anchoring bias.
4. **Three-Way Operational Gate**: Strictly separate `HYPOTHESIS_REFUTED` from `EXPERIMENT_BLOCKED` (ethics/authorization/environment barrier) and `DEFERRED_BUDGET`.
5. **Oracle-First Pilots & Four-State Verdicts**:
   - Require a valid ground-truth oracle (state diff, minimal fix SHA, execution sink, or audited sample) and deduplication unit (root cause / patch, never raw HTTP 200 or alert counts).
   - Replace binary `POSITIVE / NEGATIVE` elimination with `SUPPORTED`, `REFUTED`, `UNDERPOWERED_OR_BLIND`, and `BLOCKED_ETHICS_OR_ENV`.
6. **Single Fact Pack + Forbidden-Claim Table + Adaptive Attacker (A3)**:
   - Every numeral, `CVE-YYYY-NNNNN`, and 40-char commit SHA traces to `FACT_PACK.md`.
   - Every defense/detector is stress-tested against an **A3 Adaptive Attacker** who knows the defense's rules.

---

## Repository Structure

```text
sec-paper/
├── README.md
├── README_CN.md
├── LICENSE
├── skills/
│   ├── sec-idea-creator/
│   │   └── SKILL.md          # Web & systems security ideation + oracle-backed pilot workflow
│   └── sec-paper-writing/
│       └── SKILL.md          # Big-Four manuscript scaffolding, A1-A3 eval, Ethics & Open Science gate
├── references/
│   ├── web-and-system-threat-models.md       # W1-W6 adversary classes, A1-A3 tiers, capability table
│   ├── evaluation-and-oracle-discipline.md   # Oracles, deduplication units, Klees et al. CCS'18 rules
│   ├── anti-patterns-and-forbidden-claims.md # 8 ideation & writing anti-patterns with rewrites
│   └── venues-and-ethics-2026.md             # S&P/USENIX'26/CCS/NDSS policies, 90-day disclosure, AE
├── templates/
│   ├── SECURITY_IDEA_CARD_TEMPLATE.md        # 6-field candidate card + 4-state pilot decision
│   └── FACT_PACK_AND_FORBIDDEN_CLAIMS_TEMPLATE.md
└── tools/
    └── install_sec_paper.sh                  # Non-intrusive symlink installer for ARIS / Codex / OpenCode
```

---

## Quick Start & Integration with ARIS

```bash
git clone https://github.com/aibot88/sec-paper.git ~/script/sec-paper

# Link into an ARIS / Codex project (.agents/skills/) without touching upstream ARIS git files:
bash ~/script/sec-paper/tools/install_sec_paper.sh --project /path/to/your/project

# Optional: also override /idea-creator with /sec-idea-creator in that project:
bash ~/script/sec-paper/tools/install_sec_paper.sh --project /path/to/your/project --override-idea-creator

# Or install globally for OpenCode / Codex:
bash ~/script/sec-paper/tools/install_sec_paper.sh --opencode
bash ~/script/sec-paper/tools/install_sec_paper.sh --codex
```

---

## Acknowledgements

- Multi-agent research orchestration compatible with [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep).
- Security/privacy/crypto writing conventions, threat-model tables, and fact-pack discipline informed by [euzun/security-paper-writing](https://github.com/euzun/security-paper-writing) and [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs).
- Systems-security primitive mapping and anti-stitching lessons informed by [sys-intelligence/ai-writes-a-paper](https://github.com/sys-intelligence/ai-writes-a-paper) and foundational security evaluation work (*Evaluating Fuzz Testing*, CCS '18; *Atropos*, USENIX Security '24; *Enemy of the State*, USENIX Security '12).
