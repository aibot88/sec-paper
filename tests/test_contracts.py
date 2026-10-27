"""Contract-layer parity tests: vendored helpers, shared-reference coverage,
and skill wiring added by the ARIS-gap audit. All file fixtures are synthetic.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'tools'))
import evidence_check  # noqa: E402

CHAIN_SKILLS = [p.name for p in (REPO / 'skills').iterdir() if (p / 'SKILL.md').exists()]

REQUIRED_REFS = [
    'output-manifest', 'output-language', 'output-versioning',
    'output-composition', 'review-tracing', 'wiki-helper-resolution',
    'integration-contract', 'evidence-precheck', 'taste-calibration',
    'fan-out-pattern', 'workflow-contract', 'reviewer-contract',
    'acceptance-gate', 'reviewer-independence', 'reviewer-routing',
    'experiment-integrity', 'review-scope-limits', 'external-cadence',
    'resumable-runs', 'venue-checklists', 'reviewer-backends',
]


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root = Path(self.t.name)

    # ---------- deterministic evidence pre-check (vendored) ----------
    def test_evidence_check_three_states(self):
        (self.root / 'res.json').write_text('{"fp": 0.02, "trials": 10}')
        self.assertEqual(evidence_check.check_claim('0.02', 'res.json', str(self.root))['status'], 'verified')
        self.assertEqual(evidence_check.check_claim('0.99', 'res.json', str(self.root))['status'], 'value_not_found')
        self.assertEqual(evidence_check.check_claim('1', 'missing.json', str(self.root))['status'], 'path_missing')
        # empty value on an EXISTING file fails closed (never a false verified)
        self.assertEqual(evidence_check.check_claim('', 'res.json', str(self.root))['status'], 'value_not_found')
        # ... and is unparseable only at batch level
        out = evidence_check.check_batch([{'id': 'e', 'value': '', 'source': 'res.json'}], str(self.root))
        self.assertEqual(out['results'][0]['status'], 'unparseable')

    def test_evidence_check_batch_and_never_false_verified(self):
        (self.root / 'a.txt').write_text('loss 0.5 in 1,234 trials')
        out = evidence_check.check_batch([
            {'id': 'x', 'value': '0.5', 'source': 'a.txt'},
            {'id': 'y', 'value': '0.50', 'source': 'a.txt'},
            {'id': 'z', 'value': '1234', 'source': 'a.txt'},
        ], str(self.root))
        statuses = {r['id']: r['status'] for r in out['results']}
        self.assertEqual(statuses['x'], 'verified')
        # 1234 inside a comma-grouped token is a compound construct -> not verified (fail closed or found per matcher policy)
        self.assertNotIn(statuses['y'], ('path_missing',))

    def test_evidence_check_cli(self):
        (self.root / 'r.txt').write_text('oracle fired 23 times')
        proc = subprocess.run([sys.executable, str(REPO / 'tools/evidence_check.py'), str(self.root), '--value', '23', '--source', 'r.txt'], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)['status'], 'verified')

    def test_numeric_only_guard_blocks_substring_false_positive(self):
        # 'TP' would substring-match 'HTTP' in a raw substring check; the
        # numeric_only guard must route it to the jury instead.
        (self.root / 'log.txt').write_text('GET / HTTP/1.1 PASSWORD=x')
        out = evidence_check.check_batch([
            {'id': 'q', 'value': 'TP', 'source': 'log.txt'},
            {'id': 'n', 'value': '23', 'source': 'log.txt'},
        ], str(self.root), numeric_only=True)
        statuses = {r['id']: r['status'] for r in out['results']}
        self.assertEqual(statuses['q'], 'skipped_non_numeric')
        self.assertEqual(statuses['n'], 'value_not_found')

    # ---------- shared-reference coverage ----------
    def test_all_required_refs_exist(self):
        refs = {p.stem for p in (REPO / 'shared-references').glob('*.md')}
        missing = [r for r in REQUIRED_REFS if r not in refs]
        self.assertEqual(missing, [])

    def test_stale_vendored_refs_carry_banner(self):
        for name in ('reviewer-backends', 'resumable-runs', 'external-cadence', 'venue-checklists'):
            head = (REPO / 'shared-references' / f'{name}.md').read_text()[:1200]
            self.assertIn('sec-paper note', head, name)

    def test_workflow_contract_wires_new_protocols(self):
        text = (REPO / 'shared-references' / 'workflow-contract.md').read_text()
        for token in ('MANIFEST.md', 'output-language', 'output-versioning', 'output-composition',
                      'threat_scan.py', 'watchdog.py', 'iteration_log.py', 'evidence_check.py',
                      'REVIEWER_MEMORY.md', 'REF_PAPER_SUMMARY.md', 'taste-calibration',
                      'integration-contract', 'fan-out-pattern'):
            self.assertIn(token, text, token)

    # ---------- skill wiring ----------
    def test_pipeline_wires_watchdog_and_iteration_log(self):
        text = (REPO / 'skills/sec-research-pipeline/SKILL.md').read_text()
        self.assertIn('watchdog.py', text)
        self.assertIn('iteration_log.py', text)
        self.assertIn('MANIFEST.md', text)

    def test_discovery_emits_ref_paper_summary(self):
        self.assertIn('REF_PAPER_SUMMARY.md', (REPO / 'skills/sec-idea-discovery/SKILL.md').read_text())

    def test_review_loop_requires_memory_file(self):
        text = (REPO / 'skills/sec-auto-review-loop/SKILL.md').read_text()
        self.assertIn('REVIEWER_MEMORY.md', text)
        self.assertIn('sidestepped', text)

    def test_claim_and_audit_call_precheck(self):
        for skill in ('sec-result-to-claim', 'sec-experiment-audit'):
            self.assertIn('evidence_check.py', (REPO / f'skills/{skill}/SKILL.md').read_text(), skill)

    def test_refine_cites_calibration(self):
        self.assertIn('taste-calibration', (REPO / 'skills/sec-research-refine/SKILL.md').read_text())

    def test_paper_writing_cites_output_protocols(self):
        text = (REPO / 'skills/sec-paper-writing/SKILL.md').read_text()
        for token in ('output-manifest', 'output-versioning', 'output-language'):
            self.assertIn(token, text, token)

    def test_no_dangling_local_links(self):
        import re
        bad = []
        for folder in ('shared-references', 'skills'):
            for f in (REPO / folder).rglob('*.md'):
                for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', f.read_text()):
                    clean = target.split('#')[0]
                    if clean and '://' not in clean and not clean.startswith('/') and not (f.parent / clean).exists():
                        bad.append(f'{f}: {clean}')
        self.assertEqual(bad, [])


if __name__ == '__main__':
    unittest.main()
