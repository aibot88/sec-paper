#!/usr/bin/env python3
"""Local evidence freshness, not an attestation of scientific correctness."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from provenance import model_family

IGNORE = {'.git', '__pycache__', '.aris', '.venv', 'node_modules'}
POSITIVE = {'PASS', 'PROCEED', 'PROCEED WITH CAUTION', 'STOP'}


def local(root, value):
    root = Path(root).resolve()
    path = (root / value).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f'path escapes project: {value}')
    return path


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def snapshot(root, inputs):
    root = Path(root).resolve()
    if not inputs:
        raise ValueError('at least one explicit evidence input is required')
    hashes = {}
    for value in inputs:
        path_text, _, anchor = str(value).partition('#')
        path = local(root, path_text)
        if not path.exists():
            raise ValueError(f'missing evidence: {value}')
        if anchor:
            lines = []
            level = None
            fence = False
            for line in path.read_text().splitlines():
                if not fence and line.strip().startswith('<!--') and line.strip().endswith('-->'):
                    continue
                if line.lstrip().startswith('```'):
                    fence = not fence
                match = None if fence else re.match(r'^(#{1,6})\s+(.+?)\s*#*$', line)
                if match:
                    slug = re.sub(r'[^\w\s-]', '', match[2].strip().lower())
                    slug = re.sub(r'[\s-]+', '-', slug).strip('-')
                    if level is None and slug == anchor:
                        level = len(match[1])
                    elif level is not None and len(match[1]) <= level:
                        break
                if level is not None:
                    lines.append(line)
            if not lines:
                raise ValueError(f'missing evidence section: {value}')
            key = str(path.relative_to(root)) + '#' + anchor
            hashes[key] = hashlib.sha256(('\n'.join(lines).rstrip()+'\n').encode()).hexdigest()
            continue
        files = [path] if path.is_file() else [
            p for p in path.rglob('*')
            if p.is_file() and not (set(p.relative_to(path).parts) & IGNORE)
        ]
        if not files:
            raise ValueError(f'empty evidence directory: {value}')
        for file in files:
            file = local(root, file)
            hashes[str(file.relative_to(root))] = digest(file)
    return dict(sorted(hashes.items()))


def decision(text):
    text = text.strip()
    if text.startswith('```'):
        text = '\n'.join(text.splitlines()[1:-1])
    value = json.loads(text)
    if not isinstance(value, dict) or value.get('decision') not in (
        POSITIVE | {'REVISE', 'BLOCK', 'ABANDON', 'NOT_APPLICABLE', 'CONTINUE'}
    ):
        raise ValueError('review must return a recognized JSON decision')
    if not isinstance(value.get('in_scope'), bool) or not isinstance(value.get('findings'), list):
        raise ValueError('review requires in_scope boolean and findings list')
    return value


def validate_receipt(root, receipt, phase=None, run_id=None, allow_na=False):
    """Bind a positive Gemini verdict to bridge output and current input files.

    This detects stale/absent evidence, not a malicious owner fabricating all
    local files. Preserve raw traces for human/process audit.
    """
    root = Path(root).resolve()
    path = local(root, receipt)
    data = json.loads(path.read_text())
    if data.get('schema_version') != 1:
        raise ValueError('unsupported review receipt schema')
    if phase is not None and data.get('phase') != phase:
        raise ValueError('review phase mismatch')
    if run_id is not None and data.get('run_id') != run_id:
        raise ValueError('review run_id mismatch')
    if data.get('backend') != 'antigravity' or model_family(data.get('executor_model', '')) != 'openai':
        raise ValueError('Codex executor / AntiGravity reviewer required')
    raw_path = local(root, data['raw_trace'])
    if digest(raw_path) != data['raw_trace_sha256']:
        raise ValueError('raw review trace changed')
    raw = json.loads(raw_path.read_text())
    result = raw['bridge_result']['result']
    meta = result['structuredContent']
    if result.get('isError') or meta.get('status') != 'SUCCESS':
        raise ValueError('review did not complete successfully')
    actual = meta.get('model')
    if not isinstance(actual, str) or not actual.startswith('gemini-') or actual != data.get('reviewer_model'):
        raise ValueError('actual Gemini model identity required')
    if not meta.get('threadId') or meta['threadId'] != data.get('thread_id'):
        raise ValueError('review thread identity mismatch')
    verdict = decision(meta['content'])
    if verdict != data.get('verdict') or verdict['in_scope'] is not True:
        raise ValueError('out-of-scope or inconsistent review verdict')
    accepted = POSITIVE | ({'NOT_APPLICABLE'} if allow_na else set())
    if verdict['decision'] not in accepted:
        raise ValueError(f'non-positive review: {verdict["decision"]}')
    if any(isinstance(item, dict) and str(item.get('severity', '')).upper() in {'FATAL', 'BLOCKER', 'MAJOR'} for item in verdict['findings']):
        raise ValueError('positive verdict contains unresolved blocking findings')
    if data.get('phase') == 'sec-auto-review-loop':
        gates = verdict.get('hard_gates', {})
        if verdict['decision'] != 'STOP' or not isinstance(verdict.get('score'), (int, float)) or verdict['score'] < 6:
            raise ValueError('review-loop acceptance requires STOP and score >= 6')
        if any(gates.get(name) != 'PASS' for name in ('threat_model', 'oracle', 'adaptive_attacker', 'ethics', 'artifacts')):
            raise ValueError('review-loop hard gates must all PASS (justify non-applicability within findings/reason)')
    if verdict['decision'] == 'NOT_APPLICABLE' and not verdict.get('reason'):
        raise ValueError('NOT_APPLICABLE requires a reviewer justification')
    if data.get('snapshot') != snapshot(root, data['inputs']):
        raise ValueError('STALE: reviewed evidence changed')
    if raw.get('snapshot') != data['snapshot'] or raw.get('phase') != data['phase'] or raw.get('run_id') != data['run_id']:
        raise ValueError('receipt differs from bridge invocation evidence')
    return data
