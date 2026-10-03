"""Regression tests for full_mix gain staging and loudness normalization.

Two defects made narration-plus-music mixes unusable:

* Speech lines were combined with amix's default normalize=1, which scales
  every input by 1/(inputs still running). Lines placed with adelay count as
  running from t=0, so with 15 lines the first came out ~23.5 dB down and the
  last at full level, and the attenuated copy feeding the sidechain key was
  too quiet to duck the music under the early lines at all.
* The final single-pass loudnorm ran in dynamic mode and raised the gain in
  every music-only gap between lines, lifting the music to speech level.

The fixtures are pure tones — speech at 1 kHz, music at 200 Hz — so each can
be measured on its own with a single-bin DFT.
"""

from __future__ import annotations

import json
import math
import shutil
import subprocess
import wave
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from tools.audio.audio_mixer import AudioMixer

needs_ffmpeg = pytest.mark.skipif(
    shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None,
    reason="ffmpeg and ffprobe are required",
)

SPEECH_HZ, MUSIC_HZ = 1000, 200
LINE_SECONDS, LINE_PERIOD = 1.5, 3.5
TRUE_PEAK_CEILING = -1.5


def _tone(path: Path, hz: int, seconds: float, amplitude: float,
          rate: int = 24000, channels: int = 1) -> Path:
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
            f"aevalsrc={amplitude}*sin(2*PI*{hz}*t):s={rate}:d={seconds}",
            "-ac", str(channels), str(path),
        ],
        check=True,
        timeout=60,
    )
    return path


def _read_wav(path: Path) -> tuple[np.ndarray, int]:
    with wave.open(str(path), "rb") as handle:
        assert handle.getsampwidth() == 2
        rate, channels = handle.getframerate(), handle.getnchannels()
        raw = handle.readframes(handle.getnframes())
    samples = np.frombuffer(raw, "<i2").astype(np.float64) / 32768
    return samples.reshape(-1, channels).mean(axis=1), rate


def _level_db(samples: np.ndarray, rate: int, hz: int, start: float, end: float) -> float:
    window = samples[int(start * rate):int(end * rate)]
    n = np.arange(len(window))
    amplitude = 2 / len(window) * abs(np.sum(window * np.exp(-2j * np.pi * hz * n / rate)))
    return 20 * math.log10(max(amplitude, 1e-9))


def _loudness(path: Path) -> tuple[float, float]:
    """Integrated loudness (LUFS) and true peak (dBTP), measured independently."""
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
         "-af", "loudnorm=print_format=json", "-f", "null", "-"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        check=True, timeout=120,
    )
    report = proc.stderr[proc.stderr.rfind("{"):proc.stderr.rfind("}") + 1]
    stats = json.loads(report)
    return float(stats["input_i"]), float(stats["input_tp"])


def _speech_lines(path: Path, count: int) -> list[dict]:
    return [
        {"path": str(path), "role": "speech", "start_seconds": k * LINE_PERIOD}
        for k in range(count)
    ]


@needs_ffmpeg
def test_speech_lines_are_placed_at_unity_gain(tmp_path):
    line = _tone(tmp_path / "line.wav", SPEECH_HZ, LINE_SECONDS, 0.25)
    out = tmp_path / "mix.wav"

    result = AudioMixer().execute({
        "operation": "full_mix",
        "tracks": _speech_lines(line, 8),
        "normalize": False,
        "output_path": str(out),
    })

    assert result.success, result.error
    samples, rate = _read_wav(out)
    assert rate == 48000
    levels = [
        _level_db(samples, rate, SPEECH_HZ, k * LINE_PERIOD + 0.2, k * LINE_PERIOD + 1.3)
        for k in range(8)
    ]
    # Every line keeps its source level (0.25 = -12.04 dBFS): no 1/N scaling.
    for level in levels:
        assert level == pytest.approx(20 * math.log10(0.25), abs=0.3), levels


@needs_ffmpeg
def test_normalized_mix_keeps_ducking_and_line_levels(tmp_path):
    lines = 15
    line = _tone(tmp_path / "line.wav", SPEECH_HZ, LINE_SECONDS, 0.25)
    bed = _tone(tmp_path / "bed.wav", MUSIC_HZ, lines * LINE_PERIOD + 1, 0.5,
                rate=44100, channels=2)
    out = tmp_path / "mix.wav"

    result = AudioMixer().execute({
        "operation": "full_mix",
        "tracks": _speech_lines(line, lines) + [
            {"path": str(bed), "role": "music", "volume": 0.3},
        ],
        "output_path": str(out),
    })

    assert result.success, result.error
    loudness = result.data["loudness"]
    assert "warning" not in loudness, loudness
    integrated, true_peak = _loudness(out)
    assert integrated == pytest.approx(-16, abs=0.5)
    assert loudness["output_lufs"] == pytest.approx(integrated, abs=0.1)
    assert true_peak <= TRUE_PEAK_CEILING

    samples, rate = _read_wav(out)
    assert rate == 48000
    speech, ducked, gaps = [], [], []
    for k in range(lines):
        start = k * LINE_PERIOD
        speech.append(_level_db(samples, rate, SPEECH_HZ, start + 0.4, start + LINE_SECONDS - 0.1))
        ducked.append(_level_db(samples, rate, MUSIC_HZ, start + 0.4, start + LINE_SECONDS - 0.1))
        if k < lines - 1:
            gaps.append(_level_db(samples, rate, MUSIC_HZ, start + LINE_SECONDS + 1.0,
                                  start + LINE_PERIOD - 0.05))

    # First and last narration lines come out at the same level.
    assert max(speech) - min(speech) < 0.5, speech
    # The music ducks under every line, the first ones included...
    for k in range(lines - 1):
        assert gaps[k] - ducked[k] > 8, (k, gaps[k], ducked[k])
    # ...and normalization does not lift the music-only gaps to speech level.
    assert min(speech) - max(gaps) > 6, (speech, gaps)


@needs_ffmpeg
def test_true_peak_holds_when_the_gain_drives_the_limiter(tmp_path):
    # Quiet narration with near-full-scale 1 ms clicks (think plosives): the
    # gain that brings the narration to -14 LUFS pushes the clicks ~10 dB
    # past the ceiling, but they are too short to move the loudness.
    quiet = _tone(tmp_path / "quiet.wav", SPEECH_HZ, 6, 0.1)
    click = _tone(tmp_path / "click.wav", 3000, 0.001, 0.95, rate=48000)
    out = tmp_path / "mix.wav"

    result = AudioMixer().execute({
        "operation": "full_mix",
        "tracks": [{"path": str(quiet), "role": "speech"}] + [
            {"path": str(click), "role": "sfx", "start_seconds": t} for t in (1, 3, 5)
        ],
        "loudnorm_target": -14,
        "output_path": str(out),
    })

    assert result.success, result.error
    loudness = result.data["loudness"]
    # Without the limiter the gained clicks would land this far over the ceiling.
    assert loudness["measured_true_peak_dbtp"] + loudness["gain_db"] > TRUE_PEAK_CEILING + 6
    integrated, true_peak = _loudness(out)
    assert true_peak <= TRUE_PEAK_CEILING
    assert integrated == pytest.approx(-14, abs=0.5)


@needs_ffmpeg
def test_unnormalized_mix_is_peak_limited_instead_of_clipping(tmp_path):
    # Unity-gain summing of two in-phase 0.8 tones peaks at 1.6 (+4 dBFS).
    tone = _tone(tmp_path / "tone.wav", SPEECH_HZ, 2, 0.8)
    out = tmp_path / "mix.wav"

    result = AudioMixer().execute({
        "operation": "full_mix",
        "tracks": [
            {"path": str(tone), "role": "speech"},
            {"path": str(tone), "role": "sfx"},
        ],
        "normalize": False,
        "output_path": str(out),
    })

    assert result.success, result.error
    assert result.data["loudness"]["gain_db"] == 0
    _, true_peak = _loudness(out)
    assert true_peak <= TRUE_PEAK_CEILING


def _loudnorm_report(integrated: float, true_peak: float) -> str:
    return (
        "[Parsed_loudnorm_0 @ 0000] \n{\n"
        f'\t"input_i" : "{integrated:.2f}",\n'
        f'\t"input_tp" : "{true_peak:.2f}",\n'
        '\t"input_lra" : "3.00",\n\t"input_thresh" : "-40.00",\n'
        '\t"normalization_type" : "dynamic",\n\t"target_offset" : "0.00"\n}\n'
    )


def test_render_is_corrected_when_limiting_costs_loudness(tmp_path, monkeypatch):
    """Static gain, measured output, and one corrective re-render — no ffmpeg."""
    for name in ("speech.wav", "music.wav"):
        (tmp_path / name).write_bytes(b"stub")
    out = tmp_path / "mix.wav"
    output_measurements = [-15.2, -14.2]  # first render lost 1.2 LU to the limiter
    commands = []

    def fake_run(self, cmd, **kwargs):
        commands.append(list(cmd))
        if cmd[-3:] == ["-f", "null", "-"]:
            graph = cmd[cmd.index("-filter_complex") + 1]
            if graph.startswith("[0:a]loudnorm"):  # measuring the rendered file
                return SimpleNamespace(stdout="", stderr=_loudnorm_report(output_measurements.pop(0), -2.0))
            return SimpleNamespace(stdout="", stderr=_loudnorm_report(-30.0, -6.0))
        return SimpleNamespace(stdout="", stderr="")

    monkeypatch.setattr(AudioMixer, "run_command", fake_run)
    result = AudioMixer().execute({
        "operation": "full_mix",
        "tracks": [
            {"path": str(tmp_path / "speech.wav"), "role": "speech"},
            {"path": str(tmp_path / "speech.wav"), "role": "speech", "start_seconds": 4},
            {"path": str(tmp_path / "music.wav"), "role": "music", "volume": 0.3},
        ],
        "loudnorm_target": -14,
        "output_path": str(out),
    })

    assert result.success, result.error
    renders = [cmd for cmd in commands if cmd[-1] == str(out)]
    assert len(renders) == 2
    first_graph = renders[0][renders[0].index("-filter_complex") + 1]
    second_graph = renders[1][renders[1].index("-filter_complex") + 1]
    # Every amix sums at unity, and no dynamic loudnorm touches the render.
    amixes = [part for part in first_graph.split(";") if "amix=" in part]
    assert amixes and all("normalize=0" in part for part in amixes), amixes
    assert "loudnorm" not in first_graph
    assert "volume=16.00dB" in first_graph  # -14 - (-30)
    assert "volume=17.20dB" in second_graph  # + the 1.2 LU the limiter cost
    assert "alimiter=" in second_graph and "aresample=192000" in second_graph
    loudness = result.data["loudness"]
    assert loudness["renders"] == 2
    assert loudness["output_lufs"] == pytest.approx(-14.2)
    assert "warning" not in loudness
