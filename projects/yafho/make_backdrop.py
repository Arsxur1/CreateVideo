"""Yafho-Silicare — brand backdrops until the website art is available.

Four procedural options in the brand palette (flat textures, no gradients or neon):
    linen   warm linen, soft window light (the surface of the Kling shots) — current default
    clinic  off-white medical sheet with a faint navy dot grid
    sand    beige matte paper (#ECE6DD)
    sheets  light ground with faint outlines of silicone sheets — the product's own motif
Deterministic, license-free. Real site art always wins: drop
`assets/brand/backdrop_<w>x<h>.png` (or `backdrop.png`) and the build prefers it.
Choose an option for every video with `"backdrop": "<kind>"` in the scene files or
`YAFHO_BACKDROP=<kind>` for one build.

    python projects/yafho/make_backdrop.py                 # all kinds, all sizes
    python projects/yafho/make_backdrop.py --kinds sand    # one kind
Output: projects/yafho/assets/brand/backdrop_<kind>_<w>x<h>.png
"""

from __future__ import annotations

import zlib
import struct
from pathlib import Path

import numpy as np

PROJECT = Path(__file__).resolve().parent
OUT = PROJECT / "assets" / "brand"
BASE = np.array([0xEF, 0xE9, 0xE0], dtype=np.float32)  # warm linen, between #FBFAF7 and #ECE6DD


def smooth_noise(h: int, w: int, scale: int, rng: np.random.Generator) -> np.ndarray:
    small = rng.normal(size=(h // scale + 2, w // scale + 2)).astype(np.float32)
    ys = np.linspace(0, small.shape[0] - 1.001, h)
    xs = np.linspace(0, small.shape[1] - 1.001, w)
    y0, x0 = ys.astype(int), xs.astype(int)
    fy, fx = (ys - y0)[:, None], (xs - x0)[None, :]
    a = small[y0][:, x0]
    b = small[y0][:, x0 + 1]
    c = small[y0 + 1][:, x0]
    d = small[y0 + 1][:, x0 + 1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def linen(w: int, h: int, seed: int = 7) -> np.ndarray:
    rng = np.random.default_rng(seed)
    # weave: thin horizontal and vertical threads with slub variation
    rows = smooth_noise(h, 1, 3, rng)[:, :1] * 0.6 + rng.normal(size=(h, 1)).astype(np.float32) * 0.5
    cols = smooth_noise(1, w, 3, rng)[:1, :] * 0.6 + rng.normal(size=(1, w)).astype(np.float32) * 0.5
    weave = rows * 2.2 + cols * 2.2
    slub = smooth_noise(h, w, 90, rng) * 2.5
    grain = rng.normal(size=(h, w)).astype(np.float32) * 1.4
    # soft window light: brighter upper left, gentle falloff (very subtle)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt((xx / w + 0.15) ** 2 + (yy / h + 0.1) ** 2)
    light = (0.5 - d) * 14
    lum = weave + slub + grain + light
    img = BASE[None, None, :] + lum[..., None] * np.array([1.0, 0.96, 0.9], dtype=np.float32)
    return np.clip(img, 0, 255).astype(np.uint8)


def _grain(rng: np.random.Generator, h: int, w: int, amount: float) -> np.ndarray:
    return rng.normal(size=(h, w)).astype(np.float32) * amount + smooth_noise(h, w, 120, rng) * amount * 1.2


def clinic(w: int, h: int, seed: int = 11) -> np.ndarray:
    """Off-white sheet (#FBFAF7) with a faint navy dot grid, 1 dot per 36 px, and fine paper grain."""
    rng = np.random.default_rng(seed)
    base = np.array([0xFB, 0xFA, 0xF7], dtype=np.float32)
    img = base[None, None, :] + _grain(rng, h, w, 0.9)[..., None]
    step = 36
    yy, xx = np.mgrid[0:h, 0:w]
    dx = (xx % step) - step / 2
    dy = (yy % step) - step / 2
    dot = np.clip(2.4 - np.sqrt(dx * dx + dy * dy), 0, 1)
    navy = np.array([0x0F, 0x24, 0x40], dtype=np.float32)
    a = (dot * 0.2)[..., None]
    img = img * (1 - a) + navy[None, None, :] * a
    return np.clip(img, 0, 255).astype(np.uint8)


def sand(w: int, h: int, seed: int = 13) -> np.ndarray:
    """Beige matte paper (#ECE6DD) with soft fibre grain."""
    rng = np.random.default_rng(seed)
    base = np.array([0xEC, 0xE6, 0xDD], dtype=np.float32)
    fibre = smooth_noise(h, w, 6, rng) * 1.2 + smooth_noise(h, w, 40, rng) * 1.6
    lum = fibre + rng.normal(size=(h, w)).astype(np.float32) * 1.3
    img = base[None, None, :] + lum[..., None] * np.array([1.0, 0.97, 0.93], dtype=np.float32)
    return np.clip(img, 0, 255).astype(np.uint8)


def sheets(w: int, h: int, seed: int = 17) -> np.ndarray:
    """Light ground (#F6F7F5) with faint outlines of rounded silicone sheets in brand teal, scattered and tilted."""
    from PIL import Image, ImageDraw

    rng = np.random.default_rng(seed)
    base = np.array([0xF6, 0xF7, 0xF5], dtype=np.float32)
    img = base[None, None, :] + _grain(rng, h, w, 0.8)[..., None]
    S = 2  # supersample for smooth outlines
    layer = Image.new("L", (w * S, h * S), 0)
    d = ImageDraw.Draw(layer)
    unit = min(w, h) / 9.0  # ≈ 1 cm at phone scale
    sizes = [(4, 4), (4, 13), (5, 15), (10, 15)]  # TZ sheet sizes, cm
    cells = int(w * h / (unit * unit * 22)) + 4
    for _ in range(cells):
        sw, sh = sizes[rng.integers(len(sizes))]
        k = rng.uniform(0.35, 0.6)
        bw, bh = sw * unit * k * S, sh * unit * k * S
        cx, cy = rng.uniform(-0.05, 1.05) * w * S, rng.uniform(-0.05, 1.05) * h * S
        ang = np.deg2rad(rng.uniform(-35, 35))
        tile = Image.new("L", (int(bw + 8 * S), int(bh + 8 * S)), 0)
        ImageDraw.Draw(tile).rounded_rectangle([4 * S, 4 * S, bw + 4 * S, bh + 4 * S], radius=int(0.5 * unit * k * S),
                                                outline=255, width=int(2.2 * S))
        tile = tile.rotate(np.rad2deg(ang), expand=True, resample=Image.BICUBIC)
        layer.paste(255, (int(cx - tile.width / 2), int(cy - tile.height / 2)), tile)
    m = np.asarray(layer.resize((w, h), Image.LANCZOS), np.float32) / 255.0
    teal = np.array([0x0D, 0x94, 0x88], dtype=np.float32)
    a = (m * 0.10)[..., None]
    img = img * (1 - a) + teal[None, None, :] * a
    return np.clip(img, 0, 255).astype(np.uint8)


KINDS = {"linen": linen, "clinic": clinic, "sand": sand, "sheets": sheets}
SIZES = [(1080, 1920), (1920, 1080), (1080, 1350), (1080, 1080)]


def write_png(path: Path, img: np.ndarray) -> None:
    h, w, _ = img.shape
    raw = b"".join(b"\x00" + img[y].tobytes() for y in range(h))

    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 6)) + chunk(b"IEND", b"")
    path.write_bytes(png)


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kinds", default=",".join(KINDS))
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    for kind in [k.strip() for k in args.kinds.split(",") if k.strip()]:
        for w, h in SIZES:
            p = OUT / f"backdrop_{kind}_{w}x{h}.png"
            write_png(p, KINDS[kind](w, h))
            print(p.relative_to(PROJECT.parent.parent))


if __name__ == "__main__":
    main()
