#!/usr/bin/env python3
"""Acquire one video with yt-dlp defaults, or reuse a local file.

Usage: vd_acquire.py ITEM SOURCE [-- YT_DLP_OPTIONS...]
Creates source.mp4 as a compatibility symlink; its actual container may differ.
"""
import argparse
import json
from pathlib import Path
import subprocess


def validate(path):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                             '-of', 'json', str(path)], capture_output=True, text=True, check=True)
    info = json.loads(result.stdout)
    kinds = {s.get('codec_type') for s in info.get('streams', [])}
    if not {'video', 'audio'} <= kinds or float(info.get('format', {}).get('duration', 0)) <= 0:
        raise ValueError(f'{path}: expected video, audio, and a positive duration')
    # Decode an actual frame: successful download/metadata alone is insufficient.
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-frames:v', '1',
                    '-f', 'null', '-'], capture_output=True, text=True, check=True)
    return info


def acquire(item, source, options=()):
    item = item.resolve()
    item.mkdir(parents=True, exist_ok=True)
    alias = item / 'source.mp4'
    if alias.exists():
        media = alias.resolve()
    elif Path(source).is_file():
        media = Path(source).resolve()
    else:
        cached = [p for p in item.glob('video.*') if p.suffix.lower() in {'.mp4', '.webm', '.mkv', '.mov'} and p.is_file()]
        if len(cached) > 1:
            raise ValueError('Multiple cached videos; choose one explicitly as SOURCE')
        if cached:
            media = cached[0]
        else:
            result = subprocess.run(['yt-dlp', *options, '--no-playlist', '--print', 'after_move:filepath',
                                     '-o', str(item / 'video.%(ext)s'), source],
                                    capture_output=True, text=True, check=True)
            paths = result.stdout.strip().splitlines()
            if not paths:
                raise ValueError('yt-dlp did not report a completed media file')
            media = Path(paths[-1]).resolve()
    info = validate(media)
    if media != alias and not alias.exists():
        if alias.is_symlink():
            raise ValueError(f'Broken source symlink: {alias}; repair it before resuming')
        alias.symlink_to(media)
    (item / 'media-probe.json').write_text(json.dumps(info, indent=2) + '\n')
    return media


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('item', type=Path)
    parser.add_argument('source')
    parser.add_argument('options', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    options = args.options[1:] if args.options[:1] == ['--'] else args.options
    try:
        print(acquire(args.item, args.source, options))
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        detail = getattr(exc, 'stderr', None) or str(exc)
        parser.exit(1, f'Acquisition failed: {detail.strip()}\nCheck the installed tools and source access; invalid cached media is not treated as complete.\n')


if __name__ == '__main__':
    main()
