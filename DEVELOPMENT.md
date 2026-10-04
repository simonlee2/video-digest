# Development and verification

The public install unit is `plugins/video-digest/skills/video-digest/`. Keep everything required at runtime inside that directory. `SKILL.md` is the only discoverable entrypoint; `stages/*/STAGE.md` supplies progressive guidance. Portable, Claude and Codex manifests wrap the same content.

## Local checks

With existing Python and Pillow, from the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_install.py ../video-digest-check --host codex
python3 scripts/check_install.py ../video-digest-claude-check --host claude
python3 scripts/check_install.py ../video-digest-generic-check --host generic
```

Use fresh destinations. These checks copy only the install unit and run the copied scripts; they do not install globally or invoke a model. Missing Pillow is reported before a destination is created. Node enables the image-error JavaScript execution test; its absence causes that test to be explicitly skipped.

Regression coverage includes the selected-folder boundary, paths containing spaces, internal reference containment, complete editorial notes, image budgets/failures, source timestamps and group-wide talk numbering. Review a full talk in a permitted browser at desktop and narrow widths; structural tests do not establish visual quality. The fictional example proves deterministic setup and rendering, not real-video analysis quality.

## Editorial evaluation

Use `python3 plugins/video-digest/skills/video-digest/scripts/audit_editorial.py <item_dir>` on each compared output. It counts all editorial, including text-only and final points, identifies exact repeated blocks, and reports actual selected-frame offsets, gaps, missing evidence windows and unillustrated starred points. It does not score prose, infer semantic duplication, require evenly spaced images or prove source fidelity.

For a bounded model evaluation, reuse authorized media and a full transcript in a fresh project with only the current skill. Keep prior summaries hidden from the generation run. Compare both outputs against source passages and frames, not against a desired word-count reduction. Record coverage lost or gained, specific repeated ideas, whether notes add mechanisms/examples, and useful visuals missed by initial timestamp sampling. Preserve every approved point in the actual renderer. Report model/runtime, prompt conditions, transcript reuse, browser limits and any processing charges honestly. Do not commit recordings or full transcripts as fixtures; regression fixtures must be original or fictional.

## Packaging review

```bash
python3 scripts/package_release.py ../video-digest-release-review
```

The helper creates source, standalone-skill, Claude-plugin and Codex-plugin ZIPs with checksums outside the checkout. It refuses an existing destination. Versions must match across all three manifests. Package generation does not authorize commits, publication, model calls, or changes to sharing.

Before proposing a release, inspect tracked changes and untracked files. Keep recordings, transcripts, local paths, credentials and generated output out of source/package inputs. Preserve the original demo's synthetic label and the MIT license. Record actual host coverage in `COMPATIBILITY.md`; do not turn format validation into a claim of live runtime verification.

`INSTALL.md` is the user workflow; `RELEASE_CANDIDATE.md` records the current proposal and open gates. Keep engineering logs and machine-specific evidence outside the install unit.
