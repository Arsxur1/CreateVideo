"""piper_tts only looked for `piper` on PATH. `make setup` installs it into
.venv/bin, so unless the venv is activated the tool reported UNAVAILABLE while
installed. It now also looks next to the running interpreter."""

from __future__ import annotations

from tools.audio import piper_tts as piper_mod
from tools.audio.piper_tts import PiperTTS
from tools.base_tool import ToolStatus


def test_piper_in_venv_bin_is_found_when_not_on_path(tmp_path, monkeypatch):
    venv_bin = tmp_path / "venv" / "bin"
    venv_bin.mkdir(parents=True)
    binary = venv_bin / "piper"
    binary.write_text("#!/bin/sh\n")
    binary.chmod(0o755)
    monkeypatch.setattr(piper_mod.shutil, "which", lambda name: None)
    monkeypatch.setattr(piper_mod.sys, "executable", str(venv_bin / "python"))
    assert PiperTTS().get_status() == ToolStatus.AVAILABLE


def test_piper_missing_everywhere_is_unavailable(tmp_path, monkeypatch):
    monkeypatch.setattr(piper_mod.shutil, "which", lambda name: None)
    monkeypatch.setattr(piper_mod.sys, "executable", str(tmp_path / "python"))
    assert PiperTTS().get_status() == ToolStatus.UNAVAILABLE
