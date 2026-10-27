#!/usr/bin/env python3
"""Check the final PDF, logs, anonymity metadata and a cycle-specific policy."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import date
from pathlib import Path

from evidence import local, snapshot


def check(root, paper_dir, pdf, policy_path):
    root = Path(root).resolve()
    policy_file = local(root, policy_path)
    policy = json.loads(policy_file.read_text())
    failures = []
    if not policy.get('official_url', '').startswith('https://') or not policy.get('cycle') or not policy.get('retrieved_at') or not isinstance(policy.get('max_total_pages'), int) or policy['max_total_pages'] <= 0:
        raise ValueError('venue policy requires official_url, cycle, retrieved_at, max_total_pages')
    retrieved = date.fromisoformat(policy['retrieved_at'])
    if (date.today() - retrieved).days not in range(0, 91):
        failures.append('venue policy must be verified against current official CFP within 90 days')
    official = local(root, policy['saved_cfp'])
    if not official.is_file() or not official.stat().st_size:
        failures.append('saved official CFP evidence missing')
    for tool in ('pdfinfo', 'pdftotext', 'pdffonts'):
        if not shutil.which(tool):
            failures.append(f'missing required PDF tool: {tool}')
    paper = local(root, paper_dir)
    pdf_file = local(root, pdf)
    if not pdf_file.is_file() or not pdf_file.read_bytes().startswith(b'%PDF-'):
        failures.append('compiled PDF missing or invalid header')
    if failures:
        return dict(status='BLOCKED', failures=failures)
    def command(argv):
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=60)
        if proc.returncode:
            raise ValueError(f'{argv[0]} failed: {proc.stderr}')
        return proc.stdout
    info = command(['pdfinfo', str(pdf_file)])
    text = command(['pdftotext', '-layout', str(pdf_file), '-'])
    fonts = command(['pdffonts', str(pdf_file)])
    pages_match = re.search(r'^Pages:\s+(\d+)', info, re.M)
    if not pages_match or int(pages_match[1]) > policy['max_total_pages']:
        failures.append('PDF page count missing or exceeds cycle-specific total-page limit')
    if re.search(r'^Author:[ \t]*\S', info, re.M):
        failures.append('nonempty PDF Author metadata')
    for token in policy.get('forbidden_identifiers', []):
        if token.casefold() in (text + info).casefold():
            failures.append(f'author-identifying token: {token}')
    if re.search(r'\b(TBD|TODO|CITATION NEEDED)\b|\?\?', text):
        failures.append('unresolved citation/reference or draft placeholder in PDF')
    # pdffonts has font names/types of variable width; locate emb/sub/uni
    # columns from the header instead of splitting font names on whitespace.
    font_lines = fonts.splitlines()
    if font_lines and 'emb' in font_lines[0]:
        column = font_lines[0].index('emb')
        if any(line[column:column+3].strip() != 'yes' for line in font_lines[2:] if line.strip()):
            failures.append('unembedded PDF font')
    else:
        failures.append('cannot parse PDF font report')
    logs = list(paper.glob('*.log'))
    if not logs:
        failures.append('compile log missing')
    log = '\n'.join(p.read_text(errors='replace') for p in logs)
    if re.search(r'Overfull \\[hv]box|undefined references|Citation .+ undefined|LaTeX Error', log, re.I):
        failures.append('compile log contains overflow, undefined references or LaTeX errors')
    source = '\n'.join(p.read_text(errors='replace') for p in paper.rglob('*.tex'))
    source_files = [p for p in paper.rglob('*') if p.is_file() and p != pdf_file and p.suffix in {'.tex','.bib','.png','.jpg','.svg','.eps','.pdf'} and '.aris' not in p.parts]
    if any(p.stat().st_mtime > pdf_file.stat().st_mtime for p in source_files):
        failures.append('PDF older than a source/bibliography/figure; recompile')
    if re.search(r'\b(TBD|TODO|CITATION NEEDED)\b', source):
        failures.append('source contains draft placeholders')
    for heading in policy.get('required_sections', []):
        if heading.casefold() not in text.casefold():
            failures.append(f'required section absent from PDF: {heading}')
    inputs = [paper_dir, policy_path, policy['saved_cfp']]
    return dict(schema_version=1, status='PASS' if not failures else 'BLOCKED', failures=failures, inputs=inputs, snapshot=snapshot(root, inputs), pages=int(pages_match[1]) if pages_match else None, pdf=pdf, fonts=fonts, info=info)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--paper', default='paper')
    parser.add_argument('--pdf', default='paper/main.pdf')
    parser.add_argument('--policy', default='paper/venue-policy.json')
    args = parser.parse_args()
    try:
        result = check(args.project, args.paper, args.pdf, args.policy)
        output = local(args.project, f'{args.paper}/.aris/pdf-check.json')
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result,ensure_ascii=False,indent=2))
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0 if result['status'] == 'PASS' else 1
    except (ValueError, OSError, KeyError, subprocess.TimeoutExpired) as exc:
        print(f'BLOCKED: {exc}')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
