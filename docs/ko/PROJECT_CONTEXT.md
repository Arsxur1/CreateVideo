> 이 문서는 이중 언어 문서입니다. 각 섹션에서 영어 원문이 먼저 나오고, **[한국어]** 표시 아래에 한국어 번역이 이어집니다.
> 원본: PROJECT_CONTEXT.md @ 2b0801030c40a51fc92724403bf0c84bca8c8ab7

# OpenMontage - Shared Project Context

This is the single source of truth for project architecture and conventions. All platform-specific agent files (CLAUDE.md, CODEX.md, CURSOR.md, COPILOT.md) should point here instead of duplicating this content.

**[한국어]**
이 문서는 프로젝트 아키텍처와 규칙에 대한 단일 진실 공급원입니다. 모든 플랫폼별 에이전트 파일(CLAUDE.md, CODEX.md, CURSOR.md, COPILOT.md)은 이 내용을 복제하는 대신 여기를 참조해야 합니다.

## Identity (정체성)

OpenMontage is an open-source, AI-orchestrated video production platform.

**[한국어]**
OpenMontage는 오픈 소스 AI 주도 비디오 제작 플랫폼입니다.

## Architecture: Instruction-Driven (Agent-First) (아키텍처: 명령어 주도형 (에이전트 우선))

The AI agent IS the intelligence. Python exists only for tools and persistence. Everything else — orchestration, creative decisions, review, stage transitions — lives in instructions (YAML manifests + markdown skills) the agent follows.

**[한국어]**
AI 에이전트가 곧 지능입니다. Python은 도구와 영속성을 위해서만 존재합니다. 그 외의 모든 것 — 오케스트레이션, 창의적 결정, 검토, 단계 전환 — 에이전트가 따르는 명령어(YAML 매니페스트 + 마크다운 스킬)에 살아있습니다.

```
Agent reads pipeline manifest (YAML) → reads stage director skill (MD)
→ uses tools (Python BaseTool) → self-reviews (meta skill)
→ checkpoints (Python utility) → presents to human for approval
```

**No Python orchestrator, no Python reviewer, no Python handlers.** The agent drives the pipeline.

**[한국어]**
**Python 오케스트레이터 없음, Python 검토자 없음, Python 핸들러 없음.** 에이전트가 파이프라인을 주도합니다.

## Source of Truth (진실 공급원)

- **Agent guide & contract:** `AGENT_GUIDE.md` (tool inventory, pipeline selection, stage agents, protocols)
- **Skill index:** `skills/INDEX.md`
- **Tool registry:** `tools/tool_registry.py`
- **Pipeline manifests:** `pipeline_defs/`
- **Artifact schemas:** `schemas/artifacts/`
- **Style playbooks:** `styles/*.yaml` (schema: `schemas/styles/playbook.schema.json`)
- **Stage director skills:** `skills/pipelines/<pipeline>/<stage>-director.md`
- **Meta skills:** `skills/meta/*.md` (reviewer, checkpoint-protocol, skill-creator)
- **Architecture deep-dive:** `docs/ARCHITECTURE.md`

**[한국어]**
- **에이전트 가이드 및 계약:** `AGENT_GUIDE.md` (도구 목록, 파이프라인 선택, 스테이지 에이전트, 프로토콜)
- **스킬 인덱스:** `skills/INDEX.md`
- **도구 레지스트리:** `tools/tool_registry.py`
- **파이프라인 매니페스트:** `pipeline_defs/`
- **아티팩트 스키마:** `schemas/artifacts/`
- **스타일 플레이북:** `styles/*.yaml` (스키마: `schemas/styles/playbook.schema.json`)
- **스테이지 디렉터 스킬:** `skills/pipelines/<pipeline>/<stage>-director.md`
- **메타 스킬:** `skills/meta/*.md` (reviewer, checkpoint-protocol, skill-creator)
- **아키텍처 심층 분석:** `docs/ARCHITECTURE.md`

## Knowledge Architecture (3 Layers) (지식 아키텍처 (3개 계층))

```
Layer 1: tools/tool_registry.py     → "What tools exist" (runtime capabilities, status, cost)
Layer 2: skills/                    → "How OpenMontage uses them" (project conventions)
Layer 3: .agents/skills/            → "How the technology works" (generic API rules, skills.sh)
```

Each tool's `agent_skills[]` field bridges Layer 1 → Layer 3. See `skills/INDEX.md` for the full mapping.

**[한국어]**
각 도구의 `agent_skills[]` 필드는 계층 1 → 계층 3을 연결합니다. 전체 매핑은 `skills/INDEX.md`를 참조하십시오.

## Key Patterns (핵심 패턴)

- **Pipeline state machine:** `idea -> script -> scene_plan -> assets -> edit -> compose -> publish`
- **Instruction-driven stages:** Each stage has a director skill (MD) that teaches the agent HOW
- **Pipeline manifests:** Declarative YAML defining stages, skills, tools, review focus, approval gates
- **Capability-first tool design:** Each major family should expose a selector tool plus explicit provider tools
  - Example: `tts_selector` + `elevenlabs_tts` / `google_tts` / `openai_tts` / `piper_tts`
  - Example: `video_selector` + `heygen_video` / `wan_video` / `hunyuan_video` / `ltx_video_local` / `ltx_video_modal` / `cogvideo_video`
- **Style playbooks:** YAML defining visual language, typography, motion, audio, asset generation constraints
- **Artifacts are canonical:** `brief`, `script`, `scene_plan`, `asset_manifest`, `edit_decisions`, `render_report`, `publish_log`
- **Every tool inherits from `tools/base_tool.py`** (ToolContract)
- **Checkpoint policy** lives in pipeline manifest (`human_approval_default` per stage) + `skills/meta/checkpoint-protocol.md`
- **Reviewer** is a meta skill (`skills/meta/reviewer.md`), advisory, max 2 rounds
- **Cost tracker** (`tools/cost_tracker.py`) manages budget: estimate -> reserve -> reconcile
- **Canonical artifacts** validated against JSON schemas in `schemas/artifacts/`

**[한국어]**
- **파이프라인 상태 머신:** `idea -> script -> scene_plan -> assets -> edit -> compose -> publish`
- **명령어 주도형 스테이지:** 각 스테이지는 에이전트에게 방법을 가르치는 디렉터 스킬(MD)을 가집니다
- **파이프라인 매니페스트:** 스테이지, 스킬, 도구, 검토 초점, 승인 게이트를 정의하는 선언적 YAML
- **기능 우선 도구 설계:** 각 주요 계열은 선택기 도구와 명시적 프로바이더 도구를 노출해야 합니다
  - 예시: `tts_selector` + `elevenlabs_tts` / `google_tts` / `openai_tts` / `piper_tts`
  - 예시: `video_selector` + `heygen_video` / `wan_video` / `hunyuan_video` / `ltx_video_local` / `ltx_video_modal` / `cogvideo_video`
- **스타일 플레이북:** 시각 언어, 타이포그래피, 모션, 오디오, 자산 생성 제약 조건을 정의하는 YAML
- **아티팩트가 정본입니다:** `brief`, `script`, `scene_plan`, `asset_manifest`, `edit_decisions`, `render_report`, `publish_log`
- **모든 도구는 `tools/base_tool.py`를 상속받습니다** (ToolContract)
- **체크포인트 정책**은 파이프라인 매니페스트(스테이지별 `human_approval_default`) + `skills/meta/checkpoint-protocol.md`에 있습니다
- **검토자**는 메타 스킬(`skills/meta/reviewer.md`)입니다, 자문 역할, 최대 2라운드
- **비용 추적기** (`tools/cost_tracker.py`)는 예산을 관리합니다: 추정 -> 예약 -> 조정
- **정식 아티팩트**는 `schemas/artifacts/`의 JSON 스키마에 대해 검증됩니다

## Key Files (핵심 파일)

| File | Purpose |
|------|---------|
| `config.yaml` | Global configuration |
| `lib/config_model.py` | Runtime config loader (Pydantic) |
| `lib/checkpoint.py` | Checkpoint writer/reader |
| `lib/pipeline_loader.py` | Pipeline manifest loader + helpers |
| `lib/media_profiles.py` | Platform-specific render profiles |
| `styles/playbook_loader.py` | Style playbook loader + validator + design intelligence (color/type/a11y) |
| `tools/base_tool.py` | ToolContract base class |
| `tools/tool_registry.py` | Tool discovery and reporting |
| `tools/cost_tracker.py` | Budget governance |
| `tools/video/video_stitch.py` | Multi-clip assembly (stitch, spatial, validate, preview) |
| `tools/video/video_compose.py` | Runtime-aware composition orchestrator — routes to Remotion / HyperFrames / FFmpeg based on `edit_decisions.render_runtime` |
| `tools/video/hyperframes_compose.py` | HyperFrames runtime — workspace materialization, `hyperframes lint`/`validate`/`render`, FFmpeg floor check |
| `tools/character/character_animation.py` | Local character-animation tools — character specs, SVG rig plans, pose libraries, action timelines, HyperFrames packages, and QA reports |
| `lib/hyperframes_style_bridge.py` | Playbook → CSS custom properties + `DESIGN.md` bridge for HyperFrames workspaces |
| `remotion-composer/src/components/` | 8 Remotion components (TextCard, StatCard, ProgressBar, CalloutBox, ComparisonCard + charts/) |
| `.agents/skills/hyperframes*/` | Vendored HyperFrames Layer 3 skills (authoring contract, CLI, registry, website-to-video) |
| `skills/core/hyperframes.md` | Layer 2 — when OpenMontage should pick HyperFrames vs Remotion, artifact → workspace mapping |
| `schemas/styles/playbook.schema.json` | Playbook schema v2 with design tokens (chart_palette, scale_system, weight_matrix, color_rules) |
| `tests/qa/` | Quality validation test scripts for tool-by-tool output inspection |

**[한국어]**
| 파일 | 목적 |
|------|---------|
| `config.yaml` | 전역 설정 |
| `lib/config_model.py` | 런타임 설정 로더 (Pydantic) |
| `lib/checkpoint.py` | 체크포인트 작성기/판독기 |
| `lib/pipeline_loader.py` | 파이프라인 매니페스트 로더 + 헬퍼 |
| `lib/media_profiles.py` | 플랫폼별 렌더링 프로필 |
| `styles/playbook_loader.py` | 스타일 플레이북 로더 + 검증기 + 디자인 인텔리전스 (색상/타입/접근성) |
| `tools/base_tool.py` | ToolContract 기본 클래스 |
| `tools/tool_registry.py` | 도구 발견 및 보고 |
| `tools/cost_tracker.py` | 예산 관리 |
| `tools/video/video_stitch.py` | 멀티 클립 어셈블리 (스티치, 공간, 검증, 미리보기) |
| `tools/video/video_compose.py` | 런타임 인식 컴포지션 오케스트레이터 — `edit_decisions.render_runtime`을 기준으로 Remotion / HyperFrames / FFmpeg으로 라우팅 |
| `tools/video/hyperframes_compose.py` | HyperFrames 런타임 — 워크스페이스 구체화, `hyperframes lint`/`validate`/`render`, FFmpeg 플로어 체크 |
| `tools/character/character_animation.py` | 로컬 캐릭터 애니메이션 도구 — 캐릭터 사양, SVG 리그 계획, 포즈 라이브러리, 액션 타임라인, HyperFrames 패키지, QA 보고서 |
| `lib/hyperframes_style_bridge.py` | HyperFrames 워크스페이스용 Playbook → CSS 사용자 정의 속성 + `DESIGN.md` 브리지 |
| `remotion-composer/src/components/` | 8개 Remotion 컴포넌트 (TextCard, StatCard, ProgressBar, CalloutBox, ComparisonCard + charts/) |
| `.agents/skills/hyperframes*/` | 공급된 HyperFrames 계층 3 스킬 (작성 계약, CLI, 레지스트리, 웹사이트-비디오) |
| `skills/core/hyperframes.md` | 계층 2 — OpenMontage가 HyperFrames와 Remotion 중 언제 선택해야 하는지, 아티팩트 → 워크스페이스 매핑 |
| `schemas/styles/playbook.schema.json` | 디자인 토큰이 있는 플레이북 스키마 v2 (chart_palette, scale_system, weight_matrix, color_rules) |
| `tests/qa/` | 도구별 출력 검사를 위한 품질 검증 테스트 스크립트 |

## Available Pipelines (사용 가능한 파이프라인)

| Pipeline | Manifest | Type |
|----------|----------|------|
| `talking-head` | `pipeline_defs/talking-head.yaml` | Footage-based |
| `animated-explainer` | `pipeline_defs/animated-explainer.yaml` | AI-generated |
| `screen-demo` | `pipeline_defs/screen-demo.yaml` | Screen-recording |
| `clip-factory` | `pipeline_defs/clip-factory.yaml` | Short-form batch extraction |
| `podcast-repurpose` | `pipeline_defs/podcast-repurpose.yaml` | Podcast repurposing |
| `cinematic` | `pipeline_defs/cinematic.yaml` | Cinematic edit |
| `animation` | `pipeline_defs/animation.yaml` | Animation-first |
| `character-animation` | `pipeline_defs/character-animation.yaml` | Local rigged character animation |
| `hybrid` | `pipeline_defs/hybrid.yaml` | Source-plus-support hybrid |
| `avatar-spokesperson` | `pipeline_defs/avatar-spokesperson.yaml` | Avatar presenter |
| `localization-dub` | `pipeline_defs/localization-dub.yaml` | Localization and dubbing |
| `framework-smoke` | `pipeline_defs/framework-smoke.yaml` | Test harness |

**[한국어]**
| 파이프라인 | 매니페스트 | 유형 |
|----------|----------|------|
| `talking-head` | `pipeline_defs/talking-head.yaml` | 풋티지 기반 |
| `animated-explainer` | `pipeline_defs/animated-explainer.yaml` | AI 생성 |
| `screen-demo` | `pipeline_defs/screen-demo.yaml` | 화면 녹화 |
| `clip-factory` | `pipeline_defs/clip-factory.yaml` | 단편 배치 추출 |
| `podcast-repurpose` | `pipeline_defs/podcast-repurpose.yaml` | 팟캐스트 재가공 |
| `cinematic` | `pipeline_defs/cinematic.yaml` | 시네마틱 편집 |
| `animation` | `pipeline_defs/animation.yaml` | 애니메이션 우선 |
| `character-animation` | `pipeline_defs/character-animation.yaml` | 로컬 리그 캐릭터 애니메이션 |
| `hybrid` | `pipeline_defs/hybrid.yaml` | 소스 플러스 지원 하이브리드 |
| `avatar-spokesperson` | `pipeline_defs/avatar-spokesperson.yaml` | 아바타 프레젠터 |
| `localization-dub` | `pipeline_defs/localization-dub.yaml` | 지역화 및 더빙 |
| `framework-smoke` | `pipeline_defs/framework-smoke.yaml` | 테스트 하네스 |

## When Building New Pipelines (새 파이프라인 구축 시)

1. Create a YAML manifest in `pipeline_defs/` (validated by `pipeline_manifest.schema.json`)
2. Create stage director skills in `skills/pipelines/<pipeline-name>/` (7 skills: idea through publish)
3. Reference meta skills (reviewer, checkpoint-protocol) in the manifest
4. Add compatible playbooks to the manifest
5. Add contract tests in `tests/contracts/`

**[한국어]**
1. `pipeline_defs/`에 YAML 매니페스트 생성 (`pipeline_manifest.schema.json`로 검증됨)
2. `skills/pipelines/<pipeline-name>/`에 스테이지 디렉터 스킬 생성 (7개 스킬: 아이디어부터 출판까지)
3. 매니페스트에 메타 스킬(reviewer, checkpoint-protocol) 참조 추가
4. 매니페스트에 호환되는 플레이북 추가
5. `tests/contracts/`에 계약 테스트 추가

## When Building New Tools (새 도구 구축 시)

1. Inherit from `tools/base_tool.py` `BaseTool`
2. Put the tool in the correct capability package (`tools/audio/`, `tools/video/`, `tools/enhancement/`, `tools/analysis/`, `tools/graphics/`, `tools/avatar/`, `tools/subtitle/`)
3. Prefer the selector-plus-provider pattern:
   - one capability router tool for agent convenience
   - one concrete tool per real provider/runtime path
4. Set all contract fields (name, version, tier, capability, provider, supports, fallback_tools, agent_skills, etc.)
5. Implement `execute()` returning a `ToolResult`
6. Let discovery happen through `tools/tool_registry.py`; do not depend on ad hoc imports
7. Add a JSON schema in `schemas/tools/` if the tool has complex I/O
8. Add tests only after the runtime path is correct

**[한국어]**
1. `tools/base_tool.py`의 `BaseTool`에서 상속받습니다
2. 도구를 올바른 기능 패키지(`tools/audio/`, `tools/video/`, `tools/enhancement/`, `tools/analysis/`, `tools/graphics/`, `tools/avatar/`, `tools/subtitle/`)에 배치합니다
3. 선택기 플러스 프로바이더 패턴을 선호합니다:
   - 에이전트 편의성을 위한 하나의 기능 라우터 도구
   - 실제 프로바이더/런타임 경로당 하나의 구체적 도구
4. 모든 계약 필드(name, version, tier, capability, provider, supports, fallback_tools, agent_skills 등)를 설정합니다
5. `ToolResult`를 반환하는 `execute()`를 구현합니다
6. `tools/tool_registry.py`를 통해 발견이 일어나도록 합니다; 임시 import에 의존하지 마십시오
7. 도구에 복잡한 I/O가 있는 경우 `schemas/tools/`에 JSON 스키마를 추가합니다
8. 런타임 경로가 올바른 후에만 테스트를 추가합니다