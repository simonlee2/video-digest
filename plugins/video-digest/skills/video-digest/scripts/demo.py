#!/usr/bin/env python3
"""Build the bundled fictional reference with no media, model or network calls."""
import argparse
from pathlib import Path
import subprocess
import sys
from create_demo import create

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('output', type=Path, help='new directory; refuses overwrite')
args = parser.parse_args()
try:
    project = create(args.output.resolve())
except FileExistsError:
    parser.exit(1, 'Output exists; choose a new directory.\n')
builder = Path(__file__).resolve().parents[1] / 'stages/video-digest-site/scripts/vd_site.py'
for options in ([], ['--dist', str(project / 'dist')]):
    subprocess.run([sys.executable, str(builder), str(project), *options], check=True)
print(f'Open {project / "digest.html"}. Fictional reference; not a real-video quality benchmark.')
