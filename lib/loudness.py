"""Two-pass EBU R128 loudness normalisation for finished renders.

Social platforms play everything at roughly -14 LUFS. A render that lands at
-16 or -18 sounds quiet next to other posts, and one-pass loudnorm pumps the
music under narration. Two passes (measure, then apply with the measured
values and ``linear=true``) keep the mix shape and only move the level.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

DEFAULT_TARGET_LUFS = -14.0
DEFAULT_TRUE_PEAK_DB = -1.5
DEFAULT_LRA = 11.0


def measure_loudness(path: str | Path, target_lufs: float = DEFAULT_TARGET_LUFS,
                     true_peak_db: float = DEFAULT_TRUE_PEAK_DB, lra: float = DEFAULT_LRA) -> dict[str, Any]:
    """Run loudnorm in analysis mode and return its JSON stats (input_i, input_tp, ...)."""
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-af",
         f"loudnorm=I={target_lufs}:TP={true_peak_db}:LRA={lra}:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    match = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", proc.stderr, re.S)
    if not match:
        raise RuntimeError(f"loudnorm measurement failed for {path}: {proc.stderr[-400:]}")
    return json.loads(match.group(0))


def normalize_loudness(src: str | Path, dst: str | Path | None = None, *,
                       target_lufs: float = DEFAULT_TARGET_LUFS, true_peak_db: float = DEFAULT_TRUE_PEAK_DB,
                       lra: float = DEFAULT_LRA, audio_bitrate: str = "192k") -> dict[str, Any]:
    """Normalise ``src`` to ``target_lufs``; video stream is copied untouched.

    Writes to ``dst`` (or replaces ``src`` in place when ``dst`` is None) and
    returns ``{"before": {...}, "after": {...}, "output": path}``.
    """
    src = Path(src)
    out = Path(dst) if dst else src.with_name(src.stem + ".loudnorm" + src.suffix)
    before = measure_loudness(src, target_lufs, true_peak_db, lra)
    measured = (f"measured_I={before['input_i']}:measured_TP={before['input_tp']}:"
                f"measured_LRA={before['input_lra']}:measured_thresh={before['input_thresh']}:"
                f"offset={before['target_offset']}")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(src), "-c:v", "copy", "-af",
         f"loudnorm=I={target_lufs}:TP={true_peak_db}:LRA={lra}:{measured}:linear=true,aresample=48000",
         "-c:a", "aac", "-b:a", audio_bitrate, "-movflags", "+faststart", str(out)],
        check=True, capture_output=True,
    )
    if dst is None:
        shutil.move(str(out), str(src))
        out = src
    after = measure_loudness(out, target_lufs, true_peak_db, lra)
    return {"before": before, "after": after, "output": str(out), "target_lufs": target_lufs}
