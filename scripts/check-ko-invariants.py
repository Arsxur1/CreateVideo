#!/usr/bin/env python3
"""docs/ko 번역본이 영어 원본의 코드블록·URL·경로 토큰을 verbatim 보존했는지 검사(게이트 3).

각 (원본, 번역) 쌍에서 (1) 펜스 코드블록 내용 집합, (2) URL/경로 토큰 집합을 비교.
번역 과정에서 명령·env키·URL·경로가 변형되면 FAIL. 종료 코드 1.

알려진 한계(의도적): 확장자 없는 env변수명(FAL_KEY 등)은 펜스 코드블록 집합 비교로
잡힌다. 본문 산문 내 토큰은 확장자 기반 정규식만 커버 — 누락 토큰 수로 신호 제공.
"""
import re
import sys
import pathlib

# Windows 콘솔(CP949) stdout 인코딩 강제 — 한국어·em dash 출력 UnicodeEncodeError 방지
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
PAIRS = [
    ("docs/PROVIDERS.md", "docs/ko/PROVIDERS.md"),
    ("AGENT_GUIDE.md", "docs/ko/AGENT_GUIDE.md"),
    ("docs/ARCHITECTURE.md", "docs/ko/ARCHITECTURE.md"),
    ("docs/PR_REVIEW_GUIDE.md", "docs/ko/PR_REVIEW_GUIDE.md"),
    ("docs/comfyui-adapter-plan.md", "docs/ko/comfyui-adapter-plan.md"),
    ("PROMPT_GALLERY.md", "docs/ko/PROMPT_GALLERY.md"),
    ("PROJECT_CONTEXT.md", "docs/ko/PROJECT_CONTEXT.md"),
    ("docs/apple-silicon-mps.md", "docs/ko/apple-silicon-mps.md"),
    ("docs/SPONSORS.md", "docs/ko/SPONSORS.md"),
]
TOKEN_RE = re.compile(r"https?://\S+|[A-Za-z0-9_./-]+\.(?:py|md|ts|js|json|env|sh|yaml|yml|mp4|wav|mp3|png|toml)")


def _fenced_blocks(p):
    t = pathlib.Path(p).read_text(encoding="utf-8")
    blocks, cur, inf = [], [], False
    for ln in t.splitlines():
        if ln.lstrip().startswith("```"):
            if inf:
                blocks.append("\n".join(cur)); cur = []; inf = False
            else:
                inf = True
            continue
        if inf:
            cur.append(ln)
    if cur:
        blocks.append("\n".join(cur))
    return blocks


def check_pair(src, out):
    """불일치 문제 리스트 반환(빈 리스트 = 통과)."""
    sp, op = pathlib.Path(src), pathlib.Path(out)
    problems = []
    sb, ob = _fenced_blocks(src), _fenced_blocks(out)
    missing_blocks = [b for b in sb if b not in ob]
    if missing_blocks:
        problems.append(f"원본 코드블록 {len(missing_blocks)}개가 번역본에 verbatim 누락/변형됨 (복제·한국어 미러링은 허용)")
    st = set(TOKEN_RE.findall(sp.read_text(encoding="utf-8")))
    ot = set(TOKEN_RE.findall(op.read_text(encoding="utf-8")))
    missing = st - ot
    if missing:
        problems.append(f"토큰 누락 {len(missing)}개: {sorted(missing)[:5]}")
    return problems


def main():
    bad = 0
    for src, out in PAIRS:
        if not pathlib.Path(out).exists():
            continue
        problems = check_pair(src, out)
        if problems:
            bad += 1
            print(f"FAIL: {out}")
            for p in problems:
                print(f"  - {p}")
        else:
            print(f"OK: {out}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
