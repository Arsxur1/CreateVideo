"""Post-render checks a person would otherwise do by hand."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

from lib.loudness import measure_loudness


def _stderr(cmd: list[str]) -> str:
    return subprocess.run(cmd, capture_output=True, text=True).stderr


def review_video(video: Path, sheet: Path | None = None, every_seconds: float = 2.0) -> dict[str, Any]:
    probe = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate",
         "-of", "json", str(video)], capture_output=True, text=True).stdout)
    loud = measure_loudness(video)
    black = re.findall(r"black_start:([0-9.]+) black_end:([0-9.]+)",
                       _stderr(["ffmpeg", "-i", str(video), "-vf", "blackdetect=d=0.3:pix_th=0.06", "-an", "-f", "null", "-"]))
    silence = re.findall(r"silence_start: ([0-9.]+)",
                         _stderr(["ffmpeg", "-i", str(video), "-af", "silencedetect=n=-45dB:d=0.8", "-vn", "-f", "null", "-"]))
    report: dict[str, Any] = {
        "duration_seconds": round(float(probe["format"]["duration"]), 2),
        "streams": [{k: s.get(k) for k in ("codec_type", "codec_name", "width", "height", "r_frame_rate")} for s in probe["streams"]],
        "loudness_lufs": float(loud["input_i"]),
        "true_peak_db": float(loud["input_tp"]),
        "black_segments": [(float(a), float(b)) for a, b in black],
        "silences_over_0_8s": [float(s) for s in silence],
    }
    issues = []
    if report["true_peak_db"] > -1.0:
        issues.append(f"true peak {report['true_peak_db']} dBTP is above -1.0, may clip after platform encoding")
    for a, b in report["black_segments"]:
        if a < 0.05:
            issues.append(f"first {b:.2f}s is black/near-black: first-frame previews (WhatsApp, Shorts) will look empty")
        else:
            issues.append(f"black {a:.2f}-{b:.2f}s")
    if report["silences_over_0_8s"]:
        issues.append(f"{len(report['silences_over_0_8s'])} silent gap(s) over 0.8s")
    report["issues"] = issues
    if sheet:
        sheet.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-vf",
                        f"fps=1/{every_seconds},scale=216:384,tile=10x3:padding=3", "-frames:v", "1", str(sheet)],
                       check=True, capture_output=True)
        report["contact_sheet"] = str(sheet)
    return report
