import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

REPO=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO/'tools'))
import jobs


class JobTests(unittest.TestCase):
    def setUp(self):
        self.temporary=tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root=Path(self.temporary.name)

    def spec(self, name='job', command=None, timeout=3):
        return dict(id=name,command=command or [sys.executable,'-c','import os; print(os.environ["SEC_PAPER_SEED"])'],target='LOCAL_TEST_FIXTURE',target_revision='TEST_ONLY',seed=42,isolation_key='target-'+name,timeout_seconds=timeout)

    def wait(self,name):
        deadline=time.monotonic()+12
        while time.monotonic()<deadline:
            data=jobs.status(self.root,name)
            if data['status'] in jobs.TERMINAL:return data
            time.sleep(.05)
        self.fail('test worker did not finish')

    def test_success_and_resume_same_id_and_logs(self):
        spec=self.spec()
        jobs.start(self.root,spec)
        data=self.wait('job')
        self.assertEqual(data['status'],'SUCCEEDED')
        self.assertEqual((self.root/'results/job/stdout.log').read_text().strip(),'42')
        self.assertEqual(jobs.start(self.root,spec)['status'],'SUCCEEDED')
        changed=dict(spec,seed=99)
        with self.assertRaises(ValueError):jobs.start(self.root,changed)

    def test_timeout_preserves_partial_evidence(self):
        jobs.start(self.root,self.spec(command=[sys.executable,'-c','import time; print("partial",flush=True); time.sleep(20)'],timeout=.2))
        self.assertEqual(self.wait('job')['status'],'TIMED_OUT')
        self.assertIn('partial',(self.root/'results/job/stdout.log').read_text())

    def test_cancel_and_isolation_key(self):
        spec=self.spec(command=[sys.executable,'-c','import time;time.sleep(20)'])
        jobs.start(self.root,spec)
        other=self.spec('other');other['isolation_key']=spec['isolation_key']
        with self.assertRaises(ValueError):jobs.start(self.root,other)
        (jobs.job_dir(self.root,'job')/'cancel').touch()
        self.assertEqual(self.wait('job')['status'],'CANCELLED')

    def test_queue_six_jobs_and_dependency(self):
        specs=[self.spec('j'+str(i)) for i in range(6)]
        specs[-1]['after']=['j0','j1']
        result=jobs.run_queue(self.root,specs,3)
        self.assertTrue(all(s['status']=='SUCCEEDED' for s in result.values()))
        self.assertGreaterEqual(result['j5']['started_at'],result['j0']['finished_at'])

    def test_fail_and_unsupported_backend(self):
        jobs.start(self.root,self.spec(command=[sys.executable,'-c','raise SystemExit(9)']))
        self.assertEqual(self.wait('job')['status'],'FAILED')
        with self.assertRaises(ValueError):jobs.start(self.root,dict(self.spec('other'),backend='ssh'))

    def test_cycle_is_rejected_before_launch(self):
        first=self.spec('a');second=self.spec('b')
        first['after']=['b'];second['after']=['a']
        with self.assertRaises(ValueError):jobs.run_queue(self.root,[first,second],2)
        self.assertFalse(jobs.job_dir(self.root,'a').exists())

    def test_interrupted_worker_is_not_retried(self):
        directory=jobs.job_dir(self.root,'lost');directory.mkdir(parents=True)
        (directory/'state.json').write_text(json.dumps(dict(status='RUNNING',created_at=time.time()-60,isolation_key='held')))
        self.assertEqual(jobs.status(self.root,'lost')['status'],'INTERRUPTED')
        spec=self.spec('new');spec['isolation_key']='held'
        with self.assertRaises(ValueError):jobs.start(self.root,spec)


if __name__=='__main__':unittest.main()
