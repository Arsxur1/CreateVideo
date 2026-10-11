"""Yafho-Silicare — science posters «зачем пластина и насколько помогает» (4 pages), see SCIENCE.md.

    python projects/yafho/make_posters.py            # → output/yafho/posters/

Pages: why (почему рубец растёт) · how (как работает силикон) · howmuch (насколько помогает)
· care (памятка ухода). Two sizes per page:
    poster_<page>_4x5.png   1080×1350 — Instagram feed / carousel
    poster_<page>_a4.png    2480×3508 — A4 at 300 dpi for clinics
    posters_a4.pdf          all four A4 pages for print
    preview.png             the four 4:5 pages side by side
Text and QR come from code (YafhoPoster.tsx); the illustrations are the same 3D
cross-sections and skin textures the videos use, rendered here at poster size.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
ROOT = PROJECT.parent.parent
sys.path.insert(0, str(PROJECT))
from build_v2 import COMPOSER, qr_matrix, remotion_env  # noqa: E402

OUT = ROOT / "output" / "yafho" / "posters"
PUBLIC = COMPOSER / "public" / "yafho-posters"
PAGES = ["why", "how", "howmuch", "care"]
SIZES = {"4x5": (1080, 1350, 1), "a4": (1240, 1754, 2)}  # css size × scale → 2480×3508 for A4


def remotion_still(comp: str, props: dict, dest: Path, w: int, h: int, scale: int = 1, frame: int = 0) -> None:
    pp = OUT / f".props_{dest.stem}.json"
    pp.write_text(json.dumps(props, ensure_ascii=False), encoding="utf-8")
    subprocess.run(["npx", "remotion", "still", "src/index.tsx", comp, str(dest), f"--props={pp}", f"--width={w}",
                    f"--height={h}", f"--scale={scale}", f"--frame={frame}", "--image-format=png"],
                   cwd=COMPOSER, env=remotion_env(), check=True, capture_output=True)
    pp.unlink()


def illustration(phase: str) -> str:
    """3D cross-section at the end of a story phase, wide crop for the poster picture."""
    dest = PUBLIC / f"xsec_{phase}.png"
    if not dest.exists():
        props = {"theme": "yafho-clinical", "durationSeconds": 4, "backdrop": {"color": "#FFFFFF"},
                 "cuts": [{"id": phase, "source": "", "in_seconds": 0, "out_seconds": 4, "type": "skin_cross_section_3d",
                           "phase": phase, "introFade": False, "fitFrac": 0.92, "centerY": 0.5}]}
        remotion_still("Explainer", props, dest, 2160, 1200, frame=110)
    return f"yafho-posters/{dest.name}"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    images = {"alarm": illustration("alarm"), "seal": illustration("seal"),
              "hyper": "yafho-skin/skin_csection_hyper.png", "soft": "yafho-skin/skin_csection_soft.png"}
    qr = qr_matrix("https://instagram.com/sil.icare")
    made: dict[str, list[Path]] = {k: [] for k in SIZES}
    for i, page in enumerate(PAGES, 1):
        for key, (w, h, scale) in SIZES.items():
            dest = OUT / f"poster_{page}_{key}.png"
            remotion_still("YafhoPoster", {"variant": page, "images": images, "qr": qr, "page": f"{i} / {len(PAGES)}"},
                           dest, w, h, scale)
            made[key].append(dest)
            print(dest.relative_to(ROOT))

    from PIL import Image

    pages = [Image.open(p).convert("RGB") for p in made["a4"]]
    pdf = OUT / "posters_a4.pdf"
    pages[0].save(pdf, save_all=True, append_images=pages[1:], resolution=300)
    thumbs = [Image.open(p).convert("RGB").resize((540, 675)) for p in made["4x5"]]
    sheet = Image.new("RGB", (540 * len(thumbs) + 20 * (len(thumbs) - 1), 675), "#ECE6DD")
    for i, t in enumerate(thumbs):
        sheet.paste(t, (i * 560, 0))
    sheet.save(OUT / "preview.png")
    print(f"{pdf.relative_to(ROOT)} · {len(pages)} стр. A4 · preview.png")


if __name__ == "__main__":
    main()
