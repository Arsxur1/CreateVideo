"""Regression tests for transcriber audio decoding.

faster-whisper <= 1.2.1 decodes through PyAV with
``av.open(..., metadata_errors="ignore")``. Newer PyAV removed that keyword,
so every path-based transcription died with ``TypeError: open() got an
unexpected keyword argument 'metadata_errors'`` before reading a frame. The
tool now decodes up front and falls back to the ffmpeg CLI when faster-whisper's
own decoder fails, handing WhisperModel a 16 kHz mono float32 array.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from types import SimpleNamespace

import numpy as np
import pytest

from tools.analysis.transcriber import Transcriber

needs_ffmpeg = pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg required")

PYAV_ERROR = "open() got an unexpected keyword argument 'metadata_errors'"


class _Info:
    language = "en"
    duration = 1.0


def _install_fakes(monkeypatch, decode_audio):
    """Stub faster-whisper; return the list of audio objects passed to transcribe()."""
    received = []

    class FakeWhisperModel:
        def __init__(self, model_size, *, device, compute_type):
            pass

        def transcribe(self, audio, **kwargs):
            received.append(audio)
            return iter(()), _Info()

    monkeypatch.setitem(sys.modules, "faster_whisper", SimpleNamespace(WhisperModel=FakeWhisperModel))
    monkeypatch.setitem(sys.modules, "faster_whisper.audio", SimpleNamespace(decode_audio=decode_audio))
    # Keep device selection deterministic: no CUDA.
    monkeypatch.setitem(
        sys.modules,
        "ctranslate2",
        SimpleNamespace(get_cuda_device_count=lambda: 0, get_supported_compute_types=lambda d: set()),
    )
    return received


def _broken_pyav_decoder(path, sampling_rate):
    raise TypeError(PYAV_ERROR)


@needs_ffmpeg
def test_falls_back_to_ffmpeg_when_faster_whisper_decoder_breaks(tmp_path, monkeypatch):
    # A video container with a 2 s stereo 44.1 kHz AAC track, like the
    # reference clips that failed in production.
    clip = tmp_path / "clip.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "lavfi", "-i", "color=c=black:s=64x64:d=2",
            "-f", "lavfi", "-i", "aevalsrc=0.5*sin(2*PI*440*t):s=44100:d=2",
            "-ac", "2", "-c:v", "libx264", "-c:a", "aac", "-shortest", str(clip),
        ],
        check=True,
        timeout=60,
    )
    received = _install_fakes(monkeypatch, _broken_pyav_decoder)

    result = Transcriber().execute({"input_path": str(clip), "output_dir": str(tmp_path)})

    assert result.success, result.error
    assert result.data["audio_decoder"] == "ffmpeg"
    assert "metadata_errors" in result.data["audio_decoder_fallback_reason"]
    [audio] = received
    assert isinstance(audio, np.ndarray)
    assert audio.dtype == np.float32 and audio.ndim == 1
    assert len(audio) == pytest.approx(2 * 16000, rel=0.03)
    # Resampled to 16 kHz, the tone still sits at 440 Hz (a rate mix-up
    # would move it), at the level it was written: RMS 0.5 / sqrt(2).
    peak_hz = np.argmax(np.abs(np.fft.rfft(audio))) * 16000 / len(audio)
    assert peak_hz == pytest.approx(440, abs=5)
    rms = float(np.sqrt(np.mean(audio[4000:-4000] ** 2)))
    assert rms == pytest.approx(0.354, rel=0.1)


def test_prefers_faster_whisper_decoder_when_it_works(tmp_path, monkeypatch):
    samples = np.full(16000, 0.25, dtype=np.float32)
    calls = []

    def working_decoder(path, sampling_rate):
        calls.append((path, sampling_rate))
        return samples

    received = _install_fakes(monkeypatch, working_decoder)
    audio_file = tmp_path / "speech.wav"
    audio_file.write_bytes(b"not decoded by ffmpeg in this test")

    result = Transcriber().execute({"input_path": str(audio_file), "output_dir": str(tmp_path)})

    assert result.success, result.error
    assert calls == [(str(audio_file), 16000)]
    assert len(received) == 1 and received[0] is samples
    assert result.data["audio_decoder"] == "faster_whisper"
    assert result.data["audio_decoder_fallback_reason"] is None


@needs_ffmpeg
def test_undecodable_input_reports_both_decoders(tmp_path, monkeypatch):
    received = _install_fakes(monkeypatch, _broken_pyav_decoder)
    junk = tmp_path / "junk.mp4"
    junk.write_bytes(b"this is not a media file")

    result = Transcriber().execute({"input_path": str(junk), "output_dir": str(tmp_path)})

    assert result.success is False
    assert "metadata_errors" in result.error
    assert "ffmpeg:" in result.error
    assert received == [], "WhisperModel must not run on undecodable input"
