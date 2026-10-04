# Preview a digest without processing a video

This original fictional example exercises the real site builder: one talk, six chronological highlights, substantive editorial notes, a labeled application, and two slides. It uses no conference assets, downloads, model calls, or credentials. It includes an original fictional source script and demonstrates the editorial standard: claim, explanation, evidence, limitation, and next decision. It does not test transcription. There is no source video, so YouTube links are intentionally absent.

Run from the repository root. If your existing `python3` can import Pillow (`python3 -c "import PIL"`), replace `uv run --with pillow python` below with `python3`; no new installation or network access is needed. Otherwise, [uv](https://docs.astral.sh/uv/) can supply Pillow with the commands below; its initial run downloads dependencies.

```bash
uv run --with pillow python examples/create_demo.py /tmp/video-digest-demo
uv run --with pillow python plugins/video-digest/skills/video-digest/stages/video-digest-site/scripts/vd_site.py /tmp/video-digest-demo --dist /tmp/video-digest-demo/dist
python3 -m http.server --bind 127.0.0.1 --directory /tmp/video-digest-demo/dist 8000
```

Open http://localhost:8000. Click the talk card, inspect all six highlights and their notes, including the final decision record, and return to the overview. Stop the server with Ctrl-C. Choose a different output path if the demo directory already exists; the generator refuses to overwrite it.

For a single file you can send for review:

```bash
uv run --with pillow python plugins/video-digest/skills/video-digest/stages/video-digest-site/scripts/vd_site.py /tmp/video-digest-demo
```

The result is `/tmp/video-digest-demo/digest.html`. For public hosting, upload the contents of `dist/` to a static host after choosing the destination. Keep the synthetic-content label visible. Never upload the entire working project, which may contain source videos and transcripts.

Review the [editorial contract and quality checklist](../plugins/video-digest/skills/video-digest/references/editorial-contract.md). Compare visual captions with substantive notes and verify that later text-only points remain visible.

To check the local scripts:

```bash
uv run --with pillow python -m unittest discover -s tests -v
```

For reproducible rendering QA, run the test command above before reviewing the generated HTML. Tests build both formats, verify all six highlights and their editorial notes survive image limits, and check selected-frame source links independently from highlight links. Browser review is still required for layout and navigation; tests do not claim visual coverage.
