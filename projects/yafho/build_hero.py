"""Yafho SiliSkin — hero 50s: edit decisions + 9:16 / 16:9 / 4:5 renders.

Usage (from repo root):
    python projects/yafho/build_hero.py               # decisions + all formats + previews
    python projects/yafho/build_hero.py --only 9x16   # one format
    python projects/yafho/build_hero.py --decisions-only

Storyboard and copy come from projects/yafho/TZ.md, section 2. Real shots (R)
are picked up from projects/yafho/assets/kling/H0X.mp4; a missing clip renders
as a "нужен H0X" text card so the cut always builds. Music is the first file in
projects/yafho/assets/music/ (credit it in CREDITS.md). Logo: assets/logo.png.
Budget $0: only the local Remotion renderer (video_compose) and ffmpeg are used.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
ROOT = PROJECT.parent.parent
sys.path.insert(0, str(ROOT))

ASSETS = PROJECT / "assets"
KLING = ASSETS / "kling"
MUSIC = ASSETS / "music"
OUT = ROOT / "output" / "yafho"
DECISIONS = PROJECT / "artifacts" / "edit_decisions_hero.json"

DURATION = 50.0
MUSIC_VOLUME = 0.10  # TZ: 0.08–0.12
INSTAGRAM_URL = "https://instagram.com/sil.icare"

# id, start, end, kind (R = Kling clip, C = code), thesis (TZ.md §2)
SCENES = [
    ("H01", 0, 5, "R", "Рубец остался.\nПлотный и заметный"),
    ("H02", 5, 14, "C", "Под кожей — лишний коллаген"),
    ("H03", 14, 22, "C", "Силикон держит влагу → сигнал ↓"),
    ("H04", 22, 27, "R", "Yafho SiliSkin ·\nмедицинский силикон"),
    ("H05", 27, 32, "R", "1 · Очистить"),
    ("H06", 32, 37, "R", "2 · +1 см за край"),
    ("H07", 37, 41, "R", "3 · 12–23 ч в сутки"),
    ("H08", 41, 46, "R", "Через месяцы —\nмягче, светлее"),
    ("H09", 46, 50, "C", "@sil.icare"),
]

FORMATS = {
    "9x16": {"profile": "instagram_reels", "layout": "full"},
    "16x9": {"profile": "youtube_landscape", "layout": "split"},
    "4x5": {"profile": "instagram_portrait", "layout": "full"},
}


def qr_matrix(url: str) -> list[list[int]]:
    import qrcode

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
    qr.add_data(url)
    qr.make(fit=True)
    return [[int(v) for v in row] for row in qr.get_matrix()]


def first_file(folder: Path, exts: tuple[str, ...]) -> Path | None:
    if not folder.exists():
        return None
    files = sorted(p for p in folder.iterdir() if p.suffix.lower() in exts)
    return files[0] if files else None


def build_decisions(cross_section: str = "3d") -> dict:
    section_type = "skin_cross_section_3d" if cross_section == "3d" else "skin_cross_section"
    cuts: list[dict] = []
    overlays: list[dict] = []
    missing: list[str] = []

    for sid, start, end, kind, thesis in SCENES:
        cut: dict = {"id": sid, "source": "", "in_seconds": start, "out_seconds": end}
        if kind == "R":
            clip = KLING / f"{sid}.mp4"
            if clip.exists():
                cut["source"] = str(clip)
            else:
                missing.append(sid)
                cut.update(type="text_card", text=f"нужен {sid}", fontSize=48,
                           color="#0F2440", backgroundColor="#ECE6DD")
        elif sid == "H02":
            cut.update(type=section_type, phase="scar")
        elif sid == "H03":
            cut.update(type=section_type, phase="sealed", introFade=False)
        elif sid == "H09":
            logo = ASSETS / "logo.png"
            cut.update(type="end_card", brand="Yafho SiliSkin", handle="@sil.icare",
                       qr=qr_matrix(INSTAGRAM_URL), qrCaption="instagram.com/sil.icare")
            if logo.exists():
                cut["logoSrc"] = str(logo)
        cuts.append(cut)

        thesis_overlay = {"type": "thesis", "text": thesis, "variant": "dark",
                          "in_seconds": start + 0.3, "out_seconds": end}
        if sid == "H09":
            # The end card already shows the handle; only the 16:9 side panel repeats it.
            thesis_overlay["layouts"] = ["split"]
        overlays.append(thesis_overlay)

    overlays.append({"type": "margin_overlay", "label": "+1 см", "in_seconds": 32.6, "out_seconds": 37})
    overlays.append({"type": "time_counter", "labels": ["2 нед", "1 мес", "3 мес", "6 мес"],
                     "in_seconds": 41.2, "out_seconds": 46})

    audio: dict = {}
    track = first_file(MUSIC, (".mp3", ".wav", ".m4a", ".aac", ".ogg"))
    if track:
        audio["music"] = {"src": str(track), "volume": MUSIC_VOLUME, "fadeInSeconds": 1.5,
                          "fadeOutSeconds": 2.5, "loop": True}

    return {
        "version": "1.0",
        "renderer_family": "explainer-data",
        "render_runtime": "remotion",
        "playbook": "yafho-clinical",
        "theme": "yafho-clinical",
        "durationSeconds": DURATION,
        "cuts": cuts,
        "overlays": overlays,
        "audio": audio,
        "metadata": {
            "project": "yafho",
            "video": "hero",
            "source_of_truth": "projects/yafho/TZ.md §2",
            "missing_kling_clips": missing,
            "music": str(track.name) if track else None,
            "cross_section": cross_section,
        },
    }


def render(decisions: dict, fmt: str) -> Path:
    from tools.video.video_compose import VideoCompose

    spec = FORMATS[fmt]
    props = dict(decisions, layout=spec["layout"])
    out = OUT / f"hero_{fmt}.mp4"
    result = VideoCompose().execute({
        "operation": "remotion_render",
        "edit_decisions": props,
        "output_path": str(out),
        "profile": spec["profile"],
    })
    if not result.success:
        raise SystemExit(f"[{fmt}] render failed: {result.error}")
    return out


def previews(video: Path, fmt: str) -> None:
    folder = OUT / "previews"
    folder.mkdir(parents=True, exist_ok=True)
    frames = []
    for sid, start, end, _, _ in SCENES:
        t = start + (end - start) * 0.7
        png = folder / f"{fmt}_{sid}.png"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(video),
                        "-frames:v", "1", str(png)], check=True)
        frames.append(png)
    # contact sheet: 9 frames in a row, scaled to 360px tall
    inputs = sum((["-i", str(p)] for p in frames), [])
    chain = "".join(f"[{i}:v]scale=-2:360[s{i}];" for i in range(len(frames)))
    chain += "".join(f"[s{i}]" for i in range(len(frames))) + f"hstack=inputs={len(frames)}"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", chain,
                    str(folder / f"{fmt}_sheet.png")], check=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", choices=sorted(FORMATS), action="append")
    ap.add_argument("--decisions-only", action="store_true")
    ap.add_argument("--cross-section", choices=["3d", "2d"], default="3d",
                    help="H02/H03: Three.js 3D cutaway (default) or the flat 2D diagram")
    args = ap.parse_args()
    # Three.js needs a WebGL backend in headless Chrome.
    os.environ.setdefault("REMOTION_GL", "angle")

    decisions = build_decisions(args.cross_section)
    DECISIONS.parent.mkdir(parents=True, exist_ok=True)
    DECISIONS.write_text(json.dumps(decisions, ensure_ascii=False, indent=2), encoding="utf-8")
    missing = decisions["metadata"]["missing_kling_clips"]
    print(f"edit decisions → {DECISIONS.relative_to(ROOT)}")
    print(f"Kling clips missing (placeholders): {', '.join(missing) or 'none'}")
    print(f"music: {decisions['metadata']['music'] or 'none — add a track to assets/music/'}")
    if args.decisions_only:
        return

    OUT.mkdir(parents=True, exist_ok=True)
    for fmt in args.only or list(FORMATS):
        video = render(decisions, fmt)
        previews(video, fmt)
        print(f"[{fmt}] {video.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
