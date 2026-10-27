# Fan-Out Pattern (sec-paper scope)

When a skill needs **breadth** — many candidate ideas, many sources, many
attack angles — the executor (Codex) may parallelize generation across
worker contexts.

## sec-paper rules

- **Generation may fan out; review never collapses into the same thread.**
  Generator shards are read-only producers: they return candidates/sources,
  never score their own output. Ranking, novelty, and acceptance stay with a
  fresh AntiGravity/Gemini session (reviewer-contract.md).
- Each shard gets a disjoint slice (track × source family, or candidate
  range) and returns structured output; the parent dedups and writes the
  shared deliverable's owned section.
- Untrusted content fetched by any shard (abstracts, wiki, advisories, web
  pages, the reference paper) passes `tools/threat_scan.py --scope strict`
  before injection into downstream context — see the injection-hygiene rules
  in workflow-contract.md.
- A shard that fails produces an explicit gap note in the section, not silent
  omission; the final review sees the coverage list.
- sec-paper currently ships no shard runner of its own; Codex-side subagents
  or sequential batches both satisfy this contract. What is forbidden is a
  single self-reviewing mega-call, not a particular fan-out transport.
