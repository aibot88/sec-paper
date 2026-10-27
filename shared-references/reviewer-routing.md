# Standalone reviewer routing

Only AntiGravity with a Gemini identity is supported by this independent
deployment. `python3 tools/reviewer_route.py --project PROJECT --host codex`
resolves inline/project/default Gemini settings. `tools/review.py` invokes the
bundled bridge directly, so MCP registration is optional for CLI execution.
No Claude CLI or Codex self-review fallback. See [reviewer-contract.md](reviewer-contract.md).
