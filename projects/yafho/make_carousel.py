"""Yafho-Silicare — Instagram carousels (4:5, 1080×1350) cut from the rendered topic videos.

    python projects/yafho/make_carousel.py                  # every topic listed in CAROUSELS
    python projects/yafho/make_carousel.py 04 07            # chosen topics

TZ §3: every theme is a video plus a picture post; topic 03 is explicitly a carousel.
A slide is one frame of topic_NN_4x5.mp4 at a moment where the title and the
animation are complete (fraction of the scene). Output:
    output/yafho/carousels/topic_NN/slide_01.png … + preview.png (all slides side by side)
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
ROOT = PROJECT.parent.parent
VIDEOS = ROOT / "output" / "yafho" / "topics"
OUT = ROOT / "output" / "yafho" / "carousels"

# (scene id, fraction of the scene) per slide; the end card closes every carousel
CAROUSELS: dict[str, list[tuple[str, float]]] = {
    "04": [("T1", 0.5), ("T2", 0.38), ("T3", 0.92), ("T4", 0.95), ("T5", 0.42), ("T5", 0.95), ("T6", 0.92), ("T7", 0.95)],
    "03": [("I1", 0.95), ("I2", 0.95), ("I3", 0.95), ("I4", 0.95), ("I5", 0.95), ("I6", 0.95), ("I7", 0.9), ("I8", 0.95)],
    "07": [("E1", 0.85), ("E2", 0.88), ("E3", 0.88), ("E4", 0.88), ("E5", 0.55), ("E6", 0.95)],
    "13": [("Q1", 0.88), ("Q2", 0.88), ("Q3", 0.88), ("Q4", 0.88), ("Q5", 0.55), ("Q6", 0.95)],
    "08": [("N1", 0.88), ("N2", 0.88), ("N3", 0.88), ("N4", 0.88), ("N5", 0.95)],
    "10": [("S1", 0.9), ("S2", 0.95), ("S3", 0.95), ("S4", 0.55), ("S5", 0.95)],
    "12": [("N1", 0.95), ("N2", 0.95), ("N3", 0.95), ("N4", 0.95)],
    "06": [("Z1", 0.92), ("Z2", 0.95), ("Z3", 0.95)],
    "11": [("D1", 0.95), ("D2", 0.97), ("D3", 0.92), ("D4", 0.55), ("D5", 0.95)],
}


def build(num: str) -> Path | None:
    data = json.loads((PROJECT / "topics" / f"topic_{num}.json").read_text(encoding="utf-8"))
    video = VIDEOS / f"topic_{num}_4x5.mp4"
    if not video.exists():
        print(f"skip {num}: {video.relative_to(ROOT)} not rendered")
        return None
    scenes = {s["id"]: s for s in data["scenes"]}
    dest = OUT / f"topic_{num}"
    dest.mkdir(parents=True, exist_ok=True)
    for old in dest.glob("slide_*.png"):
        old.unlink()
    slides = []
    for i, (sid, frac) in enumerate(CAROUSELS[num], 1):
        sc = scenes[sid]
        t = sc["start"] + (sc["end"] - sc["start"]) * frac
        if sc.get("kind") != "C":
            t = min(t, sc["end"] - 0.5)  # titles fade out over the last 0.4 s of a scene
        png = dest / f"slide_{i:02d}.png"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1", str(png)],
                       check=True)
        slides.append(png)
    # preview strip
    inputs = sum((["-i", str(p)] for p in slides), [])
    chain = "".join(f"[{i}:v]scale=270:338[s{i}];" for i in range(len(slides)))
    chain += "".join(f"[s{i}]" for i in range(len(slides))) + f"hstack=inputs={len(slides)}"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", chain, str(dest / "preview.png")], check=True)
    print(f"{dest.relative_to(ROOT)} · {len(slides)} слайдов · «{data['title'].split('«')[-1].rstrip('»')}»")
    return dest


def main() -> None:
    nums = sys.argv[1:] or list(CAROUSELS)
    for n in nums:
        build(n)


if __name__ == "__main__":
    main()
