"""final_review's black-frame check used "PNG smaller than 2000 bytes", but a
pure-black 1920x1080 PNG extracted by ffmpeg weighs ~8.6 KB: the check could
never fire. It now measures mean luminance."""

from __future__ import annotations

import shutil
import subprocess

import pytest

from tools.video.video_compose import VideoCompose

needs_ffmpeg = pytest.mark.skipif(not shutil.which("ffmpeg"), reason="ffmpeg not installed")


def _render(tmp_path, color: str):
    out = tmp_path / f"{color}.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error",
         "-f", "lavfi", "-i", f"color=c={color}:s=1920x1080:d=2",
         "-f", "lavfi", "-i", "sine=frequency=440:duration=2",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(out)],
        check=True, capture_output=True, timeout=60,
    )
    return out


@needs_ffmpeg
def test_black_render_is_detected(tmp_path):
    review = VideoCompose()._run_final_review(_render(tmp_path, "black"))
    assert review["checks"]["visual_spotcheck"]["black_frames_detected"] is True


@needs_ffmpeg
def test_non_black_render_is_not_flagged(tmp_path):
    review = VideoCompose()._run_final_review(_render(tmp_path, "0x404040"))
    assert review["checks"]["visual_spotcheck"]["black_frames_detected"] is False
