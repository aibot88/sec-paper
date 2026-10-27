# Wiki / Helper Resolution Chain

`research_wiki.py`, `threat_scan.py` and the other vendored helpers live in
this repository's `tools/`. Resolve the repository root in this order:

```bash
# 1. Project pointer written by install/init
SEC_PAPER="$(python3 -c 'import json,sys;print(json.load(open(".aris/sec-paper.json"))["repo_root"])' 2>/dev/null)"
# 2. Installed skill symlink — the skill file itself is a symlink into the repo
[ -z "$SEC_PAPER" ] && SEC_PAPER="$(cd "$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")")/../.." && pwd)"
```

Inside an agent-executed skill this is simpler: the SKILL.md file's own real
path already resolves into the repo (`readlink -f` on the skill path, then
`../..`).

## Behavior

- `$SEC_PAPER/tools/<helper>.py` exists → use it. Missing owned helpers block
  the step that needs them; never require an ARIS checkout.
- wiki enrichment (`research_wiki.py`) is **non-blocking**: if the store is
  unreadable, record `WARN: wiki unreachable; ideas not persisted` and
  continue — but threat-scan failures on injected wiki content are blocking
  for that content (see injection-hygiene via workflow-contract.md).
- Never copy helper code into the research project; `.aris/sec-paper.json`
  is the only pointer the project needs.
