#!/usr/bin/env python3
"""Fail-closed final audit/freshness gate for a standalone submission bundle."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from evidence import local, snapshot, validate_receipt


def evaluate(root, manifest_path):
    root = Path(root).resolve()
    manifest = json.loads(local(root, manifest_path).read_text())
    if manifest.get('schema_version') != 1 or not manifest.get('run_id'):
        raise ValueError('submission manifest schema_version/run_id required')
    for field in ('paper_dir', 'fact_pack', 'research_contract', 'venue_policy', 'artifact_readme', 'artifact_dir'):
        if not manifest.get(field):
            raise ValueError(f'missing manifest field: {field}')
    if not isinstance(manifest.get('raw_results'), list) or not manifest['raw_results']:
        raise ValueError('raw results (or explicit formal evidence files) required')
    paper = local(root, manifest['paper_dir'])
    for filename in ('main.tex', 'main.pdf'):
        if not (paper / filename).is_file() or not (paper / filename).stat().st_size:
            raise ValueError(f'missing final paper artifact: {filename}')
    if not list(paper.glob('*.bib')):
        raise ValueError('bibliography source missing')
    for value in (manifest['fact_pack'], manifest['research_contract'], manifest['artifact_readme']):
        if not local(root, value).is_file() or not local(root, value).stat().st_size:
            raise ValueError(f'empty/missing submission evidence: {value}')
    inputs = [manifest[k] for k in ('paper_dir', 'fact_pack', 'research_contract', 'venue_policy', 'artifact_readme', 'artifact_dir')] + manifest['raw_results']
    expected = snapshot(root, inputs)
    checks = {}
    for kind in ('claims', 'citations', 'adversarial', 'proof', 'artifact'):
        data = validate_receipt(root, manifest['audits'][kind], f'paper-{kind}', manifest['run_id'], allow_na=(kind == 'proof'))
        if data.get('topology') != 'fresh':
            raise ValueError(f'{kind} final audit must be fresh-context')
        if any(data['snapshot'].get(k) != v for k, v in expected.items()):
            raise ValueError(f'{kind} audit omitted final sources/raw evidence/artifact')
        if data['verdict']['decision'] not in {'PASS', 'NOT_APPLICABLE'}:
            raise ValueError(f'{kind} final audit must PASS')
        if kind == 'proof' and manifest.get('theory_claims') is True and data['verdict']['decision'] == 'NOT_APPLICABLE':
            raise ValueError('theory claims require a proof audit PASS')
        checks[kind] = data['verdict']['decision']
    pdf_check = json.loads((paper / '.aris/pdf-check.json').read_text())
    if pdf_check.get('status') != 'PASS' or pdf_check.get('snapshot') != snapshot(root, pdf_check['inputs']):
        raise ValueError('final PDF check missing, failed or STALE')
    if pdf_check.get('pdf') != str((paper/'main.pdf').relative_to(root)):
        raise ValueError('PDF check refers to a different PDF')
    if manifest['venue_policy'] not in pdf_check['inputs']:
        raise ValueError('PDF check did not use manifest venue policy')
    return dict(status='PASS', submission_ready=True, audits=checks, snapshot=expected,
                limitation='Process evidence, not a guarantee of paper correctness or venue acceptance. Does not submit to a venue.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--manifest', default='.aris/submission.json')
    args = parser.parse_args()
    try:
        result = evaluate(args.project, args.manifest)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        result = dict(status='BLOCKED', submission_ready=False, reason=str(exc))
    output = args.project / '.aris/submission-gate.json'
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['submission_ready'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
