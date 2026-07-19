# Multi-Model Brain Documentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Document that OpenMontage's agent "brain" is swappable to any Anthropic-Messages-API-compatible model, add a first-class GLM guide alongside the existing Kimi one, make this discoverable from the English README, and give the repo owner a personal (gitignored) step-by-step switching guide for their own machine.

**Architecture:** One new English reference doc (`docs/MODEL-SETUP.md`) states the universal env-var pattern once, then has one section per concrete model (Claude baseline, Kimi, GLM, a blank template for future models). A Korean translation (`docs/ko/MODEL-SETUP.md`) follows the repo's existing bilingual-doc convention and is wired into the existing drift/invariant checkers. `docs/ko/KIMI-SETUP.md` gets a single cross-reference line and is otherwise untouched. A separate, gitignored `LOCAL-SETUP-GUIDE.md` at the repo root gives the repo owner PowerShell functions to switch brains with one word.

**Tech Stack:** Markdown docs, existing Python drift-check scripts (`scripts/check-ko-drift.py`, `scripts/check-ko-invariants.py`), existing pytest suite (`tests/test_check_ko_drift.py`, `tests/test_check_ko_invariants.py`).

## Global Constraints

- Korean translation headers must use the exact format already in use: `> 원본: <path> @ <40-char-hex-commit-hash>` (see `docs/ko/PROVIDERS.md:3`, `docs/ko/SPONSORS.md:3`).
- Bilingual body sections follow the existing pattern: English paragraph, then a `**[한국어]**` marker, then the Korean paragraph — see `docs/ko/SPONSORS.md` and `docs/ko/KIMI-SETUP.md` for the reference style.
- `check-ko-invariants.py`'s `TOKEN_RE` regex requires URLs and file-extension tokens (`.py`, `.md`, `.json`, etc.) to appear verbatim in both the English source and Korean translation — do not paraphrase code, commands, URLs, or env-var names when writing the Korean version; copy them character-for-character.
- Do NOT modify `docs/ko/KIMI-SETUP.md` beyond the single cross-reference line specified in Task 3 — it is a working, tested document.
- Do NOT include the pending Windows cp949 `open()` encoding fixes (currently uncommitted in the working tree: `lib/checkpoint.py`, `lib/config_model.py`, `lib/pipeline_loader.py`, `lib/playbook_generator.py`, `schemas/artifacts/__init__.py`, `styles/playbook_loader.py`, `tools/cost_tracker.py`, `tools/_comfyui/client.py`, three test files) in any commit created by this plan. Stage only the files this plan explicitly creates or edits.
- GLM env-var values verified via web research for this plan: endpoint `https://api.z.ai/api/anthropic`, auth var `ANTHROPIC_AUTH_TOKEN` (not `ANTHROPIC_API_KEY`), tier mapping `ANTHROPIC_DEFAULT_SONNET_MODEL=glm-4.7`, `ANTHROPIC_DEFAULT_HAIKU_MODEL=glm-4.5-air`, `API_TIMEOUT_MS=3000000`.
- Kimi env-var values already documented and verified in `docs/ko/KIMI-SETUP.md`: endpoint `https://api.moonshot.ai/anthropic` (international) / `https://api.moonshot.cn/anthropic` (mainland China), auth var `ANTHROPIC_AUTH_TOKEN`.

---

### Task 1: Write `docs/MODEL-SETUP.md` (English original)

**Files:**
- Create: `docs/MODEL-SETUP.md`

**Interfaces:**
- Consumes: nothing (first task).
- Produces: a stable file path and a stable set of `##` section anchors (`How the Brain Works`, `The Universal Pattern`, `Claude (Default)`, `Kimi (Moonshot)`, `GLM (Z.AI)`, `Any Other Compatible Model`, `Switching and Verifying`, `Caveats`, `Sources`) that Task 2 (Korean translation) and Task 4 (linking) both reference by name.

- [ ] **Step 1: Write the file**

Create `docs/MODEL-SETUP.md` with exactly this content:

```markdown
# Running OpenMontage with a Different Model Brain

OpenMontage's "AI agent" is whichever coding assistant reads this repo's
instruction files (`CLAUDE.md` / `AGENT_GUIDE.md`) and drives the Python
tools in `tools/`. That assistant's backend LLM — Claude by default — can
be swapped for any other model that exposes an Anthropic-Messages-API-
compatible endpoint, without touching any code or instruction file in
this repo.

This document explains the general pattern once, then gives the exact
settings for each model OpenMontage has been run with. For a full,
step-by-step walkthrough (installing Claude Code from scratch, verifying
the connection, troubleshooting), see
[`docs/ko/KIMI-SETUP.md`](ko/KIMI-SETUP.md) — it's written for Kimi but
the installation and verification steps apply to every model on this
page.

## How the Brain Works

The "brain" and the media-generation providers are two completely
separate things, and mixing them up is the most common point of
confusion:

- **The brain** is the LLM that reads `AGENT_GUIDE.md`, picks a pipeline,
  runs preflight, and drives the Python tools stage by stage. Changing
  the brain is an environment-variable change to your coding assistant —
  nothing in this repo needs to change.
- **Media generation** (video, image, TTS, music) is handled by separate
  provider APIs configured with their own keys in the project's `.env`
  (for example `FAL_KEY`, `ELEVENLABS_API_KEY`). Those keys are
  completely independent of which brain you use.

So "switching to Kimi" or "switching to GLM" only changes who is
directing the production — it does not unlock or change any media
provider, and it does not require a different `.env`.

## The Universal Pattern

Every model that exposes an Anthropic-Messages-API-compatible endpoint
needs the same three settings:

1. **`ANTHROPIC_BASE_URL`** — the provider's compatible endpoint.
2. **`ANTHROPIC_AUTH_TOKEN`** — the provider's API key. Note the variable
   name: it is `ANTHROPIC_AUTH_TOKEN`, not `ANTHROPIC_API_KEY`. Using the
   wrong variable name is the single most common setup mistake.
3. **Tier mapping** — Claude Code requests models by tier
   (`ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL`,
   `ANTHROPIC_DEFAULT_OPUS_MODEL`). Without mapping these to real model
   names on the target provider, Claude Code will ask for a model that
   doesn't exist there and every request will fail.

Set these as environment variables, or persist them in
`~/.claude/settings.json` under an `"env"` object. Either way, restart
your terminal (or Claude Code) after changing them — settings read at
startup will not pick up a mid-session edit.

## Claude (Default)

No configuration needed. If none of the variables above are set, Claude
Code talks to Anthropic directly and uses Claude models. This is the
baseline every other section below is a variation of.

## Kimi (Moonshot)

```bash
ANTHROPIC_BASE_URL="https://api.moonshot.ai/anthropic"
ANTHROPIC_AUTH_TOKEN="<your Moonshot API key>"
ANTHROPIC_MODEL="kimi-k2.5"
ANTHROPIC_SMALL_FAST_MODEL="kimi-k2.5"
```

If you're in mainland China, use
`https://api.moonshot.cn/anthropic` instead of the `.ai` endpoint.

Get a key from the Kimi Open Platform console at
`https://platform.kimi.ai`. Full walkthrough, including installing
Claude Code from scratch and a CLI-only alternative path:
[`docs/ko/KIMI-SETUP.md`](ko/KIMI-SETUP.md).

## GLM (Z.AI)

```bash
ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
ANTHROPIC_AUTH_TOKEN="<your Z.AI API key>"
ANTHROPIC_DEFAULT_SONNET_MODEL="glm-4.7"
ANTHROPIC_DEFAULT_OPUS_MODEL="glm-4.7"
ANTHROPIC_DEFAULT_HAIKU_MODEL="glm-4.5-air"
API_TIMEOUT_MS="3000000"
```

Get a key from the Z.AI console, under the GLM Coding Plan. Three
mistakes to avoid, in order of how often they happen:

1. Using the general `api/paas/v4` API path instead of the
   Anthropic-compatible `api/anthropic` path shown above.
2. Putting the key in `ANTHROPIC_API_KEY` instead of
   `ANTHROPIC_AUTH_TOKEN`.
3. Editing `~/.claude/settings.json` and not restarting the terminal —
   the running process keeps using whatever it read at startup.

## Any Other Compatible Model

If a provider advertises an "Anthropic-compatible" or
"Claude-compatible" endpoint, it fits the same three-variable pattern:

```bash
ANTHROPIC_BASE_URL="<the provider's compatible endpoint>"
ANTHROPIC_AUTH_TOKEN="<the provider's API key>"
ANTHROPIC_DEFAULT_SONNET_MODEL="<a real model name on that provider>"
ANTHROPIC_DEFAULT_HAIKU_MODEL="<a real, faster/cheaper model name on that provider>"
```

Verify the connection with the same command as every other model — see
"Switching and Verifying" below — before starting real production work
with it.

## Switching and Verifying

To confirm which brain is currently active, ask the assistant directly
inside a session — for example "what model are you and what endpoint are
you using" — or check which environment variables are currently set:

```bash
echo $ANTHROPIC_BASE_URL
echo $ANTHROPIC_AUTH_TOKEN
```

An empty `ANTHROPIC_BASE_URL` means you're on the Claude default. To
switch back to Claude, unset the three variables (or remove them from
`~/.claude/settings.json`) and restart the terminal.

## Caveats

- **Gate compliance is not guaranteed to be uniform across models.**
  `AGENT_GUIDE.md`'s checkpoint and human-approval gates
  (`## Human Checkpoint Protocol`) rely on the brain actually following
  the instructions in that file. A weaker or less-instruction-following
  model may skip a gate it should have stopped at.
- **This is not unmonitored, though.** Backlot's board derivation
  (`backlot/state.py`) computes a `gate_skipped` flag per stage — a gated
  stage that reached `completed` without ever passing through
  `awaiting_human` or recording `human_approved` gets flagged on the
  board regardless of which model drove the run. Check the board after a
  run with a new model, not just the terminal output.
- **Before trusting a new model with real production work**, run it
  through the `framework-smoke` pipeline first (`pipeline_defs/framework-smoke.yaml`)
  — a minimal 2-stage pipeline built for exactly this: a fast check that
  pipeline selection, preflight, and stage gating behave correctly before
  you spend a real run's worth of tokens and provider cost finding out
  they don't.

## Sources

- [Z.AI — Claude Code developer docs](https://docs.z.ai/scenario-example/develop-tools/claude)
- [Claude Code + GLM Coding Plan — 2026 Integration Guide](https://codingplan.run/guides/claude-code-with-glm)
- [ClaudeLog — How to Use Z.AI in Claude Code](https://claudelog.com/faqs/how-to-use-z-ai-in-claude-code/)
- [Using Kimi K2.5 inside Claude Code](https://kimi-k25.com/blog/kimi-k2-5-claude-code)
- [Moonshot AI forum — official guide for K2 in Claude Code](https://forum.moonshot.ai/t/do-we-have-offical-guide-for-using-k2-in-claude-code/84)
```

- [ ] **Step 2: Verify the file was written correctly**

Run: `python -c "print(open('docs/MODEL-SETUP.md', encoding='utf-8').read().count('##'))"`
Expected: a number greater than 0 (confirms the file exists and is readable as UTF-8; exact count isn't load-bearing, just confirms no read error).

- [ ] **Step 3: Commit**

```bash
git add docs/MODEL-SETUP.md
git commit -m "docs: add MODEL-SETUP.md — Kimi/GLM/generic brain-swap guide"
```

---

### Task 2: Write `docs/ko/MODEL-SETUP.md` (Korean translation)

**Files:**
- Create: `docs/ko/MODEL-SETUP.md`
- Modify: `scripts/check-ko-invariants.py:19-29` (add one entry to `PAIRS`)

**Interfaces:**
- Consumes: `docs/MODEL-SETUP.md` (Task 1) must already be committed — this task's first step reads its committed hash.
- Produces: `docs/ko/MODEL-SETUP.md`, discoverable by `check-ko-drift.py`'s `find_translation_files()` (globs `docs/ko/*.md` automatically — no code change needed there) and by `check-ko-invariants.py`'s `PAIRS` list (explicit addition required, this task does it).

- [ ] **Step 1: Get the committed hash of the English original**

Run: `git log -1 --format=%H -- docs/MODEL-SETUP.md`
Expected: a 40-character hex commit hash (the commit from Task 1, Step 3). Copy this value — it's used verbatim in Step 2 below. Call it `<HASH>`.

- [ ] **Step 2: Write the Korean translation**

Create `docs/ko/MODEL-SETUP.md`. Replace `<HASH>` in the header with the exact value from Step 1:

```markdown
> 이 문서는 이중 언어 문서입니다. 각 섹션에서 영어 원문이 먼저 나오고, **[한국어]** 표시 아래에 한국어 번역이 이어집니다.

> 원본: docs/MODEL-SETUP.md @ <HASH>

# Running OpenMontage with a Different Model Brain (다른 모델 두뇌로 OpenMontage 실행하기)

OpenMontage's "AI agent" is whichever coding assistant reads this repo's
instruction files (`CLAUDE.md` / `AGENT_GUIDE.md`) and drives the Python
tools in `tools/`. That assistant's backend LLM — Claude by default — can
be swapped for any other model that exposes an Anthropic-Messages-API-
compatible endpoint, without touching any code or instruction file in
this repo.

This document explains the general pattern once, then gives the exact
settings for each model OpenMontage has been run with. For a full,
step-by-step walkthrough (installing Claude Code from scratch, verifying
the connection, troubleshooting), see
[`docs/ko/KIMI-SETUP.md`](ko/KIMI-SETUP.md) — it's written for Kimi but
the installation and verification steps apply to every model on this
page.

**[한국어]**

OpenMontage의 "AI 에이전트"는 이 저장소의 지시 파일(`CLAUDE.md` /
`AGENT_GUIDE.md`)을 읽고 `tools/`의 Python 도구를 실행하는 코딩
어시스턴트입니다. 이 어시스턴트의 백엔드 LLM — 기본값은 Claude입니다 —
은 Anthropic Messages API 호환 엔드포인트를 제공하는 다른 모델로
바꿀 수 있으며, 이 저장소의 코드나 지시 파일을 전혀 건드리지 않습니다.

이 문서는 일반 패턴을 한 번 설명한 뒤, OpenMontage로 실행해 본 각
모델의 정확한 설정을 제공합니다. 전체 단계별 안내(Claude Code를
처음부터 설치하는 방법, 연결 확인, 문제 해결 포함)는
[`docs/ko/KIMI-SETUP.md`](ko/KIMI-SETUP.md)를 참고하십시오 — Kimi를
기준으로 작성되었지만, 설치와 연결 확인 단계는 이 문서의 모든 모델에
동일하게 적용됩니다.

## How the Brain Works (두뇌가 작동하는 방식)

The "brain" and the media-generation providers are two completely
separate things, and mixing them up is the most common point of
confusion:

- **The brain** is the LLM that reads `AGENT_GUIDE.md`, picks a pipeline,
  runs preflight, and drives the Python tools stage by stage. Changing
  the brain is an environment-variable change to your coding assistant —
  nothing in this repo needs to change.
- **Media generation** (video, image, TTS, music) is handled by separate
  provider APIs configured with their own keys in the project's `.env`
  (for example `FAL_KEY`, `ELEVENLABS_API_KEY`). Those keys are
  completely independent of which brain you use.

So "switching to Kimi" or "switching to GLM" only changes who is
directing the production — it does not unlock or change any media
provider, and it does not require a different `.env`.

**[한국어]**

"두뇌"와 미디어 생성 프로바이더는 완전히 별개이며, 이 둘을 혼동하는
것이 가장 흔한 혼란 지점입니다:

- **두뇌**는 `AGENT_GUIDE.md`를 읽고, 파이프라인을 고르고, preflight를
  실행한 뒤 Python 도구를 단계별로 실행하는 LLM입니다. 두뇌를 바꾸는
  것은 코딩 어시스턴트의 환경 변수 변경일 뿐이며, 이 저장소의 어떤
  것도 바꿀 필요가 없습니다.
- **미디어 생성**(영상, 이미지, TTS, 음악)은 프로젝트 `.env`에 별도로
  설정한 프로바이더 API 키(예: `FAL_KEY`, `ELEVENLABS_API_KEY`)가
  처리하며, 이 키들은 어떤 두뇌를 쓰는지와 완전히 독립적입니다.

즉 "Kimi로 바꾼다" 또는 "GLM으로 바꾼다"는 제작을 지휘하는 주체만
바꿀 뿐, 어떤 미디어 프로바이더도 새로 열어 주지 않으며 다른 `.env`가
필요하지도 않습니다.

## The Universal Pattern (공통 패턴)

Every model that exposes an Anthropic-Messages-API-compatible endpoint
needs the same three settings:

1. **`ANTHROPIC_BASE_URL`** — the provider's compatible endpoint.
2. **`ANTHROPIC_AUTH_TOKEN`** — the provider's API key. Note the variable
   name: it is `ANTHROPIC_AUTH_TOKEN`, not `ANTHROPIC_API_KEY`. Using the
   wrong variable name is the single most common setup mistake.
3. **Tier mapping** — Claude Code requests models by tier
   (`ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL`,
   `ANTHROPIC_DEFAULT_OPUS_MODEL`). Without mapping these to real model
   names on the target provider, Claude Code will ask for a model that
   doesn't exist there and every request will fail.

Set these as environment variables, or persist them in
`~/.claude/settings.json` under an `"env"` object. Either way, restart
your terminal (or Claude Code) after changing them — settings read at
startup will not pick up a mid-session edit.

**[한국어]**

Anthropic Messages API 호환 엔드포인트를 제공하는 모델은 모두 같은
세 가지 설정이 필요합니다:

1. **`ANTHROPIC_BASE_URL`** — 프로바이더의 호환 엔드포인트.
2. **`ANTHROPIC_AUTH_TOKEN`** — 프로바이더의 API 키. 변수 이름에
   주의하십시오: `ANTHROPIC_API_KEY`가 아니라 `ANTHROPIC_AUTH_TOKEN`입니다.
   잘못된 변수 이름을 쓰는 것이 가장 흔한 설정 실수입니다.
3. **티어 매핑** — Claude Code는 티어 이름(`ANTHROPIC_DEFAULT_SONNET_MODEL`,
   `ANTHROPIC_DEFAULT_HAIKU_MODEL`, `ANTHROPIC_DEFAULT_OPUS_MODEL`)으로
   모델을 요청합니다. 이를 대상 프로바이더의 실제 모델 이름으로
   매핑하지 않으면, Claude Code는 그곳에 존재하지 않는 모델을
   요청하게 되어 모든 요청이 실패합니다.

이 값들은 환경 변수로 설정하거나, `~/.claude/settings.json`의
`"env"` 객체에 영구 저장할 수 있습니다. 어느 쪽이든, 변경 후에는
터미널(또는 Claude Code)을 재시작해야 합니다 — 시작 시점에 읽은
설정은 세션 중간의 수정을 반영하지 않습니다.

## Claude (Default) (Claude (기본값))

No configuration needed. If none of the variables above are set, Claude
Code talks to Anthropic directly and uses Claude models. This is the
baseline every other section below is a variation of.

**[한국어]**

별도 설정이 필요 없습니다. 위 변수들이 하나도 설정되어 있지 않으면
Claude Code는 Anthropic에 직접 연결해 Claude 모델을 사용합니다. 아래
모든 섹션은 이 기본값의 변형입니다.

## Kimi (Moonshot)

```bash
ANTHROPIC_BASE_URL="https://api.moonshot.ai/anthropic"
ANTHROPIC_AUTH_TOKEN="<your Moonshot API key>"
ANTHROPIC_MODEL="kimi-k2.5"
ANTHROPIC_SMALL_FAST_MODEL="kimi-k2.5"
```

If you're in mainland China, use
`https://api.moonshot.cn/anthropic` instead of the `.ai` endpoint.

Get a key from the Kimi Open Platform console at
`https://platform.kimi.ai`. Full walkthrough, including installing
Claude Code from scratch and a CLI-only alternative path:
[`docs/ko/KIMI-SETUP.md`](ko/KIMI-SETUP.md).

**[한국어]**

중국 본토에서 사용하는 경우에는 `.ai` 엔드포인트 대신
`https://api.moonshot.cn/anthropic`을 사용하십시오.

Kimi Open Platform 콘솔(`https://platform.kimi.ai`)에서 키를
발급받으십시오. Claude Code를 처음부터 설치하는 방법과 CLI 전용
대체 경로를 포함한 전체 안내는
[`docs/ko/KIMI-SETUP.md`](ko/KIMI-SETUP.md)를 참고하십시오.

## GLM (Z.AI)

```bash
ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
ANTHROPIC_AUTH_TOKEN="<your Z.AI API key>"
ANTHROPIC_DEFAULT_SONNET_MODEL="glm-4.7"
ANTHROPIC_DEFAULT_OPUS_MODEL="glm-4.7"
ANTHROPIC_DEFAULT_HAIKU_MODEL="glm-4.5-air"
API_TIMEOUT_MS="3000000"
```

Get a key from the Z.AI console, under the GLM Coding Plan. Three
mistakes to avoid, in order of how often they happen:

1. Using the general `api/paas/v4` API path instead of the
   Anthropic-compatible `api/anthropic` path shown above.
2. Putting the key in `ANTHROPIC_API_KEY` instead of
   `ANTHROPIC_AUTH_TOKEN`.
3. Editing `~/.claude/settings.json` and not restarting the terminal —
   the running process keeps using whatever it read at startup.

**[한국어]**

Z.AI 콘솔의 GLM Coding Plan에서 키를 발급받으십시오. 자주 발생하는
순서대로, 피해야 할 실수 세 가지:

1. 위에 표시된 Anthropic 호환 경로 `api/anthropic` 대신 일반
   `api/paas/v4` API 경로를 사용하는 것.
2. 키를 `ANTHROPIC_AUTH_TOKEN`이 아니라 `ANTHROPIC_API_KEY`에
   넣는 것.
3. `~/.claude/settings.json`을 수정하고 터미널을 재시작하지 않는
   것 — 실행 중인 프로세스는 시작 시점에 읽은 값을 계속 사용합니다.

## Any Other Compatible Model (그 외 호환 모델)

If a provider advertises an "Anthropic-compatible" or
"Claude-compatible" endpoint, it fits the same three-variable pattern:

```bash
ANTHROPIC_BASE_URL="<the provider's compatible endpoint>"
ANTHROPIC_AUTH_TOKEN="<the provider's API key>"
ANTHROPIC_DEFAULT_SONNET_MODEL="<a real model name on that provider>"
ANTHROPIC_DEFAULT_HAIKU_MODEL="<a real, faster/cheaper model name on that provider>"
```

Verify the connection with the same command as every other model — see
"Switching and Verifying" below — before starting real production work
with it.

**[한국어]**

프로바이더가 "Anthropic 호환" 또는 "Claude 호환" 엔드포인트를
제공한다고 명시하면, 같은 세 가지 변수 패턴에 맞습니다:

```bash
ANTHROPIC_BASE_URL="<the provider's compatible endpoint>"
ANTHROPIC_AUTH_TOKEN="<the provider's API key>"
ANTHROPIC_DEFAULT_SONNET_MODEL="<a real model name on that provider>"
ANTHROPIC_DEFAULT_HAIKU_MODEL="<a real, faster/cheaper model name on that provider>"
```

실제 프로덕션 작업을 시작하기 전에, 아래 "전환과 확인" 섹션과 같은
방법으로 연결을 확인하십시오.

## Switching and Verifying (전환과 확인)

To confirm which brain is currently active, ask the assistant directly
inside a session — for example "what model are you and what endpoint are
you using" — or check which environment variables are currently set:

```bash
echo $ANTHROPIC_BASE_URL
echo $ANTHROPIC_AUTH_TOKEN
```

An empty `ANTHROPIC_BASE_URL` means you're on the Claude default. To
switch back to Claude, unset the three variables (or remove them from
`~/.claude/settings.json`) and restart the terminal.

**[한국어]**

현재 어떤 두뇌가 활성화되어 있는지 확인하려면, 세션 안에서 어시스턴트에게
직접 물어보거나(예: "너 지금 무슨 모델이고 어떤 엔드포인트 쓰고
있어?") 현재 설정된 환경 변수를 확인하십시오:

```bash
echo $ANTHROPIC_BASE_URL
echo $ANTHROPIC_AUTH_TOKEN
```

`ANTHROPIC_BASE_URL`이 비어 있으면 Claude 기본값을 쓰고 있는
것입니다. Claude로 되돌리려면 세 변수를 해제하거나
(`~/.claude/settings.json`에서 제거하고) 터미널을 재시작하십시오.

## Caveats (주의 사항)

- **Gate compliance is not guaranteed to be uniform across models.**
  `AGENT_GUIDE.md`'s checkpoint and human-approval gates
  (`## Human Checkpoint Protocol`) rely on the brain actually following
  the instructions in that file. A weaker or less-instruction-following
  model may skip a gate it should have stopped at.
- **This is not unmonitored, though.** Backlot's board derivation
  (`backlot/state.py`) computes a `gate_skipped` flag per stage — a gated
  stage that reached `completed` without ever passing through
  `awaiting_human` or recording `human_approved` gets flagged on the
  board regardless of which model drove the run. Check the board after a
  run with a new model, not just the terminal output.
- **Before trusting a new model with real production work**, run it
  through the `framework-smoke` pipeline first (`pipeline_defs/framework-smoke.yaml`)
  — a minimal 2-stage pipeline built for exactly this: a fast check that
  pipeline selection, preflight, and stage gating behave correctly before
  you spend a real run's worth of tokens and provider cost finding out
  they don't.

**[한국어]**

- **게이트 준수는 모델마다 균일하다고 보장되지 않습니다.**
  `AGENT_GUIDE.md`의 체크포인트·승인 게이트(`## Human Checkpoint
  Protocol`)는 두뇌가 그 문서의 지시를 실제로 따른다는 전제에
  의존합니다. 지시 이행력이 약한 모델은 멈춰야 할 게이트를 건너뛸 수
  있습니다.
- **하지만 무방비 상태는 아닙니다.** Backlot의 보드 상태 계산
  (`backlot/state.py`)은 스테이지마다 `gate_skipped` 플래그를
  계산합니다 — `awaiting_human`을 거치지도 않고 `human_approved`도
  기록하지 않은 채 `completed`에 도달한 게이트 스테이지는, 어떤
  모델이 실행했든 보드에 표시됩니다. 새 모델로 실행한 뒤에는 터미널
  출력뿐 아니라 보드도 확인하십시오.
- **새 모델에 실제 프로덕션 작업을 맡기기 전에** `framework-smoke`
  파이프라인(`pipeline_defs/framework-smoke.yaml`)으로 먼저
  테스트하십시오 — 파이프라인 선택, preflight, 스테이지 게이팅이
  올바르게 동작하는지 빠르게 확인하기 위해 만들어진 최소 2단계
  파이프라인입니다. 실제 실행 분량의 토큰과 프로바이더 비용을 쓰고
  나서야 문제를 발견하는 것을 막아 줍니다.

## Sources (출처)

- [Z.AI — Claude Code developer docs](https://docs.z.ai/scenario-example/develop-tools/claude)
- [Claude Code + GLM Coding Plan — 2026 Integration Guide](https://codingplan.run/guides/claude-code-with-glm)
- [ClaudeLog — How to Use Z.AI in Claude Code](https://claudelog.com/faqs/how-to-use-z-ai-in-claude-code/)
- [Using Kimi K2.5 inside Claude Code](https://kimi-k25.com/blog/kimi-k2-5-claude-code)
- [Moonshot AI forum — official guide for K2 in Claude Code](https://forum.moonshot.ai/t/do-we-have-offical-guide-for-using-k2-in-claude-code/84)
```

- [ ] **Step 3: Add the new pair to the invariants checker**

In `scripts/check-ko-invariants.py`, the `PAIRS` list currently reads (lines 19-29):

```python
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
```

Add one line so it reads:

```python
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
    ("docs/MODEL-SETUP.md", "docs/ko/MODEL-SETUP.md"),
]
```

- [ ] **Step 4: Run the drift checker**

Run: `python scripts/check-ko-drift.py`
Expected: exit code `0`, output includes a line `OK: docs\ko\MODEL-SETUP.md` (or `docs/ko/MODEL-SETUP.md` depending on platform path separator).

- [ ] **Step 5: Run the invariants checker**

Run: `python scripts/check-ko-invariants.py`
Expected: exit code `0`, output includes a line `OK: docs/ko/MODEL-SETUP.md`.

- [ ] **Step 6: Run the existing pytest suite for both checkers**

Run: `python -m pytest tests/test_check_ko_drift.py tests/test_check_ko_invariants.py -q`
Expected: all tests pass (no failures — the new `PAIRS` entry must not break existing fixture-based tests, since those tests exercise the checker functions against synthetic fixtures, not the new file itself).

- [ ] **Step 7: Commit**

```bash
git add docs/ko/MODEL-SETUP.md scripts/check-ko-invariants.py
git commit -m "docs(ko): add Korean translation of MODEL-SETUP.md"
```

---

### Task 3: Link the new doc from README.md, README_ko.md, and KIMI-SETUP.md

**Files:**
- Modify: `README.md:676`
- Modify: `README_ko.md:1393`
- Modify: `docs/ko/KIMI-SETUP.md:1-11`

**Interfaces:**
- Consumes: `docs/MODEL-SETUP.md` and `docs/ko/MODEL-SETUP.md` (Tasks 1-2) must exist at the paths linked here.
- Produces: nothing consumed by later tasks — this is the last content task.

- [ ] **Step 1: Add a link in README.md**

In `README.md`, find this existing line (currently line 676):

```markdown
> **Coming soon:** Local LLM support via **Ollama** and **LM Studio** — run the full production pipeline without any cloud LLM.
```

Replace it with:

```markdown
> **Coming soon:** Local LLM support via **Ollama** and **LM Studio** — run the full production pipeline without any cloud LLM.

Already possible today: swap Claude for **Kimi**, **GLM**, or any other Anthropic-compatible model — see [`docs/MODEL-SETUP.md`](docs/MODEL-SETUP.md).
```

- [ ] **Step 2: Update the link line in README_ko.md**

In `README_ko.md`, find this existing line (currently line 1393):

```markdown
한국어 사용법 가이드: [docs/ko/USAGE.md](docs/ko/USAGE.md) · Kimi 연결 가이드: [docs/ko/KIMI-SETUP.md](docs/ko/KIMI-SETUP.md)
```

Replace it with:

```markdown
한국어 사용법 가이드: [docs/ko/USAGE.md](docs/ko/USAGE.md) · 모델 두뇌 교체 가이드: [docs/ko/MODEL-SETUP.md](docs/ko/MODEL-SETUP.md) · Kimi 연결 가이드: [docs/ko/KIMI-SETUP.md](docs/ko/KIMI-SETUP.md)
```

- [ ] **Step 3: Add a cross-reference line to KIMI-SETUP.md**

In `docs/ko/KIMI-SETUP.md`, find the existing header block (lines 1-4):

```markdown
> 이 문서는 이중 언어 문서입니다. 각 섹션에서 영어 원문이 먼저 나오고, **[한국어]** 표시 아래에 한국어 번역이 이어집니다.

> 원본: (한국어 오리지널 — 대응 원본 없음)

# Running OpenMontage with Kimi (Kimi로 OpenMontage 실행하기)
```

Insert one line after the `> 원본:` line, so it reads:

```markdown
> 이 문서는 이중 언어 문서입니다. 각 섹션에서 영어 원문이 먼저 나오고, **[한국어]** 표시 아래에 한국어 번역이 이어집니다.

> 원본: (한국어 오리지널 — 대응 원본 없음)

> Other models (GLM, etc.) and the general env-var pattern: see [`docs/MODEL-SETUP.md`](../MODEL-SETUP.md) / [`docs/ko/MODEL-SETUP.md`](MODEL-SETUP.md). (다른 모델(GLM 등)과 공통 환경 변수 패턴은 [`docs/MODEL-SETUP.md`](../MODEL-SETUP.md) / [`docs/ko/MODEL-SETUP.md`](MODEL-SETUP.md)를 참고하십시오.)

# Running OpenMontage with Kimi (Kimi로 OpenMontage 실행하기)
```

Do not change anything else in this file.

- [ ] **Step 4: Re-run both drift/invariant checkers to confirm nothing broke**

Run: `python scripts/check-ko-drift.py && python scripts/check-ko-invariants.py`

Expected: `check-ko-drift.py` now reports `STALE` for `docs/ko/KIMI-SETUP.md` — this is expected and correct, because `KIMI-SETUP.md` has no English original (`ORIGINAL_RE` matches the `한국어 오리지널` marker, so it should print `SKIP`, not `STALE`; if it prints `STALE` instead, the inserted line accidentally broke the `ORIGINAL_RE` match on the `> 원본:` line — check that the new cross-reference line was inserted *after*, not *replacing*, the `> 원본: (한국어 오리지널 ...)` line). Confirm the actual output says `SKIP: docs\ko\KIMI-SETUP.md (한국어 오리지널)` before proceeding. `check-ko-invariants.py` output should be unaffected (KIMI-SETUP.md is not in its `PAIRS` list).

- [ ] **Step 5: Commit**

```bash
git add README.md README_ko.md docs/ko/KIMI-SETUP.md
git commit -m "docs: link MODEL-SETUP.md from README, README_ko, and KIMI-SETUP"
```

---

### Task 4: Personal local setup guide (gitignored)

**Files:**
- Create: `LOCAL-SETUP-GUIDE.md` (repo root — gitignored, never committed)
- Modify: `.gitignore` (add one entry)

**Interfaces:**
- Consumes: the env-var values documented in Task 1/2 (`docs/MODEL-SETUP.md`'s Kimi and GLM sections) — this task's content must match those exactly, since it's the same information repackaged as an actionable checklist.
- Produces: nothing (terminal task, no other task depends on this file).

- [ ] **Step 1: Add the gitignore entry first**

In `.gitignore`, append to the end of the file:

```
# Personal, machine-specific setup notes — never shared/committed
LOCAL-*.md
```

- [ ] **Step 2: Verify the ignore rule works before creating the file**

Run: `git check-ignore -v LOCAL-SETUP-GUIDE.md`
Expected: prints a line showing `.gitignore:<line-number>:LOCAL-*.md	LOCAL-SETUP-GUIDE.md` — confirms the pattern matches before any content is written, so there's no window where the file could be accidentally staged.

- [ ] **Step 3: Write the local guide**

Create `LOCAL-SETUP-GUIDE.md`:

```markdown
# 내 컴퓨터에서 브레인 바꾸기 (개인용, 커밋 안 됨)

Windows 11 + Claude Code 이미 설치된 상태 기준. 문서 원본은
`docs/MODEL-SETUP.md` / `docs/ko/MODEL-SETUP.md` — 이건 그걸 실제로
따라 하기 위한 개인 체크리스트.

## 1. Kimi 키 발급

1. 브라우저로 `https://platform.kimi.ai` 접속, 로그인 (계정 없으면 가입).
2. 왼쪽 메뉴에서 API Keys (또는 API 관리) 클릭.
3. 기본(default) 프로젝트에서 "새 키 생성" 클릭.
4. 생성된 키를 안전한 곳에 복사. 다시 못 봄 — 놓치면 재발급.
5. 이 키가 `ANTHROPIC_AUTH_TOKEN` 값이 됨.

해외 엔드포인트: `https://api.moonshot.ai/anthropic`
중국 본토면: `https://api.moonshot.cn/anthropic`

## 2. GLM 키 발급

1. 브라우저로 Z.AI 콘솔 접속 (`https://z.ai` 가입/로그인).
2. GLM Coding Plan 섹션에서 플랜 선택 (Lite $10/월부터).
3. API Keys 메뉴에서 키 생성.
4. 키 복사해서 안전한 곳에 보관.

엔드포인트: `https://api.z.ai/api/anthropic` (주의: `api/paas/v4` 아님)

## 3. PowerShell 프로필에 전환 함수 추가

PowerShell 프로필 파일 열기(없으면 새로 만듦):

```powershell
if (-not (Test-Path $PROFILE)) { New-Item -ItemType File -Path $PROFILE -Force }
notepad $PROFILE
```

아래 함수 세 개를 파일 끝에 붙여넣기. `<여기에-키>` 부분만 실제 키로 교체:

```powershell
function use-kimi {
    $env:ANTHROPIC_BASE_URL = "https://api.moonshot.ai/anthropic"
    $env:ANTHROPIC_AUTH_TOKEN = "<여기에-Kimi-키>"
    $env:ANTHROPIC_MODEL = "kimi-k2.5"
    $env:ANTHROPIC_SMALL_FAST_MODEL = "kimi-k2.5"
    Write-Host "brain -> Kimi (kimi-k2.5)" -ForegroundColor Cyan
}

function use-glm {
    $env:ANTHROPIC_BASE_URL = "https://api.z.ai/api/anthropic"
    $env:ANTHROPIC_AUTH_TOKEN = "<여기에-GLM-키>"
    $env:ANTHROPIC_DEFAULT_SONNET_MODEL = "glm-4.7"
    $env:ANTHROPIC_DEFAULT_OPUS_MODEL = "glm-4.7"
    $env:ANTHROPIC_DEFAULT_HAIKU_MODEL = "glm-4.5-air"
    $env:API_TIMEOUT_MS = "3000000"
    Write-Host "brain -> GLM (glm-4.7 / glm-4.5-air)" -ForegroundColor Cyan
}

function use-claude {
    Remove-Item Env:\ANTHROPIC_BASE_URL -ErrorAction SilentlyContinue
    Remove-Item Env:\ANTHROPIC_AUTH_TOKEN -ErrorAction SilentlyContinue
    Remove-Item Env:\ANTHROPIC_MODEL -ErrorAction SilentlyContinue
    Remove-Item Env:\ANTHROPIC_SMALL_FAST_MODEL -ErrorAction SilentlyContinue
    Remove-Item Env:\ANTHROPIC_DEFAULT_SONNET_MODEL -ErrorAction SilentlyContinue
    Remove-Item Env:\ANTHROPIC_DEFAULT_OPUS_MODEL -ErrorAction SilentlyContinue
    Remove-Item Env:\ANTHROPIC_DEFAULT_HAIKU_MODEL -ErrorAction SilentlyContinue
    Remove-Item Env:\API_TIMEOUT_MS -ErrorAction SilentlyContinue
    Write-Host "brain -> Claude (default)" -ForegroundColor Cyan
}
```

저장하고 새 PowerShell 창 열기 (또는 `. $PROFILE` 실행해서 즉시 반영).

## 4. 전환 확인법

새 PowerShell 창에서:

```powershell
use-kimi
echo $env:ANTHROPIC_BASE_URL
```

예상 출력: `https://api.moonshot.ai/anthropic`

그 상태로 Claude Code 새로 실행하고 세션 안에서 물어보기:
"너 지금 무슨 모델이고 어떤 엔드포인트로 연결됐어?"
→ Kimi/Moonshot이라고 답하면 정상.

Claude로 되돌리기: `use-claude` 실행 후 새 터미널.

## 5. 문제 생겼을 때

| 증상 | 원인 | 해결 |
|---|---|---|
| "model not found" 에러 | 티어 매핑(`ANTHROPIC_DEFAULT_SONNET_MODEL` 등) 안 함 | `use-kimi`/`use-glm` 함수 다시 확인, 오타 없는지 |
| 인증 실패 (401) | 키를 `ANTHROPIC_API_KEY`에 넣음 | `ANTHROPIC_AUTH_TOKEN`인지 확인 |
| 여전히 Claude로 붙음 | 기존 터미널에서 함수만 실행하고 Claude Code는 재시작 안 함 | Claude Code 프로세스 완전히 껐다 켜기 |
| GLM 연결 실패 | `api/paas/v4` 경로 씀 | `api/anthropic` 경로로 수정 |
| 함수가 안 보임 | `$PROFILE` 저장 후 새 창 안 열었음 | 새 PowerShell 창 열거나 `. $PROFILE` 실행 |
```

- [ ] **Step 4: Confirm the file is genuinely untracked**

Run: `git status --short LOCAL-SETUP-GUIDE.md`
Expected: no output at all (empty) — confirms git is not tracking it and `git add -A` elsewhere in this session would not accidentally stage it.

- [ ] **Step 5: Commit the .gitignore change only**

```bash
git add .gitignore
git commit -m "chore: gitignore personal LOCAL-*.md setup notes"
```

(No commit for `LOCAL-SETUP-GUIDE.md` itself — it must never be committed.)

---

## Final Verification

- [ ] **Step 1: Run the full doc-check suite one more time**

Run: `python scripts/check-ko-drift.py && python scripts/check-ko-invariants.py && python -m pytest tests/test_check_ko_drift.py tests/test_check_ko_invariants.py -q`

Expected: both scripts exit `0`, pytest reports all passed, and the drift output shows `OK: docs\ko\MODEL-SETUP.md` (or `docs/ko/...` depending on OS) alongside the existing `OK`/`SKIP` lines for every other translated doc.

- [ ] **Step 2: Confirm the working tree only has the expected uncommitted state**

Run: `git status --short`
Expected: no output related to `docs/MODEL-SETUP.md`, `docs/ko/MODEL-SETUP.md`, `scripts/check-ko-invariants.py`, `README.md`, `README_ko.md`, `docs/ko/KIMI-SETUP.md`, or `.gitignore` (all committed in Tasks 1-4). `LOCAL-SETUP-GUIDE.md` must not appear at all (gitignored). Any output should only be the pre-existing, unrelated uncommitted files noted in the Global Constraints section (the cp949 encoding fixes) — do not touch or commit those as part of this plan.
