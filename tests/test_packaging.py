import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]

class PackagingTests(unittest.TestCase):
    def test_manifest_identity_and_skill_tree(self):
        plugin = ROOT / 'plugins/video-digest'
        manifests = [json.loads((plugin / name).read_text()) for name in
                     ('plugin.json', '.codex-plugin/plugin.json', '.claude-plugin/plugin.json')]
        self.assertEqual(len({(m['name'], m['version']) for m in manifests}), 1)
        self.assertLessEqual(len(manifests[0]['extensions']['com.openai']['interface']['shortDescription']), 30)
        self.assertEqual(manifests[0]['extensions']['com.openai']['interface'], manifests[1]['interface'])
        entry = plugin / 'skills/video-digest'
        self.assertEqual(list((plugin / 'skills').glob('*/SKILL.md')), [entry / 'SKILL.md'])
        self.assertEqual(len(list(entry.rglob('SKILL.md'))), 1)
        self.assertEqual(len(list((entry / 'stages').glob('*/STAGE.md'))), 5)
        self.assertNotIn('user-invocable:', (entry / 'SKILL.md').read_text())
        for marketplace in ('.agents/plugins/marketplace.json', '.claude-plugin/marketplace.json'):
            source = json.loads((ROOT / marketplace).read_text())['plugins'][0]['source']
            path = source['path'] if isinstance(source, dict) else source
            self.assertEqual((ROOT / path).resolve(), plugin.resolve())

    def test_bundled_relative_references_stay_inside_install_unit(self):
        entry = ROOT / 'plugins/video-digest/skills/video-digest'
        for document in entry.rglob('*.md'):
            for target in re.findall(r'\]\(([^)]+)\)', document.read_text()):
                if '://' in target or target.startswith('#'):
                    continue
                target = target.split('#', 1)[0]
                resolved = (document.parent / target).resolve()
                self.assertTrue(resolved.is_relative_to(entry.resolve()), (document, target))
                self.assertTrue(resolved.exists(), (document, target))

    def test_doctor_help_and_structured_report(self):
        doctor = ROOT / 'plugins/video-digest/skills/video-digest/scripts/doctor.py'
        result = subprocess.run([sys.executable, str(doctor), '--help'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        result = subprocess.run([sys.executable, str(doctor), '--json'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertTrue(report['ready'])
        self.assertEqual(report['route'], 'demo')

    def test_missing_pillow_fails_before_creating_project(self):
        spec = importlib.util.spec_from_file_location('preflight_install', ROOT / 'scripts/check_install.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'untouched'
            failed = subprocess.CompletedProcess([], 1, '{}', 'Missing: Pillow in the selected Python environment')
            with patch.object(module.subprocess, 'run', return_value=failed):
                with self.assertRaisesRegex(RuntimeError, 'Pillow'):
                    module.check(destination)
            self.assertFalse(destination.exists())

    def test_clean_project_install_and_render(self):
        spec = importlib.util.spec_from_file_location('check_install', ROOT / 'scripts/check_install.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temporary:
            for host in ('codex', 'claude', 'generic'):
                destination = Path(temporary) / ('isolated project ' + host)
                module.check(destination, host=host)
                skills = destination / ('.claude/skills' if host == 'claude' else '.agents/skills')
                self.assertTrue((skills / 'video-digest/scripts/doctor.py').is_file())
                self.assertEqual(len(list(skills.rglob('SKILL.md'))), 1)
                with self.assertRaises(FileExistsError):
                    module.check(destination, host=host)
