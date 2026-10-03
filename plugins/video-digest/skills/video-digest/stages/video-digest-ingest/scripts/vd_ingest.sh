#!/bin/bash
# Ingest ONE item: acquire video + transcribe + 30s timeline. Idempotent.
#   vd_ingest.sh <item_dir> <youtube_url | /path/to/video.ext> [lang]
# lang optional (e.g. en); omit to let Whisper autodetect.
set -euo pipefail
D="${1:?item_dir}"; SRC="${2:?url_or_file}"; LANG_OPT="${3:-}"
mkdir -p "$D/transcript"

# --- acquire and validate ---
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$SCRIPT_DIR/vd_acquire.py" "$D" "$SRC"

# --- transcribe (loop-propagation OFF — critical) ---
if [ -f "$D/transcript/transcript.tsv" ]; then
  echo "== transcript exists, skip"
else
  ffmpeg -y -hide_banner -loglevel error -i "$D/source.mp4" -vn -ac 1 -ar 16000 \
    -c:a pcm_s16le "$D/transcript/audio16k.wav"
  LANG_ARGS=(); [ -n "$LANG_OPT" ] && LANG_ARGS=(--language "$LANG_OPT")
  uvx --from mlx-whisper mlx_whisper "$D/transcript/audio16k.wav" \
    --model mlx-community/whisper-large-v3-turbo \
    --output-dir "$D/transcript" --output-name transcript --output-format all \
    "${LANG_ARGS[@]}" --condition-on-previous-text False --verbose False
  rm -f "$D/transcript/audio16k.wav"
fi

# --- 30s timeline (for segmentation / skimming) ---
awk -F'\t' 'NR>1{ms=$1;b=int(ms/30000)*30;t=$3;gsub(/^ +| +$/,"",t);
  if(b!=p&&NR>2){print L;L=""} h=int(b/3600);m=int((b%3600)/60);s=b%60;
  ts=sprintf("%02d:%02d:%02d",h,m,s); L=(L==""?ts"  "t:L" "t); p=b} END{if(L)print L}' \
  "$D/transcript/transcript.tsv" > "$D/transcript/timeline_30s.txt"
echo "INGESTED: $D"
