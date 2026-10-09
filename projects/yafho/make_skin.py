"""Yafho-Silicare — procedural top-down skin close-ups with healed scars (numpy + PIL, $0).

    python projects/yafho/make_skin.py            # all shapes × states (skips existing)
    python projects/yafho/make_skin.py --force

Writes remotion-composer/public/yafho-skin/skin_<shape>_<state>.png (1600×1600,
60 px per cm, scar centred). States of one and the same scar:

    fresh — young healed scar: pink, slightly raised, smooth and glossy
    hyper — untreated outcome: red, raised, wider ridge (hypertrophic)
    soft  — with silicone: paler, flat, soft — «мягче, светлее, ровнее»

Shapes: line (forearm, after surgery), csection (lower abdomen, horizontal),
burn (back of hand, patch), keloid (shoulder nodule), stria (stretch marks).
Healed scars only — no wounds, crusts or blood (TZ rules). The component
SkinSwatch.tsx mirrors the scar boxes below (SHAPES) to place sheets and
the «+1 см» margin.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / "remotion-composer" / "public" / "yafho-skin"
N = 1600
PX_CM = 60.0
C = N / 2

# light olive skin (TZ: Central Asian woman's hands, light olive skin)
SKIN = np.array([224.0, 189.0, 166.0])
STATES = {
    #        colour of scar tissue, colour alpha, halo alpha, ridge height (px), ridge width × , texture kept, gloss
    "fresh": dict(col=(214, 128, 126), a=0.55, halo=0.16, h=5.0, w=1.0, tex=0.25, gloss=0.55),
    "hyper": dict(col=(178, 82, 94), a=0.76, halo=0.24, h=12.0, w=2.1, tex=0.12, gloss=0.75),
    "soft": dict(col=(238, 210, 194), a=0.50, halo=0.0, h=1.0, w=0.8, tex=0.55, gloss=0.30),
}
# scar boxes in cm (w, h) — mirrored in SkinSwatch.tsx
SHAPES = {
    "line": (0.6, 10.0),
    "csection": (12.0, 1.2),
    "burn": (7.0, 9.0),
    "keloid": (2.2, 1.5),
    "stria": (3.4, 9.0),
}


# --------------------------------------------------------------------------- helpers

def blur(a: np.ndarray, sigma: float) -> np.ndarray:
    """Gaussian blur via FFT (periodic edges are fine for textures)."""
    if sigma <= 0:
        return a
    fy = np.fft.fftfreq(a.shape[0])[:, None]
    fx = np.fft.fftfreq(a.shape[1])[None, :]
    g = np.exp(-2 * (np.pi * sigma) ** 2 * (fx ** 2 + fy ** 2))
    return np.real(np.fft.ifft2(np.fft.fft2(a) * g))


def noise(rng: np.random.Generator, sigma: float) -> np.ndarray:
    n = blur(rng.standard_normal((N, N)), sigma)
    return n / (n.std() + 1e-9)


def cells(rng: np.random.Generator, size: float) -> np.ndarray:
    """Cellular (Voronoi) F2−F1: small near cell borders → skin furrows."""
    g = int(np.ceil(N / size)) + 2
    jit = rng.random((g, g, 2))
    yy, xx = np.mgrid[0:N, 0:N].astype(np.float32)
    cy, cx = (yy // size).astype(int), (xx // size).astype(int)
    f1 = np.full((N, N), 1e9, np.float32)
    f2 = np.full((N, N), 1e9, np.float32)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            ny, nx = np.clip(cy + dy, 0, g - 1), np.clip(cx + dx, 0, g - 1)
            py = (ny + jit[ny, nx, 0]) * size
            px = (nx + jit[ny, nx, 1]) * size
            d = np.hypot(yy - py, xx - px)
            f2 = np.where(d < f1, f1, np.minimum(f2, d))
            f1 = np.minimum(f1, d)
    return f2 - f1


def stroke_layer(paths: list[list[tuple[float, float]]], widths: list[list[float]]) -> np.ndarray:
    """Rasterise tapered strokes (radius per sample) into a 0..1 mask."""
    img = Image.new("L", (N, N), 0)
    d = ImageDraw.Draw(img)
    for pts, ws in zip(paths, widths):
        for (x, y), r in zip(pts, ws):
            d.ellipse([x - r, y - r, x + r, y + r], fill=255)
    return np.asarray(img, np.float32) / 255.0


def curve(p0, p1, bend: float, n: int = 260, wobble: float = 0.0, rng=None) -> list[tuple[float, float]]:
    """Quadratic curve from p0 to p1 (cm, relative to centre), bend in cm, px out."""
    (x0, y0), (x1, y1) = p0, p1
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    lx, ly = x1 - x0, y1 - y0
    ln = np.hypot(lx, ly)
    nx, ny = -ly / ln, lx / ln
    cxp, cyp = mx + nx * bend, my + ny * bend
    t = np.linspace(0, 1, n)
    x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cxp + t ** 2 * x1
    y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cyp + t ** 2 * y1
    if wobble and rng is not None:
        w = np.convolve(rng.standard_normal(n), np.ones(25) / 25, mode="same") * wobble * 4
        x, y = x + nx * w, y + ny * w
    return [(C + a * PX_CM, C + b * PX_CM) for a, b in zip(x, y)]


def taper(n: int, r_mid: float, ends: float = 0.18) -> list[float]:
    t = np.linspace(0, 1, n)
    k = np.clip(np.minimum(t, 1 - t) / ends, 0, 1)
    return list(r_mid * np.sqrt(k) + 0.3)


# --------------------------------------------------------------------------- base skin

def base_skin(rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Albedo (N,N,3), micro-relief height (N,N), hair mask (N,N)."""
    furrow = cells(rng, 7.0)
    relief = -0.45 * np.exp(-(furrow / 1.1) ** 2)
    relief += 0.12 * noise(rng, 0.8) + 0.10 * noise(rng, 4.0)
    # pores
    pores = np.zeros((N, N), np.float32)
    k = int(N * N / 800)
    ys, xs = rng.integers(0, N, k), rng.integers(0, N, k)
    pores[ys, xs] = 1.0
    relief -= 0.75 * blur(pores, 1.1) * (2 * np.pi * 1.3 ** 2)
    relief = blur(relief, 0.8)

    tone = 0.018 * noise(rng, 120) + 0.008 * noise(rng, 30)
    red = 0.015 * noise(rng, 80)
    alb = SKIN[None, None, :] * (1 + tone[..., None])
    alb[..., 0] *= 1 + red
    alb[..., 1] *= 1 + red * 0.3
    # a few faint freckles
    fr = np.zeros((N, N), np.float32)
    k = 70
    fr[rng.integers(0, N, k), rng.integers(0, N, k)] = 1.0
    fr = np.clip(blur(fr, 3.0) * (2 * np.pi * 9) * 0.35, 0, 0.35)
    alb *= 1 - fr[..., None] * np.array([0.18, 0.24, 0.3])

    # fine vellus hair, running along the limb
    hair = Image.new("L", (N, N), 0)
    d = ImageDraw.Draw(hair)
    for _ in range(900):
        x, y = rng.uniform(0, N), rng.uniform(0, N)
        ang = np.deg2rad(rng.normal(100, 12))
        ln = rng.uniform(14, 34)
        d.line([x, y, x + np.cos(ang) * ln, y + np.sin(ang) * ln], fill=int(rng.uniform(70, 150)), width=1)
    hm = blur(np.asarray(hair, np.float32) / 255.0, 0.5)
    return alb, relief, hm


# --------------------------------------------------------------------------- scars

def scar_mask(shape: str, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray, float]:
    """Return (core mask 0..1, longitudinal bump noise, sign of relief: +1 raised, −1 depressed)."""
    if shape == "line":
        p = curve((0.15, -5.0), (-0.15, 5.0), 0.35, wobble=0.04, rng=rng)
        m = stroke_layer([p], [taper(len(p), 0.3 * PX_CM)])
        return m, noise(rng, 16), 1.0
    if shape == "csection":
        p = curve((-6.0, 0.1), (6.0, 0.1), -0.55, wobble=0.04, rng=rng)
        m = stroke_layer([p], [taper(len(p), 0.32 * PX_CM, 0.12)])
        return m, noise(rng, 16), 1.0
    if shape == "keloid":
        img = Image.new("L", (N, N), 0)
        ImageDraw.Draw(img).ellipse([C - 1.1 * PX_CM, C - 0.75 * PX_CM, C + 1.1 * PX_CM, C + 0.75 * PX_CM], fill=255)
        m = blur(np.asarray(img, np.float32) / 255.0, 8)
        return np.clip(m * 1.4, 0, 1), noise(rng, 10) * 0.4, 1.0
    if shape == "stria":
        paths, widths = [], []
        for i, (dx, ln, wd) in enumerate(((-1.5, 3.2, 0.2), (-0.5, 4.4, 0.3), (0.5, 4.0, 0.26), (1.45, 2.8, 0.18))):
            p = curve((dx - 0.25, -ln), (dx + 0.25, ln), 0.35, wobble=0.04, rng=rng)
            paths.append(p)
            widths.append(taper(len(p), wd * PX_CM, 0.35))
        return blur(stroke_layer(paths, widths), 2.5), noise(rng, 12), -1.0
    if shape == "burn":
        img = Image.new("L", (N, N), 0)
        d = ImageDraw.Draw(img)
        for _ in range(26):
            x = rng.normal(0, 1.6) * PX_CM
            y = rng.normal(0, 2.2) * PX_CM
            r = rng.uniform(0.8, 1.7) * PX_CM
            d.ellipse([C + x - r, C + y - r, C + x + r, C + y + r], fill=255)
        m = blur(np.asarray(img, np.float32) / 255.0, 14)
        edge = 0.5 + 0.12 * noise(rng, 18)
        m = np.clip((m - edge) * 5 + 0.5, 0, 1)
        return blur(m, 3), noise(rng, 16), 1.0
    raise ValueError(shape)


def render(shape: str, state: str, base, seed: int) -> Image.Image:
    alb, relief, hair = base
    rng = np.random.default_rng(seed)  # same scar geometry for every state
    core, bumps, sign = scar_mask(shape, rng)
    st = STATES[state]
    if shape == "stria" and state == "soft":
        st = dict(st, col=(242, 228, 220), a=0.55)
    if shape == "stria" and state == "hyper":
        st = dict(st, col=(170, 92, 128), a=0.62, h=3.0)
    if shape == "stria" and state == "fresh":
        st = dict(st, col=(196, 122, 146), h=2.2)

    w = st["w"]
    if w > 1.0 and shape in ("line", "csection", "keloid"):  # untreated scar spreads wider
        core = np.clip(blur(core, 3.5 * w) * 2.4, 0, 1)
    ridge = blur(core, 3.0 * w + 1.0)
    if w > 1.0:  # wider, thicker untreated ridge
        ridge = np.clip(blur(np.clip(core * 1.0, 0, 1), 6.0 * w) * 1.8, 0, 1) * 0.6 + ridge * 0.6
    ridge = np.clip(ridge, 0, 1)
    lumpy = 1 + (0.16 if state == "hyper" else 0.05) * bumps
    if shape == "burn":
        lumpy = 1 + (0.22 if state == "hyper" else 0.08) * bumps
    height = sign * st["h"] * ridge * lumpy
    if shape == "keloid":
        height = st["h"] * 1.6 * blur(core, 10) * lumpy

    colm = np.clip(blur(core, 2.5 * w + 1.5) * 1.15, 0, 1)
    halo = np.clip(blur(core, 22 * w) * 2.2, 0, 1)
    tissue = np.clip(blur(core, 2.0), 0, 1)  # where skin texture is replaced by scar tissue
    if shape == "burn":
        mott = np.clip(0.75 + 0.25 * noise(rng, 7), 0, 1)
        colm = colm * mott

    h_total = relief * (1 - tissue * (1 - st["tex"])) + height
    a = (colm * st["a"] + halo * st["halo"] * (1 - colm))[..., None]
    col = np.array(st["col"], np.float32)[None, None, :]
    albedo = alb * (1 - a) + col * a
    # hair does not grow on scar tissue
    hair_k = hair * (1 - tissue)
    albedo = albedo * (1 - 0.22 * hair_k[..., None])

    # lighting: soft window light from upper left, subtle skin sheen, glossy scar tissue
    gy, gx = np.gradient(h_total)
    nx, ny, nz = -gx * 0.9, -gy * 0.9, np.ones_like(gx)
    inv = 1 / np.sqrt(nx ** 2 + ny ** 2 + nz ** 2)
    nx, ny, nz = nx * inv, ny * inv, nz * inv
    L = np.array([-0.45, -0.55, 0.70])
    L /= np.linalg.norm(L)
    diff = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
    flat = L[2]
    shade = 0.42 + 0.58 * diff / flat
    shade = blur(shade, 0.7)  # skin scatters light a little
    Hh = L + np.array([0, 0, 1.0])
    Hh /= np.linalg.norm(Hh)
    nh = np.clip(nx * Hh[0] + ny * Hh[1] + nz * Hh[2], 0, 1)
    gloss = 0.035 + st["gloss"] * 0.12 * tissue
    spec = (nh ** 60) * gloss * 255
    # limb curvature: gentle falloff towards the left/right edges
    xx = (np.arange(N) - C) / C
    curv = (1 - 0.10 * xx ** 2)[None, :]
    rgb = albedo * shade[..., None] * curv[..., None] + spec[..., None] * np.array([1.0, 0.97, 0.94])
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--shapes", default=",".join(SHAPES))
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    base = None
    for i, shape in enumerate(s.strip() for s in args.shapes.split(",") if s.strip()):
        for state in STATES:
            dest = OUT / f"skin_{shape}_{state}.png"
            if dest.exists() and not args.force:
                continue
            if base is None:
                base = base_skin(np.random.default_rng(7))
            render(shape, state, base, seed=100 + i).save(dest, optimize=True)
            print(f"→ {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
