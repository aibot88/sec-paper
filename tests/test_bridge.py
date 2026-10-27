"""Offline bridge tests with an explicitly fake local CLI; no live reviews."""
import importlib.util
import json
import os
import queue
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SERVER=Path(__file__).resolve().parents[1]/'tools/antigravity-exec/server.py'
FAKE='''#!/usr/bin/env python3
import json,sys,time,uuid
from pathlib import Path
a=sys.argv[1:]
def arg(k):return a[a.index(k)+1]
p=json.loads(sys.stdin.readline())['message']['content']
t=arg('--conversation') if '--conversation' in a else str(uuid.uuid4())
if p!='NO_METADATA':
 Path(arg('--log-file')).write_text('Propagating selected model override to backend: label="Gemini 3.8 Flash (High)"\\n')
print(json.dumps({'event':'init','conversation_id':t,'init':{'model':'wrong' if p=='WRONG_MODEL' else arg('--model')}}),flush=True)
if p=='SLOW':time.sleep(10)
if p=='EOF':sys.exit(0)
print(json.dumps({'event':'result','result':{'conversation_id':t,'status':'ERROR' if p=='FAIL' else 'WAITING' if p=='WAIT' else 'SUCCESS','response':'' if p=='EMPTY' else 'TEST_FIXTURE:'+p}}),flush=True)
'''


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        fake=self.root/'fake-agy';fake.write_text(FAKE);fake.chmod(0o700)
        env=patch.dict(os.environ,{'AGY_BIN':str(fake),'AGY_EXEC_STATE_DIR':str(self.root/'state'),'AGY_EXEC_TIMEOUT_SEC':'.4'})
        env.start();self.addCleanup(env.stop)
        spec=importlib.util.spec_from_file_location('test_bridge',SERVER)
        self.bridge=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.bridge)
        self.events=[];self.bridge.send_message=self.events.append

    def call(self,prompt,name='antigravity',extra=None):
        args=dict(prompt=prompt,cwd=str(self.root)) if name=='antigravity' else dict(prompt=prompt)
        args.update(extra or {})
        return self.bridge.handle_call({'id':1,'params':{'name':name,'arguments':args}},queue.Queue(),[])['result']

    def test_success_and_continuation(self):
        first=self.call('hello');self.assertFalse(first.get('isError',False))
        thread=first['structuredContent']['threadId']
        reply=self.call('again','antigravity-reply',{'threadId':thread})
        self.assertEqual(reply['structuredContent']['threadId'],thread)

    def test_actual_identity_preserved(self):
        result=self.call('ok')['structuredContent']
        self.assertEqual(result['model'],'gemini-3.8-flash-high')
        self.assertEqual(result['status'],'SUCCESS')

    def test_wrong_model_is_error(self):
        self.assertTrue(self.call('WRONG_MODEL')['isError'])

    def test_failure_wait_empty_eof(self):
        for prompt in ('FAIL','WAIT','EMPTY','EOF'):
            with self.subTest(prompt=prompt):self.assertTrue(self.call(prompt)['isError'])

    def test_timeout_is_error(self):
        self.assertTrue(self.call('SLOW')['isError'])

    def test_missing_effort_metadata_is_not_fabricated(self):
        self.assertIsNone(self.call('NO_METADATA')['structuredContent']['effort'])

    def test_reply_cannot_change_model(self):
        first=self.call('hello')['structuredContent']['threadId']
        result=self.bridge.handle_call({'id':1,'params':{'name':'antigravity-reply','arguments':{'prompt':'x','threadId':first,'model':'wrong'}}},queue.Queue(),[])
        self.assertIn('error',result)

    def test_long_prompt_stays_stdin(self):
        prompt='x'*100000
        self.assertEqual(self.call(prompt)['structuredContent']['content'],'TEST_FIXTURE:'+prompt)


if __name__=='__main__':unittest.main()
