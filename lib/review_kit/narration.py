"""Narration: one TTS call per line, trim + tempo, stitch onto a timeline."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any


def duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True).stdout
    return float(out.strip())


def synthesize_lines(lines: list[dict[str, Any]], voice: dict[str, Any], out_dir: Path, only: set[str] | None = None) -> list[Path]:
    """Generate ``NN-<id>.mp3`` per line through the TTS selector (provider from the theme voice)."""
    from tools.audio.tts_selector import TTSSelector

    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for i, line in enumerate(lines, 1):
        out = out_dir / f"{i:02d}-{line['id']}.mp3"
        paths.append(out)
        if only is not None and line["id"] not in only:
            continue
        provider = voice.get("provider", "fish_audio")
        # allowed_providers pins the theme's voice: no silent fallback to another provider.
        params = {"preferred_provider": provider, "allowed_providers": [provider], "text": line["text"], "output_path": str(out)}
        for key in ("model", "reference_id", "temperature"):
            if voice.get(key) not in (None, ""):
                params[key] = voice[key]
        result = TTSSelector().execute(params)
        if not result.success:
            raise RuntimeError(f"TTS failed for line {line['id']!r}: {result.error}")
    return paths


def process_line(src: Path, out: Path, tempo: float) -> float:
    """Trim leading/trailing silence and apply tempo (pitch kept). Returns seconds."""
    out.parent.mkdir(parents=True, exist_ok=True)
    trim = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,"
            "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse")
    af = trim + (f",atempo={tempo}" if abs(tempo - 1.0) > 1e-3 else "")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-af", af, "-ar", "48000", "-ac", "1", str(out)],
                   check=True, capture_output=True)
    return duration(out)


def stitch(lines: list[dict[str, Any]], processed: list[Path], out: Path, lead: float, gap: float) -> dict[str, Any]:
    """Place processed lines on one track: ``lead`` seconds in, ``gap`` seconds apart."""
    timeline, t = [], lead
    for line, path in zip(lines, processed):
        d = duration(path)
        timeline.append({"id": line["id"], "file": str(path), "start": round(t, 3), "end": round(t + d, 3)})
        t += d + gap
    total = t - gap
    inputs, filters = [], []
    for i, seg in enumerate(timeline):
        inputs += ["-i", seg["file"]]
        ms = int(seg["start"] * 1000)
        filters.append(f"[{i}]adelay={ms}|{ms}[a{i}]")
    mix = "".join(f"[a{i}]" for i in range(len(timeline)))
    filters.append(f"{mix}amix=inputs={len(timeline)}:normalize=0,apad=pad_dur=1[out]")
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filters), "-map", "[out]",
                    "-ar", "48000", "-ac", "1", "-t", f"{total + 1.0:.2f}", str(out)], check=True, capture_output=True)
    return {"timeline": timeline, "voice_seconds": round(total, 3), "duration_seconds": round(total + 1.0, 2)}
