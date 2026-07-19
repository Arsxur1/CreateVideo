"""tests for scripts/check-ko-drift.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import importlib
ckd = importlib.import_module("check-ko-drift")


def write(tmp_path, text):
    p = tmp_path / "sample.md"
    p.write_text(text, encoding="utf-8")
    return p


H40 = "a" * 40


def test_header_ok(tmp_path):
    p = write(tmp_path, f"> 안내\n> 원본: docs/X.md @ {H40}\n\n# T\n")
    status, recorded, current = ckd.check_file(
        tmp_path, p, head_hash=lambda root, src: H40
    )
    assert status == "OK" and recorded == H40 and current == H40


def test_header_stale(tmp_path):
    p = write(tmp_path, f"> 원본: docs/X.md @ {H40}\n")
    status, recorded, current = ckd.check_file(
        tmp_path, p, head_hash=lambda root, src: "b" * 40
    )
    assert status == "STALE" and recorded == H40 and current == "b" * 40


def test_korean_original_skip(tmp_path):
    p = write(tmp_path, "> 원본: (한국어 오리지널 — 대응 원본 없음)\n")
    status, _, _ = ckd.check_file(tmp_path, p, head_hash=lambda r, s: H40)
    assert status == "SKIP"


def test_no_header(tmp_path):
    p = write(tmp_path, "# 그냥 문서\n")
    status, _, _ = ckd.check_file(tmp_path, p, head_hash=lambda r, s: H40)
    assert status == "NOHEADER"
