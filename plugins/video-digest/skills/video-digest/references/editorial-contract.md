# Editorial output contract

Use this contract when writing highlights, pairing frames, or handing content to a site adapter.
`highlights.json` is the canonical renderer input. Preserve every approved highlight in chronological order, including text-only points and later conclusions. Image budgets limit images; they never limit text or editorial notes.

## Ground each point

Read the full talk and the passage around the timestamp. Write the speaker's specific claim, the mechanism or reasoning, and a concrete example or evidence when the source supplies one. Explain the supported implication without turning an anecdote into general proof. Use two or three concise notes when useful; substance determines length. A slide title or description alone is not analysis.

Check selected frames at full resolution. Verify uncertain names, numbers and quotations against the frame or recording; omit or qualify anything unresolved. A frame may illustrate a wider passage, so retain both its exact extraction time and the passage's evidence range. Identify panel/speaker images as representative. Keep predictions, reported internal results and demonstrated behavior distinct. Label your own proposed applications as editorial interpretation.

## Edit for information gained

Give each highlight one distinct job in the argument. The heading names it, `text` states the claim, and notes add reasoning, evidence or a necessary caveat. Do not restate the claim in two notes merely to fill a template. One useful note can be enough; retain more when the source needs them. An editorial application is optional, not a required ending for every block. Prefer one concrete overall takeaway to repeating the same recommendation under several frames.

Before approval, perform an explicit compression pass over the complete draft. Organize by distinct reasoning or decisions, not every transcript transition. Adjacent setup, adoption and results from one example usually belong in one or two blocks; keep them separate only when each earns its own reusable lesson. Merge genuinely duplicate points, or let each retain its different mechanism/example. Keep later conclusions and important limitations; brevity must not become truncation. Once approved, the renderer preserves every point. Do not shorten text by slicing the input array.

Keep caveats about a particular result beside that result. Put general transcription or verification limitations in one source note/footer rather than repeatedly announcing omitted material in highlight notes. Review the overall takeaway too: one decision and the evidence needed to make it is usually enough. Save a short `editorial-review.md` in the output item naming the points combined/shortened and why any apparently similar points remain. This records the editing judgment, not just the audit’s counts.

Review the visual coverage of the argument, not just individual candidates. A close-up at a highlight timestamp does not mean the passage has no useful slide. For an important unillustrated concept, inspect other moments in its supporting passage and select a relevant diagram, workflow or demonstration if present. Preserve the highlight time and record the new frame's actual offset separately. Do not fill time intervals with irrelevant images or force slides into a discussion-only talk.

Run `python3 scripts/audit_editorial.py <item_dir>` from this skill directory before delivery. It reports word counts, exact repeated blocks, missing evidence ranges, selected-frame gaps and unillustrated starred highlights. These are review prompts, not an automatic quality score or word/image quota. Compare the report with a prior version when evaluating a change, then review semantic repetition, coverage and source fidelity yourself.

## Fields on each highlight

```json
{
  "i": 3,
  "ts": "00:03:00",
  "sec": 180,
  "text": "The fictional follow-up supports testing the wording, not claiming a sales increase.",
  "files": ["h03_0.jpg"],
  "frame_seconds": [180],
  "caption": "Fictional slide with the heading Close the loop.",
  "image_alt": "Fictional slide: Close the loop",
  "editorial_heading": "Separate comprehension from conversion",
  "editorial_notes": [
    "Five of six fictional participants understand the revision. The comparison concerns comprehension in these sessions, not population-wide conversion.",
    "The next step is a limited rollout tracking completion and support contacts together, so clearer copy does not conceal unrealistic delivery expectations."
  ],
  "editorial_inference": "Use separate measures for understanding and downstream behavior.",
  "evidence_start_seconds": 180,
  "evidence_end_seconds": 230
}
```

- `text`: approved transcript-grounded highlight, preserved even with structured notes.
- `caption` / `image_alt`: visual metadata; never substitute these for editorial content.
- `editorial_heading` / `editorial_notes`: substantive analysis, rendered explicitly in full. Required for newly authored or revised frame highlights. Legacy text-only inputs remain supported.
- `editorial_inference`: optional application in the editor's voice; renderer labels it **Editorial application**.
- `evidence_start_seconds` / `evidence_end_seconds`: source-video offsets for the supporting passage, not fabricated precision for each sentence.
- The image source link uses the selected candidate’s actual `frame_seconds` value; the highlight link retains `sec`. Legacy records without candidate times receive no guessed frame link.
- `files` and `frame_seconds`: parallel arrays of candidate filenames and actual extraction offsets. `sel_<stem>.json` selects an array index. Keep the existing highlight `i`, `sec` and source provenance stable during editorial revisions.

For a separate frame-manifest handoff, use `video_id` + `seconds` (actual selected-frame offset) as deterministic keys; copy the editorial fields above alongside `caption`, `image_alt`, `source_url`, relative `file`, and extraction provenance. Keep the complete talk highlights separately. Adapters must render all `editorial_notes`, label `editorial_inference`, and preserve later highlights rather than taking a fixed leading slice. The repository renderer reads `highlights.json`; a frame manifest is an adapter contract, not a replacement input.

The current renderer displays structured editorial in its source language in either language view. Translate existing `zh.json.hl` highlights normally; disclose this editorial fallback for bilingual output rather than claiming full translation.

## Quality checklist before delivery

- Every included talk is grounded in its full transcript; inaccessible material is identified.
- Every frame has a relevant claim and explanation, with specific evidence/example when available. Adjacent points advance the argument rather than repeat it.
- Notes add information beyond their heading and highlight; optional applications do not repeat the overall takeaway. Important unillustrated passages were checked for useful frames beyond the initial candidates.
- Every selected image has been inspected; exact frame links and evidence windows are correct.
- Speaker claims, uncertainty and editorial applications are distinguishable.
- Every approved highlight and editorial note appears in the rendered detail view, including the final point. Check image-budget and text-only paths.
- Caption/alt text remains visual metadata. No source transcript, private media or credentials are accidentally included in the deliverable.
- Inspect the overview and a full detail view at desktop and narrow widths using permitted preview tools. If preview access is blocked, report the limitation and structural checks performed.

The bundled `scripts/create_demo.py` generates an original fictional reference with six highlights, two images and a source script. It demonstrates the distinction between observation, inference and a next decision; it is not evidence from a real event.
