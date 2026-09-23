"""Small deterministic sound effects, synthesised locally (no licence to track).

bloom  - soft rising pad, for a reveal
pop    - low punch, for a price or number slam
whoosh - filtered noise sweep, for fast cuts
tick   - short click, for list items and checks
"""
from __future__ import annotations

import math
import wave
from pathlib import Path

import numpy as np

SR = 48000


def _write(path: Path, signal: np.ndarray) -> None:
    signal = np.clip(signal, -1, 1)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((signal * 32000).astype("<i2").tobytes())


def _envelope(n: int, attack: float, release: float) -> np.ndarray:
    env = np.ones(n)
    a, r = int(attack * SR), int(release * SR)
    env[:a] = np.linspace(0, 1, a) ** 2
    env[-r:] = np.linspace(1, 0, r) ** 2
    return env


def _lowpass(x: np.ndarray, alpha: np.ndarray | float) -> np.ndarray:
    alphas = np.broadcast_to(alpha, x.shape)
    y = np.empty_like(x)
    acc = 0.0
    for i, (v, a) in enumerate(zip(x, alphas)):
        acc += a * (v - acc)
        y[i] = acc
    return y


def write_all(out_dir: Path, seed: int = 7) -> list[str]:
    rng = np.random.default_rng(seed)

    n = int(0.45 * SR)
    sweep = np.linspace(0.02, 0.35, n) * np.sin(np.linspace(0, math.pi, n)) + 0.01
    _write(out_dir / "whoosh.wav", _lowpass(rng.standard_normal(n), sweep) * _envelope(n, 0.2, 0.2) * 0.9)

    n = int(0.07 * SR)
    t = np.arange(n) / SR
    _write(out_dir / "tick.wav", np.sin(2 * math.pi * 1900 * t) * np.exp(-t * 70) * 0.5)

    n = int(1.6 * SR)
    t = np.arange(n) / SR
    pad = sum(np.sin(2 * math.pi * f * t) for f in (220, 330, 440, 660)) / 4
    _write(out_dir / "bloom.wav", pad * _envelope(n, 0.9, 0.6) * 0.35
           + _lowpass(rng.standard_normal(n), 0.05) * _envelope(n, 1.0, 0.5) * 0.25)

    n = int(0.25 * SR)
    t = np.arange(n) / SR
    _write(out_dir / "pop.wav", np.sin(2 * math.pi * (140 - 80 * t / 0.25) * t) * np.exp(-t * 18) * 0.9)
    return ["bloom", "pop", "whoosh", "tick"]
