#!/usr/bin/env bash
# Yafho-Silicare — rebuild EVERYTHING after new inputs (site backdrop, logo, pack sizes, Kling clips).
#
#   bash projects/yafho/build_all.sh            # all videos in 9x16,16x9,4x5,1x1 + every derived file
#   bash projects/yafho/build_all.sh --quick    # 9:16 only (check before the long run)
#
# Order: assets → topics → hero v4 → cuts / stories / carousels → long guide →
# subtitles / thumbnails → portfolio page → inventory → rule check.
# Full run ≈ 8–10 h on 4 CPU (3D scenes ≈ 50 s CPU per second of video); --quick ≈ 2 h.
#
# Headless sandbox (see README «Закрытые сети»): set REMOTION_BROWSER_EXECUTABLE,
# REMOTION_GL=angle, REMOTION_OFFLINE_GOOGLE_FONTS=1 and REMOTION_TIMEOUT_MS=180000 first.
set -euo pipefail
cd "$(dirname "$0")/../.."
Y=projects/yafho
FORMATS="9x16,16x9,4x5,1x1"
[ "${1:-}" = "--quick" ] && FORMATS="9x16"
export REMOTION_GL="${REMOTION_GL:-angle}"
export REMOTION_TIMEOUT_MS="${REMOTION_TIMEOUT_MS:-180000}"
step() { echo; echo "=== $* · $(date +%H:%M:%S)"; }

step "assets: backdrop, skin textures, music"
python $Y/make_backdrop.py
python $Y/make_skin.py
python $Y/topics/series2.py
for f in $Y/hero_v4.json $Y/topics/topic_*.json; do python $Y/make_music.py --data "$f"; done

step "rules check before rendering"
python $Y/check_rules.py --strict

step "topics 01–17 · $FORMATS"
bash $Y/build_topics.sh "$FORMATS" 04 02 05 03 06 07 08 01 09 10 11 12 13 14 15 16 17

step "hero v4 · $FORMATS"
for fmt in ${FORMATS//,/ }; do
  python $Y/build_v2.py --data $Y/hero_v4.json --final --formats "$fmt"
done
python $Y/build_v2.py --data $Y/hero_v4.json --cards --formats "$FORMATS"
python $Y/make_cuts.py --data $Y/hero_v4.json --formats "$FORMATS"

step "stories, carousels"
for f in $Y/topics/topic_*.json; do
  grep -q '"cuts"' "$f" && python $Y/make_cuts.py --data "$f" --formats 9x16
done
[[ "$FORMATS" == *4x5* ]] && python $Y/make_carousel.py

if [[ "$FORMATS" == *16x9* ]]; then
  step "long guide 16:9, thumbnails"
  python $Y/make_longform.py
  python $Y/make_thumbs.py
fi

step "subtitles, portfolio page, inventory, final check"
python $Y/make_srt.py
python $Y/make_portfolio.py
python $Y/make_index.py
python $Y/check_rules.py
step "done"
