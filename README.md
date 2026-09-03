# video-digest

A set of [Claude Code](https://claude.com/claude-code) skills that turn talk videos into a **shareable web digest**: a card grid of every talk, and per-talk pages with a TL;DR, "take this to work" takeaways, timestamped highlights, and the speaker's actual slides paired with what they said — each deep-linking back into YouTube.

Point it at a YouTube playlist, a channel's streams tab, one long multi-talk conference stream, a single video, or a folder of local files. Everything runs locally: `yt-dlp` for download, Whisper for transcription, `ffmpeg` for frames, and Claude for the judgment calls (segmenting talks, summarizing, picking which frame is really a slide).

Built while digesting AI Engineer World's Fair 2026, Cursor Compile 2026, and Figma's conference, then generalized.

## The pipeline

Five composable stage skills plus an orchestrator. Each stage is idempotent per item, so you can re-run one talk — or one stage — without touching the rest.

| Stage | Skill | In → Out |
|---|---|---|
| — | `video-digest` | orchestrator: routes by source shape, owns project config |
| 1. Ingest | `video-digest-ingest` | source (URL / playlist / folder) → `video.mp4`, transcript, 30s timeline per item |
| 2. Segment | `video-digest-segment` | multi-talk streams only: timeline → `talks.json` |
| 3. Summarize | `video-digest-summarize` | transcript slices → summary docs, TL;DR + takeaway JSON, optional 繁中 translation |
| 4. Slides | `video-digest-slides` | highlights → candidate frames → montages → vision-picked slide per highlight |
| 5. Site | `video-digest-site` | everything → `index.html` / `dist/` (+ optional synthesis essay) |

Routing:

- **YouTube playlist / folder of videos** → each video is its own item; skip segment.
- **Long multi-talk stream** → one item, then segment it into talks.
- **Single talk** → one item, skip segment.

## Requirements

- **Apple Silicon Mac** — transcription runs [`mlx-whisper`](https://github.com/ml-explore/mlx-examples/tree/main/whisper) (`large-v3-turbo`, ~10–15× realtime). On other platforms, swap the one `uvx --from mlx-whisper` line in `video-digest-ingest/scripts/vd_ingest.sh` for `whisper`/`faster-whisper`; no other stage cares.
- `yt-dlp` and `ffmpeg` / `ffprobe` — `brew install yt-dlp ffmpeg`
- [`uv`](https://docs.astral.sh/uv/) — pulls Whisper and Pillow on demand (`uvx`, `uv run --with pillow`), so there's nothing to pip-install
- `python3`

Budget roughly 2–5 min download and ~0.5–1 GB disk per hour of video.

## Install

Copy the skill directories into your Claude Code skills folder:

```bash
git clone https://github.com/simonlee2/video-digest.git
cp -R video-digest/video-digest* ~/.claude/skills/
```

Or symlink them, so a `git pull` updates the installed skills:

```bash
git clone https://github.com/simonlee2/video-digest.git ~/Developer/video-digest
for d in ~/Developer/video-digest/video-digest*; do ln -s "$d" ~/.claude/skills/; done
```

## Use

In Claude Code, just describe the source:

```
make a digest from https://www.youtube.com/playlist?list=...
```

Claude picks up the `video-digest` skill, probes the source (count and duration first), runs **one talk end-to-end as a pilot** so you can fix the config before fanning out, then batches the rest.

A project looks like this:

```
<project>/
├── digest.json                  # config: title, brand, audience, languages, slide_cap, glossary…
├── groups/<group>/              # a group = a tab/section (a day, a track, or the whole event)
│   └── <NN-item>/               # an item = ONE source video
│       ├── source.json          # title, speaker, YouTube url (→ deep links in the digest)
│       ├── transcript/ sessions/ frames/ montages/
│       └── talks.json highlights.json
├── narrative.json               # optional cross-talk synthesis essay
└── dist/                        # the published site
```

`digest.json` is where you steer the output: `audience` shapes the takeaways ("what should a platform engineer do because of this talk"), `languages: ["en","zh"]` turns on a Traditional Chinese toggle, `glossary` fixes recurring Whisper mishearings of product and speaker names, `slide_cap` bounds how many slides each talk embeds.

## Output

Two modes from the same content:

- **`dist/` folder** — 900px slides as separate files, effectively uncapped; publish to any static host.
- **Single self-contained HTML file** — slides inlined as data URIs, capped around 8 MB; good for pasting into an artifact or emailing.

## Cost note

The orchestrator delegates per stage: cheap models for the mechanical per-talk text and vision matching, the strongest model only for talk segmentation and the synthesis essay. The model tier table lives in `video-digest/SKILL.md`.

## License

MIT
