"""Stitch the eight 'Dưới tán hoa — Ngày 10' shots into the 9:16 master.

The two Vietnamese cards are burned in here rather than kept in a sidecar
subtitle file: the deliverable is a vertical short that gets uploaded straight
to a feed, and feeds do not carry .srt. There is no voice-over — no TTS
provider on this machine speaks Vietnamese — so these cards and the shop logo
on the final marker carry the entire text of the piece.

    python scripts/stitch_duoi_tan_hoa.py [--dir <clip-dir>] [--out <mp4>]
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

FONT = "C\:/Windows/Fonts/arial.ttf"
OPEN_TEXT = "10 ngày trước khi hoa nở…"
# The shop name is not drawn as text any more: shot 8's marker carries the real
# logo, printed into the frame Flow animated. A caption repeating it would sit
# on top of the sign saying the same thing twice.
END_SMALL = "CÒN 10 NGÀY"
FADE = 0.6                     # seconds each card takes to appear and leave


def probe_duration(clip: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(clip)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def card(text: str, size: int, y: str, start: float, end: float) -> str:
    """One drawtext filter that fades in, holds, and fades out."""
    safe = text.replace(":", r"\:").replace("'", r"\'").replace(",", r"\,")
    alpha = (f"if(lt(t,{start}),0,"
             f"if(lt(t,{start + FADE}),(t-{start})/{FADE},"
             f"if(lt(t,{end - FADE}),1,"
             f"if(lt(t,{end}),({end}-t)/{FADE},0))))")
    return (f"drawtext=fontfile='{FONT}':text='{safe}':fontsize={size}:"
            f"fontcolor=white:alpha='{alpha}':x=(w-text_w)/2:y={y}:"
            f"shadowcolor=black@0.35:shadowx=1:shadowy=1")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dir", default="projects/duoi-tan-hoa-ngay-10/assets/v2/video")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    clip_dir = Path(args.dir)
    clips = sorted(c for c in clip_dir.glob("*.mp4")
                   if len(c.stem) > 2 and c.stem[:2].isdigit())
    if len(clips) != 8:
        raise SystemExit(f"expected 8 numbered clips in {clip_dir}, found {len(clips)}")

    out = Path(args.out or (clip_dir / "duoi_tan_hoa_ngay10_9x16.mp4"))
    # The concat demuxer needs a list file; ffmpeg resolves its paths relative
    # to the list, so write it beside the clips.
    listing = clip_dir / "_concat.txt"
    listing.write_text("".join(f"file '{c.name}'\n" for c in clips), encoding="utf-8")

    spans = [probe_duration(c) for c in clips]
    total = sum(spans)
    last_start = total - spans[-1]

    filters = ",".join([
        card(OPEN_TEXT, 26, "h*0.80", 0.8, spans[0] - 0.7),
        card(END_SMALL, 24, "h*0.82", last_start + 1.6, total),
    ])

    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
         "-i", str(listing), "-vf", filters,
         "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)],
        check=True)
    listing.unlink()

    size_mb = out.stat().st_size / 1_048_576
    print(f"{out}  {probe_duration(out):.2f}s  {size_mb:.1f} MiB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
