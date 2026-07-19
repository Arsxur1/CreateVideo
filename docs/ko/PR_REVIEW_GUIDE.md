> 이 문서는 이중 언어 문서입니다. 각 섹션에서 영어 원문이 먼저 나오고, **[한국어]** 표시 아래에 한국어 번역이 이어집니다.

> 원본: docs/PR_REVIEW_GUIDE.md @ 7ee36dd6b66c7dc0712da194786b77da1c2e7ed3

# Pull Request Review Guide (풀 리뷰 가이드)

This guide is for community reviewers, maintainers, and AI assistants reviewing
OpenMontage pull requests. It is a review framework, not a closed checklist.
Use it to structure the review, then keep looking for issues that are specific
to the PR in front of you.

OpenMontage is an agent-orchestrated video production system. Many PRs affect
more than the file they edit: a provider change can affect tool discovery,
selector routing, setup instructions, pipeline decisions, cost reporting, and
the user-visible production flow. Good reviews protect those contracts.

**[한국어]**

이 가이드는 OpenMontage 풀 리뷰를 하는 커뮤니티 리뷰어, 메인테이너, AI 어시스턴트를 위한 문서입니다. 리뷰 프레임워크이지, 단순 체크리스트가 아닙니다. 이 가이드를 사용해 리뷰를 구조화한 후에도, 앞에 있는 PR의 특정 문제를 계속 찾아야 합니다.

OpenMontage는 에이전트가 오케스트라하는 영상 제작 시스템입니다. 많은 PR이 수정하는 파일 이상에 영향을 미칩니다: 프로바이더 변경은 도구 발견, 셀렉터 라우팅, 설정 안내, 파이프라인 결정, 비용 보고, 사용자에게 보이는 제작 흐름에 모두 영향을 줄 수 있습니다. 좋은 리뷰는 이런 계약을 보호합니다.

---

## Review Mindset (리뷰 마인드셋)

Start with these questions:

- Does this PR move OpenMontage in the right direction?
- Is the scope focused, or is it mixing unrelated changes?
- Can a user, maintainer, or agent understand the behavior after this lands?
- Does the PR preserve the agent-first architecture?
- Does it introduce regressions in provider discovery, pipeline artifacts, or
  rendering behavior?
- Are tests and docs updated at the same level as the behavior change?
- Are there security, privacy, dependency, or supply-chain concerns?

The answer can be "useful, but not merge-ready." That is a good review outcome
when the idea is aligned but the implementation needs cleanup.

**[한국어]**

다음 질문으로 시작합니다.

- 이 PR이 OpenMontage를 올바른 방향으로 이동시키나요?
- 범위가 집중되어 있나요, 아니면 관련 없는 변경이 섞여 있나요?
- 이것이 적용된 후 사용자, 메인테이너, 에이전트가 동작을 이해할 수 있나요?
- 이 PR이 에이전트 우선 아키텍처를 유지하나요?
- 프로바이더 발견, 파이프라인 아티팩트, 렌더링 동작에 회귀를 도입하나요?
- 테스트와 문서가 동작 변경과 동일한 수준으로 업데이트되었나요?
- 보안, 프라이버시, 의존성, 공급망에 관심사가 있나요?

답은 "유용하지만 병합 준비가 아님"이 될 수 있습니다. 아이디어는 맞지만 구현이 정리가 필요할 때 좋은 리뷰 결과입니다.

---

## Review Outputs (리뷰 결과)

A useful review should usually produce one of these outcomes:

- **Approve**: the PR is useful, focused, tested, and low-risk enough to merge.
- **Comment**: the PR is promising but needs cleanup before approval.
- **Request changes**: the PR has blockers that would create regressions,
  break contracts, or mislead users.
- **Close or redirect**: the PR is not aligned, mostly noise, or belongs in an
  issue/discussion before code.

Avoid rubber-stamp approvals. Also avoid turning every concern into a blocker.
Name the actual severity and explain the impact.

**[한국어]**

유용한 리뷰는 일반적으로 다음 결과 중 하나를 생성해야 합니다.

- **승인**: PR은 유용하고, 집중되어 있고, 테스트되었고, 병합하기에 충분히 낮은 위험입니다.
- **코멘트**: PR은 유망하지만 승인 전에 정리가 필요합니다.
- **변경 요청**: PR에 회귀를 만들거나, 계약을 깨거나, 사용자를 오도할 차단 문제가 있습니다.
- **닫기 또는 리다이렉트**: PR이 정렬되지 않았거나, 대부분 노이즈이거나, 코드보다 이슈/토론에 속합니다.

고무도장 승인은 피하십시오. 또한 모든 우려를 차단 문제로 만드는 것도 피하십시오. 실제 심각도를 명명하고 영향을 설명하십시오.

---

## General Review Areas (일반 리뷰 영역)

### Project Direction (프로젝트 방향)

Check whether the PR solves a real OpenMontage problem.

- Does it improve video production quality, reliability, speed, portability,
  provider coverage, local execution, docs, tests, or contributor experience?
- Does it duplicate an existing path without improving it?
- Is it a speculative feature with no clear user workflow?
- Does it introduce maintenance burden disproportionate to the value?

**[한국어]**

PR이 실제 OpenMontage 문제를 해결하는지 확인하십시오.

- 영상 제작 품질, 신뢰성, 속도, 이식성, 프로바이더 커버리지, 로컬 실행, 문서, 테스트, 기여자 경험을 향상시키나요?
- 기존 경로를 개선 없이 복제하나요?
- 명확한 사용자 워크플로우가 없는 추측적 기능인가요?
- 가치에 비례하지 않는 유지 관리 부담을 도입하나요?

---

### Scope Hygiene (범위 위생)

Noise makes reviews unsafe.

- Are unrelated files changed?
- Are lockfiles changed only when dependencies actually changed?
- Are generated files, screenshots, binary assets, or local artifacts included
  without reason?
- Are docs/test fixes bundled with feature work in a way that hides risk?
- Is the branch stale against latest `main`?

If a PR is useful but noisy, ask for a narrower diff before deep approval.

**[한국어]**

노이즈는 리뷰를 안전하지 않게 만듭니다.

- 관련 없는 파일이 변경되었나요?
- 의존성이 실제로 변경된 경우에만 lockfile이 변경되었나요?
- 생성된 파일, 스크린샷, 바이너리 자산, 로컬 아티팩트가 이유 없이 포함되었나요?
- 문서/테스트 수정이 기능 작업과 함께 묶여 위험을 숨기고 있나요?
- 최신 `main`에 대해 브랜치가 오래되었나요?

PR이 유용하지만 노이즈가 많으면 깊은 승인 전에 더 좁은 diff를 요청하십시오.

---

### Regression Risk (회귀 위험)

Look beyond the changed file.

- Does the change affect existing users or only add a new optional path?
- Does it alter default provider selection, fallback behavior, or setup menus?
- Does it change schemas, artifacts, or pipeline stage contracts?
- Does it change rendering output, timing, audio, captions, or file paths?
- Does it create silent fallback behavior where the user should be told?

**[한국어]**

변경된 파일 이상을 보십시오.

- 이 변경이 기존 사용자에게 영향을 주나요, 아니면 새로운 선택적 경로만 추가하나요?
- 기본 프로바이더 선택, 대체 동작, 설정 메뉴를 변경하나요?
- 스키마, 아티팩트, 파이프라인 단계 계약을 변경하나요?
- 렌더링 출력, 타이밍, 오디오, 캡션, 파일 경로를 변경하나요?
- 사용자에게 알려야 할 침묵 대체 동작을 만들나요?

---

### Security and Supply Chain (보안 및 공급망)

Review security issues factually and with evidence. Do not make public claims
about a contributor's intent. If you see suspicious code, describe the behavior
and risk.

Check for:

- New network calls, uploads, telemetry, or background processes
- Secret exfiltration risks, `.env` reads, token logging, or unsafe debug output
- Shell execution, `subprocess`, dynamic imports, `eval`, `exec`, or generated
  code execution
- Dependency additions, install scripts, package-lock churn, or broad version
  ranges
- Unsafe file deletion, path traversal, archive extraction, or writes outside
  the expected project directory
- Remote model downloads or provider calls that are not surfaced in metadata
- Prompt injection surfaces where external content could instruct the agent

Use language like:

- "I found a security blocker: this command executes user-controlled input."
- "This dependency change needs justification before merge."
- "I did not find an actionable security issue in the reviewed diff."

Avoid public phrasing like:

- "No malicious intent."
- "This author is safe."
- "This is definitely harmless."

**[한국어]**

증거와 함께 사실적으로 보안 문제를 검토하십시오. 기여자의 의도에 대해 공개 주장하지 마십시오. 의심스러운 코드를 보면 동작과 위험을 설명하십시오.

다음을 확인하십시오.

- 새로운 네트워크 호출, 업로드, 원격측정, 백그라운드 프로세스
- 시크릿 유출 위험, `.env` 읽기, 토큰 로깅, 안전하지 않은 디버그 출력
- 셸 실행, `subprocess`, 동적 가져오기, `eval`, `exec`, 생성된 코드 실행
- 의존성 추가, 설치 스크립트, 패키지-lock 변경, 넓은 버전 범위
- 안전하지 않은 파일 삭제, 경로 순회, 아카이브 추출, 예상 프로젝트 디렉토리 외부 쓰기
- 메타데이터에 표시되지 않은 원격 모델 다운로드 또는 프로바이더 호출
- 외부 콘텐츠가 에이전트에 지시할 수 있는 프롬프트 인젝션 표면

다음과 같은 언어를 사용하십시오.

- "보안 차단 문제를 발견했습니다: 이 명령은 사용자 제어 입력을 실행합니다."
- "이 의존성 변경은 병합 전에 정당성이 필요합니다."
- "검토한 diff에서 실행 가능한 보안 문제를 찾지 못했습니다."

다음과 같은 공개 표현은 피하십시오.

- "악의적인 의도 없음."
- "이 작성자는 안전함."
- "이것은 확실히 무해함."

---

### Performance and Resource Use (성능 및 리소스 사용)

OpenMontage works with video, audio, image generation, and local models. Small
code changes can create large runtime costs.

- Does the PR add repeated model loads instead of reusing state?
- Does it download large files without clear setup/status messaging?
- Does it increase render time, memory, VRAM, disk, or network use?
- Does it change frame extraction, composition, encoding, or audio processing
  in a way that could slow common paths?
- Are resource profiles and cost estimates realistic?

**[한국어]**

OpenMontage는 영상, 오디오, 이미지 생성, 로컬 모델로 작업합니다. 작은 코드 변경도 큰 런타임 비용을 만들 수 있습니다.

- PR이 상태를 재사용하는 대신 반복적인 모델 로드를 추가하나요?
- 명확한 설정/상태 메시지 없이 큰 파일을 다운로드하나요?
- 렌더링 시간, 메모리, VRAM, 디스크, 네트워크 사용을 증가시키나요?
- 일반적인 경로를 늦출 수 있는 방식으로 프레임 추출, 합성, 인코딩, 오디오 처리를 변경하나요?
- 리소스 프로필과 비용 추정이 현실적이나요?

---

## OpenMontage Architecture Checks (OpenMontage 아키텍처 검사)

### Agent-First Architecture (에이전트 우선 아키텍처)

OpenMontage's control plane is the agent following markdown skills and YAML
manifests. Python should provide tools and persistence, not hidden orchestration.

Flag PRs that:

- Add Python orchestrators for creative decisions, stage transitions, or review
  policy
- Hide provider/model/runtime decisions inside code without user visibility
- Bypass pipeline manifests, stage director skills, checkpoints, or review
- Move quality policy into ad hoc code instead of documented instructions

Good PRs keep intelligence in instructions and contracts, with Python handling
well-bounded execution.

**[한국어]**

OpenMontage의 제어 평면은 마크다운 스킬과 YAML 매니페스트를 따르는 에이전트입니다. Python은 도구와 지속성을 제공해야 하지, 숨겨진 오케스트레이션을 제공하면 안 됩니다.

다음 PR을 표시하십시오.

- 창의적 결정, 단계 전환, 리뷰 정책을 위한 Python 오케스트레이터 추가
- 사용자 표시 없이 프로바이더/모델/런타임 결정을 코드 안에 숨김
- 파이프라인 매니페스트, 단계 감독 스킬, 체크포인트, 리뷰 우회
- 문서화된 지시 대신 임시 코드로 품질 정책 이동

좋은 PR은 지시와 계약에 지능을 유지하고, Python은 잘 경계된 실행을 처리합니다.

---

### Tool Contract (도구 계약)

Every tool should inherit from `tools/base_tool.py` and satisfy the `BaseTool`
contract.

For new or changed tools, review:

- `name`, `version`, `tier`, `capability`, `provider`
- `runtime`, `stability`, `execution_mode`, `determinism`
- `dependencies` using supported prefixes such as `cmd:`, `env:`, `python:`
- `install_instructions`
- `input_schema`, `output_schema`, and artifact behavior
- `supports`, `best_for`, `not_good_for`
- `resource_profile`
- `retry_policy`
- `fallback` and `fallback_tools`
- `agent_skills`
- `user_visible_verification`
- `estimate_cost()` and `estimate_runtime()` where relevant
- `execute()` returning a `ToolResult`

Metadata is user-facing. If setup, offline behavior, cost, model downloads, or
hardware requirements are inaccurate, the provider menu and agent planning will
mislead users.

**[한국어]**

모든 도구는 `tools/base_tool.py`에서 상속받고 `BaseTool` 계약을 만족해야 합니다.

새로운 도구나 변경된 도구의 경우 다음을 검토하십시오.

- `name`, `version`, `tier`, `capability`, `provider`
- `runtime`, `stability`, `execution_mode`, `determinism`
- `cmd:`, `env:`, `python:` 같은 지원되는 접두사를 사용하는 `dependencies`
- `install_instructions`
- `input_schema`, `output_schema`, 아티팩트 동작
- `supports`, `best_for`, `not_good_for`
- `resource_profile`
- `retry_policy`
- `fallback` 및 `fallback_tools`
- `agent_skills`
- `user_visible_verification`
- 관련한 경우 `estimate_cost()` 및 `estimate_runtime()`
- `ToolResult`를 반환하는 `execute()`

메타데이터는 사용자 대면입니다. 설정, 오프라인 동작, 비용, 모델 다운로드, 하드웨어 요구사항이 부정확하면 프로바이더 메뉴와 에이전트 계획이 사용자를 오도합니다.

---

### Tool Registry and Discovery (도구 레지스트리 및 발견)

Tool discovery flows through `tools/tool_registry.py`. Avoid hardcoded tool
lists unless there is a strong reason.

Check:

- Does the tool register through normal package discovery?
- Does it use the right `capability` so selectors can find it?
- Does `get_status()` report availability accurately?
- Does an import failure in one optional provider break unrelated discovery?
- Does the provider menu show useful setup instructions?
- Does the PR accidentally make unavailable tools look configured?

Useful commands:

```bash
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.capability_catalog(), indent=2))"
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu_summary(), indent=2))"
```

**[한국어]**

도구 발견은 `tools/tool_registry.py`를 통해 흐릅니다. 강한 이유가 없으면 하드코딩된 도구 목록을 피하십시오.

다음을 확인하십시오.

- 도구가 일반적인 패키지 발견을 통해 등록되나요?
- 셀렉터가 찾을 수 있도록 올바른 `capability`를 사용하나요?
- `get_status()`가 가용성을 정확하게 보고하나요?
- 하나의 선택적 프로바이더에서 가져오기 실패가 관련 없는 발견을 깨나요?
- 프로바이더 메뉴가 유용한 설정 안내를 보여주나요?
- PR이 실수로 사용할 수 없는 도구를 구성된 것처럼 보이게 하나요?

유용한 명령은 위의 코드 블록을 참조하십시오.

---

### Selectors and Providers (셀렉터 및 프로바이더)

Selectors route capability-level requests to provider tools:

- `tts_selector`
- `image_selector`
- `video_selector`

When reviewing selector or provider changes:

- Confirm the provider has the correct `capability`.
- Confirm selector input names map to provider input names.
- Confirm provider-specific options do not get silently ignored.
- Confirm user preference is respected when explicit.
- Confirm unavailable providers do not block available alternatives.
- Confirm ranking/fallback changes are tested.
- Confirm the selector still returns useful alternatives and reasoning.

Adding a provider should usually not require selector code changes. If it does,
the PR should explain why.

**[한국어]**

셀렉터는 기능 수준 요청을 프로바이더 도구로 라우팅합니다.

- `tts_selector`
- `image_selector`
- `video_selector`

셀렉터나 프로바이더 변경을 검토할 때 다음을 확인하십시오.

- 프로바이더가 올바른 `capability`를 가지고 있는지 확인하십시오.
- 셀렉터 입력 이름이 프로바이더 입력 이름에 매핑되는지 확인하십시오.
- 프로바이더별 옵션이 조용히 무시되지 않는지 확인하십시오.
- 명시적일 때 사용자 선호가 존중되는지 확인하십시오.
- 사용할 수 없는 프로바이더가 사용 가능한 대안을 차단하지 않는지 확인하십시오.
- 순위/대체 변경이 테스트되었는지 확인하십시오.
- 셀렉터가 여전히 유용한 대안과 추론을 반환하는지 확인하십시오.

프로바이더를 추가하는 것은 일반적으로 셀렉터 코드 변경을 필요로 하지 않습니다. 필요하면 PR이 이유를 설명해야 합니다.

---

### Pipeline Manifests and Stage Skills (파이프라인 매니페스트 및 단계 스킬)

Pipeline manifests live in `pipeline_defs/`. Stage instructions live in
`skills/pipelines/`.

For pipeline changes, check:

- Manifest schema validity
- Stage order and stage names
- `produces` artifacts
- `tools_available`
- `review_focus`
- `success_criteria`
- `checkpoint_required`
- `human_approval_default`
- Matching stage director skills
- Tests in `tests/contracts/` or `tests/pipelines/`

The manifest and the stage skill must agree. If the manifest says a stage
produces `scene_plan`, the director skill should actually guide creation of a
valid `scene_plan`.

**[한국어]**

파이프라인 매니페스트는 `pipeline_defs/`에 있습니다. 단계 지시는 `skills/pipelines/`에 있습니다.

파이프라인 변경의 경우 다음을 확인하십시오.

- 매니페스트 스키마 유효성
- 단계 순서 및 단계 이름
- `produces` 아티팩트
- `tools_available`
- `review_focus`
- `success_criteria`
- `checkpoint_required`
- `human_approval_default`
- 일치하는 단계 감독 스킬
- `tests/contracts/` 또는 `tests/pipelines/`의 테스트

매니페스트와 단계 스킬은 일치해야 합니다. 매니페스트가 단계가 `scene_plan`을 생성한다고 하면, 감독 스킬은 실제로 유효한 `scene_plan` 생성을 안내해야 합니다.

---

### Canonical Artifacts and Schemas (정식 아티팩트 및 스키마)

Artifacts in `schemas/artifacts/` are contracts between stages.

When reviewing schema or artifact changes:

- Does every producer still write valid artifacts?
- Does every consumer still understand the artifact?
- Are required fields justified?
- Are migrations or backward compatibility needed?
- Do tests cover valid and invalid examples?
- Does the checkpoint protocol still work with the changed artifact?

Schema changes are high-impact. Treat them as cross-pipeline changes unless the
PR proves otherwise.

**[한국어]**

`schemas/artifacts/`의 아티팩트는 단계 간의 계약입니다.

스키마나 아티팩트 변경을 검토할 때 다음을 확인하십시오.

- 모든 프로듀서가 여전히 유효한 아티팩트를 쓰나요?
- 모든 소비자가 여전히 아티팩트를 이해하나요?
- 필수 필드가 정당화되었나요?
- 마이그레이션 또는 하위 호환성이 필요한가요?
- 테스트가 유효하고 무효한 예제를 포함하나요?
- 체크포인트 프로토콜이 변경된 아티팩트로 여전히 작동하나요?

스키마 변경은 영향이 큽니다. PR이 그렇지 않음을 증명하지 않는 한 교차 파이프라인 변경으로 처리하십시오.

---

### Checkpoints and Review Policy (체크포인트 및 리뷰 정책)

OpenMontage uses checkpoints for resume, human approval, audit trails, and
stage gating.

Check:

- Does the PR preserve checkpoint status semantics?
- Does it avoid skipping required human approval?
- Does it preserve cost snapshots and review metadata where expected?
- Does it avoid writing incomplete canonical artifacts as completed stages?
- Does it align with `skills/meta/checkpoint-protocol.md`?
- Does it align with `skills/meta/reviewer.md`?

Review logic should remain instruction-driven unless the PR is adding a narrow
mechanical validator.

**[한국어]**

OpenMontage는 재개, 인간 승인, 감사 추적, 단계 게이트를 위해 체크포인트를 사용합니다.

다음을 확인하십시오.

- PR이 체크포인트 상태 의미를 보존하나요?
- 필수 인간 승인을 건너뛰는 것을 피하나요?
- 예상되는 곳에 비용 스냅샷과 리뷰 메타데이터를 보존하나요?
- 불완전한 정식 아티팩트를 완료된 단계로 쓰는 것을 피하나요?
- `skills/meta/checkpoint-protocol.md`와 정렬되나요?
- `skills/meta/reviewer.md`와 정렬되나요?

리뷰 로직은 지시에 따라야 합니다. PR이 좁은 기계적 검증기를 추가하는 경우를 제외하고.

---

### Composition Runtimes (합성 런타임)

OpenMontage can compose with Remotion, HyperFrames, or FFmpeg. Runtime choices
are user-visible production decisions.

For render/composition PRs, check:

- Does `video_compose` preserve explicit `render_runtime` routing?
- Are Remotion, HyperFrames, and FFmpeg paths considered where relevant?
- Does the PR avoid silent runtime swaps?
- Are runtime availability errors surfaced as blockers?
- Are Node, FFmpeg, `npx`, and package requirements checked accurately?
- Do render reports contain enough evidence to debug failures?
- Are browser previews treated as QA/debug artifacts when the production render
  path is different?

Silent downgrades from motion-led production to still-led fallback are review
findings, not harmless implementation details.

**[한국어]**

OpenMontage는 Remotion, HyperFrames, FFmpeg로 합성할 수 있습니다. 런타임 선택은 사용자에게 보이는 제작 결정입니다.

렌더/합성 PR의 경우 다음을 확인하십시오.

- `video_compose`가 명시적 `render_runtime` 라우팅을 보존하나요?
- 관련 있는 곳에서 Remotion, HyperFrames, FFmpeg 경로가 고려되나요?
- PR이 침묵 런타임 스왑을 피하나요?
- 런타임 가용성 오류가 차단 문제로 표시되나요?
- Node, FFmpeg, `npx`, 패키지 요구사항이 정확하게 검사되나요?
- 렌더 보고서에 실패를 디버그할 충분한 증거가 포함되어 있나요?
- 프로덕션 렌더 경로가 다를 때 브라우저 미리보기가 QA/디버그 아티팩트로 처리되나요?

모션 주도 제작에서 정지 주도 대체로의 침묵 다운그레이드는 리뷰 결과이지 무해한 구현 세부사항이 아닙니다.

---

### Cost, Budget, and Paid Providers (비용, 예산, 유료 프로바이더)

OpenMontage should not silently spend money or imply a paid provider is free.

Check:

- Does the tool estimate cost accurately enough for planning?
- Are first-time paid provider uses visible to the user?
- Does the provider doc mention pricing/free-tier caveats?
- Does fallback from paid to free, or free to paid, require user visibility?
- Are model downloads, hosted endpoints, or cloud GPU usage described honestly?

**[한국어]**

OpenMontage는 돈을 침묵하게 지출하거나 유료 프로바이더가 무료라고 암시해서는 안 됩니다.

다음을 확인하십시오.

- 도구가 계획을 위해 충분히 정확하게 비용을 추정하나요?
- 처음 유료 프로바이더 사용이 사용자에게 보이나요?
- 프로바이더 문서가 가격/무료 등급 주의를 언급하나요?
- 유료에서 무료로, 무료에서 유료로의 대체가 사용자 표시를 요구하나요?
- 모델 다운로드, 호스트된 엔드포인트, 클라우드 GPU 사용이 정직하게 설명되었나요?

---

### Docs and User-Facing Claims (문서 및 사용자 대면 주장)

Docs are part of the product. Provider setup docs often drive agent behavior.

Check:

- Does the PR update `docs/PROVIDERS.md` when adding a provider?
- Does `docs/ARCHITECTURE.md` need an update for architectural changes?
- Are setup instructions accurate on macOS, Windows, and Linux where claimed?
- Do docs distinguish API keys, local installs, model downloads, and cached
  offline operation?
- Are package versions and model versions clearly separated?
- Are limitations stated plainly?

**[한국어]**

문서는 제품의 일부입니다. 프로바이더 설정 문서는 종종 에이전트 동작을 주도합니다.

다음을 확인하십시오.

- 프로바이더를 추가할 때 PR이 `docs/PROVIDERS.md`를 업데이트하나요?
- 아키텍처 변경에 대해 `docs/ARCHITECTURE.md` 업데이트가 필요한가요?
- 설정 안내가 주장한 macOS, Windows, Linux에서 정확한가요?
- 문서가 API 키, 로컬 설치, 모델 다운로드, 캐시된 오프라인 작업을 구별하나요?
- 패키지 버전과 모델 버전이 명확하게 분리되어 있나요?
- 제한 사항이 명확하게 설명되어 있나요?

---

## Scenario-Specific Review Prompts (시나리오별 리뷰 프롬프트)

### New Provider or Tool (새 프로바이더 또는 도구)

Ask:

- Is this provider useful for OpenMontage workflows?
- Does it add real coverage or just duplicate an existing provider?
- Is the provider internationally known, nationally or regionally important,
  or otherwise clearly valuable to OpenMontage users?
- Is the tool discoverable through the registry?
- Does the matching selector discover and route to it?
- Are provider inputs compatible with selector inputs?
- Does status checking reflect real availability?
- Are setup docs, dependencies, cost, network, and cache behavior accurate?
- Does it have focused tests?
- Does it avoid importing heavyweight dependencies at module import time?
- Are generated artifacts written to expected paths?

Minimum expected coverage:

- Tool metadata/contract test
- Registry discovery test
- Status behavior test with dependencies mocked when needed
- Selector/routing test if it joins a selector-backed capability
- Docs update for user-visible providers

Provider viability matters. OpenMontage should not become a grab bag of
unmaintained or one-off integrations. A provider does not need to be globally
dominant, but it should have a clear reason to belong here.

Consider:

- Is there evidence of an active user base, maintained API docs, SDK support,
  or community adoption?
- Is it widely used internationally, or meaningfully popular in a specific
  national, regional, language, or industry market?
- Does it unlock a capability, language, price point, region, quality tier,
  compliance posture, or local/offline workflow that existing providers do not
  cover well?
- Are pricing, quotas, API access, model availability, and terms clear enough
  for contributors to test and maintain the integration?
- Is the provider likely to remain usable over the next six months?
- Does the provider's value justify the maintenance burden it adds?

**[한국어]**

다음을 질문하십시오.

- 이 프로바이더가 OpenMontage 워크플로우에 유용한가요?
- 실제 커버리지를 추가하나요, 아니면 기존 프로바이더를 단순히 복제하나요?
- 프로바이더가 국제적으로 알려져 있거나, 국가/지역적으로 중요하거나, OpenMontage 사용자에게 명백하게 가치가 있나요?
- 도구가 레지스트리를 통해 발견 가능한가요?
- 일치하는 셀렉터가 이를 발견하고 라우팅하나요?
- 프로바이더 입력이 셀렉터 입력과 호환되나요?
- 상태 확인이 실제 가용성을 반영하나요?
- 설정 문서, 의존성, 비용, 네트워크, 캐시 동작이 정확한가요?
- 집중된 테스트가 있나요?
- 모듈 가져오기 시점에 무거운 의존성 가져오기를 피하나요?
- 생성된 아티팩트가 예상 경로에 쓰이나요?

최소 예상 커버리지:

- 도구 메타데이터/계약 테스트
- 레지스트리 발견 테스트
- 필요할 때 의존성이 모의된 상태 동작 테스트
- 셀렉터 지원 기능에 참여하는 경우 셀렉터/라우팅 테스트
- 사용자에게 보이는 프로바이더를 위한 문서 업데이트

프로바이더 실행 가능성이 중요합니다. OpenMontage는 유지 관리되지 않거나 일회성 통합의 집합이 되어서는 안 됩니다. 프로바이더가 전 세계적으로 지배적일 필요는 없지만, 여기에 속할 명확한 이유는 있어야 합니다.

다음을 고려하십시오.

- 활성 사용자 기반, 유지 관리되는 API 문서, SDK 지원, 커뮤니티 채택의 증거가 있나요?
- 국제적으로 널리 사용되거나, 특정 국가, 지역, 언어, 산업 시장에서 의미 있게 인기가 있나요?
- 기존 프로바이더가 잘 커버하지 않는 기능, 언어, 가격대, 지역, 품질 등급, 준수 태세, 로컬/오프라인 워크플로우를 잠금 해제하나요?
- 기여자가 통합을 테스트하고 유지하기에 가격, 할당량, API 액세스, 모델 가용성, 약관이 충분히 명확한가요?
- 프로바이더가 다음 6개월 동안 사용 가능한 상태로 유지될 가능성이 있나요?
- 프로바이더의 가치가 추가하는 유지 관리 부담을 정당화하나요?

---

### Selector Change (셀렉터 변경)

Ask:

- Does it still auto-discover providers?
- Does it avoid hardcoded provider lists?
- Does it preserve explicit user preference?
- Does it handle unavailable providers cleanly?
- Does it explain the selected provider?
- Does it preserve alternatives considered?
- Does it map shared inputs to provider-specific inputs?

**[한국어]**

다음을 질문하십시오.

- 여전히 프로바이더를 자동 발견하나요?
- 하드코딩된 프로바이더 목록을 피하나요?
- 명시적 사용자 선호를 보존하나요?
- 사용할 수 없는 프로바이더를 깔끔하게 처리하나요?
- 선택된 프로바이더를 설명하나요?
- 고려된 대안을 보존하나요?
- 공유 입력을 프로바이더별 입력에 매핑하나요?

---

### Local GPU or Model Runtime Change (로컬 GPU 또는 모델 런타임 변경)

Ask:

- Is the hardware requirement accurate?
- Does CPU/MPS/CUDA behavior match the implementation?
- Are dtype choices safe for each device?
- Are model downloads and cache behavior documented?
- Does the resource profile reflect realistic RAM, VRAM, and disk needs?
- Does setup avoid pretending local GPU install is a one-minute API-key fix?

**[한국어]**

다음을 질문하십시오.

- 하드웨어 요구사항이 정확한가요?
- CPU/MPS/CUDA 동작이 구현과 일치하나요?
- 각 장치에 dtype 선택이 안전한가요?
- 모델 다운로드 및 캐시 동작이 문서화되었나요?
- 리소스 프로필이 현실적인 RAM, VRAM, 디스크 요구사항을 반영하나요?
- 설정이 로컬 GPU 설치가 1분 API 키 수정이라고 가장하는 것을 피하나요?

---

### Render Runtime Change (렌더 런타임 변경)

Ask:

- Does it preserve runtime choice in `edit_decisions.render_runtime`?
- Does it avoid fallback without user-visible approval?
- Are Remotion and HyperFrames contracts respected?
- Are smoke tests or render probes included?
- Does final output get validated with ffprobe/frame/audio checks where relevant?

**[한국어]**

다음을 질문하십시오.

- `edit_decisions.render_runtime`에서 런타임 선택을 보존하나요?
- 사용자에게 보이는 승인 없이 대체를 피하나요?
- Remotion 및 HyperFrames 계약이 존중되나요?
- 연기 테스트 또는 렌더 프로브가 포함되어 있나요?
- 관련 있는 곳에서 최종 출력이 ffprobe/프레임/오디오 검사로 검증되나요?

---

### Pipeline or Skill Change (파이프라인 또는 스킬 변경)

Ask:

- Does the manifest still validate?
- Do stage skills exist and match stage names?
- Are `review_focus` and `success_criteria` meaningful?
- Are canonical artifacts valid?
- Are human approval gates correct?
- Are tests updated?

**[한국어]**

다음을 질문하십시오.

- 매니페스트가 여전히 유효성 검사를 통과하나요?
- 단계 스킬이 존재하고 단계 이름과 일치하나요?
- `review_focus`와 `success_criteria`가 의미 있나요?
- 정식 아티팩트가 유효한가요?
- 인간 승인 게이트가 올바른가요?
- 테스트가 업데이트되었나요?

---

### Schema Change (스키마 변경)

Ask:

- Which producers and consumers are affected?
- Is the field required or optional?
- Do existing checkpoints/artifacts still work?
- Are tests updated for both valid and invalid data?
- Does the change need a migration note?

**[한국어]**

다음을 질문하십시오.

- 어떤 프로듀서와 소비자가 영향을 받나요?
- 필드가 필수인가요 선택적인가요?
- 기존 체크포인트/아티팩트가 여전히 작동하나요?
- 유효하고 무효한 데이터에 대해 테스트가 업데이트되었나요?
- 변경에 마이그레이션 노트가 필요한가요?

---

### Dependency or Lockfile Change (의존성 또는 Lockfile 변경)

Ask:

- Is the dependency necessary for the PR?
- Is the lockfile change proportional?
- Are install scripts or transitive packages risky?
- Is the package maintained and appropriately licensed?
- Does it work on the supported Python/Node versions?
- Are version bounds too loose or too strict?

**[한국어]**

다음을 질문하십시오.

- 의존성이 PR에 필요한가요?
- lockfile 변경이 비례적인가요?
- 설치 스크립트 또는 전이적 패키지가 위험한가요?
- 패키지가 유지 관리되고 적절하게 라이선스되었나요?
- 지원되는 Python/Node 버전에서 작동하나요?
- 버전 범위가 너무 느슨하거나 엄격한가요?

---

### Docs-Only Change (문서 전용 변경)

Ask:

- Is the doc technically accurate?
- Does it match current code and registry behavior?
- Does it overpromise provider quality, cost, offline operation, or platform
  support?
- Does it point users to the right setup and troubleshooting path?

Docs-only PRs can still create regressions by teaching users or agents the
wrong behavior.

**[한국어]**

다음을 질문하십시오.

- 문서가 기술적으로 정확한가요?
- 현재 코드와 레지스트리 동작과 일치하나요?
- 프로바이더 품질, 비용, 오프라인 작업, 플랫폼 지원을 과대 약속하나요?
- 사용자를 올바른 설정 및 문제 해결 경로로 안내하나요?

문서 전용 PR도 사용자나 에이전트에게 잘못된 동작을 가르침으로써 회귀를 만들 수 있습니다.

---

## Testing Expectations (테스트 기대 사항)

Pick tests based on risk. Do not require expensive integration tests for every
small doc fix, but do require evidence for changed behavior.

Common checks:

```bash
python -m pytest tests/contracts -q
python -m pytest tests/tools -q
python -m pytest tests/qa -q
python -m py_compile path/to/changed_file.py
```

For provider PRs, focused mocked tests are often better than expensive live API
tests. Live-provider QA is useful when credentials and cost are acceptable, but
the contract should not depend on a maintainer having every provider configured.

If tests cannot be run, the review should say why and what risk remains.

**[한국어]**

위험을 기준으로 테스트를 선택하십시오. 모든 작은 문서 수정에 비싼 통합 테스트를 요구하지 마십시오. 그러나 변경된 동작에 대한 증거는 요구하십시오.

일반적인 검사는 위의 코드 블록을 참조하십시오.

프로바이더 PR의 경우 집중된 모의 테스트가 비싼 라이브 API 테스트보다 낫습니다. 라이브 프로바이더 QA는 자격 증명과 비용이 수용 가능할 때 유용하지만, 계약은 메인테이너가 모든 프로바이더를 구성했다는 것에 의존해서는 안 됩니다.

테스트를 실행할 수 없으면 리뷰가 이유와 남은 위험을 말해야 합니다.

---

## PR Comment Guidance (PR 코멘트 가이드)

Good review comments are specific, evidence-based, and actionable.

Prefer:

- "This test fails with the current branch: `...`"
- "This provider will not be discovered because `capability` is set to `...`."
- "This setup claim is misleading because first run downloads model weights."
- "Please split the lockfile churn from this provider change."

Avoid:

- Vague comments like "clean this up"
- Personal comments about the contributor
- Public speculation about intent
- Overclaiming safety
- Long lists of nits when there is a clear blocker

When a PR has several issues, prefer one consolidated comment. It helps the
author fix everything in one pass. Use inline comments for exact line-level
bugs that need code context.

Suggested public language for security review:

- "I found an actionable security issue in this diff."
- "This area needs a security review before merge."
- "I did not find an actionable security issue in the reviewed diff."

Do not state or imply that a contributor has or lacks malicious intent. Review
the code and behavior.

**[한국어]**

좋은 리뷰 코멘트는 구체적이고, 증거 기반이며, 실행 가능합니다.

다음을 선호하십시오.

- "이 테스트는 현재 브랜치에서 실패합니다: `...`"
- "이 프로바이더는 `capability`가 `...`로 설정되어 있어 발견되지 않을 것입니다."
- "이 설정 주장은 오해의 소지가 있습니다. 첫 실행이 모델 가중치를 다운로드하기 때문입니다."
- "이 프로바이더 변경에서 lockfile 변경을 분리해 주십시오."

다음을 피하십시오.

- "이걸 정리하십시오" 같은 모호한 코멘트
- 기여자에 대한 개인적 코멘트
- 의도에 대한 공개적 추측
- 안전성 과대 주장
- 명확한 차단 문제가 있을 때의 긴 답증 목록

PR에 여러 문제가 있으면 하나의 통합된 코멘트를 선호하십시오. 이것이 작성자가 한 번에 모든 것을 수정하는 데 도움이 됩니다. 코드 컨텍스트가 필요한 정확한 줄 수준 버그에는 인라인 코멘트를 사용하십시오.

보안 리뷰를 위한 제안 공개 언어:

- "이 diff에서 실행 가능한 보안 문제를 발견했습니다."
- "이 영역은 병합 전에 보안 리뷰가 필요합니다."
- "검토한 diff에서 실행 가능한 보안 문제를 찾지 못했습니다."

기여자에게 악의적인 의도가 있거나 없다고 말하거나 암시하지 마십시오. 코드와 동작을 검토하십시오.

---

## Maintainer and AI-Agent Workflow (메인테이너 및 AI 에이전트 워크플로우)

This section is public so contributors understand how reviews are performed.
It is a workflow, not a limit on reviewer judgment.

For a full review:

1. Fetch latest `main`.
2. Check out the PR in a clean worktree.
3. Inspect PR metadata: title, linked issues, changed files, author notes, and
   prior comments.
4. Review the diff for scope, usefulness, and architecture fit.
5. Identify the PR scenario: provider, selector, pipeline, schema, runtime,
   docs, tests, dependency, or mixed.
6. Apply the relevant scenario prompts from this guide.
7. Run focused tests or explain why they were not run.
8. Check docs and user-facing claims against implementation.
9. Check security, dependency, and supply-chain risk.
10. Write findings ordered by severity.
11. Decide: approve, comment, request changes, or close/redirect.

For AI-assisted review, ask the agent to report evidence, not just conclusions:

- Commands run and their results
- Files inspected
- Architecture contracts touched
- Risks that remain unverified
- Exact merge blockers

Do not approve from a summary alone. The reviewer or agent should inspect the
diff and relevant project contracts.

**[한국어]**

이 섹션은 공개되어 있으므로 기여자가 리뷰가 수행되는 방식을 이해합니다. 이것은 워크플로우이지 리뷰어 판단에 대한 제한이 아닙니다.

전체 리뷰를 위해 다음을 수행하십시오.

1. 최신 `main`을 가져옵니다.
2. 깨끗한 워크트리에서 PR을 체크아웃합니다.
3. PR 메타데이터를 검사합니다: 제목, 연결된 이슈, 변경된 파일, 작성자 노트, 이전 코멘트.
4. 범위, 유용성, 아키텍처 적합성에 대해 diff를 검토합니다.
5. PR 시나리오를 식별합니다: 프로바이더, 셀렉터, 파이프라인, 스키마, 런타임, 문서, 테스트, 의존성 또는 혼합.
6. 이 가이드에서 관련 시나리오 프롬프트를 적용합니다.
7. 집중된 테스트를 실행하거나 실행하지 않은 이유를 설명합니다.
8. 구현에 대해 문서와 사용자 대면 주장을 확인합니다.
9. 보안, 의존성, 공급망 위험을 확인합니다.
10. 심각도별로 결과를 작성합니다.
11. 결정: 승인, 코멘트, 변경 요청 또는 닫기/리다이렉트.

AI 지원 리뷰의 경우 에이전트에게 결론뿐만 아니라 증거를 보고하도록 요청하십시오.

- 실행된 명령 및 결과
- 검사된 파일
- 접촉된 아키텍처 계약
- 검증되지 않은 위험
- 정확한 병합 차단 문제

요약만으로 승인하지 마십시오. 리뷰어나 에이전트는 diff와 관련 프로젝트 계약을 검사해야 합니다.

---

## Merge-Readiness Rubric (병합 준비 상태 루브릭)

Before approving, confirm:

- The PR is useful and aligned with project direction.
- The diff is focused and free of unrelated churn.
- Architecture contracts are preserved.
- Tests cover the behavior at the right level.
- Docs match user-visible behavior.
- Security and supply-chain risks have been considered.
- Performance, cost, and resource claims are realistic.
- The branch is current enough that review findings are still valid.
- Remaining risks are acceptable and stated.

Approving does not mean the PR is perfect. It means the change is useful,
understood, appropriately tested, and safe enough to land.

**[한국어]**

승인 전 다음을 확인하십시오.

- PR이 유용하고 프로젝트 방향과 정렬됩니다.
- diff가 집중되어 있고 관련 없는 변경이 없습니다.
- 아키텍처 계약이 보존됩니다.
- 테스트가 올바른 수준에서 동작을 포함합니다.
- 문서가 사용자에게 보이는 동작과 일치합니다.
- 보안 및 공급망 위험이 고려되었습니다.
- 성능, 비용, 리소스 주장이 현실적입니다.
- 브랜치가 리뷰 결과가 여전히 유효할 만큼 최신입니다.
- 남은 위험이 수용 가능하고 명시되어 있습니다.

승인은 PR이 완벽하다는 것을 의미하지 않습니다. 변경이 유용하고 이해되고, 적절하게 테스트되었으며, 착륙하기에 충분히 안전하다는 것을 의미합니다.