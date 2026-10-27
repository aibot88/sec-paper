# Third-party provenance

The following implementations were vendored/adapted from
[ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep),
upstream checkout reference `18bceb3c71c638bef58096274e1c9a6d323dbc0a`
(reference recorded during this repair; the previous unpinned import was made
earlier and its exact historical source commit was not recorded):

- tools/run_state.py, idea_discovery_gate.py, provenance.py, reviewer_route.py
- tools/iteration_log.py, watchdog.py, threat_scan.py, research_wiki.py
- tools/antigravity-exec/server.py and aris-antigravity-review.md
- original shared-references/{reviewer-backends,resumable-runs,external-cadence,
  experiment-integrity,review-scope-limits,venue-checklists}.md

Local changes include fixed Codex/Gemini roles, real trace freshness,
sec-phase defaults and nested section parsing, phase kinds/namespaces and
subprocess stream cleanup. The newer standalone runtime/audit helpers and
regression tests are sec-paper additions. No auto-update from ARIS is assumed;
review upstream changes and rerun local tests before importing them.

ARIS license, retained in full:

MIT License

Copyright (c) 2026 wanshuiyin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
