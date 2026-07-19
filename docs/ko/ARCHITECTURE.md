> 이 문서는 이중 언어 문서입니다. 각 섹션에서 영어 원문이 먼저 나오고, **[한국어]** 표시 아래에 한국어 번역이 이어집니다.

> 원본: docs/ARCHITECTURE.md @ 8e1128400b40eb5b17c73785a525d63ee35bfcda

# OpenMontage Architecture (OpenMontage 아키텍처)

> Last updated: 2026-03-28 | Derived from code exploration, not prior documentation.

OpenMontage is an **agent-orchestrated video production platform**. An LLM coding assistant (Claude Code, Cursor, Copilot, etc.) acts as the orchestrator — reading pipeline manifests, following skill instructions, calling Python tools, and checkpointing state. There is no runtime Python orchestrator; the agent _is_ the control plane.

**[한국어]**

> 최종 업데이트: 2026-03-28 | 기존 문서가 아닌 코드 탐색을 통해 작성됨

OpenMontage는 **에이전트가 오케스트라하는 영상 제작 플랫폼**입니다. LLM 코딩 어시스턴트(Claude Code, Cursor, Copilot 등)가 오케스트레이터 역할을 합니다. 파이프라인 매니페스트를 읽고, 스킬 지시를 따르며, Python 도구를 호출하고 상태를 체크포인팅합니다. 별도의 Python 런타임 오케스트레이터는 없으며, 에이전트가 곧 제어 평면입니다.

---

## High-Level Flow (상위 수준 흐름)

```
User gives topic/idea
        |
        v
Agent reads pipeline manifest (YAML)
        |
        v
For each stage:
   1. Agent reads stage-director skill (Markdown)
   2. Agent calls Python tools via tool registry
   3. Agent writes checkpoint (JSON) with artifacts
   4. Agent self-reviews using meta/reviewer skill
   5. Human approval gate (if configured)
        |
        v
Final video output
```

**[한국어]**

```
사용자가 주제/아이디어를 제시
        |
        v
에이전트가 파이프라인 매니페스트를 읽음 (YAML)
        |
        v
각 단계마다:
   1. 에이전트가 스테이지 디렉터 스킬을 읽음 (Markdown)
   2. 에이전트가 툴 레지스트리를 통해 Python 도구를 호출
   3. 에이전트가 체크포인트를 작성 (JSON) 및 산출물과 함께
   4. 에이전트가 meta/reviewer 스킬을 사용한 자체 검토
   5. 사람 승인 게이트 (설정된 경우)
        |
        v
최종 영상 출력
```

---

## Repository Layout (저장소 레이아웃)

```
OpenMontage/
├── lib/                    # Core runtime infrastructure (Python)
│   ├── config_model.py     # Pydantic config: LLM, budget, checkpoint, output, paths
│   ├── checkpoint.py       # Pipeline state persistence & stage transitions
│   ├── pipeline_loader.py  # YAML manifest loading & validation
│   ├── media_profiles.py   # Platform-specific render profiles (YouTube, TikTok, etc.)
│   ├── env_loader.py       # .env variable management
│   └── providers/          # (Reserved for future provider abstractions)
│
├── tools/                  # 57+ Python tool implementations
│   ├── base_tool.py        # Abstract base class — the tool contract
│   ├── tool_registry.py    # Auto-discovery singleton registry
│   ├── cost_tracker.py     # Budget governance (estimate → reserve → reconcile)
│   ├── analysis/           # Transcription, scene detection, frame sampling, video understanding
│   ├── audio/              # TTS (ElevenLabs, OpenAI, Piper), music gen, mixing, enhancement
│   ├── avatar/             # Talking head animation, lip sync
│   ├── enhancement/        # Upscale, bg removal, face enhance/restore, color grading
│   ├── graphics/           # Image gen (FLUX, GPT Image, Recraft, local diffusion), stock, diagrams, code snippets, math animation
│   ├── publishers/         # (Reserved)
│   ├── subtitle/           # SRT/VTT generation from timestamps
│   └── video/              # 13 video gen providers, composition, stitching, trimming
│
├── pipeline_defs/          # YAML pipeline manifests
├── schemas/                # JSON Schema definitions for validation
│   ├── artifacts/          # 11 artifact schemas (brief → publish_log)
│   ├── checkpoints/        # Checkpoint state schema
│   ├── pipelines/          # Pipeline manifest schema
│   ├── styles/             # Style playbook schema
│   └── tools/              # Tool-specific schemas
│
├── skills/                 # Layer 2: OpenMontage-specific agent instructions
│   ├── core/               # FFmpeg, Remotion, WhisperX, color grading skills
│   ├── creative/           # Video editing, enhancement, data viz, prompt engineering
│   ├── meta/               # reviewer, checkpoint-protocol, skill-creator
│   └── pipelines/          # Per-pipeline stage-director skills
│
├── .agents/skills/         # Layer 3: external technology skills (FFmpeg, HyperFrames, GSAP, etc.)
├── styles/                 # Visual style playbooks (YAML) + loader
├── remotion-composer/      # Node.js/React — Remotion video composition renderer
├── tests/                  # Contract tests, QA integration tests, eval harness
├── docs/                   # Best-practices guides, session handoffs, audits
└── config.yaml             # Global runtime configuration
```

**[한국어]**

```
OpenMontage/
├── lib/                    # 핵심 런타임 인프라 (Python)
│   ├── config_model.py     # Pydantic 설정: LLM, 예산, 체크포인트, 출력, 경로
│   ├── checkpoint.py       # 파이프라인 상태 지속성 및 단계 전이
│   ├── pipeline_loader.py  # YAML 매니페스트 로딩 및 검증
│   ├── media_profiles.py   # 플랫폼별 렌더 프로필 (YouTube, TikTok 등)
│   ├── env_loader.py       # .env 변수 관리
│   └── providers/          # (향후 프로바이더 추상화를 위해 예약됨)
│
├── tools/                  # 57개 이상의 Python 도구 구현
│   ├── base_tool.py        # 추상 기본 클래스 — 도구 계약
│   ├── tool_registry.py    # 자동 발견 싱글톤 레지스트리
│   ├── cost_tracker.py     # 예산 관리 (추정 → 예약 → 정산)
│   ├── analysis/           # 전사, 장면 감지, 프레임 샘플링, 비디오 이해
│   ├── audio/              # TTS (ElevenLabs, OpenAI, Piper), 음악 생성, 믹싱, 향상
│   ├── avatar/             # 토킹 헤드 애니메이션, 립싱크
│   ├── enhancement/        # 업스케일, 배경 제거, 얼굴 향상/복원, 색 보정
│   ├── graphics/           # 이미지 생성 (FLUX, GPT Image, Recraft, 로컬 디퓨전), 스톡, 다이어그램, 코드 스니펫, 수학 애니메이션
│   ├── publishers/         # (예약됨)
│   ├── subtitle/           # 타임스탬프에서 SRT/VTT 생성
│   └── video/              # 13개 비디오 생성 프로바이더, 컴포지션, 스티칭, 자르기
│
├── pipeline_defs/          # YAML 파이프라인 매니페스트
├── schemas/                # 검증을 위한 JSON 스키마 정의
│   ├── artifacts/          # 11개 산출물 스키마 (brief → publish_log)
│   ├── checkpoints/        # 체크포인트 상태 스키마
│   ├── pipelines/          # 파이프라인 매니페스트 스키마
│   ├── styles/             # 스타일 플레이북 스키마
│   └── tools/              # 도구별 스키마
│
├── skills/                 # 레이어 2: OpenMontage 전용 에이전트 지시
│   ├── core/               # FFmpeg, Remotion, WhisperX, 색 보정 스킬
│   ├── creative/           # 비디오 편집, 향상, 데이터 시각화, 프롬프트 엔지니어링
│   ├── meta/               # reviewer, checkpoint-protocol, skill-creator
│   └── pipelines/          # 파이프라인별 스테이지 디렉터 스킬
│
├── .agents/skills/         # 레이어 3: 외부 기술 스킬 (FFmpeg, HyperFrames, GSAP 등)
├── styles/                 # 시각적 스타일 플레이북 (YAML) + 로더
├── remotion-composer/      # Node.js/React — Remotion 비디오 컴포지션 렌더러
├── tests/                  # 계약 테스트, QA 통합 테스트, eval 하니스
├── docs/                   # 모범 사례 가이드, 세션 핸드오프, 감사
└── config.yaml             # 전역 런타임 설정
```

---

## Core Architectural Principles (핵심 아키텍처 원칙)

### 1. Agent-First Orchestration (에이전트 우선 오케스트레이션)

There is **no Python orchestrator**. The LLM agent:
- Reads the pipeline manifest to know the stage order
- Reads each stage-director skill for detailed instructions
- Calls tools, evaluates results, makes creative decisions
- Writes checkpoints to persist state between stages

Python provides **tools and persistence only**. All intelligence lives in skill instructions (Markdown) and pipeline manifests (YAML).

**[한국어]**

**Python 오케스트레이터는 없습니다**. LLM 에이전트는 다음을 수행합니다.
- 파이프라인 매니페스트를 읽어 단계 순서를 파악
- 각 스테이지 디렉터 스킬을 읽어 상세한 지시를 확인
- 도구를 호출하고 결과를 평가하며 창의적 결정을 내림
- 단계 간 상태 지속을 위해 체크포인트를 작성

Python은 **도구와 지속성만 제공**합니다. 모든 지능은 스킬 지시(Markdown)와 파이프라인 매니페스트(YAML)에 있습니다.

### 2. No LLM API Key in Runtime (런타임에 LLM API 키 없음)

OpenMontage does not call LLM APIs at runtime. The coding assistant running in the user's IDE _is_ the LLM. Tools that need generation (images, video, TTS) call domain-specific APIs directly (ElevenLabs, fal.ai, HeyGen, etc.), not general-purpose LLM endpoints.

**[한국어]**

OpenMontage는 런타임에 LLM API를 호출하지 않습니다. 사용자 IDE에서 실행 중인 코딩 어시스턴트가 곧 LLM입니다. 생성이 필요한 도구(이미지, 비디오, TTS)는 일반용 LLM 엔드포인트가 아닌 도메인별 API(ElevenLabs, fal.ai, HeyGen 등)를 직접 호출합니다.

### 3. Dual-Provider Support (이중 프로바이더 지원)

Every capability must support both **API providers** (cloud, paid) and **local/open-source alternatives** (free, GPU-dependent). The selector pattern enforces this by routing to whatever is available.

**[한국어]**

모든 기능은 **API 프로바이더**(클라우드, 유료)와 **로컬/오픈소스 대안**(무료, GPU 종속)을 모두 지원해야 합니다. 셀렉터 패턴은 사용 가능한 것으로 라우팅함으로써 이를 강제합니다.

---

## The Tool System (도구 시스템)

### BaseTool Contract (BaseTool 계약)

All tools inherit from `BaseTool` (ABC) and declare:

| Field | Purpose |
|-------|---------|
| `name`, `version` | Identity |
| `tier` | CORE, VOICE, ENHANCE, GENERATE, SOURCE, ANALYZE, PUBLISH |
| `capability` | What it does (e.g., `tts`, `image_generation`, `video_post`) |
| `provider` | Which service (e.g., `elevenlabs`, `ffmpeg`, `selector`) |
| `runtime` | LOCAL, LOCAL_GPU, API, HYBRID |
| `stability` | EXPERIMENTAL, BETA, PRODUCTION |
| `dependencies` | Required binaries (`cmd:ffmpeg`), env vars (`env:ELEVENLABS_API_KEY`), Python packages (`python:torch`) |
| `input_schema`, `output_schema` | JSON Schema for inputs/outputs |
| `fallback_tools` | Ordered fallback chain |
| `agent_skills` | Links to Layer 3 knowledge skills |
| `resource_profile` | CPU, RAM, VRAM, disk, network requirements |
| `retry_policy` | Max retries, backoff strategy |

**Required method:** `execute(inputs) -> ToolResult`

`ToolResult` carries: `success`, `data`, `artifacts` (file paths), `error`, `cost_usd`, `duration_seconds`, `seed`, `model`.

**[한국어]**

모든 도구는 `BaseTool`(ABC)에서 상속받고 다음을 선언합니다.

| 필드 | 목적 |
|------|------|
| `name`, `version` | 식별자 |
| `tier` | CORE, VOICE, ENHANCE, GENERATE, SOURCE, ANALYZE, PUBLISH |
| `capability` | 수행 기능 (예: `tts`, `image_generation`, `video_post`) |
| `provider` | 서비스 (예: `elevenlabs`, `ffmpeg`, `selector`) |
| `runtime` | LOCAL, LOCAL_GPU, API, HYBRID |
| `stability` | EXPERIMENTAL, BETA, PRODUCTION |
| `dependencies` | 필수 바이너리 (`cmd:ffmpeg`), 환경 변수 (`env:ELEVENLABS_API_KEY`), Python 패키지 (`python:torch`) |
| `input_schema`, `output_schema` | 입출력용 JSON 스키마 |
| `fallback_tools` | 순서 대체 체인 |
| `agent_skills` | 레이어 3 지식 스킬 링크 |
| `resource_profile` | CPU, RAM, VRAM, 디스크, 네트워크 요구 사항 |
| `retry_policy` | 최대 재시도 횟수, 백오프 전략 |

**필수 메서드:** `execute(inputs) -> ToolResult`

`ToolResult`는 다음을 포함합니다: `success`, `data`, `artifacts` (파일 경로), `error`, `cost_usd`, `duration_seconds`, `seed`, `model`.

### Tool Registry (도구 레지스트리)

`ToolRegistry` is a singleton that auto-discovers all `BaseTool` subclasses via `pkgutil.walk_packages()`. No manual registration.

Key queries:
- `get_by_capability("tts")` — all TTS tools
- `get_by_provider("elevenlabs")` — all ElevenLabs tools
- `get_available()` — tools whose dependencies are satisfied
- `find_fallback("elevenlabs_tts")` — resolve fallback chain
- `support_envelope()` — full capability report for agent consumption
- `gpu_required_tools()`, `network_required_tools()`

**[한국어]**

`ToolRegistry`는 `pkgutil.walk_packages()`를 통해 모든 `BaseTool` 서브클래스를 자동으로 발견하는 싱글톤입니다. 수동 등록이 필요 없습니다.

주요 쿼리:
- `get_by_capability("tts")` — 모든 TTS 도구
- `get_by_provider("elevenlabs")` — 모든 ElevenLabs 도구
- `get_available()` — 의존성이 충족된 도구
- `find_fallback("elevenlabs_tts")` — 대체 체인 해결
- `support_envelope()` — 에이전트 사용을 위한 전체 기능 보고
- `gpu_required_tools()`, `network_required_tools()`

### Selector Pattern (셀렉터 패턴)

Three selector tools abstract multi-provider capabilities:

| Selector | Capability | How selection works |
|----------|-----------|---------------------|
| `tts_selector` | Text-to-speech | Ranks discovered providers by task fit, quality, control, reliability, cost, latency, and continuity |
| `image_selector` | Image generation | Ranks discovered providers from the live registry; no hardcoded provider order |
| `video_selector` | Video generation | Ranks discovered providers from the live registry; user preference is respected when explicitly provided |

Selectors route based on: user preference when explicitly set, then scored ranking across available providers. They adapt input schemas between providers transparently.

**[한국어]**

세 가지 셀렉터 도구가 다중 프로바이더 기능을 추상화합니다.

| 셀렉터 | 기능 | 선택 방식 |
|--------|------|-----------|
| `tts_selector` | 텍스트 음성 변환 | 발견된 프로바이더를 작업 적합성, 품질, 제어, 신뢰성, 비용, 지연 시간, 연속성으로 순위 매김 |
| `image_selector` | 이미지 생성 | 라이브 레지스트리에서 발견된 프로바이더를 순위 매김. 하드코딩된 프로바이더 순서 없음 |
| `video_selector` | 비디오 생성 | 라이브 레지스트리에서 발견된 프로바이더를 순위 매김. 명시적으로 제공된 경우 사용자 선호를 존중 |

셀렉터는 명시적으로 설정된 사용자 선호를 우선으로 하고, 그 다음 사용 가능한 프로바이더 간 순위 매김으로 라우팅합니다. 프로바이더 간 입력 스키마를 투명하게 변환합니다.

### Tool Inventory by Category (카테고리별 도구 목록)

**Analysis (4):** transcriber (WhisperX), scene_detect, frame_sampler, video_understand (CLIP/BLIP-2)

**Audio (8):** elevenlabs_tts, google_tts, openai_tts, piper_tts, tts_selector, music_gen, audio_mixer, audio_enhance

**Avatar (2):** talking_head (SadTalker/MuseTalk), lip_sync (Wav2Lip)

**Enhancement (5):** upscale (Real-ESRGAN), bg_remove (rembg/U2Net), face_enhance, face_restore (CodeFormer/GFPGAN), color_grade (FFmpeg LUTs)

**Graphics (13):** flux_image, grok_image, google_imagen, openai_image, recraft_image, local_diffusion, pexels_image, pixabay_image, image_selector, code_snippet, diagram_gen, math_animate (ManimCE), image_gen (deprecated)

**Subtitle (1):** subtitle_gen

**Video (18):** grok_video, heygen_video, higgsfield_video, veo_video, kling_video, runway_video, minimax_video, wan_video, hunyuan_video, cogvideo_video, ltx_video_local, ltx_video_modal, pexels_video, pixabay_video, video_selector, video_compose (FFmpeg), video_stitch, video_trimmer

**[한국어]**

**분석 (4개):** transcriber (WhisperX), scene_detect, frame_sampler, video_understand (CLIP/BLIP-2)

**오디오 (8개):** elevenlabs_tts, google_tts, openai_tts, piper_tts, tts_selector, music_gen, audio_mixer, audio_enhance

**아바타 (2개):** talking_head (SadTalker/MuseTalk), lip_sync (Wav2Lip)

**향상 (5개):** upscale (Real-ESRGAN), bg_remove (rembg/U2Net), face_enhance, face_restore (CodeFormer/GFPGAN), color_grade (FFmpeg LUTs)

**그래픽 (13개):** flux_image, grok_image, google_imagen, openai_image, recraft_image, local_diffusion, pexels_image, pixabay_image, image_selector, code_snippet, diagram_gen, math_animate (ManimCE), image_gen (deprecated)

**자막 (1개):** subtitle_gen

**비디오 (18개):** grok_video, heygen_video, higgsfield_video, veo_video, kling_video, runway_video, minimax_video, wan_video, hunyuan_video, cogvideo_video, ltx_video_local, ltx_video_modal, pexels_video, pixabay_video, video_selector, video_compose (FFmpeg), video_stitch, video_trimmer

---

## Pipeline System (파이프라인 시스템)

### Pipeline Manifests (파이프라인 매니페스트)

Each pipeline is a YAML file in `pipeline_defs/` defining:

```yaml
name: animated-explainer
version: "2.0"
category: generated          # talking_head | generated | hybrid | screen_recording | animation | cinematic | custom
default_checkpoint_policy: guided

orchestration:
  mode: executive-producer
  skill: pipelines/explainer/executive-producer
  budget_default_usd: 2.00
  max_revisions_per_stage: 3

compatible_playbooks:
  - clean-professional
  - flat-motion-graphics

stages:
  - name: research
    skill: pipelines/explainer/research-director
    produces: [research_brief]
    tools_available: []
    checkpoint_required: false
    human_approval_default: false
    review_focus: [...]
    success_criteria: [...]
  # ... through publish
```

**[한국어]**

각 파이프라인은 `pipeline_defs/`에 있는 YAML 파일로 다음을 정의합니다.

```yaml
name: animated-explainer
version: "2.0"
category: generated          # talking_head | generated | hybrid | screen_recording | animation | cinematic | custom
default_checkpoint_policy: guided

orchestration:
  mode: executive-producer
  skill: pipelines/explainer/executive-producer
  budget_default_usd: 2.00
  max_revisions_per_stage: 3

compatible_playbooks:
  - clean-professional
  - flat-motion-graphics

stages:
  - name: research
    skill: pipelines/explainer/research-director
    produces: [research_brief]
    tools_available: []
    checkpoint_required: false
    human_approval_default: false
    review_focus: [...]
    success_criteria: [...]
  # ... through publish
```

### Available Pipelines (사용 가능한 파이프라인)

| Pipeline | Category | Description |
|----------|----------|-------------|
| `animated-explainer` | generated | AI-produced explainer with research, narration, visuals, music |
| `animation` | animation | Motion graphics, kinetic typography |
| `avatar-spokesperson` | talking_head | Avatar-driven presenter videos |
| `character-animation` | animation | Local rigged cartoon characters with SVG rigs, pose libraries, GSAP timelines, and HyperFrames rendering |
| `cinematic` | cinematic | Trailer, teaser, mood-driven edits |
| `clip-factory` | custom | Batch short-form clips from long source |
| `hybrid` | hybrid | Source footage + AI-generated support visuals |
| `localization-dub` | custom | Subtitle, dub, and translate existing video |
| `podcast-repurpose` | hybrid | Podcast highlights to video |
| `screen-demo` | screen_recording | Software screen recordings and walkthroughs |
| `talking-head` | talking_head | Footage-led speaker videos |
| `framework-smoke` | custom | Minimal smoke test for framework validation |

**[한국어]**

| 파이프라인 | 카테고리 | 설명 |
|-----------|----------|------|
| `animated-explainer` | generated | 리서치, 내레이션, 시각, 음악이 있는 AI 제작 설명 영상 |
| `animation` | animation | 모션 그래픽, 키네틱 타이포그래피 |
| `avatar-spokesperson` | talking_head | 아바타 기반 발표자 영상 |
| `character-animation` | animation | SVG 리그, 포즈 라이브러리, GSAP 타임라인, HyperFrames 렌더링을 갖춘 로컬 리깅 캐릭터 |
| `cinematic` | cinematic | 트레일러, 티저, 분위기 기반 편집 |
| `clip-factory` | custom | 긴 소스에서 일괄 단편 클립 생성 |
| `hybrid` | hybrid | 소스 영상 + AI 생성 보조 시각 |
| `localization-dub` | custom | 기존 비디오의 자막, 더빙, 번역 |
| `podcast-repurpose` | hybrid | 팟캐스트 하이라이트를 비디오로 |
| `screen-demo` | screen_recording | 소프트웨어 화면 녹화 및 데모 |
| `talking-head` | talking_head | 영상 기반 스피커 비디오 |
| `framework-smoke` | custom | 프레임워크 검증을 위한 최소 스모크 테스트 |

### Standard Stage Progression (표준 단계 진행)

Most production pipelines follow a canonical 8-stage flow:

```
research → proposal → script → scene_plan → assets → edit → compose → publish
```

Each stage:
1. Has a **stage-director skill** (Markdown instructions for the agent)
2. Declares **tools_available** (what the agent can call)
3. **Produces** one or more canonical artifacts
4. Has **review_focus** criteria and **success_criteria**
5. Can require **human approval** before proceeding

Specialized pipelines may insert domain-specific stages. For example,
`character-animation` adds `character_design` and `rig_plan` before
`scene_plan`, then emits a HyperFrames workspace and final deliverable at
`projects/<project-name>/renders/final.mp4`.

**[한국어]**

대부분의 제작 파이프라인은 표준 8단계 흐름을 따릅니다.

```
research → proposal → script → scene_plan → assets → edit → compose → publish
```

각 단계는 다음을 포함합니다.
1. **스테이지 디렉터 스킬** (에이전트용 Markdown 지시)
2. **tools_available** 선언 (에이전트가 호출할 수 있는 것)
3. 하나 이상의 표준 **산출물 생성**
4. **review_focus** 기준과 **success_criteria**
5. 진행 전 **사람 승인** 요구 가능

특화된 파이프라인은 도메인별 단계를 삽입할 수 있습니다. 예를 들어 `character-animation`은 `scene_plan` 전에 `character_design`과 `rig_plan`을 추가하고, `projects/<project-name>/renders/final.mp4`에 HyperFrames 작업 공간과 최종 산출물을 내보냅니다.

---

## Checkpoint System (체크포인트 시스템)

Checkpoints persist pipeline state as JSON in the project's `pipeline/` directory.

```json
{
  "version": "1.0",
  "project_id": "my-video",
  "stage": "script",
  "status": "completed",
  "timestamp": "2026-03-28T10:00:00Z",
  "checkpoint_policy": "guided",
  "human_approval_required": false,
  "human_approved": true,
  "artifacts": { "script": { ... } },
  "review": { ... },
  "cost_snapshot": { ... }
}
```

**Status values:** `pending` | `in_progress` | `awaiting_human` | `completed` | `failed`

**Checkpoint policies:**
- `guided` — checkpoint at key creative stages, auto-proceed on mechanical ones
- `manual_all` — human approval at every stage
- `auto_noncreative` — auto-proceed unless stage is creative (assets, edit)

**Functions:** `write_checkpoint()`, `read_checkpoint()`, `get_latest_checkpoint()`, `get_completed_stages()`, `get_next_stage()`

**[한국어]**

체크포인트는 프로젝트의 `pipeline/` 디렉토리에 파이프라인 상태를 JSON으로 지속합니다.

```json
{
  "version": "1.0",
  "project_id": "my-video",
  "stage": "script",
  "status": "completed",
  "timestamp": "2026-03-28T10:00:00Z",
  "checkpoint_policy": "guided",
  "human_approval_required": false,
  "human_approved": true,
  "artifacts": { "script": { ... } },
  "review": { ... },
  "cost_snapshot": { ... }
}
```

**상태 값:** `pending` | `in_progress` | `awaiting_human` | `completed` | `failed`

**체크포인트 정책:**
- `guided` — 핵심 창의 단계에서 체크포인트, 기계적 단계는 자동 진행
- `manual_all` — 모든 단계에서 사람 승인
- `auto_noncreative` — 창의 단계(assets, edit)가 아니면 자동 진행

**함수:** `write_checkpoint()`, `read_checkpoint()`, `get_latest_checkpoint()`, `get_completed_stages()`, `get_next_stage()`

### Canonical Artifacts (11 types, all JSON-schema validated) (표준 산출물 11개, 모두 JSON 스키마 검증)

| Artifact | Stage | Contains |
|----------|-------|----------|
| `research_brief` | research | Landscape analysis, data points, audience insights, angles |
| `proposal_packet` | proposal | Concept options, production plan, cost estimates, approval gate |
| `brief` | idea | Title, hook, key points, tone, style, platform, duration |
| `script` | script | Timestamped sections with enhancement cues, pronunciation guides |
| `scene_plan` | scene_plan | Scene definitions with type, description, timing |
| `asset_manifest` | assets | Generated assets with path, source tool, scene association |
| `edit_decisions` | edit | Editorial cuts with in/out timings |
| `render_report` | compose | Output metadata (format, resolution, duration) |
| `publish_log` | publish | Platform publication entries with status |
| `review` | (any) | Reviewer feedback and approval records |
| `cost_log` | (any) | Budget tracking entries |

**[한국어]**

| 산출물 | 단계 | 포함 내용 |
|--------|------|-----------|
| `research_brief` | research | 현황 분석, 데이터 포인트, 대중 통찰, 각도 |
| `proposal_packet` | proposal | 콘셉트 옵션, 제작 계획, 비용 추정, 승인 게이트 |
| `brief` | idea | 제목, 후크, 핵심 포인트, 어조, 스타일, 플랫폼, 지속 시간 |
| `script` | script | 향상 큐와 발음 가이드가 있는 타임스탬프 섹션 |
| `scene_plan` | scene_plan | 유형, 설명, 타이밍이 있는 장면 정의 |
| `asset_manifest` | assets | 경로, 소스 도구, 장면 연결이 있는 생성 에셋 |
| `edit_decisions` | edit | 인/아웃 타이밍이 있는 편집 컷 |
| `render_report` | compose | 출력 메타데이터 (형식, 해상도, 지속 시간) |
| `publish_log` | publish | 상태가 있는 플랫폼 게시 항목 |
| `review` | (any) | 검토자 피드백 및 승인 기록 |
| `cost_log` | (any) | 예산 추적 항목 |

---

## Budget Governance (예산 관리)

The `CostTracker` enforces spending controls across the pipeline.

### Lifecycle

```
estimate(tool, operation, $) → entry_id
        |
reserve(entry_id)          # locks budget
        |
reconcile(entry_id, $)     # records actual spend
```

### Budget Modes

| Mode | Behavior |
|------|----------|
| `observe` | Track costs, no enforcement |
| `warn` | Log warnings on overruns, allow execution |
| `cap` | Reject operations that exceed remaining budget |

### Controls
- **Total budget** (default: $10.00)
- **Reserve holdback** (default: 10%) — kept as safety margin
- **Single-action approval threshold** (default: $0.50) — pause for approval above this
- **New paid tool approval** — first-time use of any paid tool requires confirmation
- Persists to `cost_log.json` per project

**[한국어]**

`CostTracker`는 파이프라인 전체에서 지출 통제를 강제합니다.

**Lifecycle (라이프사이클)**

```
estimate(tool, operation, $) → entry_id
        |
reserve(entry_id)          # 예산을 잠금
        |
reconcile(entry_id, $)     # 실제 지출 기록
```

**Budget Modes (예산 모드)**

| 모드 | 동작 |
|------|------|
| `observe` | 비용 추적만, 강제 없음 |
| `warn` | 초과 시 경고 로그, 실행 허용 |
| `cap` | 잔여 예산 초과 작업 거부 |

**Controls (통제)**
- **총 예산** (기본값: $10.00)
- **예비 보유** (기본값: 10%) — 안전 마진으로 보관
- **단일 작업 승인 임계값** (기본값: $0.50) — 이 이상이면 승인을 위해 일시 중지
- **새 유료 도구 승인** — 유료 도구의 첫 사용에는 확인 필요
- 프로젝트별 `cost_log.json`에 지속

---

## 3-Layer Knowledge Architecture (3계층 지식 아키텍처)

```
Layer 3: .agents/skills/          External technology knowledge (47 skills)
         "How the technology works"    FFmpeg, ElevenLabs API, FLUX, Remotion, Three.js, etc.
              ^
              | agent_skills[] references
              |
Layer 2: skills/                  OpenMontage conventions
         "How this project uses the tech"  Pipeline integration, quality checklists, artifact mappings
              ^
              | stage skill references
              |
Layer 1: tools/ + pipeline_defs/  Executable capabilities + orchestration definitions
         "What exists and when to use it"  BaseTool contracts, pipeline manifests
```

Each tool's `agent_skills[]` field links Layer 1 to Layers 2 and 3. For example:
- `video_compose.agent_skills = ["remotion-best-practices", "remotion", "ffmpeg"]`
- `tts_selector.agent_skills = ["text-to-speech", "elevenlabs", "openai-docs"]`

**[한국어]**

```
레이어 3: .agents/skills/          외부 기술 지식 (47개 스킬)
         "기술이 어떻게 작동하는지"        FFmpeg, ElevenLabs API, FLUX, Remotion, Three.js 등
              ^
              | agent_skills[] 참조
              |
레이어 2: skills/                  OpenMontage 관례
         "이 프로젝트가 기술을 사용하는 방법"  파이프라인 통합, 품질 체크리스트, 산출물 매핑
              ^
              | 스테이지 스킬 참조
              |
레이어 1: tools/ + pipeline_defs/  실행 가능 기능 + 오케스트레이션 정의
         "무엇이 있고 언제 사용하는지"      BaseTool 계약, 파이프라인 매니페스트
```

각 도구의 `agent_skills[]` 필드는 레이어 1을 레이어 2와 3에 연결합니다. 예를 들어:
- `video_compose.agent_skills = ["remotion-best-practices", "remotion", "ffmpeg"]`
- `tts_selector.agent_skills = ["text-to-speech", "elevenlabs", "openai-docs"]`

---

## Configuration (설정)

### config.yaml

```yaml
llm:
  provider: anthropic
  temperature: 0.7
  max_tokens: 4096

budget:
  mode: warn
  total_usd: 10.00
  reserve_pct: 0.10
  single_action_approval_usd: 0.50

checkpoint:
  policy: guided
  storage_dir: pipeline

output:
  default_format: mp4
  default_codec: libx264
  default_audio_codec: aac
  default_resolution: 1920x1080
  default_fps: 30
  default_crf: 23

paths:
  pipeline_dir: pipeline
  library_dir: library
  styles_dir: styles
  skills_dir: skills
  output_dir: output
```

All config is validated via Pydantic models in `lib/config_model.py`.

**[한국어]**

```yaml
llm:
  provider: anthropic
  temperature: 0.7
  max_tokens: 4096

budget:
  mode: warn
  total_usd: 10.00
  reserve_pct: 0.10
  single_action_approval_usd: 0.50

checkpoint:
  policy: guided
  storage_dir: pipeline

output:
  default_format: mp4
  default_codec: libx264
  default_audio_codec: aac
  default_resolution: 1920x1080
  default_fps: 30
  default_crf: 23

paths:
  pipeline_dir: pipeline
  library_dir: library
  styles_dir: styles
  skills_dir: skills
  output_dir: output
```

모든 설정은 `lib/config_model.py`의 Pydantic 모델을 통해 검증됩니다.

### Environment Variables (.env) (환경 변수)

| Variable | Used By | Purpose |
|----------|---------|---------|
| `ELEVENLABS_API_KEY` | elevenlabs_tts, music_gen | TTS, music, sound effects |
| `OPENAI_API_KEY` | openai_tts, openai_image | TTS fallback, GPT Image 2 |
| `XAI_API_KEY` | grok_image, grok_video | Grok image editing/generation, Grok video generation |
| `FAL_KEY` | flux_image, kling_video, veo_video, minimax_video, recraft_image | fal.ai hosted models (FLUX, Veo, Kling, MiniMax, Recraft) |
| `KLING_API_KEY` | kling_official_video, kling_official_image, kling_tts, kling_avatar, kling_lip_sync | Official Kling direct API for video, image, TTS, avatar, and lip sync |
| `KLING_API_BASE_URL` | kling_official_video, kling_official_image, kling_tts, kling_avatar, kling_lip_sync | Optional official Kling API endpoint override |
| `HEYGEN_API_KEY` | heygen_video | Multi-provider video generation |
| `PEXELS_API_KEY` | pexels_image, pexels_video | Stock media |
| `PIXABAY_API_KEY` | pixabay_image, pixabay_video | Stock media |
| `GOOGLE_API_KEY` | google_imagen, google_tts | Google Imagen images, Google Cloud TTS |
| `RUNWAY_API_KEY` | runway_video | Runway Gen-3/Gen-4 direct |
| `HIGGSFIELD_API_KEY` + `HIGGSFIELD_API_SECRET` | higgsfield_video | Higgsfield multi-model video |
| `MODAL_LTX2_ENDPOINT_URL` | ltx_video_modal | Self-hosted LTX-2 |
| `VIDEO_GEN_LOCAL_ENABLED` | local video tools | Enable local GPU generation |
| `VIDEO_GEN_LOCAL_MODEL` | wan, hunyuan, ltx, cogvideo | Select local model |

Kling Official support stays inside the existing provider and capability model.
`kling_official_video` and `kling_official_image` handle Classic, Turbo, and Omni
request shapes, while Elements and Account Usage live under `tools/_kling/` as
internal helpers for element ID references and low-frequency account diagnostics;
they are not separate pipeline stages, selectors, or generated-asset capabilities.

Kling Official also adds provider tools only where OpenMontage already has a
matching capability slot: `kling_tts` for `tts`, plus `kling_avatar` and
`kling_lip_sync` for `avatar`. Official Kling audio effects and video effects are
not registered as tools because current pipelines do not define stable
`sound_effects` or `video_effects` capability routing.

**[한국어]**

| 변수 | 사용 도구 | 목적 |
|------|----------|------|
| `ELEVENLABS_API_KEY` | elevenlabs_tts, music_gen | TTS, 음악, 효과음 |
| `OPENAI_API_KEY` | openai_tts, openai_image | TTS 대체, GPT Image 2 |
| `XAI_API_KEY` | grok_image, grok_video | Grok 이미지 편집/생성, Grok 비디오 생성 |
| `FAL_KEY` | flux_image, kling_video, veo_video, minimax_video, recraft_image | fal.ai 호스팅 모델 (FLUX, Veo, Kling, MiniMax, Recraft) |
| `KLING_API_KEY` | kling_official_video, kling_official_image, kling_tts, kling_avatar, kling_lip_sync | 비디오, 이미지, TTS, 아바타, 립싱크를 위한 Kling 공식 직접 API |
| `KLING_API_BASE_URL` | kling_official_video, kling_official_image, kling_tts, kling_avatar, kling_lip_sync | 선택적 Kling 공식 API 엔드포인트 재정의 |
| `HEYGEN_API_KEY` | heygen_video | 다중 프로바이더 비디오 생성 |
| `PEXELS_API_KEY` | pexels_image, pexels_video | 스톡 미디어 |
| `PIXABAY_API_KEY` | pixabay_image, pixabay_video | 스톡 미디어 |
| `GOOGLE_API_KEY` | google_imagen, google_tts | Google Imagen 이미지, Google Cloud TTS |
| `RUNWAY_API_KEY` | runway_video | Runway Gen-3/Gen-4 직접 |
| `HIGGSFIELD_API_KEY` + `HIGGSFIELD_API_SECRET` | higgsfield_video | Higgsfield 다중 모델 비디오 |
| `MODAL_LTX2_ENDPOINT_URL` | ltx_video_modal | 셀프 호스팅 LTX-2 |
| `VIDEO_GEN_LOCAL_ENABLED` | 로컬 비디오 도구 | 로컬 GPU 생성 활성화 |
| `VIDEO_GEN_LOCAL_MODEL` | wan, hunyuan, ltx, cogvideo | 로컬 모델 선택 |

Kling 공식 지원은 기존 프로바이더 및 기능 모델 내에 유지됩니다.
`kling_official_video`와 `kling_official_image`는 Classic, Turbo, Omni 요청 형태를 처리하고,
Elements와 Account Usage는 `tools/_kling/` 아래에 요소 ID 참조 및 저빈도 계정 진단을 위한 내부 도우미로 존재합니다.
이들은 별도의 파이프라인 단계, 셀렉터, 생성 에셋 기능이 아닙니다.

Kling 공식은 또한 OpenMontage에 이미 일치하는 기능 슬롯이 있는 곳에만 프로바이더 도구를 추가합니다:
`tts`를 위한 `kling_tts`, `avatar`를 위한 `kling_avatar`와 `kling_lip_sync`.
Kling 공식 오디오 효과와 비디오 효과는 현재 파이프라인이 안정적인 `sound_effects`나
`video_effects` 기능 라우팅을 정의하지 않으므로 도구로 등록되지 않습니다.

---

## Visual Style System (시각적 스타일 시스템)

Style playbooks in `styles/` define visual language for pipelines:

- `clean-professional.yaml` — Corporate, polished look
- `flat-motion-graphics.yaml` — Modern flat design
- `minimalist-diagram.yaml` — Technical, minimal diagrams

Loaded by `styles/playbook_loader.py`. Each pipeline declares `compatible_playbooks` in its manifest. Validated against `schemas/styles/playbook.schema.json`.

**[한국어]**

`styles/`에 있는 스타일 플레이북은 파이프라인의 시각적 언어를 정의합니다.

- `clean-professional.yaml` — 기업형, 세련된 룩
- `flat-motion-graphics.yaml` — 현대적 평면 디자인
- `minimalist-diagram.yaml` — 기술적, 미니멀 다이어그램

`styles/playbook_loader.py`가 로드합니다. 각 파이프라인은 매니페스트에 `compatible_playbooks`를 선언합니다. `schemas/styles/playbook.schema.json`에 대해 검증됩니다.

---

## Media Profiles (미디어 프로필)

Platform-specific render configurations in `lib/media_profiles.py`:

| Profile | Resolution | Aspect | Notes |
|---------|-----------|--------|-------|
| `youtube_landscape` | 1920x1080 | 16:9 | Standard YouTube |
| `youtube_4k` | 3840x2160 | 16:9 | 4K YouTube |
| `youtube_shorts` | 1080x1920 | 9:16 | Max 60s |
| `instagram_reels` | 1080x1920 | 9:16 | Max 90s |
| `instagram_feed` | 1080x1080 | 1:1 | Square |
| `tiktok` | 1080x1920 | 9:16 | Vertical |
| `linkedin` | 1920x1080 | 16:9 | Landscape |
| `cinematic` | 2560x1080 | 21:9 | Ultrawide |

Each profile specifies codec, audio codec, CRF, pixel format, max file size, max duration, and caption format. `ffmpeg_output_args(profile)` generates the corresponding FFmpeg flags.

**[한국어]**

`lib/media_profiles.py`에 있는 플랫폼별 렌더 설정:

| 프로필 | 해상도 | 화면 비율 | 비고 |
|--------|--------|----------|------|
| `youtube_landscape` | 1920x1080 | 16:9 | 표준 YouTube |
| `youtube_4k` | 3840x2160 | 16:9 | 4K YouTube |
| `youtube_shorts` | 1080x1920 | 9:16 | 최대 60초 |
| `instagram_reels` | 1080x1920 | 9:16 | 최대 90초 |
| `instagram_feed` | 1080x1080 | 1:1 | 정사각형 |
| `tiktok` | 1080x1920 | 9:16 | 세로 |
| `linkedin` | 1920x1080 | 16:9 | 가로 |
| `cinematic` | 2560x1080 | 21:9 | 울트라 와이드 |

각 프로필은 코덱, 오디오 코덱, CRF, 픽셀 형식, 최대 파일 크기, 최대 지속 시간, 자막 형식을 지정합니다. `ffmpeg_output_args(profile)`은 해당 FFmpeg 플래그를 생성합니다.

---

## Composition Runtimes (컴포지션 런타임)

OpenMontage has a multi-runtime composition layer. Three engines live behind `video_compose`, chosen at proposal and locked in `edit_decisions.render_runtime`:

### Remotion (React-based)

A standalone Node.js/React subproject in `remotion-composer/` using [Remotion](https://www.remotion.dev/).

- **React 18** + **Remotion 4.0** + **TypeScript 5.3**
- Handles the existing scene-component stack (`text_card`, `stat_card`, charts, captions, `TalkingHead`, `CinematicRenderer`)
- Scripts: `start` (studio), `build` (render), `upgrade`

### HyperFrames (HTML/CSS/GSAP)

Consumed via `npx hyperframes` (no monorepo checkout needed). Runtime floor: Node.js ≥ 22, FFmpeg, `npx`.

- Handles kinetic typography, product promos, launch reels, website-to-video, registry blocks, and SVG/GSAP character rigs
- Driver: `tools/video/hyperframes_compose.py` materializes a workspace under `projects/<name>/hyperframes/`, then runs `lint → validate → render`
- Layer 3 skills vendored at `.agents/skills/hyperframes*/`; Layer 2 guide at `skills/core/hyperframes.md`
- The `character-animation` pipeline uses HyperFrames as the production render package. Browser previews are QA/debug artifacts only, not the render path.

### FFmpeg (fallback / simple cuts)

- Handles pure concat/trim when no composition is needed
- Also handles subtitle burn-in as a post-hoc operation

`video_compose` reads `edit_decisions.render_runtime` and dispatches via `_render_via_hyperframes`, `_remotion_render`, or `_render_via_ffmpeg`. Silent runtime swaps are forbidden — the tool returns a structured blocker when the chosen runtime is unavailable. See `AGENT_GUIDE.md` → "Composition Runtimes (Inside video_compose)" and `skills/core/hyperframes.md` for the full decision matrix.

**[한국어]**

OpenMontage는 다중 런타임 컴포지션 레이어를 갖추고 있습니다. `video_compose` 뒤에 세 가지 엔진이 있으며, proposal에서 선택되고 `edit_decisions.render_runtime`에 잠깁니다.

**Remotion (React 기반)** — [Remotion](https://www.remotion.dev/)을 사용하는 `remotion-composer/`의 독립형 Node.js/React 하위 프로젝트입니다. **React 18** + **Remotion 4.0** + **TypeScript 5.3**을 사용하며, 기존 장면 구성 요소 스택(`text_card`, `stat_card`, 차트, 자막, `TalkingHead`, `CinematicRenderer`)을 처리합니다. 스크립트: `start` (스튜디오), `build` (렌더), `upgrade`.

**HyperFrames (HTML/CSS/GSAP)** — `npx hyperframes`를 통해 사용 (모노레포 체크아웃 불필요). 런타임 요구사항: Node.js ≥ 22, FFmpeg, `npx`. 키네틱 타이포그래피, 제품 프로모, 런치 릴, 웹사이트-투-비디오, 레지스트리 블록, SVG/GSAP 캐릭터 리그를 처리합니다. 드라이버: `tools/video/hyperframes_compose.py`가 `projects/<name>/hyperframes/` 아래에 작업 공간을 구체화한 다음 `lint → validate → render`를 실행합니다. 레이어 3 스킬은 `.agents/skills/hyperframes*/`에 벤더됨. 레이어 2 가이드는 `skills/core/hyperframes.md`에 있음. `character-animation` 파이프라인은 HyperFrames를 제작 렌더 패키지로 사용. 브라우저 미리보기는 QA/디버그 산출물만, 렌더 경로가 아님.

**FFmpeg (대체 / 단순 자르기)** — 컴포지션이 필요 없을 때 순수 concat/trim을 처리
- 자막 입히기도 사후 작업으로 처리

`video_compose`는 `edit_decisions.render_runtime`을 읽고 `_render_via_hyperframes`, `_remotion_render`, `_render_via_ffmpeg`를 통해 디스패치합니다. 묵시적 런타임 교체는 금지되어 있습니다 — 선택된 런타임을 사용할 수 없을 때 도구는 구조적 블로커를 반환합니다. 전체 의사결정 매트릭스는 `AGENT_GUIDE.md` → "Composition Runtimes (Inside video_compose)"와 `skills/core/hyperframes.md`를 참조하십시오.

---

## Test Architecture (테스트 아키텍처)

```
tests/
├── contracts/              # Phase 0-3: tool contract validation, schema checks, registry tests
├── qa/                     # Integration tests: TTS, image gen, music, audio mix, video compose/stitch, E2E
├── eval/                   # Golden scenario replay harness for regression testing
├── pipelines/              # Pipeline-level tests
├── tools/                  # Individual tool tests
└── styles/                 # Style playbook tests
```

**Contract tests** verify every tool satisfies the `BaseTool` contract: identity fields, schemas, dependency declarations, inheritance.

**QA tests** call real tools (with real APIs/binaries) and inspect output quality.

**Eval harness** (`tests/eval/replay_harness/`) replays golden scenarios with tolerance-based comparison for stochastic outputs.

**[한국어]**

```
tests/
├── contracts/              # Phase 0-3: 도구 계약 검증, 스키마 확인, 레지스트리 테스트
├── qa/                     # 통합 테스트: TTS, 이미지 생성, 음악, 오디오 믹스, 비디오 컴포즈/스티치, E2E
├── eval/                   # 회귀 테스트를 위한 골든 시나리오 리플레이 하니스
├── pipelines/              # 파이프라인 수준 테스트
├── tools/                  # 개별 도구 테스트
└── styles/                 # 스타일 플레이북 테스트
```

**계약 테스트**는 모든 도구가 `BaseTool` 계약(식별 필드, 스키마, 의존성 선언, 상속)을 충족하는지 검증합니다.

**QA 테스트**는 실제 도구(실제 API/바이너리)를 호출하고 출력 품질을 검사합니다.

**Eval 하니스**(`tests/eval/replay_harness/`)는 허용 기반 비교로 골든 시나리오를 재현하여 회귀를 테스트합니다.

---

## System Dependencies (시스템 의존성)

**Required:**
- Python >= 3.10
- FFmpeg (used by ~15 tools)

**Optional (extend capabilities):**
- Node.js (for Remotion composer)
- GPU + CUDA (for local video/image generation)
- Piper (offline TTS)
- ManimCE (math animations)
- Mermaid CLI (diagram generation)

**Python packages:** pyyaml, pydantic, jsonschema, python-dotenv (core); pytest, pytest-asyncio (dev); torch, torchvision, torchaudio (GPU)

**[한국어]**

**필수:**
- Python >= 3.10
- FFmpeg (15개 도구에서 사용)

**선택 사항 (기능 확장):**
- Node.js (Remotion composer용)
- GPU + CUDA (로컬 비디오/이미지 생성용)
- Piper (오프라인 TTS)
- ManimCE (수학 애니메이션)
- Mermaid CLI (다이어그램 생성)

**Python 패키지:** pyyaml, pydantic, jsonschema, python-dotenv (핵심); pytest, pytest-asyncio (개발); torch, torchvision, torchaudio (GPU)

---

## Key Design Decisions (주요 설계 결정)

1. **No runtime orchestrator** — The LLM agent reads YAML + Markdown and drives everything. This makes the system debuggable (just read the skill) and model-agnostic.

2. **Checkpoint-based resumption** — Any stage can fail and the pipeline resumes from the last checkpoint. No re-running completed stages.

3. **Schema-validated artifacts** — Every stage output is validated against a JSON Schema before the checkpoint is written. Prevents garbage propagation.

4. **Budget as a first-class concept** — Cost estimation before execution, budget reservation, and reconciliation. The agent cannot silently overspend.

5. **Selector pattern over hard-coded providers** — Capabilities degrade gracefully. Missing an API key? The selector falls through to the next provider or a local alternative.

6. **Skills over code for intelligence** — Creative decisions, quality checklists, review criteria, and prompt templates live in Markdown skills, not Python. This means the agent's behavior can be tuned by editing text files, not code.

**[한국어]**

1. **런타임 오케스트레이터 없음** — LLM 에이전트가 YAML과 Markdown을 읽고 모든 것을 구동합니다. 이로 인해 시스템이 디버그 가능(스킬만 읽으면 됨)하고 모델에 구애받지 않습니다.

2. **체크포인트 기반 재개** — 어떤 단계든 실패하면 파이프라인이 마지막 체크포인트에서 재개됩니다. 완료된 단계를 다시 실행할 필요가 없습니다.

3. **스키마 검증 산출물** — 모든 단계 출력은 체크포인트 작성 전 JSON 스키마에 대해 검증됩니다. 가비지 전파를 방지합니다.

4. **일급 개념으로서의 예산** — 실행 전 비용 추정, 예산 예약, 정산. 에이전트가 조용히 초과 지출할 수 없습니다.

5. **하드코딩된 프로바이더 대신 셀렉터 패턴** — 기능이 우아하게 저하됩니다. API 키가 누락되었나요? 셀렉터는 다음 프로바이더나 로컬 대안으로 넘어갑니다.

6. **지능을 위한 코드 대신 스킬** — 창의적 결정, 품질 체크리스트, 검토 기준, 프롬프트 템플릿은 Python이 아닌 Markdown 스킬에 있습니다. 즉, 에이전트 동작은 텍스트 파일 편집으로 튜닝할 수 있고 코드를 수정할 필요가 없습니다.