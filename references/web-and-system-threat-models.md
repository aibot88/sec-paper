# Web & Systems Security Threat Models — Reference Sheet

> *"A security paper without a threat model is a wish, not a result."*

Every security candidate in `sec-idea-creator` and every manuscript in `sec-paper-writing` must answer four questions explicitly:

1. **Who is the adversary?** (starting privileges, knowledge, vantage point, query/request budget)
2. **What security property is at stake?** (Confidentiality, Integrity, Availability, Authorization, Tenant/Context Isolation — never conflate them)
3. **What is in scope vs. out of scope?** (and why the out-of-scope exclusions are realistic)
4. **What is in the Trusted Computing Base (TCB)?** (which components, configurations, or cryptographic primitives are assumed correct)

---

## 1. Common Web & Application Security Adversary Classes

### W1 — Unauthenticated Remote Web Adversary
- **Capabilities:** Sends arbitrary HTTP/1.1, HTTP/2, HTTP/3, WebSocket, or GraphQL requests over the public internet; controls headers, cookies, query strings, bodies, and timing of its own requests.
- **Cannot:** Read other users' network traffic (unless combined with a network adversary), access server filesystem/env vars directly, or forge cryptographic signatures.
- **Typical targets:** Pre-auth RCE/SSRF, authentication bypass, cache poisoning, request smuggling, open redirect / OAuth flow hijacking.

### W2 — Authenticated Low-Privilege / Cross-Tenant Adversary
- **Capabilities:** Possesses one or more valid user/tenant accounts (`User A`, `Tenant A`) and optionally a legitimate high-privilege account in a *separate* self-owned tenant (`Admin of Tenant A`) to learn API schemas and parameter structures.
- **Goal:** Access or mutate resources belonging to `User B` or `Tenant B` (BOLA / IDOR / BFLA / cross-tenant isolation failure).
- **Critical distinction:** Using a second self-owned account to infer API structure is **in scope** for realistic Web attackers; possessing `Victim Tenant B`'s credentials or admin token is **circular and invalid** unless studying post-compromise lateral movement.

### W3 — Cross-Origin Browser / Client-Side Adversary (Web Attacker)
- **Capabilities:** Operates `https://attacker.example`; lures a victim browser to visit it; executes arbitrary JavaScript in its own origin; opens popups/iframes; sends cross-origin requests subject to SOP/CORS/SameSite rules; observes timing/frame-count side channels.
- **Typical targets:** XSS, CSRF, XS-Leaks, postMessage origin confusion, OAuth/OIDC token leakage, Service Worker / browser storage state pollution.

### W4 — Cross-Layer / Differential Parsing Adversary
- **Capabilities:** Crafts inputs that traverse a chain of intermediaries (CDN → WAF → Reverse Proxy → API Gateway → Web Framework → ORM / Template Engine / Auth Service).
- **Key mechanism:** Exploits semantic discrepancies where Component 1 (e.g., WAF or auth gateway) sees a benign/authorized request while Component 2 (e.g., backend router or serializer) executes a privileged action.

### W5 — Untrusted Third-Party Content / Indirect Prompt & Tool Adversary (LLM-Web / Agent Systems)
- **Capabilities:** Controls external data ingested by an application or agent (webpages, emails, issues, uploaded documents, third-party MCP/tool metadata) without controlling the user's direct prompt or system configuration.
- **Goal:** Hijack planning or control flow (Prompt-Flow Integrity violation), trigger over-privileged tool calls, or exfiltrate sensitive context across trust levels.

### W6 — Co-Tenant / Local Side-Channel Adversary
- **Capabilities:** Shares physical hardware (CPU cache, branch predictor, shared container host) or observes fine-grained remote network timing.
- **Rule:** If side channels are out of scope for a Web/application paper, state so explicitly and explain why (e.g., "we target logical authorization invariants; microarchitectural leakage requires co-residency and is orthogonal").

---

## 2. Three-Tier Attacker Progression for Defense & Detection Papers

Never evaluate a Web defense, WAF, sanitizer, or runtime monitor against a single static payload list. Define three attacker tiers:

| Tier | Name | Knowledge & Budget | Role in Evaluation |
|------|------|--------------------|--------------------|
| **A1** | **Static / Off-the-Shelf Attacker** | Uses existing public scanners, CVE PoCs, or standard benchmark payloads without knowing the defense. | Sanity check only — necessary but never sufficient for a top-venue claim. |
| **A2** | **State- / Workflow-Aware Attacker** | Has valid role accounts, crawls application workflows, and mutates parameters/states within a fixed request budget. | Main baseline comparison under matched request/time budget. |
| **A3** | **Adaptive White-Box Attacker** | Knows the defense's exact architecture, grammar, policy DSL, or anomaly threshold and optimizes inputs/workflows to evade it. | **Mandatory stress test.** Characterizes where the defense still holds and where its fundamental boundary lies. |

---

## 3. Paste-and-Adapt Adversary Capability Table (LaTeX / Markdown)

Include a table of this form in every `Threat Model` section and `sec-idea-creator` candidate card:

| Capability / Assumption | In Scope | Out of Scope | Notes / Justification |
|-------------------------|:--------:|:------------:|-----------------------|
| Unauthenticated HTTP/GraphQL requests | ✓ | | Standard remote entry point |
| Registering attacker-owned accounts / tenants | ✓ | | Public SaaS / multi-role Web assumption |
| Knowing backend endpoint schemas via own account | ✓ | | White-box/gray-box schema visibility |
| Adaptive evasion with full knowledge of defense (A3) | ✓ | | Evaluated in §6.3 |
| Compromising victim browser via unrelated 0-day RCE | | ✓ | Violates browser TCB |
| Direct database / OS root access on server | | ✓ | Server OS & DB engine are in TCB |
| Physical / microarchitectural co-residency side channels | | ✓ | Orthogonal to application-layer authorization |
