import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'plugins/video-digest/skills/video-digest/scripts/audit_editorial.py'
spec = importlib.util.spec_from_file_location('editorial_audit', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class EditorialAuditTests(unittest.TestCase):
    def fixture(self, root, highlights, selections):
        (root / 'frames/test').mkdir(parents=True)
        (root / 'highlights.json').write_text(json.dumps({'test': {'highlights': highlights}}))
        (root / 'frames/sel_test.json').write_text(json.dumps(selections))
        for h in highlights:
            for filename in h.get('files', []):
                (root / 'frames/test' / filename).write_bytes(b'fixture')

    def test_all_text_and_late_points_count_without_image_quota(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            highlights = [{'i': i, 'text': 'Distinct claim', 'editorial_notes': ['Evidence adds detail'],
                           'evidence_start_seconds': i * 10, 'evidence_end_seconds': i * 10 + 9}
                          for i in range(7)]
            self.fixture(root, highlights, {})
            report = module.audit(root)['talks']['test']
            self.assertEqual(report['highlights'], 7)
            self.assertEqual(report['notes'], 7)
            self.assertEqual(report['editorial_words'], 35)
            self.assertEqual(report['selected_frames'], [])
            self.assertIsNone(report['largest_between_frame_gap'])
            self.assertEqual(report['missing_or_invalid_evidence_highlights'], [])
            self.assertEqual(len(report['exact_repeated_blocks']), 12)

    def test_actual_replacement_offsets_and_unillustrated_priorities(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            highlights = [
                {'i': 0, 'sec': 60, 'files': ['later.jpg'], 'frame_seconds': [90]},
                {'i': 1, 'sec': 180, 'weight': 2},
                {'i': 2, 'sec': 330, 'files': ['before.jpg', 'exact.jpg'], 'frame_seconds': [300, 330]}]
            self.fixture(root, highlights, {'0': 0, '1': None, '2': 0})
            report = module.audit(root)['talks']['test']
            self.assertEqual(report['selected_frames'], [{'highlight': 0, 'seconds': 90}, {'highlight': 2, 'seconds': 300}])
            self.assertEqual(report['largest_between_frame_gap'], {'start_seconds': 90, 'end_seconds': 300, 'seconds': 210})
            self.assertEqual(report['unillustrated_priority_highlights'], [1])

    def test_duplicate_claim_note_and_missing_evidence_are_review_prompts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root, [{'i': 0, 'text': 'Measure actual use.', 'editorial_notes': ['Measure actual use!']}], {})
            report = module.audit(root)['talks']['test']
            self.assertEqual(report['missing_or_invalid_evidence_highlights'], [0])
            self.assertEqual(report['exact_repeated_blocks'][0]['repeat']['field'], 'note')

    def test_invalid_selection_or_unknown_actual_time_fails(self):
        for pick, offsets, error in [(2, [5], 'invalid selection'), (0, [], 'actual frame time')]:
            with self.subTest(pick=pick), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.fixture(root, [{'i': 0, 'files': ['a.jpg'], 'frame_seconds': offsets}], {'0': pick})
                with self.assertRaisesRegex(ValueError, error):
                    module.audit(root)
