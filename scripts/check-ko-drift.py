#!/usr/bin/env python3
"""docs/ko 번역본이 영어 원본 대비 stale한지 검사한다.

각 번역 파일 헤더의 `> 원본: <path> @ <hash>`와 원본 파일의 최신 커밋
해시(git log -1)를 비교한다. STALE 또는 NOHEADER가 1개라도 있으면
종료 코드 1.
"""
import re
import subprocess
import sys
from pathlib import Path

# Windows 콘솔(CP949) stdout 인코딩 강제 — 한국어·em dash 출력 UnicodeEncodeError 방지
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent.parent
HEADER_RE = re.compile(r"^> 원본: (?P<src>\S+) @ (?P<hash>[0-9a-f]{40})\s*$", re.M)
ORIGINAL_RE = re.compile(r"^> 원본: \(한국어 오리지널", re.M)


def find_translation_files(root):
    files = sorted(
        f for f in (root / "docs" / "ko").glob("*.md")
        if not f.name.startswith("_")
    )
    readme_ko = root / "README_ko.md"
    if readme_ko.exists():
        files.append(readme_ko)
    return files


def source_head_hash(root, src):
    out = subprocess.run(
        ["git", "log", "-1", "--format=%H", "--", src],
        cwd=root, capture_output=True, text=True, check=True,
    )
    h = out.stdout.strip()
    if not h:
        raise RuntimeError(f"no git history for source: {src}")
    return h


def check_file(root, path, head_hash=source_head_hash):
    text = path.read_text(encoding="utf-8")
    if ORIGINAL_RE.search(text):
        return ("SKIP", None, None)
    m = HEADER_RE.search(text)
    if not m:
        return ("NOHEADER", None, None)
    current = head_hash(root, m.group("src"))
    recorded = m.group("hash")
    return ("OK" if current == recorded else "STALE", recorded, current)


def main():
    root = REPO_ROOT
    bad = 0
    for path in find_translation_files(root):
        status, recorded, current = check_file(root, path)
        rel = path.relative_to(root)
        if status == "OK":
            print(f"OK: {rel}")
        elif status == "SKIP":
            print(f"SKIP: {rel} (한국어 오리지널)")
        elif status == "NOHEADER":
            print(f"NOHEADER: {rel} — 원본 헤더 없음")
            bad += 1
        else:
            print(f"STALE: {rel} (원본 {recorded[:7]} -> {current[:7]})")
            bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
