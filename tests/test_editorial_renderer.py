"""Exercise the real CLI and final HTML, including image-loss paths."""
from html.parser import HTMLParser
import json
import re
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_first_run import load, ROOT, SITE


class VisibleContent(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.text = []
        self.alts = []
        self.hidden = 0
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.hidden += 1
        if tag == 'img':
            self.alts.append(dict(attrs).get('alt'))

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.hidden -= 1

    def handle_data(self, data):
        if not self.hidden:
            self.text.append(data)


class EditorialRendererTests(unittest.TestCase):
    def test_group_numbering_spans_sources_without_changing_routes(self):
        demo = load('numbering_demo', ROOT / 'examples/create_demo.py')
        with tempfile.TemporaryDirectory() as directory:
            project = demo.create(Path(directory) / 'demo')
            first = next(project.glob('groups/*/*/source.json')).parent
            second = first.parent / '02-second-source'
            shutil.copytree(first, second)
            metadata = json.loads((second / 'source.json').read_text())
            metadata['key'] = 'second-source'
            (second / 'source.json').write_text(json.dumps(metadata))
            for mode in ('single', 'dist'):
                args = ['--dist', str(project / 'dist')] if mode == 'dist' else []
                subprocess.run([sys.executable, str(SITE), str(project), *args], check=True, capture_output=True)
                source = (project / ('dist/index.html' if args else 'digest.html')).read_text()
                panels = re.findall(r'<article class="session".*?</article>', source, re.S)
                self.assertEqual(len(panels), 2)
                for number, panel in enumerate(panels, 1):
                    self.assertIn(f'No.&nbsp;{number:02d}', panel)
                self.assertIn('id="demo-second-source-t1"', panels[1])
                self.assertNotIn('id="demo-second-source-t2"', source)

    @unittest.skipUnless(shutil.which('node'), 'Node required for image error-handler execution')
    def test_image_fallback_handles_early_and_late_failure(self):
        demo = load('fallback_demo', ROOT / 'examples/create_demo.py')
        with tempfile.TemporaryDirectory() as directory:
            project = demo.create(Path(directory) / 'demo')
            subprocess.run([sys.executable, str(SITE), str(project)], check=True, capture_output=True)
            source = (project / 'digest.html').read_text()
            script = source.split('<script>', 1)[1].split('const grids=', 1)[0]
            harness = '''
const assert=require('node:assert/strict');
function img(complete,width){return {complete,naturalWidth:width,
 addEventListener(type,fn){this.error=fn},replaceWith(node){this.replacement=node}}}
const early=img(true,0),late=img(false,0),healthy=img(true,900);
global.document={createElement:()=>({}),querySelectorAll:()=>[early,late,healthy]};
'''
            checks = '''
assert.equal(early.replacement.textContent,'Image unavailable');
assert.equal(late.replacement,undefined);
late.error();
assert.equal(late.replacement.className,'image-unavailable');
assert.equal(healthy.replacement,undefined);
'''
            result = subprocess.run(['node', '-e', harness + script + checks], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('Record the decision', source)

    def test_selected_frame_links_to_actual_time_without_moving_highlight(self):
        demo = load('timestamp_demo', ROOT / 'examples/create_demo.py')
        with tempfile.TemporaryDirectory() as directory:
            project = demo.create(Path(directory) / 'demo')
            hp = next(project.glob('groups/*/*/highlights.json'))
            source = hp.parent / 'source.json'
            metadata = json.loads(source.read_text())
            metadata['url'] = 'https://www.youtube.com/watch?v=fictional'
            source.write_text(json.dumps(metadata))
            data = json.loads(hp.read_text())
            beat = next(iter(data.values()))['highlights'][0]
            beat.update(sec=60, ts='00:01:00', files=['0.jpg', '0.jpg'], frame_seconds=[55, 65])
            selection = next(hp.parent.glob('frames/sel_*.json'))
            picks = json.loads(selection.read_text()); picks['0'] = 1
            selection.write_text(json.dumps(picks))
            for recorded_times in ([55, 65], []):
                beat['frame_seconds'] = recorded_times
                hp.write_text(json.dumps(data))
                for mode in ('single', 'dist'):
                    with self.subTest(times=recorded_times, mode=mode):
                        args = ['--dist', str(project / 'dist')] if mode == 'dist' else []
                        subprocess.run([sys.executable, str(SITE), str(project), *args], check=True, capture_output=True)
                        output = project / ('dist/index.html' if args else 'digest.html')
                        rendered = output.read_text()
                        self.assertIn('href="https://www.youtube.com/watch?v=fictional&amp;t=60s"', rendered)
                        if recorded_times:
                            self.assertIn('class="frame-source" href="https://www.youtube.com/watch?v=fictional&amp;t=65s"', rendered)
                            self.assertIn('Watch frame at 00:01:05', rendered)
                            self.assertNotIn('&amp;t=55s', rendered)
                        else:
                            self.assertNotIn('Watch frame at 00:01:05', rendered)

    def test_all_approved_content_survives_image_limits_and_missing_frames(self):
        demo = load('editorial_demo', ROOT / 'examples/create_demo.py')
        with tempfile.TemporaryDirectory() as directory:
            project = demo.create(Path(directory) / 'demo')
            hp = next(project.glob('groups/*/*/highlights.json'))
            highlights = json.loads(hp.read_text())
            beats = next(iter(highlights.values()))['highlights']
            self.assertGreater(len(beats), 2)  # catches a first-two-only adapter
            beats[-1]['editorial_notes'].append('Literal <script> is text, not executable markup.')
            hp.write_text(json.dumps(highlights))
            cfg_path = project / 'digest.json'
            base = json.loads(cfg_path.read_text())
            cases = [
                {'slide_cap': 2, 'dedup_threshold': 0},
                {'slide_cap': 1, 'dedup_threshold': 0},
                {'slide_cap': 0},
                {'slide_cap': 2, 'slide_budget': 1, 'slide_floor': 0},
                {'slide_cap': 2, 'dedup_threshold': 255},
            ]
            # A selected frame that is missing must lose only its image.
            beats[2]['files'] = ['missing.jpg']
            hp.write_text(json.dumps(highlights))
            sp = next(hp.parent.glob('frames/sel_*.json'))
            picks = json.loads(sp.read_text()); picks['2'] = 0
            sp.write_text(json.dumps(picks))
            for config in cases:
                cfg_path.write_text(json.dumps({**base, **config}))
                for mode in ('single', 'dist'):
                    with self.subTest(config=config, mode=mode):
                        args = ['--dist', str(project / 'dist')] if mode == 'dist' else []
                        run = subprocess.run([sys.executable, str(SITE), str(project), *args], capture_output=True, text=True)
                        self.assertEqual(run.returncode, 0, run.stderr)
                        output = project / ('dist/index.html' if args else 'digest.html')
                        source = output.read_text()
                        parsed = VisibleContent(source)
                        visible = '\n'.join(parsed.text)
                        previous = -1
                        for beat in beats:
                            position = visible.index(beat['text'])
                            self.assertGreater(position, previous)
                            previous = position
                            self.assertIn(beat['editorial_heading'], visible)
                            for note in beat['editorial_notes']:
                                self.assertIn(note, visible)
                        self.assertIn('Editorial application:', visible)
                        self.assertIn(beats[-1]['editorial_inference'], visible)
                        self.assertIn('&lt;script&gt;', source)
                        if config.get('slide_cap') == 2 and config.get('dedup_threshold') == 0:
                            self.assertIn(beats[0]['image_alt'], parsed.alts)
                            self.assertIn(beats[0]['caption'], visible)
                        if config.get('slide_cap') == 0:
                            self.assertNotIn('<figure class="slide">', source)

    def test_legacy_text_only_highlight_still_renders(self):
        demo = load('legacy_demo', ROOT / 'examples/create_demo.py')
        with tempfile.TemporaryDirectory() as directory:
            project = demo.create(Path(directory) / 'demo')
            hp = next(project.glob('groups/*/*/highlights.json'))
            data = json.loads(hp.read_text())
            for beat in next(iter(data.values()))['highlights']:
                for key in list(beat):
                    if key.startswith('editorial_') or key in ('caption', 'image_alt'):
                        del beat[key]
            hp.write_text(json.dumps(data))
            subprocess.run([sys.executable, str(SITE), str(project)], check=True, capture_output=True)
            visible = '\n'.join(VisibleContent((project / 'digest.html').read_text()).text)
            for beat in next(iter(data.values()))['highlights']:
                self.assertIn(beat['text'], visible)
