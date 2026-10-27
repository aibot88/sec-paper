#!/usr/bin/env python3
"""Standalone CLI for the bundled AntiGravity bridge. No Codex fallback."""
from __future__ import annotations

import argparse
import importlib.util
import json
import queue
import uuid
from pathlib import Path

from evidence import decision, digest, local, snapshot
from reviewer_route import resolve_route


def bridge_call(project, route, prompt, continuation=None):
    spec = importlib.util.spec_from_file_location('sec_agy_bridge', Path(__file__).parent / 'antigravity-exec/server.py')
    bridge = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bridge)
    events = []
    bridge.send_message = events.append
    if continuation:
        name = 'antigravity-reply'
        args = {'threadId': continuation, 'prompt': prompt}
    else:
        name = 'antigravity'
        args = dict(prompt=prompt, cwd=str(project), model=route['model'], effort=route['effort'])
    response = bridge.handle_call({'id': 1, 'params': {'name': name, 'arguments': args}}, queue.Queue(), [])
    return response, events


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['probe', 'run'])
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--input', action='append', default=[])
    parser.add_argument('--prompt-file', type=Path)
    parser.add_argument('--phase', default='probe')
    parser.add_argument('--run-id', default='probe')
    parser.add_argument('--executor', default='codex-gpt-6.1-sol')
    parser.add_argument('--round', type=int, default=1)
    parser.add_argument('--pending-job', action='append', default=[])
    parser.add_argument('--continue-from', help='Prior receipt for warm repair checks only; final audits stay fresh')
    args = parser.parse_args()
    project = args.project.resolve()
    try:
        route = resolve_route(project, 'codex')
        if not args.executor.startswith(('codex', 'gpt-', 'openai/')):
            raise ValueError('executor must be Codex/OpenAI')
        if args.action == 'probe':
            prompt = 'Reply with exactly SEC_PAPER_GEMINI_PROBE_OK. Do not use any tools.'
            inputs = {}
        else:
            if not args.prompt_file:
                raise ValueError('--prompt-file is required')
            inputs = snapshot(project, args.input)
            prompt = args.prompt_file.read_text() + '\n\nRead these project-relative inputs directly:\n' + '\n'.join(args.input)
            prompt += '\nReturn ONLY JSON: {"decision":"PASS|REVISE|BLOCK|PROCEED|PROCEED WITH CAUTION|ABANDON|STOP|CONTINUE|NOT_APPLICABLE", "in_scope":true, "findings":[{"severity":"MAJOR", "path":"...", "reason":"..."}], "reason":"..."}. Never report PASS for unresolved blockers. Do not edit files.'
            if args.phase == 'sec-auto-review-loop':
                prompt += '\nAlso include score (number) and hard_gates with keys threat_model, oracle, adaptive_attacker, ethics, artifacts each PASS or FAIL. For non-defense tracks justify adaptive-attacker non-applicability in reason and use PASS only when that justification is sound. STOP requires score >= 6 and all gates PASS; otherwise CONTINUE/BLOCK.'
        continuation = None
        if args.continue_from:
            old = json.loads(local(project, args.continue_from).read_text())
            if old['run_id'] != args.run_id or old['reviewer_model'] != route['model']:
                raise ValueError('warm review must preserve run and model')
            continuation = old['thread_id']
        response, events = bridge_call(project, route, prompt, continuation)
        trace_dir = project / '.aris/traces' / uuid.uuid4().hex
        trace_dir.mkdir(parents=True)
        raw_path = trace_dir / 'raw.json'
        raw_path.write_text(json.dumps(dict(phase=args.phase, run_id=args.run_id, prompt=prompt, snapshot=inputs, bridge_result=response, events=events), ensure_ascii=False, indent=2))
        result = response.get('result', {})
        meta = result.get('structuredContent', {})
        if result.get('isError') or meta.get('status') != 'SUCCESS' or meta.get('model') != route['model'] or not str(meta.get('model', '')).startswith('gemini-') or not meta.get('threadId'):
            raise ValueError(f'REVIEW_UNAVAILABLE: {result}; raw trace: {raw_path}')
        if args.action == 'probe':
            if meta.get('content', '').strip() != 'SEC_PAPER_GEMINI_PROBE_OK':
                raise ValueError('probe response mismatch')
            print(json.dumps({'status':'PROBE_OK','model':meta['model'],'thread_id':meta['threadId'],'trace':str(raw_path)}))
            return 0
        verdict = decision(meta['content'])
        if inputs != snapshot(project, args.input):
            raise ValueError('evidence changed during review; repeat on stable inputs')
        receipt = dict(schema_version=1, backend='antigravity', executor_model=args.executor, reviewer_model=meta['model'], thread_id=meta['threadId'], phase=args.phase, run_id=args.run_id, inputs=args.input, snapshot=inputs, verdict=verdict, raw_trace=str(raw_path.relative_to(project)), raw_trace_sha256=digest(raw_path), topology='warm' if continuation else 'fresh')
        receipt_path = trace_dir / 'receipt.json'
        receipt_path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2))
        if args.phase == 'sec-auto-review-loop':
            state_dir = project / 'review-stage'
            state_dir.mkdir(exist_ok=True)
            row = dict(run_id=args.run_id, round=args.round, phase=args.phase,
                       receipt=str(receipt_path.relative_to(project)), raw_trace=receipt['raw_trace'],
                       decision=verdict['decision'], accepted=False)
            with (state_dir / 'ACQUITTAL_LOG.jsonl').open('a') as handle:
                handle.write(json.dumps(row) + '\n')
            state = dict(schema_version=1, run_id=args.run_id, round=args.round,
                         status='review_returned', current_phase='review',
                         executor_model=args.executor, reviewer_route=route,
                         requested_model=route['model'], reported_model=meta['model'],
                         thread_id=meta['threadId'], pending_jobs=args.pending_job,
                         evidence_inputs=args.input, receipt=row['receipt'],
                         weaknesses=verdict['findings'], next_action='validate_or_fix')
            (state_dir / 'REVIEW_STATE.json').write_text(json.dumps(state,indent=2))
        print(json.dumps({'receipt':str(receipt_path.relative_to(project)), 'decision':verdict['decision'], 'model':meta['model']}, ensure_ascii=False))
        return 0 if verdict['in_scope'] and verdict['decision'] in {'PASS','PROCEED','PROCEED WITH CAUTION','STOP','NOT_APPLICABLE'} else 1
    except (ValueError, OSError, KeyError) as exc:
        print(f'BLOCKED: {exc}')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
