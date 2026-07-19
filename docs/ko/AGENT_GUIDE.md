> 이 문서는 이중 언어 문서입니다. 각 섹션에서 영어 원문이 먼저 나오고, **[한국어]** 표시 아래에 한국어 번역이 이어집니다.

> 원본: AGENT_GUIDE.md @ a2a0d8c8af0c046ead098b43c8a8d55d2ee0d421

> ⚠️ 참조용 번역입니다. 에이전트 동작 계약의 정본은 영어 원본 [AGENT_GUIDE.md](../../AGENT_GUIDE.md)입니다.

# OpenMontage - Agent Guide (OpenMontage - 에이전트 가이드)

Start here. This is the complete operating guide and agent contract for OpenMontage.

**[한국어]**

여기서 시작하십시오. 이 문서는 OpenMontage의 전체 운영 가이드이자 에이전트 계약서입니다.

For architecture, key files, and conventions see [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md).

아키텍처, 핵심 파일, 규칙은 [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md)를 참조하십시오.

---

## First Interaction — Onboarding (첫 상호작용 — 온보딩)

When the user's first message is vague, exploratory, or asks what you can do ("make me a video", "what can you do?", "help me create something", "I want to make content"), read the onboarding skill **before** doing anything else:

**[한국어]**

사용자의 첫 메시지가 모호하거나 탐색적이거나 당신이 무엇을 할 수 있는지 물을 때 ("동영상을 만들어줘", "무엇을 할 수 있어?", "무언가를 만드는 것을 도와줘", "콘텐츠를 만들고 싶어"), 다른 작업을 수행하기 전에 **먼저** 온보딩 스킬을 읽으십시오:

**Read:** `skills/meta/onboarding.md`

**읽으십시오:** `skills/meta/onboarding.md`

This skill teaches you to run discovery, classify the user's setup, present capabilities in plain language, and offer starter prompts tailored to their available tools. The goal: get the user from "curious" to "making a video" in under 60 seconds.

**[한국어]**

이 스킬은 발견 단계를 실행하고, 사용자의 설정을 분류하고, 평이한 언어로 기능을 제시하고, 사용 가능한 도구에 맞춤화된 시작 프롬프트를 제공하는 방법을 알려줍니다. 목표: 60초 이내에 사용자를 "호기심" 단계에서 "동영상 제작" 단계로 가져오는 것입니다.

**Skip onboarding** when the user arrives with a specific, actionable request (e.g., "Make a 60-second explainer about black holes"). Go directly to Rule Zero.

**[한국어]**

사용자가 구체적이고 실행 가능한 요청을 가지고 올 때는 **온보딩을 건너뛰십시오** (예: "블랙홀에 대한 60초 설명 영상을 만들어줘"). 바로 룰 제로로 가십시오.

---

## Reference Video Entry Point (참조 동영상 진입점)

When the user provides a **video URL or local video file as inspiration** — for example:

**[한국어]**

사용자가 영감으로 **동영상 URL이나 로컬 동영상 파일을 제공**할 때 — 예를 들어:

- "Can you make a video like this?"
- "I love this YouTube Short. Make me something similar."
- "Use this Reel as a reference."

— "이런 동영상을 만들 수 있어?"
— "이 유튜브 숏이 마음에 들어. 비슷한 걸 만들어줘."
— "이 릴을 참조로 사용해."

— do **not** treat this as a generic web-search or prompt-writing request.

**[한국어]**

— 이것을 일반적인 웹 검색이나 프롬프트 작성 요청으로 **처리하지 마십시오.**

This is a first-class workflow in OpenMontage.

**[한국어]**

이것은 OpenMontage의 1급 워크플로우입니다.

### Required behavior (필수 동작)

1. **Read:** `skills/meta/video-reference-analyst.md`
2. **Run the reference analysis workflow** using the local analysis tools (`video_analyzer`, transcript extraction, scene detection, frame sampling)
3. **Produce a grounded summary** of what the reference is doing:
   - content
   - pacing
   - structure
   - style
   - what makes it work
4. **Then** run normal capability audit and pipeline selection
5. Present **2-3 differentiated concepts** for the user's version — not a carbon copy

**[한국어]**

1. **읽으십시오:** `skills/meta/video-reference-analyst.md`
2. 로컬 분석 도구(`video_analyzer`, transcript extraction, scene detection, frame sampling)를 사용하여 **참조 분석 워크플로우 실행**
3. 참조가 수행하는 것에 대한 **근거 기반 요약 작성**:
   - 콘텐츠
   - 페이싱
   - 구조
   - 스타일
   - 효과가 있는 이유
4. **그 후** 일반적인 기능 감사 및 파이프라인 선택 실행
5. 사용자 버전에 대해 **2-3개의 차별화된 컨셉** 제시 — 복사본이 아님

### Important distinction (중요한 구분)

- **Reference-driven request:** "make me something like this" -> use `video-reference-analyst.md`
- **Source-footage request:** "edit this footage" / "cut this into clips" -> use `source_media_review` and the appropriate footage-led pipeline

**[한국어]**

- **참조 기반 요청:** "이런 걸 만들어줘" -> `video-reference-analyst.md` 사용
- **소스 풋티지 요청:** "이 풋티지를 편집해줘" / "이것을 클립으로 잘라줘" -> `source_media_review`와 적절한 풋티지 기반 파이프라인 사용

If a model misses this distinction, it will often fall back to plain search + guesswork. That is incorrect for OpenMontage.

**[한국어]**

모델이 이 구분을 놓치면 일반 검색 + 추측으로 회귀하는 경우가 많습니다. 이것은 OpenMontage에서 올바르지 않습니다.

---

## Rule Zero — All Production Goes Through a Pipeline (룰 제로 — 모든 제작은 파이프라인을 통과)

**Every video production request MUST go through the pipeline system. No exceptions.**

**[한국어]**

**모든 동영상 제작 요청은 파이프라인 시스템을 통과해야 합니다. 예외 없음.**

When the user asks to make, create, produce, or generate any video content — a trailer, explainer, clip, animation, or any other video — the agent must:

**[한국어]**

사용자가 동영상을 만들고, 생성하고, 제작하고, 생산해달라고 요청할 때 — 트레일러, 설명 영상, 클립, 애니메이션, 또는 그 외 모든 동영상 — 에이전트는 다음을 수행해야 합니다:

1. **Identify the pipeline.** Match the request to one of the pipelines in `pipeline_defs/`. If unclear, ask the user.
2. **Read the pipeline manifest.** `pipeline_defs/<pipeline>.yaml` — know the stages, tools, and quality gates.
3. **Run preflight.** Discover available tools via the registry. Present the capability menu.
4. **Execute stage by stage.** For EACH stage, read the stage director skill (`skills/pipelines/<pipeline>/<stage>-director.md`) BEFORE doing any work in that stage.
5. **Read Layer 3 skills before calling tools.** Before using any tool with an `agent_skills` field, read the referenced skill in `.agents/skills/`. These contain provider-specific prompting guidance, parameter optimization, and quality techniques that dramatically improve output.

**[한국어]**

1. **파이프라인 식별.** `pipeline_defs/`의 파이프라인 중 하나와 요청을 매칭하십시오. 불명확하면 사용자에게 물어보십시오.
2. **파이프라인 매니페스트 읽기.** `pipeline_defs/<pipeline>.yaml` — 단계, 도구, 품질 게이트를 알아야 합니다.
3. **사전 점검 실행.** 레지스트리를 통해 사용 가능한 도구를 발견하십시오. 기능 메뉴를 제시하십시오.
4. **단계별 실행.** 각 단계에 대해, 해당 단계에서 작업을 수행하기 **전에** 단계 감독 스킬(`skills/pipelines/<pipeline>/<stage>-director.md`)을 읽으십시오.
5. **도구 호출 전 레이어 3 스킬 읽기.** `agent_skills` 필드가 있는 도구를 사용하기 전에 `.agents/skills/`에서 참조되는 스킬을 읽으십시오. 이것들은 프로바이더별 프롬프팅 지침, 매개변수 최적화, 출력을 극적으로 향상시키는 품질 기법을 포함합니다.

**Do NOT:**

**[한국어]**

**하지 마십시오:**

- Write ad-hoc Python scripts to call tools directly
- Skip the pipeline and go straight to API calls
- Generate assets without reading the stage director skill first
- Use a tool without checking its Layer 3 skill for prompting guidance
- Bypass preflight, checkpoints, or review

- 도구를 직접 호출하는 임시 Python 스크립트 작성
- 파이프라인을 건너뛰고 바로 API 호출로 가기
- 단계 감독 스킬을 먼저 읽지 않고 자산 생성
- 프롬프팅 지침을 위해 레이어 3 스킬을 확인하지 않고 도구 사용
- 사전 점검, 체크포인트, 검토 우회

The intelligence is in the skills, not in improvised code. An agent that reads the director skills and Layer 3 knowledge will produce significantly better output than one that calls tools directly with generic prompts.

**[한국어]**

지능은 스킬에 있지 임시 코드에 있지 않습니다. 감독 스킬과 레이어 3 지식을 읽는 에이전트는 일반 프롬프트로 도구를 직접 호출하는 에이전트보다 훨씬 더 나은 출력을 생성합니다.

---

## What OpenMontage Is (OpenMontage란)

OpenMontage is an instruction-driven video production system. The AI agent IS the intelligence — it reads instructions (pipeline manifests + stage director skills + meta skills) and drives the pipeline using tools.

**[한국어]**

OpenMontage는 명령 기반 동영상 제작 시스템입니다. AI 에이전트가 곧 지능입니다 — 에이전트는 명령(파이프라인 매니페스트 + 단계 감독 스킬 + 메타 스킬)을 읽고 도구를 사용하여 파이프라인을 구동합니다.

```
Agent reads pipeline manifest (YAML) -> reads stage director skill (MD)
-> uses tools (Python BaseTool subclasses) -> self-reviews (meta skill)
-> checkpoints (Python utility) -> presents to human for approval
```

**[한국어]**

```
에이전트가 파이프라인 매니페스트 읽기 (YAML) -> 단계 감독 스킬 읽기 (MD)
-> 도구 사용 (Python BaseTool 서브클래스) -> 자체 검토 (메타 스킬)
-> 체크포인트 (Python 유틸리티) -> 승인을 위해 인간에게 제시
```

**Python = tools + persistence.** No orchestration logic, creative decisions, review logic, or checkpoint policy in Python code. The agent makes those decisions guided by instructions.

**[한국어]**

**Python = 도구 + 지속성.** Python 코드에 오케스트레이션 로직, 창의적 결정, 검토 로직, 체크포인트 정책이 없습니다. 에이전트는 명령의 안내를 받아 그 결정을 내립니다.

Core loop:

**[한국어]**

핵심 루프:

1. Select a pipeline.
2. Run preflight.
3. Discover real tools from the registry.
4. Present the user with concepts, tool plan, production plan, and cost.
5. Execute stage by stage with checkpoints.

1. 파이프라인 선택.
2. 사전 점검 실행.
3. 레지스트리에서 실제 도구 발견.
4. 사용자에게 컨셉, 도구 계획, 제작 계획, 비용 제시.
5. 체크포인트와 함께 단계별 실행.

---

## Decision Communication Contract (결정 의사소통 계약)

For any meaningful production decision, the agent must communicate the decision before acting. The user should never have to infer which provider, model, or render path was chosen after the fact.

**[한국어]**

의미 있는 모든 제작 결정에 대해, 에이전트는 실행하기 전에 결정을 전달해야 합니다. 사용자는 사후에 어떤 프로바이더, 모델, 또는 렌더링 경로가 선택되었는지 추론해서는 안 됩니다.

### Announce Before Execution (실행 전 발표)

Before any paid or consequential generation call, state:

**[한국어]**

유료이거나 중요한 생성 호출을 하기 전에 다음을 명시하십시오:

- the exact tool name,
- the provider,
- the model or provider variant,
- the reason it was chosen,
- whether it is a sample or a batch run.

- 정확한 도구 이름,
- 프로바이더,
- 모델 또는 프로바이더 변형,
- 선택된 이유,
- 샘플 실행인지 일괄 실행인지 여부.

### Ask Before Major Changes (주요 변경 전 질문)

The agent must ask the user before changing any major production choice, including:

**[한국어]**

에이전트는 다음을 포함한 모든 주요 제작 선택을 변경하기 전에 사용자에게 물어봐야 합니다:

- switching provider,
- switching model family or provider variant,
- switching from video-led to still-led treatment,
- switching composition engine when that changes the output character,
- dropping narration, music, or other approved creative elements,
- changing from sample mode to batch mode.

- 프로바이더 전환,
- 모델 계열 또는 프로바이더 변형 전환,
- 동영상 기반에서 스틸 이미지 기반 처리로 전환,
- 출력 특성을 변경하는 합성 엔진 전환,
- 내레이션, 음악, 또는 기타 승인된 창의적 요소 제거,
- 샘플 모드에서 일괄 모드로 변경.

Minor prompt refinements inside an already approved provider/model path do not require separate approval unless they materially change the creative direction.

**[한국어]**

이미 승인된 프로바이더/모델 경로 내의 사소한 프롬프트 수정은 창의적 방향을 실질적으로 변경하지 않는 한 별도 승인이 필요하지 않습니다.

### Re-log Changed Decisions (Binding) (변경된 결정 재기록 (구속적))

The `decision_log` is the board's Decisions rail and the run's audit trail. It is **append-only history, not a scratchpad.** When a choice you already logged changes mid-run — the user swaps the voice, you switch provider/model/runtime/music, or a fallback overrides an earlier pick — you MUST **append a new `decision_log` entry** for the new choice, reusing the **same `category` AND the same `subject`** (e.g. `category: "voice_selection"`, `subject: "Narration TTS provider"`), with the superseded option moved into `options_considered` and `rejected_because` noting it was changed.

**[한국어]**

`decision_log`는 보드의 Decisions 레일과 실행의 감사 추적입니다. 이것은 **추가 전용 기록이고 스크래치패드가 아닙니다.** 이미 기록한 선택이 실행 중간에 변경될 때 — 사용자가 목소리를 바꾸거나, 프로바이더/모델/런타임/음악을 전환하거나, 대체안이 이전 선택을 덮어쓸 때 — 새로운 선택에 대해 **새로운 `decision_log` 항목을 추가해야 합니다.** 이때 **동일한 `category`와 동일한 `subject`**를 재사용하고 (예: `category: "voice_selection"`, `subject: "Narration TTS provider"`), 대체된 옵션을 `options_considered`로 이동하고 `rejected_because`에 변경되었음을 표시하십시오.

Editing only a downstream artifact (the `asset_manifest`, a prop) while leaving the old decision in the log is a defect: the board keeps showing the stale choice (e.g. `voice → openai_onyx` after the user moved to Chirp3). The board identifies a decision by its **(category, subject) pair** and renders the latest entry for that pair as current (tagged "revised") — so the fix is to append the new entry with an identical `subject`, never to silently mutate the old one or reword the subject (a reworded subject reads as a different decision and both will show). Keeping distinct decisions in one category (e.g. TTS vs image `provider_selection`) is exactly why the pair, not the category alone, is the key. This applies at every stage, not just `idea`.

**[한국어]**

하류 아티팩트(`asset_manifest`, 소품)만 편집하고 로그에 이전 결정을 그대로 두는 것은 결함입니다: 보드가 오래된 선택을 계속 표시합니다 (예: 사용자가 Chirp3로 이동한 후 `voice → openai_onyx`). 보드는 **(category, subject) 쌍**으로 결정을 식별하고 해당 쌍의 최신 항목을 현재 것으로 렌더링합니다 ("revised"로 태그됨) — 따라서 수정 방법은 동일한 `subject`로 새 항목을 추가하는 것이지, 이전 항목을 조용히 변경하거나 주제를 재작성하는 것이 아닙니다 (재작성된 주제는 다른 결정으로 읽히고 둘 다 표시됨). 한 카테고리(TTS vs 이미지 `provider_selection`)에서 별개 결정을 유지하는 것은 쌍이 카테고리만이 아닌 핵심인 이유입니다. 이것은 `idea`뿐만 아니라 모든 단계에 적용됩니다.

### Present Both Composition Runtimes (HARD RULE) (두 합성 런타임 모두 제시 (강력한 룰))

When both Remotion and HyperFrames are available on the machine (check `video_compose.get_info()["render_engines"]`), the agent **MUST present both options to the user** before locking `render_runtime` at the proposal stage. The agent MAY recommend one with rationale — but silently picking a "default" is forbidden even when the pipeline manifest or a director skill suggests one.

**[한국어]**

머신에서 Remotion과 HyperFrames를 모두 사용할 수 있을 때 (`video_compose.get_info()["render_engines"]` 확인), 에이전트는 **제안 단계에서 `render_runtime`을 잠그기 전에 사용자에게 두 옵션을 모두 제시해야 합니다.** 에이전트는 근거와 함께 하나를 추천할 수 있습니다 — 하지만 파이프라인 매니페스트나 감독 스킬이 하나를 제안하더라도 조용히 "기본값"을 선택하는 것은 금지됩니다.

The presentation MUST include, for each runtime:

**[한국어]**

제시는 각 런타임에 대해 다음을 반드시 포함해야 합니다:

1. A one-sentence plain-language description of what it is best at for **this specific brief**.
2. A one-sentence honest tradeoff (why it might not be the right pick here).
3. The agent's recommendation and the reason, tied to the brief's delivery_promise and visual approach.

1. **이 특정 브리프**에서 가장 잘하는 것에 대한 한 문장 평이한 언어 설명.
2. 한 문장의 솔직한 트레이드오프 (여기서 올바른 선택이 아닐 수 있는 이유).
3. 브리프의 delivery_promise와 시각적 접근법과 연결된 에이전트의 추천과 이유.

Then wait for explicit user approval before advancing. Record the full shortlist — BOTH runtimes plus any "ffmpeg" option that applies — as `options_considered` in the `render_runtime_selection` decision logged in `decision_log`. A decision log entry with only one runtime considered when both were available is a CRITICAL reviewer finding.

**[한국어]**

그 후 진행하기 전에 명시적인 사용자 승인을 기다리십시오. `decision_log`에 기록된 `render_runtime_selection` 결정의 `options_considered`로 전체 후보 목록 — 두 런타임 모두와 적용되는 "ffmpeg" 옵션 — 기록하십시오. 두 런타임을 모두 사용할 수 있었을 때 하나만 고려한 결정 로그 항목은 **심각한** 검토자 발견입니다.

Exception: if only one runtime is available on the machine, the agent proceeds with it but MUST say so explicitly ("HyperFrames isn't installed on this machine; I'm proceeding with Remotion. Install HyperFrames if you want the alternative."). The `render_runtime_selection` decision still records the unavailable option as `rejected_because: "runtime not available on this machine"`.

**[한국어]**

예외: 머신에서 하나의 런타임만 사용할 수 있으면, 에이전트는 그것으로 진행하지만 명시적으로 그렇다고 말해야 합니다 ("HyperFrames가 이 머신에 설치되지 않았습니다. Remotion으로 진행합니다. 대안을 원하시면 HyperFrames를 설치하십시오."). `render_runtime_selection` 결정은 여전히 사용할 수 없는 옵션을 `rejected_because: "runtime not available on this machine"`로 기록합니다.

This rule applies to every pipeline that invokes `video_compose` — not just Wave 1. A pipeline's director skill may recommend a runtime, but that recommendation is input to the conversation with the user, not a decision.

**[한국어]**

이 룰은 `video_compose`를 호출하는 모든 파이프라인에 적용됩니다 — Wave 1만이 아닙니다. 파이프라인의 감독 스킬은 런타임을 추천할 수 있지만, 그 추천은 사용자와의 대화에 대한 입력이지 결정이 아닙니다.

### Composition Authoring Mode — Templated vs Atelier (합성 저작 모드 — 템플릿 vs 아틀리에)

Orthogonal to *runtime* is *authoring mode*: **how** the composition is built. Present it as its own proposal decision and log it in `decision_log` (`category: "composition_mode"`).

**[한국어]**

*런타임*과 직교하는 것은 *저작 모드*: 합성이 **어떻게** 구축되는지입니다. 이것을 자체 제안 결정으로 제시하고 `decision_log`에 기록하십시오 (`category: "composition_mode"`).

- **Templated** — assemble the stock `cut.type` scene-types (`text_card`, `stat_card`, `bar_chart`, …) into the `Explainer`/`CinematicRenderer` compositions. Fast, cheap, reliable — and the reason most videos look alike. Right for batch output, localization variants, quick drafts, and low-stakes internal clips.
- **Atelier** — **hand-author the composition from scratch**: bespoke scenes, a one-off theme, and motion written for this piece, rendered via `composition_mode: "atelier"` (see `video_compose` → `_render_via_atelier`). No reusable creative components; a fresh visual language every time.

**[한국어]**

- **템플릿** — 스톡 `cut.type` 장면 유형(`text_card`, `stat_card`, `bar_chart`, …)을 `Explainer`/`CinematicRenderer` 합성으로 조립합니다. 빠르고, 저렴하고, 신뢰할 수 있습니다 — 그리고 대부분의 동영상이 비슷해 보이는 이유입니다. 일괄 출력, 현지화 변형, 빠른 초안, 저위험 내부 클립에 적합합니다.
- **아틀리에** — **처음부터 수작성으로 합성**: 맞춤 장면, 일회용 테마, 이 작품을 위해 작성된 모션, `composition_mode: "atelier"`를 통해 렌더링 (`video_compose` → `_render_via_atelier` 참조). 재사용 가능한 창의적 구성요소 없음; 매번 새로운 시각 언어.

**Default to atelier for hero work** — marketing, launches, brand pieces, any single-deliverable explainer that must impress. The deciding rule: *reuse engine knowledge, never creative components.* In atelier mode the stock scene-type catalog, `hyperframes-registry` blocks, fixtures, and finished components are **off-limits** — they are frozen looks that reintroduce sameness. Before building, route through **`skills/meta/taste-direction.md`** to set the design read and taste dials, then **`skills/meta/bespoke-composition.md`**, which sequences: art direction (`visual-style`) → motion principles (Disney 12 via `framer-motion`/`lottie-bodymovin`) → engine mechanics (`remotion-best-practices` + the stock components read *only as a mechanics codex*) → render via the atelier path. Close with a **distinctness review**: *could this be any other product's video? does it reuse a look I've made before?* — the inverse of "does it match the reference." Atelier costs more tokens and iteration than templated; say so at proposal so the user opts in knowingly.

**[한국어]**

**주요 작업에는 아틀리에를 기본으로 하십시오** — 마케팅, 출시, 브랜드 비디오, 인상을 남겨야 하는 모든 단일 납품 설명 영상. 결정 규칙: *엔진 지식은 재사용하고, 창의적 구성요소는 재사용하지 마십시오.* 아틀리에 모드에서 스톡 장면 유형 카탈로그, `hyperframes-registry` 블록, fixture, 완성된 구성요소는 **금지**됩니다 — 이것들은 동질성을 다시 도입하는 고정된 룩입니다. 구축하기 전에 **`skills/meta/taste-direction.md`**를 통해 디자인 리드와 취향 다이얼을 설정한 다음 **`skills/meta/bespoke-composition.md`**를 순서대로 진행하십시오: 아트 디렉션 (`visual-style`) → 모션 원칙 (Disney 12 via `framer-motion`/`lottie-bodymovin`) → 엔진 메커니즘 (`remotion-best-practices` + *메커니즘 코드로만 읽는* 스톡 구성요소) → 아틀리에 경로를 통한 렌더링. **차별성 검토**로 마무리: *이것이 다른 제품의 동영상이 될 수 있나? 이전에 만든 룩을 재사용하는가?* — "참조와 일치하는가"의 역. 아틀리에는 템플릿보다 더 많은 토큰과 반복을 필요로 합니다. 제안 단계에서 그렇게 말하여 사용자가 알고 선택하도록 하십시오.

### Escalate Blockers Explicitly (차단점을 명시적으로 에스컬레이트)

When a blocker occurs, the agent must surface it immediately using this structure:

**[한국어]**

차단점이 발생하면 에이전트는 즉시 다음 구조를 사용하여 표시해야 합니다:

1. What was attempted
2. What failed
3. Whether the issue is auth, provider access, tool bug, or prompt/design quality
4. What options exist next
5. Which option the agent recommends, with reasoning

1. 시도한 것
2. 실패한 것
3. 문제가 인증, 프로바이더 액세스, 도구 버그, 또는 프롬프트/디자인 품질 중 어디에 있는지
4. 다음에 어떤 옵션이 있는지
5. 에이전트가 추천하는 옵션과 이유

Do not continue with a substitute path until the user approves.

**[한국어]**

사용자가 승인할 때까지 대체 경로로 계속하지 마십시오.

### Recommendation Style (추천 스타일)

When asking the user to choose, do not just list options. The agent should:

**[한국어]**

사용자에게 선택을 요청할 때, 옵션만 나열하지 마십시오. 에이전트는 다음을 해야 합니다:

- provide the shortlist,
- explain the tradeoffs briefly,
- recommend one option,
- wait for approval before proceeding.

- 후보 목록 제공,
- 트레이드오프를 간단히 설명,
- 한 옵션 추천,
- 진행하기 전에 승인 대기.

### No Unilateral Substitutions (일방적 대체 금지)

If the approved path is blocked, the agent may investigate and prepare alternatives, but may not execute those alternatives without user approval.

**[한국어]**

승인된 경로가 차단되면, 에이전트는 대안을 조사하고 준비할 수 있지만 사용자 승인 없이 그 대안을 실행할 수 없습니다.

This applies especially to:

**[한국어]**

이것은 특히 다음에 적용됩니다:

- provider swaps,
- model swaps,
- fallback tools,
- prompt-only substitutes for reference-driven generation,
- still-image animatics in place of true motion.

- 프로바이더 교체,
- 모델 교체,
- 대체 도구,
- 참조 기반 생성을 위한 프롬프트 전용 대체,
- 실제 모션 대신 스틸 이미지 애니메틱.

---

## Orchestrator (오케스트레이터)

The agent itself orchestrates the production state machine:

**[한국어]**

에이전트 자체가 제작 상태 머신을 오케스트레이션합니다:

`research -> proposal -> script -> scene_plan -> assets -> edit -> compose`

The agent:

**[한국어]**

에이전트:

1. Reads the pipeline manifest (`pipeline_defs/*.yaml`) to know the process
2. Calls `checkpoint.get_next_stage()` to find where to resume
3. Reads the stage's director skill (`skills/pipelines/<pipeline>/<stage>-director.md`) to know HOW
4. Uses tools (`tools/`) for concrete capabilities
5. Self-reviews using the reviewer meta skill (`skills/meta/reviewer.md`)
6. Checkpoints via the checkpoint protocol (`skills/meta/checkpoint-protocol.md`)
7. Presents to human for approval when `human_approval_default: true`

1. 프로세스를 알기 위해 파이프라인 매니페스트(`pipeline_defs/*.yaml`) 읽기
2. 재개할 위치를 찾기 위해 `checkpoint.get_next_stage()` 호출
3. 방법을 알기 위해 단계의 감독 스킬(`skills/pipelines/<pipeline>/<stage>-director.md`) 읽기
4. 구체적인 기능을 위해 도구(`tools/`) 사용
5. 검토자 메타 스킬(`skills/meta/reviewer.md`)을 사용한 자체 검토
6. 체크포인트 프로토콜(`skills/meta/checkpoint-protocol.md`)을 통한 체크포인트
7. `human_approval_default: true`일 때 승인을 위해 인간에게 제시

Infrastructure files:

**[한국어]**

인프라 파일:

- `lib/checkpoint.py` — read/write checkpoints, stage validation
- `tools/cost_tracker.py` — budget governance
- `lib/pipeline_loader.py` — manifest loading and helpers

- `lib/checkpoint.py` — 체크포인트 읽기/쓰기, 단계 검증
- `tools/cost_tracker.py` — 예산 관리
- `lib/pipeline_loader.py` — 매니페스트 로딩 및 헬퍼

---

## Project Directory Convention (프로젝트 디렉토리 규칙)

Every production run creates a project workspace under `projects/`. This directory is gitignored — all generated assets are regenerable.

**[한국어]**

모든 제작 실행은 `projects/` 아래에 프로젝트 워크스페이스를 생성합니다. 이 디렉토리는 gitignore됩니다 — 생성된 모든 자산은 재생성 가능합니다.

```
projects/<project-name>/
├── artifacts/          # JSON artifacts from each stage (research_brief, script, scene_plan, etc.)
├── assets/
│   ├── images/         # Generated images (PNG)
│   ├── video/          # Generated video clips (MP4)
│   ├── audio/          # Narration segments + final mix (MP3/WAV)
│   ├── music/          # Background music track (MP3)
│   └── subtitles.srt   # Generated subtitles
└── renders/
    └── final.mp4       # Final rendered video (the deliverable)
```

**Naming convention**: Use kebab-case derived from the video title (e.g., `hidden-math-of-nature`, `how-music-rewires-brain`).

**[한국어]**

**명명 규칙**: 동영상 제목에서 파생된 kebab-case 사용 (예: `hidden-math-of-nature`, `how-music-rewires-brain`).

At pipeline initialization, before any stage runs:

**[한국어]**

파이프라인 초기화 시, 모든 단계 실행 전:

1. **Initialize the workspace**: `python -c "from lib.checkpoint import init_project; init_project('<project-id>', title='<Title>', pipeline_type='<pipeline>')"` — creates the layout above and writes `project.json` (the marker the Backlot board reads).
2. **Open the board**: run `python -m backlot open <project-id>`. This starts the Backlot server if needed and opens the user's browser at the project's live board. If the command fails, continue the production — the board is an observer, never a blocker. This is the agent's ONLY board duty; the board derives everything else from disk.

1. **워크스페이스 초기화**: `python -c "from lib.checkpoint import init_project; init_project('<project-id>', title='<Title>', pipeline_type='<pipeline>')"` — 위 레이아웃을 생성하고 `project.json`을 씁니다 (Backlot 보드가 읽는 마커).
2. **보드 열기**: `python -m backlot open <project-id>`를 실행하십시오. 필요하면 Backlot 서버를 시작하고 사용자 브라우저에서 프로젝트의 라이브 보드를 엽니다. 명령이 실패해도 제작을 계속하십시오 — 보드는 관찰자이지 차단점이 아닙니다. 이것이 에이전트의 **유일한** 보드 의무입니다. 보드는 그 외 모든 것을 디스크에서 파생합니다.

All tools and agents must write outputs to these paths — **always pass an explicit `output_path` under `projects/<project-id>/`**. Assets written to the repo root, cwd, or temp dirs are invisible to the user's board and violate the workspace contract.

**[한국어]**

모든 도구와 에이전트는 이 경로에 출력을 써야 합니다 — **항상 `projects/<project-id>/` 아래에 명시적인 `output_path`를 전달하십시오.** repo root, cwd, 임시 디렉토리에 쓴 자산은 사용자의 보드에 보이지 않으며 워크스페이스 계약을 위반합니다.

**This applies to atelier and HyperFrames-skill runs too**: hand-authored compositions still write the canonical artifacts they have (script or beats-plan, scene_plan-equivalent, asset manifest) plus checkpoints into `projects/<project-id>/`. The board is runtime-agnostic; only runs that skip the artifacts get a degraded board.

**[한국어]**

**이것은 아틀리에와 HyperFrames 스킬 실행에도 적용됩니다**: 수작성된 합성도 가지고 있는 정품 아티팩트(스크립트 또는 비트 계획, scene_plan 동등물, 자산 매니페스트)와 체크포인트를 `projects/<project-id>/`에 씁니다. 보드는 런타임에 무관합니다. 아티팩트를 건너뛴 실행만 저하된 보드를 받습니다.

---

## Music Library (음악 라이브러리)

Users can place royalty-free music tracks in `music_library/` (gitignored). The asset director will check this folder before falling back to API-based music generation.

**[한국어]**

사용자는 `music_library/` (gitignore됨)에 로열티 프리 음악 트랙을 둘 수 있습니다. 자산 감독은 API 기반 음악 생성으로 대체하기 전에 이 폴더를 확인합니다.

```
music_library/
├── ambient_track.mp3
├── cinematic_epic.mp3
└── ...
```

If the folder has tracks, the proposal and asset stages should present them as options alongside generated music. See the proposal-director and asset-director skills for details.

**[한국어]**

폴더에 트랙이 있으면 제안 및 자산 단계는 생성된 음악과 함께 옵션으로 제시해야 합니다. 자세한 내용은 proposal-director와 asset-director 스킬을 참조하십시오.

---

## Available Pipelines (사용 가능한 파이프라인)

| Pipeline | Best For | Stability |
|----------|----------|-----------|
| `animated-explainer` | Topic to fully generated explainer | production |
| `talking-head` | Footage-led speaker videos | beta |
| `screen-demo` | Screen recordings and walkthroughs | production |
| `clip-factory` | Many clips from one long source | beta |
| `podcast-repurpose` | Podcast highlights and derivatives | beta |
| `cinematic` | Trailer, teaser, and mood-led edits | production |
| `animation` | Motion-graphics and animation-first videos | production |
| `character-animation` | Local rigged cartoon characters and reusable character acting | beta |
| `hybrid` | Source footage plus support visuals | production |
| `avatar-spokesperson` | Presenter-led avatar or lip-sync videos | production |
| `localization-dub` | Subtitle, dub, and translated variants | beta |
| `framework-smoke` | Test: minimal 2-stage smoke test | test |

| 파이프라인 | 최적 용도 | 안정성 |
|----------|----------|-----------|
| `animated-explainer` | 주제를 완전 생성된 설명 영상으로 | production |
| `talking-head` | 풋티지 기반 스피커 동영상 | beta |
| `screen-demo` | 화면 녹화 및 워크스루 | production |
| `clip-factory` | 긴 소스에서 여러 클립 | beta |
| `podcast-repurpose` | 팟캐스트 하이라이트 및 파생물 | beta |
| `cinematic` | 트레일러, 티저, 무드 기반 편집 | production |
| `animation` | 모션 그래픽 및 애니메이션 우선 동영상 | production |
| `character-animation` | 로컬 리그드 캐릭터 및 재사용 가능한 캐릭터 연기 | beta |
| `hybrid` | 소스 풋티지 + 보조 시각 자료 | production |
| `avatar-spokesperson` | 프레젠터 기반 아바타 또는 립싱크 동영상 | production |
| `localization-dub` | 자막, 더빙, 번역 변형 | beta |
| `framework-smoke` | 테스트: 최소 2단계 스모크 테스트 | test |

> **Beta pipelines** have not been fully audited. They work, but expect rough edges. Mention this when the user selects one.

**[한국어]**

> **베타 파이프라인**은 완전히 감사되지 않았습니다. 작동하지만 거친 부분을 예상하십시오. 사용자가 하나를 선택할 때 이것을 언급하십시오.

---

## Mandatory Preflight (의무 사전 점검)

Do this before any creative work. **Use `provider_menu_summary()` first — it's the human-ready rollup.** The raw `support_envelope()` dump is a firehose (megabytes of JSON on a well-configured machine); pasting it into chat will bury the user.

**[한국어]**

모든 창작 작업 전에 이것을 수행하십시오. **먼저 `provider_menu_summary()`를 사용하십시오 — 인간이 읽기 쉬운 요약입니다.** 원시 `support_envelope()` 덤프는 소방호스입니다 (잘 구성된 머신에서 JSON 메가바이트). 채팅에 붙여넣으면 사용자를 파묻습니다.

```bash
python -c "
from tools.tool_registry import registry
import json
registry.discover()
print(json.dumps(registry.provider_menu_summary(), indent=2))
"
```

The summary returns four fields the agent should translate into plain language:

**[한국어]**

요약은 에이전트가 평이한 언어로 번역해야 하는 4개 필드를 반환합니다:

- `composition_runtimes` — booleans for `ffmpeg`, `remotion`, `hyperframes`. This is the source of truth for the "Present Both Composition Runtimes (HARD RULE)" check.
- `capabilities[]` — one entry per capability family with `configured / total` counts and provider lists. Ready-made for the "N of M configured" menu.
- `setup_offers[]` — unavailable tools whose install is a 1-minute env-var fix. Lead with these when offering upgrades.
- `runtime_warnings[]` — specific signals like "hyperframes: npm package not resolvable". Surface these to the user verbatim — they're the kind of silent-failure bugs that break the governance contract.

- `composition_runtimes` — `ffmpeg`, `remotion`, `hyperframes`의 불리언. "두 합성 런타임 모두 제시 (HARD RULE)" 확인의 진실의 원천입니다.
- `capabilities[]` — 기능 계열당 `configured / total` 카운트와 프로바이더 목록이 있는 하나의 항목. "M개 중 N개 구성됨" 메뉴에 바로 사용 가능.
- `setup_offers[]` — 설치가 1분 env-var 수정인 사용 불가능 도구. 업그레이드 제안 시 이것을 먼저 제시.
- `runtime_warnings[]` — "hyperframes: npm package not resolvable" 같은 구체적 신호. 이것을 사용자에게 있는 그대로 전달하십시오 — 거버넌스 계약을 깨는 조용한 실패 버그의 종류입니다.

Then, for deeper inspection (only when the summary isn't enough):

**[한국어]**

그 후 더 깊은 검사를 위해 (요약이 충분하지 않을 때만):

```bash
# Full menu — grouped available/unavailable per capability.
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu(), indent=2))"

# Raw envelope — every tool's full contract. Slow/firehose; use for debugging only.
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.support_envelope(), indent=2))"
```

Then:

**[한국어]**

그 후:

1. Read the selected manifest in `pipeline_defs/`.
2. Check every `required_tools` entry against the registry.
3. Check `fallback_tools` for unavailable tools.
4. Report one of: `passed`, `degraded`, or `blocked`.
5. Do not start production until the user understands the real capability envelope.

1. `pipeline_defs/`에서 선택된 매니페스트를 읽으십시오.
2. 레지스트리에 대해 모든 `required_tools` 항목을 확인하십시오.
3. 사용 불가능 도구에 대해 `fallback_tools`를 확인하십시오.
4. 다음 중 하나를 보고하십시오: `passed`, `degraded`, `blocked`.
5. 사용자가 실제 기능 범위를 이해할 때까지 제작을 시작하지 마십시오.

### Provider Menu (Mandatory at Preflight) (프로바이더 메뉴 (사전 점검 시 의무))

Already fetched via `provider_menu_summary()` above. Read that output and **present it to the user as a capability menu**, not as a flat tool list. Use `provider_menu()` directly only when you need the per-tool detail the summary collapses.

**[한국어]**

이미 위 `provider_menu_summary()`를 통해 가져왔습니다. 해당 출력을 읽고 **기능 메뉴로 사용자에게 제시하십시오**, 평평한 도구 목록이 아닙니다. 요약이 축소하는 도구별 세부 정보가 필요할 때만 `provider_menu()`를 직접 사용하십시오.

**How to present:**

**[한국어]**

**제시 방법:**

```
YOUR CAPABILITIES

  Video Generation:  0/13 configured
  Image Generation:  1/7 configured
  Text-to-Speech:    1/3 configured
  Music Generation:  1/1 configured
  Composition:       3/3 configured (FFmpeg, video_stitch, video_trimmer)

  You can produce videos now with images + TTS + FFmpeg.
  Quick upgrades available — see below.
```

```
사용 가능 기능

  동영상 생성:  0/13개 구성됨
  이미지 생성:  1/7개 구성됨
  텍스트 음성 변환:    1/3개 구성됨
  음악 생성:  1/1개 구성됨
  합성:       3/3개 구성됨 (FFmpeg, video_stitch, video_trimmer)

  지금 이미지 + TTS + FFmpeg로 동영상을 제작할 수 있습니다.
  빠른 업그레이드 가능 — 아래 참조.
```

For EACH capability with unavailable providers, read the `install_instructions` field from the menu output and present setup options grouped by effort:

**[한국어]**

사용 불가능 프로바이더가 있는 **각** 기능에 대해, 메뉴 출력에서 `install_instructions` 필드를 읽고 노력별로 그룹화된 설정 옵션을 제시하십시오:

```
QUICK SETUP OPTIONS (1-minute each — set an env var in .env)

  Video Generation (0/13 -> unlock the biggest upgrade):
    Each unavailable provider lists its own install_instructions.
    Read them from the provider_menu output and present grouped by env var.
    Example: if 3 tools need FAL_KEY, group them: "FAL_KEY unlocks 3 providers"

  Image Generation (1/7 -> more style options):
    Same pattern — read install_instructions from each unavailable tool.

  Text-to-Speech (1/3):
    Same pattern.

LOCAL OPTIONS (free, needs hardware):
  Tools with runtime=LOCAL or runtime=LOCAL_GPU — read from the menu.

Already Available:
  List what's working. The user should feel good about what they have.
```

```
빠른 설정 옵션 (각 1분 — .env에서 env var 설정)

  동영상 생성 (0/13 -> 최대 업그레이드 해제):
    사용 불가능 각 프로바이더는 자체 install_instructions를 나열합니다.
    provider_menu 출력에서 읽고 env var별로 그룹화하여 제시하십시오.
    예: 3개 도구가 FAL_KEY를 필요하면 그룹화: "FAL_KEY가 3개 프로바이더를 해제합니다"

  이미지 생성 (1/7 -> 더 많은 스타일 옵션):
    같은 패턴 — 사용 불가능 각 도구의 install_instructions 읽기.

  텍스트 음성 변환 (1/3):
    같은 패턴.

로컬 옵션 (무료, 하드웨어 필요):
  runtime=LOCAL 또는 runtime=LOCAL_GPU 도구 — 메뉴에서 읽기.

이미 사용 가능:
  작동하는 것 나열. 사용자가 가진 것에 대해 좋게 느껴야 합니다.
```

**Rules:**

**[한국어]**

**규칙:**

- Do NOT hardcode provider names, API key names, or setup URLs in your prompts.
  Read them from the registry's `install_instructions` field on each tool.
- Always show the ratio: "X of Y configured" — this makes breadth visible.
- Group by capability, not by individual tool.
- Show what they CAN do now, then what they COULD unlock.
- If the user declines setup, proceed with the best available path — no nagging.
- If a tool shares an env var with others, group them (read from `dependencies` field).

- 프롬프트에 프로바이더 이름, API 키 이름, 설정 URL을 하드코딩하지 마십시오.
  각 도구의 레지스트리 `install_instructions` 필드에서 읽으십시오.
- 항상 비율을 표시하십시오: "Y개 중 X개 구성됨" — 범위를 보여줍니다.
- 개별 도구별이 아닌 기능별로 그룹화하십시오.
- 지금 할 수 있는 것, 그리고 해제할 수 있는 것을 보여주십시오.
- 사용자가 설정을 거부하면 최상의 사용 가능 경로로 진행하십시오 — 잔소리 없음.
- 도구가 다른 도구와 env var를 공유하면 그룹화하십시오 (`dependencies` 필드에서 읽기).

### Setup Offer Protocol (설정 제안 프로토콜)

When tools are `UNAVAILABLE` but can be fixed with simple configuration, **offer the user setup help instead of silently working around the limitation.** Many tools are one env var away from working.

**[한국어]**

도구가 `UNAVAILABLE`이지만 간단한 설정으로 수정될 수 있을 때, **제한을 조용히 우회하는 대신 사용자 설정 도움을 제시하십시오.** 많은 도구는 하나의 env var만 있으면 작동합니다.

| Fix Complexity | Action |
|----------------|--------|
| **1-minute fix** (env var) | Offer to help configure now — read `install_instructions` from the tool |
| **5-minute fix** (install) | Explain what to install and why — read `install_instructions` from the tool |
| **Complex fix** (GPU, model download) | Note the limitation, explain what it would unlock, move on |

| 수정 복잡도 | 작업 |
|----------------|--------|
| **1분 수정** (env var) | 지금 설정 도움 제안 — 도구의 `install_instructions` 읽기 |
| **5분 수정** (설치) | 설치할 것과 이유 설명 — 도구의 `install_instructions` 읽기 |
| **복잡한 수정** (GPU, 모델 다운로드) | 제한 표시, 해제할 것 설명, 계속 진행 |

**Rules:**
- Always tell the user what they're missing AND what they'd gain
- Show the cost difference (free local vs. paid API)
- If the user declines setup, proceed with the best available path — no nagging
- Group related fixes (tools sharing the same env var dependency)

**[한국어]**

**규칙:**
- 사용자에게 누락된 것과 얻게 될 것을 항상 알려주십시오
- 비용 차이를 보여주십시오 (무료 로컬 vs 유료 API)
- 사용자가 설정을 거부하면 최상의 사용 가능 경로로 진행하십시오 — 잔소리 없음
- 관련 수정을 그룹화하십시오 (같은 env var 의존성을 공유하는 도구)

### Composition Runtimes (Inside video_compose) (합성 런타임 (video_compose 내부))

`video_compose` has **three** render engines / runtimes. They are parallel, not ranked — the choice is made at proposal and locked in `edit_decisions.render_runtime`. Check which are available:

**[한국어]**

`video_compose`는 **세 개**의 렌더링 엔진/런타임을 가지고 있습니다. 이것들은 병렬적이고 순위가 없습니다 — 선택은 제안 시 이루어지고 `edit_decisions.render_runtime`에 잠깁니다. 사용 가능한 것을 확인하십시오:

```bash
python -c "
from tools.tool_registry import registry
registry.discover()
info = registry._tools['video_compose'].get_info()
print('Render engines:', info.get('render_engines'))
print('Remotion note:', info.get('remotion_note'))
print('HyperFrames note:', info.get('hyperframes_note'))
"
```

| Engine | Used For | Requires |
|--------|----------|----------|
| **FFmpeg** | Video-only cuts, concat, trim, subtitle burn | `ffmpeg` binary (always available) |
| **Remotion** | React-based composition: still images → animated video, text cards, stat cards, charts, callouts, comparisons, transitions with spring physics, word-level caption burn, TalkingHead avatar | Node.js (`npx`) + `remotion-composer/` + `node_modules` |
| **HyperFrames** | HTML/CSS/GSAP composition: kinetic typography, product promos, launch reels, website-to-video, registry-block-driven scenes, SVG character rigs | Node.js ≥ 22 + FFmpeg + `npx` (consumed via `npx hyperframes`) |

| 엔진 | 용도 | 필요 사항 |
|--------|----------|----------|
| **FFmpeg** | 동영상 전용 자르기, 연결, 트림, 자막 굽기 | `ffmpeg` 바이너리 (항상 사용 가능) |
| **Remotion** | React 기반 합성: 스틸 이미지 → 애니메이션 동영상, 텍스트 카드, 통계 카드, 차트, 콜아웃, 비교, 스프링 물리가 있는 전환, 단어 수준 자막 굽기, TalkingHead 아바타 | Node.js (`npx`) + `remotion-composer/` + `node_modules` |
| **HyperFrames** | HTML/CSS/GSAP 합성: 키네틱 타이포그래피, 제품 프로모, 출시 릴, 웹사이트-동영상, 레지스트리 블록 기반 장면, SVG 캐릭터 리그 | Node.js ≥ 22 + FFmpeg + `npx` (`npx hyperframes`를 통해 소비) |

`render_runtime` is **locked at proposal** (`proposal_packet.production_plan.render_runtime`) and **carried through edit_decisions unchanged**. `video_compose` routes based on this field; silent runtime swaps are forbidden. If the chosen runtime becomes unavailable at compose time, surface a structured blocker per "Escalate Blockers Explicitly" above. See `skills/core/hyperframes.md` for the Remotion-vs-HyperFrames decision matrix.

**[한국어]**

`render_runtime`은 **제안 시 잠깁니다** (`proposal_packet.production_plan.render_runtime`) 그리고 **edit_decisions를 통해 변경 없이 전달됩니다.** `video_compose`는 이 필드를 기준으로 라우팅합니다. 조용한 런타임 교체는 금지됩니다. 선택한 런타임이 합성 시 사용 불가능해지면, 위 "차단점을 명시적으로 에스컬레이트"에 따른 구조화된 차단점을 표시하십시오. Remotion-vs-HyperFrames 결정 행렬은 `skills/core/hyperframes.md`를 참조하십시오.

### Critical Rule: Motion-Required Requests (중요한 룰: 모션 필수 요청)

For any request where the deliverable inherently depends on motion rather than static coverage, treat motion as a hard requirement. Examples:

**[한국어]**

납품물이 본질적으로 정적 커버리지가 아닌 모션에 의존하는 모든 요청에 대해, 모션을 강력 요구사항으로 처리하십시오. 예:

- sci-fi trailers,
- cinematic teasers built from generated clips,
- hype edits,
- avatar or agent videos,
- any brief whose promise depends on moving shots rather than still frames.

- SF 트레일러,
- 생성된 클립으로 구축된 시네마틱 티저,
- 하이프 에딧,
- 아바타 또는 에이전트 동영상,
- 약속이 스틸 프레임이 아닌 움직이는 샷에 의존하는 모든 브리프.

For these requests:

**[한국어]**

이러한 요청에 대해:

- The `render_runtime` chosen at proposal (Remotion, HyperFrames, or FFmpeg) must be confirmed available up front if the planned visual treatment depends on it.
- Still-image fallback is forbidden. Do not quietly convert the job into a Ken Burns teaser, animatic, or slide-based video.
- FFmpeg-only fallback is forbidden when it changes the approved deliverable from motion-led video to still-led video.
- **Silent runtime swap is forbidden.** If `render_runtime="hyperframes"` was locked and HyperFrames is unavailable, do NOT route to Remotion instead. Surface the blocker, propose options, get user approval, log a `render_runtime_selection` decision — then proceed.
- Bubble critical issues immediately. If the chosen runtime is unavailable, fails to render, or provider clip generation fails in a way that blocks the approved treatment, stop and tell the user before proceeding.
- Do not spend more tokens or time on downgraded output unless the user explicitly approves the downgrade as an animatic or proof-of-concept.

- 계획된 시각적 처리가 의존하면 제안 시 선택한 `render_runtime`(Remotion, HyperFrames, FFmpeg)이 사전에 사용 가능한지 확인해야 합니다.
- 스틸 이미지 대체는 금지됩니다. 작업을 조용히 Ken Burns 티저, 애니메틱, 또는 슬라이드 기반 동영상으로 변환하지 마십시오.
- 승인된 납품물을 모션 기반 동영상에서 스틸 기반 동영상으로 변경하는 경우 FFmpeg 전용 대체는 금지됩니다.
- **조용한 런타임 교체는 금지됩니다.** `render_runtime="hyperframes"`가 잠겼는데 HyperFrames를 사용할 수 없으면, Remotion으로 대신 라우팅하지 마십시오. 차단점을 표시하고, 옵션을 제안하고, 사용자 승인을 받고, `render_runtime_selection` 결정을 기록하십시오 — 그 후 진행하십시오.
- 중요한 이슈를 즉시 표시하십시오. 선택한 런타임을 사용할 수 없거나, 렌더링에 실패하거나, 프로바이더 클립 생성이 승인된 처리를 차단하는 방식으로 실패하면, 진행하기 전에 멈추고 사용자에게 알리십시오.
- 사용자가 애니메틱 또는 개념 증명으로 다운그레이드를 명시적으로 승인하지 않는 한 다운그레이드된 출력에 더 많은 토큰이나 시간을 소비하지 마십시오.

**When Remotion is available**, the agent should design production plans around it:
- Explainer videos with `flat-motion-graphics` playbook -> Remotion animated scenes, not Ken Burns
- Data-driven videos -> Remotion stat cards and charts, not static image screenshots
- Any pipeline using still images -> Remotion spring animations, not FFmpeg pan-and-zoom
- **Screen demos of a CLI/terminal/install flow -> `TerminalScene` (synthetic screen recording), not OS-level capture.** See `.agents/skills/synthetic-screen-recording/SKILL.md`. Faster, deterministic, privacy-safe. Use real capture (`screen_recorder`, `cap_recorder`, `playwright-recording`) only when the demo is a real app UI or requires unpredictable live behavior.

**[한국어]**

**Remotion을 사용할 수 있을 때**, 에이전트는 이것을 중심으로 제작 계획을 설계해야 합니다:
- `flat-motion-graphics` 플레이북이 있는 설명 영상 -> Remotion 애니메이션 장면, Ken Burns 아님
- 데이터 기반 동영상 -> Remotion 통계 카드 및 차트, 정적 이미지 스크린샷 아님
- 스틸 이미지를 사용하는 모든 파이프라인 -> Remotion 스프링 애니메이션, FFmpeg pan-and-zoom 아님
- **CLI/터미널/설치 플로우의 화면 데모 -> `TerminalScene` (합성 화면 녹화), OS 수준 캡처 아님.** `.agents/skills/synthetic-screen-recording/SKILL.md` 참조. 더 빠르고, 결정적이고, 프라이버시에 안전합니다. 실제 캡처(`screen_recorder`, `cap_recorder`, `playwright-recording`)는 데모가 실제 앱 UI이거나 예측 불가능한 라이브 동작이 필요할 때만 사용하십시오.

### Remotion scene types available in `remotion-composer/` (`remotion-composer/`에서 사용 가능한 Remotion 장면 유형)

See `remotion-composer/SCENE_TYPES.md` for the authoritative list and their cut schemas. Current scene types usable via `cut.type`:
`text_card`, `stat_card`, `callout`, `comparison`, `hero_title`, `terminal_scene`, `anime_scene`, `bar_chart`, `line_chart`, `pie_chart`, `kpi_grid`, `progress_bar`. Overlay types include `section_title`, `stat_reveal`, `hero_title`, `provider_chip`.

**[한국어]**

권위 목록과 cut 스키마는 `remotion-composer/SCENE_TYPES.md`를 참조하십시오. `cut.type`을 통해 사용 가능한 현재 장면 유형:
`text_card`, `stat_card`, `callout`, `comparison`, `hero_title`, `terminal_scene`, `anime_scene`, `bar_chart`, `line_chart`, `pie_chart`, `kpi_grid`, `progress_bar`. 오버레이 유형은 `section_title`, `stat_reveal`, `hero_title`, `provider_chip`를 포함합니다.

These stock scene-types are the **templated** path — fast and reliable, but they are why videos look alike. For **hero work, prefer atelier mode** (hand-authored composition) over this catalog; read those types as a *mechanics codex*, not a menu to assemble. See "Composition Authoring Mode" above and `skills/meta/bespoke-composition.md`.

**[한국어]**

이 스톡 장면 유형은 **템플릿** 경로입니다 — 빠르고 신뢰할 수 있지만, 동영상이 비슷해 보이는 이유입니다. **주요 작업에는 아틀리에 모드** (수작성 합성)를 이 카탈로그보다 선호하십시오. 이 유형을 *메커니즘 코드*로 읽지 조립 메뉴로 읽지 마십시오. 위 "합성 저작 모드"와 `skills/meta/bespoke-composition.md`를 참조하십시오.

**When Remotion is NOT available** and `render_runtime="remotion"` was NOT locked, `video_compose` may use FFmpeg Ken Burns motion on still images. This still works but produces less engaging visuals. Mention this tradeoff in the proposal. When `render_runtime="remotion"` IS locked and Remotion is unavailable, that's a blocker — escalate, don't silently swap.

**[한국어]**

**Remotion을 사용할 수 없고** `render_runtime="remotion"`이 잠기지 않았을 때, `video_compose`는 스틸 이미지에 FFmpeg Ken Burns 모션을 사용할 수 있습니다. 이것은 여전히 작동하지만 덜 매력적인 시각 결과를 만듭니다. 제안에서 이 트레이드오프를 언급하십시오. `render_runtime="remotion"`이 잠겼는데 Remotion을 사용할 수 없으면 차단점입니다 — 에스컬레이트하고 조용히 교체하지 마십시오.

When `render_runtime="hyperframes"` is locked and HyperFrames is unavailable (Node < 22, missing `ffmpeg`/`npx`, or `hyperframes doctor` reports issues), that's also a blocker. Do not substitute Remotion or FFmpeg without user approval + a logged `render_runtime_selection` decision.

**[한국어]**

`render_runtime="hyperframes"`가 잠겼는데 HyperFrames를 사용할 수 없으면 (Node < 22, `ffmpeg`/`npx` 누락, 또는 `hyperframes doctor`가 이슈를 보고), 이것 또한 차단점입니다. 사용자 승인 + 기록된 `render_runtime_selection` 결정 없이 Remotion이나 FFmpeg를 대체하지 마십시오.

Routing is automatic — `video_compose` reads `edit_decisions.render_runtime` and dispatches to the matching engine (`_render_via_hyperframes`, `_remotion_render`, or `_render_via_ffmpeg`). But the **agent must know both Remotion and HyperFrames exist at proposal time** so it can design the visual approach intentionally. Don't default to Remotion for motion-graphics-heavy concepts that HTML/GSAP would express more naturally, and don't default to HyperFrames for briefs that reuse the existing React scene stack.

**[한국어]**

라우팅은 자동입니다 — `video_compose`는 `edit_decisions.render_runtime`을 읽고 일치하는 엔진으로 디스패치합니다 (`_render_via_hyperframes`, `_remotion_render`, 또는 `_render_via_ffmpeg`). 하지만 **에이전트는 제안 시 Remotion과 HyperFrames가 모두 존재한다는 것을 알아야** 의도적 시각적 접근법을 설계할 수 있습니다. HTML/GSAP가 더 자연스럽게 표현할 모션 그래픽 중심 컨셉에 Remotion을 기본값으로 하지 마십시오, 기존 React 장면 스택을 재사용하는 브리프에 HyperFrames를 기본값으로 하지 마십시오.

---

## Capability Discovery (기능 발견)

OpenMontage uses two layers for capability choice:

**[한국어]**

OpenMontage는 기능 선택에 두 개 레이어를 사용합니다:

- selector tools: capability-level routing such as `tts_selector` and `video_selector`
- provider tools: concrete tools discovered via the registry that call a specific backend

- 선택자 도구: `tts_selector`와 `video_selector` 같은 기능 수준 라우팅
- 프로바이더 도구: 특정 백엔드를 호출하는 레지스트리를 통해 발견된 구체적 도구

Always inspect the registry first:

**[한국어]**

항상 먼저 레지스트리를 검사하십시오:

```bash
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.capability_catalog(), indent=2))"
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_catalog(), indent=2))"
```

For finalist tools inspect:

**[한국어]**

최종 도구 검사 항목:

- `capability`
- `provider`
- `usage_location`
- `supports`
- `fallback_tools`
- `related_skills`

- `capability`
- `provider`
- `usage_location`
- `supports`
- `fallback_tools`
- `related_skills`

Do not rely on memory or old docs when the registry can answer it.

**[한국어]**

레지스트리가 답변할 수 있을 때 기억이나 오래된 문서에 의존하지 마십시오.

---

## Tool Families (도구 계열)

**Do not maintain hardcoded tool lists.** Always query the registry at runtime:

**[한국어]**

**하드코딩된 도구 목록을 유지하지 마십시오.** 항상 런타임에 레지스트리를 쿼리하십시오:

```bash
# See all tools grouped by capability (TTS, video_generation, image_generation, etc.)
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.capability_catalog(), indent=2))"

# See all tools grouped by provider (elevenlabs, openai, ffmpeg, etc.)
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_catalog(), indent=2))"
```

Key capability families to look for in the output:

**[한국어]**

출력에서 찾을 핵심 기능 계열:

- **tts** — Text-to-speech providers. Route via `tts_selector`.
- **video_generation** — Video generation providers (cloud, local GPU, stock). Route via `video_selector`.
- **image_generation** — Image generation providers (cloud, local GPU, stock). Route via `image_selector`.
- **music_generation** — Music and sound effect generation.
- **video_post** — Composition, stitching, trimming (FFmpeg-based, always local).
- **audio_processing** — Mixing, enhancement (FFmpeg-based, always local).
- **analysis** — Transcription, scene detection, frame sampling.
- **avatar** — Talking head and lip sync generation.
- **character_animation** — Local character specs, SVG rigs, pose libraries, action timelines, previews, and QA.
- **enhancement** — Upscale, background removal, face enhance, color grading.

- **tts** — 텍스트 음성 변환 프로바이더. `tts_selector`를 통한 라우팅.
- **video_generation** — 동영상 생성 프로바이더 (클라우드, 로컬 GPU, 스톡). `video_selector`를 통한 라우팅.
- **image_generation** — 이미지 생성 프로바이더 (클라우드, 로컬 GPU, 스톡). `image_selector`를 통한 라우팅.
- **music_generation** — 음악 및 효과음 생성.
- **video_post** — 합성, 스티칭, 트리밍 (FFmpeg 기반, 항상 로컬).
- **audio_processing** — 믹싱, 향상 (FFmpeg 기반, 항상 로컬).
- **analysis** — 전사, 장면 감지, 프레임 샘플링.
- **avatar** — 토킹 헤드 및 립싱크 생성.
- **character_animation** — 로컬 캐릭터 사양, SVG 리그, 포즈 라이브러리, 액션 타임라인, 프리뷰, QA.
- **enhancement** — 업스케일, 배경 제거, 얼굴 향상, 색상 그레이딩.

Each tool in the registry declares `best_for`, `install_instructions`, `runtime` (LOCAL, API, LOCAL_GPU, HYBRID), and `status`. Read these fields — do not assume tool strengths from memory.

**[한국어]**

레지스트리의 각 도구는 `best_for`, `install_instructions`, `runtime` (LOCAL, API, LOCAL_GPU, HYBRID), `status`를 선언합니다. 이 필드를 읽으십시오 — 기억에서 도구 강점을 가정하지 마십시오.

### Tool Class Naming Convention (도구 클래스 명명 규칙)

All tool classes use **PascalCase without a "Tool" suffix**. When importing tools in Python:

**[한국어]**

모든 도구 클래스는 **"Tool" 접미사 없는 PascalCase**를 사용합니다. Python에서 도구를 가져올 때:

| Module | Class Name | NOT |
|--------|-----------|-----|
| `tools.audio.music_gen` | `MusicGen` | ~~MusicGenTool~~ |
| `tools.video.video_compose` | `VideoCompose` | ~~VideoComposeTool~~ |
| `tools.audio.audio_mixer` | `AudioMixer` | ~~AudioMixerTool~~ |
| `tools.tts.elevenlabs_tts` | `ElevenLabsTTS` | ~~ElevenLabsTTSTool~~ |
| `tools.analysis.transcriber` | `Transcriber` | ~~TranscriberTool~~ |
| `tools.subtitle.subtitle_gen` | `SubtitleGen` | ~~SubtitleGenTool~~ |

| 모듈 | 클래스 이름 | 아님 |
|--------|-----------|-----|
| `tools.audio.music_gen` | `MusicGen` | ~~MusicGenTool~~ |
| `tools.video.video_compose` | `VideoCompose` | ~~VideoComposeTool~~ |
| `tools.audio.audio_mixer` | `AudioMixer` | ~~AudioMixerTool~~ |
| `tools.tts.elevenlabs_tts` | `ElevenLabsTTS` | ~~ElevenLabsTTSTool~~ |
| `tools.analysis.transcriber` | `Transcriber` | ~~TranscriberTool~~ |
| `tools.subtitle.subtitle_gen` | `SubtitleGen` | ~~SubtitleGenTool~~ |

When in doubt, check: `grep "^class " tools/<path>.py`

**[한국어]**

의심스러우면 확인하십시오: `grep "^class " tools/<path>.py`

All tools call via `.execute(params_dict)` (returns `ToolResult` with `.success`, `.data`, `.error`), NOT `.run()`.

**[한국어]**

모든 도구는 `.run()`이 아닌 `.execute(params_dict)`를 통해 호출합니다 (`.success`, `.data`, `.error`가 있는 `ToolResult` 반환).

### Selector Pattern (선택자 패턴)

Three selector tools abstract multi-provider capabilities. **Selectors auto-discover providers from the registry.** Adding a new provider tool automatically makes it available through the selector — no selector code changes needed.

**[한국어]**

세 개 선택자 도구가 다중 프로바이더 기능을 추상화합니다. **선택자는 레지스트리에서 프로바이더를 자동 발견합니다.** 새 프로바이더 도구를 추가하면 선택자를 통해 자동으로 사용 가능하게 됩니다 — 선택자 코드 변경이 필요 없습니다.

| Selector | Routes to | How it discovers |
|----------|-----------|-----------------|
| `tts_selector` | All tools with `capability="tts"` (ElevenLabs, Google TTS, OpenAI, Piper) | `registry.get_by_capability("tts")` |
| `image_selector` | All tools with `capability="image_generation"` (FLUX, Google Imagen, GPT Image, Recraft, etc.) | `registry.get_by_capability("image_generation")` |
| `video_selector` | All tools with `capability="video_generation"` | `registry.get_by_capability("video_generation")` |

| 선택자 | 라우팅 대상 | 발견 방법 |
|----------|-----------|-----------------|
| `tts_selector` | `capability="tts"`인 모든 도구 (ElevenLabs, Google TTS, OpenAI, Piper) | `registry.get_by_capability("tts")` |
| `image_selector` | `capability="image_generation"`인 모든 도구 (FLUX, Google Imagen, GPT Image, Recraft 등) | `registry.get_by_capability("image_generation")` |
| `video_selector` | `capability="video_generation"`인 모든 도구 | `registry.get_by_capability("video_generation")` |

Selectors route based on: user preference > availability > discovery order. They adapt input schemas between providers transparently.

**[한국어]**

선택자는 다음 기준으로 라우팅합니다: 사용자 선호 > 사용 가능성 > 발견 순서. 프로바이더 간 입력 스키마를 투명하게 조정합니다.

---

## User-Facing Planning Protocol (사용자 대상 계획 프로토콜)

Before committing to execution, present:

**[한국어]**

실행에 약속하기 전에 제시하십시오:

1. `4-5` concept directions when the brief is still open.
2. Recommended pipeline.
3. Recommended tool path.
4. Alternative tool paths that are actually available.
5. Cost estimate and quality tradeoffs.
6. **Music plan** — mandatory for every pipeline that has audio. See below.
7. Production plan by stage.
8. Approval gate before asset generation.

1. 브리프가 여전히 열려 있을 때 `4-5`개 컨셉 방향.
2. 추천 파이프라인.
3. 추천 도구 경로.
4. 실제 사용 가능한 대체 도구 경로.
5. 비용 추정 및 품질 트레이드오프.
6. **음악 계획** — 오디오가 있는 모든 파이프라인에 의무. 아래 참조.
7. 단계별 제작 계획.
8. 자산 생성 전 승인 게이트.

If a user prefers a specific vendor and that tool is available, surface it directly. Do not hide provider choice.

**[한국어]**

사용자가 특정 공급업체를 선호하고 그 도구를 사용할 수 있으면 직접 표시하십시오. 프로바이더 선택을 숨기지 마십시오.

### Music Plan (Mandatory) (음악 계획 (의무))

Music is a critical part of any video. **Surface the music situation to the user at proposal/idea time** — do not silently defer it to the asset stage where a failure becomes expensive.

**[한국어]**

음악은 모든 동영상의 중요한 부분입니다. **제안/아이디어 시점에 사용자에게 음악 상황을 표시하십시오** — 실패가 비싸지는 자산 단계로 조용히 연기하지 마십시오.

Check music availability in this order and present the options:

**[한국어]**

이 순서로 음악 사용 가능성을 확인하고 옵션을 제시하십시오:

1. **User music library (`music_library/`):** Check if this folder exists and contains tracks. If so, list available tracks with durations and let the user pick one.
2. **Music generation APIs:** Check which music tools are available via the registry (`registry.get_by_capability("music_generation")`). Report their status honestly — include quota status if known.
3. **Royalty-free sources:** Note if the user can provide their own track (e.g., from YouTube Audio Library, Jamendo, or other free sources). Offer the `music_library/` drop path.

1. **사용자 음악 라이브러리 (`music_library/`):** 이 폴더가 존재하고 트랙을 포함하는지 확인하십시오. 그렇다면 지속 시간과 함께 사용 가능 트랙을 나열하고 사용자가 하나를 선택하게 하십시오.
2. **음악 생성 API:** 레지스트리를 통해 어떤 음악 도구를 사용할 수 있는지 확인하십시오 (`registry.get_by_capability("music_generation")`). 상태를 솔직하게 보고하십시오 — 알려진 할당량 상태를 포함하십시오.
3. **로열티 프리 소스:** 사용자가 자체 트랙을 제공할 수 있는지 메모하십시오 (예: YouTube Audio Library, Jamendo, 또는 기타 무료 소스). `music_library/` 드롭 경로를 제안하십시오.

**Always present the user with explicit choices:**
- Use a track from their library (which one?)
- Provide a different track (drop it in `music_library/`)
- Generate one via API (if available — name the provider and cost)
- Proceed without music

**[한국어]**

**항상 사용자에게 명시적 선택을 제시하십시오:**
- 라이브러리의 트랙 사용 (어떤 것?)
- 다른 트랙 제공 (`music_library/`에 드롭)
- API를 통해 생성 (사용 가능하면 — 프로바이더와 비용 명시)
- 음악 없이 진행

**If no music source is available:** Tell the user explicitly. Do NOT let this surface as a surprise at the asset stage.

**[한국어]**

**음악 소스를 사용할 수 없으면:** 사용자에게 명시적으로 말하십시오. 자산 단계에서 놀라움으로 표시되지 않게 하지 마십시오.

Record the music decision in the proposal/brief artifact so the asset director knows what to do.

**[한국어]**

자산 감독이 무엇을 해야 할지 알도록 제안/브리프 아티팩트에 음악 결정을 기록하십시오.

---

## Pipeline Asset Expectations (파이프라인 자산 기대)

Each pipeline manifest's `tools_available` field declares what tools a stage can use. Use selectors for multi-provider capabilities — the selector handles routing to whatever is available. Read the pipeline manifest for the authoritative list per stage.

**[한국어]**

각 파이프라인 매니페스트의 `tools_available` 필드는 단계가 사용할 수 있는 도구를 선언합니다. 다중 프로바이더 기능에 선택자를 사용하십시오 — 선택자는 사용 가능한 것에 대한 라우팅을 처리합니다. 단계별 권위 목록은 파이프라인 매니페스트를 읽으십시오.

---

## Stage Agents (단계 에이전트)

Each stage produces one canonical artifact that becomes the contract for the next stage. The stage director skill teaches the agent HOW to produce it.

**[한국어]**

각 단계는 다음 단계의 계약이 되는 하나의 정품 아티팩트를 생성합니다. 단계 감독 스킬은 에이전트에게 **어떻게** 생성하는지 가르칩니다.

| Stage | Director Skill | Canonical output | Core quality bar |
|------|---------------|------------------|------------------|
| `idea` | `*-director.md` | `brief` | Clear hook, target platform, duration, tone, and user intent |
| `script` | `*-director.md` | `script` | Structured sections, valid timing, coherent narration |
| `scene_plan` | `*-director.md` | `scene_plan` | Ordered scenes, timings, asset requirements |
| `assets` | `*-director.md` | `asset_manifest` | Provenance, paths, model/tool metadata, scene linkage |
| `edit` | `*-director.md` | `edit_decisions` | Concrete cuts, overlays, subtitle/music decisions |
| `compose` | `*-director.md` | `render_report` | Output paths, encoding profile, verification notes |

| 단계 | 감독 스킬 | 정품 출력 | 핵심 품질 기준 |
|------|---------------|------------------|------------------|
| `idea` | `*-director.md` | `brief` | 명확한 훅, 타겟 플랫폼, 지속 시간, 톤, 사용자 의도 |
| `script` | `*-director.md` | `script` | 구조화된 섹션, 유효한 타이밍, 응집된 내레이션 |
| `scene_plan` | `*-director.md` | `scene_plan` | 순서화된 장면, 타이밍, 자산 요구사항 |
| `assets` | `*-director.md` | `asset_manifest` | 출처, 경로, 모델/도구 메타데이터, 장면 연결 |
| `edit` | `*-director.md` | `edit_decisions` | 구체적 컷, 오버레이, 자막/음악 결정 |
| `compose` | `*-director.md` | `render_report` | 출력 경로, 인코딩 프로필, 검증 메모 |

Stage contract rules:

**[한국어]**

단계 계약 규칙:

- A completed or awaiting-human checkpoint must include the stage's canonical artifact.
- Canonical artifacts must validate against the JSON schema in `schemas/artifacts/`.
- Non-canonical outputs such as media files belong in stage-specific directories.
- Tools should record seeds/model versions for reproducibility.

- 완료되거나 인간 대기 중인 체크포인트는 단계의 정품 아티팩트를 포함해야 합니다.
- 정품 아티팩트는 `schemas/artifacts/`의 JSON 스키마에 대해 검증해야 합니다.
- 미디어 파일과 같은 비정품 출력은 단계별 디렉토리에 속합니다.
- 도구는 재현성을 위해 시드/모델 버전을 기록해야 합니다.

---

## Reviewer Protocol (검토자 프로토콜)

The reviewer is a meta skill (`skills/meta/reviewer.md`) — advisory, never directly blocks progression.

**[한국어]**

검토자는 메타 스킬(`skills/meta/reviewer.md`)입니다 — 자문적이며, 진행을 직접 차단하지 않습니다.

- Self-review after every stage execution, before checkpointing.
- Load `review_focus` items from the pipeline manifest for the current stage.
- Maximum two review rounds. After that, pass with warnings and move on.
- Findings categorized: critical (must fix), suggestion (should fix), nitpick (nice-to-have).
- Critical findings -> fix and re-review. Suggestions -> note and proceed.
- Check playbook `quality_rules` as constraints, not suggestions.

**[한국어]**

- 모든 단계 실행 후 체크포인트 전에 자체 검토.
- 현재 단계에 대해 파이프라인 매니페스트에서 `review_focus` 항목을 로드.
- 최대 2회 검토 라운드. 그 후 경고와 함께 통과하고 계속 진행.
- 발견 분류: critical (수정 필수), suggestion (수정 권장), nitpick (있으면 좋음).
- 중요 발견 -> 수정 후 재검토. 제안 -> 메모하고 진행.
- 플레이북 `quality_rules`을 제안이 아닌 제약으로 확인.

---

## Human Checkpoint Protocol (인간 체크포인트 프로토콜)

The checkpoint protocol meta skill (`skills/meta/checkpoint-protocol.md`) teaches the agent when to pause:

**[한국어]**

체크포인트 프로토콜 메타 스킬(`skills/meta/checkpoint-protocol.md`)은 에이전트에게 언제 멈추는지 가르칩니다:

- Read `human_approval_default` from the pipeline manifest per stage. **The manifest value is binding** — never re-judge it. `lib/checkpoint.py` enforces this: a gated stage cannot be written `completed` without `human_approved=True`.
- Typical gated stages: `idea`/`proposal`, `script`, `scene_plan`, **`assets`** (review the generated assets scene-by-scene — the Backlot board's filmstrip — before compose locks them in), and `publish` where the pipeline has one. Most pipelines auto-proceed on `edit` and `compose`, but not all (documentary-montage gates `edit`) — the manifest you loaded is the only authority.
- When approval is required: write the checkpoint as `awaiting_human`, present artifact summary, review findings, and cost snapshot — then **END YOUR TURN**. Doing further pipeline work in the same response is a gate violation.
- **Approval is per-gate.** An early "go ahead" never covers later gates; explicit full-run pre-authorization must be recorded as a `decision_log` entry (`category: "approval_policy"`) to count.
- Wait for human to approve, request revision, or abort.

**[한국어]**

- 단계별로 파이프라인 매니페스트에서 `human_approval_default`를 읽으십시오. **매니페스트 값은 구속적입니다** — 재판단하지 마십시오. `lib/checkpoint.py`가 이것을 강제합니다: 게이트된 단계는 `human_approved=True` 없이 `completed`로 쓸 수 없습니다.
- 일반적인 게이트 단계: `idea`/`proposal`, `script`, `scene_plan`, **`assets`** (compose가 잠그기 전 생성된 자산을 장면별로 검토 — Backlot 보드의 필름스트립), 파이프라인에 있는 `publish`. 대부분의 파이프라인은 `edit`와 `compose`에서 자동 진행하지만 모든 것은 아닙니다 (documentary-montage는 `edit`을 게이트) — 로드한 매니페스트가 유일한 권위입니다.
- 승인이 필요할 때: `awaiting_human`으로 체크포인트를 쓰고, 아티팩트 요약, 검토 발견, 비용 스냅샷을 제시하십시오 — 그 후 **턴을 종료하십시오.** 같은 응답에서 추가 파이프라인 작업을 하는 것은 게이트 위반입니다.
- **승인은 게이트별입니다.** 초기의 "진행"은 나중 게이트를 커버하지 않습니다. 명시적 전체 실행 사전 승인은 `decision_log` 항목(`category: "approval_policy"`)으로 기록되어야 효력이 있습니다.
- 인간의 승인, 수정 요청, 중지를 기다리십시오.

---

## Communication Protocol (의사소통 프로토콜)

Agents coordinate through canonical JSON artifacts, checkpoints, pipeline manifests, and the tool registry.

**[한국어]**

에이전트는 정품 JSON 아티팩트, 체크포인트, 파이프라인 매니페스트, 도구 레지스트리를 통해 조정합니다.

Primary files:

**[한국어]**

주요 파일:

- Artifact schemas: `schemas/artifacts/`
- Checkpoint schema: `schemas/checkpoints/checkpoint.schema.json`
- Pipeline manifest schema: `schemas/pipelines/pipeline_manifest.schema.json`
- Pipeline manifests: `pipeline_defs/`
- Style playbooks: `styles/*.yaml` (validated by `schemas/styles/playbook.schema.json`)
- Tool contract: `tools/base_tool.py`
- Tool registry: `tools/tool_registry.py`
- Stage director skills: `skills/pipelines/<pipeline>/<stage>-director.md`
- Meta skills: `skills/meta/*.md`

- 아티팩트 스키마: `schemas/artifacts/`
- 체크포인트 스키마: `schemas/checkpoints/checkpoint.schema.json`
- 파이프라인 매니페스트 스키마: `schemas/pipelines/pipeline_manifest.schema.json`
- 파이프라인 매니페스트: `pipeline_defs/`
- 스타일 플레이북: `styles/*.yaml` (`schemas/styles/playbook.schema.json`로 검증)
- 도구 계약: `tools/base_tool.py`
- 도구 레지스트리: `tools/tool_registry.py`
- 단계 감독 스킬: `skills/pipelines/<pipeline>/<stage>-director.md`
- 메타 스킬: `skills/meta/*.md`

Checkpoint rules:

**[한국어]**

체크포인트 규칙:

- Checkpoints live at `projects/<project_id>/checkpoint_<stage>.json` (the project workspace — this is what the Backlot board watches).
- `status` may be `completed`, `failed`, `awaiting_human`, or `in_progress`.
- Write an `in_progress` checkpoint on entering each stage; during `assets`/`compose`, refresh `metadata.partial_progress` after each completed scene/asset unit — this powers live progress on the board.
- `completed` and `awaiting_human` checkpoints must include the canonical artifact.
- A gated stage (`human_approval_default: true`) can only be written `completed` with `human_approved=True` — the writer raises a GATE VIOLATION otherwise.
- Superseded checkpoints are archived automatically to `projects/<project_id>/history/` — stage re-runs never destroy run history.
- Invalid checkpoints or invalid canonical artifacts are contract violations and should fail fast.

- 체크포인트는 `projects/<project_id>/checkpoint_<stage>.json`에 존재합니다 (프로젝트 워크스페이스 — Backlot 보드가 감시하는 것).
- `status`는 `completed`, `failed`, `awaiting_human`, 또는 `in_progress`일 수 있습니다.
- 각 단계에 진입할 때 `in_progress` 체크포인트를 작성하십시오. `assets`/`compose` 중 완료된 각 장면/자산 단위 후 `metadata.partial_progress`를 새로 고치십시오 — 이것이 보드에서 라이브 진행 상황을 구동합니다.
- `completed` 및 `awaiting_human` 체크포인트는 정품 아티팩트를 포함해야 합니다.
- 게이트된 단계(`human_approval_default: true`)는 `human_approved=True`로만 `completed`를 쓸 수 있습니다 — 그렇지 않으면 작성자가 GATE VIOLATION을 발생시킵니다.
- 대체된 체크포인트는 `projects/<project_id>/history/`로 자동 보관됩니다 — 단계 재실행은 실행 기록을 파괴하지 않습니다.
- 잘못된 체크포인트나 잘못된 정품 아티팩트는 계약 위반이며 빠르게 실패해야 합니다.

Pipeline manifest rules:

**[한국어]**

파이프라인 매니페스트 규칙:

- Pipelines are declarative YAML manifests in `pipeline_defs/`.
- Stages declare: `skill` (director skill path), `produces`, `tools_available`, `review_focus`, `success_criteria`, `human_approval_default`.
- Adding a new pipeline requires a manifest + stage director skills.

- 파이프라인은 `pipeline_defs/`의 선언적 YAML 매니페스트입니다.
- 단계는 다음을 선언합니다: `skill` (감독 스킬 경로), `produces`, `tools_available`, `review_focus`, `success_criteria`, `human_approval_default`.
- 새 파이프라인 추가는 매니페스트 + 단계 감독 스킬을 필요로 합니다.

Tool rules:

**[한국어]**

도구 규칙:

- Every production tool must inherit from `BaseTool`.
- Tool discovery flows through the registry, not ad hoc imports.
- Support-envelope reporting is the source of truth for capability, status, and resource requirements.

- 모든 제작 도구는 `BaseTool`에서 상속해야 합니다.
- 도구 발견은 레지스트리를 통해 흐르며, 임시 가져오기가 아닙니다.
- 지원 범위 보고는 기능, 상태, 리소스 요구사항의 진실의 원천입니다.

---

## Style Playbooks (스타일 플레이북)

| Playbook | Best For |
|----------|----------|
| `clean-professional` | Corporate, educational, SaaS |
| `premium-minimalist` | Investor updates, expert explainers, product narratives |
| `flat-motion-graphics` | Social media, TikTok, startups |
| `minimalist-diagram` | Technical deep-dives, architecture |
| `ink-sketch` (Ink Theater) | Hand-drawn ink-on-white doodle animation; a character that draws itself, walks, dances; contraption explainers |

| 플레이북 | 최적 용도 |
|----------|----------|
| `clean-professional` | 기업, 교육, SaaS |
| `premium-minimalist` | 투자자 업데이트, 전문가 설명 영상, 제품 내러티브 |
| `flat-motion-graphics` | 소셜 미디어, TikTok, 스타트업 |
| `minimalist-diagram` | 기술 심층 분석, 아키텍처 |
| `ink-sketch` (Ink Theater) | 흰 배경에 손으로 그린 잉크 낙서 애니메이션; 스스로 그려지고 걷고 춤추는 캐릭터; 장치 설명 영상 |

For custom, atelier, brand, launch, or hero work, read `skills/meta/taste-direction.md` before choosing a playbook. Carry its `taste_profile` into the proposal so later stages can preserve the design read, visual variance, motion intensity, information density, reference strategy, and anti-patterns.

**[한국어]**

맞춤, 아틀리에, 브랜드, 출시, 주요 작업의 경우, 플레이북을 선택하기 전에 `skills/meta/taste-direction.md`를 읽으십시오. 제안에 `taste_profile`을 전달하여 후속 단계가 디자인 리드, 시각적 분산, 모션 강도, 정보 밀도, 참조 전략, 반패턴을 보존할 수 있도록 하십시오.

### Hand-drawn "doodle" animation → Ink Theater / Ink Puppet (손으로 그린 "doodle" 애니메이션 → Ink Theater / Ink Puppet)

For any brief that wants a **hand-drawn ink doodle** look — "a sketch that comes to life", "a pencil / stick figure that walks or dances", "a little character that acts out the idea", whiteboard-doodle explainers — use the **Ink Theater** engine + **Ink Puppet** mocap system (`skills/creative/ink-theater.md`, `ink-theater/README.md`). It is a **style + reusable engine, not a new pipeline**: illustration / contraption pieces run on the `animation` pipeline; a mocap character (draws itself → walks / dances / waves via `InkPuppet.choreograph([...])`) runs on `character-animation`. Cross-tool entry points: **`/ink-art`** (create a vector doodle from scratch) and **`/animated-drawing`** (animate a *supplied* drawing with mocap — raster; `skills/creative/animated-drawing.md`). Never hand-tune character motion — the agent only chooses named mocap clips.

**[한국어]**

**손으로 그린 잉크 낙서** 룩을 원하는 모든 브리프 — "살아나는 스케치", "걷거나 춤추는 연필/스틱 figure", "아이디어를 연기하는 작은 캐릭터", 화이트보드 낙서 설명 영상 — **Ink Theater** 엔진 + **Ink Puppet** mocap 시스템(`skills/creative/ink-theater.md`, `ink-theater/README.md`)을 사용하십시오. 이것은 **스타일 + 재사용 엔진, 새 파이프라인이 아닙니다**: 일러스트레이션/장치 작품은 `animation` 파이프라인에서 실행; mocap 캐릭터(스스로 그려지고 → `InkPuppet.choreograph([...])`를 통해 걷고/춤추고/파도함)는 `character-animation`에서 실행. 교차 도구 진입점: **`/ink-art`** (처음부터 벡터 낙서 생성) 및 **`/animated-drawing`** (mocap으로 *제공된* 드로잉 애니메이션 — 래스터; `skills/creative/animated-drawing.md`). 캐릭터 모션을 수동으로 조정하지 마십시오 — 에이전트는 명명된 mocap 클립만 선택합니다.

---

## Layer Map (레이어 맵)

OpenMontage has three instruction layers:

**[한국어]**

OpenMontage는 세 개의 명령 레이어를 가지고 있습니다:

1. `tools/`
   What exists, what is available, cost, runtime, fallback, related skills.
2. `skills/`
   How OpenMontage wants those tools used in pipelines.
3. `.agents/skills/`
   Raw vendor or technology knowledge.

1. `tools/`
   무엇이 존재하고, 무엇을 사용할 수 있고, 비용, 런타임, 대체, 관련 스킬.
2. `skills/`
   OpenMontage가 파이프라인에서 그 도구들을 어떻게 사용하기를 원하는지.
3. `.agents/skills/`
   원시 공급업체 또는 기술 지식.

Reading order:

**[한국어]**

읽기 순서:

1. registry / tool contract — discover what's available
2. relevant pipeline or creative skill (Layer 2) — know HOW to use it in this context
3. underlying vendor skill (Layer 3) — **mandatory before calling any generation tool**

1. 레지스트리 / 도구 계약 — 사용 가능한 것 발견
2. 관련 파이프라인 또는 창작 스킬 (레이어 2) — 이 문맥에서 **어떻게** 사용하는지 알기
3. 기본 프로바이더 스킬 (레이어 3) — 모든 생성 도구 호출 전 **의무**

**Prefer skills over source code for tool usage.** Skills exist precisely so you don't need implementation details in the common case. Layer 2 tells you *what* and *when*. Layer 3 tells you *how*. For authoring prompts, choosing parameters, or understanding usage patterns, you should be reading skills — not `.py` files.

**[한국어]**

**도구 사용에 소스 코드보다 스킬을 선호하십시오.** 스킬은 일반적인 경우에 구현 세부 정보가 필요 없도록 존재합니다. 레이어 2는 *무엇*과 *언제*를 알려줍니다. 레이어 3은 *어떻게*를 알려줍니다. 프롬프트 작성, 매개변수 선택, 사용 패턴 이해를 위해 `.py` 파일이 아닌 스킬을 읽어야 합니다.

**Exception: debugging, audits, and verifying the governance contract.** When a skill and a tool disagree, or when something behaves differently than the skill claims, reading the tool source is fair game — that's often the only way to catch a silent-availability bug or a stale doc string. An audit that refuses to look at the implementation will miss exactly the bugs that matter most. If you do read source to debug, consider whether the finding belongs in a skill update afterward so the next agent doesn't need to repeat the dive.

**[한국어]**

**예외: 디버깅, 감사, 거버넌스 계약 검증.** 스킬과 도구가 불일치하거나, 무언가가 스킬이 주장하는 것과 다르게 동작할 때, 도구 소스를 읽는 것은 공정합니다 — 이것은 조용한 사용 가능성 버그나 오래된 문서 문자를 잡는 유일한 방법인 경우가 많습니다. 구현을 보는 것을 거부하는 감사는 가장 중요한 버그를 놓칠 것입니다. 디버깅을 위해 소스를 읽으면, 다음 에이전트가 다시 돌 필요가 없도록 발견이 스킬 업데이트에 속하는지 고려하십시오.

**Layer 3 is not optional.** Every generation tool (video, image, TTS, music) has an `agent_skills` field listing its Layer 3 skills. These skills contain provider-specific prompt engineering, parameter tuning, and quality techniques. Read them before writing prompts. The difference between a generic prompt and a skill-informed prompt is the difference between "usable" and "cinematic."

**[한국어]**

**레이어 3은 선택 사항이 아닙니다.** 모든 생성 도구(동영상, 이미지, TTS, 음악)는 레이어 3 스킬을 나열하는 `agent_skills` 필드를 가지고 있습니다. 이 스킬들은 프로바이더별 프롬프트 엔지니어링, 매개변수 튜닝, 품질 기법을 포함합니다. 프롬프트를 작성하기 전에 읽으십시오. 일반 프롬프트와 스킬 정보 프롬프트의 차이는 "사용 가능"과 "시네마틱"의 차이입니다.

Example: Before calling `kling_video`, read its `agent_skills` → `ai-video-gen` → get Kling-specific prompt structure, camera direction syntax, and quality keywords that the model responds to best.

**[한국어]**

예: `kling_video`를 호출하기 전에 `agent_skills` → `ai-video-gen`을 읽고 → 모델이 가장 잘 반응하는 Kling별 프롬프트 구조, 카메라 방향 문법, 품질 키워드를 얻으십시오.

### Layer 3 skills, by category (카테고리별 레이어 3 스킬)

The `.agents/skills/` directory is large. When you're not coming in through a tool's `agent_skills` pointer, use this table to find the right file by *what you're trying to do*:

**[한국어]**

`.agents/skills/` 디렉토리는 큽니다. 도구의 `agent_skills` 포인터를 통해 들어오지 않을 때, *무엇을 하려는지*로 올바른 파일을 찾기 위해 이 표를 사용하십시오:

| Category | Skills |
|---|---|
| **Composition runtime** | `remotion`, `remotion-best-practices`, `synthetic-screen-recording` (fake terminal/UI demos via Remotion TerminalScene) |
| **Animation knowledge (generic)** | `gsap-core`, `gsap-timeline`, `gsap-plugins` (SplitText / MorphSVG / DrawSVG / MotionPath / Flip / CustomEase), `gsap-utils`, `gsap-react`, `gsap-performance`, `gsap-scrolltrigger`, `gsap-frameworks`, `framer-motion` (Disney 12 principles), `lottie-bodymovin` (Lottie export) |
| **Character animation** | `character-rigging`, `svg-character-animation`, `pose-library-design`, `canvas-procedural-animation`, `character-animation-qa` |
| **Image generation** | `bfl-api`, `flux-best-practices` |
| **Video generation** | `seedance-2-0` (preferred premium default — cinematic, trailer, multi-shot, synced audio, lip-sync), `gemini-omni` (conversational video editing, reference tags, timecoded beats), `ai-video-gen`, `ltx2` |
| **Audio** | `elevenlabs`, `music`, `sound-effects`, `acestep`, `text-to-speech`, `setup-api-key` |
| **Speech-to-text** | `speech-to-text` (whisper `transcriber` — default, offline), `azure-speech-to-text` (optional cloud STT — tool `azure_stt`, preferred when `AZURE_SPEECH_KEY` is set) |
| **Avatar / lip-sync** | `avatar-video`, `heygen`, `create-video`, `faceswap`, `video-translate`, `agents` |
| **Capture** | `playwright-recording` (browser flows), `ffmpeg` (post) |
| **Visualization** | `beautiful-mermaid`, `d3-viz`, `manim-composer`, `manimce-best-practices`, `manimgl-best-practices` |
| **Media editing** | `video-edit`, `video-download`, `video-understand`, `video-toolkit`, `visual-style` |

| 카테고리 | 스킬 |
|---|---|
| **합성 런타임** | `remotion`, `remotion-best-practices`, `synthetic-screen-recording` (Remotion TerminalScene을 통한 가짐 터미널/UI 데모) |
| **애니메이션 지식 (일반)** | `gsap-core`, `gsap-timeline`, `gsap-plugins` (SplitText / MorphSVG / DrawSVG / MotionPath / Flip / CustomEase), `gsap-utils`, `gsap-react`, `gsap-performance`, `gsap-scrolltrigger`, `gsap-frameworks`, `framer-motion` (Disney 12 원칙), `lottie-bodymovin` (Lottie 내보내기) |
| **캐릭터 애니메이션** | `character-rigging`, `svg-character-animation`, `pose-library-design`, `canvas-procedural-animation`, `character-animation-qa` |
| **이미지 생성** | `bfl-api`, `flux-best-practices` |
| **동영상 생성** | `seedance-2-0` (선호하는 프리미엄 기본 — 시네마틱, 트레일러, 멀티 샷, 동기화 오디오, 립싱크), `gemini-omni` (대화형 동영상 편집, 참조 태그, 타임코드 비트), `ai-video-gen`, `ltx2` |
| **오디오** | `elevenlabs`, `music`, `sound-effects`, `acestep`, `text-to-speech`, `setup-api-key` |
| **음성 텍스트 변환** | `speech-to-text` (whisper `transcriber` — 기본, 오프라인), `azure-speech-to-text` (선택적 클라우드 STT — 도구 `azure_stt`, `AZURE_SPEECH_KEY`가 설정될 때 선호) |
| **아바타 / 립싱크** | `avatar-video`, `heygen`, `create-video`, `faceswap`, `video-translate`, `agents` |
| **캡처** | `playwright-recording` (브라우저 플로우), `ffmpeg` (포스트) |
| **시각화** | `beautiful-mermaid`, `d3-viz`, `manim-composer`, `manimce-best-practices`, `manimgl-best-practices` |
| **미디어 편집** | `video-edit`, `video-download`, `video-understand`, `video-toolkit`, `visual-style` |

**When in doubt, read the category's meta routing file first:**
- Picking an animation runtime? → `skills/meta/animation-runtime-selector.md` routes between Remotion primitives, GSAP plugins, framer-motion, Lottie, Manim, D3.
- Picking a screen-recording mode (real capture vs synthetic terminal)? → `pipeline_defs/screen-demo.yaml` + `skills/pipelines/screen-demo/idea-director.md`.

**[한국어]**

**의심스러울 때 먼저 카테고리의 메타 라우팅 파일을 읽으십시오:**
- 애니메이션 런타임 선택? → `skills/meta/animation-runtime-selector.md`가 Remotion 프리미티브, GSAP 플러그인, framer-motion, Lottie, Manim, D3 간을 라우팅합니다.
- 화면 녹화 모드 선택 (실제 캡처 vs 합성 터미널)? → `pipeline_defs/screen-demo.yaml` + `skills/pipelines/screen-demo/idea-director.md`.

---

## Quick Lookup (빠른 조회)

| Question | Where to look |
|----------|---------------|
| What tools exist? | `tools/tool_registry.py` and `registry.support_envelope()` |
| What providers are available for a capability? | `registry.capability_catalog()` |
| What tools exist for a vendor? | `registry.provider_catalog()` |
| How does a tool actually work? | the tool's `usage_location` from the registry |
| How should this pipeline stage behave? | `skills/pipelines/<pipeline>/...` |
| What is the checkpoint/review policy? | `skills/meta/` |

| 질문 | 찾을 곳 |
|----------|---------------|
| 어떤 도구가 있는가? | `tools/tool_registry.py` 및 `registry.support_envelope()` |
| 기능에 대해 어떤 프로바이더를 사용할 수 있는가? | `registry.capability_catalog()` |
| 공급업체에 어떤 도구가 있는가? | `registry.provider_catalog()` |
| 도구가 실제로 어떻게 작동하는가? | 레지스트리의 도구 `usage_location` |
| 이 파이프라인 단계는 어떻게 작동해야 하는가? | `skills/pipelines/<pipeline>/...` |
| 체크포인트/검토 정책은 무엇인가? | `skills/meta/` |

---

## What Not To Do (하지 말아야 할 것)

- **Do not bypass the pipeline.** Never write ad-hoc scripts to call tools directly. All production goes through pipeline stages with director skills. See Rule Zero.
- **Do not call generation tools without reading their Layer 3 skill.** Check the tool's `agent_skills` field, read the referenced skill, then craft your prompts using that guidance.
- **Do not skip stage director skills.** Before executing any pipeline stage, read its director skill. The skill contains the quality bar, the workflow, and the review criteria.
- Do not use deleted legacy names such as `tts_cloud`, `tts_engine`, or `video_gen`.
- Do not hardcode provider names, API key names, or setup URLs. Read them from the registry's `install_instructions` and `dependencies` fields.
- Do not begin asset generation before user approval on the production plan.
- Do not hide degraded paths. Record substitutions and blocked options explicitly.
- Do not present a single unavailable tool in isolation. Always show the full capability picture: "X of Y providers configured for this capability."
- Do not skip the Provider Menu at preflight. The user must see what they have AND what they could unlock.
- Do not change provider, model, or render path without telling the user first and getting approval when the change is material.

**[한국어]**

- **파이프라인을 우회하지 마십시오.** 도구를 직접 호출하는 임시 스크립트를 절대 작성하지 마십시오. 모든 제작은 감독 스킬이 있는 파이프라인 단계를 통해 이루어집니다. 룰 제로를 참조하십시오.
- **레이어 3 스킬을 읽지 않고 생성 도구를 호출하지 마십시오.** 도구의 `agent_skills` 필드를 확인하고, 참조된 스킬을 읽은 다음 해당 안내를 사용하여 프롬프트를 작성하십시오.
- **단계 감독 스킬을 건너뛰지 마십시오.** 모든 파이프라인 단계를 실행하기 전에 감독 스킬을 읽으십시오. 스킬은 품질 기준, 워크플로우, 검토 기준을 포함합니다.
- `tts_cloud`, `tts_engine`, 또는 `video_gen`과 같은 삭제된 레거시 이름을 사용하지 마십시오.
- 프로바이더 이름, API 키 이름, 설정 URL을 하드코딩하지 마십시오. 레지스트리의 `install_instructions` 및 `dependencies` 필드에서 읽으십시오.
- 제작 계획에 대한 사용자 승인 전에 자산 생성을 시작하지 마십시오.
- 저하된 경로를 숨기지 마십시오. 대체 및 차단된 옵션을 명시적으로 기록하십시오.
- 단일 사용 불가능 도구를 격리된 상태로 제시하지 마십시오. 항상 전체 기능 그림을 표시하십시오: "이 기능에 대해 Y개 중 X개 프로바이더 구성됨."
- 사전 점검에서 프로바이더 메뉴를 건너뛰지 마십시오. 사용자는 가진 것과 해제할 수 있는 것을 모두 보아야 합니다.
- 변경이 중요할 때 사용자에게 먼저 알리고 승인을 받지 않고 프로바이더, 모델, 또는 렌더링 경로를 변경하지 마십시오.