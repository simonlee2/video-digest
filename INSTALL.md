# Install video-digest

Six skills in one plugin. Installs on Claude Code and Codex from the same repo; works by plain copy on any other harness that reads agent skills.

## Claude Code

```bash
claude plugin marketplace add simonlee2/video-digest
claude plugin install video-digest@video-digest
```

Then start a new session and say *"make a digest from <playlist url>"*, or invoke `/video-digest`.

Verify:

```bash
claude plugin list
claude plugin details video-digest    # should list all six skills
```

Update / uninstall:

```bash
claude plugin marketplace update video-digest
claude plugin uninstall video-digest
claude plugin marketplace remove video-digest
```

Keep it installed but idle: `claude plugin disable video-digest`.

## Codex

```bash
codex plugin marketplace add simonlee2/video-digest --ref main
codex plugin add video-digest@video-digest
```

Verify:

```bash
codex plugin list
```

Update / uninstall:

```bash
codex plugin marketplace upgrade video-digest
codex plugin remove video-digest
codex plugin marketplace remove video-digest
```

## Any other agent-skills harness

The skills are plain directories with a `SKILL.md`, `scripts/`, and `references/` — nothing harness-specific inside them.

```bash
git clone https://github.com/simonlee2/video-digest.git
cp -R video-digest/plugins/video-digest/skills/* <wherever your agent scans>
# ~/.claude/skills/ · ~/.codex/skills/ · ~/.cursor/skills/ · .agents/skills/ · ~/.config/opencode/skills/
```

Or symlink, so `git pull` updates the installed skills:

```bash
git clone https://github.com/simonlee2/video-digest.git ~/Developer/video-digest
for d in ~/Developer/video-digest/plugins/video-digest/skills/*; do ln -s "$d" ~/.claude/skills/; done
```

Start a new session afterward — skills are indexed at session start.

## After installing

Install the runtime tools too, or the ingest stage fails on first use:

```bash
brew install yt-dlp ffmpeg
brew install uv          # pulls Whisper and Pillow on demand
```

Transcription assumes an Apple Silicon Mac (`mlx-whisper`). On other platforms, swap the one `uvx --from mlx-whisper` line in `plugins/video-digest/skills/video-digest-ingest/scripts/vd_ingest.sh` for `whisper` or `faster-whisper`.

## Troubleshooting

**Skills don't show up.** Restart the agent — the plugin index is read at session start.

**`marketplace add` fails.** Use the `owner/repo` form, or point a local path at the repo root (not `.claude-plugin/`).

**Duplicate skills.** If you previously copied `video-digest*` into `~/.claude/skills/` by hand, remove those copies — otherwise the loose copy and the plugin's copy both match the same requests.

**`python3 scripts/vd_*.py` not found.** Those paths are relative to the skill's own directory; run from there or prefix the skill dir.
