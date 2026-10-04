# TL;DR + practical takeaway → sessions/<name>.take.json   (fan out ~5 talks/agent, use an available capable model)

INPUT: {ITEM_DIR}/sessions/<name>.md (summary + highlights).

For each WRITE {ITEM_DIR}/sessions/<name>.take.json = {"tldr": "...", "takeaway": "..."}:
- tldr: 1–2 punchy sentences capturing the core thesis. No fluff, no "in this talk".
- takeaway: a concise decision or practice for {AUDIENCE}, usually 1–3 sentences —
  a concrete decision, practice, tool, or mental model. Specific to the content, not generic.
Read `../../../references/editorial-contract.md`. Distinguish speaker recommendations from your own application, labeling the latter in the takeaway. Tie advice to the talk’s evidence and constraints. Prefer one useful next decision with its conditions over a checklist of every highlight. Do not repeat this same application under multiple frames. Ground strictly in the summary; don't invent. Return a one-line-per-talk confirmation.
