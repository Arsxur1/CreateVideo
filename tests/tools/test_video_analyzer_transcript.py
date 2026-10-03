"""Regression: video_analyzer must transcribe local video files.

The Whisper step only ran when a separate audio file existed, and only URL
downloads produce one. A local file carries just ``video_path``, so
standard-depth analysis of a local clip never called the transcriber and
reported ``has_transcript: false``. A failed transcription was also dropped
without a trace in ``steps_failed``.
"""

from __future__ import annotations

import shutil
import subprocess

import pytest

from tools.analysis.transcriber import Transcriber
from tools.analysis.video_analyzer import VideoAnalyzer
from tools.base_tool import ToolResult

pytestmark = pytest.mark.skipif(
    shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None,
    reason="ffmpeg and ffprobe are required",
)


@pytest.fixture
def local_clip(tmp_path):
    clip = tmp_path / "local_clip.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "lavfi", "-i", "color=c=gray:s=160x90:d=2",
            "-f", "lavfi", "-i", "sine=frequency=440:duration=2",
            "-c:v", "libx264", "-c:a", "aac", "-shortest", str(clip),
        ],
        check=True,
        timeout=60,
    )
    return clip


def test_standard_depth_transcribes_a_local_video(local_clip, tmp_path, monkeypatch):
    calls = []

    def fake_transcribe(self, inputs):
        calls.append(inputs)
        return ToolResult(
            success=True,
            data={
                "segments": [{"start": 0.0, "end": 1.5, "text": "hello from a local file"}],
                "language": "en",
            },
        )

    monkeypatch.setattr(Transcriber, "execute", fake_transcribe)

    result = VideoAnalyzer().execute({
        "source": str(local_clip),
        "analysis_depth": "standard",
        "output_dir": str(tmp_path / "analysis"),
    })

    assert result.success, result.error
    assert [call["input_path"] for call in calls] == [str(local_clip)]
    meta = result.data["_analysis_meta"]
    assert meta["has_transcript"] is True
    assert "transcript_whisper" in meta["steps_completed"]
    assert result.data["narration_transcript"]["full_text"] == "hello from a local file"


def test_transcriber_failure_is_reported(local_clip, tmp_path, monkeypatch):
    monkeypatch.setattr(
        Transcriber,
        "execute",
        lambda self, inputs: ToolResult(success=False, error="decoder exploded"),
    )

    result = VideoAnalyzer().execute({
        "source": str(local_clip),
        "analysis_depth": "transcript_only",
        "output_dir": str(tmp_path / "analysis"),
    })

    assert result.success, result.error
    assert "transcript_whisper: decoder exploded" in result.data["_analysis_meta"]["steps_failed"]
