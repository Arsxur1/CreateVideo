# Encoding Hygiene Guard + Vendor Encoding Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an AST-based regression guard that fails the test suite if any new text-mode `open()` without `encoding=` lands in production code, and fix the three remaining real cp949 hazards in vendored skill scripts.

**Architecture:** A standalone scanner script (`scripts/check-encoding-hygiene.py`) following the repo's existing checker convention (`scripts/check-ko-drift.py` + `tests/test_check_ko_drift.py`), plus a pytest module with 7 synthetic-fixture unit cases and 1 repo-level guard case. Vendor fixes are one-kwarg edits to 3 files under `.agents/skills/` and `.claude/skills/`.

**Tech Stack:** Python stdlib only (`ast`, `pathlib`, `sys`), pytest.

**Spec:** `docs/superpowers/specs/2026-07-19-encoding-hygiene-design.md`

## Global Constraints

- Scanner is AST-based — never regex — so comments, docstrings, and string literals containing `open(` must NOT be flagged.
- Binary-mode opens (`"rb"`, `"wb"`, `"ab"`, any mode string containing `b`) are NEVER flagged. `encoding` is invalid in binary mode.
- Any explicit `encoding=` value passes — the guard polices explicitness, not a specific codec.
- Dynamic (non-literal) mode arguments are statically unresolvable: skip them, count them, never fail on them.
- Skip set is exactly: `.git`, `.agents`, `.claude`, `node_modules`, `venv`, `.venv`, `__pycache__`, `.pytest_cache`, `projects`, `remotion-composer`, `music_library`, `corpus`, `scratch`, `internal`. Vendor skill dirs (`.agents`, `.claude`) are excluded on purpose — the guard polices production code, not vendored knowledge.
- Scripts must reconfigure stdout to UTF-8 at import (cp949 console crashes on Korean/em-dash output otherwise) — same pattern as `scripts/check-ko-drift.py:14-16`.
- Vendor edits: add `encoding="utf-8"` and nothing else. No reformatting, no other changes to vendored files.
- Stage only the files each task explicitly creates or edits — never `git add -A`.

---

### Task 1: Scanner script + guard tests

**Files:**
- Create: `scripts/check-encoding-hygiene.py`
- Test: `tests/test_check_encoding_hygiene.py`

**Interfaces:**
- Consumes: nothing (first task).
- Produces (Task 2 verifies against these):
  - `find_violations(path) -> tuple[list[int], int]` — `(line_numbers_of_unencoded_text_opens, skipped_dynamic_mode_count)`
  - `iter_py_files(root) -> Iterator[Path]` — sorted scan targets minus skip set
  - `main(root=None) -> int` — exit code, prints `FAIL:` lines + summary

- [ ] **Step 1: Write the failing test file**

Create `tests/test_check_encoding_hygiene.py` with exactly this content:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_check_encoding_hygiene.py -q`
Expected: collection error — `ModuleNotFoundError: No module named 'check-encoding-hygiene'` (the script does not exist yet).

- [ ] **Step 3: Write the scanner**

Create `scripts/check-encoding-hygiene.py` with exactly this content:

```python
#!/usr/bin/env python3
"""encoding-hygiene guard: 텍스트 모드 open() 중 encoding= 없는 것을 FAIL로 보고.

Windows cp949 환경에서 인코딩 미지정 텍스트 open()은 비ASCII 문자를 만나는
순간 크래시. AST로 repo를 스캔해 (1) bare open() 호출 중 (2) 텍스트 모드
(기본값 포함)이면서 (3) encoding= 키워드가 없는 것을 잡는다. 바이너리 모드
(b 포함)와 동적 모드(변수 등 정적 판별 불가)는 제외. 발견이 1개라도 있으면
종료 코드 1.
"""
import ast
import pathlib
import sys

# Windows 콘솔(CP949) stdout 인코딩 강제 — 한국어·em dash 출력 UnicodeEncodeError 방지
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

SKIP_DIRS = {
    ".git", ".agents", ".claude", "node_modules", "venv", ".venv",
    "__pycache__", ".pytest_cache", "projects", "remotion-composer",
    "music_library", "corpus", "scratch", "internal",
}


def iter_py_files(root):
    """스캔 대상 .py 경로를 정렬해 반환 (SKIP_DIRS 제외)."""
    for p in sorted(pathlib.Path(root).rglob("*.py")):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        yield p


def _mode_node(call):
    """open() 호출의 mode 인자 노드 반환 (위치 2번째 또는 mode= 키워드). 없으면 None."""
    if len(call.args) >= 2:
        return call.args[1]
    for kw in call.keywords:
        if kw.arg == "mode":
            return kw.value
    return None


def find_violations(path):
    """한 파일의 (findings, skipped) 반환.

    findings: 인코딩 없는 텍스트 모드 open() 의 라인 번호 리스트.
    skipped: 모드가 동적이라 정적 판별 불가로 건너뛴 호출 수.
    """
    tree = ast.parse(
        pathlib.Path(path).read_text(encoding="utf-8", errors="replace"),
        filename=str(path),
    )
    findings, skipped = [], 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not (isinstance(node.func, ast.Name) and node.func.id == "open"):
            continue
        if any(kw.arg == "encoding" for kw in node.keywords):
            continue
        mode = _mode_node(node)
        if mode is not None and not isinstance(mode, ast.Constant):
            skipped += 1
            continue
        if (
            isinstance(mode, ast.Constant)
            and isinstance(mode.value, str)
            and "b" in mode.value
        ):
            continue
        findings.append(node.lineno)
    return findings, skipped


def main(root=None):
    root = pathlib.Path(root) if root else REPO_ROOT
    bad = skipped = scanned = 0
    for p in iter_py_files(root):
        scanned += 1
        findings, sk = find_violations(p)
        skipped += sk
        for lineno in findings:
            bad += 1
            print(f"FAIL: {p}:{lineno} — text-mode open() without encoding=")
    print(f"{bad} findings, {scanned} files scanned, {skipped} skipped dynamic-mode calls")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_check_encoding_hygiene.py -q`
Expected: `8 passed` (7 synthetic-fixture cases + `test_repo_is_clean`).

Note: `test_repo_is_clean` passes immediately because commit `4d0af4c` already removed every production text-mode `open()` lacking `encoding=`, and the remaining unencoded calls are binary-mode or inside skipped vendor dirs.

- [ ] **Step 5: Run the script standalone**

Run: `python scripts/check-encoding-hygiene.py; echo "EXIT=$?"`
Expected: exit `0`; final line matches `0 findings, <N> files scanned, <K> skipped dynamic-mode calls` with `N` ≥ 261 (the repo had 261 scannable files on 2026-07-19, plus the two files this task adds).

- [ ] **Step 6: Commit**

```bash
git add scripts/check-encoding-hygiene.py tests/test_check_encoding_hygiene.py
git commit -m "chore: add encoding-hygiene guard for unencoded text-mode open()"
```

---

### Task 2: Vendor script encoding fixes (3 files)

**Files:**
- Modify: `.agents/skills/hyperframes-creative/scripts/extract-audio-data.py:181`
- Modify: `.agents/skills/video-understand/scripts/understand_video.py:366`
- Modify: `.claude/skills/video-understand/scripts/understand_video.py:366`

**Interfaces:**
- Consumes: nothing from Task 1's code — but uses Task 1's guard script for the final verification sweep.
- Produces: nothing consumed by later tasks (terminal task).

- [ ] **Step 1: Fix `extract-audio-data.py`**

In `.agents/skills/hyperframes-creative/scripts/extract-audio-data.py`, replace this exact line (4-space indent):

```python
    with open(args.output, "w") as f:
```

with:

```python
    with open(args.output, "w", encoding="utf-8") as f:
```

- [ ] **Step 2: Fix `.agents` copy of `understand_video.py`**

In `.agents/skills/video-understand/scripts/understand_video.py`, replace this exact line (8-space indent):

```python
        with open(os.path.join(tmp_dir, json_files[0]), "r") as f:
```

with:

```python
        with open(os.path.join(tmp_dir, json_files[0]), "r", encoding="utf-8") as f:
```

- [ ] **Step 3: Fix `.claude` copy of `understand_video.py`**

In `.claude/skills/video-understand/scripts/understand_video.py`, apply the identical replacement as Step 2 (the two copies are byte-identical).

- [ ] **Step 4: Compile-check the edited files**

Run: `python -m compileall .agents/skills/hyperframes-creative/scripts/extract-audio-data.py .agents/skills/video-understand/scripts/understand_video.py .claude/skills/video-understand/scripts/understand_video.py`
Expected: all three listed as `Compiling ...` with no error lines; exit code `0`.

- [ ] **Step 5: Confirm the guard still passes repo-wide**

Run: `python scripts/check-encoding-hygiene.py; echo "EXIT=$?"`
Expected: exit `0`, `0 findings` — vendor dirs are in `SKIP_DIRS`, so these edits are outside the guard's scope; this step proves the edit didn't accidentally touch an in-scope file.

- [ ] **Step 6: Run the checker test modules**

Run: `python -m pytest tests/test_check_encoding_hygiene.py tests/test_check_ko_drift.py tests/test_check_ko_invariants.py -q`
Expected: all pass (15 tests: 8 new + 4 ko-drift + 3 ko-invariants).

- [ ] **Step 7: Commit**

```bash
git add .agents/skills/hyperframes-creative/scripts/extract-audio-data.py .agents/skills/video-understand/scripts/understand_video.py .claude/skills/video-understand/scripts/understand_video.py
git commit -m "fix: utf-8 encoding for vendored skill script open() calls"
```

---

## Final Verification

- [ ] **Step 1: Guard script clean**

Run: `python scripts/check-encoding-hygiene.py; echo "EXIT=$?"`
Expected: exit `0`, `0 findings`.

- [ ] **Step 2: Targeted suites pass**

Run: `python -m pytest tests/test_check_encoding_hygiene.py tests/test_check_ko_drift.py tests/test_check_ko_invariants.py -q`
Expected: all 15 tests pass.

- [ ] **Step 3: Broader suite sweep**

Run: `python -m pytest tests/ -q`
Expected: no NEW failures caused by this change. The full suite has 70+ files including QA/e2e tests that may require provider credentials or GPU tools; if a failure appears, confirm it also fails on the pre-change baseline (`git stash`, re-run that one test, `git stash pop`) before treating it as caused by this plan. This plan touches no production module, so any failing test that imports `lib/`, `tools/`, `schemas/`, `styles/`, `backlot/` unmodified by this plan is by definition pre-existing.

- [ ] **Step 4: Working tree clean**

Run: `git status --short`
Expected: no output — both commits landed, no stray files. (If the plan file itself is committed as part of closing out, that is the only allowed addition.)
