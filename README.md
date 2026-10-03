# Video Digest

Turn a talk or playlist into a browsable HTML digest: timestamped highlights, genuine video frames, and takeaways grounded in what the speakers said.

**One self-contained skill.** Use it with Claude Code, Codex, or an Agent Skills-compatible harness with file, shell and image tools. No hosted app or plugin account is required. Current review candidate: **0.3.0-rc.3**, not yet released.

## Try it without a video

From this checkout, using existing Python and Pillow:

```bash
python3 scripts/check_install.py ../video-digest-try --host codex
```

Use `--host claude` for `.claude/skills`, or `--host generic` for a neutral `.agents/skills` project. The command refuses existing destinations, installs only the self-contained `video-digest` folder, and builds the fictional demo with the copied scripts.

Open `../video-digest-try/demo/digest.html`. The labeled fictional example demonstrates layout and editorial structure, not real-video transcription quality.

## Use it on a recording

Start your agent in the new project and ask:

> Use video-digest to make a private English digest of /absolute/path/to/my-talk.mp4 for a product builder. Process one talk as a pilot. Use real frames and transcript-grounded takeaways. Save the HTML for review; do not publish.

A YouTube URL or playlist works too, subject to source access. The agent checks tools, acquires and validates playable media, transcribes, selects real frames, grounds the analysis in the transcript, and builds HTML. It can work sequentially; subagents are optional.

[Install and first-run guide](INSTALL.md) · [Host coverage](COMPATIBILITY.md) · [Release review](RELEASE_CANDIDATE.md)

## What runs where

Media acquisition, transcription and rendering run on your machine. The bundled transcription path uses `mlx-whisper` on Apple Silicon Macs; other platforms need a transcript adapter. Your agent's text/vision model performs the editorial work and may send transcripts/frames to a provider or incur usage charges. This is not a claim of fully on-device inference.

Runtime: Python, Pillow, ffmpeg/ffprobe; yt-dlp for remote sources; uv/uvx for the bundled transcription command. The first model/package download needs network access. Run the bundled doctor before installing anything.

## Output and sharing

You get `digest.html`, or `dist/index.html` plus image assets. Every approved highlight remains visible even when image budgets remove a frame. Image captions describe the image; separate editorial notes explain claims, mechanisms and examples, with labeled applications. Frames link to their actual source timestamps.

Review the result before sharing. Choose a destination and audience explicitly, and use material you have permission to process and publish. Keep source recordings and full transcripts out of the published folder.

## Contributing

See [DEVELOPMENT.md](DEVELOPMENT.md) for repository structure, local tests, packaging and release review. The [editorial contract](plugins/video-digest/skills/video-digest/references/editorial-contract.md) defines the quality bar.

MIT license covers the code and original reference; source-video rights remain with their owners.
