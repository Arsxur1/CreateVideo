"""Yafho-Silicare — pre-publication check (TZ §5, CLAUDE.md «Жёсткие правила») over every scene file.

    python projects/yafho/check_rules.py               # hero_v3, hero_v4 (if any), topics/topic_*.json, CONTENT_PLAN.md
    python projects/yafho/check_rules.py --strict      # exit 1 on any error (for CI / before publishing)

Checks
  · forbidden promises: «уберёт», «100%», «навсегда», «гарантия», «излечит», «полностью исчезнет»
  · every title ≤ 6 words and on screen ≥ 2.5 s (same timing rule as build_v2.py)
  · every study figure (stat) carries a source line
  · brand name is Yafho-Silicare (no «SiliSkin»)
  · no Kling placeholders left (warning: shows «нужен H0X» until the clip is added)
Writes projects/yafho/CHECK_REPORT.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
KLING = PROJECT / "assets" / "kling"
FORBIDDEN = [r"убер[её]т", r"100\s*%", r"навсегда", r"гарант", r"излеч", r"полностью исчез", r"SiliSkin"]
MAX_WORDS = 6
MIN_HOLD = 2.5


# text colour / background pairs used by the Yafho components (tokens.ts)
CONTRAST_PAIRS = [
    ("#0F2440", "#FFFFFF"),  # navy titles / labels on white cards
    ("#FFFFFF", "#0F2440"),  # white on navy (titles, end card, month pill)
    ("#5B6472", "#FFFFFF"),  # muted source lines, «схема»
    ("#B04408", "#FFFFFF"),  # orangeText: «+1 см» labels
    ("#FFFFFF", "#B04408"),  # day clock event chips
    ("#FFFFFF", "#0A7067"),  # day clock wear chips
    ("#0A7067", "#E3F3F1"),  # «Правильно / Ответ» labels
    ("#B42318", "#FBEAE8"),  # «Ошибка» label
    ("#0F2440", "#E3F3F1"),  # check list / fact text
    ("#D4560F", "#FFFFFF"),  # brand orange — lines, arrows, icons only
    ("#0D9488", "#FFFFFF"),  # brand teal — lines, arcs, icons only
]


def contrast(fg: str, bg: str) -> float:
    def lum(h: str) -> float:
        c = [int(h.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    a, b = sorted((lum(fg), lum(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def words(text: str) -> int:
    """Words a viewer reads: tokens with a letter or digit (·, —, =, → do not count)."""
    return sum(1 for tok in re.split(r"\s+", text.strip()) if re.search(r"[\wА-Яа-яЁё]", tok))


def texts_of(scene: dict) -> list[str]:
    out = [t["text"] for t in scene.get("titles", [])]
    for key in ("cta", "footnote"):
        if scene.get(key):
            out.append(scene[key])
    if scene.get("stat"):
        out += [scene["stat"]["value"], scene["stat"]["label"]]
    if scene.get("chips"):
        out += [scene["chips"].get("title", ""), *scene["chips"]["items"]]
    cut = scene.get("cut", {})
    for key in ("myth", "fact", "title", "checkNote"):
        if cut.get(key):
            out.append(cut[key])
    out += [i["text"] for i in cut.get("checkItems", [])]
    return out


def check_file(path: Path) -> tuple[list[str], list[str], int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    warnings: list[str] = []
    n_titles = 0
    for s in data["scenes"]:
        sid = f"{path.stem}/{s['id']}"
        dur = s["end"] - s["start"]
        titles = s.get("titles", [])
        for i, t in enumerate(titles):
            n_titles += 1
            w = words(t["text"])
            if w > MAX_WORDS:
                errors.append(f"{sid}: титр «{t['text'].replace(chr(10), ' ')}» — {w} слов (> {MAX_WORDS})")
            t_in = t["at"] * dur + (t.get("lead", 0.3) if t["at"] == 0 else 0)
            t_out = titles[i + 1]["at"] * dur if i + 1 < len(titles) else dur
            if t_out - t_in < MIN_HOLD - 1e-6:
                errors.append(f"{sid}: титр «{t['text'].replace(chr(10), ' ')}» держится {t_out - t_in:.2f} с (< {MIN_HOLD})")
        for txt in texts_of(s):
            for pat in FORBIDDEN:
                if re.search(pat, txt, re.IGNORECASE):
                    errors.append(f"{sid}: запрещённая формулировка /{pat}/ в «{txt.replace(chr(10), ' ')}»")
        if s.get("stat") and not s["stat"].get("source", "").strip():
            errors.append(f"{sid}: цифра «{s['stat']['value']}» без источника")
        clip = s.get("kling") if s.get("kind") == "R" else None
        if clip and not (KLING / f"{clip}.mp4").exists():
            warnings.append(f"{sid}: заглушка «нужен {clip}» (нет assets/kling/{clip}.mp4)")
    if data.get("brand", "Yafho-Silicare") != "Yafho-Silicare":
        errors.append(f"{path.stem}: бренд «{data.get('brand')}» вместо Yafho-Silicare")
    return errors, warnings, n_titles


def check_markdown(path: Path) -> list[str]:
    errors = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith(("**Правила", "- Только", "> ")) or "Никаких" in line:
            continue  # the rule lines themselves quote the forbidden words
        for pat in FORBIDDEN:
            if re.search(pat, line, re.IGNORECASE):
                errors.append(f"{path.name}:{n}: запрещённая формулировка /{pat}/")
    return errors


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    files = [p for p in [PROJECT / "hero_v3.json", PROJECT / "hero_v4.json"] if p.exists()]
    files += sorted((PROJECT / "topics").glob("topic_*.json"))
    all_err: list[str] = []
    all_warn: list[str] = []
    rows = []
    for f in files:
        e, w, n = check_file(f)
        all_err += e
        all_warn += w
        rows.append(f"| `{f.relative_to(PROJECT)}` | {n} | {len(e)} | {len(w)} |")
    plan = PROJECT / "CONTENT_PLAN.md"
    if plan.exists():
        all_err += check_markdown(plan)

    report = ["# Проверка перед публикацией (ТЗ §5)", "",
              "Сгенерировано `check_rules.py`. Правила: титр ≤ 6 слов и ≥ 2,5 с; нет «уберёт / 100% / навсегда / гарантия»; "
              "у каждой цифры есть источник; бренд Yafho-Silicare; заглушки Kling — предупреждение.", "",
              "| Файл | Титров | Ошибок | Предупреждений |", "|---|---|---|---|", *rows, "",
              f"**Итого: ошибок {len(all_err)}, предупреждений {len(all_warn)}.**", ""]
    if all_err:
        report += ["## Ошибки", "", *[f"- {x}" for x in all_err], ""]
    if all_warn:
        report += ["## Предупреждения", "", *[f"- {x}" for x in all_warn], ""]
    report += ["## Вручную (код не проверит)", "",
               "- Размеры пластин сверены с упаковкой (темы 06, 14–17).",
               "- Нет лиц, ран, крови — в кадрах Kling, когда они появятся.", ""]
    report += ["## Контраст текста (WCAG, ТЗ: ≥ 4,5:1)", "", "| Текст | Фон | Контраст |", "|---|---|---|",
               *[f"| `{a}` | `{b}` | {contrast(a, b):.2f}:1 {'✓' if contrast(a, b) >= 4.5 else '— только линии и иконки'} |"
                 for a, b in CONTRAST_PAIRS], ""]
    (PROJECT / "CHECK_REPORT.md").write_text("\n".join(report), encoding="utf-8")
    print(f"{len(files)} файлов · ошибок {len(all_err)} · предупреждений {len(all_warn)} → projects/yafho/CHECK_REPORT.md")
    for x in all_err:
        print("  ✗", x)
    if args.strict and all_err:
        sys.exit(1)


if __name__ == "__main__":
    main()
