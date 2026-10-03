# Project layout and configuration

```
<project>/
├── digest.json                  # config (below)
├── groups/<group>/              # group = a tab/section (a day, a track, or the whole event)
│   ├── group.json               # {key,label,date?,hours?}  key MUST be kebab [a-z0-9-]
│   └── <item>/                  # item = ONE source video; prefix NN- for order (01-opening-keynote)
│       ├── source.json          # {key,label,subtitle,url?}  url → YouTube deep links in the digest
│       ├── video.* source.mp4   # working media; source.mp4 = compatibility symlink
│       ├── transcript/          # transcript.{tsv,txt,srt...}, timeline_30s.txt, *.clean.txt
│       ├── talks.json manifest.json highlights.json zh.json
│       ├── sessions/ frames/ montages/ clips/
├── dist/                        # local HTML output for review
└── narrative.json narrative.zh.json   # optional essay
```

## digest.json (project config)

All text fields accept a string (EN-only) or `{"en":..., "zh":...}`. Minimal example:

```json
{
  "key": "compile26",
  "title": "Cursor Compile 2026 · Digest",
  "brand": "CURSOR · COMPILE 26",
  "kicker": "Cursor Compile 2026",
  "headline": "The conference, in slides & takeaways.",
  "lede": "Skim the talks, then open any one for the slides, the thesis, and what it means for your work.",
  "footer": "Transcripts are automatically generated and may contain recognition errors.",
  "audience": "an engineer building with AI",
  "whisper_language": "en",
  "languages": ["en"],
  "slide_cap": 8,
  "glossary": [["\\bKursor\\b", "Cursor"]],
  "nonspeech": ["thank you."]
}
```

- `audience` — steers takeaway prompts ("what should X do because of this talk").
- `languages` — add `"zh"` to enable the 繁中 toggle (translate step becomes required).
- `slide_cap` — max embedded slides/talk. Bound by the publish target: single-file builds are size-capped (~8 MB), folder builds are file-count-capped by the host (~1000 is a common ceiling) → cap ≈ (limit − overhead) / talks.
- `glossary`/`nonspeech` — transcript corrections; start empty, fill after reading the pilot transcript.
- Optional `kinds` — extra talk-kind pills: `{"demo": {"class":"fire","en":"Demo","zh":"示範"}}`. Built-ins: main/keynote (green), fireside (purple), track/talk (blue); `cutaway`+`nonspeech` are always excluded from the digest.

