#!/usr/bin/env python3
"""Check existing dependencies; never installs, logs in, downloads or calls a model."""
import argparse
import importlib.util
import json
import platform
import shutil
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--json', action='store_true', help='print a machine-readable report')
parser.add_argument('--require', choices=('demo', 'media', 'transcription'), default='demo', help='return nonzero if this route lacks dependencies')
args = parser.parse_args()
tools = {name: shutil.which(name) for name in ('yt-dlp', 'ffmpeg', 'ffprobe', 'uv', 'uvx')}
missing = []
if not importlib.util.find_spec('PIL'):
    missing.append('Pillow in the selected Python environment')
if args.require in ('media', 'transcription'):
    missing.extend(name for name in ('ffmpeg', 'ffprobe') if not tools[name])
if args.require == 'transcription':
    if not tools['uvx']: missing.append('uvx')
    if sys.platform != 'darwin' or platform.machine() != 'arm64': missing.append('Apple Silicon for bundled mlx-whisper, or an alternate transcript adapter')
report = {'python': platform.python_version(), 'route': args.require, 'ready': not missing, 'missing': missing,
          'tools': tools, 'notes': ['yt-dlp required only for remote acquisition.', 'First transcription may download packages/model weights.', 'Editorial uses your agent text/vision model; provider processing and charges may apply.']}
if args.json:
    print(json.dumps(report, indent=2))
else:
    print(f"{args.require}: {'ready' if report['ready'] else 'missing dependencies'}")
    for name,path in tools.items(): print(f'{name}: {path or "not found"}')
    for note in report['notes']: print(note)
if missing: print('Missing: ' + '; '.join(missing), file=sys.stderr)
sys.exit(0 if report['ready'] else 1)
