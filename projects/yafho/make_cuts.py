"""Yafho-Silicare — 15 s cut-downs edited from the rendered hero v2 (no re-render).

    python projects/yafho/make_cuts.py              # every hero_v2_<fmt>.mp4 that exists
    python projects/yafho/make_cuts.py --formats 9x16

Each cut is a list of (scene, from, to) windows in scene-relative seconds,
chosen so every title is already on screen and held ≥ 2.5 s. Windows are
joined with short cross-dissolves; the soundtrack is the last N seconds of
the hero music so every cut lands on the same end chord as the end card.

Output: output/yafho/v2/cut_<A|B|C>_<fmt>.mp4
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


def build_cut(video: Path, music: Path | None, data: dict, key: str, dest: Path) -> float:
    scenes = {s["id"]: s for s in data["scenes"]}
    spans = []
    for sid, a, b in CUTS[key]["windows"]:
        sc = scenes[sid]
        a = second_title_at(sc) if a is None else a
        spans.append((sc["start"] + a, sc["start"] + b))

    parts = []
    for i, (a, b) in enumerate(spans):
        parts.append(f"[0:v]trim=start={a:.3f}:end={b:.3f},setpts=PTS-STARTPTS,fps=30,format=yuv420p[v{i}]")
    length = spans[0][1] - spans[0][0]
    last = "v0"
    for i in range(1, len(spans)):
        d = spans[i][1] - spans[i][0]
        out = f"x{i}"
        parts.append(f"[{last}][v{i}]xfade=transition=fade:duration={XFADE}:offset={length - XFADE:.3f}[{out}]")
        length += d - XFADE
        last = out
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video)]
    maps = ["-map", f"[{last}]"]
    if music and music.exists():
        total = data["duration"]
        cmd += ["-i", str(music)]
        parts.append(
            f"[1:a]atrim=start={total - length:.3f}:end={total:.3f},asetpts=PTS-STARTPTS,"
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
    args = ap.parse_args()
    data = json.loads((PROJECT / "hero_v2.json").read_text(encoding="utf-8"))
    music = PROJECT / "assets" / "music" / data["music"]["file"]
    for fmt in [f.strip() for f in args.formats.split(",") if f.strip()]:
        video = OUT / f"hero_v2_{fmt}.mp4"
        if not video.exists():
            print(f"skip {fmt}: {video.relative_to(ROOT)} not rendered yet")
            continue
        for key, cut in CUTS.items():
            dest = OUT / f"cut_{key}_{fmt}.mp4"
            length = build_cut(video, music, data, key, dest)
            print(f"{dest.relative_to(ROOT)} · {length:.1f} s · «{cut['name']}»")


if __name__ == "__main__":
    main()
