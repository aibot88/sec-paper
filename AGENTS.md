# sec-paper execution contract

This is an independent project, not an ARIS installation. Codex generates,
implements and executes. AntiGravity/Gemini reviews; unavailable review is
BLOCKED. Never invoke Claude Code or substitute Codex self-review.

Read `shared-references/workflow-contract.md` and
`shared-references/reviewer-contract.md` before running a research workflow.
Resolve the repository from `.aris/sec-paper.json` in the research project,
or the real path of the installed Skill symlink. All helpers live in this
repository's `tools/`; never require an ARIS checkout.

Use `python3 tools/project.py doctor --project <research-project> --live`
before unattended review. Probe failures block review; missing Docker blocks
only experiments that need it; missing TeX/PDF tools blocks submission, not
literature work. Record capabilities, sources actually accessible, scope and
resource budgets; do not invent unavailable results or reviewer receipts.

The Skills are agent-executed specifications. Tests exercise the orchestration
contracts, not the scientific truth of a future research result. Only final,
fresh Gemini audits plus deterministic artifact checks permit a
`submission-ready` statement. A test fixture is never a research acceptance.
