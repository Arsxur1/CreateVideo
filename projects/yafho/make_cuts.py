"""Yafho-Silicare — 15 s cut-downs edited from the rendered hero v2 (no re-render).

    python projects/yafho/make_cuts.py              # every hero_v2_<fmt>.mp4 that exists
    python projects/yafho/make_cuts.py --formats 9x16
    python projects/yafho/make_cuts.py --data projects/yafho/hero_v3.json   # cuts + audience cards from the scene file

Each cut is a list of (scene, from, to) windows in scene-relative seconds,
chosen so every title is already on screen and held ≥ 2.5 s. Windows are
joined with short cross-dissolves; the soundtrack is the last N seconds of
the hero music so every cut lands on the same end chord as the end card.

Output: output/yafho/v2/cut_<A|B|C>_<fmt>.mp4 (topics: <cut_prefix>_<key>_<fmt>.mp4)
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
ROOT = PROJECT.parent.parent
OUT = ROOT / "output" / "yafho" / "v2"
XFADE = 0.25

CUTS = {
    "A": {
        "name": "Почему рубец остаётся",
        "windows": [("S01", 0.0, 3.2), ("S06", 0.3, 3.1), ("S07", None, 6.5), ("S08", None, 6.0), ("S13", 0.0, 3.2)],
    },
    "B": {
        "name": "Как работает силикон",
        "windows": [("S09", 0.0, 3.0), ("S10", 0.0, 6.0), ("S12", None, 7.0), ("S13", 0.0, 3.2)],
    },
    "C": {
        "name": "Как наклеить",
        "windows": [("S09", 0.0, 2.8), ("S11a", 0.0, 3.0), ("S11b", 0.0, 3.0), ("S11c", 0.0, 3.0), ("S13", 0.0, 3.6)],
    },
}


def second_title_at(scene: dict) -> float:
    """Scene-relative start of the scene's last title (used when 'from' is None)."""
    t = scene["titles"][-1]
    return t["at"] * (scene["end"] - scene["start"])


def build_cut(video: Path, music: Path | None, data: dict, windows: list, dest: Path, cards_dir: Path | None = None,
              fmt: str = "9x16") -> float:
    scenes = {s["id"]: s for s in data["scenes"]}
    inputs = ["-i", str(video)]
    # each item: (input index, start, end)
    spans: list[tuple[int, float, float]] = []
    for w in windows:
        if isinstance(w, dict) and "card" in w:
            clip = (cards_dir or video.parent) / f"card_{w['card']}_{fmt}.mp4"
            if not clip.exists():
                raise SystemExit(f"missing {clip} — render it with build_v2.py --cards")
            inputs += ["-i", str(clip)]
            idx = len(inputs) // 2 - 1
            dur = float(data["cards"][w["card"]]["duration"])
            spans.append((idx, 0.0, dur))
            continue
        sid, a, b = w
        sc = scenes[sid]
        a = second_title_at(sc) if a is None else a
        spans.append((0, sc["start"] + a, sc["start"] + b))

    parts = []
    for i, (src, a, b) in enumerate(spans):
        parts.append(f"[{src}:v]trim=start={a:.3f}:end={b:.3f},setpts=PTS-STARTPTS,fps=30,format=yuv420p[v{i}]")
    length = spans[0][2] - spans[0][1]
    last = "v0"
    for i in range(1, len(spans)):
        d = spans[i][2] - spans[i][1]
        out = f"x{i}"
        parts.append(f"[{last}][v{i}]xfade=transition=fade:duration={XFADE}:offset={length - XFADE:.3f}[{out}]")
        length += d - XFADE
        last = out
    cmd = ["ffmpeg", "-y", "-loglevel", "error", *inputs]
    maps = ["-map", f"[{last}]"]
    if music and music.exists():
        total = data["duration"]
        cmd += ["-i", str(music)]
        mi = len(inputs) // 2
        parts.append(
            f"[{mi}:a]atrim=start={total - length:.3f}:end={total:.3f},asetpts=PTS-STARTPTS,"
            f"afade=t=in:d=0.6,afade=t=out:st={length - 1.2:.3f}:d=1.2[a]"
        )
        maps += ["-map", "[a]"]
    cmd += ["-filter_complex", ";".join(parts), *maps,
            "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(dest)]
    subprocess.run(cmd, check=True)
    return length


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--formats", default="9x16,16x9,4x5")
    ap.add_argument("--data", default=str(PROJECT / "hero_v2.json"))
    args = ap.parse_args()
    data_path = Path(args.data)
    data = json.loads(data_path.read_text(encoding="utf-8"))
    out_dir = ROOT / data.get("output_dir", "output/yafho/v2")
    music = PROJECT / "assets" / "music" / data["music"]["file"]
    cuts = data.get("cuts") or {k: {"name": v["name"], "windows": [list(w) for w in v["windows"]]} for k, v in CUTS.items()}
    for fmt in [f.strip() for f in args.formats.split(",") if f.strip()]:
        video = out_dir / f"{data_path.stem}_{fmt}.mp4"
        if not video.exists():
            print(f"skip {fmt}: {video.relative_to(ROOT)} not rendered yet")
            continue
        prefix = data.get("cut_prefix", "cut")  # topics: "topic_NN_story" so cut files never collide
        for key, cut in cuts.items():
            dest = out_dir / f"{prefix}_{key}_{fmt}.mp4"
            length = build_cut(video, music, data, cut["windows"], dest, out_dir, fmt)
            print(f"{dest.relative_to(ROOT)} · {length:.1f} s · «{cut['name']}»")


if __name__ == "__main__":
    main()
