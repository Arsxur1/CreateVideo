"""Yafho-Silicare — in-house ambient score for hero v2 (no third-party license).

Synthesised from scratch with numpy, scored to the story acts in hero_v2.json:

    1 hook        low drone + a single bell
    2 backstory   soft minor pads (Am–F–C–G), slow heartbeat pulse
    3 alarm       denser (Dm–Am–Esus–E), pulse on every beat, ticking speeds up
    4 window      everything holds on a thin high pad, then a riser
    5–7 solution  resolves to major (C–G–Am–F …), warm plucked arpeggio
    8 end card    Cadd9 swell and fade

plus quiet sound accents: whoosh on the dive into 3D, a click on the
"window", a chime when the product appears, a soft touch when the sheet lands.

88 BPM · 48 kHz stereo · mastered to about -18 LUFS (calm background level).

Usage (from repo root):
    python projects/yafho/make_music.py
Output: projects/yafho/assets/music/yafho_ambient_v2.wav
"""

from __future__ import annotations

import json
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np

PROJECT = Path(__file__).resolve().parent
OUT = PROJECT / "assets" / "music" / "yafho_ambient_v2.wav"
SR = 48_000
BPM = 88
BEAT = 60 / BPM
rng = np.random.default_rng(20261007)


def hz(midi: float) -> float:
    return 440.0 * 2 ** ((midi - 69) / 12)


def note(name: str) -> int:
    names = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
    pitch, octave = name[:-1], int(name[-1])
    return 12 * (octave + 1) + names[pitch]


CHORDS = {
    "Am": ["A2", "E3", "A3", "C4", "E4"],
    "F": ["F2", "C3", "F3", "A3", "C4"],
    "C": ["C3", "G3", "C4", "E4", "G4"],
    "G": ["G2", "D3", "G3", "B3", "D4"],
    "Dm": ["D3", "A3", "D4", "F4", "A4"],
    "Esus": ["E2", "B2", "E3", "A3", "B3"],
    "E": ["E2", "B2", "E3", "G#3", "B3"],
    "Ahigh": ["A4", "B4", "E5"],
    "Cadd9": ["C3", "G3", "D4", "E4", "G4"],
}


def acts(data: dict) -> dict[int, tuple[float, float]]:
    out: dict[int, tuple[float, float]] = {}
    for s in data["scenes"]:
        a = s["act"]
        lo, hi = out.get(a, (s["start"], s["end"]))
        out[a] = (min(lo, s["start"]), max(hi, s["end"]))
    return out


def env(n: int, attack: float, release: float) -> np.ndarray:
    a = min(n, int(attack * SR))
    r = min(n - a, int(release * SR))
    e = np.ones(n)
    if a:
        e[:a] = np.sin(np.linspace(0, np.pi / 2, a)) ** 2
    if r:
        e[n - r:] = np.cos(np.linspace(0, np.pi / 2, r)) ** 2
    return e


def place(buf: np.ndarray, sig: np.ndarray, t: float, gain: float = 1.0, pan: float = 0.0) -> None:
    i = int(t * SR)
    if i >= buf.shape[1]:
        return
    sig = sig[: buf.shape[1] - i]
    left, right = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    buf[0, i:i + len(sig)] += sig * gain * left
    buf[1, i:i + len(sig)] += sig * gain * right


def pad_voice(f: float, dur: float, bright: float) -> np.ndarray:
    """Detuned additive 'saw' with soft harmonic roll-off (warm pad)."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = np.zeros(n)
    for det in (-0.12, 0.0, 0.11):
        ff = f * 2 ** (det / 12)
        ph = rng.uniform(0, 2 * np.pi)
        for h in range(1, 7):
            if ff * h > 6000:
                break
            sig += np.sin(2 * np.pi * ff * h * t + ph * h) / (h ** (2.2 - bright))
    # slow movement
    sig *= 0.85 + 0.15 * np.sin(2 * np.pi * 0.17 * t + rng.uniform(0, 6))
    return sig / 3


def chord(buf, name, t0, dur, gain, bright=0.4, attack=1.2, release=1.6):
    for i, nm in enumerate(CHORDS[name]):
        v = pad_voice(hz(note(nm)), dur + release, bright) * env(int((dur + release) * SR), attack, release)
        place(buf, v, t0, gain / len(CHORDS[name]), pan=(i / max(1, len(CHORDS[name]) - 1) - 0.5) * 0.6)


def pluck(f: float, dur: float = 1.4) -> np.ndarray:
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) + 0.12 * np.sin(2 * np.pi * 3 * f * t)
    return sig * np.exp(-t * 3.2) * env(n, 0.004, 0.2)


def bell(f: float, dur: float = 3.5) -> np.ndarray:
    n = int(dur * SR)
    t = np.arange(n) / SR
    partials = [(1, 1.0, 1.0), (2.76, 0.45, 1.8), (5.4, 0.25, 3.0), (8.9, 0.12, 4.5)]
    sig = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * d) for r, a, d in partials)
    return sig * env(n, 0.002, 0.5)


def thump(dur: float = 0.5) -> np.ndarray:
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 62 * np.exp(-t * 6) + 42
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def fft_filter(sig: np.ndarray, lo: float | None = None, hi: float | None = None) -> np.ndarray:
    spec = np.fft.rfft(sig)
    freqs = np.fft.rfftfreq(len(sig), 1 / SR)
    mask = np.ones_like(freqs)
    if hi:
        mask *= 1 / (1 + (freqs / hi) ** 4)
    if lo:
        mask *= 1 / (1 + (lo / np.maximum(freqs, 1)) ** 4)
    return np.fft.irfft(spec * mask, len(sig))


def tick(dur: float = 0.06) -> np.ndarray:
    n = int(dur * SR)
    noise = fft_filter(rng.normal(size=n), lo=3500, hi=9000)
    return noise * np.exp(-np.arange(n) / SR * 60)


def whoosh(dur: float, rising: bool = True) -> np.ndarray:
    """Noise sweep: crossfade from a dark to a bright band (or back)."""
    n = int(dur * SR)
    noise = rng.normal(size=n)
    dark = fft_filter(noise, lo=150, hi=900)
    bright = fft_filter(noise, lo=1200, hi=6000)
    x = np.linspace(0, 1, n)
    mix = x if rising else 1 - x
    shape = np.sin(np.pi * x) ** 1.5
    return (dark * (1 - mix) + bright * mix) * shape


def reverb(buf: np.ndarray, seconds: float = 2.8, wet: float = 0.32) -> np.ndarray:
    n_ir = int(seconds * SR)
    t = np.arange(n_ir) / SR
    out = np.empty_like(buf)
    for ch in range(2):
        ir = rng.normal(size=n_ir) * np.exp(-t * 2.3)
        ir = fft_filter(ir, lo=120, hi=5500)
        ir /= np.sqrt(np.sum(ir ** 2))
        size = 1 << int(np.ceil(np.log2(buf.shape[1] + n_ir)))
        conv = np.fft.irfft(np.fft.rfft(buf[ch], size) * np.fft.rfft(ir, size), size)[: buf.shape[1]]
        out[ch] = buf[ch] * (1 - wet) + conv * wet
    return out


def compose(data: dict) -> np.ndarray:
    total = float(data["duration"])
    buf = np.zeros((2, int(total * SR)))
    A = acts(data)

    # 1 · hook — drone + bell
    a0, a1 = A[1]
    for m in ("A1", "E2"):
        d = pad_voice(hz(note(m)), a1 - a0 + 1.5, 0.1) * env(int((a1 - a0 + 1.5) * SR), 1.5, 1.5)
        place(buf, d, a0, 0.22)
    place(buf, bell(hz(note("A4"))), a0 + 0.4, 0.10, pan=-0.2)
    place(buf, bell(hz(note("E5"))), a0 + 2.6, 0.07, pan=0.25)

    # 2 · backstory — Am F C G, heartbeat on beats 1 & 3
    s, e = A[2]
    seq = ["Am", "F", "C", "G"]
    step = (e - s) / len(seq)
    for i, c in enumerate(seq):
        chord(buf, c, s + i * step, step, 0.55, bright=0.35)
    t = s + BEAT
    while t < e:
        place(buf, thump(), t, 0.30)
        t += 2 * BEAT

    # 3 · alarm — Dm Am Esus E, pulse every beat, ticks 8ths → 16ths
    s, e = A[3]
    seq = ["Dm", "Am", "Esus", "E"]
    step = (e - s) / len(seq)
    for i, c in enumerate(seq):
        chord(buf, c, s + i * step, step, 0.62, bright=0.6, attack=0.6)
    t = s
    while t < e:
        place(buf, thump(), t, 0.36)
        t += BEAT
    t = s
    while t < e:
        p = (t - s) / (e - s)
        place(buf, tick(), t, 0.05 + 0.07 * p, pan=float(rng.uniform(-0.5, 0.5)))
        t += BEAT / (2 if p < 0.5 else 4)

    # 4 · window — thin high pad, click, riser into the solution
    s, e = A[4]
    chord(buf, "Ahigh", s, e - s, 0.30, bright=0.2, attack=0.8, release=1.0)
    place(buf, tick(0.08), s + 0.25, 0.25)
    place(buf, whoosh(e - s - 2.0 + 1.0, rising=True), s + 2.0, 0.10)

    # 5–7 · solution, steps, result — major, warm arpeggio, soft pulse per bar
    plan = [(5, ["C", "G", "Am", "F"]), (6, ["C", "G", "F", "C"]), (7, ["F", "G", "C"])]
    for act, seq in plan:
        s, e = A[act]
        step = (e - s) / len(seq)
        for i, c in enumerate(seq):
            chord(buf, c, s + i * step, step, 0.5, bright=0.55, attack=0.5 if act == 5 and i == 0 else 0.9)
            tones = [note(n) + 12 for n in CHORDS[c][1:4]]
            t = s + i * step
            k = 0
            while t < s + (i + 1) * step - 0.05:
                place(buf, pluck(hz(tones[k % len(tones)] + (12 if k % 4 == 3 else 0))), t, 0.06,
                      pan=0.35 * np.sin(k))
                t += BEAT / 2
                k += 1
        t = s
        while t < e:
            place(buf, thump(), t, 0.20)
            t += 4 * BEAT
    s5 = A[5][0]
    place(buf, bell(hz(note("C5"))), s5 + 0.05, 0.10)
    place(buf, bell(hz(note("G5"))), s5 + 0.25, 0.06, pan=0.3)

    # 8 · end card — Cadd9 swell and fade
    s, e = A[8]
    chord(buf, "Cadd9", s, e - s, 0.55, bright=0.45, attack=0.8, release=2.5)
    place(buf, bell(hz(note("E5"))), s + 0.3, 0.08)

    # accents tied to scenes
    sc = {x["id"]: x for x in data["scenes"]}
    dive = sc["S02"]["start"]
    place(buf, whoosh(1.6, rising=False), dive - 0.8, 0.16)  # dive into the skin
    land = sc["S10"]["start"] + 0.32 * (sc["S10"]["end"] - sc["S10"]["start"])
    place(buf, thump(0.4), land, 0.22)  # sheet touches the skin
    place(buf, fft_filter(rng.normal(size=int(0.25 * SR)), lo=200, hi=1500) * np.exp(-np.arange(int(0.25 * SR)) / SR * 14), land, 0.05)

    # master: reverb, gentle fades, peak safety
    buf = reverb(buf)
    buf *= env(buf.shape[1], 0.6, 2.2)
    buf /= np.max(np.abs(buf)) + 1e-9
    return buf * 0.7


def write_wav(path: Path, buf: np.ndarray) -> None:
    pcm = (np.clip(buf.T, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def loudnorm(src: Path, dst: Path, target: float = -18.0) -> str:
    """Two-pass EBU R128 normalisation with ffmpeg; returns the measured integrated loudness."""
    flt = f"loudnorm=I={target}:TP=-1.5:LRA=11"
    first = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(src), "-af", flt + ":print_format=json", "-f", "null", "-"],
                           capture_output=True, text=True)
    m = json.loads(first.stderr[first.stderr.rindex("{"):first.stderr.rindex("}") + 1])
    second = (f"{flt}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
              f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-af", second, "-ar", str(SR), str(dst)], check=True)
    return m["input_i"]


def main() -> None:
    data = json.loads((PROJECT / "hero_v2.json").read_text(encoding="utf-8"))
    buf = compose(data)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp) / "raw.wav"
        write_wav(raw, buf)
        measured = loudnorm(raw, OUT)
    print(f"{OUT.relative_to(PROJECT.parent.parent)} · {data['duration']} s · raw {measured} LUFS → -18 LUFS")


if __name__ == "__main__":
    main()
