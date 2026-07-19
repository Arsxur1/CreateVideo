"""tests for scripts/check-encoding-hygiene.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import importlib
ceh = importlib.import_module("check-encoding-hygiene")


def write(tmp_path, source):
    p = tmp_path / "sample.py"
    p.write_text(source, encoding="utf-8")
    return p


def test_bare_open_flagged(tmp_path):
    findings, skipped = ceh.find_violations(write(tmp_path, "open(p)\n"))
    assert findings == [1] and skipped == 0


def test_text_modes_flagged(tmp_path):
    src = 'open(p, "r")\nopen(p, "wt")\nopen(p, mode="a")\n'
    findings, _ = ceh.find_violations(write(tmp_path, src))
    assert findings == [1, 2, 3]


def test_binary_modes_ok(tmp_path):
    src = 'open(p, "rb")\nopen(p, "wb")\nopen(p, mode="ab")\n'
    findings, _ = ceh.find_violations(write(tmp_path, src))
    assert findings == []


def test_encoding_kwarg_ok(tmp_path):
    src = 'open(p, encoding="utf-8")\nopen(p, "r", encoding="cp949")\n'
    findings, _ = ceh.find_violations(write(tmp_path, src))
    assert findings == []


def test_dynamic_mode_skipped(tmp_path):
    findings, skipped = ceh.find_violations(write(tmp_path, "open(p, mode)\n"))
    assert findings == [] and skipped == 1


def test_comment_and_string_ignored(tmp_path):
    src = '# open(p) is bad\ns = "open(p)"\n'
    findings, _ = ceh.find_violations(write(tmp_path, src))
    assert findings == []


def test_attribute_open_ignored(tmp_path):
    src = 'import gzip\ngzip.open(p, "rt")\nobj.open(p)\n'
    findings, _ = ceh.find_violations(write(tmp_path, src))
    assert findings == []


def test_repo_is_clean():
    assert ceh.main() == 0
