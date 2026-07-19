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
