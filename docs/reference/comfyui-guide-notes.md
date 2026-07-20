# ComfyUI 완벽 가이드 — OpenMontage용 정리 노트

원본: `docs/reference/Stable Diffusion ComfyUI 완벽 가이드_통합_s.pdf` (조피디 연구소, 2024-11-14 초판 / 2025-01-07·2025-06-09 개정, "완벽 가이드"(26장) + "활용편"(15장) 통합본)

이 문서는 원본 전자책(1243페이지)에서 OpenMontage의 현재 ComfyUI 연동
(`tools/_comfyui/`, `comfyui_image`, `comfyui_video`)과 2026년 현재
ComfyUI 기준으로 여전히 유효한 내용만 골라 정리한 것입니다. 원본이
가르치는 구형 UI(메뉴 패널 방식)와 Windows Portable 수동 설치 등은
Comfy Desktop 통합 앱 등장 이후 대부분 대체되었으므로, 화면 조작
설명은 걷어내고 파라미터·설정값·워크플로우 구조 같은 UI에 무관한
알맹이만 남겼습니다.

## 제외한 내용과 이유

- **2장 설치 준비 / 2.2 설치 방법 / 2.3 화면 설명 및 조작 방법(메뉴
  패널 위치)** — 책 자체가 집필 시점에도 이미 신형 Top/Bottom 메뉴 UI가
  존재한다고 언급하면서 "많은 분들에게 익숙한 기존 UI로 강의"를
  선택했다고 밝힘. 2026년 현재는 그 신형 UI조차 지나 **Comfy Desktop**
  (2026-06 개편)이 표준 진입점이 되었으므로, 메뉴 버튼 위치·캔버스
  조작법 같은 화면 설명은 전부 걷어냄. 노드 연결/데이터 흐름 개념만
  "노드/워크플로우 기초" 절에 남김.
- **25장 부록1(설치 방법 총정리: 구글 Colab / Mac 수동 설치 / Windows
  수동 설치 / Desktop 설치)** — Comfy Desktop 통합 앱이 로컬·원격·포터블
  인스턴스를 하나의 앱에서 버전·커스텀노드·스냅샷까지 관리해주므로
  대부분의 사용자에게 더 이상 필요하지 않음. Windows AMD/Linux처럼
  Desktop 미지원 환경이 남아있는 사용자는 원본 PDF 25장을 직접 참고할 것.
- **6.3장의 ComfyUI Manager `security_level` 안내** — 2025년 중반 이후
  ComfyUI Manager는 git-URL 설치·pip 설치를 더 이상 `security_level`
  하나로 묶어 제어하지 않고, `allow_git_url_install` /
  `allow_pip_install` 같은 개별 플래그로 분리했음(악성 노드 자동 스캔도
  추가됨). 책의 "security_level = weak로 낮추라"는 안내는 최신
  ComfyUI Manager에는 그대로 적용되지 않으므로 절차 대신 개념만 남김.
- **부록 FAQ(원본 문서 끝부분)** — PDF 텍스트 추출 과정에서 다단 레이아웃이
  깨져 한글이 뒤섞여 사실상 복원 불가능한 상태였음. Insightface
  버전 불일치, OpenCV 충돌, 짧은 경로 이슈 같은 되풀이되는 주제만
  파악해 "문제 해결 팁" 절에 요약.
- **CogVideo(2B/5B, 2024-08 공개), ToonCrafter, MimicMotion** — 각각
  CogVideoX 세대·프레임 보간 전용·포즈 전이 전용 도구로, 2026년 기준
  Wan 2.1/2.2, Hunyuan Video, LTX Video 같은 최신 네이티브 비디오
  모델에 비해 품질·속도가 뒤처짐. OpenMontage에는 이미 `wan_video`,
  `cogvideo_video`, `comfyui_video`(WAN 2.2 14B) 툴이 있으므로 완전
  삭제하지 않고 "비디오 생성 배경지식" 절에 한 문단씩만 남겨 존재를
  알려둠.
- **17~22장, 19.2 버튜버, 활용편 8~11장(Nvidia Cosmos Video, Hunyuan
  3D 2.0, Flux PuLID 상세 다운로드/설치, Sonic 립싱크 준비 과정)** —
  단계별 모델 다운로드·커스텀 노드 설치 스크린샷 절차는 화면 조작과
  분리하기 어려워 통째로 제외하고, 워크플로우 아이디어·핵심 노드
  이름만 "실전 레시피 아이디어" 절에 요약해 남김.
- **Flux.1 Kontext를 "Pro/Max만 유료 API로 사용 가능, Dev는 미출시"로
  설명한 부분(15.1)** — **웹 검색으로 확인한 결과 이는 이미 낡은
  정보**: FLUX.1 Kontext **[dev]는 2025-06-26 오픈 웨이트로 정식
  출시**되어 ComfyUI에서 로컬로 무료 사용 가능하다(FLUX.1
  Non-Commercial License). 아래 FLUX Kontext 절에서 이 최신 사실로
  교체해 정리함.

## 1. 노드·워크플로우 기초

ComfyUI는 전 과정이 노드로 연결된 시각적 파이프라인이다. 핵심 개념은
UI 세대가 바뀌어도 그대로 유효하다.

- **기본 흐름**: `Load Checkpoint` → `CLIP Text Encode`(긍정/부정) →
  `KSampler` → `VAE Decode` → `SaveImage`. `Empty Latent Image`가
  노이즈 이미지를 만들고, `KSampler`가 체크포인트·프롬프트·설정값을
  기반으로 노이즈를 점진적으로 제거하며, `VAE Decode`가 최종 픽셀
  이미지로 복원한다.
- **KSampler 핵심 옵션**: `seed`(고정하려면 `control_after_generate =
  fixed`), `steps`, `cfg`(프롬프트 반영 강도), `sampler_name` /
  `scheduler`(취향 문제, 여러 조합 테스트 권장), `denoise`(img2img에서
  낮을수록 원본 유지, 높을수록 결과가 원본과 멀어짐).
- **연결점 색상**은 데이터 타입을 의미하며 동일 색상끼리만 연결 가능
  (MODEL/CLIP/VAE/CONDITIONING/LATENT/IMAGE/MASK 등).
- **배치 생성**: `batch_size`(Empty Latent Image, 한 번에 생성 수량,
  VRAM 비례) vs `batch count`(Extra options에서 노출, 생성 반복
  횟수, 시간 비례). VRAM이 부족하면 batch_size는 1로 두고 batch
  count만 올리는 편이 안전.
- **그룹화**: 노드를 드래그해 Group으로 묶거나(`Add Group`), 여러
  노드를 선택 후 "Convert to Group Node"로 하나의 커스텀 UI처럼
  합칠 수 있음. 큰 워크플로우를 관리할 때 필수.
- **Primitive 노드**: 연결 대상에 따라 타입이 자동 결정되는 범용
  입력 노드. 동일한 프롬프트/시드를 여러 노드에 동시에 공급할 때
  씀(예: Slider LoRA 비교 워크플로우에서 두 KSampler에 같은 seed
  전달).
- **워크플로우 저장/불러오기**: `.json`으로 저장·공유 가능하고,
  ComfyUI/A1111에서 생성된 이미지 자체에도 워크플로우 메타데이터가
  박혀 있어 이미지를 캔버스에 드래그하면 그대로 복원된다.
  **주의 — API 형식**: OpenMontage `tools/_comfyui/client.py`는
  `POST /prompt`에 **API 포맷 JSON**만 받는다. ComfyUI 메뉴의 기본
  `Save`는 캔버스 레이아웃용 UI 포맷이며 API 포맷이 아니다. 커스텀
  워크플로우를 OpenMontage에 넘기려면 반드시 API 포맷으로 다시
  내보내야 한다(`.agents/skills/comfyui/SKILL.md` 참고). 원본 책은
  이 구분을 다루지 않으므로 별도로 챙겨야 하는 부분.

## 2. Custom Node와 ComfyUI Manager

- **설치 경로 4가지**: GitHub URL을 `custom_nodes`에 git clone / zip
  다운로드 / **ComfyUI Manager → Custom Nodes Manager**(검색·설치) /
  **ComfyUI Manager → Install via Git URL**. 대부분은 뒤의 두 방법으로
  충분.
- **Install Missing Custom Nodes**: 공유받은 워크플로우에 설치 안 된
  노드가 있을 때 자동 탐지·설치. `.agents/skills/comfyui/SKILL.md`도
  커스텀 노드 누락 시 이 경로(또는 워크플로우 작성자의 설치 문서)를
  안내하라고 명시하므로 그대로 유효한 흐름.
- 노드 우측 상단에 뜨는 배지(옵션 → Node Badge → "Show all")로 노드
  ID와 커스텀 노드 여부(이름 표시 vs 기본 아이콘)를 구분할 수 있음 —
  워크플로우 디버깅 시 유용.
- **여전히 유효하고 자주 언급된 필수 커스텀 노드** (2026 기준 GitHub
  저장소 확인 필요, 아래는 원본이 실제 사용한 것들):
  - `pythongosssss/ComfyUI-Custom-Scripts` — 임베딩 자동완성, 그래프
    자동 정렬, 워크플로우를 PNG로 내보내기.
  - `pythongosssss/ComfyUI-WD14-Tagger` — 이미지 → 태그 프롬프트 추출.
  - `rgthree/rgthree-comfy` — `Lora Loader Stack`(로라 최대 4개 동시
    적용), `Seed`, `Fast Groups Bypass`, `Image Comparer`, 선택 출력
    노드만 실행하는 `Queue Selected Output Nodes`.
  - `kijai/ComfyUI-KJNodes` — `SetNode`/`GetNode`로 연결선 없이 원격
    연결(대형 워크플로우 정리에 필수).
  - `chrisgoringe/cg-use-everywhere` — `Anything Everywhere` /
    `Anything Everywhere3` / `Prompts Everywhere`로 모델·VAE·프롬프트를
    자동 원격 연결. FLUX처럼 모델 3종을 여러 노드에 반복 연결해야
    할 때 특히 유용.
  - `Kosinkadink/ComfyUI-VideoHelperSuite` — `Load Video`, `Video
    Combine` 등 영상 입출력 표준 노드.
  - `storyicon/comfyui_segment_anything` — SAM + GroundingDINO 기반
    텍스트 프롬프트 자동 마스킹(`GroundingDinoSAMSegment`).
  - `Acly/comfyui-inpaint-nodes` — Outpainting 확장 영역에 자연스러운
    노이즈를 채우는 `Fill Masked Area`/`Blur Masked Area`.
  - `chflame163/ComfyUI_LayerStyle` — `LayerUtility: H/L Frequency
    Detail Restore`(합성 후 원본 디테일 복원), `ImageBlendAdvance V2`
    (레이어 합성), `Purge VRAM`.
  - `city96/ComfyUI-GGUF` — FLUX/Wan/Hunyuan 등 대형 모델의 GGUF
    양자화 버전 로더. 저VRAM 환경의 핵심.
  - `Jonseed/ComfyUI-Detail-Daemon` — 샘플링 중 노이즈 스케줄을 조작해
    디테일을 강화(FLUX 권장 0.1~1.0, SDXL 권장 0.25 미만).

## 3. LoRA 활용

- A1111의 `<lora:name:weight>` 프롬프트 문법과 달리 ComfyUI는 반드시
  **노드**로 LoRA를 연결해야 한다: `LoraLoader`(model+clip 동시 적용)
  또는 이미지 생성에 영향 없이 모델에만 적용하는
  `LoraLoaderModelOnly`(ControlNet-as-LoRA류에 사용).
- 옵션: `lora_name`, `strength_model`(기본 모델 가중치에 대한 영향),
  `strength_clip`(텍스트-이미지 정합에 대한 영향). 두 값을 다르게 줄 수
  있음.
- **다중 LoRA**는 `LoraLoader`를 일렬로 여러 개 연결해도 되지만,
  rgthree의 `Lora Loader Stack (rgthree)` 노드 1개로 최대 4개를 한
  번에 관리하는 편이 훨씬 깔끔함(5개 이상이면 두 번째 스택 노드를
  이어붙임).
- **Concept Slider LoRA**(CivitAI에 "slider"로 검색): 나이·표정·피부톤·
  체형 등 속성을 이미지 구조는 유지한 채 연속적으로(음수~양수)
  조절하는 LoRA 계열. `strength_model`/`strength_clip`을 Input으로
  변환해 `Primitive` 노드와 연결하고 `Auto Queue`를 켜면 슬라이더
  값을 바꿀 때마다 실시간 재생성되어 최적값을 빠르게 탐색할 수 있음.
- **OpenMontage 연동 관점**: `.agents/skills/comfyui/SKILL.md`에
  명시된 대로 **현재 `comfyui_image`/`comfyui_video`는 임의 그래프에
  LoRA를 자동 주입하지 않는다.** LoRA를 쓰려면 위 `LoraLoader`/
  `LoraLoaderModelOnly` 체인이 이미 포함된 워크플로우를
  `workflow_json`/`workflow_path` + `output_node`로 직접 넘겨야
  한다 — 이 장의 내용이 정확히 그 워크플로우를 만드는 방법이다.

## 4. 이미지 편집 기법

### Img2Img / 실시간 스케치
- txt2img에서 `Empty Latent Image`만 `Load Image` → `VAE Encode`로
  교체하면 img2img가 된다. `denoise`가 핵심 변수(0=원본 그대로,
  1=원본 무시).
- **LCM 기반 실시간 스케치**: LCM LoRA(strength 0.5) + `steps 3~8`,
  `cfg 1~3`으로 설정하면 노이즈 제거를 몇 스텝만에 끝내 사실상
  실시간으로 이미지가 생성된다. `AlekPet` 커스텀 노드의
  `PainterNode`(브러시 스케치 캔버스)를 `Load Image` 자리에 연결하고
  `Auto Queue`를 켜면 그림을 그릴 때마다 결과가 즉시 갱신됨. 게임
  아이콘 스케치(21.2장)에서는 SDXL Lightning 4-step 모델로 동일한
  기법을 재사용함.

### 업스케일 4가지 (원본 9장)
| 방식 | 원리 | 특징 |
|---|---|---|
| Upscale using Model | `Load Upscale Model` + `Upscale Image (using Model)`(예: 4x-UltraSharp) | 가장 단순, 픽셀 업스케일만 |
| Img2img Upscale | 업스케일 후 낮은 denoise(~0.35)로 재생성 | 디테일 보강, 시간 배로 |
| **Ultimate SD Upscale** | 이미지를 타일로 쪼개 각각 업스케일 후 합성(`mode_type: Linear/Chess/None`, `tile_width/height`, `mask_blur`, `tile_padding`) | 원본 변형 최소화하며 품질 향상, 커스텀 노드 `ssitu/ComfyUI_UltimateSDUpscale` 필요 |
| Latent Upscale | `Upscale Latent By`로 픽셀화 이전 잠재 벡터 단계에서 확장 | 속도·품질 모두 우수하지만 denoise 값에 민감(0.35~0.7 사이 실험 필요) |

FLUX에서는 `Ultimate SD Upscale`을 `steps=1`, `denoise=0.20`처럼
극단적으로 낮게 줘도 품질이 크게 향상됨(FLUX 자체 품질이 높기
때문). 흐릿하고 노이즈 많은 옛날 사진은 Ultimate SD Upscale보다
FLUX ControlNet Upscale(전용 ControlNet 모델 + WD14 Tagger로 원본
태그 추출 후 재사용) 쪽이 더 낫다고 원본이 명시.

### Inpainting / Outpainting
- 기본 체인: `Load Image` → 마스크(`Open in MaskEditor` 또는
  segment-anything 자동 마스킹) → `VAE Encode (for Inpainting)` 또는
  `InpaintModelConditioning` → `KSampler`. `grow_mask_by`로 마스크
  경계를 확장/축소.
- **Soft Inpainting**: `Differential Diffusion` 노드(모델에 연결) +
  `Gaussian Blur Mask`(마스크에 블러)로 경계를 자연스럽게 블렌딩.
  일반 Inpainting보다 안경·머리카락처럼 섬세한 요소의 경계가 훨씬
  매끄러움.
- **Inpainting 전용 모델을 직접 합성하는 트릭**: `ModelMergeSubtract`로
  (Base Inpainting 모델 − Base 모델 = 인페인팅 가중치만) 뽑아낸 뒤,
  `ModelMergeAdd`로 원하는 고품질 체크포인트에 다시 얹으면, 일반
  Inpainting 전용 모델보다 퀄리티 높은 나만의 Inpainting 모델을 만들
  수 있음.
- **Outpainting**: `Pad Image for Outpainting`(left/top/right/bottom
  픽셀 확장 + `feathering`)으로 캔버스를 넓히고 마스크를 자동
  생성한 뒤, 나머지는 Inpainting과 동일 체인. 확장 영역 경계에 라인이
  보이면 `comfyui-inpaint-nodes`의 `Fill Masked Area`(옵션:
  neutral/telea/navier-stokes) + `Blur Masked Area` + `GrowMask`로
  노이즈를 채운 뒤 Soft Inpainting까지 얹으면 경계가 완전히 사라짐.

### ControlNet / IP-Adapter
- 기본 체인: `Load Image` → 전처리 노드(`Canny`, `Depth Anything`,
  `OpenPose Pose`/`DWPose Estimator`, `SAM Segmentor` 등) →
  `Load ControlNet Model` → `Apply ControlNet`(`strength`,
  `start_percent`, `end_percent`) → `KSampler`.
- 여러 ControlNet을 병렬로 동시에 걸 수 있으나 VRAM·속도 부담이 크므로
  그룹 단위로 `Bypass Group Nodes`/`Set Group Nodes to Always`로
  필요한 것만 켜고 끄는 패턴을 원본이 반복 사용.
- **IP-Adapter**(참조 이미지의 스타일·구도·색감을 반영): 프리셋별
  참조 충실도가 다름 — `LIGHT`(분위기만) < `STANDARD` < `VIT-G`(구도까지)
  < `PLUS`(스타일+구도+포즈+배경 전부, 과할 수 있음) <
  `PLUS FACE`/`FULL FACE`(얼굴 전용). ControlNet과 함께 쓸 때는
  `weight`를 낮추거나 `VIT-G` 프리셋으로 내려서 과적합을 피하는 편이
  실전에서 잘 맞았다고 원본이 명시.

## 5. FLUX 계열 (여전히 핵심, 단 FLUX 2로 세대교체됨에 주의)

OpenMontage `comfyui_image`는 이미 **FLUX 2 Dev NVFP4**를 번들
워크플로우로 쓴다. 아래는 원본이 다룬 **FLUX.1** 시대의 기법이며,
모델 자체는 한 세대 전이지만 워크플로우 패턴(가이던스 별도 처리,
전용 샘플러, 양자화 포맷 선택)은 FLUX 2에도 그대로 통용된다.

- **양자화 포맷 선택**: FP8(`weight_dtype: fp8_e4m3fn`) / GGUF(`Q2`~`Q8`
  숫자가 비트수, `city96/ComfyUI-GGUF`의 `Unet Loader (GGUF)` 사용) /
  NF4(체크포인트 취급, `\models\checkpoints`에 저장). 본인 VRAM에
  맞는 비트수를 고르는 게 핵심이며 GGUF/NF4/FP8 모두 워크플로우
  구조는 거의 동일하고 로더 노드만 바뀜.
- FLUX는 **네거티브 프롬프트를 쓰지 않음**. `KSampler` 대신
  `SamplerCustomAdvanced` + `BasicGuider`/`BasicScheduler`/
  `KSamplerSelect`(sampler=euler, scheduler=simple) 조합을 쓰고,
  `FluxGuidance` 노드로 CFG 대신 정제된 guidance 값을 준다
  (일반 생성 3.5, Fill/Inpaint 계열은 공식 권장 30).
- **FLUX Turbo LoRA**(`alimama-creative/FLUX.1-Turbo-Alpha`): 8
  step만으로 20 step 수준 품질, 속도 2배 이상. `Power Lora Loader
  (rgthree)`로 켜고 끄며 A/B 비교 권장.
- **Detail Daemon**(`Jonseed/ComfyUI-Detail-Daemon`): 샘플링
  스케줄러의 노이즈 곡선을 조작해 디테일을 끌어올림. `detail_amount`
  FLUX 0.1~1.0 권장, `start`/`end` 조정 구간 지정.
- **가속 캐싱(TeaCache / First Block Cache)**: 반복 연산 결과를 캐시해
  1.5~2배 속도 향상. `rel_l1_thresh`가 낮을수록 자주 캐시(속도↑
  품질↓). PuLID·Wan 계열에서도 동일 원리로 재사용됨(`WanVideo Tea
  Cache` 등). 속도 우선 작업에는 유용하지만 품질이 최우선이면
  비활성화 권장.
- **FLUX.1 Tools 4종**(Black Forest Labs 공식, 여전히 현역):
  - **Fill** — 전용 Inpaint/Outpaint 모델. `noise_mask=true`(인페인트)
    /`false`(아웃페인트 확장부 흐릿함 방지), guidance 30 권장.
  - **Depth / Canny** — 전용 ControlNet 모델(23.8GB 풀버전 또는
    Civitai 경량화 11GB대 버전), guidance 30 권장.
  - **Redux** — IP-Adapter와 유사한 스타일 어댑터. 주의: 공식적으로는
    Dev 모델에서 이미지+텍스트 프롬프트 동시 반영이 지원되지 않고
    이미지만 참조됨(Pro Ultra 전용 기능) — 텍스트를 함께 반영하려면
    커스텀 노드 `Apply Style Model (Adjusted)`로 교체하고
    `strength`(0.0~0.3=텍스트 우선, 0.4~0.7=균형, 0.8~1.0=이미지
    스타일 우선)를 조절.
  - 다중 활용 예: **CatVTON LoRA**(`zhengchong/CatVTON`) + Fill +
    Redux로 의상 이미지와 모델 이미지를 한 장으로 합쳐 가상 착용
    이미지를 생성하는 실전 워크플로우(피팅 모델 이미지 자동 생성).
- **FLUX ControlNet 통합 모델**: `Shakker-Labs`/`Kijai` 양자화 버전의
  `Flux.1-dev-ControlNet-Union-Pro`가 Canny/Depth/Pose/Tile/Blur를
  한 모델로 지원. `SetUnionControlNetType` 노드로 기능 선택
  (`auto` 권장).
- **FLUX Kontext — 2026년 기준 최신 상태로 갱신**: 원본은 "Dev
  버전 미출시, Pro/Max만 유료 API"로 설명하지만, **FLUX.1
  Kontext [dev]는 2025-06-26에 오픈 웨이트로 정식 출시**되어
  FLUX.1 Non-Commercial License 하에 로컬·무료 사용이 가능하다
  (ComfyUI day-0 네이티브 지원). 이미지 한 장 + 자연어 프롬프트만으로
  일관된 인물/스타일을 유지한 채 편집(의상 교체, 배경 교체·확장,
  표정·각도 변경, 스타일 전이)이 가능한 것이 핵심 강점 — 참조
  이미지 두 장을 좌우/상하로 이어붙여 한 장으로 넣으면 "인물 A에
  제품 B를 합성" 같은 합성 작업도 가능(단, 두 이미지의 시각 요소가
  서로 겹치지 않게 준비할 것 — 예: 인물 참조 이미지에 탱크탑이
  보이면 새 의상 프롬프트가 잘 반영되지 않는 문제 발생).
  Pro/Max는 여전히 유료 API(ComfyUI 계정 Credit 기준 Pro
  $0.04/Max $0.08 수준, 변동 가능)로만 제공됨.

## 6. 비디오 생성 배경지식 (구세대 → 현행 비교)

OpenMontage에는 이미 diffusers 기반 `wan_video`, `cogvideo_video`와
ComfyUI 기반 `comfyui_video`(WAN 2.2 14B FP8 4-step)가 있다. 아래는
그 배경이 되는 기술들의 위치를 정리한 것 — **직접 번들되지 않은
모델을 커스텀 워크플로우로 쓰고 싶을 때의 참고 지도**로 보면 된다.

- **AnimateDiff**(SD1.5 기반, `Kosinkadink/ComfyUI-AnimateDiff-Evolved`) —
  2026년에도 완전히 죽지 않음: **6~8GB VRAM** 저사양 환경에서 SD1.5
  체크포인트 생태계를 그대로 활용할 수 있는 몇 안 되는 경로라 여전히
  쓰인다(웹 검색 확인). 다만 Wan 2.1/2.2 같은 신세대 모델 대비 동작
  일관성·화질은 명백히 뒤처짐. 핵심 노드: `AnimateDiff Loader`,
  `Context Options`(`context_length`/`context_overlap`로 프레임 간
  연속성 제어), `Prompt Scheduling`(프레임별 프롬프트 전환),
  ControlNet과 함께 쓸 때는 반드시 `Load Advanced ControlNet Model`
  사용. FaceDetailer로 얼굴 뭉개짐 보정하는 패턴은 다른 저사양
  파이프라인에도 재사용 가능.
- **SVD(Stable Video Diffusion)** — img2vid 전용, 25프레임/720p급.
  `motion_bucket_id`(움직임 강도), `augmentation_level`(원본과의
  차이 정도), `fps=6` 권장. `FILM VFI` 노드로 프레임 보간해 체감
  프레임레이트를 올리는 패턴은 여전히 유용(Wan/Hunyuan 출력에도
  동일하게 적용 가능).
- **CogVideoX(2B/5B, 2024)** — OpenMontage `cogvideo_video`가 이미
  지원하는 모델 계열. 720x480 고정 해상도, 6초/8fps 한계가 뚜렷해
  2026 기준으로는 저사양 대체재 정도의 위치. VRAM 부족 시
  `enable_sequential_cpu_offload` + `CogVideo Decode`의
  `enable_vae_tiling`이 유효한 완화책.
- **Hunyuan Video**(Tencent, 130억 파라미터) — 여전히 현역급 오픈소스
  비디오 모델. **8GB VRAM에서도 `VAE Decode (Tiled)` 노드**(ComfyUI
  v0.3.10+)로 구동 가능한 게 핵심 — 시간축 타일링이라 공간 타일링보다
  메모리 효율이 훨씬 좋음. GGUF 양자화(6~14GB), FastHunyuan
  체크포인트/LoRA로 8 step(오리지널 50 step 대비 8배 가속) 생성도
  지원.
- **LTX Video(LTXV, Lightricks)** — ComfyUI 네이티브 지원, RTX
  4090에서 5초 분량(121프레임)을 20 step으로 수 초 만에 생성할 만큼
  빠름. `.agents/skills/comfyui/SKILL.md`가 8-12GB급 저VRAM
  옵션으로 명시한 모델 중 하나. `LTXVAddGuide`로 특정 프레임에
  키프레임 강제 삽입, 이전 영상의 마지막 프레임을 이어붙여 5초
  단위로 무한 확장 생성하는 패턴이 특히 실전적. 프롬프트 마지막에
  "the scene is captured in real-life footage." 문장을 붙이면 실사
  톤이 강화된다고 원본이 강조.
- **Nvidia Cosmos** — 7B/14B, 12GB에서 1280x704/121프레임을 무타일링
  디코딩 가능할 만큼 VAE가 효율적. 121프레임 고정에 최적화되어 있어
  다른 길이로 생성하면 품질이 깨지는 경향. 참고용으로만 남김(니치).

## 7. Wan 2.1/2.2 심화 — VACE 올인원 모델

`.agents/skills/comfyui/SKILL.md`가 8-12GB급 저VRAM 옵션으로 Wan 2.1
1.3B를 명시하고 있고, OpenMontage의 번들 `comfyui_video`는 WAN 2.2
14B FP8이므로 이 장은 커스텀 워크플로우 작성 시 가장 직접적으로
쓸모 있는 절이다.

- **모델 크기 선택**: t2v는 1.3B(약 13억 파라미터, 저VRAM)와
  14B(고품질) 두 갈래, i2v는 14B만 있고 480p/720p 최적화 버전으로
  나뉨. 정밀도는 fp16 > bf16 > fp8_scaled > fp8 순으로 품질이 좋음.
  14B 원본은 28.6~32.8GB이므로 대부분은 `city96`의 GGUF 양자화
  버전(`Q2`~`Q8`)을 VRAM에 맞춰 선택.
- **공통 모델 4종**: Checkpoint(`diffusion_models` 또는 GGUF는
  `unet`), Clip(`umt5_xxl_fp8_e4m3fn_scaled`, type=`wan`),
  VAE(`wan_2.1_vae`), Clip Vision(`clip_vision_h`, i2v에만 필요).
- **t2v 기본값**: `ModelSamplingSD3`(shift 기본값 유지),
  `KSampler`(steps 30, cfg 6.0, sampler `uni_pc`, scheduler
  `simple`), `Video Combine`(frame_rate 16).
- **i2v**: `WanImageToVideo` 노드가 해상도(모델의 480p/720p에 맞춤)와
  `length`를 받음. `CLIP Vision Encode`로 참조 이미지를 인코딩.
- **v2v(1.3B 저VRAM 경로)**: `LoraLoaderModelOnly` +
  `wan2.1-1.3b-control-lora-depth` 같은 "ControlNet-as-LoRA" 모델로
  가볍게 구조 제어. `SplitSigmas`로 샘플링을 2단계(high_sigmas로
  전체 구조 → low_sigmas로 디테일)로 나눠 두 개의 `SamplerCustom`에
  순차 연결하는 패턴이 품질 향상에 크게 기여. 프롬프트는
  `Florence2Run`(`MiaoshouAI/Florence-2-base-PromptGen-v2.0`)으로
  참조 이미지에서 자동 추출 가능. `WanVideo Tea Cache (native)`로
  속도 향상(1.3B 권장 `rel_l1_thresh` 0.05~0.08).
- **공식 ControlNet(Wan 2.1 Fun 모델)**: Open Pose/Canny(LineArt)/Depth
  3종 지원. `wan2.1_fun_control_1.3B_bf16` 체크포인트 +
  `WanFunControlToVideo` 노드(start_image + control_video를 함께
  입력). Control Tile LoRA는 Fun ControlNet 모델과 함께 못 쓰므로
  별도 `Load Diffusion Model`(오리지널 t2v 1.3B)에 연결해야 함.
- **Effect LoRA**(`Remade-AI`, HuggingFace) — i2v 워크플로우에 LoRA
  하나만 얹으면 되는 재미있는 상업용 이펙트: `Squish`(찰흙처럼
  누르기), `Rotate`(360도 회전), `Inflate`(풍선처럼 부풀리기),
  `Cakeify`(단면이 케이크로 변하는 컷), `Crush`(압착). 각 LoRA마다
  고유 트리거 키워드가 있음(예: `sq41sh squish effect`,
  `r0t4tion 360 degrees rotation`). SNS 숏폼에 바로 쓸 수 있는
  수준의 완성도.
- **VACE(올인원 모델, Alibaba)** — 참조-비디오 생성(R2V), 비디오
  편집(V2V), 마스크 기반 편집(MV2V)을 하나의 모델로 통합. 핵심 노드:
  `WanVideo Model Loader`(+ `vace_model` 입력에 `WanVideo VACE Model
  Select` 연결), `WanVideo VACE Encode`(`input_frames`/`ref_images`/
  `input_masks`/`prev_vace_embeds` 입력으로 다양한 조합 가능),
  `WanVideo Sampler`, `WanVideo Decode`(`enable_vae_tiling`으로 긴
  영상 대응). 실전 활용 5가지 패턴을 원본이 모두 예제로 제공:
  1. **기본**: 참조 이미지 1장 → 자연스러운 동작 영상.
  2. **배경 교체**: `Image Rembg`로 배경 제거(흰색 채움 권장) 후
     프롬프트에 새 배경 키워드 추가.
  3. **포즈 컨트롤**: 참고 영상을 `OpenPose Pose`로 분석 →
     `input_frames`에 포즈, `ref_images`에 인물 이미지를 따로 넣어
     "이 사람이 이 포즈로 움직이게" 구현. 포즈 참고 영상의 첫
     프레임과 참조 이미지의 포즈를 비슷하게 맞추면 결과가 더 안정적.
  4. **시작/끝 프레임 지정**: `WanVideo VACE Start To End Frame`
     노드로 시작·끝 이미지를 주면 중간 프레임을 보간 생성(카메라
     줌아웃 + 인물 회전 같은 연출 가능). 두 프레임의 인물/의상/배경
     차이가 크면 결과가 부자연스러워짐.
  5. **제품 홍보 영상**: 인물 이미지 + 제품 이미지 각각 배경 제거 →
     `Image Concatenate`로 좌우 결합 → 레퍼런스 이미지로 사용,
     프롬프트에 "인물이 제품을 든다"는 상호작용을 직접 서술. 두
     피사체의 상대적 크기 비율을 맞추는 것이 품질의 핵심.
  - 부가 품질 노드: `WanVideo Enhance-A-Video`(얼굴/손 디테일 강화,
    weight 0.5~2.0), `WanVideo SLG`(특정 Transformer 블록만 조정,
    보통 후반부 블록), `WanVideo TeaCache`(속도 우선 시에만 사용,
    품질 우선 작업에는 비활성화 권장).

## 8. 캐릭터 일관성 유지 & 얼굴

- **정의**: 얼굴 생김새·의상 스타일·전체 이미지 톤 3요소를 여러 장에
  걸쳐 동일하게 유지하는 것.
- **FLUX Fill + Redux 조합** — 참조 인물 이미지와 새 포즈/배경
  참조 이미지를 좌우로 이어붙여 한 장으로 만든 뒤, 오른쪽 절반만
  인페인팅(Differential Diffusion으로 소프트 인페인트) + Redux로
  왼쪽 인물의 스타일을 참조시켜 "동일 인물, 새 포즈/배경" 이미지를
  생성. 프롬프트에 "이것은 한 쌍의 이미지이며 오른쪽은 왼쪽과 동일
  인물의 사진"이라고 명시하는 것이 핵심. ControlNet(Depth,
  strength 0.5)까지 더하면 구도 일치도가 더 올라감.
- **ACE Plus Portrait LoRA**(`ali-vilab/ACE_Plus`) — FLUX Fill
  워크플로우와 통합이 잘 되는 얼굴 전용 보정 LoRA. 1차 생성 후 얼굴만
  다시 SAM으로 마스킹(`prompt: "face, eyes"`)해 2차 인페인팅으로
  얼굴 싱크로율을 높이는 2단계 패턴.
- **Flux PuLID**(`ComfyUI_PuLID_Flux_ll`) — 얼굴 임베딩을 직접
  주입하는 방식이라 Redux/IP-Adapter보다 얼굴 재현율이 높음.
  `weight`, `start_at`/`end_at`으로 강도·적용 구간 조절.
  `Pulid Flux Options`의 `input_face_order`(left-right 등)와
  `input_face_index`로 다중 얼굴 참조 이미지에서 특정 인물만 선택
  가능. 마스크로 여러 `Apply PuLID Flux` 노드를 병렬 연결하면 한
  이미지에 서로 다른 얼굴 2명을 동시에 합성 가능.
- **ReActor**(`Gourieff/comfyui-reactor-node`, Face Swap) — 웹 검색
  결과 **2026년 현재도 활발히 유지보수됨**. 최근 "ReActor Core"로
  개편되어 과거 원본 책이 요구하던 Insightface 수동 설치·Visual
  Studio C++ 빌드 도구 설치 없이도 동작하도록 간소화됨(설치
  난이도가 낮아졌으므로 책의 복잡한 사전 준비 절차는 최신 버전
  기준으로 낡은 정보). 핵심 옵션: `face_restore_model`(codeformer/
  GFPGAN이 품질 우수), `input_faces_index`/`source_faces_index`(다중
  얼굴 중 선택), `face_model`을 별도 파일로 저장해 재사용 가능.
  영상에도 그대로 적용 가능(`ReActor Face Booster`로 후보정).
  9종 이상의 대안 페이스스왑 노드(`ComfyUI-DeepFuze`,
  `ComfyUI-InstantId-FaceSwap` 등)도 존재하니 라이선스나 결과물
  요구사항에 따라 비교해볼 것.
- **Advanced Live Portrait**(`PowerHouseMan/ComfyUI-AdvancedLivePortrait`) —
  `Expression Editor (PHM)`로 회전/눈썹/눈깜빡임/입모양을 슬라이더로
  세밀 조정하거나 샘플 이미지의 표정을 그대로 전이. 여러 표정을
  프레임 구간별로 배치(`"1 = 5:5"` 같은 문법)해 표정 전환 애니메이션
  생성, 웹캠 실시간 캡처로 버추얼 아바타 프리뷰까지 가능.
- **Sonic 립싱크**(Tencent) — 오디오 기반 얼굴 애니메이션. 입모양뿐
  아니라 어깨 들썩임 같은 미세한 호흡 동작까지 재현하는 것이 강점.
  SVD 기반이라 `SVD-img2vid-xt-1-1` 체크포인트가 필요. 니치하지만
  대안이 마땅치 않은 영역이라 후보로 기록.

## 9. 실전 레시피 아이디어 (활용편 요약)

원본 활용편 17~22장의 세부 절차는 화면 조작 위주라 생략했지만,
재사용 가치가 있는 노드 조합 아이디어만 남긴다.

- **AI 인플루언서 얼굴 고정 + 무한 포즈 생성**: IP-Adapter FaceID
  Plus V2로 대표 얼굴을 고정한 뒤, OpenPose ControlNet으로 포즈만
  바꿔가며 대량 생성 — 동일 인물의 SNS 콘텐츠를 스튜디오 촬영 없이
  양산하는 패턴.
- **댄스 챌린지 영상**: `MimicMotion`으로 참고 영상의 포즈를
  추출(`include_body/hand/face`)해 다른 인물 이미지에 이식 →
  ReActor로 얼굴 보정 → 여러 결과를 `Image Concatenate Multi`로
  나란히 배치한 비교 영상까지 한 워크플로우로 완성.
- **패턴 디자인(시임리스 타일)**: `Seamless Tile` 노드(모델의 MODEL
  입출력에 삽입) + 타일 전용 `Circular VAE Decode (tile)`로 이음새
  없는 반복 패턴 생성. `iTools Grid Filler`(`gaps=0`)로 큰 캔버스에
  자동 배열. 복잡한 디자인 요소는 중앙에, 이음새 부분은 단순한
  패턴으로 배치해야 인쇄 오차에 안전하다는 실무 팁.
- **제품 이미지 합성**: `GroundingDinoSAMSegment`로 제품만 분리 →
  배경 생성(ControlNet Depth/Lineart) → `ImageBlendAdvance V2`로
  합성 → **`LayerUtility: H/L Frequency Detail Restore`로 Encode/
  Decode 과정에서 손상된 제품 로고·텍스트 디테일을 원본과
  주파수 합성해 복원**(가장 실전적인 팁 — VAE 왕복을 거치면 텍스트가
  뭉개진다는 것을 원본이 직접 실험으로 보여줌). 반사 효과는 제품
  이미지를 뒤집고(`Image Flip`) 블러 처리해 반투명 오버레이로 얹는
  식으로 저비용 구현. 조명은 `IC-Light`(`iclight_sd15_fc`/`fbc`/
  `fcon` 3종, 마스크로 광원 위치 제어)로 추가.
- **게임 아이콘**: 전용 체크포인트+LoRA 조합에 `Text Multiline` 3개
  (퀄리티/오브젝트/배경 프롬프트)를 `Text Concatenate`로 합쳐 관리하는
  프롬프트 구조화 패턴 + Mixamo 모션 캡처 화면을 OpenPose 참조
  이미지로 활용하는 아이디어.

## 10. LLM 연동 (Ollama)

- ComfyUI + `stavsap/comfyui-ollama` 커스텀 노드로 로컬 LLM(Ollama)을
  프롬프트 생성/이미지 분석에 활용하는 패턴. 원본은 `llama3.2`
  계열을 썼지만 Ollama 모델 목록은 계속 갱신되므로 실제 사용 시점의
  최신 vision/text 모델로 교체하면 됨 — 노드 구조 자체는 모델
  버전과 무관하게 유효.
- `Ollama Generate Advance`: 프롬프트 입력란 + 시스템 메시지
  입력란 2개. 한국어로 대략적인 아이디어만 입력해도 시스템
  메시지("AI 이미지 생성 프롬프트 전문가로서 주제/구도/분위기/색감/
  조명을 문단별로 영어로 서술")로 영어 상세 프롬프트를 자동 생성 —
  언어 장벽 해소용으로 실전적.
- 2단계 체이닝(1차 생성 → 2차 노드에서 요약)으로 지나치게 긴
  프롬프트를 다듬는 패턴, `context` 출력을 다음 노드에 연결해 대화
  맥락을 유지하는 패턴도 유효.
- `Ollama Vision`: 이미지를 분석해 상세 프롬프트를 자동 작성 —
  설명하기 어려운 몽환적/추상적 이미지의 프롬프트 역산에 유용.
  Llama Vision → Llama Text(요약) → 이미지 생성 3단계 파이프라인이
  VRAM 부담이 크므로 `LayerUtility: Purge VRAM`을 중간에 끼워
  넣는 것을 원본이 권장.

## 11. 문제 해결 팁 (부록 FAQ에서 복원 가능했던 부분)

- **ComfyUI Manager 설치 실패**("This action is not allowed..."): 구
  버전은 `config.ini`의 `security_level`, 최신 버전(2025+)은
  `allow_git_url_install`/`allow_pip_install` 플래그로 제어 방식이
  바뀌었으니 사용 중인 Manager 버전의 실제 설정 항목을 확인할 것.
- **OOM(Out of Memory)**: 해상도를 낮추거나 그래픽카드 VRAM 사용량이
  더 적은 양자화 버전(GGUF/fp8)으로 교체.
- **ReActor 관련 에러**(`insightface` 휠 설치 실패, `basicsr`/
  `future` 모듈 누락, OpenCV 충돌): Python 버전에 정확히 맞는
  `insightface` 휠 재설치, `opencv-python==4.7.0.72`로 다운그레이드
  등 원본이 제시한 해결책들은 여전히 유효한 클래스의 문제이지만,
  ReActor Core 개편 이후에는 애초에 insightface 수동 설치 자체가
  불필요해졌을 가능성이 높으므로 최신 설치 가이드를 먼저 확인.
- **Windows 긴 경로 문제**: `ComfyUI`를 `C:\Users\...\매우\긴\경로`
  대신 `D:\ComfyUI`처럼 짧은 경로에 설치하면 일부 커스텀 노드의
  파일 다운로드/경로 관련 오류가 해결됨.

## 12. 자주 쓰는 단축키

| 단축키 | 기능 |
|---|---|
| Ctrl+Enter | 큐에 생성 추가 |
| Ctrl+Shift+Enter | 현재 큐에 우선 추가 |
| Ctrl+Alt+Enter | 실행 중인 큐 취소 |
| Ctrl+Z / Ctrl+Y | 실행 취소 / 다시 실행 |
| Ctrl+S / Ctrl+O | 워크플로우 저장 / 불러오기 |
| Ctrl+A | 모든 노드 선택 |
| Ctrl+M | 선택 노드 음소거(뮤트) |
| Ctrl+B | 선택 노드 우회(Bypass) |
| Ctrl+G | 선택 노드 그룹화 |
| Ctrl+D | 디폴트 워크플로우 불러오기 |
| Ctrl+C / Ctrl+V | 노드 복사/붙여넣기(외부 연결 미유지) |
| Ctrl+C / Ctrl+Shift+V | 노드 복사/붙여넣기(외부 연결 유지) |
| Alt+드래그 | 노드 드래그 복사 |
| Alt + / Alt − | 캔버스 확대 / 축소 |
| Space + 드래그 | 캔버스 이동 |
| Double-Click(빈 캔버스) | 노드 검색 팔레트 열기 |
| Ctrl+Alt+좌클릭 | 클릭한 슬롯의 모든 연결선 해제 |
| Q / H / R | 큐 표시 / 기록 표시 / 그래프 새로고침 |

macOS는 Ctrl 대신 Cmd로 대체 가능.

## OpenMontage 연동 시 참고

이 책에서 다룬 기법 대부분(LoRA 다중 적용, ControlNet, IP-Adapter,
Inpainting/Outpainting, 업스케일, Wan VACE, FLUX Kontext, Effect
LoRA 등)은 **OpenMontage `comfyui_image`/`comfyui_video`에 번들
워크플로우로 내장되어 있지 않다.** `.agents/skills/comfyui/SKILL.md`
기준 연동 경로는 다음과 같다.

1. 위 절들에서 소개한 노드 구성으로 ComfyUI 캔버스에서 워크플로우를
   직접 만들고 실제 생성까지 검증한다.
2. **ComfyUI의 API 포맷으로 내보낸다** (일반 UI `Save`가 아니라
   API 형식 export — 2번째 "노드/워크플로우 기초" 절 참고). API
   포맷이 아니면 `POST /prompt` 제출이 실패한다.
3. `comfyui_image`/`comfyui_video` 호출 시 `workflow_json` 또는
   `workflow_path` + **필수** `output_node`(최종 저장 노드, 보통
   `SaveImage`/`SaveVideo`/`VHS_VideoCombine` — 여러 개면 프리뷰가
   아닌 최종 결과물 노드를 선택)를 함께 전달한다.
4. LoRA를 쓰는 워크플로우라면 `LoraLoader`/`LoraLoaderModelOnly`
   체인이 이미 그래프 안에 포함돼 있어야 한다 — 현재 툴은 이를
   자동 주입하지 않는다.
5. 재현성을 위해 `workflow_name`, `workflow_model`,
   `workflow_model_stack`(베이스 모델, 양자화, 텍스트 인코더, VAE,
   LoRA와 강도, 샘플러/스케줄러, steps, guidance)을 알고 있는 범위
   내에서 채워 넘긴다. 툴이 최종 워크플로우의 SHA-256 해시를 자동
   기록하므로, 이 해시 + 모델 스택 + seed + 해상도 + 프롬프트가
   재현성 계약이 된다.
6. 커스텀 노드가 없다는 에러가 나면 `data.missing_models[]`(모델
   누락) 또는 ComfyUI Manager의 Install Missing Custom Nodes(노드
   누락)를 먼저 확인하도록 사용자에게 안내한다 — 직접 해결하려 하지
   말 것.
7. 저VRAM(8-12GB) 환경에서는 이 문서의 Wan 2.1 1.3B, LTXV FP8/양자화,
   Hunyuan Video GGUF+VAE Decode(Tiled), FLUX GGUF/NF4 절이 실제로
   쓸 커스텀 워크플로우 후보다. 번들된 WAN 2.2 14B FP8 i2v/t2v는
   16GB급 고품질 프로파일이라는 점을 사용자에게 먼저 알릴 것.
