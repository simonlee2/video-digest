#!/usr/bin/env python3
"""Package local source and plugin archives without git mutation or publication."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
import tempfile
import shutil
from check_install import prepare_skills

ROOT = Path(__file__).resolve().parents[1]

def files_under(root):
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise ValueError(f'Symlink not allowed in release: {path}')
        if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc' and path.name != '.DS_Store':
            yield path

def package(destination):
    destination.mkdir(parents=True, exist_ok=False)
    plugin = ROOT / 'plugins/video-digest'
    version = json.loads((plugin / 'plugin.json').read_text())['version']
    archives = []
    for host in ('claude', 'codex'):
        archive = destination / f'video-digest-{version}-{host}-plugin.zip'
        with tempfile.TemporaryDirectory() as temporary:
            staged = Path(temporary) / 'video-digest'
            shutil.copytree(plugin, staged, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            shutil.rmtree(staged / 'skills')
            prepare_skills(plugin / 'skills', staged / 'skills', host)
            shutil.rmtree(staged / ('.claude-plugin' if host == 'codex' else '.codex-plugin'))
            with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
                for path in files_under(staged):
                    z.write(path, Path('video-digest') / path.relative_to(staged))
                z.write(ROOT / 'LICENSE', 'video-digest/LICENSE')
        archives.append(archive)
    archive = destination / f'video-digest-{version}-skill.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for path in files_under(plugin / 'skills/video-digest'):
            z.write(path, Path('video-digest') / path.relative_to(plugin / 'skills/video-digest'))
    archives.append(archive)
    archive = destination / f'video-digest-{version}-source.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for name in ('README.md', 'INSTALL.md', 'LICENSE', 'RELEASE_CANDIDATE.md', 'COMPATIBILITY.md', 'DEVELOPMENT.md', 'EVALUATION.md', '.gitignore'):
            z.write(ROOT / name, Path('video-digest') / name)
        for name in ('.agents', '.claude-plugin', 'plugins', 'examples', 'scripts', 'tests'):
            for path in files_under(ROOT / name):
                z.write(path, Path('video-digest') / path.relative_to(ROOT))
    archives.append(archive)
    (destination / 'SHA256SUMS').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in archives))
    print('\n'.join(str(p) for p in archives))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path, help='new release directory')
    args = parser.parse_args()
    try:
        package(args.destination.resolve())
    except FileExistsError:
        parser.exit(1, 'Destination exists; choose a new directory.\n')
