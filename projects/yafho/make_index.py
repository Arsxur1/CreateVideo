"""Yafho-Silicare — inventory of every delivered file (videos, stories, cuts, covers, carousels).

    python projects/yafho/make_index.py      # → projects/yafho/DELIVERABLES.md

Scans output/yafho/ (git-ignored renders) and lists what exists, with duration
and size, next to the scene file it was built from.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
ROOT = PROJECT.parent.parent
OUT = ROOT / "output" / "yafho"
FMTS = ("9x16", "16x9", "4x5", "1x1")


def dur(p: Path) -> str:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    try:
        return f"{float(r.stdout.strip()):.1f} с"
    except ValueError:
        return "?"


def mark(p: Path) -> str:
    return "✓" if p.exists() else "—"


def main() -> None:
    lines = ["# Yafho-Silicare — что готово", "",
             "Сгенерировано `make_index.py` по папке `output/yafho/` (рендеры не хранятся в git — пересобираются командами из README).", ""]

    lines += ["## Hero", "", "| Версия | Длина | 9:16 | 16:9 | 4:5 | 1:1 | Нарезки 15 с |", "|---|---|---|---|---|---|---|"]
    for ver, name in (("v4", "hero v4 — без заглушек (основная)"), ("v3", "hero v3 — с заглушками Kling"), ("v2", "hero v2 — длинная")):
        d = OUT / ver
        stem = f"hero_{ver}"
        first = d / f"{stem}_9x16.mp4"
        cuts = sorted({p.name.split("_")[1] for p in d.glob("cut_*_9x16.mp4")}) if d.exists() else []
        lines.append(f"| {name} | {dur(first) if first.exists() else '—'} | " +
                     " | ".join(mark(d / f"{stem}_{f}.mp4") for f in FMTS) + f" | {', '.join(cuts) or '—'} |")
    lines.append("")

    lines += ["## Темы", "", "| № | Тема | Длина | 9:16 | 16:9 | 4:5 | 1:1 | Обложка | Сторис | Карусель |", "|---|---|---|---|---|---|---|---|---|---|"]
    for data_path in sorted((PROJECT / "topics").glob("topic_*.json")):
        n = data_path.stem.split("_")[1]
        data = json.loads(data_path.read_text(encoding="utf-8"))
        name = data["title"].split("«")[-1].rstrip("»")
        t = OUT / "topics"
        v = t / f"topic_{n}_9x16.mp4"
        car = OUT / "carousels" / f"topic_{n}"
        slides = len(list(car.glob("slide_*.png"))) if car.exists() else 0
        lines.append(f"| {n} | {name} | {dur(v) if v.exists() else '—'} | " +
                     " | ".join(mark(t / f"topic_{n}_{f}.mp4") for f in FMTS) +
                     f" | {mark(t / f'topic_{n}_4x5_cover.png')} | {mark(t / f'topic_{n}_story_S_9x16.mp4')} | "
                     f"{f'{slides} слайдов' if slides else '—'} |")
    lines.append("")

    vids = list(OUT.rglob("*.mp4"))
    size = sum(p.stat().st_size for p in vids) / 1e6
    lines += [f"Всего видеофайлов: **{len(vids)}** ({size:.0f} МБ).", "",
              "Гид 16:9: `output/yafho/longform/guide_16x9.mp4` + `chapters.txt`. Субтитры: `output/yafho/subtitles/`. Обложки YouTube: `output/yafho/thumbs/`.", "",
              "Пути: `output/yafho/v4/`, `output/yafho/topics/topic_NN_<формат>.mp4`, сторис `topic_NN_story_S_9x16.mp4`, "
              "обложки `topic_NN_<формат>_cover.png`, карусели `output/yafho/carousels/topic_NN/`.", ""]
    (PROJECT / "DELIVERABLES.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"projects/yafho/DELIVERABLES.md · {len(vids)} видео · {size:.0f} МБ")


if __name__ == "__main__":
    main()
