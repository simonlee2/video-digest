---
name: video-digest-site
description: Build and publish the digest website from processed video-digest content - overview card grid, per-talk detail pages with slides and takeaways, YouTube deep links, optional EN/Traditional-Chinese toggle and a cited synthesis essay. Stage 5 (final) of the video-digest pipeline. Use when rendering or publishing a video digest site, or refreshing it after new talks.
user-invocable: false
---

# video-digest-site

Input: project dir with `digest.json` + processed `groups/<group>/<item>/` (manifest, highlights, sel_*, take.json; optional zh.json). Needs Pillow.

## Build
> Script paths below are relative to **this skill's own directory** (`.../skills/video-digest-*/`). Run them from there, or prefix the skill dir — the `<project>` / `<item_dir>` arguments are separate and can be anywhere.


```
python3 scripts/vd_site.py <project>                 # single-file digest.html (data-URI images)
python3 scripts/vd_site.py <project> --dist <project>/dist   # folder site (index.html + assets/)
```

- **Single file** (`digest.html`): everything inlined as data URIs. HARD CAP ~8 MB — past ~10 MB most hosts truncate or 403. Size is slide-count-bound; levers: `slide_cap` in digest.json, `IMG_W`/`IMG_Q` in the script. Big events → use dist mode.
- **Dist folder**: `index.html` + `assets/` with crisp 900px slides as separate files. Effectively uncapped on size, but bounded by whatever **file count** the host tolerates — check `ls <project>/dist/assets | wc -l` and lower `slide_cap` if it's near the limit.
- Talks/highlights link to YouTube (`source.json` url) at the right timestamp automatically.

## Publish — whatever this environment offers

**Pick the target BEFORE building**: the target decides the build mode, not the reverse. Do not assume any particular
publishing tool exists — look at what is actually available in this session (skills, MCP tools, installed CLIs) and use it.

1. **Find a target.** Look for, roughly in this order:
   - a **folder/static-site publisher** — a publish/deploy skill or MCP tool, an artifact service that takes multiple
     files, a site-publishing feature of the host app, or a CLI already installed and authed
     (`gh` → Pages, `netlify`, `vercel`, `wrangler`, `surge`, `rsync`/`scp` to a known server);
   - else a **single-file publisher** — an artifact/canvas tool, a paste-an-HTML-page feature, `gh gist`;
   - else **nothing** — that's fine, see step 5.
   If more than one is available, or the user has a habitual one, ask which; don't silently pick.
   Concrete examples, purely as recognition aids — the list is not exhaustive and none of these is required:
   a `here-now`-style publish skill or an equivalent hosting MCP tool (folder), the host app's own artifact or
   canvas tool (usually single-file), a host's "sites"/page-publishing feature, GitHub Pages via `gh`.
2. **Build to fit it.** Folder-capable → `--dist`. Single-file-only → default mode, and confirm the file is under the
   target's size cap before uploading (`du -h <project>/digest.html`).
3. **Verify** (below) before you upload anything.
4. **Publish, then report the URL.** Note the slug/URL/target in the project (e.g. append to `digest.json` or a
   `PUBLISH.md`) so a later refresh re-publishes to the SAME place instead of scattering copies. Publishing is
   outward-facing — get the user's go-ahead the first time, and say plainly where it went.
5. **No publisher available**: leave `dist/` on disk, serve it locally to eyeball
   (`python3 -m http.server -d <project>/dist 8000`), and tell the user exactly what the artifact is — a
   self-contained static folder any host will take — so they can drop it wherever they like.

Known host quirks worth checking against the numbers above: file-count ceilings (here.now fails >1000 files),
single-file size caps (~8 MB for most artifact hosts), and hosts that rewrite or strip inline `<script>`.

## Verify before publishing

Open the built file in a browser (or the agent-browser skill): check a card → detail → slide captions render, hash
routing works (#back button), no horizontal scroll, and (if zh) the toggle.

## Optional: synthesis essay (extra tab)

1. `python3 scripts/vd_corpus.py <project>` → `narrative_corpus.md` + `narrative_cite_index.txt`.
2. STRONG model reads both, writes `<project>/narrative.json`:
   `{title,dek,reading_time,sections:[{kicker,heading,blocks:[{type:"para"|"pull",text}]}],coda}` —
   thesis + 3-5 themed sections + coda; inline `[[sid]]` citations ONLY from the cite index (rendered as numbered superscript links + "Talks cited" list).
3. Optional `narrative.zh.json` (same shape, `[[sid]]` preserved verbatim).
4. Rebuild — the essay tab appears automatically when narrative.json exists. Config: digest.json `essay_tab` (tab/CTA label), `essay: {kicker, byline}`.

## digest.json knobs used here

`title, brand, kicker, headline, lede, footer` (string or `{en,zh}`), `languages` (zh enables toggle), `slide_cap`, `kinds` (pill class/labels), `essay_tab`, `essay`. See the `video-digest` umbrella skill.
