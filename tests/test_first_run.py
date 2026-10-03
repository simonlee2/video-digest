import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'plugins/video-digest/skills/video-digest/stages'
SITE = SKILLS / 'video-digest-site/scripts/vd_site.py'
PROBE = SKILLS / 'video-digest-ingest/scripts/vd_probe.py'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FirstRunTests(unittest.TestCase):
    def test_probe_empty_playlist_and_missing_entry(self):
        probe = load('probe', PROBE)
        for entries, count in [([], 0), ([None, {'id': 'abc', 'title': 'Example'}], 1)]:
            with patch.object(probe.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, json.dumps({'entries': entries}))):
                self.assertEqual(len(probe.probe_url('https://example.com')[1]), count)

    def test_single_video_uses_page_url_not_media_url(self):
        probe = load('probe', PROBE)
        with patch.object(probe.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, json.dumps({'id': 'abc', 'url': 'https://cdn.example/media'}))):
            self.assertEqual(probe.probe_url('https://youtu.be/abc')[1][0]['url'], 'https://youtu.be/abc')

    def test_unknown_duration_retained_in_worklist(self):
        probe = load('probe', PROBE)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'worklist.json'
            with patch.object(sys, 'argv', [str(PROBE), 'https://example.com', '--json', str(output)]), patch.object(probe, 'probe_url', return_value=('Example', [{'idx': 1, 'id': 'abc', 'title': 'Unknown', 'duration': None}])):
                probe.main()
            self.assertEqual(len(json.loads(output.read_text())['items']), 1)

    def test_probe_bad_source_has_actionable_error(self):
        result = subprocess.run([sys.executable, str(PROBE), '/missing/folder'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('not a folder', result.stderr)
        self.assertNotIn('Traceback', result.stderr)

    def test_demo_both_modes_and_slide_cap(self):
        demo = load('demo', ROOT / 'examples/create_demo.py')
        with tempfile.TemporaryDirectory() as directory:
            project = demo.create(Path(directory) / 'demo')
            cfg_path = project / 'digest.json'
            cfg = json.loads(cfg_path.read_text())
            cfg['slide_cap'] = 1
            cfg_path.write_text(json.dumps(cfg))
            highlights_path = next(project.glob('groups/*/*/highlights.json'))
            highlights = json.loads(highlights_path.read_text())
            for talk in highlights.values():
                for highlight in talk['highlights']:
                    highlight.update(image_alt='A chart of feedback loops', editorial_heading='Measure the learning loop',
                                     editorial_notes=['Compare decisions before and after feedback.', 'Retain the later evidence too.'])
            highlights_path.write_text(json.dumps(highlights))
            for arguments, output in [([], project / 'digest.html'), (['--dist', str(project / 'dist')], project / 'dist/index.html')]:
                result = subprocess.run([sys.executable, str(SITE), str(project), *arguments], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('1 slides', result.stdout)
                self.assertIn('Small feedback loops', output.read_text())
                self.assertIn('alt="A chart of feedback loops"', output.read_text())
                self.assertIn('<strong>Measure the learning loop</strong>', output.read_text())
                self.assertIn('<li>Retain the later evidence too.</li>', output.read_text())
            self.assertEqual(len(list((project / 'dist/assets').glob('*.jpg'))), 1)
            with self.assertRaises(FileExistsError):
                demo.create(project)
