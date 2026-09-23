"""Caption timing: one caption chunk per spoken sentence, snapped to real pauses.

Works across languages: the voice can be Tamil while captions are English,
because timing comes from the audio's pauses and the spoken sentence lengths,
not from matching words.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any

SENTENCE_END = re.compile(r"(?<=[.?!।])\s+")


def pause_midpoints(path: Path, noise_db: float = -38, min_silence: float = 0.18) -> list[float]:
    err = subprocess.run(["ffmpeg", "-i", str(path), "-af", f"silencedetect=n={noise_db}dB:d={min_silence}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", err)]
    return [(a + b) / 2 for a, b in zip(starts, ends)]


def split_long(text: str, start: float, end: float, max_chars: int) -> list[tuple[str, float, float]]:
    """Split a caption over ``max_chars`` at the punctuation nearest its middle; time shared by length."""
    if len(text) <= max_chars:
        return [(text, start, end)]
    cuts = [m.end() for m in re.finditer(r"[,.?!]\s", text)]
    if not cuts:
        return [(text, start, end)]
    cut = min(cuts, key=lambda c: abs(c - len(text) / 2))
    left, right = text[:cut].strip(), text[cut:].strip()
    mid = start + (end - start) * len(left) / (len(left) + len(right))
    return split_long(left, start, mid, max_chars) + split_long(right, mid, end, max_chars)


def boundaries(spoken: str, n_chunks: int, seg_seconds: float, pauses: list[float], snap_window: float = 1.2) -> list[float]:
    """Where to switch captions inside one line: expected by sentence length, snapped to a pause."""
    parts = [p for p in SENTENCE_END.split(spoken.strip()) if p.strip()]
    if len(parts) != n_chunks:
        parts = [spoken] * n_chunks
    lengths = [len(p) for p in parts]
    total = sum(lengths)
    expected, acc = [], 0
    for length in lengths[:-1]:
        acc += length
        expected.append(acc / total * seg_seconds)
    snapped = []
    for e in expected:
        pick = min(pauses, key=lambda p: abs(p - e)) if pauses else e
        snapped.append(pick if abs(pick - e) <= snap_window else e)
    return sorted(snapped)


def time_captions(lines: list[dict[str, Any]], timeline: list[dict[str, Any]], max_chars: int = 52) -> list[dict[str, Any]]:
    captions = []
    for line, seg in zip(lines, timeline):
        chunks = line.get("captions") or []
        if not chunks:
            continue
        seg_seconds = seg["end"] - seg["start"]
        edges = [0.0] + boundaries(line["text"], len(chunks), seg_seconds, pause_midpoints(Path(seg["file"]))) + [seg_seconds]
        for i, chunk in enumerate(chunks):
            a, b = seg["start"] + edges[i], seg["start"] + edges[i + 1]
            for text, pa, pb in split_long(chunk, a, b, max_chars):
                captions.append({"text": text, "start": round(pa, 3), "end": round(pb, 3), "line": line["id"]})
    return captions


def _ts(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def to_srt(captions: list[dict[str, Any]], offset: float = 0.0) -> str:
    return "\n".join(f"{i}\n{_ts(c['start'] + offset)} --> {_ts(c['end'] + offset)}\n{c['text']}\n"
                     for i, c in enumerate(captions, 1))
