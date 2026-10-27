#!/usr/bin/env python3
"""Initialize a standalone project and report real host capabilities."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from reviewer_route import resolve_route


def initialize(project):
    project = Path(project).resolve()
    repo = Path(__file__).resolve().parent.parent
    directory = project / '.aris'
    directory.mkdir(parents=True, exist_ok=True)
    config = directory / 'reviewer.json'
    if not config.exists():
        config.write_text((repo / '.aris/reviewer.example.json').read_text())
    route = resolve_route(project, 'codex')  # reject incompatible pre-existing config
    (directory / 'sec-paper.json').write_text(json.dumps({'schema_version':1, 'repo_root':str(repo), 'executor':'codex', 'reviewer':route}, indent=2))
    return route


def doctor(project, live=False):
    project = Path(project).resolve()
    capabilities = {name: shutil.which(name) for name in ('agy', 'docker', 'latexmk', 'pdfinfo', 'pdftotext', 'pdffonts', 'git')}
    route = resolve_route(project, 'codex')
    result = dict(python=sys.version.split()[0], repo_root=str(Path(__file__).resolve().parent.parent), reviewer=route, capabilities=capabilities,
                  cpu_count=__import__('os').cpu_count(), literature_sources={'web':'requires host web access or configured API; never infer availability', 'local_pdfs':str(project/'papers')}, live_probe='NOT_RUN')
    if live:
        code = subprocess.run([sys.executable, str(Path(__file__).parent / 'review.py'), 'probe', '--project', str(project)], capture_output=True, text=True)
        result['live_probe'] = {'exit_code':code.returncode, 'output':code.stdout, 'error':code.stderr}
        if code.returncode:
            raise ValueError(f'Gemini probe failed: {result}')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['init', 'doctor'])
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    try:
        result = initialize(args.project) if args.action == 'init' else doctor(args.project, args.live)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0
    except (OSError, ValueError) as exc:
        print(f'BLOCKED: {exc}')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
