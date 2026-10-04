import json
from pathlib import Path
import runpy
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT=Path(__file__).resolve().parents[1]/'plugins/video-digest/skills/video-digest/stages/video-digest-slides/scripts/vd_frames.py'

class FrameTimeTests(unittest.TestCase):
    def test_actual_offset_times_survive_failed_candidate(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'sessions').mkdir()
            talk={'id':1,'title':'Fixture','speaker':'Test','start':'00:00:00','end':'00:00:10','clip':'clips/01_test.mp4','program':{'kind':'talk'}}
            (root/'manifest.json').write_text(json.dumps({'talks':[talk]}))
            (root/'sessions/01_test.md').write_text('- **[00:00:04]** Useful highlight\n')
            def extract(command,**kwargs):
                if command[-1].endswith('_0.jpg'):return
                Path(command[-1]).write_bytes(b'fixture')
            with patch.object(sys,'argv',[str(SCRIPT),str(root)]),patch('subprocess.run',side_effect=extract):
                runpy.run_path(str(SCRIPT),run_name='__main__')
            highlight=json.loads((root/'highlights.json').read_text())['01_test']['highlights'][0]
            self.assertEqual(highlight['files'],['h00_1.jpg','h00_2.jpg'])
            self.assertEqual(highlight['frame_seconds'],[4,9])
