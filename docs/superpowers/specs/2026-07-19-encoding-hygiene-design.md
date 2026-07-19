# Design: Encoding Hygiene Guard + Vendor Script Encoding Fixes

## Problem

On this repo's primary development machine (Windows 11, Korean locale, cp949 console), Python's `open()` defaults to the cp949 codec. Any text-mode `open()` without an explicit `encoding=` is a latent crash or mojibake bug the moment the file contains non-ASCII (Korean text, em dashes, box-drawing characters). Commit `4d0af4c` ("후속작업1") fixed all text-mode occurrences then known in production code, but:

- Nothing prevents the next agent or contributor from adding a new unencoded text-mode `open()` tomorrow. The bug class is invisible on Linux/macOS CI and on UTF-8 Windows setups, so it passes review easily.
- A repo-wide scan (2026-07-19) found the remaining unencoded `open()` calls are all binary-mode (`"rb"`/`"wb"` — correct as-is) except **two text-mode calls inside vendored Layer-3 skill scripts**, which would still crash if run on the maintainer's machine:
  - `.agents/skills/hyperframes-creative/scripts/extract-audio-data.py:181` — `open(args.output, "w")`
  - `.agents/skills/video-understand/scripts/understand_video.py:366` — `open(..., "r")`
  - `.claude/skills/video-understand/scripts/understand_video.py:366` — byte-identical copy of the `.agents` file (the `hyperframes-creative` skill exists only under `.agents/skills/`; there is no `.claude` copy)

## Goals

1. A regression guard that fails the test suite if any new text-mode `open()` without `encoding=` lands in production code.
2. Guard must be AST-based — no false positives from comments, docstrings, or string literals containing `open(`.
3. Guard must not flag binary-mode opens (`"rb"`, `"wb"`, `"ab"`, etc.) — those correctly take no `encoding`.
4. Follow the repo's existing checker convention: a standalone script in `scripts/` plus a pytest module in `tests/` (precedent: `scripts/check-ko-drift.py` + `tests/test_check_ko_drift.py`).
5. Fix the two vendored skill scripts (three files total, counting the `.claude/skills/` copy of `understand_video.py`) so the maintainer's machine can run them without a cp949 crash.

## Non-Goals

- Linting for anything other than unencoded `open()` (no general ruff/flake8 adoption — evaluated and rejected, see Alternatives).
- Scanning `pathlib` helpers (`read_text`/`write_text` without `encoding=`) — a separate, smaller bug class; can be added to the same scanner later without changing its interface.
- Retrofitting `encoding=` onto binary-mode opens (invalid — `encoding` is not allowed in binary mode).
- Running or functionally testing the vendored skill scripts (they need video inputs and provider credentials; the change is a one-word kwarg, verified by import/compile only).

## Approach

### 1. `scripts/check-encoding-hygiene.py` (new)

AST-based scanner, modeled on `check-ko-drift.py`'s structure (module-level functions, `main()` returning an exit code, cp949-safe stdout reconfigure at import time).

**Scan scope:** every `*.py` file under the repo root, minus an explicit skip set:

```
.git, node_modules, venv, .venv, __pycache__, .pytest_cache,
projects, remotion-composer, .agents, .claude, music_library,
corpus, scratch, internal
```

Rationale: `.agents/` and `.claude/` are vendored knowledge (Layer 3 skills) — not production code, and the guard should not police upstream content. `projects/` is gitignored runtime output. `remotion-composer/` is a Node project.

Current scope size (measured 2026-07-19): 261 files — root-level 2, `backlot` 4, `lib` 20, `schemas` 5, `scripts` 9, `styles` 1, `tests` 77, `tools` 143.

**Flag policy** (per `ast.Call` to a bare `open(...)` name):

| Call shape | Verdict |
|---|---|
| `open(p)` — no mode arg | FLAG (text mode is the default) |
| `open(p, "r"/"w"/"a"/"x"/"rt"/"wt"/...)` without `encoding=` | FLAG |
| any mode string containing `b` | OK (binary) |
| `encoding=` present (any value) | OK |
| mode passed as a non-literal (variable, call result) | SKIP — statically unresolvable; counted and reported as `skipped=N` in output, never a failure |
| `open` used as a method/attribute (`f.open(...)`, `tarfile.open(...)`, `gzip.open(...)`) | out of scope — AST only matches bare `Name` calls |

`encoding="utf-8"` is not prescribed — any explicit `encoding=` value passes. The guard polices explicitness, not a specific codec.

**Output:** one `FAIL: <path>:<line>` line per finding, a summary line (`N findings, M files scanned, K skipped dynamic-mode calls`), exit code 1 iff findings > 0. Mirrors the tone of the existing checkers.

### 2. `tests/test_check_encoding_hygiene.py` (new)

Mirrors `tests/test_check_ko_drift.py`: `sys.path.insert` of `scripts/`, `importlib.import_module("check-encoding-hygiene")`, synthetic fixtures written to `tmp_path`.

Unit cases (each a tiny synthetic `.py` source string):

1. bare `open(p)` → flagged
2. `open(p, "r")` / `open(p, "wt")` → flagged
3. `open(p, "rb")` / `open(p, "wb")` → not flagged
4. `open(p, encoding="utf-8")` → not flagged
5. `open(p, mode)` (dynamic) → not flagged; skip counter increments
6. `open(` inside a comment and inside a string literal → not flagged (AST advantage over regex)
7. `gzip.open(p, "rt")` / `obj.open(p)` → not flagged (attribute call, out of scope)

Repo-level case:

8. running the scanner over the actual repo root yields zero findings (the regression guard itself)

### 3. Vendor script fixes (3 files)

Add `encoding="utf-8"` to the two text-mode opens, in every copy that exists:

| File | Line | Change |
|---|---|---|
| `.agents/skills/hyperframes-creative/scripts/extract-audio-data.py` | 181 | `open(args.output, "w")` → `open(args.output, "w", encoding="utf-8")` |
| `.agents/skills/video-understand/scripts/understand_video.py` | 366 | `open(os.path.join(tmp_dir, json_files[0]), "r")` → same with `encoding="utf-8"` |
| `.claude/skills/video-understand/scripts/understand_video.py` | 366 | same as `.agents` copy |

These directories are intentionally excluded from the guard's scan scope — the fixes are for local robustness on the maintainer's machine, not compliance with the guard.

## File Changes Summary

| File | Change |
|---|---|
| `scripts/check-encoding-hygiene.py` | New — AST scanner, exit 1 on findings |
| `tests/test_check_encoding_hygiene.py` | New — 7 unit cases + 1 repo-level guard case |
| `.agents/skills/hyperframes-creative/scripts/extract-audio-data.py` | Add `encoding="utf-8"` (1 line) |
| `.agents/skills/video-understand/scripts/understand_video.py` | Add `encoding="utf-8"` (1 line) |
| `.claude/skills/video-understand/scripts/understand_video.py` | Same as `.agents` copy |

## Testing / Verification

- `python scripts/check-encoding-hygiene.py` — exit 0, output reports 0 findings and a nonzero scanned-file count (~261).
- `python -m pytest tests/test_check_encoding_hygiene.py -q` — all 8 cases pass.
- `python -m pytest tests/test_check_ko_drift.py tests/test_check_ko_invariants.py -q` — existing checker suites unaffected.
- `python -m compileall .agents/skills/hyperframes-creative/scripts/extract-audio-data.py .agents/skills/video-understand/scripts/understand_video.py .claude/skills/video-understand/scripts/understand_video.py` — vendor edits leave the files importable.
- Full `python -m pytest -q` run before committing, to catch any collateral damage.

## Alternatives Considered

- **Pytest-only guard (no standalone script)** — rejected. The repo's checker convention is script + thin pytest wrapper; a standalone script is also reusable from CI or a future pre-commit hook without invoking pytest.
- **Adopt ruff rule `PLW1514` (`unspecified-encoding`)** — rejected for this task. ruff is not currently installed and the repo has no `pyproject.toml`/`ruff.toml`; introducing a new lint toolchain, config file, and CI wiring is out of proportion to the bug class being guarded (YAGNI). If the repo later adopts ruff, this scanner can be retired in its favor.
- **Regex-based scanner** — rejected. The 2026-07-19 scan that seeded this task was regex-based and produced a false positive on a *comment* containing `open()` (`tools/video/clip_cache.py:284`). AST eliminates the class.
- **Exclude `tests/` from scan scope** — rejected. Test helpers write and read real files on the same cp949 machine; `tests/` is production-adjacent code with the same crash mode.
