"""Source media → Remotion public/ (rotation-aware proxies, 4K crops, photos)."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageFilter, ImageOps

VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".mkv"}
PHOTO_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".webp"}


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, capture_output=True)


def slugify(name: str) -> str:
    keep = "".join(c.lower() if c.isalnum() else "-" for c in Path(name).stem)
    return "-".join(p for p in keep.split("-") if p)


def inventory(source_dir: Path) -> dict[str, Any]:
    """Default prep plan for every clip and photo in a source folder."""
    clips, photos = {}, {}
    for path in sorted(source_dir.iterdir()):
        ext = path.suffix.lower()
        if ext in VIDEO_EXTS:
            clips[slugify(path.name)] = {"file": path.name, "grade": ""}
        elif ext in PHOTO_EXTS:
            photos[slugify(path.name)] = {"file": path.name}
    return {"source_dir": str(source_dir), "clips": clips, "photos": photos, "crops": {}}


def make_proxy(src: Path, out: Path, grade: str = "", force: bool = False) -> None:
    """1080x1920 30fps H.264. ffmpeg applies the phone's rotation tag automatically."""
    if out.exists() and not force:
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,hqdn3d=1.5:1.5:3:3"
    if grade:
        vf += "," + grade.lstrip(",")
    _run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-an", "-vf", vf + ",format=yuv420p",
          "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-movflags", "+faststart", str(out)])


def _frame(src: Path, t: float, out: Path) -> Image.Image:
    _run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(src), "-frames:v", "1", str(out)])
    return Image.open(out)


def sharpest_frame_time(src: Path, around: float, window: float = 0.3, step: float = 0.1, tmp: Path | None = None) -> float:
    """Pick the least motion-blurred frame near ``around`` (Laplacian variance)."""
    tmp = tmp or src.with_suffix(".probe.png")
    best_t, best = around, -1.0
    t = max(0.0, around - window)
    while t <= around + window + 1e-6:
        img = _frame(src, t, tmp).convert("L")
        small = np.asarray(img.resize((img.width // 4, img.height // 4)), dtype=np.float32)
        lap = small[1:-1, 1:-1] * 4 - small[:-2, 1:-1] - small[2:, 1:-1] - small[1:-1, :-2] - small[1:-1, 2:]
        score = float(lap.var())
        if score > best:
            best_t, best = t, score
        t += step
    tmp.unlink(missing_ok=True)
    return round(best_t, 2)


def crop_still(src: Path, t: float, box_1080: tuple[float, float, float], out: Path, work: Path) -> dict[str, Any]:
    """Crop a 9:16 box from the full-resolution frame at the sharpest time near ``t``.

    ``box_1080`` is (x, y, width) in 1080-wide coordinates, matching what you
    see in a 1080x1920 proxy frame; height is width * 16/9.
    """
    best_t = sharpest_frame_time(src, t, tmp=work / "_probe.png")
    full = _frame(src, best_t, work / "_full.png").convert("RGB")
    scale = full.width / 1080
    x, y, w = box_1080
    h = w * 16 / 9
    box = tuple(int(round(v * scale)) for v in (x, y, x + w, y + h))
    img = full.crop(box).resize((1080, 1920), Image.LANCZOS)
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, quality=93)
    (work / "_full.png").unlink(missing_ok=True)
    return {"time": best_t, "box_px": box, "upscale": round(1080 / (box[2] - box[0]), 2)}


def prepare_photo(src: Path, out: Path, width: int = 1440) -> None:
    img = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    img = img.resize((width, int(width * img.height / img.width)), Image.LANCZOS)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, quality=92)


def run_prep(plan: dict[str, Any], public_dir: Path, work_dir: Path, force: bool = False) -> list[str]:
    source = Path(plan["source_dir"])
    done = []
    for name, clip in plan.get("clips", {}).items():
        make_proxy(source / clip["file"], public_dir / "video" / f"{name}.mp4", clip.get("grade", ""), force)
        done.append(f"video/{name}.mp4")
    for name, photo in plan.get("photos", {}).items():
        prepare_photo(source / photo["file"], public_dir / "stills" / f"photo-{name}.jpg")
        done.append(f"stills/photo-{name}.jpg")
    work_dir.mkdir(parents=True, exist_ok=True)
    for name, crop in plan.get("crops", {}).items():
        clip_file = plan["clips"][crop["clip"]]["file"]
        info = crop_still(source / clip_file, float(crop["t"]), (crop["x"], crop["y"], crop["w"]),
                          public_dir / "stills" / f"{name}.jpg", work_dir)
        crop["resolved"] = info
        done.append(f"stills/{name}.jpg")
    return done
