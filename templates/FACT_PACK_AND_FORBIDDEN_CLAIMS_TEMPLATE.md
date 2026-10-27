# Single Fact Pack & Forbidden-Claim Table Template

Maintain this file (`FACT_PACK.md`) as the single source of truth from pilot completion through camera-ready submission. Every numeral, CVE, commit SHA, and comparative claim in the manuscript must trace here.

---

## 1. Benchmark & Target Corpus Provenance

| Target ID | Application / Dataset | Exact Version | Git Commit SHA (40-char) / DOI | Deployment Mode | Auth / Seed State |
|-----------|-----------------------|---------------|--------------------------------|-----------------|-------------------|
| T01       | [App Name]            | `vX.Y.Z`      | `<40-char-sha>`                | Local Docker    | 2 tenants, 3 roles|

---

## 2. Verified Vulnerability / Result Ledger

| Finding ID | Target | Root-Cause Location | Oracle Used | CVE / Advisory Status | Minimal Fix SHA | Counted as Unique Bug? |
|------------|--------|---------------------|-------------|-----------------------|-----------------|------------------------|
| B01        | T01    | `path/to/file:L120` | State diff  | `CVE-YYYY-NNNNN`      | `<40-char-sha>` | Yes (1)                |

---

## 3. Headline Metrics (Paste-Ready & Scope-Bounded)

- **Raw Alerts Generated**: `[N_raw]`
- **Deduplicated True-Positive Root Causes**: `[N_tp]` (verified via `[Oracle]`)
- **False Positives**: `[N_fp]` (Precision: `[XX.X%]` on `[Benchmark/Corpus]`)
- **Performance under Adaptive Attacker (A3)**: `[Metric changes from X% (A1/A2) to Y% (A3)]`
- **Runtime / Memory Overhead**: `[Median +XX.X%, IQR XX.X% across N trials]`

---

## 4. Forbidden-Claim Table (Enforced During Writing & Review)

| Forbidden Claim (NEVER Write) | Why It Is Invalid | Permitted Scope-Bounded Rewrite | Evidence Source |
|-------------------------------|-------------------|---------------------------------|-----------------|
| "Our method is novel / the first to..." (before full literature + DBLP lock) | Unverified priority claim invites easy reviewer refutation | "To our knowledge, we are the first to formalize and evaluate [specific mechanism] under [specific threat model], extending [prior work]." | Phase 4 Novelty Check |
| "Zero false positives" (unbounded) | Only holds on tested deterministic oracles/targets | "We observed zero false positives across the [N] tested applications under our differential state oracle; false positives can still arise when [condition]." | Evaluation §6.2 |
| "Outperforms Baseline B" (from a single short fuzzing/probing run) | Stochastic variance and timeout inversions (Klees et al., CCS'18) | "Across [N] independent trials of [T] hours, our method achieves a median of [X] vs. [Y] ($p = ...$, Mann-Whitney U)." | Evaluation §6.1 |
| "统一/全栈防御框架结合了 A+B+C" | Triggers the Unified-Framework stitching anti-pattern | "Our coupled enforcement loop pairs [Component 1] with [Component 2] to preserve [Security Invariant] across [Trust Boundary]." | Design §4 |
