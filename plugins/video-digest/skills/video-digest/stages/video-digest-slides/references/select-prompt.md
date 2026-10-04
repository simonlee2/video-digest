# SELECT the slide frame per highlight (vision) → frames/sel_<name>.json
# (fan out ~5 talks/agent; use an available vision-capable model)

INPUTS: montages {ITEM_DIR}/montages/<name>_pN.jpg (page names in montages/index.json);
highlight text in {ITEM_DIR}/highlights.json. Each montage row is one highlight. Labels identify
array index j and actual extraction time. Initial candidates usually use −5s/exact/+5s;
failed extractions may compress the array, so read `files` and `frame_seconds`, not an assumed index-to-offset mapping.

For EACH highlight i, choose the candidate j (0/1/2) whose image is a CLEAN, readable slide
belonging to THIS talk (text/bullets/chart/diagram/code/title). Choose **null** if none is a
usable slide (speaker/host/audience/wide stage, sponsor-logo wall, black/transition frame, or
clearly a DIFFERENT talk's slide). Tie-breakers: best match to the highlight text; most readable;
prefer the candidate closest to the highlight time when equal. Firesides/demo-only talks: null is expected.

These initial candidates are a starting point, not the search boundary. Review the argument's major concepts and important unillustrated passages. If nearby samples only show the speaker, inspect suitable moments elsewhere in the supporting passage before giving up on a useful diagram or demo. Choose times from the transcript and video, not evenly spaced decoration. A matching frame may precede or follow the highlight. Keep `sec` unchanged and update the candidate filename and corresponding `frame_seconds` to the actual extraction time. You may replace a candidate slot with this new image, then regenerate the montage; preserve approved editorial fields. Never label a later frame with the highlight time.

Prefer images that explain a mechanism, evidence or workflow over generic title slides. Review coverage across the argument; a long image gap is a reason to inspect, not a requirement to add an image. If no useful slide exists, retain the substantive text-only point and record that decision.

Read each montage with the available image-inspection tool. WRITE {ITEM_DIR}/frames/sel_<name>.json =
{"0": j-or-null, "1": ...} including EVERY highlight index. Return one line per talk (e.g. "7/9 slides").
