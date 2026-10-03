---
name: video-digest
description: Build a shareable web digest (per-talk TL;DR, takeaways, slides paired with narration) from videos. Sources - a long multi-talk stream (YouTube or file), a YouTube playlist, a single video, or a local folder of videos. Use when asked to "make a digest / recap / summary site" from talks, a conference, a playlist, or recorded videos.
---

# video-digest — orchestrator

Turn videos into a digest site: overview card grid → per-talk detail (TL;DR, "take this to work", slides with substantive highlights), optional bilingual toggle + synthesis essay. Generalized from the AIE WF2026 pipeline.

## First run

Run `python3 scripts/doctor.py` from this skill directory to check available tools without installing anything. For an offline output preview, run `python3 scripts/demo.py /path/to/new-demo`; it uses bundled original fictional material and the real renderer. It does not prove real-video editorial quality.

This directory is the complete install unit. Do not require repository siblings, a fixed agent brand, a subagent tool or a specific model provider. Read only the stage guide needed for the current task:

| Stage | Bundled guide |
| --- | --- |
| Acquire and transcribe | [Ingest](stages/video-digest-ingest/STAGE.md) |
| Split a multi-talk stream | [Segment](stages/video-digest-segment/STAGE.md) |
| Ground summaries in transcript | [Summarize](stages/video-digest-summarize/STAGE.md) |
| Extract, inspect and explain real frames | [Frames](stages/video-digest-slides/STAGE.md) |
| Build and review HTML | [Site](stages/video-digest-site/STAGE.md) |

Scripts named in a stage guide are relative to that guide's directory. Stage guides are internal resources, not separately installed skills.

Routing by source shape:
- **YouTube playlist / folder of videos** → ingest each video as its own item (skip segment). One group per playlist/folder.
- **Long multi-talk stream** → one item, then segment.
- **Single talk video** → one item, skip segment.

Before creating or editing a project, read [project layout and configuration](references/project-config.md). Keep generated media and transcripts in the output project, outside the skill source.

## Workflow

Use [the editorial output contract and quality checklist](references/editorial-contract.md) when authoring or integrating the digest. Visual captions and substantive editorial are separate fields; preserve all approved points.

1. **Scope**: probe the source first (`video-digest-ingest` has probe scripts) — count videos, total duration. Estimate: download time and disk depend on the selected media quality; mlx-whisper large-v3-turbo ≈ 10–15× realtime on Apple Silicon; probe actual media sizes when available.
2. **PILOT FIRST** on batches: run ONE item end-to-end (ingest → summarize → slides → site), inspect the output, fix config (glossary, kinds, prompts), then batch the rest. Never fan out 50 downloads before one full-path validation.
3. Batch: run ingestion within available memory. Process editorial work serially or delegate small batches when the host supports it; delegation is optional.
4. **Essay (default, every digest)**: after all talks are processed, run the site skill's corpus step and write the synthesis essay (`narrative.json`) with the STRONGEST model — plus `narrative.zh.json` if bilingual. On by default; skip only if asked.
5. Site: build locally for review by default. If publishing is requested, choose an available destination and build its supported format; publish only within the user’s authorized destination and audience. Inspect the final output with permitted browser tools and report any QA limitation.
6. Register done items in `<project>/ingested.json` `{"items":{"<videoId>":{"group","item"}}}` so re-runs skip them.

## Model choice and privacy

Use the current agent or available subagents for editorial work; a particular provider or model name is not required. Match capability to the source: full-transcript reasoning and frame verification need adequate text and vision quality. Delegate in small batches when useful and supported. Recheck weak or uncertain output rather than optimizing solely for model cost.

Media acquisition, transcription and rendering can run on the local machine. Editorial inference uses the agent's configured model, which may send transcripts and frames to a provider and incur usage charges. Describe this distinction accurately; local scripts do not imply fully on-device inference.

## Ops notes

- Every stage is idempotent per item — safe to re-run one item without touching others.
- LLM steps write files the next deterministic step reads; you can re-run any LLM step alone and rebuild the site.
- New talks appearing over time (ongoing playlist/channel): re-probe, ingest only unregistered items, rebuild site, republish to the same slug/URL.
