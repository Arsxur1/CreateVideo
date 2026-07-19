> 이 문서는 이중 언어 문서입니다. 각 섹션에서 영어 원문이 먼저 나오고, **[한국어]** 표시 아래에 한국어 번역이 이어집니다.

> 원본: docs/comfyui-adapter-plan.md @ 7c4bb08890c3ab6b00576496f51071af253a0504

# ComfyUI Provider Adapter for OpenMontage (OpenMontage용 ComfyUI 프로바이더 어댑터)

**RFC: Native ComfyUI backend for image and video generation**

**RFC: 이미지 및 영상 생성을 위한 네이티브 ComfyUI 백엔드**

---

## Motivation (동기)

OpenMontage's local GPU tools (`wan_video`, `hunyuan_video`, `cogvideo_video`,
`local_diffusion`) use HuggingFace `diffusers` directly. This works on x86 +
consumer GPUs but breaks on newer hardware where the PyTorch ecosystem hasn't
caught up:

**[한국어]**
OpenMontage의 로컬 GPU 도구들(`wan_video`, `hunyuan_video`, `cogvideo_video`,
`local_diffusion`)은 HuggingFace `diffusers`를 직접 사용합니다. 이 방식은 x86 +
소비자 GPU에서는 동작하지만, PyTorch 생태계가 아직 따라가지 못하는 최신 하드웨어에서는 문제가 발생합니다:

| Issue | Detail |
|-------|--------|
| **NVIDIA Blackwell (sm_121)** | No stable PyTorch wheels for aarch64 + CUDA 13.0. Requires NGC containers or nightly builds. |
| **Flash Attention** | Does not support sm_121. Must be replaced with SageAttention v3 or native SDPA. |
| **Unified Memory (GB10/DGX Spark)** | `nvidia-smi` cannot report VRAM. Diffusers' memory estimation breaks. |
| **Model format mismatch** | Diffusers expects HF repos. Production deployments use `.safetensors` checkpoints with quantized variants (NVFP4, FP8) that diffusers doesn't natively load. |

**[한국어]**
| Issue | Detail |
|-------|--------|
| **NVIDIA Blackwell (sm_121)** | aarch64 + CUDA 13.0용 안정적인 PyTorch 휠이 없음. NGC 컨테이너나 나이틀리 빌드가 필요함. |
| **Flash Attention** | sm_121을 지원하지 않음. SageAttention v3 또는 네이티브 SDPA로 대체해야 함. |
| **Unified Memory (GB10/DGX Spark)** | `nvidia-smi`가 VRAM을 보고하지 못함. Diffusers의 메모리 추정이 깨짐. |
| **모델 형식 불일치** | Diffusers는 HF 저장소를 기대함. 실제 운영 환경은 diffusers가 기본으로 로드하지 못하는 양자화 변종(NVFP4, FP8)이 있는 `.safetensors` 체크포인트를 사용함. |

ComfyUI already solves all of these. NVIDIA ships official ComfyUI containers
for DGX Spark. The community has optimized workflows for Blackwell (SageAttention,
NVFP4 quantization, LightX2V 4-step LoRAs). Models like WAN 2.2, FLUX 2,
and ACE-Step run reliably through ComfyUI on hardware where diffusers cannot.

**[한국어]**
ComfyUI는 이미 이 모든 문제를 해결합니다. NVIDIA는 DGX Spark용 공식 ComfyUI 컨테이너를 제공합니다. 커뮤니티는 Blackwell용 최적화된 워크플로우를 개발했습니다(SageAttention,
NVFP4 양자화, LightX2V 4-단계 LoRA). WAN 2.2, FLUX 2, ACE-Step 같은 모델은 diffusers가 동작하지 않는 하드웨어에서도 ComfyUI를 통해 안정적으로 실행됩니다.

A ComfyUI adapter gives OpenMontage access to any model ComfyUI supports,
on any hardware ComfyUI runs on, without shipping or maintaining PyTorch builds.

**[한국어]**
ComfyUI 어댑터를 통해 OpenMontage는 PyTorch 빌드를 배포하거나 유지 관리할 필요 없이, ComfyUI가 지원하는 모든 모델에 ComfyUI가 실행 가능한 모든 하드웨어에서 접근할 수 있습니다.

---

## Design (설계)

### Architecture (아키텍처)

```
OpenMontage Agent
    |
    v
video_selector / image_selector
    |
    v
comfyui_video    comfyui_image    (new tools)
    |                |
    v                v
ComfyUI REST API  (POST /prompt, GET /history, GET /view)
    |
    v
GPU (any hardware ComfyUI supports)
```

### Integration model (통합 모델)

Two new `BaseTool` subclasses plus one shared client library:

**[한국어]**
두 개의 새로운 `BaseTool` 서브클래스와 하나의 공유 클라이언트 라이브러리:

```
tools/
  _comfyui/
    __init__.py
    client.py              # Shared ComfyUI REST client
    workflows/             # Bundled workflow templates
      flux2-txt2img.json
      wan22-t2v-4step.json
      wan22-i2v-4step.json
  graphics/
    comfyui_image.py       # capability="image_generation", provider="comfyui"
  video/
    comfyui_video.py       # capability="video_generation", provider="comfyui"
```

### Registry and selector integration (레지스트리 및 셀렉터 통합)

The tools declare `capability` and `provider` as class attributes.
`tool_registry.discover()` picks them up automatically via `pkgutil.walk_packages`.
`video_selector` and `image_selector` find them via `registry.get_by_capability()`.
The only selector change is operation-specific filtering in `video_selector` so
ComfyUI is not selected for `image_to_video` when only the text-to-video bundled
models are installed, or vice versa.

**[한국어]**
도구들은 `capability`와 `provider`를 클래스 속성으로 선언합니다.
`tool_registry.discover()`는 `pkgutil.walk_packages`를 통해 자동으로 이들을 감지합니다.
`video_selector`와 `image_selector`는 `registry.get_by_capability()`를 통해 이들을 찾습니다.
셀렉터의 유일한 변경 사항은 `video_selector`에서의 연산별 필터링으로, text-to-video 번들 모델만 설치된 경우
ComfyUI가 `image_to_video`에 대해 선택되지 않도록 하거나, 그 반대의 경우를 처리합니다.

---

## Shared Client: `tools/_comfyui/client.py` (공유 클라이언트)

Encapsulates the ComfyUI REST API pattern proven in production (used by the
Bard project's Airflow DAGs for thousands of generations):

**[한국어]**
프로덕션에서 검증된 ComfyUI REST API 패턴을 캡슐화합니다(Bard 프로젝트의 Airflow DAG에서 수천 건의 생성에 사용됨):

The endpoint contract was checked against current ComfyUI server documentation
and the April 2026 third-party developer guide:

**[한국어]**
엔드포인트 계약은 현재 ComfyUI 서버 문서와 2026년 4월 타사 개발자 가이드를 기준으로 검증되었습니다:

- Official routes: `POST /prompt`, `GET /history/{prompt_id}`, `GET /view`,
  `POST /upload/image`, `GET /object_info/{node_class}`, `GET /models/{folder}`,
  `GET /system_stats`, and `WS /ws` are documented server routes.
- `/prompt` accepts the workflow in API format under the `prompt` key and
  returns `prompt_id`, `number`, and `node_errors` on validation.
- `/history/{prompt_id}` returns completed node outputs; artifact records include
  `filename`, `subfolder`, and `type`. The client passes all three through to
  `/view` instead of assuming `type=output`.
- Workflows must be exported in ComfyUI API format, not the regular visual
  canvas workflow format.

**[한국어]**
- 공식 경로: `POST /prompt`, `GET /history/{prompt_id}`, `GET /view`,
  `POST /upload/image`, `GET /object_info/{node_class}`, `GET /models/{folder}`,
  `GET /system_stats`, `WS /ws`는 문서화된 서버 경로입니다.
- `/prompt`는 `prompt` 키 아래의 API 형식 워크플로우를 받고 검증 시
  `prompt_id`, `number`, `node_errors`를 반환합니다.
- `/history/{prompt_id}`는 완료된 노드 출력을 반환합니다. 아티팩트 레코드는
  `filename`, `subfolder`, `type`을 포함합니다. 클라이언트는 `type=output`으로 가정하는 대신
  이 세 가지를 모두 `/view`에 전달합니다.
- 워크플로우는 일반적인 시각 캔버스 워크플로우 형식이 아닌 ComfyUI API 형식으로 내보내야 합니다.

References:

**[한국어]**
참고 자료:

- https://docs.comfy.org/development/comfyui-server/comms_routes
- https://www.runflow.io/blog/comfyui-api-developer-guide

```python
class ComfyUIClient:
    """Thin client for the ComfyUI REST API."""

    def __init__(self, server_url: str | None = None):
        self.server_url = server_url or os.environ.get(
            "COMFYUI_SERVER_URL", "http://localhost:8188"
        )

    def is_available(self) -> bool:
        """Health check -- can we reach the server?"""

    def submit(self, workflow: dict) -> str:
        """POST /prompt. Returns prompt_id. Raises on node_errors."""

    def poll(self, prompt_id: str, timeout: int = 600, interval: int = 5) -> dict:
        """GET /history/{prompt_id} until complete. Returns outputs dict."""

    def download(self, filename: str, subfolder: str, dest: Path) -> Path:
        """GET /view?filename=...&type=output. Writes bytes to dest."""

    def upload_image(self, local_path: Path, name: str) -> str:
        """POST /upload/image. Returns server-side filename for LoadImage nodes."""

    def generate(self, workflow: dict, output_node: str, dest: Path,
                 timeout: int = 600) -> Path:
        """Full cycle: submit -> poll -> download. Returns artifact path."""
```

**Why a shared client?** The submit/poll/download cycle is identical across
image and video generation. The only differences are: which workflow template,
which nodes to customize, and which output node to read from.

**[한국어]**
**공유 클라이언트인 이유?** submit/poll/download 사이클은 이미지와 영상 생성 모두에서 동일합니다.
유일한 차이점은 사용할 워크플로우 템플릿, 커스터마이즈할 노드, 읽을 출력 노드뿐입니다.

---

## Tool Specifications (도구 사양)

### `comfyui_image` -- Image Generation (이미지 생성)

| Field | Value |
|-------|-------|
| capability | `image_generation` |
| provider | `comfyui` |
| runtime | `LOCAL_GPU` |
| tier | `GENERATE` |
| stability | `EXPERIMENTAL` |
| capabilities | `text_to_image`, `image_to_image` |
| dependencies | (runtime: ComfyUI server reachable) |
| fallback_tools | `flux_image`, `local_diffusion`, `openai_image` |
| cost | `$0.00` (local compute) |

**Bundled workflow:** `flux2-txt2img.json`

**[한국어]**
**번들 워크플로우:** `flux2-txt2img.json`

Loads FLUX 2 Dev (NVFP4) with Mistral text encoder. Templated nodes:

**[한국어]**
FLUX 2 Dev (NVFP4)를 Mistral 텍스트 인코더와 함께 로드합니다. 템플릿화된 노드:

| Node | Class | Templated field |
|------|-------|-----------------|
| 4 | CLIPTextEncode | `text` (prompt) |
| 6 | EmptyFlux2LatentImage | `width`, `height` |
| 7 | RandomNoise | `noise_seed` |
| 10 | Flux2Scheduler | `steps` |
| 13 | SaveImage | `filename_prefix` |

**Input schema:**

**[한국어]**
**입력 스키마:**

```yaml
prompt:        string    # required
width:         integer   # default 1024
height:        integer   # default 1024
steps:         integer   # default 20
seed:          integer   # optional (random if omitted)
guidance:      number    # default 3.5
output_path:   string    # where to save the image
workflow_json: string    # optional custom workflow; requires output_node
workflow_path: string    # optional path to workflow JSON; requires output_node
output_node:   string    # required for custom workflows
workflow_name: string    # optional custom workflow provenance label
workflow_model: string   # optional custom model/provenance label
workflow_model_stack: [] # optional custom dependency provenance
```

**get_status():** Pings ComfyUI server and checks bundled FLUX model names via
`/object_info`. Returns `AVAILABLE` when the server and bundled model set are
ready, `DEGRADED` when the server is reachable but bundled models are missing,
and `UNAVAILABLE` when the server cannot be reached.

**[한국어]**
**get_status():** ComfyUI 서버에 핑을 보내고 `/object_info`를 통해 번들 FLUX 모델 이름을 확인합니다.
서버와 번들 모델 세트가 준비되면 `AVAILABLE`을, 서버는 접근 가능하지만 번들 모델이 누락되면 `DEGRADED`를,
서버에 접근할 수 없으면 `UNAVAILABLE`을 반환합니다.

**execute() flow:**
1. Deep-copy workflow template
2. Inject prompt, seed, dimensions, steps into templated nodes
3. `client.generate(workflow, output_node="13", dest=output_path)`
4. Return `ToolResult` with artifact path, seed, model info

**[한국어]**
**execute() 흐름:**
1. 워크플로우 템플릿을 깊은 복사
2. 템플릿화된 노드에 프롬프트, 시드, 치수, 단계 주입
3. `client.generate(workflow, output_node="13", dest=output_path)`
4. 아티팩트 경로, 시드, 모델 정보가 포함된 `ToolResult` 반환

For custom workflows, the caller must provide `workflow_json` or `workflow_path`
plus `output_node`. The tool does not assume bundled node IDs for custom
workflows, and provenance is reported as user-supplied unless the caller provides
`workflow_model`. Results also include the final workflow SHA-256 hash and, for
bundled workflows, the known model stack.

**[한국어]**
커스텀 워크플로우의 경우 호출자는 `workflow_json` 또는 `workflow_path`와
함께 `output_node`를 제공해야 합니다. 도구는 커스텀 워크플로우에 대해 번들 노드 ID를 가정하지 않으며,
호출자가 `workflow_model`을 제공하지 않는 한 출처는 사용자 제공으로 보고됩니다.
결과에는 최종 워크플로우 SHA-256 해시와 번들 워크플로우의 경우 알려진 모델 스택도 포함됩니다.

---

### `comfyui_video` -- Video Generation (영상 생성)

| Field | Value |
|-------|-------|
| capability | `video_generation` |
| provider | `comfyui` |
| runtime | `LOCAL_GPU` |
| tier | `GENERATE` |
| stability | `EXPERIMENTAL` |
| capabilities | `text_to_video`, `image_to_video` |
| dependencies | (runtime: ComfyUI server reachable) |
| fallback_tools | `wan_video`, `hunyuan_video`, `ltx_video_local` |
| cost | `$0.00` (local compute) |

**Bundled workflows:**

**[한국어]**
**번들 워크플로우:**

1. **`wan22-i2v-4step.json`** -- Image-to-video (WAN 2.2 14B, fp8, 4-step LightX2V LoRA)
2. **`wan22-t2v-4step.json`** -- Text-to-video (WAN 2.2 14B, fp8, 4-step LightX2V LoRA)

These bundled WAN 2.2 14B FP8 workflows are the high-quality profile and
recommend roughly 16GB VRAM. That is not a ComfyUI-wide requirement. The
`comfyui_video` tool's top-level `resource_profile` is an 8GB provider floor so
preflight does not imply ComfyUI itself requires 16GB. Low-VRAM users should use
custom workflows such as Wan 2.1 1.3B, LTX-Video/LTXV FP8 or quantized graphs,
or Wan 2.2 GGUF/quantized community workflows, with shorter frame counts and
lower resolutions as needed.

**[한국어]**
이 번들 WAN 2.2 14B FP8 워크플로우는 고품질 프로필로 약 16GB VRAM을 권장합니다.
이것은 ComfyUI 전체 요구사항이 아닙니다. `comfyui_video` 도구의 최상위 `resource_profile`은
8GB 프로바이더 기준이므로 사전 점검이 ComfyUI 자체에 16GB가 필요하다는 의미는 아닙니다.
낮은 VRAM 사용자는 필요에 따라 더 짧은 프레임 수와 낮은 해상도로 Wan 2.1 1.3B, LTX-Video/LTXV FP8
또는 양자화된 그래프, Wan 2.2 GGUF/양자화된 커뮤니티 워크플로우 같은 커스텀 워크플로우를 사용해야 합니다.

**I2V workflow -- templated nodes:**

**[한국어]**
**I2V 워크플로우 -- 템플릿화된 노드:**

| Node | Class | Templated field |
|------|-------|-----------------|
| 93 | CLIPTextEncode | `text` (positive prompt) |
| 97 | LoadImage | `image` (server filename from upload) |
| 98 | WanImageToVideo | `width`, `height`, `length` |
| 86 | KSamplerAdvanced | `noise_seed` |
| 108 | SaveVideo | `filename_prefix` |

**Input schema:**

**[한국어]**
**입력 스키마:**

```yaml
prompt:               string    # required
operation:            string    # "text_to_video" | "image_to_video" (default: t2v)
reference_image_path: string    # local path (for i2v)
reference_image_url:  string    # URL (for i2v, downloaded first)
width:                integer   # default 640
height:               integer   # default 640
num_frames:           integer   # default 81 (5s at 16fps)
seed:                 integer   # optional
output_path:          string    # where to save the video
workflow_json:        string    # optional custom workflow; requires output_node
workflow_path:        string    # optional path to workflow JSON; requires output_node
output_node:          string    # required for custom workflows
workflow_name:        string    # optional custom workflow provenance label
workflow_model:       string    # optional custom model/provenance label
workflow_model_stack: []        # optional custom dependency provenance
```

**execute() flow (i2v):**
1. Upload reference image via `client.upload_image()`
2. Deep-copy i2v workflow template
3. Inject prompt, uploaded image name, seed, dimensions
4. `client.generate(workflow, output_node="108", dest=output_path, timeout=900)`
5. Return `ToolResult`

**[한국어]**
**execute() 흐름 (i2v):**
1. `client.upload_image()`를 통해 참조 이미지 업로드
2. i2v 워크플로우 템플릿 깊은 복사
3. 프롬프트, 업로드된 이미지 이름, 시드, 치수 주입
4. `client.generate(workflow, output_node="108", dest=output_path, timeout=900)`
5. `ToolResult` 반환

**execute() flow (t2v):**
1. Deep-copy t2v workflow template
2. Inject prompt, seed, dimensions
3. `client.generate(workflow, output_node="16", dest=output_path, timeout=900)`
4. Return `ToolResult`

**[한국어]**
**execute() 흐름 (t2v):**
1. t2v 워크플로우 템플릿 깊은 복사
2. 프롬프트, 시드, 치수 주입
3. `client.generate(workflow, output_node="16", dest=output_path, timeout=900)`
4. `ToolResult` 반환

`comfyui_video` publishes `operation_statuses` in `get_info()` and implements
`is_operation_available(operation)` for selector routing. This keeps partial
ComfyUI installs useful for the installed mode without advertising unavailable
operation modes as ready. `video_selector` also applies this readiness check
when `operation="rank"` by using `target_operation`, so preflight rankings do
not promote ComfyUI for an operation whose bundled models are missing.

**[한국어]**
`comfyui_video`는 `get_info()`에서 `operation_statuses`를 게시하고 셀렉터 라우팅을 위해
`is_operation_available(operation)`를 구현합니다. 이렇게 하면 불완전한 ComfyUI 설치가
사용 가능한 모드에 대해서는 유용하면서 사용 불가능한 연산 모드를 준비된 것으로 광고하지 않습니다.
`video_selector`도 `operation="rank"`일 때 `target_operation`을 사용하여 이 준비 상태 확인을 적용하므로,
사전 점검 순위가 번들 모델이 누락된 연산에 대해 ComfyUI를 승격시키지 않습니다.

---

### `comfyui_music` -- Music Generation (not shipped) (음악 생성 (배포되지 않음))

We explored adding a `comfyui_music` tool using the ACE-Step 3.5B model.
The model runs well in ComfyUI, but the ComfyUI node interface for
ACE-Step is not standardized -- there are multiple custom node packs with
different class names (`AceStepModelLoader` vs native `TextEncodeAceStepAudio`,
etc.).  Shipping a workflow that only works with one specific custom node
pack would break for most users.

**[한국어]**
ACE-Step 3.5B 모델을 사용하는 `comfyui_music` 도구 추가를 타색했습니다.
모델은 ComfyUI에서 잘 실행되지만 ACE-Step용 ComfyUI 노드 인터페이스가 표준화되지 않았습니다.
서로 다른 클래스 이름을 가진 여러 커스텀 노드 팩이 있습니다(`AceStepModelLoader` vs 네이티브 `TextEncodeAceStepAudio` 등).
특정 커스텀 노드 팩에서만 작동하는 워크플로우를 배포하면 대부분의 사용자에게서 작동하지 않을 것입니다.

**Future path:** ACE-Step support should be revisited once OpenMontage decides
the music-generation routing shape and a portable ComfyUI audio workflow
contract. Current image/video workflow overrides are intentionally scoped to
image and video artifacts, not arbitrary audio workflows.

**[한국어]**
**향후 경로:** ACE-Step 지원은 OpenMontage가 음악 생성 라우팅 형태와 이식 가능한 ComfyUI 오디오 워크플로우 계약을 결정한 후 재검토해야 합니다. 현재 이미지/영상 워크플로우 재정의는 의도적으로 이미지 및 영상 아티팩트로 범위가 지정되어 있으며, 임의의 오디오 워크플로우가 아닙니다.

---

## Workflow Override Mechanism (워크플로우 재정의 메커니즘)

The image and video tools accept either `workflow_json` or `workflow_path`.
When provided, the custom workflow replaces the bundled template entirely and
the caller must also provide `output_node`. This stricter contract is required
because community workflows use arbitrary node IDs.

**[한국어]**
이미지 및 영상 도구는 `workflow_json` 또는 `workflow_path`를 받습니다.
제공될 경우 커스텀 워크플로우가 번들 템플릿을 완전히 대체하며
호출자도 `output_node`를 제공해야 합니다. 커뮤니티 워크플로우는 임의 노드 ID를 사용하므로
이 더 엄격한 계약이 필요합니다.

- Using newer model checkpoints without code changes
- Custom sampling strategies (different schedulers, step counts, LoRAs)
- Community workflows dropped in as-is
- A/B testing different generation approaches

**[한국어]**
- 코드 변경 없이 최신 모델 체크포인트 사용
- 커스텀 샘플링 전략(서로 다른 스케줄러, 단계 수, LoRA)
- 커뮤니티 워크플로우를 있는 그대로 추가
- 서로 다른 생성 접근 방식 A/B 테스트

The agent can also read workflow files from `tools/_comfyui/workflows/` and
modify them programmatically before passing to `execute()`.

**[한국어]**
에이전트는 `tools/_comfyui/workflows/`에서 워크플로우 파일을 읽고
`execute()`에 전달하기 전에 프로그래밍 방식으로 수정할 수도 있습니다.

Custom workflow result metadata reports `workflow_provenance.source` as
`user_supplied` and uses `workflow_model`, `model`, or `workflow_name` as the
model label when provided. If no custom label is supplied, the model is reported
as `custom-comfyui-workflow` instead of one of the bundled model names. The
provenance payload also records `workflow_hash_sha256`. For user-supplied
workflows, callers should provide `workflow_model_stack` with base model, text
encoder, VAE, LoRAs and strengths, scheduler, steps, and guidance when known.

**[한국어]**
커스텀 워크플로우 결과 메타데이터는 `workflow_provenance.source`를 `user_supplied`로 보고하고
제공될 경우 `workflow_model`, `model`, 또는 `workflow_name`을 모델 라벨로 사용합니다.
커스텀 라벨이 제공되지 않으면 모델은 번들 모델 이름 중 하나가 아닌 `custom-comfyui-workflow`로 보고됩니다.
출처 페이로드는 `workflow_hash_sha256`도 기록합니다. 사용자 제공 워크플로우의 경우 호출자는
알고 있는 경우 기본 모델, 텍스트 인코더, VAE, LoRA 및 강도, 스케줄러, 단계, 안내를 포함하는
`workflow_model_stack`을 제공해야 합니다.

---

## Agent Skill and Setup Contract (에이전트 스킬 및 설정 계약)

Both ComfyUI tools advertise the Layer 3 `comfyui` skill. Agents must read
`.agents/skills/comfyui/SKILL.md` before calling either tool so they know how to
load community workflows, identify output nodes, handle LoRA loader chains, and
record custom workflow provenance.

**[한국어]**
두 ComfyUI 도구는 Layer 3 `comfyui` 스킬을 광고합니다. 에이전트는
커뮤니티 워크플로우 로드, 출력 노드 식별, LoRA 로더 체인 처리, 커스텀 워크플로우 출처 기록 방법을
알기 위해 어느 도구를 호출하기 전에 `.agents/skills/comfyui/SKILL.md`를 읽어야 합니다.

Unavailable ComfyUI tools expose a structured `setup_offer` in `get_info()`,
`provider_menu()`, and `provider_menu_summary().setup_offers[]`:

**[한국어]**
사용 불가능한 ComfyUI 도구는 `get_info()`, `provider_menu()`,
`provider_menu_summary().setup_offers[]`에서 구조화된 `setup_offer`를 노출합니다:

```yaml
kind: local_server
env_var: COMFYUI_SERVER_URL
default_url: http://localhost:8188
health_check: GET /system_stats
```

When bundled models are missing, the tool returns a machine-readable
`data.missing_models[]` list with filename, role, destination hint, and download
URL when OpenMontage knows the canonical source. Agents should surface that
payload rather than parsing prose error text.

**[한국어]**
번들 모델이 누락되면 도구는 파일 이름, 역할, 대상 힌트, OpenMontage가 정식 소스를 알고 있는 경우 다운로드 URL이 포함된
기계 읽기 가능한 `data.missing_models[]` 목록을 반환합니다. 에이전트는 산문 오류 텍스트를 구문 분석하는 대신
이 페이로드를 표시해야 합니다.

---

## Configuration (구성)

**Environment variables:**

**[한국어]**
**환경 변수:**

```bash
# .env
COMFYUI_SERVER_URL=http://localhost:8188    # ComfyUI API endpoint
COMFYUI_POLL_INTERVAL=5                     # seconds between status checks
COMFYUI_POLL_TIMEOUT=600                    # max wait for image gen
COMFYUI_VIDEO_TIMEOUT=900                   # max wait for video gen
```

**For Docker Compose setups** (ComfyUI in a container):

**[한국어]**
**Docker Compose 설정용** (컨테이너의 ComfyUI):

```bash
COMFYUI_SERVER_URL=http://host.docker.internal:8188
# or
COMFYUI_SERVER_URL=http://comfyui:8188      # if on same docker network
```

---

## Provider Selection Behavior (프로바이더 선택 동작)

When the adapter is available, selectors will rank it alongside other providers
using OpenMontage's 7-dimension scoring:

**[한국어]**
어댑터를 사용할 수 있을 때 셀렉터는 OpenMontage의 7차원 점수 매기기를 사용하여
다른 프로바이더와 함께 순위를 매깁니다:

| Dimension | ComfyUI score | Rationale |
|-----------|---------------|-----------|
| Task fit | High | Supports t2i, i2v, t2v |
| Quality | High | Latest models (FLUX 2, WAN 2.2 14B) |
| Control | Highest | Full workflow customization |
| Reliability | High | Proven in production |
| Cost | $0 | Local compute |
| Latency | Medium | GPU-bound, no network round-trip |
| Continuity | High | Deterministic with seeds |

**[한국어]**
| Dimension | ComfyUI 점수 | 근거 |
|-----------|---------------|------|
| 작업 적합성 | 높음 | t2i, i2v, t2v 지원 |
| 품질 | 높음 | 최신 모델 (FLUX 2, WAN 2.2 14B) |
| 제어 | 최고 | 완전한 워크플로우 커스터마이제이션 |
| 신뢰성 | 높음 | 프로덕션에서 검증됨 |
| 비용 | $0 | 로컬 컴퓨팅 |
| 지연 시간 | 중간 | GPU 종속, 네트워크 왕복 없음 |
| 연속성 | 높음 | 시드로 결정론적 |

When ComfyUI is unavailable (server down), selectors fall through to other
available providers. When only one video operation is configured, `video_selector`
uses the tool's operation-specific readiness to avoid selecting ComfyUI for the
missing mode.

**[한국어]**
ComfyUI를 사용할 수 없을 때(서버 다운) 셀렉터는 다른 사용 가능한 프로바이저로 넘어갑니다.
하나의 영상 연산만 구성된 경우 `video_selector`는 누락된 모드에 대해 ComfyUI를 선택하지 않도록
도구의 연산별 준비 상태를 사용합니다.

---

## What This Unlocks (이것이 가능하게 하는 것)

### Immediate (with existing models) (즉시 (기존 모델로))

- **FLUX 2 Dev NVFP4** image generation -- Blackwell-optimized, ~60s per image
- **WAN 2.2 14B FP8 high-quality profile** i2v with 4-step acceleration -- ~3.5 min per 5s clip, about 16GB VRAM recommended
- **WAN 2.2 14B FP8 high-quality profile** t2v (models downloaded, workflow included), about 16GB VRAM recommended

**[한국어]**
- **FLUX 2 Dev NVFP4** 이미지 생성 -- Blackwell 최적화, 이미지당 약 60초
- **WAN 2.2 14B FP8 고품질 프로필** 4-단계 가속 i2v -- 5초 클립당 약 3.5분, 약 16GB VRAM 권장
- **WAN 2.2 14B FP8 고품질 프로필** t2v (모델 다운로드됨, 워크플로우 포함), 약 16GB VRAM 권장

### Low-VRAM profile (낮은 VRAM 프로필)

ComfyUI can still be useful on 8GB-12GB GPUs when the user supplies an
appropriate `workflow_json` or `workflow_path`. Good candidates include:

**[한국어]**
ComfyUI는 사용자가 적절한 `workflow_json` 또는 `workflow_path`를 제공하면
8GB-12GB GPU에서도 여전히 유용할 수 있습니다. 좋은 후보는 다음과 같습니다:

- Wan 2.1 1.3B workflows for lower-memory text-to-video.
- LTX-Video/LTXV FP8 or quantized workflows for fast short clips.
- Wan 2.2 GGUF/quantized community workflows at lower resolution and frame count.

**[한국어]**
- 낮은 메모리용 text-to-video용 Wan 2.1 1.3B 워크플로우
- 빠른 짧은 클립용 LTX-Video/LTXV FP8 또는 양자화 워크플로우
- 더 낮은 해상도와 프레임 수의 Wan 2.2 GGUF/양자화 커뮤니티 워크플로우

OpenMontage should treat those as custom workflow profiles until a blessed
low-VRAM workflow is bundled. For custom workflows, resource requirements are
workflow-supplied rather than inferred from the bundled WAN 2.2 14B profile.

**[한국어]**
OpenMontage는 축복받은 낮은 VRAM 워크플로우가 번들될 때까지 이것들을 커스텀 워크플로우 프로필로 처리해야 합니다.
커스텀 워크플로우의 경우 리소스 요구사항은 번들 WAN 2.2 14B 프로필에서 추론하는 것이 아니라 워크플로우에서 제공합니다.

### Future (add models to ComfyUI, no code changes to OpenMontage) (향후 (ComfyUI에 모델 추가, OpenMontage 코드 변경 없음))

- Newer checkpoints (WAN 3.x, FLUX 3, etc.) -- just update workflow JSON
- ControlNet, IP-Adapter, AnimateDiff -- supported via ComfyUI custom nodes
- Upscaling, inpainting, outpainting -- ComfyUI nodes exist
- Any model the ComfyUI ecosystem supports

**[한국어]**
- 최신 체크포인트 (WAN 3.x, FLUX 3 등) -- 워크플로우 JSON만 업데이트
- ControlNet, IP-Adapter, AnimateDiff -- ComfyUI 커스텀 노드로 지원
- 업스케일링, 인페인팅, 아웃페인팅 -- ComfyUI 노드 존재
- ComfyUI 생태계가 지원하는 모든 모델

### Hardware portability (하드웨어 이식성)

The same adapter works on:
- NVIDIA DGX Spark (GB10, aarch64, CUDA 13.0)
- Consumer GPUs (RTX 3090/4090, x86)
- Cloud instances (A100, H100)
- Multi-GPU setups (ComfyUI handles device placement)

**[한국어]**
동일한 어댑터는 다음 환경에서 작동합니다:
- NVIDIA DGX Spark (GB10, aarch64, CUDA 13.0)
- 소비자 GPU (RTX 3090/4090, x86)
- 클라우드 인스턴스 (A100, H100)
- 멀티 GPU 설정 (ComfyUI가 디바이스 배치를 처리)

No PyTorch version pinning, no architecture-specific wheels, no CUDA
compatibility matrices. ComfyUI is the abstraction layer.

**[한국어]**
PyTorch 버전 고정, 아키텍처별 휠, CUDA 호환성 매트릭스 없음.
ComfyUI가 추상화 계층입니다.

---

## Implementation Scope (구현 범위)

| Component | Files | Estimated size |
|-----------|-------|----------------|
| Shared client | `tools/_comfyui/client.py` | ~180 lines |
| Shared metadata | `tools/_comfyui/metadata.py` | setup, model stack, provenance helpers |
| Image tool | `tools/graphics/comfyui_image.py` | ~140 lines |
| Video tool | `tools/video/comfyui_video.py` | ~190 lines |
| Layer 3 skill | `.agents/skills/comfyui/SKILL.md` | usage contract |
| Registry summary | `tools/tool_registry.py` | setup offer surfacing |
| Selector readiness filter | `tools/video/video_selector.py` | small operation-readiness check |
| Workflow templates | `tools/_comfyui/workflows/*.json` | 3 files |
| Tests | `tests/contracts/test_comfyui_tools.py` | ~200 lines |
| Docs | `docs/comfyui-adapter-plan.md` | This file |

**[한국어]**
| Component | Files | 예상 크기 |
|-----------|-------|----------|
| 공유 클라이언트 | `tools/_comfyui/client.py` | ~180줄 |
| 공유 메타데이터 | `tools/_comfyui/metadata.py` | setup, 모델 스택, 출처 도우미 |
| 이미지 도구 | `tools/graphics/comfyui_image.py` | ~140줄 |
| 영상 도구 | `tools/video/comfyui_video.py` | ~190줄 |
| Layer 3 스킬 | `.agents/skills/comfyui/SKILL.md` | 사용 계약 |
| 레지스트리 요약 | `tools/tool_registry.py` | setup offer 표시 |
| 셀렉터 준비 상태 필터 | `tools/video/video_selector.py` | 작은 연산 준비 상태 확인 |
| 워크플로우 템플릿 | `tools/_comfyui/workflows/*.json` | 3개 파일 |
| 테스트 | `tests/contracts/test_comfyui_tools.py` | ~200줄 |
| 문서 | `docs/comfyui-adapter-plan.md` | 이 파일 |

**Total:** ~500 lines of Python + 3 workflow JSONs.

**[한국어]**
**전체:** Python ~500줄 + 워크플로우 JSON 3개.

No changes to: `base_tool.py`, existing non-ComfyUI generation providers, any
pipeline definition, or any schema.

**[한국어]**
변경 없음: `base_tool.py`, 기존 비ComfyUI 생성 프로바이더, 파이프라인 정의, 스키마.

---

## Open Questions (열린 질문)

1. **Workflow versioning:** Should workflow JSONs live in the repo or be
   user-provided via a config directory? Bundling gives reproducibility;
   external gives flexibility.

2. **Async generation:** ComfyUI supports websocket connections for real-time
   progress. Worth implementing for long video generations, or is polling
   sufficient?

3. **Multi-server:** Should the adapter support multiple ComfyUI instances
   (e.g., one for images, one for video) via per-capability URLs?

4. **Music generation:** ACE-Step works in ComfyUI but OpenMontage needs a
   dedicated music-generation routing contract before adding `comfyui_music`.
   The follow-up should decide selector integration, audio artifact schemas, and
   a portable workflow/output-node contract rather than treating music as a
   hidden image/video workflow override.

**[한국어]**
1. **워크플로우 버전 관리:** 워크플로우 JSON을 저장소에 두거나 구성 디렉터리를 통해 사용자 제공으로 해야 할까요? 번들링은 재현성을 제공하고 외부는 유연성을 제공합니다.

2. **비동기 생성:** ComfyUI는 실시간 진행 상황용 웹소켓 연결을 지원합니다. 긴 영상 생성에 구현할 가치가 있나요, 아니면 폴링으로 충분한가요?

3. **멀티 서버:** 어댑터가 기능별 URL을 통해 여러 ComfyUI 인스턴스(예: 이미지용 하나, 영상용 하나)를 지원해야 하나요?

4. **음악 생성:** ACE-Step은 ComfyUI에서 작동하지만 OpenMontage는 `comfyui_music`을 추가하기 전에 전용 음악 생성 라우팅 계약이 필요합니다. 후속 작업은 음악을 숨겨진 이미지/영상 워크플로우 재정의로 처리하는 대신 셀렉터 통합, 오디오 아티팩트 스키마, 이식 가능한 워크플로우/출력 노드 계약을 결정해야 합니다.