# 파이프라인 진행 상황 (Living Status Board)

> 이미지/영상 생성 툴을 아직 연결하지 않은 상태에서 **지금 어디까지 갈 수 있고, 어디서 막히는지** 한눈에 보는 문서.
> 진행할 때마다 **아래 체크박스와 "현재 상태 한 줄"을 직접 수정**하세요.

---

## 📍 현재 상태 한 줄

<!-- 진행할 때마다 이 한 줄만 바꿔도 충분합니다 -->
**`scene_plan` 까지 완료 → `assets` 에서 BLOCKED (이미지 생성 미연결)**

| | |
|---|---|
| **마지막 수정** | 2026-07-20 |
| **대상 파이프라인** | `animated-explainer` (주제 → 완성 영상) |
| **현재 데모 run** | `beautiful-green-life` (research→scene_plan 완료, assets 대기) |
| **지금 당장 실행 가능** | `research` · `proposal` · `script` · `scene_plan` (기획/작성 4단계) |
| **막힌 지점(wall)** | `assets` — `image_selector` (이미지 생성) 가 required |

---

## 🗺️ 전체 8단계 진행 체크리스트

체크박스를 직접 `[x]` 로 바꿔가며 진행 상황을 추적하세요.

| # | 단계 | 산출물 | 생성 툴 필요? | 상태 |
|---|------|--------|--------------|------|
| 1 | `research` | research_brief | ✗ | ☐ 완료 |
| 2 | `proposal` | proposal_packet | ✗ | ☐ 완료 |
| 3 | `script` | script | ✗ | ☐ 완료 |
| 4 | `scene_plan` | scene_plan | ✗ (`tools_available: []`) | ☐ 완료 ← **여기까지는 키 없이 가능** |
| 5 | `assets` | asset_manifest | **필수: image + tts** | ☐ 대기(BLOCKED) ← **벽** |
| 6 | `edit` | edit_decisions | 직접 툴 없음 (asset_manifest 입력 필요) | ☐ 대기 |
| 7 | `compose` | render_report → `final.mp4` | **필수: video_compose + audio_mixer** | ☐ 대기 |
| 8 | `publish` | publish_log | export_bundle | ☐ 대기 |

> 💡 **핵심:** `assets`(5)만 뚫리면 `edit → compose → publish` 는 의존성 타고 자동으로 이어집니다.
> 즉 **벽은 한 개** — 이미지 생성 연결 한 번이면 남은 4단계가 전부 풀립니다.

---

## 🚧 왜 `assets` 에서 막히는가

`pipeline_defs/animated-explainer.yaml` 의 `assets` 스테이지에 명시되어 있습니다:

```yaml
required_tools:
  - tts_selector       # 내레이션(TTS)
  - image_selector     # ← 이미지 생성 (필수)
optional_tools:
  - video_selector     # 영상 생성 (없어도 OK — image가 필수라 어차피 통과)
```

`image_selector` 가 **required** 이므로, 이미지 생성 provider가 하나라도 연결돼야 preflight 통과 → assets 진입 가능.

---

## 🔓 언락하려면 (이미지 생성 연결)

**경로 A — provider 키 하나 설정 (가장 빠름)**
- `PEXELS_API_KEY` (무료 추천 — 실사 자연 스톡, 이미지+영상 동시 지원)
- 또는 `FAL_KEY` (FLUX 등 다수 provider 언락)

**경로 B — 바깥에서 이미지 직접 만들어 드롭 (키 불필요)**
- 외부 툴로 이미지 생성 → `projects/<id>/assets/images/` 에 저장
- asset_manifest 에서 `source: "provided"` / `source_tool: "user_provided"` 로 연결

**TTS (내레이션) 도 함께 필요**
- `pip install piper-tts` (오프라인 무료) 또는 본인 목소리 MP3 제공

> 연결 후엔 이 문서 위쪽 "현재 상태 한 줄"과 아래 단계 체크박스를 업데이트하세요.

---

## ✏️ 이 문서를 업데이트하는 법

진행하면서 **3곳만** 바꾸면 됩니다:

1. **"현재 상태 한 줄"** — 지금 어디까지 왔는지 한 문장
2. **"마지막 수정"** 날짜
3. **진행 체크리스트**의 해당 단계 체크박스 `[ ]` → `[x]`

새 provider를 연결했으면 "🔓 언락하려면" 항목에 체크/취소선을 표시해 두면 다음에 보기 편합니다.

---

## 🔗 관련 문서

- 전 단계 상세 흐름 + 스킬 활용: [`front-pipeline-walkthrough.md`](front-pipeline-walkthrough.md)
- 이 세션 전체 기록: [`session-2026-07-20.md`](session-2026-07-20.md)
- 레퍼런스 영상 분석 가이드: [`REFERENCE-VIDEO-GUIDE.md`](REFERENCE-VIDEO-GUIDE.md)
- provider 설정 전체 목록: [`../PROVIDERS.md`](../PROVIDERS.md)
- 파이프라인 매니페스트 원본: [`../../pipeline_defs/animated-explainer.yaml`](../../pipeline_defs/animated-explainer.yaml)
