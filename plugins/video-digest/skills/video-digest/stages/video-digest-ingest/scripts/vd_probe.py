#!/usr/bin/env python3
"""Probe a digest source: YouTube playlist/channel URL or a local folder of videos.
Prints a worklist (idx, id, duration, title) + totals and ingest estimates.
Usage: vd_probe.py <url|folder> [--json out.json]"""
import argparse, json, subprocess, sys
from pathlib import Path

VIDEO_EXT = {".mp4", ".mkv", ".webm", ".mov", ".m4v", ".avi"}

def probe_url(url):
    r = subprocess.run(["yt-dlp", "--flat-playlist", "-J", url],
                       capture_output=True, text=True, check=True)
    d = json.loads(r.stdout)
    entries = d["entries"] if "entries" in d else [d]  # single video → treat as 1-entry list
    items = []
    for i, e in enumerate(entries or [], 1):
        if not e:
            continue
        items.append({"idx": i, "id": e.get("id"), "title": e.get("title"),
                      "duration": e.get("duration"),
                      "url": e.get("webpage_url") or (e.get("url") if "entries" in d else url) or f"https://youtu.be/{e.get('id')}"})
    return d.get("title") or url, items

def probe_folder(folder):
    items = []
    files = sorted(p for p in Path(folder).iterdir() if p.is_file() and p.suffix.lower() in VIDEO_EXT)
    for i, p in enumerate(files, 1):
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "default=nk=1:nw=1", str(p)], capture_output=True, text=True)
        try: dur = float(r.stdout.strip())
        except ValueError: dur = None
        items.append({"idx": i, "id": p.stem, "title": p.stem,
                      "duration": dur, "url": str(p.resolve())})
    return str(folder), items

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source", help="YouTube URL or folder of videos")
    ap.add_argument("--json", type=Path, dest="output", help="write worklist JSON")
    a = ap.parse_args()
    src = a.source
    if not Path(src).is_dir() and not src.startswith(("https://", "http://")):
        ap.error(f"source is not a folder or HTTP(S) URL: {src}")
    try:
        title, items = probe_folder(src) if Path(src).is_dir() else probe_url(src)
    except FileNotFoundError as exc:
        ap.exit(1, f"Missing tool: {exc.filename}. Install yt-dlp and ffmpeg (includes ffprobe).\n")
    except subprocess.CalledProcessError as exc:
        ap.exit(1, f"Source probe failed: {(exc.stderr or str(exc)).strip()}\n")
    ok = [x for x in items if x["duration"]]
    skipped = [x for x in items if not x["duration"]]
    print(f"SOURCE: {title}\nITEMS: {len(ok)} usable, {len(skipped)} with unknown duration (review before ingest)")
    for x in ok:
        m = int(x["duration"] // 60)
        print(f"  {x['idx']:3d}. [{m:3d}m] {x['id']}  {x['title']}")
    for x in skipped:
        print(f"  ---. [ ? ] {x['id']}  {x['title']}  (duration unknown)")
    tot_h = sum(x["duration"] for x in ok) / 3600
    print(f"\nTOTAL: {tot_h:.1f} h of known-duration video")
    if skipped:
        print("Estimates exclude unknown durations; check those items before planning the full run.")
    print(f"ESTIMATES: download ~{tot_h*3:.0f}–{tot_h*5:.0f} min · "
          f"transcribe ~{tot_h*60/12:.0f} min (mlx-whisper ≈12× realtime, serial) · "
          f"disk ~{tot_h*0.7:.1f} GB")
    if a.output:
        out = a.output
        out.write_text(json.dumps({"source": title, "items": items}, indent=2))
        print(f"worklist → {out}")

if __name__ == "__main__":
    main()
