"""Generated content must survive disabled or failed scripting, in both formats."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

from test_first_run import load, ROOT, SITE


def fixture(destination):
    project = load('progressive_demo', ROOT / 'examples/create_demo.py').create(destination)
    (project / 'narrative.json').write_text(json.dumps({
        'title': 'Fictional discussion', 'dek': 'Original regression fixture',
        'sections': [{'heading': 'Retain the final decision', 'blocks': [
            {'type': 'para', 'text': 'The discussion remains readable without a script.'}]}],
        'coda': 'Final discussion conclusion.'}))
    for extra in ([], ['--dist', str(project / 'dist')]):
        subprocess.run([sys.executable, str(SITE), str(project), *extra], check=True, capture_output=True)
    return project


class ProgressiveRendererTests(unittest.TestCase):
    def test_default_visibility_and_native_anchor_targets(self):
        with tempfile.TemporaryDirectory() as directory:
            project = fixture(Path(directory) / 'demo')
            for output in (project / 'digest.html', project / 'dist/index.html'):
                with self.subTest(format=output.name):
                    source = output.read_text()
                    ids = re.findall(r'\bid="([^"]+)"', source)
                    self.assertEqual(len(ids), len(set(ids)))
                    for target in re.findall(r'href="#([^"]+)"', source):
                        self.assertIn(target, ids)
                    css = source.split('<style>', 1)[1].split('</style>', 1)[0]
                    for selector in ('.ovgrid', '.session', '.essaywrap'):
                        self.assertRegex(css, re.escape(selector) + r'\{display:block[;}]')
                    # Catch the actual blank-preview regression, not merely text in hidden markup.
                    for selectors, declarations in re.findall(r'([^{}]+)\{([^{}]*)\}', css):
                        if 'display:none' in declarations and any(token in selectors for token in
                                ('.ovgrid', '.session', '.essaywrap', '.detailwrap', '.ovwrap', '.masthead')):
                            for selector in selectors.split(','):
                                self.assertIn('html.enhanced', selector)
                    self.assertIn('Final discussion conclusion.', source)
                    self.assertEqual(source.count('<figure class="slide">'), 2)

    @unittest.skipUnless(shutil.which('node'), 'Node required for routing/initialization execution')
    def test_routing_enhances_only_after_successful_initialization(self):
        with tempfile.TemporaryDirectory() as directory:
            project = fixture(Path(directory) / 'demo')
            for output in (project / 'digest.html', project / 'dist/index.html'):
                source = output.read_text()
                script = source.split('<script>', 1)[1].split('</script>', 1)[0]
                sid = re.search(r'<article class="session" id="([^"]+)"', source)[1]
                group = re.search(r'<section class="ovgrid" id="([^"]+)"', source)[1]
                harness = r'''
const assert=require('node:assert/strict'), vm=require('node:vm');
const script=SCRIPT, sid=SID, group=GROUP;
for(const hash of ['', '#'+sid, '#essay', '#%']){
 const classes=initial=>{const set=new Set(initial);return {contains:x=>set.has(x),add:x=>set.add(x),remove:x=>set.delete(x),toggle:(x,on)=>on?set.add(x):set.delete(x)}};
 const grid={dataset:{day:group},classList:classes([])};
 const panel={dataset:{day:group},classList:classes(['session'])};
 const root={classList:classes([])};
 const body={dataset:{},classList:classes([])};
 const events={};
 const context={document:{documentElement:root,body,
  querySelectorAll:q=>q==='.ovgrid'?[grid]:q==='.session'?[panel]:[],
  getElementById:id=>id===sid?panel:id==='essay'?{}:null},
  location:{hash},window:{scrollTo(){}},localStorage:{getItem(){throw Error('storage blocked')}},
  addEventListener:(type,fn)=>events[type]=fn};
 vm.createContext(context);
 if(hash==='#%'){
  assert.throws(()=>vm.runInContext(script,context));
  assert.equal(root.classList.contains('enhanced'),false);
 }else{
  vm.runInContext(script,context);
  assert.equal(root.classList.contains('enhanced'),true);
  assert.equal(body.dataset.view,hash==='#essay'?'essay':hash?'detail':'overview');
  context.location.hash='#'+sid;events.hashchange();assert.equal(body.dataset.view,'detail');
  assert.equal(panel.classList.contains('active'),true);
  context.location.hash='#'+group;events.hashchange();assert.equal(body.dataset.view,'overview');
 }
}
'''.replace('SCRIPT', json.dumps(script)).replace('SID', json.dumps(sid)).replace('GROUP', json.dumps(group))
                result = subprocess.run(['node', '-e', harness], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)

    @unittest.skipUnless(os.environ.get('VIDEO_DIGEST_CHROME') and shutil.which('node'),
                         'Set VIDEO_DIGEST_CHROME to an existing Chromium binary; Node 22+ required')
    def test_real_browser_without_and_with_javascript(self):
        with tempfile.TemporaryDirectory() as directory:
            project = fixture(Path(directory) / 'demo')
            result = subprocess.run(['node', str(ROOT / 'tests/browser_progressive.mjs'), str(project)],
                                    capture_output=True, text=True, timeout=180)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
