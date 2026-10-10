"""Yafho-Silicare — YouTube / VK thumbnails 1280×720.

    python projects/yafho/make_thumbs.py      # → output/yafho/thumbs/<video>.jpg

· topics and hero: the 16:9 frame at the topic's `cover_at` (hook title on screen), scaled to 1280×720
· long guide: its own still rendered in Remotion — effect comparison on the left,
  big title on the right (text from code, brand palette).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
ROOT = PROJECT.parent.parent
OUT = ROOT / "output" / "yafho" / "thumbs"
sys.path.insert(0, str(PROJECT))


def frame(video: Path, t: float, dest: Path) -> None:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(video), "-frames:v", "1",
                    "-vf", "scale=1280:720", "-q:v", "3", str(dest)], check=True)


def guide_thumb(dest: Path) -> None:
    import build_v2 as b

    data = {"backdrop": "linen", "public_dir": "yafho-longform"}
    b.configure(PROJECT / "guide.json", data)
    props = {
        # full 16:9 canvas: the two outcomes side by side, one big title — readable at thumbnail size
        "theme": "yafho-clinical", "durationSeconds": 2, "layout": "full",
        "cuts": [{"id": "cmp", "source": "", "in_seconds": 0, "out_seconds": 2, "type": "skin_demo", "skinShape": "csection",
                  "skinStep": "compare", "progressFrom": 1, "progressTo": 1, "introFade": False,
                  "areaTop": 0.04, "areaBottom": 0.62}],
        "overlays": [{"type": "thesis", "text": "Рубец: два исхода. Гид за 4 минуты", "variant": "dark",
                      "fontSize": 84, "in_seconds": 0, "out_seconds": 2}],
    }
    bd = b.backdrop_for(data, (1920, 1080))
    if bd:
        props["backdrop"] = {"image": bd}
    pp = OUT / "_guide_props.json"
    pp.write_text(json.dumps(props, ensure_ascii=False), encoding="utf-8")
    png = OUT / "_guide.png"
    subprocess.run(["npx", "remotion", "still", "src/index.tsx", "Explainer", str(png), f"--props={pp}", "--frame=40",
                    "--width=1920", "--height=1080"], cwd=b.COMPOSER, env=b.remotion_env(), check=True, capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(png), "-vf", "scale=1280:720", "-q:v", "3", str(dest)], check=True)
    pp.unlink()
    png.unlink()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    n = 0
    hero = ROOT / "output" / "yafho" / "v4" / "hero_v4_16x9.mp4"
    if hero.exists():
        frame(hero, 2.2, OUT / "hero_v4.jpg")
        n += 1
    for f in sorted((PROJECT / "topics").glob("topic_*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        video = ROOT / "output" / "yafho" / "topics" / f"{f.stem}_16x9.mp4"
        if video.exists():
            frame(video, float(data.get("cover_at", 2.0)), OUT / f"{f.stem}.jpg")
            n += 1
    guide_thumb(OUT / "guide_16x9.jpg")
    n += 1
    print(f"{OUT.relative_to(ROOT)} · {n} обложек 1280×720")


if __name__ == "__main__":
    main()
