"""Yafho-Silicare — subtitles (.srt) for every video, made from the on-screen text in the scene files.

    python projects/yafho/make_srt.py      # → output/yafho/subtitles/<video>.srt

The videos have no voice; the .srt repeats what the viewer reads (titles, chips,
check lists, Q&A, study figures with sources, end-card call to action) with the
same timing build_v2.py uses. Upload it as the caption track on YouTube / VK:
captions are indexed by search and read aloud by screen readers.
Also writes subtitles for the long guide (guide_16x9.srt) by shifting each
chapter's lines to its place in the edit.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
ROOT = PROJECT.parent.parent
OUT = ROOT / "output" / "yafho" / "subtitles"
sys.path.insert(0, str(PROJECT))


def flat(text: str) -> str:
    return " ".join(text.replace("\n", " ").split())


def cues(data: dict) -> list[tuple[float, float, str]]:
    """(start, end, text) in the order they appear, mirroring build_v2.build_animatic."""
    out: list[tuple[float, float, str]] = []
    for s in data["scenes"]:
        a, b = s["start"], s["end"]
        dur = b - a
        titles = s.get("titles", [])
        for i, t in enumerate(titles):
            t_in = a + t["at"] * dur + (t.get("lead", 0.3) if t["at"] == 0 else 0)
            t_out = a + titles[i + 1]["at"] * dur if i + 1 < len(titles) else b
            text = flat(t["text"])
            if t.get("footnote") and s.get("footnote"):
                text += f" ({s['footnote']})"
            out.append((t_in, t_out, text))
        if s.get("chips"):
            ch = s["chips"]
            out.append((a, b, flat(ch.get("title", "")) + " " + ", ".join(flat(x) for x in ch["items"]) + "."))
        cut = s.get("cut", {})
        if cut.get("type") == "check_list":
            items = "; ".join(("✓ " if i.get("kind", "ok") == "ok" else "✗ " if i.get("kind") == "no" else "! ") + flat(i["text"])
                              for i in cut["checkItems"])
            out.append((a, b, f"{flat(cut.get('title', ''))} {items}."))
        if cut.get("type") == "myth_fact":
            if cut.get("mythVariant") == "qa":
                out.append((a, b, f"Вопрос: {flat(cut['myth'])} Ответ: {flat(cut['fact'])}"))
            else:
                out.append((a, b, f"Ошибка: {flat(cut['myth'])}. Правильно: {flat(cut['fact'])}."))
        if cut.get("type") == "day_clock":
            out.append((a, b, "07:00 наклеить; 07–21 день — под одеждой; 21:00 промыть, сменить; 22–07 ночь — вторая пластина. "
                              "23 ч на коже в сутки."))
        if cut.get("type") == "size_guide":
            out.append((a, b, "4×4 см — лицо, мелкий; 4×13 см — рука; 5×15 см — живот; 10×15 см — ожог."))
        if cut.get("type") == "result_curve":
            out.append((a, b, "Схема по срокам из инструкции: недели — первые изменения; 1–3 мес — заметно; 3–6 мес — ровнее."))
        if s.get("stat"):
            st = s["stat"]
            out.append((a + st.get("delay", 1.5), b, f"{flat(st['value'])} — {flat(st['label'])}. Источник: {st['source']}"))
        if s.get("kind") == "C":
            out.append((a + 0.3, b, (flat(s["cta"]) + ". " if s.get("cta") else "") + "Yafho-Silicare · @sil.icare"))
    out.sort(key=lambda c: c[0])
    return out


def stamp(t: float) -> str:
    ms = int(round(max(0.0, t) * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write(path: Path, items: list[tuple[float, float, str]]) -> None:
    blocks = [f"{i}\n{stamp(a)} --> {stamp(b)}\n{text}\n" for i, (a, b, text) in enumerate(items, 1)]
    path.write_text("\n".join(blocks), encoding="utf-8")


def guide() -> int:
    """Shift each chapter's cues to its place in output/yafho/longform/guide_16x9.mp4 (same order as make_longform)."""
    import make_longform as lf

    items: list[tuple[float, float, str]] = []
    hero = json.loads((PROJECT / "hero_v4.json").read_text(encoding="utf-8"))
    hero_body = lf.body_end(hero)
    t = 0.0
    items += [(a, min(b, hero_body), x) for a, b, x in cues(hero) if a < hero_body]
    t += hero_body
    for i, (title, line, n) in enumerate(lf.CHAPTERS):
        items.append((t + 0.1, t + lf.CARD, f"{i + 1} · {title} — {line}"))
        t += lf.CARD
        data = json.loads((PROJECT / "topics" / f"topic_{n}.json").read_text(encoding="utf-8"))
        body = lf.body_end(data)
        items += [(t + a, t + min(b, body), x) for a, b, x in cues(data) if a < body]
        t += body
    items += [(t + a - hero_body, t + b - hero_body, x) for a, b, x in cues(hero) if a >= hero_body]
    write(OUT / "guide_16x9.srt", items)
    return len(items)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    files = [PROJECT / "hero_v4.json", *sorted((PROJECT / "topics").glob("topic_*.json"))]
    total = 0
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        c = cues(data)
        write(OUT / f"{f.stem}.srt", c)
        total += len(c)
    g = guide()
    print(f"{OUT.relative_to(ROOT)} · {len(files) + 1} файлов · {total + g} строк")


if __name__ == "__main__":
    main()
