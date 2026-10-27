"""PDF-check fixtures; a passing technical fixture is NOT a real submission."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

REPO=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO/'tools'))
import paper_check


class PaperCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        (self.root/'paper').mkdir()
        (self.root/'paper/official-cfp.md').write_text('TEST FIXTURE ONLY, NOT AN ACTUAL VENUE POLICY')
        self.policy=dict(official_url='https://example.invalid/test-fixture',cycle='TEST_ONLY',retrieved_at=date.today().isoformat(),saved_cfp='paper/official-cfp.md',max_total_pages=2,required_sections=[],forbidden_identifiers=[])
        self.save_policy()

    def save_policy(self):
        (self.root/'paper/venue-policy.json').write_text(json.dumps(self.policy))

    def test_missing_pdf_is_blocked(self):
        result=paper_check.check(self.root,'paper','paper/main.pdf','paper/venue-policy.json')
        self.assertEqual(result['status'],'BLOCKED')

    def test_invalid_venue_policy_rejected(self):
        self.policy['max_total_pages']=0;self.save_policy()
        with self.assertRaises(ValueError):paper_check.check(self.root,'paper','paper/main.pdf','paper/venue-policy.json')

    @unittest.skipUnless(all(shutil.which(x) for x in ('latexmk','pdfinfo','pdftotext','pdffonts')), 'real TeX/PDF tools not installed')
    def test_real_compile_pdf_inspection_and_stale_source(self):
        tex=self.root/'paper/main.tex'
        tex.write_text(r'\documentclass{article}\begin{document}Anonymous technical test fixture.\end{document}')
        proc=subprocess.run(['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error','main.tex'],cwd=tex.parent,capture_output=True,text=True,timeout=90)
        self.assertEqual(proc.returncode,0,proc.stdout[-2000:]+proc.stderr[-1000:])
        result=paper_check.check(self.root,'paper','paper/main.pdf','paper/venue-policy.json')
        self.assertEqual(result['status'],'PASS',result)
        tex.write_text(tex.read_text()+'\n% source changed after compilation\n')
        result=paper_check.check(self.root,'paper','paper/main.pdf','paper/venue-policy.json')
        self.assertEqual(result['status'],'BLOCKED')
        self.assertTrue(any('older' in item for item in result['failures']))


if __name__=='__main__':unittest.main()
