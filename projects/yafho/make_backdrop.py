"""Yafho-Silicare — brand backdrop until the website art is available.

Procedural warm linen (the same light linen surface as in the Kling shots),
soft window light from the upper left, fine weave and a little grain.
Deterministic, license-free. Replace with real site art by dropping
`assets/brand/backdrop_<w>x<h>.png` (or `backdrop.png`) — the build prefers it.

    python projects/yafho/make_backdrop.py
Output: projects/yafho/assets/brand/backdrop_linen_{1080x1920,1920x1080,1080x1350}.png
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


def write_png(path: Path, img: np.ndarray) -> None:
    h, w, _ = img.shape
    raw = b"".join(b"\x00" + img[y].tobytes() for y in range(h))

    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 6)) + chunk(b"IEND", b"")
    path.write_bytes(png)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for w, h in [(1080, 1920), (1920, 1080), (1080, 1350)]:
        p = OUT / f"backdrop_linen_{w}x{h}.png"
        write_png(p, linen(w, h))
        print(p.relative_to(PROJECT.parent.parent))


if __name__ == "__main__":
    main()
