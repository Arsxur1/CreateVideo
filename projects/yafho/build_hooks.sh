#!/usr/bin/env bash
# Yafho-Silicare — render the A/B hook variants (hooks/*.json) in 9:16 and 4:5 for ad tests (AB_TESTS.md).
#   bash projects/yafho/build_hooks.sh            # all variants
#   bash projects/yafho/build_hooks.sh 14 16      # chosen topics
# Output: output/yafho/hooks/topic_NN_hook{B,C}_<fmt>.mp4 (variant A = output/yafho/topics/topic_NN_<fmt>.mp4)
set -euo pipefail
cd "$(dirname "$0")/../.."
python projects/yafho/make_hooks.py >/dev/null
TOPICS="${*:-04 05 14 15 16 17}"
for n in $TOPICS; do
  for v in B C; do
    f="projects/yafho/hooks/topic_${n}_hook${v}.json"
    echo "== ${n}${v} · $(date +%H:%M:%S)"
    python projects/yafho/build_v2.py --data "$f" --final --formats 9x16,4x5
  done
done
echo "== hooks done $(date +%H:%M:%S)"
