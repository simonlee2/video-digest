# Video Digest 0.3.0-rc.3 — local review candidate

Draft-PR candidate; not tagged, released or installed globally. This is one self-contained Agent Skill, packaged directly and in thin Claude/Codex plugin wrappers. No hosted app is required.

## Applied reference lessons

- One entrypoint and selected-folder install unit: `skills/video-digest/` includes scripts, internal stage guides, quality references, license and original demo content. There are no required repository siblings or files named `metadata.json`.
- Progressive disclosure: users install and name one skill; the agent opens only the stage guide needed. Stage internals use `STAGE.md` and are not extra discoverable skills.
- Portable `name`/`description` frontmatter. No vendor model name, mandatory slash command, subagent API, or invocation metadata in the core.
- Doctor → offline demo → one real source. No global/all-skills installer default. No untested npx command advertised.
- Shared evidence/quality policy, real playable-media validation, accurate frame timestamps, complete editorial rendering, correct numbering and graceful failed images.

[COMPATIBILITY.md](COMPATIBILITY.md) links the official specification, host conventions and reference repositories that informed these choices. No external skill text/assets were copied.

## Reproduce

From the source checkout with Python and Pillow:

```bash
python3 scripts/check_install.py ../video-digest-try --host codex
python3 -m unittest discover -s tests -v
python3 scripts/package_release.py ../video-digest-release-review
```

Use `--host claude` or `--host generic` with a fresh output directory for those layouts. The check copies **only the single install unit** and runs its bundled demo through its bundled renderer. All relative documentation references stay inside that unit. Tests include paths with spaces and refuse overwrite.

## Actual verification

- 24 tests pass, including isolated Codex, Claude and generic layouts, both HTML formats, all approved highlights, image-loss paths, numbering, exact frame links, relative reference containment and doctor output.
- The neutral entry skill passes the local Codex skill-creator validator. Claude Code 2.1.280 validates the project-local skill components and plugin manifest.
- Fresh Codex 0.156.1 `debug prompt-input` discovers the final installed entrypoint; internal stages do not appear in its skill catalog. This local diagnostic sent no prompt to an external model.
- A live Claude model session was not started. Its available validator verifies files, not live discovery. No equivalent documented no-model prompt-discovery diagnostic was found; an interactive host check is still needed before claiming that coverage.
- Cursor and VS Code installation paths are supported by their official documentation, but those hosts were not exercised here. Generic compatibility is an expectation, not a completed runtime test.
- Python compilation, shell syntax and diff checks pass. No global install, new account or paid API was used for these deterministic checks. Subsequent explicitly authorized subscription pilots are reported separately in the PR.
- Previous eleven-talk real-media processing and desktop/mobile digest QA remain supporting workflow evidence. The deterministic clean-install test uses synthetic material. Separately authorized Codex subscription evaluations use the full existing Dan Shipper source and cached transcript; see [EVALUATION.md](EVALUATION.md).
- Structured editorial remains in its source language when the existing bilingual view changes; full editorial translation is not claimed.

## Release gates

1. Review the bounded Codex real-source evidence in [EVALUATION.md](EVALUATION.md). Decide whether to proceed with a Codex-first release or wait for safe authorized Claude capacity; do not claim Claude inference coverage from file validation. Browser visual QA of the latest output remains unverified.
2. Review the draft PR before merging or tagging a release. The candidate branch and default branch are distinct installation targets.
3. Approve public demo content. The included original fictional demo is suitable for a labeled layout/workflow preview. The private conference digest needs a separate rights/publication decision before public use.
4. Approve the post and final links after the release exists. No post has been sent.

Recommended first documented/tested path: Codex project-local install. Claude and common harnesses remain supported design targets with explicit coverage boundaries, rather than a claim that every host has been tested.

## Proposed social draft — not posted

I built Video Digest as a skill for coding agents: give it a talk or playlist, and it helps turn recordings into a browsable digest with timestamped highlights, real video frames, and takeaways grounded in what the speakers said.

It’s one portable skill, with packaging for Claude Code and Codex. Media processing runs on your machine; editorial work uses your agent’s model. The result is ordinary HTML you can review before sharing.

I’m starting with the skill rather than a hosted app. Early version; the bundled transcription setup targets Apple Silicon Macs. [Add approved release and demo links.]

Demo plan: show the original fictional card, open its notes, and distinguish the short visual caption from the substantive explanation. Label it “Fictional reference — layout/workflow preview.” It is not evidence of transcription accuracy. A later approved real-video demo can show timestamp links back to its source.

## Latest local repository polish

README now focuses on product/install/use; DEVELOPMENT.md owns engineering checks and packaging. The entrypoint links to a separate configuration reference. Removed unsupported transcript-accuracy percentages. Install preflight reports missing Pillow before creating output. Generated media, environments and local outputs are ignored. The repository/PR is authoritative; prior RC3 ZIPs are historical snapshots.
