"""All receipts in this module are SYNTHETIC TEST FIXTURES, not real reviews."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO/'tools'))
import evidence
import idea_discovery_gate as gate
import run_state as state
import reviewer_route
import submission_gate


def fixture_receipt(root, phase, run_id, inputs, decision='PASS', topology='fresh', extra=None):
    """Deliberately synthesize bridge data to exercise verifiers offline."""
    directory = root/'.aris/traces'/f'TEST_FIXTURE_{phase}'
    directory.mkdir(parents=True, exist_ok=True)
    verdict = dict(decision=decision, in_scope=True, findings=[])
    verdict.update(extra or {})
    hashes = evidence.snapshot(root, inputs)
    meta = dict(status='SUCCESS', model='gemini-3.8-flash-high', threadId='TEST_FIXTURE_NOT_A_REAL_THREAD', content=json.dumps(verdict))
    raw = dict(phase=phase, run_id=run_id, snapshot=hashes, bridge_result={'result':{'structuredContent':meta}}, events=[])
    raw_path = directory/'raw.json'
    raw_path.write_text(json.dumps(raw))
    receipt = dict(schema_version=1, backend='antigravity', executor_model='codex-gpt-6.1-sol', reviewer_model=meta['model'], thread_id=meta['threadId'], phase=phase, run_id=run_id, inputs=inputs, snapshot=hashes, verdict=verdict, raw_trace=str(raw_path.relative_to(root)), raw_trace_sha256=evidence.digest(raw_path), topology=topology)
    path = directory/'receipt.json'
    path.write_text(json.dumps(receipt))
    return str(path.relative_to(root))


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def put(self, path, content='fixture evidence\n'):
        file = self.root/path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content)
        return file

    def complete_discovery(self):
        self.put('idea-stage/IDEA_REPORT.md', '# Fixture\n## Literature Landscape\nliterature\n## Ranked Ideas\n### Candidate 1\nreal test content\n## Novelty Verification\nnovelty\n## External Critical Review\nreview\n')
        for name in ('FINAL_PROPOSAL.md','EXPERIMENT_PLAN.md','EXPERIMENT_TRACKER.md','REVIEW_SUMMARY.md'):
            self.put('refine-logs/'+name)
        state.start_run(str(self.root),'ideas',list(gate.REQUIRED_PHASES))
        anchors = ['literature-landscape','ranked-ideas','novelty-verification','external-critical-review']
        for i, phase in enumerate(gate.REQUIRED_PHASES):
            artifact = 'idea-stage/IDEA_REPORT.md#'+anchors[i] if i < 4 else 'refine-logs/FINAL_PROPOSAL.md'
            state.set_status(str(self.root),'ideas',phase,'done',artifact)
            if phase in gate.REVIEW_REQUIRED_PHASES:
                inputs = [artifact]
                if phase == 'sec-research-refine-pipeline':
                    inputs = ['refine-logs']
                receipt = fixture_receipt(self.root,phase,'ideas',inputs)
                state.accept(str(self.root),'ideas',phase,receipt,'gemini-3.8-flash-high')

    def test_default_is_gemini_and_no_codex_fallback(self):
        route = reviewer_route.resolve_route(self.root,'codex')
        self.assertEqual(route['backend'],'antigravity')
        self.assertEqual(route['model'],'gemini-3.8-flash-high')
        for backend in ('codex','claude-code','grok'):
            with self.assertRaises(ValueError):
                reviewer_route.resolve_route(self.root,'codex',reviewer=backend)

    def test_reviewer_documented_cli(self):
        proc = subprocess.run([sys.executable,str(REPO/'tools/reviewer_route.py'),'--project',str(self.root),'--host','codex'],capture_output=True,text=True)
        self.assertEqual(proc.returncode,0,proc.stderr)
        self.assertEqual(json.loads(proc.stdout)['backend'],'antigravity')

    def test_independent_install_initializes_and_links(self):
        proc = subprocess.run(['bash',str(REPO/'tools/install_sec_paper.sh'),'--project',str(self.root)],capture_output=True,text=True)
        self.assertEqual(proc.returncode,0,proc.stderr)
        self.assertTrue((self.root/'.aris/reviewer.json').is_file())
        self.assertEqual(json.loads((self.root/'.aris/sec-paper.json').read_text())['repo_root'],str(REPO))
        self.assertTrue((self.root/'.agents/skills/sec-paper-audit/SKILL.md').is_file())

    def test_installer_preserves_real_skill_directory(self):
        self.put('.agents/skills/sec-ablation-planner/user.txt','user work')
        proc = subprocess.run(['bash',str(REPO/'tools/install_sec_paper.sh'),'--project',str(self.root)],capture_output=True,text=True)
        self.assertNotEqual(proc.returncode,0)
        self.assertEqual((self.root/'.agents/skills/sec-ablation-planner/user.txt').read_text(),'user work')

    def test_creator_calls_owned_novelty_skill(self):
        text = (REPO/'skills/sec-idea-creator/SKILL.md').read_text()
        self.assertNotIn('`/novelty-check`',text)
        self.assertIn('/sec-novelty-check',text)

    def test_nested_candidate_is_not_empty(self):
        file = self.put('report.md','## Ranked Ideas\n\n### Candidate 1\nbody\n## Next\n')
        self.assertEqual(gate._section_has_content(file,'ranked-ideas'),(True,True))
        file.write_text('## Ranked Ideas\n### Candidate 1\n## Next\n')
        self.assertEqual(gate._section_has_content(file,'ranked-ideas'),(True,False))

    def test_section_snapshot_allows_other_sections_but_detects_owned_edits(self):
        file = self.put('report.md','## Ranked Ideas\n### Candidate 1\nbody\n## Later\nx\n')
        before = evidence.snapshot(self.root,['report.md#ranked-ideas'])
        file.write_text(file.read_text().replace('Later\nx','Later\ny'))
        self.assertEqual(before,evidence.snapshot(self.root,['report.md#ranked-ideas']))
        file.write_text(file.read_text().replace('body','changed'))
        self.assertNotEqual(before,evidence.snapshot(self.root,['report.md#ranked-ideas']))

    def test_arbitrary_trace_id_is_rejected(self):
        state.start_run(str(self.root),'r',['sec-research-review'])
        self.put('report.md')
        state.set_status(str(self.root),'r','sec-research-review','done','report.md')
        with self.assertRaises((OSError,ValueError)):
            state.accept(str(self.root),'r','sec-research-review','FAKE_ID','gemini-3.8-flash-high')

    def test_full_discovery_gate_and_resume(self):
        self.complete_discovery()
        result = gate.run(self.root,'ideas','idea-stage/IDEA_REPORT.md')
        self.assertEqual(result.verdict,'PASS',result.reasons)
        self.assertIsNone(state.resume_point(str(self.root),'ideas'))

    def test_missing_plan_empty_proposal_block(self):
        self.complete_discovery()
        (self.root/'refine-logs/EXPERIMENT_PLAN.md').unlink()
        (self.root/'refine-logs/FINAL_PROPOSAL.md').write_text('')
        self.assertEqual(gate.evaluate(self.root,state.load_run(str(self.root),'ideas')).verdict,'BLOCKED')

    def test_stale_receipt_blocks_gate_and_resume(self):
        self.complete_discovery()
        report = self.root/'idea-stage/IDEA_REPORT.md'
        report.write_text(report.read_text().replace('novelty\n','ABANDON\n'))
        self.assertEqual(gate.evaluate(self.root,state.load_run(str(self.root),'ideas')).verdict,'BLOCKED')
        self.assertEqual(state.resume_point(str(self.root),'ideas')['phase'],'sec-novelty-check')

    def test_trace_changed_and_negative_and_wrong_run_block(self):
        self.put('report.md')
        for verdict in ('REVISE','BLOCK','ABANDON','CONTINUE'):
            path = fixture_receipt(self.root,'sec-research-review','r',['report.md'],verdict)
            with self.assertRaises(ValueError): evidence.validate_receipt(self.root,path)
        path = fixture_receipt(self.root,'sec-research-review','r',['report.md'])
        with self.assertRaises(ValueError): evidence.validate_receipt(self.root,path,run_id='different')
        data=json.loads((self.root/path).read_text())
        (self.root/data['raw_trace']).write_text('{}')
        with self.assertRaises(ValueError): evidence.validate_receipt(self.root,path)

    def test_warm_final_and_same_family_advance_block(self):
        self.put('report.md')
        state.start_run(str(self.root),'r',['sec-research-review'])
        state.set_status(str(self.root),'r','sec-research-review','done','report.md')
        path=fixture_receipt(self.root,'sec-research-review','r',['report.md'],topology='warm')
        with self.assertRaises(ValueError): state.accept(str(self.root),'r','sec-research-review',path,'gemini-3.8-flash-high')
        with self.assertRaises(ValueError): state.mark_provisional(str(self.root),'r','sec-research-review','x','codex')
        with self.assertRaises(ValueError): state.start_run(str(self.root),'p',['x'],provisional_advances=True)

    def test_parent_child_namespace_collision_rejected(self):
        state.start_run(str(self.root),'r',['sec-idea-discovery'])
        with self.assertRaises(ValueError): state.start_run(str(self.root),'r',list(gate.REQUIRED_PHASES))
        child=state.start_run(str(self.root),'r-ideas',list(gate.REQUIRED_PHASES),parent_run_id='r')
        self.assertEqual(child['parent_run_id'],'r')

    def test_review_loop_needs_explicit_stop_and_all_gates(self):
        self.put('results.json','{}')
        receipt=fixture_receipt(self.root,'sec-auto-review-loop','r',['results.json'],decision='PASS')
        with self.assertRaises(ValueError): evidence.validate_receipt(self.root,receipt)
        extra={'score':7,'hard_gates':dict.fromkeys(('threat_model','oracle','adaptive_attacker','ethics','artifacts'),'PASS')}
        receipt=fixture_receipt(self.root,'sec-auto-review-loop','r',['results.json'],decision='STOP',extra=extra)
        self.assertTrue(evidence.validate_receipt(self.root,receipt))
        extra['hard_gates']['oracle']='FAIL'
        receipt=fixture_receipt(self.root,'sec-auto-review-loop','r',['results.json'],decision='STOP',extra=extra)
        with self.assertRaises(ValueError): evidence.validate_receipt(self.root,receipt)

    def test_submission_final_audits_and_staleness(self):
        for file in ('paper/main.tex','paper/main.pdf','paper/references.bib','FACT_PACK.md','contract.md','results/run.json','artifact/README.md','artifact/reproduce.py','paper/venue-policy.json'):
            self.put(file)
        inputs=['paper','FACT_PACK.md','contract.md','results','artifact']
        manifest=dict(schema_version=1,run_id='paper-run',paper_dir='paper',fact_pack='FACT_PACK.md',research_contract='contract.md',raw_results=['results'],venue_policy='paper/venue-policy.json',artifact_readme='artifact/README.md',artifact_dir='artifact',theory_claims=False,audits={})
        for kind in ('claims','citations','adversarial','proof','artifact'):
            manifest['audits'][kind]=fixture_receipt(self.root,'paper-'+kind,'paper-run',inputs,decision='NOT_APPLICABLE' if kind=='proof' else 'PASS',extra={'reason':'fixture has no proof claims'})
        self.put('paper/.aris/pdf-check.json',json.dumps(dict(status='PASS',inputs=['paper'],snapshot=evidence.snapshot(self.root,['paper']),pdf='paper/main.pdf')))
        # Actual gate must require that the format check used the venue policy.
        pdf_check=json.loads((self.root/'paper/.aris/pdf-check.json').read_text())
        pdf_check['inputs'].append('paper/venue-policy.json')
        pdf_check['snapshot']=evidence.snapshot(self.root,pdf_check['inputs'])
        self.put('paper/.aris/pdf-check.json',json.dumps(pdf_check))
        self.put('.aris/submission.json',json.dumps(manifest))
        self.assertTrue(submission_gate.evaluate(self.root,'.aris/submission.json')['submission_ready'])
        self.put('results/run.json','changed evidence')
        with self.assertRaises(ValueError): submission_gate.evaluate(self.root,'.aris/submission.json')

    def test_path_escape_rejected(self):
        with self.assertRaises(ValueError): evidence.snapshot(self.root,['../outside'])


if __name__ == '__main__': unittest.main()
