# Research Brief (RESEARCH_BRIEF.md)

Read by `sec-idea-discovery` Phase 0 and `sec-research-pipeline` Stage 0.
Everything here is a constraint, not a suggestion.

## Direction
[One paragraph: the security problem area — e.g., "cross-tenant
authorization failures in API-gateway / microservice compositions"]

## Target Venue & Timeline
- Venue: [USENIX_SEC | IEEE_SP | ACM_CCS | NDSS | PETS | ACSAC]
- Target cycle: [e.g., USENIX Security '26 winter cycle]
- Hard deadline: [YYYY-MM-DD]

## Authorization Scope (REQUIRED — pipeline-wide invariant)
- [ ] local-only (default): containerized/local targets only
- [ ] consented-scope: external targets allowed ONLY as listed below
- Permitted targets: [domains/hosts/repos owned or under written consent]
- Forbidden: [production third-party services, real user data, ...]

## Available Resources
- Compute: [local workers / SSH hosts / container quota]
- Baselines & corpora: [existing scanners, benchmark suites, datasets]
- Existing code: [repos to build on, or "from scratch"]

## Constraints
- Non-goals: [what this project will not attempt]
- Disclosure obligations: [coordinated disclosure requirements]
- Other: [anonymity, collaboration, tooling constraints]
