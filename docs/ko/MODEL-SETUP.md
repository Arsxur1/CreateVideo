> 이 문서는 이중 언어 문서입니다. 각 섹션에서 영어 원문이 먼저 나오고, **[한국어]** 표시 아래에 한국어 번역이 이어집니다.

> 원본: docs/MODEL-SETUP.md @ af75044f32ebc33c3798ea871dfd9cda82877ecc

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
