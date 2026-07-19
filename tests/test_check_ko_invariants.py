"""tests for scripts/check-ko-invariants.py — 게이트 3(코드펜스·URL·경로 불변)."""
import sys, importlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
cki = importlib.import_module("check-ko-invariants")


def test_token_extraction(tmp_path):
    s = tmp_path / "s.md"
    s.write_text("see https://a.com/x and `foo.py`\n", encoding="utf-8")
    toks = cki.TOKEN_RE.findall(s.read_text(encoding="utf-8"))
    assert "https://a.com/x" in toks and "foo.py" in toks


def test_fenced_block_drift_detected(tmp_path):
    s = tmp_path / "s.md"; o = tmp_path / "o.md"
    s.write_text("```\nFAL_KEY=abc\n```\n", encoding="utf-8")
    o.write_text("```\nFAL_KEY=xyz\n```\n", encoding="utf-8")
    assert cki.check_pair(s, o) != []


def test_identical_passes(tmp_path):
    s = tmp_path / "s.md"; o = tmp_path / "o.md"
    body = "```\nFAL_KEY=abc\n```\nlink: https://a.com\n"
    s.write_text(body, encoding="utf-8")
    o.write_text(body, encoding="utf-8")
    assert cki.check_pair(s, o) == []
