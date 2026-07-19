# 한국어 로컬라이제이션 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** OpenMontage 영어 문서 9개를 `docs/ko/` 이중언어 한국어 문서로 번역하고, 원본 변경을 추적하는 drift 체크 인프라를 완성한다.

**Architecture:** 번역은 파일당 1개 서브에이전트 병렬 팬아웃(번역) + 파일당 1개 리뷰 에이전트 팬아웃(게이트 검사+인플레이스 수정). 동기화는 각 번역 파일 헤더의 원본 커밋 해시와 `scripts/check-ko-drift.py` 비교로 수동 감지.

**Tech Stack:** Python 3 stdlib만(subprocess+git), pytest(기존 tests/ 관례), Markdown.

**Spec:** `docs/superpowers/specs/2026-07-19-ko-localization-design.md`

## Global Constraints

모든 태스크에 암묵적으로 적용:

- **커밋 금지**: 사용자 지시(2026-07-19)로 git commit을 수행하지 않는다. 계획의 "Commit" 단계는 전부 생략.
- 번역 형식(모든 번역 태스크 공통):
  1. 파일 상단 안내: `> 이 문서는 이중 언어 문서입니다. 각 섹션에서 영어 원문이 먼저 나오고, **[한국어]** 표시 아래에 한국어 번역이 이어집니다.`
  2. 그 다음 줄 원본 헤더: `> 원본: <원본 상대경로> @ <40자리 커밋 해시>`
  3. 섹션마다 영어 원문 → `**[한국어]**` 마커 줄 → 한국어 번역.
  4. 헤딩: `## English Title (한국어 제목)` 병기.
  5. 코드 블록, 셸 명령, 파일 경로, URL, 환경변수명, 모델 ID는 verbatim 유지. 코드 블록 내 주석만 한국어 미러링 허용.
  6. 표는 `[한국어]` 블록에서 헤더 셀 포함 전체 재표기.
  7. 합니다체 통일(`~세요` 종결 금지). 차용어: 프로바이더, 파이프라인, 렌더링, 체크포인트, 의사결정 기록.
- 품질 게이트(모든 번역·리뷰 태스크 공통):
  1. 원본 헤딩 목록과 번역본 헤딩 목록의 순서·개수·영어 문구 일치. 추출 규칙: 레벨 1~6(`^#{1,6} `) 매치, **코드펜스 내부 줄 제외**(펜스 토글 추출기 — self-verify·Task 13 Step 3의 `heads()` 사용)
  2. 깨진 글리프 grep 0건: `물묣|물료|난레이션|침침|내리에이션|열흘 개|세요|[가-힣]+[A-Z][가-힣]+`
  3. 코드 펜스 난·URL·경로 원본과 동일(`scripts/check-ko-invariants.py`로 검증)
  4. `**[한국어]**` 마커가 번역된 섹션마다 존재. 예외: `PROMPT_GALLERY.md`에서 산문 없이 프롬프트 블록(`>`)만 있는 섹션은 마커 생략 가능(헤딩은 `### English (한국어)` 유지)
  5. `세요` 종결 grep 0건
- 참고 레퍼런스(형식 표준): `docs/ko/USAGE.md`, `docs/ko/KIMI-SETUP.md`, `README_ko.md`

---

### Task 1: drift 체크 스크립트

**Files:**
- Create: `scripts/check-ko-drift.py`
- Create: `scripts/check-ko-invariants.py` (게이트 3 — 코드펜스·URL·경로 불변)
- Test: `tests/test_check_ko_drift.py`
- Test: `tests/test_check_ko_invariants.py`

**Interfaces:**
- Consumes: 없음(첫 태스크)
- Produces: `check_file(root: Path, path: Path, head_hash=source_head_hash) -> tuple[str, str|None, str|None]` — 상태는 `"OK" | "STALE" | "SKIP" | "NOHEADER"`; `main() -> int` 종료코드 0/1. Task 2·13이 이 스크립트를 실행한다.
- Produces: `check-ko-invariants.check_pair(src, out) -> list[str]` (빈 리스트=통과), `main() -> int` 종료코드 0/1. Task 13이 실행한다.

- [ ] **Step 1: 실패 테스트 작성**

`tests/test_check_ko_drift.py`:

```python
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
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `python -m pytest tests/test_check_ko_drift.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'check-ko-drift'`

- [ ] **Step 3: 스크립트 구현**

`scripts/check-ko-drift.py`:

```python
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
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `python -m pytest tests/test_check_ko_drift.py -v`
Expected: 4 passed

- [ ] **Step 5: 현재 상태에서 실행(실패 예상)**

Run: `python scripts/check-ko-drift.py`
Expected: `NOHEADER` 다수 + 종료 코드 1 (Task 2에서 헤더 백필 후 OK로 전환)

- [ ] **Step 6: invariant 스크립트 실패 테스트 작성**

`tests/test_check_ko_invariants.py`:

```python
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
```

- [ ] **Step 7: 테스트 실패 확인**

Run: `python -m pytest tests/test_check_ko_invariants.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'check-ko-invariants'`

- [ ] **Step 8: 스크립트 구현**

`scripts/check-ko-invariants.py`:

```python
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

# Windows 콘솔(CP949) stdout 인코딩 강제 — 한국어 출력 UnicodeEncodeError 방지
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
```

- [ ] **Step 9: 테스트 통과 확인**

Run: `python -m pytest tests/test_check_ko_invariants.py -v`
Expected: 3 passed

---

### Task 2: 기존 완료 파일 헤더 백필 + 정리

**Files:**
- Modify: `README_ko.md` (상단 블록인용 영역)
- Modify: `docs/ko/USAGE.md:1-8` (안내 블록인용 + Related guides)
- Modify: `docs/ko/KIMI-SETUP.md:1-3` (안내 블록인용)
- Delete: `docs/ko/_draft_readme_part1.md`, `docs/ko/_draft_readme_part2.md` (사용자 확인 후)

**Interfaces:**
- Consumes: Task 1의 `scripts/check-ko-drift.py`
- Produces: 모든 기존 ko 파일이 `OK` 또는 `SKIP` 판정 — Task 13 최종 검증의 전제.

- [ ] **Step 1: 원본 해시 조회**

Run: `git log -1 --format=%H -- README.md`
출력된 40자리 해시를 기록(이하 `<README_HASH>`).

- [ ] **Step 2: README_ko.md 헤더 삽입**

파일 상단의 이중언어 안내 블록인용(`> 이 문서는 이중 언어 문서입니다...`) 바로 다음 줄에 삽입:

```
> 원본: README.md @ <README_HASH>
```

- [ ] **Step 3: USAGE.md / KIMI-SETUP.md 헤더 삽입**

각 파일 첫 줄의 안내 블록인용 다음 줄에 삽입(두 파일은 한국어 오리지널):

```
> 원본: (한국어 오리지널 — 대응 원본 없음)
```

- [ ] **Step 4: USAGE.md Related guides 링크 복원**

현재 5행 부근의 영어/한국어 "Related guides" 줄에 README_ko 링크를 되돌린다. 두 줄을 각각 아래처럼 수정:

영어 줄:
`Related guides: [Kimi Setup Guide (KIMI-SETUP.md)](KIMI-SETUP.md) · [Bilingual Korean README (README_ko.md)](../../README_ko.md)`

한국어 줄:
`관련 문서: [Kimi 설정 가이드 (KIMI-SETUP.md)](KIMI-SETUP.md) · [이중언어 한국어 README (README_ko.md)](../../README_ko.md)`

(수정 전 현재 두 줄을 읽고 정확한 기존 문구에 맞춰 Edit할 것 — 위는 목표 형태.)

- [ ] **Step 5: draft 파일 삭제 (사용자 확인 게이트)**

`README_ko.md`에 병합이 끝난 `_draft_readme_part1.md`, `_draft_readme_part2.md` 삭제가 안전한지 **사용자에게 확인 후** 삭제:

Run: `rm docs/ko/_draft_readme_part1.md docs/ko/_draft_readme_part2.md`

사용자가 보류를 원하면 이 단계만 건너뛰고 태스크 계속.

- [ ] **Step 6: drift 스크립트로 검증**

Run: `python scripts/check-ko-drift.py`
Expected: `README_ko.md` → `OK`, `USAGE.md`/`KIMI-SETUP.md` → `SKIP`. (아직 번역 안 된 나머지는 존재하지 않으므로 출력에 없음.) 종료 코드 0.

---

### Task 3~11: 번역 팬아웃 (파일당 1 서브에이전트, 병렬)

**공통:** 각 태스크는 아래 "번역 에이전트 프롬프트 템플릿"을 해당 파일 정보로 채워 서브에이전트로 디스패치한다. 9개 전부 동일 계약 — Global Constraints의 형식 규칙·품질 게이트를 프롬프트에 그대로 포함한다. 대형 파일(PROVIDERS, AGENT_GUIDE)은 "한 번의 Write가 어려우면 순차 Edit으로 청크 분할" 지시를 추가한다.

**번역 에이전트 프롬프트 템플릿:**

```
Task: translate <SOURCE> into a bilingual Korean document at <OUTPUT>.

Read first (format standard): docs/ko/USAGE.md, docs/ko/KIMI-SETUP.md.

Rules:
1. First line blockquote: > 이 문서는 이중 언어 문서입니다. 각 섹션에서 영어 원문이 먼저 나오고, **[한국어]** 표시 아래에 한국어 번역이 이어집니다.
2. Second line: > 원본: <SOURCE> @ <hash>  — get <hash> via:
   git log -1 --format=%H -- <SOURCE>
3. Per section: English original first, then a line with exactly **[한국어]**, then the Korean translation.
4. Headings: `## English Title (한국어 제목)`.
5. Code blocks, commands, paths, URLs, env vars, model IDs: VERBATIM. Comments inside code blocks may be mirrored in Korean.
6. Tables: translate fully in the [한국어] block including header cells.
7. Formal Korean (합니다체). No ~세요 endings. Loanwords: 프로바이더/파이프라인/렌더링/체크포인트/의사결정 기록.
<EXTRA_RULES>

Self-verify before finishing (all must pass):
- python - <<'PYEOF'
  import re, sys
  def _heads(p):
      t = open(p, encoding='utf-8').read(); inf = False; out = []
      for ln in t.splitlines():
          if ln.lstrip().startswith('```'): inf = not inf; continue
          if not inf:
              m = re.match(r'^#{1,6} (.+?)\s*(?:\(|$)', ln)
              if m: out.append(m.group(1))
      return out
  hs = _heads(r'<SOURCE>'); ho = _heads(r'<OUTPUT>')
  print('headings', len(hs), len(ho)); sys.exit(0 if hs == ho else 1)
  PYEOF
- grep -nE "물묣|물료|난레이션|침침|내리에이션|열흘 개|세요|[가-힣]+[A-Z][가-힣]+" <OUTPUT>  (expect: no output)
- code fences/URLs unchanged vs source

Report: section list, line count, gate results.
```

**태스크별 매핑 및 추가 규칙(`<EXTRA_RULES>`):**

| Task | SOURCE | OUTPUT | EXTRA_RULES |
|---|---|---|---|
| 3 | `docs/PROVIDERS.md` | `docs/ko/PROVIDERS.md` | 최대 파일(933줄). 청크 쓰기 지시 포함. |
| 4 | `AGENT_GUIDE.md` | `docs/ko/AGENT_GUIDE.md` | 헤더 3번째 줄에 추가: `> ⚠️ 참조용 번역입니다. 에이전트 동작 계약의 정본은 영어 원본 [AGENT_GUIDE.md](../../AGENT_GUIDE.md)입니다.` |
| 5 | `docs/ARCHITECTURE.md` | `docs/ko/ARCHITECTURE.md` | 없음 |
| 6 | `docs/PR_REVIEW_GUIDE.md` | `docs/ko/PR_REVIEW_GUIDE.md` | 없음 |
| 7 | `docs/comfyui-adapter-plan.md` | `docs/ko/comfyui-adapter-plan.md` | 없음 |
| 8 | `PROMPT_GALLERY.md` | `docs/ko/PROMPT_GALLERY.md` | 프롬프트 예시 블록은 사용자가 AI에 붙여넣는 텍스트 — 영어 원문 유지 + 한국어 설명만 번역 |
| 9 | `PROJECT_CONTEXT.md` | `docs/ko/PROJECT_CONTEXT.md` | 없음 |
| 10 | `docs/apple-silicon-mps.md` | `docs/ko/apple-silicon-mps.md` | 없음 |
| 11 | `docs/SPONSORS.md` | `docs/ko/SPONSORS.md` | 없음 |

각 태스크의 Steps (3~11 공통):

- [ ] **Step 1: 템플릿을 채워 서브에이전트 디스패치** (9개 병렬 — 단일 메시지 다중 디스패치)
- [ ] **Step 2: 에이전트 완료 보고 수집** — 게이트 자가검증 통과 못한 파일은 동일 에이전트에 SendMessage로 수정 지시
- [ ] **Step 3: 메인 세션 스팟체크** — 해당 파일에 대해:
  Run: `grep -cE "^\*\*\[한국어\]\*\*" <OUTPUT>` (1 이상)
  Run: `grep -nE "물묣|물료|난레이션|침침|내리에이션|열흘 개|세요|[가-힣]+[A-Z][가-힣]+" <OUTPUT>` (출력 없음)
  Run: `head -2 <OUTPUT>` (안내+원본 헤더 2줄 확인)
  (게이트 3 코드펜스·URL·경로 불변은 `python scripts/check-ko-invariants.py`로 검증 — 파일별 완료 후 재실행; 아직 없는 쌍은 건너뜀)

---

### Task 12: 리뷰+수정 팬아웃 (파일당 1 리뷰 에이전트, 병렬)

**Files:**
- Modify: `docs/ko/*.md` (Task 3~11 산출물 9개, 필요 시 인플레이스 수정)

**Interfaces:**
- Consumes: Task 3~11 산출물, Global Constraints의 품질 게이트 5종
- Produces: 게이트 무통과 0개 상태 — Task 13의 입력.

- [ ] **Step 1: 리뷰 에이전트 9개 병렬 디스패치**

각 프롬프트:

```
Review and fix <OUTPUT> against its source <SOURCE> (bilingual Korean doc).

Check each gate; fix in place immediately on failure; re-check after fixing:
1. Heading coverage: source headings (levels 1-6, OUTSIDE code fences) all present, same order, same English text (parenthesized Korean appended is expected). Use the fence-aware `heads()` extractor from Task 13 Step 3.
2. Corruption grep zero: 물묣|물료|난레이션|침침|내리에이션|열흘 개|세요|[가-힣]+[A-Z][가-힣]+ — plus scan visually for broken Korean glyphs or stray Latin fragments inside Korean words.
3. Code fences, commands, URLs, paths, env vars identical to source. (자동 검증: `python scripts/check-ko-invariants.py` — FAIL 시 인플레이스 수정 후 재실행)
4. **[한국어]** marker present for every translated section. (예외: `PROMPT_GALLERY.md`의 산문 없는 프롬프트-only 섹션은 생략 가능)
5. No ~세요 endings (합니다체 only).
6. Translation accuracy spot-check: read every section pair; fix mistranslations, number errors (e.g. dozen=12), and register breaks.
7. Header lines intact: line 1 bilingual notice, line 2 `> 원본: <SOURCE> @ <hash>` — verify hash still equals `git log -1 --format=%H -- <SOURCE>`; if the source moved, update the hash.
Report: per-gate verdict, fixes applied, final verdict pass/fail.
```

- [ ] **Step 2: fail 보고 파일 재처리** — fail 1개라도 있으면 해당 에이전트에 SendMessage로 재수정 지시 후 재검증

---

### Task 13: 최종 검증

**Files:**
- Read-only 검증 (산출물 없음)

**Interfaces:**
- Consumes: 전 태스크 산출물
- Produces: 완료 보고

- [ ] **Step 1: drift 스크립트 전체 실행**

Run: `python scripts/check-ko-drift.py`
Expected: 12개 파일 전부 `OK` 또는 `SKIP`, 종료 코드 0

- [ ] **Step 2: invariant 스크립트 실행(게이트 3)**

Run: `python scripts/check-ko-invariants.py`
Expected: 번역 완료 파일 전부 `OK`, 종료 코드 0 (코드블록·URL·경로 토큰 불변)

- [ ] **Step 3: 전 파일 게이트 일괄 검사**

Run (Bash 도구/git-bash — PowerShell 아님):
```bash
cd C:/ysj/OpenMontage
for f in docs/ko/*.md README_ko.md; do
  echo "== $f =="
  grep -nE "물묣|물료|난레이션|침침|내리에이션|열흘 개|세요|[가-힣]+[A-Z][가-힣]+" "$f" || echo "glyphs OK"
  grep -c "^\*\*\[한국어\]\*\*" "$f"
done
```
Expected: 전 파일 `glyphs OK`; 마커 카운트는 원본 H1~H2 섹션 수 이상(`PROMPT_GALLERY.md` 프롬프트-only 섹션 제외 — 경고 only)

- [ ] **Step 4: 헤딩 커버리지 일괄 비교**

Run (Bash 도구/git-bash — PowerShell 아님):
```bash
python - <<'EOF'
import re, sys, pathlib
pairs = [
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
def heads(p):
    t = pathlib.Path(p).read_text(encoding="utf-8")
    inf = False; out = []
    for ln in t.splitlines():
        if ln.lstrip().startswith("```"):
            inf = not inf; continue
        if not inf:
            m = re.match(r"^(#{1,6}) (.+?)\s*(?:\(|$)", ln)
            if m: out.append(m.group(2))
    return out
bad = 0
for src, out in pairs:
    a, b = heads(src), heads(out)
    ok = a == b
    print(("OK  " if ok else "FAIL"), out, f"({len(a)}/{len(b)})")
    bad += 0 if ok else 1
sys.exit(1 if bad else 0)
EOF
```
Expected: 전 파일 `OK`, 종료 코드 0

- [ ] **Step 5: 완료 보고**

파일별 줄 수·게이트 결과 요약을 사용자에게 보고. 커밋은 하지 않는다(Global Constraints) — 커밋 여부·단위는 사용자에게 확인.

---

## Self-Review 기록

- 스펙 커버리지: §3 매핑 9개 → Task 3~11 ✓ / §4 형식 → Global Constraints ✓ / §5.1 헤더 → Task 2·번역템플릿 규칙2 ✓ / §5.2 스크립트 → Task 1 ✓ / §5.3 AGENT_GUIDE → Task 4 EXTRA_RULES ✓ / §6 게이트 → Global Constraints + Task 12 ✓ / §7 단계0 정리 → Task 2 ✓ / §7 커밋 전략(커밋 없음) → Global Constraints ✓ / §8 비범위 → 태스크 없음(의도적) ✓
- 플레이스홀더: 없음(모든 코드·명령 실제 값)
- 타입 일관성: `check_file` 시그니처 Task 1 정의와 테스트 호출 일치(`head_hash=lambda root, src: ...`)

## 개정 이력

- **2026-07-19 (리뷰 패치 — 12결함 수정):**
  1. 헤딩 추출기 코드펜스 인지 + 레벨 1~6 확장(게이트1·self-verify·Task12·Task13 `heads()`·spec §6.1) — 펜스 내 `#`주석 노이지 제거, `####` 서브섹션 커버.
  2. 게이트3 invariant 스크립트 `scripts/check-ko-invariants.py` + `tests/test_check_ko_invariants.py` 추가(Task 1 Step 6~9, Task 13 Step 2).
  3. `_`접두 파일 제외(`find_translation_files`) — draft 보류 시에도 exit 0 보장.
  4. AGENT_GUIDE 경고 링크 `../` → `../../`(plan Task 4·spec §5.3).
  5. grep 패턴 `|세요` + `|[가-힣]+[A-Z][가-힣]+` 추가(게이트2 정의·self-verify·Task 3-11·Task 12·Task 13).
  6. 게이트4 마커 = 섹션 수 비교(원본 H1~H2 하한) + `PROMPT_GALLERY.md` 프롬프트-only 섹션 예외.
  7. Task 13 bash 블록에 "Bash 도구/git-bash" 주석(PowerShell 파서에러 방지).
  8. `source_head_hash` 빈 출력 가드(untracked/missing src → 거짓 STALE 방지).
  9. Task 2 Step 4 `관련 가이드` → `관련 문서`(기존 파일 용어 일치).
