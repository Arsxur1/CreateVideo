"""Regression: HyperFrames CLI output must be decoded as UTF-8, not the locale.

`npx hyperframes doctor --json` prints UTF-8 ("—" and "·" in check details).
In text mode without an explicit encoding, Python decodes child output with
the OS locale — GBK (cp936) on Chinese Windows — so the pipe reader thread
died with UnicodeDecodeError and the output came back as None. Preflight lost
the doctor's report, and every `--json` operation (lint, check, render, ...)
lost the CLI's result.

The fake subprocess.run below replays that failure on any platform: it
decodes with GBK unless the caller asks for an encoding, as a cp936 locale
does, and yields None where CPython's reader thread would have died.
"""

from __future__ import annotations

import subprocess

from tools.video import hyperframes_compose as hf_module
from tools.video.hyperframes_compose import HyperFramesCompose

DOCTOR_JSON = (
    '{"ok": false, "checks": ['
    '{"name": "whisper-cpp", "ok": false, '
    '"detail": "Not found (optional — needed for transcription)"}, '
    '{"name": "CPU", "ok": true, "detail": "4 cores · 2.5GHz"}]}'
).encode("utf-8")


def _locale_run(returncode: int = 0, stdout: bytes = b"", stderr: bytes = b""):
    def run(cmd, **kwargs):
        def decode(data: bytes):
            if not kwargs.get("text"):
                return data
            try:
                return data.decode(kwargs.get("encoding") or "gbk", kwargs.get("errors") or "strict")
            except UnicodeDecodeError:
                return None

        return subprocess.CompletedProcess(cmd, returncode, decode(stdout), decode(stderr))

    return run


def test_doctor_json_survives_a_non_utf8_locale(monkeypatch):
    monkeypatch.setattr(hf_module.subprocess, "run", _locale_run(stdout=DOCTOR_JSON))

    proc = HyperFramesCompose()._run_hf(["doctor", "--json"], cwd=None, timeout=30, check=False)

    report = HyperFramesCompose._parse_json_output(proc.stdout)
    assert report is not None, "doctor --json output was lost to a locale decode error"
    assert report["checks"][0]["detail"] == "Not found (optional — needed for transcription)"


def test_cli_probe_keeps_the_doctor_error_text(monkeypatch):
    monkeypatch.setattr(HyperFramesCompose, "_cli_probe_cache", None)
    monkeypatch.setattr(hf_module.shutil, "which", lambda name: name)
    monkeypatch.setattr(
        hf_module.subprocess,
        "run",
        _locale_run(returncode=1, stderr="Error — Chrome failed to launch\n".encode("utf-8")),
    )

    probe = HyperFramesCompose._probe_cli()

    assert probe == {"error": "doctor failed: Error — Chrome failed to launch"}


def test_cli_probe_passes_when_doctor_exits_cleanly(monkeypatch):
    monkeypatch.setattr(HyperFramesCompose, "_cli_probe_cache", None)
    monkeypatch.setattr(hf_module.shutil, "which", lambda name: name)
    monkeypatch.setattr(hf_module.subprocess, "run", _locale_run(stdout=DOCTOR_JSON))

    assert HyperFramesCompose._probe_cli() == {"status": "ok"}


def test_run_hf_timeout_returns_text_when_output_arrives_as_bytes(monkeypatch):
    # On POSIX, TimeoutExpired carries the partial output as raw bytes even
    # in text mode; concatenating it with the timeout note raised TypeError.
    def time_out(cmd, **kwargs):
        raise subprocess.TimeoutExpired(
            cmd, 5, output="frame 12 — rendering".encode("utf-8"), stderr=b"slow encoder"
        )

    monkeypatch.setattr(hf_module.subprocess, "run", time_out)

    proc = HyperFramesCompose()._run_hf(["render"], cwd=None, timeout=5, check=False)

    assert proc.returncode == 124
    assert proc.stdout == "frame 12 — rendering"
    assert proc.stderr == "slow encoder\n[timeout after 5s]"
