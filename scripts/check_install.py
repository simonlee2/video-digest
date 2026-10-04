#!/usr/bin/env python3
"""Copy only the self-contained skill into a fresh project and run its offline demo."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def prepare_skills(source, installed, host):
    # Host selection changes discovery location, not the portable skill content.
    installed.mkdir(parents=True)
    shutil.copytree(source / 'video-digest', installed / 'video-digest',
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store'))

def check(destination, host='codex'):
    if destination.exists():
        raise FileExistsError(destination)
    doctor = ROOT / 'plugins/video-digest/skills/video-digest/scripts/doctor.py'
    ready = subprocess.run([sys.executable, str(doctor), '--json'], capture_output=True, text=True)
    if ready.returncode:
        raise RuntimeError(ready.stderr.strip() + '\nUse a Python environment with Pillow, or run with uv run --with pillow python if downloads are authorized.')
    destination.mkdir(parents=True, exist_ok=False)
    installed = destination / ('.claude/skills' if host == 'claude' else '.agents/skills')
    prepare_skills(ROOT / 'plugins/video-digest/skills', installed, host)
    skill = installed / 'video-digest'
    assert len(list(installed.iterdir())) == 1
    assert len(list(skill.rglob('SKILL.md'))) == 1
    project = destination / 'demo'
    subprocess.run([sys.executable, str(skill / 'scripts/demo.py'), str(project)], check=True)
    source = json.loads(next(project.glob('groups/*/*/highlights.json')).read_text())
    for artifact in (project / 'digest.html', project / 'dist/index.html'):
        rendered = artifact.read_text()
        for talk in source.values():
            for point in talk['highlights']:
                assert point['text'] in rendered
                for note in point['editorial_notes']:
                    assert note in rendered
    print(f'PASS: isolated single skill; both builds preserve all highlights and editorial notes.\nReview: {project / "digest.html"}')
    return destination

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', choices=('codex', 'claude', 'generic'), default='codex')
    parser.add_argument('destination', type=Path, help='new project directory; refuses existing paths')
    args = parser.parse_args()
    try:
        check(args.destination.resolve(), args.host)
    except FileExistsError:
        parser.exit(1, 'Destination exists. Choose a new directory; nothing was overwritten.\n')
    except RuntimeError as exc:
        parser.exit(1, str(exc) + '\n')
