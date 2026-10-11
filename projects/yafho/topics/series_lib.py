"""Yafho-Silicare — shared helpers for the generated topic files (series 2 and 3).

Facts come only from the product passport (TZ §0). Titles ≤ 6 words.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FORMATS = {
    "9x16": {"profile": "instagram_reels", "layout": "full"},
    "16x9": {"profile": "youtube_landscape", "layout": "split",
             "cut_overrides": {"skin_demo": {"areaTop": 0.035, "areaBottom": 0.965},
                               "result_curve": {"areaTop": 0.035, "areaBottom": 0.965}}},
    "4x5": {"profile": "instagram_portrait", "layout": "full", "cut3d": {"centerY": 0.42, "fitFrac": 0.9}},
    "1x1": {"profile": "instagram_feed", "layout": "full", "cut3d": {"centerY": 0.4, "fitFrac": 0.85}},  # Telegram
}


def skin(shape: str, step: str, **kw) -> dict:
    return {"type": "skin_demo", "skinShape": shape, "skinStep": step, **kw}


def scene(sid: str, start: float, end: float, shot: str, cut: dict | None = None, titles=(), **kw) -> dict:
    s = {"id": sid, "start": start, "end": end, "kind": "CUT" if cut else "C", "shot": shot, "titles": list(titles)}
    if cut:
        s["cut"] = cut
    s.update(kw)
    return s


def title(text: str, at: float = 0, lead: float = 0, **kw) -> dict:
    return {"text": text, "at": at, "lead": lead, **kw}


def end_card(sid: str, start: float, end: float, cta: str) -> dict:
    return scene(sid, start, end, "эндкард", cta=cta)


def write(num: str, name: str, scenes: list[dict], score: dict, cover_at: float, story: dict, plan: str) -> None:
    d = {
        "title": f"Yafho-Silicare — тема {num} «{name}»",
        "plan": f"projects/yafho/{plan}#{num}",
        "brand": "Yafho-Silicare",
        "output_dir": "output/yafho/topics",
        "public_dir": "yafho-topics",
        "duration": scenes[-1]["end"],
        "backdrop": "linen",
        "cover_at": cover_at,
        "audio": "no voice — titles + arrows + music",
        "music": {"file": f"yafho_topic_{num}.wav", "volume": 1.0, "fadeInSeconds": 0.05, "fadeOutSeconds": 1.5},
        "scenes": scenes,
        "score": score,
        "formats": copy.deepcopy(FORMATS),
        "cut_prefix": f"topic_{num}_story",
        "cuts": {"S": story},
    }
    (HERE / f"topic_{num}.json").write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"topic_{num}.json · {d['duration']} s · «{name}»")


def seg(start, end, mood, *chords):
    return {"start": start, "end": end, "mood": mood, "chords": list(chords)}


def acc(t, kind):
    return {"t": t, "kind": kind}
