# Install Video Digest

The complete install unit is **`plugins/video-digest/skills/video-digest/`**. Copying just this directory is supported: it contains all scripts, stage guides, references and fictional demo content. No repository siblings or separate stage installs are required.

## 1. Choose your host

From the candidate source checkout:

```bash
python3 scripts/check_install.py ../video-digest-try --host codex
# Alternatively, choose a fresh destination:
python3 scripts/check_install.py ../video-digest-claude-try --host claude
python3 scripts/check_install.py ../video-digest-generic-try --host generic
```

These install locally to the new project's `.agents/skills/video-digest` (Codex/generic) or `.claude/skills/video-digest` (Claude) and build the demo. They refuse overwrite and do not change global configuration. Python and Pillow are required. If Pillow is missing and dependency downloads are acceptable, prefix the command with `uv run --with pillow python` instead of `python3`.

For a manual install into an existing project, copy the single skill directory to the host's documented skill location. Preserve existing customizations. For example, if the destination does not already contain `video-digest`:

```bash
mkdir -p /path/to/project/.agents/skills
cp -R plugins/video-digest/skills/video-digest /path/to/project/.agents/skills/
```

See [COMPATIBILITY.md](COMPATIBILITY.md) for official host paths and actual test coverage. No universal slash command or subagent tool is assumed. Start a fresh session in the destination project and name `video-digest` in your request.

## 2. Check tools

From the installed skill directory:

```bash
python3 scripts/doctor.py
python3 scripts/doctor.py --require media --json
```

Doctor does not install, log in, download or call a model. It reports missing dependencies and returns nonzero when the selected route is not ready. `--require transcription` checks the bundled Apple Silicon/uvx route. Remote URLs also need yt-dlp; existing local files do not.

Runtime dependencies:

- Python 3.9+ and Pillow for the offline demo and HTML.
- ffmpeg/ffprobe for playable-media validation and frame extraction.
- yt-dlp for remote acquisition; use current defaults rather than a prescribed client/format.
- uv/uvx + mlx-whisper for bundled Apple Silicon transcription. First use downloads packages and model weights. Other platforms need an adapter producing `transcript/transcript.tsv` with `start`, `end` in milliseconds, and `text`.
- An agent with text/vision understanding for editorial judgment; it may use an external provider and incur charges.

If desired, install missing macOS tools with `brew install yt-dlp ffmpeg uv`. Check existing tools first; installation is separate from using the skill.

## 3. Open the offline demo

From the installed skill directory, without the original repository:

```bash
python3 scripts/demo.py /path/to/new-demo
```

Open `/path/to/new-demo/digest.html`. Both standalone and folder builds are generated. The original fictional script and images demonstrate the expected layout, explanations and labeled applications. They do not establish real-video transcription or editorial quality.

## 4. Process one source

In your agent:

> Use video-digest to digest /absolute/path/to/my-talk.mp4 for a product builder. Start with one talk, verify the transcript and real frames, and save a private local HTML draft. Do not publish.

Replace the path with an authorized YouTube URL if desired. Verify the opening and closing highlights, the substantive notes and actual frame timestamp links before batching. Source access restrictions are blockers, not permission to bypass them.

## Plugin route and release status

Thin plugin packages for Claude Code and Codex contain this same self-contained skill. The repository also has marketplace manifests. The **0.3.0-rc.3** candidate is on a review branch, not a tagged release. Select that exact branch or commit when reviewing; default-branch commands may fetch the previous version.

Claude's installed CLI validates the plugin; `claude --plugin-dir /path/to/extracted/video-digest` is its documented local loading option. Codex supports marketplace registration/add commands, but this session has not performed a global marketplace install. Recommend the verified project-local route for this candidate. Do not advertise untested `npx skills add` commands or a released version before publication.

## Update, recovery and review

Replace only the installed `video-digest` folder after preserving customizations; avoid loose-copy/plugin duplicates. Old six-skill installs need migration: remove their old stage copies only after backing up any edits, then install the single folder.

A missing image retains editorial text; invalid media stops acquisition. Re-running extraction regenerates `highlights.json`, so preserve approved editorial edits first. Script paths in a stage guide are relative to that guide's directory.

Share only `digest.html` or the final `dist/` folder after a rights/destination decision. Working folders can include full recordings/transcripts. Run `python3 -m unittest discover -s tests -v` from the source checkout for the regression suite; Pillow is required and one JavaScript behavior check uses Node.
