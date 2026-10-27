#!/usr/bin/env python3
"""Minimal independent local POSIX job/queue backend; commands are argv arrays."""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

from evidence import local

TERMINAL = {'SUCCEEDED', 'FAILED', 'TIMED_OUT', 'CANCELLED', 'INTERRUPTED'}


def write(path, data):
    temporary = path.with_name(path.name + f'.{os.getpid()}.tmp')
    temporary.write_text(json.dumps(data, indent=2))
    temporary.replace(path)


def job_dir(root, job_id):
    if not job_id or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in job_id):
        raise ValueError('job ID must use letters, digits, hyphen or underscore')
    return Path(root) / '.aris/jobs' / job_id


def validate_spec(spec):
    if spec.get('backend', 'local') != 'local':
        raise ValueError('only local backend supported; SSH/GPU needs an explicit adapter')
    if not isinstance(spec.get('command'), list) or not spec['command'] or not all(isinstance(s, str) for s in spec['command']):
        raise ValueError('command must be a nonempty argv string array (no implicit shell)')
    if not isinstance(spec.get('timeout_seconds'), (int, float)) or spec['timeout_seconds'] <= 0:
        raise ValueError('positive timeout_seconds required')
    for name in ('target', 'target_revision', 'isolation_key', 'seed'):
        if name not in spec or spec[name] is None or str(spec[name]) == '':
            raise ValueError(f'{name} required')


def status(root, job_id):
    directory = job_dir(root, job_id)
    data = json.loads((directory / 'state.json').read_text())
    if data['status'] in TERMINAL:
        return data
    # Worker holds this lock for its entire lifecycle; no PID-only trust on resume.
    with (directory / 'worker.lock').open('a') as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return data
        if time.time() - data['created_at'] < 3:
            return data  # detached worker startup window
        data.update(status='INTERRUPTED', reason='worker absent; inspect target and logs before reusing isolation key')
        write(directory / 'state.json', data)
        return data


def start(root, spec):
    root = Path(root).resolve()
    validate_spec(spec)
    directory = job_dir(root, spec['id'])
    directory.parent.mkdir(parents=True, exist_ok=True)
    with (directory.parent / 'scheduler.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if directory.exists():
            if json.loads((directory / 'spec.json').read_text()) != spec:
                raise ValueError('existing job ID has a different spec; use a new ID')
            return status(root, spec['id'])
        for state_file in directory.parent.glob('*/state.json'):
            prior = json.loads(state_file.read_text())
            # Interrupted worker may leave a child/target alive. Never auto-reuse.
            if prior['isolation_key'] == spec['isolation_key'] and prior['status'] not in (TERMINAL - {'INTERRUPTED'}):
                raise ValueError('isolation key occupied or interrupted; inspect and allocate a new target')
        results = local(root, f'results/{spec["id"]}')
        if results.exists():
            raise ValueError('results directory already exists; never overwrite evidence')
        directory.mkdir()
        results.mkdir(parents=True)
        write(directory / 'spec.json', spec)
        write(results / 'config.json', spec)
        data = dict(id=spec['id'], status='STARTING', created_at=time.time(), isolation_key=spec['isolation_key'])
        write(directory / 'state.json', data)
        with (directory / 'worker.log').open('wb') as log:
            worker_proc = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), '_worker', '--project', str(root), '--id', spec['id']], stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True)
            threading.Thread(target=worker_proc.wait, daemon=True).start()
        return data


def worker(root, job_id):
    root = Path(root).resolve()
    directory = job_dir(root, job_id)
    results = root / 'results' / job_id
    with (directory / 'worker.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        spec = json.loads((directory / 'spec.json').read_text())
        data = json.loads((directory / 'state.json').read_text())
        env = dict(os.environ, SEC_PAPER_RESULTS=str(results), SEC_PAPER_SEED=str(spec['seed']))
        proc = None
        stopped = [False]
        def request_stop(*_):
            stopped[0] = True
        signal.signal(signal.SIGTERM, request_stop)
        signal.signal(signal.SIGINT, request_stop)
        try:
            with (results / 'stdout.log').open('wb') as out, (results / 'stderr.log').open('wb') as err:
                proc = subprocess.Popen(spec['command'], cwd=root, env=env, stdin=subprocess.DEVNULL, stdout=out, stderr=err, start_new_session=True)
                began = time.monotonic()
                data.update(status='RUNNING', pid=proc.pid, worker_pid=os.getpid(), started_at=time.time())
                write(directory / 'state.json', data)
                outcome = None
                while proc.poll() is None:
                    if stopped[0] or (directory / 'cancel').exists():
                        outcome = 'CANCELLED'
                    elif time.monotonic() - began > spec['timeout_seconds']:
                        outcome = 'TIMED_OUT'
                    if outcome:
                        break
                    time.sleep(.1)
                # Always clean the group's remaining descendants, even when the
                # parent command exited successfully (daemon leakage is not OK).
                try:
                    os.killpg(proc.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                try:
                    proc.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    pass
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                proc.wait()
                data.update(status=outcome or ('SUCCEEDED' if proc.returncode == 0 else 'FAILED'), returncode=proc.returncode, finished_at=time.time())
        except Exception as exc:
            if proc is not None:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                proc.wait()
            data.update(status='FAILED', reason=str(exc), finished_at=time.time())
        write(directory / 'state.json', data)
        write(results / 'job.json', data)


def run_queue(root, specs, parallel):
    if parallel < 1 or not specs or len({s['id'] for s in specs}) != len(specs):
        raise ValueError('nonempty unique jobs and positive parallel required')
    for spec in specs:
        validate_spec(spec)
        if set(spec.get('after', [])) - {s['id'] for s in specs}:
            raise ValueError('unknown wave dependency')
    # Cycle detection, before starting anything.
    resolved = set()
    while len(resolved) < len(specs):
        ready = {s['id'] for s in specs if set(s.get('after', [])) <= resolved}
        if ready <= resolved:
            raise ValueError('cyclic wave dependencies')
        resolved |= ready
    while True:
        states = {s['id']: status(root, s['id']) for s in specs if job_dir(root, s['id']).exists()}
        if any(v['status'] in TERMINAL - {'SUCCEEDED'} for v in states.values()):
            raise ValueError('queue blocked by failed/timeout/cancelled/interrupted job; no auto-retry')
        if len(states) == len(specs) and all(v['status'] == 'SUCCEEDED' for v in states.values()):
            return states
        active = sum(v['status'] not in TERMINAL for v in states.values())
        occupied = {v['isolation_key'] for v in states.values() if v['status'] not in TERMINAL}
        for spec in specs:
            if active >= parallel:
                break
            if spec['id'] not in states and spec['isolation_key'] not in occupied and all(states.get(dep, {}).get('status') == 'SUCCEEDED' for dep in spec.get('after', [])):
                start(root, spec)
                occupied.add(spec['isolation_key'])
                active += 1
        time.sleep(.1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['start', 'status', 'wait', 'cancel', 'queue', '_worker'])
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--id')
    parser.add_argument('--spec', type=Path)
    parser.add_argument('--parallel', type=int, default=2)
    args = parser.parse_args()
    try:
        if args.action == '_worker':
            worker(args.project, args.id)
            return 0
        if args.action in {'start', 'queue'}:
            specs = json.loads(args.spec.read_text())
            data = start(args.project, specs) if args.action == 'start' else run_queue(args.project, specs, args.parallel)
        else:
            directory = job_dir(args.project, args.id)
            if args.action == 'cancel':
                (directory / 'cancel').touch()
            data = status(args.project, args.id)
            if args.action == 'wait':
                while data['status'] not in TERMINAL:
                    time.sleep(.1)
                    data = status(args.project, args.id)
        print(json.dumps(data, ensure_ascii=False))
        return 0 if data.get('status', 'SUCCEEDED') in {'SUCCEEDED', 'STARTING', 'RUNNING'} else 1
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f'BLOCKED: {exc}')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
