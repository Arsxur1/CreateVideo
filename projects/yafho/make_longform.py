"""Yafho-Silicare — «Гид по силиконовым пластинам»: one 16:9 long video for YouTube / the website.

    python projects/yafho/make_longform.py           # → output/yafho/longform/guide_16x9.mp4 + chapters.txt

Edited from the rendered 16:9 videos (no new facts): hero v4 as the intro, then the
topic videos as chapters — each without its own end card — separated by 2.5 s
chapter cards (rendered once in Remotion with a soft score), and one end card at
the very end. chapters.txt holds YouTube chapter timestamps for the description.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
ROOT = PROJECT.parent.parent
sys.path.insert(0, str(PROJECT))
OUT = ROOT / "output" / "yafho" / "longform"
COMPOSER = ROOT / "remotion-composer"
CARD = 2.5
XF = 0.3  # audio fade at every join

# (chapter title, short line under it, topic number)
CHAPTERS = [
    ("Почему рубец растёт", "рана зажила, а рубец уплотняется", "02"),
    ("Кому подходит", "пять типичных рубцов", "03"),
    ("Когда начинать", "сразу после закрытия раны и снятия швов", "10"),
    ("Как наклеить", "пять шагов", "04"),
    ("Какой размер", "рубец + 1 см со всех сторон", "06"),
    ("День с пластиной", "12–23 ч в сутки, две пластины", "11"),
    ("Когда ждать результат", "недели → 1–3 мес → 3–6 мес", "05"),
    ("Три ошибки", "и как правильно", "07"),
    ("Когда нельзя", "противопоказания", "12"),
    ("Что говорят исследования", "цифры с источниками", "08"),
]


def run(cmd: list[str], **kw) -> None:
    subprocess.run(cmd, check=True, **kw)


def body_end(data: dict) -> float:
    """Where the topic's own end card starts (kind C as the last scene)."""
    last = data["scenes"][-1]
    return last["start"] if last.get("kind") == "C" else data["duration"]


def render_cards() -> Path:
    """All chapter cards in one 16:9 video (brand backdrop + centred numbered title + soft score)."""
    import make_music as mm
    from build_v2 import backdrop_for, configure, remotion_env

    OUT.mkdir(parents=True, exist_ok=True)
    total = CARD * len(CHAPTERS)
    data = {"backdrop": "linen", "duration": total, "public_dir": "yafho-longform",
            "score": {"bpm": 88, "segments": [{"start": i * CARD, "end": (i + 1) * CARD, "mood": "light",
                                               "chords": ["F" if i % 2 else "C"]} for i in range(len(CHAPTERS))],
                      "accents": [{"t": i * CARD + 0.05, "kind": "chime"} for i in range(len(CHAPTERS))]}}
    configure(OUT / "chapters.json", data)
    import build_v2
    build_v2.PUBLIC.mkdir(parents=True, exist_ok=True)
    wav = build_v2.PUBLIC / "chapters.wav"
    mm.write_wav(OUT / "_chapters_raw.wav", mm.compose_score(data))
    mm.loudnorm(OUT / "_chapters_raw.wav", wav)
    (OUT / "_chapters_raw.wav").unlink()
    overlays = []
    for i, (title, line, _) in enumerate(CHAPTERS):
        overlays.append({"type": "thesis", "text": f"{i + 1} · {title}", "subtitle": line, "variant": "dark",
                         "position": "center", "fontSize": 92, "in_seconds": i * CARD + 0.1, "out_seconds": (i + 1) * CARD})
    props = {"theme": "yafho-clinical", "durationSeconds": total, "layout": "full",
             "cuts": [{"id": "bg", "source": "", "in_seconds": 0, "out_seconds": total, "type": "blank"}],
             "overlays": overlays,
             "audio": {"music": {"src": f"{build_v2.PUBLIC_REL}/chapters.wav", "volume": 1.0, "fadeInSeconds": 0.05, "fadeOutSeconds": 0.3}}}
    bd = backdrop_for(data, (1920, 1080))
    if bd:
        props["backdrop"] = {"image": bd}
    pp = OUT / "_chapters_props.json"
    pp.write_text(json.dumps(props, ensure_ascii=False), encoding="utf-8")
    dest = OUT / "_chapters_16x9.mp4"
    run(["npx", "remotion", "render", "src/index.tsx", "Explainer", str(dest), f"--props={pp}", "--width=1920", "--height=1080"],
        cwd=COMPOSER, env=remotion_env(), capture_output=True)
    pp.unlink()
    return dest


def segment(src: Path, a: float, b: float, dest: Path) -> None:
    d = b - a
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{a:.3f}", "-i", str(src), "-t", f"{d:.3f}",
         "-vf", "fps=30,format=yuv420p,scale=1920:1080",
         "-af", f"aresample=48000,afade=t=in:d={XF},afade=t=out:st={max(0, d - XF):.3f}:d={XF}",
         "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", str(dest)])


def stamp(t: float) -> str:
    return f"{int(t // 60)}:{int(t % 60):02d}"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    cards = render_cards()
    hero_data = json.loads((PROJECT / "hero_v4.json").read_text(encoding="utf-8"))
    hero = ROOT / "output" / "yafho" / "v4" / "hero_v4_16x9.mp4"
    parts: list[Path] = []
    marks: list[tuple[float, str]] = []
    t = 0.0

    def add(src: Path, a: float, b: float, name: str, mark: str | None = None) -> None:
        nonlocal t
        p = OUT / f"_{len(parts):02d}_{name}.mp4"
        segment(src, a, b, p)
        if mark:
            marks.append((t, mark))
        parts.append(p)
        t += b - a

    hero_body = body_end(hero_data)
    add(hero, 0, hero_body, "hero", "Один рубец — два исхода")
    for i, (title, _line, n) in enumerate(CHAPTERS):
        data = json.loads((PROJECT / "topics" / f"topic_{n}.json").read_text(encoding="utf-8"))
        add(cards, i * CARD, (i + 1) * CARD, f"card{i + 1}", title)
        add(ROOT / "output" / "yafho" / "topics" / f"topic_{n}_16x9.mp4", 0, body_end(data), f"t{n}")
    add(hero, hero_body, hero_data["duration"], "end", "Начните, пока рубец молодой")

    lst = OUT / "_list.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in parts), encoding="utf-8")
    dest = OUT / "guide_16x9.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
         "-movflags", "+faststart", str(dest)], cwd=OUT)
    for p in parts:
        p.unlink()
    lst.unlink()
    chapters = "\n".join(f"{stamp(s)} {m}" for s, m in marks)
    (OUT / "chapters.txt").write_text(chapters + "\n", encoding="utf-8")
    print(f"{dest.relative_to(ROOT)} · {stamp(t)} · {len(CHAPTERS)} глав\n{chapters}")


if __name__ == "__main__":
    os.environ.setdefault("REMOTION_GL", "angle")
    main()
