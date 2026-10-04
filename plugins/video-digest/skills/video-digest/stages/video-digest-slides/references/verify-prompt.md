# VERIFY each chosen frame matches its highlight (vision) → overwrite frames/sel_<name>.json
# (fan out ~5 talks/agent; independently check the selection)

INPUTS: current picks {ITEM_DIR}/frames/sel_<name>.json; text in {ITEM_DIR}/highlights.json.
Candidate files: {ITEM_DIR}/frames/<name>/h<II>_<j>.jpg (II = 2-digit highlight index, j = 0/1/2).

For EACH highlight with a non-null pick: Read that chosen frame full-res. Does the slide clearly
support the highlight text (same topic / the stat/chart/diagram/title it refers to)?
- YES → keep. NO (speaker, unrelated/generic title, another talk's slide) → Read the other 2
  candidates and pick the best match; if none matches → null.
For null picks: read candidate offsets from `frame_seconds` rather than assuming j=1 is exact. For a core concept without an image, inspect its supporting passage beyond the initial samples if selection has not already done so. Keep null when no useful matching image exists; never add an image just to fill a gap.
Be strict: keep only if a viewer would agree the slide goes with the point. When torn, prefer null.

Verify the selected filename and actual frame offset together, including any replacement candidates. Recheck that early, middle and concluding concepts with useful visuals have not been missed by the initial sampling. Inspect readable source resolution when a chart's small text matters. A visually correct frame still needs substantive editorial; caption text alone is insufficient.

Overwrite {ITEM_DIR}/frames/sel_<name>.json (every highlight index present). Return a concise
changelog of CHANGED highlights + reason, and kept/changed/nulled counts.
