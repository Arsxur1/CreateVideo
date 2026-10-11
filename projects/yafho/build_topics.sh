#!/usr/bin/env bash
# Yafho-Silicare — build the topic series (TZ §3) one after another.
#
#   bash projects/yafho/build_topics.sh                    # all topics, 9x16
#   bash projects/yafho/build_topics.sh 9x16,16x9,4x5      # all formats
#   bash projects/yafho/build_topics.sh 9x16 04 02         # chosen topics
#
# Order follows TZ §4: 04 → 02 → 05, then 03 → 06 → 07 → 08 → 01 → 09; then series 2 (10–17) and 3 (18–21).
# Output: output/yafho/topics/topic_<NN>_<fmt>.mp4 (+ _sheet.png contact sheet, _cover.png post picture).
set -euo pipefail
cd "$(dirname "$0")/../.."
FORMATS="${1:-9x16}"  # 9x16 · 16x9 · 4x5 · 1x1 (Telegram)
shift || true
TOPICS="${*:-04 02 05 03 06 07 08 01 09 10 11 12 13 14 15 16 17 18 19 20 21}"
for n in $TOPICS; do
  data="projects/yafho/topics/topic_${n}.json"
  [ -f "projects/yafho/assets/music/yafho_topic_${n}.wav" ] || python projects/yafho/make_music.py --data "$data"
  echo "== topic ${n} · ${FORMATS} · $(date +%H:%M:%S)"
  python projects/yafho/build_v2.py --data "$data" --final --formats "$FORMATS"
done
echo "== done $(date +%H:%M:%S)"
