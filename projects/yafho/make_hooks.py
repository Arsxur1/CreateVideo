"""Yafho-Silicare — A/B hook variants for ads: same video, a different first scene (0–4 s).

    python projects/yafho/make_hooks.py          # writes hooks/topic_NN_hook{B,C}.json
    bash projects/yafho/build_hooks.sh           # renders them (9:16 + 4:5)

A = the published topic as is. B and C replace only the opening scene: title
(≤ 6 words, facts from the TZ passport only) and, where noted, the visual.
Everything after the hook — and the music — stays identical, so the ad test
measures the hook alone. Plan and metrics: AB_TESTS.md.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
OUT = PROJECT / "hooks"

SKIN_SHAPE = {"04": "line", "05": "line", "14": "csection", "15": "line", "16": "burn", "17": "stria"}

# topic → {variant: (title, visual)}; visual: None = keep, "effect" = sheet on a dense scar fading, "compare" = two outcomes
HOOKS: dict[str, dict[str, tuple[str, str | None]]] = {
    "04": {"B": ("Пластина не помогла?\nПроверьте 5 шагов", None),
           "C": ("Один рубец.\nДва исхода.", "compare")},
    "05": {"B": ("Бросили через неделю?\nРано", None),
           "C": ("Недели → 1–3 мес →\n3–6 мес", "effect")},
    "14": {"B": ("Шов стал плотнее\nи краснее?", None),
           "C": ("Начните сразу\nпосле снятия швов", "effect")},
    "15": {"B": ("Рубец стал плотнее\nи краснее?", None),
           "C": ("Начните сразу\nпосле снятия швов", "effect")},
    "16": {"B": ("Ожог зажил,\nа рубец растёт?", None),
           "C": ("Начните, как только\nкожа закрылась", "effect")},
    "17": {"B": ("Растяжки свежие\nи заметные?", None),
           "C": ("3–6 месяцев —\nсветлее, ровнее", "effect")},
}


def variant(num: str, key: str, title: str, visual: str | None) -> dict:
    src = json.loads((PROJECT / "topics" / f"topic_{num}.json").read_text(encoding="utf-8"))
    d = copy.deepcopy(src)
    d["title"] = src["title"].rstrip("»") + f" — крючок {key}»"
    d["output_dir"] = "output/yafho/hooks"
    d["public_dir"] = "yafho-hooks"
    d["hook_of"] = f"topic_{num}"
    d.pop("cuts", None)
    d.pop("cut_prefix", None)
    d["formats"] = {k: v for k, v in d["formats"].items() if k in ("9x16", "4x5")}
    first = d["scenes"][0]
    first["titles"] = [{"text": title, "at": 0, "lead": 0.1}]
    shape = SKIN_SHAPE[num]
    if visual == "effect":
        first.update(kind="CUT", shot=f"крючок {key}: пластина на плотном рубце, рубец бледнеет",
                     cut={"type": "skin_demo", "skinShape": shape, "skinStep": "effect", "months": 6,
                          "skinFrom": "hyper", "reveal": False})
    elif visual == "compare":
        first.update(kind="CUT", shot=f"крючок {key}: два исхода, 0 → 6 мес",
                     cut={"type": "skin_demo", "skinShape": shape, "skinStep": "compare", "progressFrom": 0, "progressTo": 1})
    else:
        first["shot"] = f"крючок {key}: " + first.get("shot", "")
    d["cover_at"] = min(2.0, first["end"] - 0.5)
    return d


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for num, vs in HOOKS.items():
        for key, (title, visual) in vs.items():
            p = OUT / f"topic_{num}_hook{key}.json"
            p.write_text(json.dumps(variant(num, key, title, visual), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"{p.relative_to(PROJECT)} · «{title.replace(chr(10), ' ')}»")


if __name__ == "__main__":
    main()
