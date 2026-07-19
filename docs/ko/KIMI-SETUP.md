> 이 문서는 이중 언어 문서입니다. 각 섹션에서 영어 원문이 먼저 나오고, **[한국어]** 표시 아래에 한국어 번역이 이어집니다.

> 원본: (한국어 오리지널 — 대응 원본 없음)

> Other models (GLM, etc.) and the general env-var pattern: see [`docs/MODEL-SETUP.md`](../MODEL-SETUP.md) / [`docs/ko/MODEL-SETUP.md`](MODEL-SETUP.md). (다른 모델(GLM 등)과 공통 환경 변수 패턴은 [`docs/MODEL-SETUP.md`](../MODEL-SETUP.md) / [`docs/ko/MODEL-SETUP.md`](MODEL-SETUP.md)를 참고하십시오.)

# Running OpenMontage with Kimi (Kimi로 OpenMontage 실행하기)

This guide shows how to run OpenMontage with Moonshot AI's Kimi models as the agent brain instead of Claude.

**[한국어]**

이 가이드는 OpenMontage의 에이전트 두뇌를 Claude 대신 Moonshot AI의 Kimi 모델로 바꿔 실행하는 방법을 설명합니다.

## 1. How OpenMontage Uses an AI Model (OpenMontage가 AI 모델을 사용하는 방식)

OpenMontage is not a program with an LLM SDK wired in. The "AI agent" is whichever coding assistant reads the repo's instruction files (`CLAUDE.md` / `AGENTS.md` / `AGENT_GUIDE.md`) and drives the Python tools in `tools/`. In that setup the LLM acts as the director: it reads `AGENT_GUIDE.md`, picks a pipeline, runs preflight, and executes stage by stage. The actual media generation (video, image, TTS, music) is handled by separate provider APIs configured with their own keys in the project's `.env` (for example `FAL_KEY`), and those keys are completely independent of which LLM brain you use. So "connecting Kimi" means running the agent harness on Kimi, nothing more.

**The Kimi API key only replaces the agent brain. It does NOT give you video or image generation.** This separation is the number one confusion point, so keep it in mind through the rest of this guide.

**[한국어]**

OpenMontage는 LLM SDK가 내장된 프로그램이 아닙니다. 여기서 말하는 "AI 에이전트"는 저장소의 지시 파일(`CLAUDE.md` / `AGENTS.md` / `AGENT_GUIDE.md`)을 읽고 `tools/`의 Python 도구를 실행해 주는 코딩 어시스턴트입니다. 이 구조에서 LLM은 감독(director) 역할을 합니다. `AGENT_GUIDE.md`를 읽고, 파이프라인을 고르고, preflight를 실행한 뒤 단계별로 제작을 진행합니다. 실제 미디어 생성(영상, 이미지, TTS, 음악)은 프로젝트 `.env`에 별도로 설정한 프로바이더 API 키(예: `FAL_KEY`)가 처리하며, 이 키들은 어떤 LLM을 두뇌로 쓰는지와 완전히 독립적으로 동작합니다. 즉 "Kimi를 연결한다"는 것은 에이전트 하니스를 Kimi로 돌린다는 뜻, 그 이상도 이하도 아닙니다.

**Kimi API 키는 에이전트의 두뇌만 바꿔 줍니다. 영상이나 이미지 생성 기능을 제공하지는 않습니다.** 가장 많이 혼동하는 지점이니, 이후 내용을 읽는 동안 이 구분을 염두에 두십시오.

## 2. Get a Kimi API Key (Kimi API 키 발급받기)

1. Go to the Kimi Open Platform console at https://platform.kimi.ai and sign in.
2. Create an API key in the default project.
3. Copy the key somewhere safe. You will paste it as `ANTHROPIC_AUTH_TOKEN` below.

Note on endpoints: the international endpoint is `https://api.moonshot.ai/anthropic`. If you are in mainland China, use `https://api.moonshot.cn/anthropic` instead. The examples below use the international endpoint.

**[한국어]**

1. Kimi Open Platform 콘솔(https://platform.kimi.ai)에 접속해 로그인합니다.
2. 기본(default) 프로젝트에서 API 키를 생성합니다.
3. 키를 안전한 곳에 복사해 둡니다. 아래에서 `ANTHROPIC_AUTH_TOKEN` 값으로 사용합니다.

엔드포인트 참고 사항: 해외용 엔드포인트는 `https://api.moonshot.ai/anthropic`입니다. 중국 본토에서 사용하는 경우에는 `https://api.moonshot.cn/anthropic`을 대신 사용하십시오. 아래 예시는 해외용 엔드포인트 기준입니다.

## 3. Path A (Recommended): Claude Code Running on Kimi (경로 A (권장): Kimi에서 Claude Code 실행하기)

Claude Code supports Anthropic-compatible endpoints, and Moonshot exposes one for Kimi. Point Claude Code at that endpoint and the harness stays Claude Code while the model becomes Kimi. Because Claude Code reads the same instruction files (`CLAUDE.md` → `AGENT_GUIDE.md`) regardless of the backend model, the OpenMontage flow works unchanged: pipeline selection, preflight, stage gates, everything. This is the better-tested route for this repo.

**[한국어]**

Claude Code는 Anthropic 호환 엔드포인트를 지원하고, Moonshot은 Kimi용 호환 엔드포인트를 제공합니다. Claude Code가 이 엔드포인트를 바라보게 설정하면 하니스는 Claude Code 그대로이고 모델만 Kimi로 바뀝니다. Claude Code는 백엔드 모델과 상관없이 같은 지시 파일(`CLAUDE.md` → `AGENT_GUIDE.md`)을 읽기 때문에, 파이프라인 선택부터 preflight, 단계별 게이트까지 OpenMontage의 작동 방식은 그대로 유지됩니다. 이 저장소에서는 가장 검증이 잘 된 경로입니다.

### Install Claude Code (Claude Code 설치하기)

Windows (PowerShell):

```powershell
# Install Node.js
winget install OpenJS.NodeJS

# Allow local scripts so npm global shims run
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

# Install Claude Code
npm install -g @anthropic-ai/claude-code
```

macOS / Linux:

```bash
npm install -g @anthropic-ai/claude-code
```

**[한국어]**

Windows (PowerShell):

```powershell
# Node.js 설치
winget install OpenJS.NodeJS

# npm 전역 shim이 실행되도록 로컬 스크립트 허용
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

# Claude Code 설치
npm install -g @anthropic-ai/claude-code
```

macOS / Linux:

```bash
npm install -g @anthropic-ai/claude-code
```

### Set environment variables (환경 변수 설정하기)

These commands apply to the current terminal session only. For a persistent setup, see the `settings.json` alternative below.

Windows PowerShell:

```powershell
# Point Claude Code at Moonshot's Anthropic-compatible endpoint
$env:ANTHROPIC_BASE_URL="https://api.moonshot.ai/anthropic"
# Your API key from platform.kimi.ai
$env:ANTHROPIC_AUTH_TOKEN="<your Moonshot API key>"
# Pin every model alias to Kimi
$env:ANTHROPIC_MODEL="kimi-k3[1m]"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL="kimi-k3[1m]"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL="kimi-k3[1m]"
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL="kimi-k3[1m]"
$env:ANTHROPIC_DEFAULT_FABLE_MODEL="kimi-k3[1m]"
# Subagents use the same model
$env:CLAUDE_CODE_SUBAGENT_MODEL="kimi-k3[1m]"
# The Kimi endpoint does not support tool search
$env:ENABLE_TOOL_SEARCH="false"
# Auto-compact window for the 1M-token kimi-k3 context (use 262144 for kimi-k2.7-code)
$env:CLAUDE_CODE_AUTO_COMPACT_WINDOW="1048576"
# Maximum effort level
$env:CLAUDE_CODE_EFFORT_LEVEL="max"
```

macOS / Linux (bash):

```bash
# Point Claude Code at Moonshot's Anthropic-compatible endpoint
export ANTHROPIC_BASE_URL="https://api.moonshot.ai/anthropic"
# Your API key from platform.kimi.ai
export ANTHROPIC_AUTH_TOKEN="<your Moonshot API key>"
# Pin every model alias to Kimi
export ANTHROPIC_MODEL="kimi-k3[1m]"
export ANTHROPIC_DEFAULT_OPUS_MODEL="kimi-k3[1m]"
export ANTHROPIC_DEFAULT_SONNET_MODEL="kimi-k3[1m]"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="kimi-k3[1m]"
export ANTHROPIC_DEFAULT_FABLE_MODEL="kimi-k3[1m]"
# Subagents use the same model
export CLAUDE_CODE_SUBAGENT_MODEL="kimi-k3[1m]"
# The Kimi endpoint does not support tool search
export ENABLE_TOOL_SEARCH="false"
# Auto-compact window for the 1M-token kimi-k3 context (use 262144 for kimi-k2.7-code)
export CLAUDE_CODE_AUTO_COMPACT_WINDOW="1048576"
# Maximum effort level
export CLAUDE_CODE_EFFORT_LEVEL="max"
```

If you choose `kimi-k2.7-code` instead of `kimi-k3`, set `CLAUDE_CODE_AUTO_COMPACT_WINDOW` to `262144`. In mainland China, replace the base URL with `https://api.moonshot.cn/anthropic`.

**[한국어]**

아래 명령은 현재 터미널 세션에만 적용됩니다. 영구적으로 적용하려면 다음 절의 `settings.json` 방식을 사용하십시오.

Windows PowerShell:

```powershell
# Claude Code가 Moonshot의 Anthropic 호환 엔드포인트를 사용하도록 지정
$env:ANTHROPIC_BASE_URL="https://api.moonshot.ai/anthropic"
# platform.kimi.ai에서 발급받은 API 키
$env:ANTHROPIC_AUTH_TOKEN="<your Moonshot API key>"
# 모든 모델 별칭을 Kimi로 고정
$env:ANTHROPIC_MODEL="kimi-k3[1m]"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL="kimi-k3[1m]"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL="kimi-k3[1m]"
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL="kimi-k3[1m]"
$env:ANTHROPIC_DEFAULT_FABLE_MODEL="kimi-k3[1m]"
# 서브에이전트도 같은 모델 사용
$env:CLAUDE_CODE_SUBAGENT_MODEL="kimi-k3[1m]"
# Kimi 엔드포인트는 tool search를 지원하지 않음
$env:ENABLE_TOOL_SEARCH="false"
# 1M 토큰 컨텍스트에 맞춘 자동 압축 창 (kimi-k2.7-code는 262144)
$env:CLAUDE_CODE_AUTO_COMPACT_WINDOW="1048576"
# 최대 effort level
$env:CLAUDE_CODE_EFFORT_LEVEL="max"
```

macOS / Linux (bash):

```bash
# Claude Code가 Moonshot의 Anthropic 호환 엔드포인트를 사용하도록 지정
export ANTHROPIC_BASE_URL="https://api.moonshot.ai/anthropic"
# platform.kimi.ai에서 발급받은 API 키
export ANTHROPIC_AUTH_TOKEN="<your Moonshot API key>"
# 모든 모델 별칭을 Kimi로 고정
export ANTHROPIC_MODEL="kimi-k3[1m]"
export ANTHROPIC_DEFAULT_OPUS_MODEL="kimi-k3[1m]"
export ANTHROPIC_DEFAULT_SONNET_MODEL="kimi-k3[1m]"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="kimi-k3[1m]"
export ANTHROPIC_DEFAULT_FABLE_MODEL="kimi-k3[1m]"
# 서브에이전트도 같은 모델 사용
export CLAUDE_CODE_SUBAGENT_MODEL="kimi-k3[1m]"
# Kimi 엔드포인트는 tool search를 지원하지 않음
export ENABLE_TOOL_SEARCH="false"
# 1M 토큰 컨텍스트에 맞춘 자동 압축 창 (kimi-k2.7-code는 262144)
export CLAUDE_CODE_AUTO_COMPACT_WINDOW="1048576"
# 최대 effort level
export CLAUDE_CODE_EFFORT_LEVEL="max"
```

`kimi-k3` 대신 `kimi-k2.7-code`를 사용한다면 `CLAUDE_CODE_AUTO_COMPACT_WINDOW`를 `262144`로 설정하십시오. 중국 본토에서는 base URL을 `https://api.moonshot.cn/anthropic`으로 바꿉니다.

### Persistent alternative: settings.json (영구 설정 대안: settings.json)

If you do not want to re-enter the variables every session, put them in an `env` block in `~/.claude/settings.json`:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.moonshot.ai/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "<your Moonshot API key>",
    "ANTHROPIC_MODEL": "kimi-k3[1m]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "kimi-k3[1m]",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "kimi-k3[1m]",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "kimi-k3[1m]",
    "ANTHROPIC_DEFAULT_FABLE_MODEL": "kimi-k3[1m]",
    "CLAUDE_CODE_SUBAGENT_MODEL": "kimi-k3[1m]",
    "ENABLE_TOOL_SEARCH": "false",
    "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "1048576",
    "CLAUDE_CODE_EFFORT_LEVEL": "max"
  }
}
```

The key is stored in plaintext, so do not commit this file. Restart Claude Code after saving. Keep in mind that `env` values in `settings.json` override terminal exports.

**[한국어]**

매 세션마다 변수를 다시 입력하고 싶지 않다면 `~/.claude/settings.json`의 `env` 블록에 넣으면 됩니다.

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.moonshot.ai/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "<your Moonshot API key>",
    "ANTHROPIC_MODEL": "kimi-k3[1m]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "kimi-k3[1m]",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "kimi-k3[1m]",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "kimi-k3[1m]",
    "ANTHROPIC_DEFAULT_FABLE_MODEL": "kimi-k3[1m]",
    "CLAUDE_CODE_SUBAGENT_MODEL": "kimi-k3[1m]",
    "ENABLE_TOOL_SEARCH": "false",
    "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "1048576",
    "CLAUDE_CODE_EFFORT_LEVEL": "max"
  }
}
```

키가 평문으로 저장되므로 이 파일을 git에 커밋하지 마십시오. 저장 후에는 Claude Code를 재시작해야 적용됩니다. `settings.json`의 `env` 값은 터미널 export보다 우선순위가 높다는 점도 기억해 두십시오.

### Verify the connection (연결 확인하기)

Run `claude`, then type `/status`. The Base URL must read `https://api.moonshot.ai/anthropic` and the model must show `kimi-k3[1m]`. Then send any message (for example `hi`) and expect a normal reply. The `/model` menu does not list Kimi models, so always verify with `/status`.

**[한국어]**

`claude`를 실행한 뒤 `/status`를 입력합니다. Base URL이 `https://api.moonshot.ai/anthropic`이고 모델이 `kimi-k3[1m]`으로 표시되어야 합니다. 이어서 아무 메시지(예: `hi`)를 보낸 뒤 정상적인 응답이 오는지 확인합니다. `/model` 메뉴에는 Kimi 모델이 표시되지 않으므로, 연결 확인은 반드시 `/status`로 합니다.

### Clean up legacy variables (레거시 변수 정리하기)

If you hit 401 errors, a legacy `ANTHROPIC_API_KEY` is usually conflicting with `ANTHROPIC_AUTH_TOKEN`. Remove the legacy key. Also clean stale `ANTHROPIC_*` entries in `~/.claude/settings.json` and in your shell profiles when switching providers, because a stale `settings.json` entry silently wins over your terminal exports.

**[한국어]**

401 오류가 발생하면 보통 예전 `ANTHROPIC_API_KEY`가 `ANTHROPIC_AUTH_TOKEN`과 충돌하는 경우입니다. 레거시 키를 제거하십시오. 또한 프로바이더를 바꿀 때는 `~/.claude/settings.json`과 셸 프로필 양쪽에서 오래된 `ANTHROPIC_*` 항목을 정리해야 합니다. `settings.json`에 남아 있는 값이 터미널 export를 조용히 덮어쓰는 경우가 흔합니다.

## 4. Path B: Kimi Code CLI (경로 B: Kimi Code CLI)

Kimi Code CLI is Moonshot's own single-binary terminal agent. It reads repo instruction files such as `AGENTS.md`, and since OpenMontage's `AGENTS.md` routes straight to `AGENT_GUIDE.md`, the same agent contract still applies. It ships with built-in subagents (coder, explore, plan) and MCP support. For this repo, Path A is the better-tested route; Path B is a valid alternative that follows the same contract.

Install (Windows PowerShell):

```powershell
irm https://code.kimi.com/kimi-code/install.ps1 | iex
```

Install (macOS / Linux):

```bash
curl -fsSL https://code.kimi.com/kimi-code/install.sh | bash
```

Alternative installers:

```bash
# Homebrew
brew install kimi-code

# npm (requires Node.js 22.19.0+)
npm install -g @moonshot-ai/kimi-code
```

First run: type `kimi`, then `/login` and choose Kimi Code OAuth or a Moonshot Open Platform API key. On Windows, Git for Windows is required because the CLI uses the bundled Git Bash as its shell; if Git is installed in a custom location, set `KIMI_SHELL_PATH` to your `bash.exe` path. Repo: https://github.com/MoonshotAI/kimi-code. Docs: https://www.kimi.com/code/docs

**[한국어]**

Kimi Code CLI는 Moonshot이 직접 만든 단일 바이너리 터미널 에이전트입니다. `AGENTS.md` 같은 저장소 지시 파일을 읽는데, OpenMontage의 `AGENTS.md`는 바로 `AGENT_GUIDE.md`로 연결되므로 동일한 에이전트 계약이 그대로 적용됩니다. coder, explore, plan 같은 내장 서브에이전트와 MCP를 지원합니다. 이 저장소 기준으로는 Path A가 더 검증된 경로이고, Path B는 같은 계약을 따르는 유효한 대안입니다.

설치 (Windows PowerShell):

```powershell
irm https://code.kimi.com/kimi-code/install.ps1 | iex
```

설치 (macOS / Linux):

```bash
curl -fsSL https://code.kimi.com/kimi-code/install.sh | bash
```

다른 설치 방법:

```bash
# Homebrew
brew install kimi-code

# npm (Node.js 22.19.0 이상 필요)
npm install -g @moonshot-ai/kimi-code
```

첫 실행: `kimi`를 입력한 뒤 `/login`에서 Kimi Code OAuth 또는 Moonshot Open Platform API 키를 선택합니다. Windows에서는 Git for Windows가 필요합니다. CLI가 Git에 포함된 Git Bash를 셸로 사용하기 때문입니다. Git이 다른 위치에 설치되어 있다면 `KIMI_SHELL_PATH`를 해당 `bash.exe` 경로로 설정하십시오. 저장소: https://github.com/MoonshotAI/kimi-code. 문서: https://www.kimi.com/code/docs

## 5. After Connecting: Make Your First Video (연결 후: 첫 번째 영상 만들기)

Whichever path you chose, swapping the brain does not touch the Python side. From the repo root, confirm the preflight command works:

```bash
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu_summary(), indent=2))"
```

The output is your real capability menu: which media providers are configured. That list comes from your `.env` provider keys, not from Kimi. Now ask for a video in plain language. A Korean example prompt:

"블랙홀에 대해 60초짜리 설명 영상을 만들어 줘" ("Make a 60-second explainer about black holes.")

The agent will follow the `AGENT_GUIDE.md` flow: pipeline selection, preflight, concept proposals, approval gates, then production.

**[한국어]**

어느 경로를 택했든 두뇌를 바꿔도 Python 쪽은 그대로입니다. 저장소 루트에서 preflight 명령이 동작하는지 확인해 보십시오.

```bash
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu_summary(), indent=2))"
```

출력 결과는 현재 설정된 미디어 프로바이더 메뉴입니다. 이 목록은 Kimi가 아니라 `.env`의 프로바이더 키에서 나옵니다. 이제 자연어로 영상을 요청하면 됩니다. 한국어 예시 프롬프트입니다.

"블랙홀에 대해 60초짜리 설명 영상을 만들어 줘"

에이전트는 `AGENT_GUIDE.md`의 흐름대로 파이프라인 선택, preflight, 콘셉트 제안, 승인 게이트를 거쳐 제작을 진행합니다.

## 6. Model Choice and Cost (모델 선택과 비용)

`kimi-k3[1m]` is the default recommendation. To switch models, change `ANTHROPIC_MODEL` and the `ANTHROPIC_DEFAULT_*` variables to the model id you want.

| Model | Context | Best for | Notes |
|-------|---------|----------|-------|
| `kimi-k3[1m]` | 1M tokens (1048576) | Default recommendation | Thinking on by default; works out of the box; released 2026-07-16 |
| `kimi-k2.7-code` | 256K | Cheaper coding-optimized option | Requires thinking enabled in Claude Code (press Tab until "Thinking on"); without it requests fail with "400 invalid thinking" and WebSearch breaks. Set `CLAUDE_CODE_AUTO_COMPACT_WINDOW` to `262144` |
| `kimi-k2.7-code-highspeed` | 256K | Same as k2.7-code, faster | Roughly 5-6x faster output; same thinking requirement |
| `kimi-k2.6` | 256K | Latency-sensitive simple tasks | Thinking optional |

Pricing (as of July 2026, check the platform for current rates):

| Model | Input (per 1M tokens) | Cached input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------------|------------------------|
| `kimi-k3` | $3.00 | $0.30 | $15.00 |
| `kimi-k2.7-code` | $0.95 | — | $4.00 |
| `kimi-k2.6` | $0.95 | — | $4.00 |
| `kimi-k2.5` | $0.60 | — | $3.00 |

**[한국어]**

기본 추천 모델은 `kimi-k3[1m]`입니다. 모델을 바꾸려면 `ANTHROPIC_MODEL`과 `ANTHROPIC_DEFAULT_*` 변수를 원하는 모델 id로 변경하십시오.

| 모델 | 컨텍스트 | 용도 | 비고 |
|------|----------|------|------|
| `kimi-k3[1m]` | 1M 토큰 (1048576) | 기본 추천 | thinking이 기본 활성화되어 별도 설정 없이 동작, 2026-07-16 출시 |
| `kimi-k2.7-code` | 256K | 더 저렴한 코딩 특화 옵션 | Claude Code에서 thinking을 켜야 함(Tab을 눌러 "Thinking on" 표시). 끄면 "400 invalid thinking" 오류가 나고 WebSearch가 깨짐. `CLAUDE_CODE_AUTO_COMPACT_WINDOW`는 `262144`로 설정 |
| `kimi-k2.7-code-highspeed` | 256K | k2.7-code와 동일하되 더 빠른 출력 | 출력 속도 약 5-6배, thinking 요구 사항 동일 |
| `kimi-k2.6` | 256K | 지연 시간에 민감한 간단한 작업 | thinking 선택 사항 |

가격 (2026년 7월 기준이며, 최신 요금은 플랫폼에서 확인하십시오):

| 모델 | 입력 (100만 토큰당) | 캐시된 입력 (100만 토큰당) | 출력 (100만 토큰당) |
|------|--------------------|--------------------------|--------------------|
| `kimi-k3` | $3.00 | $0.30 | $15.00 |
| `kimi-k2.7-code` | $0.95 | — | $4.00 |
| `kimi-k2.6` | $0.95 | — | $4.00 |
| `kimi-k2.5` | $0.60 | — | $3.00 |

## 7. Limitations and Caveats (제한 사항과 주의점)

- Tool search is not supported on the Kimi endpoint, so `ENABLE_TOOL_SEARCH` must stay `"false"` (already set in the env blocks above).
- WebFetch is not supported on the Kimi endpoint. Workaround: paste the page content into chat or use an MCP scraping tool.
- The `/model` menu in Claude Code does not list Kimi models. Verify your connection with `/status` instead.
- On 401 errors, remove any legacy `ANTHROPIC_API_KEY` that conflicts with `ANTHROPIC_AUTH_TOKEN`.
- `env` values in `~/.claude/settings.json` override terminal exports. When switching providers, clean stale `ANTHROPIC_*` entries in `settings.json` and in your shell profiles.

**[한국어]**

- Kimi 엔드포인트는 tool search를 지원하지 않으므로 `ENABLE_TOOL_SEARCH`는 반드시 `"false"`여야 합니다(위 env 블록에 이미 포함되어 있습니다).
- Kimi 엔드포인트에서는 WebFetch를 사용할 수 없습니다. 페이지 내용을 채팅에 붙여 넣거나 MCP 스크래핑 도구를 사용하는 방법으로 우회하십시오.
- Claude Code의 `/model` 메뉴에는 Kimi 모델이 표시되지 않습니다. `/status`로 연결을 확인하십시오.
- 401 오류가 발생하면 `ANTHROPIC_AUTH_TOKEN`과 충돌하는 레거시 `ANTHROPIC_API_KEY`를 제거하십시오.
- `~/.claude/settings.json`의 `env` 값은 터미널 export보다 우선합니다. 프로바이더를 전환할 때는 `settings.json`과 셸 프로필의 오래된 `ANTHROPIC_*` 항목을 정리하십시오.

## 8. Sources (출처)

This guide is based on the following Moonshot documentation and pricing references (checked July 2026):

- https://platform.kimi.ai/docs/guide/claude-code-kimi
- https://github.com/MoonshotAI/kimi-code
- https://www.kimi.com/code/docs/en/kimi-code-cli/guides/getting-started.html
- https://benchlm.ai/moonshot/api-pricing

**[한국어]**

이 가이드는 다음 Moonshot 문서와 요금 자료를 기반으로 작성했습니다(2026년 7월 확인).

- https://platform.kimi.ai/docs/guide/claude-code-kimi
- https://github.com/MoonshotAI/kimi-code
- https://www.kimi.com/code/docs/en/kimi-code-cli/guides/getting-started.html
- https://benchlm.ai/moonshot/api-pricing
