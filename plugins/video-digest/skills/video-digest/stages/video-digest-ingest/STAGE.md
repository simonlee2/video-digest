---
name: video-digest-ingest
description: Acquire videos and transcribe them for a video digest project - probe/enumerate a YouTube playlist, channel streams tab, or local folder; acquire playable media with yt-dlp; extract audio; transcribe with mlx-whisper; emit a 30s timeline. Stage 1 of the video-digest pipeline. Use when ingesting videos for a digest, or when asked to download+transcribe talk videos.
---

# video-digest-ingest

Deterministic stage 1. See `video-digest` (umbrella) for the project layout.

## Scripts (in `scripts/`, all take explicit paths — no env vars)
> Script paths below are relative to **this skill's own directory** (`.../skills/video-digest-*/`). Run them from there, or prefix the skill dir — the `<project>` / `<item_dir>` arguments are separate and can be anywhere.


### Probe a source (ALWAYS do this first; supports pilot-first)
```
python3 scripts/vd_probe.py <playlist_or_channel_url | /path/to/folder>
```
Prints a worklist table (id, duration, title) + totals and time/disk estimates. Add `--json out.json` to save the worklist. Unknown durations stay in the worklist and require review; missing duration alone does not establish that an item is live or unavailable.

### Ingest one item (download/link + transcribe + timeline)
```
bash scripts/vd_ingest.sh <item_dir> <youtube_url | /path/to/video.ext> [lang]
```
- Acquires one video with the installed `yt-dlp` defaults, or reuses a local file. `source.mp4` is a compatibility symlink; the underlying container may be WebM or another supported format. Validates video/audio streams, duration, and frame decoding before treating an item as acquired.
- Extracts 16k mono wav → transcribes via `uvx --from mlx-whisper mlx_whisper` (large-v3-turbo) with `--condition-on-previous-text False` (**critical: prevents hallucinated repeat-loops erasing real content**).
- `lang` optional (e.g. `en`); omit to autodetect.
- Idempotent: skips download/transcribe if outputs exist.

### Author metadata for a single-talk item (playlist entry / lone video)
```
python3 scripts/vd_single.py <item_dir> --title "T" --speaker "Name · Org" [--kind talk] [--url <video_url>]
```
Reads real duration via ffprobe → writes 1-talk `talks.json` (00:00:00 → duration), plus `source.json` (label=title, subtitle=speaker, url). Skip this for multi-talk streams — use `video-digest-segment` instead, and write `source.json` by hand.

## Batch workflow (playlist / folder)

1. `vd_probe.py <url>` → worklist. Derive title/speaker per video from its YouTube title (e.g. "Talk Name, Speaker | Event" → split; verify against transcript later).
2. Pilot ONE item end-to-end through all stages before batching.
3. Batch **serially** (concurrent Whisper exhausts RAM):
   for each entry → `vd_ingest.sh groups/<group>/NN-<slug> <url> [lang] < /dev/null` then `vd_single.py ...`.
   `NN-` prefix (01, 02…) = playlist order = digest order.
   **In a `while read` loop you MUST redirect the ingest call's stdin (`< /dev/null`)** — ffmpeg/yt-dlp otherwise eat the loop's input and mangle subsequent lines.
   **TSV worklists read by `bash read`: never leave a field empty** (tab is IFS whitespace, so consecutive tabs collapse and fields shift). Use a placeholder like `-` for unknown speaker and translate it in the consumer.
4. Create `groups/<group>/group.json` `{"key":"<group>","label":"..."}` once.

## Acquisition judgment

Use `yt-dlp` for remote acquisition. Start with the installed version and normal defaults; choose formats, quality, clients, and other flags only when the source, available tools, or output requirements justify them. Full-quality media is acceptable; smaller media may save time and disk if frames remain readable.

For acquisition without transcription, or an explicit optional override:

```bash
python3 scripts/vd_acquire.py <item_dir> <url_or_file>
python3 scripts/vd_acquire.py <item_dir> <url> -- <yt-dlp-options>
```

A successful exit or existing filename is not enough: require playable video/audio, positive duration, and an actual decoded frame. Keep source URL, video ID, duration, and extraction timestamps with outputs. Stop on access restrictions; use authorized local media when provided. Ask before paid services, new installs, login, or security changes when those are not already authorized.

If acquisition fails, inspect the actual binary/version, error stage, and available runtimes. Compare against any user-demonstrated working command. Optional format or extractor overrides are diagnostics, not a mandatory sequence; avoid hard-coding a platform identity or upgrading tools without evidence. Report the concrete blocker rather than silently switching to thumbnails or treating an HTML error page as media.

For frame selection, verify useful visual content at the recorded video timestamp. Preserve source provenance, and distinguish representative speaker/panel views from slides that support a particular highlight.
