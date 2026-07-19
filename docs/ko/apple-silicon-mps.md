> 이 문서는 이중 언어 문서입니다. 각 섹션에서 영어 원문이 먼저 나오고, **[한국어]** 표시 아래에 한국어 번역이 이어집니다.

> 원본: docs/apple-silicon-mps.md @ 7cd8fbf4b77ebab41907f87938d83865365cee26

# Apple Silicon (MPS) Support (Apple Silicon (MPS) 지원)

OpenMontage supports Apple Silicon Macs (M1/M2/M3/M4/M5) via PyTorch's
Metal Performance Shaders (MPS) backend. Local GPU tools — video generation,
upscaling, and face restoration — automatically detect and use MPS when
available.

**[한국어]**

OpenMontage는 PyTorch의 Metal Performance Shaders (MPS) 백엔드를 통해 Apple Silicon Mac(M1/M2/M3/M4/M5)을 지원합니다. 로컬 GPU 도구 — 영상 생성, 업스케일링, 얼굴 복원 —는 사용 가능한 경우 MPS를 자동으로 감지하고 사용합니다.

---

## Requirements (요구 사항)

- macOS 12.3 (Monterey) or later
- Apple Silicon Mac (M-series chip)
- Python 3.10+

**[한국어]**

- macOS 12.3 (Monterey) 이상
- Apple Silicon Mac (M 시리즈 칩)
- Python 3.10 이상

---

## Quick Setup (빠른 설정)

```bash
# Enable local generation
export VIDEO_GEN_LOCAL_ENABLED=true

# Install dependencies — MPS support is included in the default torch wheel
uv pip install diffusers transformers accelerate torch pillow requests

# For upscaling and face restoration
uv pip install realesrgan gfpgan
```

**[한국어]**

별도의 CUDA 빌드나 MPS 패키지가 필요 없습니다 — macOS에서 `uv pip install torch`를 실행하면 MPS 지원이 자동으로 포함됩니다.

---

## How It Works (작동 방식)

The `get_torch_device()` helper in `tools/video/_shared.py` detects the best
available device:

**[한국어]**

`tools/video/_shared.py`에 있는 `get_torch_device()` 헬퍼가 가장 좋은 사용 가능한 장치를 감지합니다.

1. **CUDA** (NVIDIA GPU) — used when available; fastest for diffusion models
2. **MPS** (Apple Silicon Metal) — used on M-series Macs; good performance
3. **CPU** — fallback, always available but significantly slower

**[한국어]**

1. **CUDA** (NVIDIA GPU) — 사용 가능한 경우 사용됨; 디퓨전 모델에 가장 빠름
2. **MPS** (Apple Silicon Metal) — M 시리즈 Mac에서 사용됨; 좋은 성능
3. **CPU** — 대체 장치, 항상 사용 가능하지만 상당히 느림

Device selection is automatic. All local GPU tools (`upscale`, `face_restore`,
`ltx_video_local`, `wan_video_local`, etc.) route through this helper.

**[한국어]**

장치 선택은 자동입니다. 모든 로컬 GPU 도구(`upscale`, `face_restore`, `ltx_video_local`, `wan_video_local` 등)가 이 헬퍼를 통해 연결됩니다.

---

## Known Limitations (알려진 제한 사항)

- **VRAM**: Apple Silicon uses unified memory. Models that require >16 GB VRAM
  may not fit on 16 GB Macs. Check the tool's `resource_profile.vram_mb`.
- **bfloat16**: Not supported on MPS. The pipeline automatically uses float16
  on MPS and float32 on CPU.
- **CPU offloading**: `enable_model_cpu_offload()` is CUDA-only. On MPS, the
  pipeline falls back to direct device placement.
- **Half-precision in Real-ESRGAN**: fp16 can produce NaN artifacts on MPS, so
  upscaling automatically uses fp32 on non-CUDA devices.

**[한국어]**

- **VRAM**: Apple Silicon은 통합 메모리를 사용합니다. 16GB 이상 VRAM을 필요로 하는 모델은 16GB Mac에 맞지 않을 수 있습니다. 도구의 `resource_profile.vram_mb`를 확인하십시오.
- **bfloat16**: MPS에서 지원되지 않습니다. 파이프라인은 MPS에서 자동으로 float16을, CPU에서 float32를 사용합니다.
- **CPU 오프로딩**: `enable_model_cpu_offload()`는 CUDA 전용입니다. MPS에서 파이프라인은 직접 장치 배치로 대체됩니다.
- **Real-ESRGAN의 반정밀도**: fp16은 MPS에서 NaN 아티팩트를 생성할 수 있으므로, CUDA가 아닌 장치에서는 업스케일링이 자동으로 fp32를 사용합니다.

---

## Verifying MPS Is Active (MPS 활성 상태 확인)

```python
from tools.video._shared import get_torch_device
print(get_torch_device())  # Should print "mps" on Apple Silicon
```

If this prints `"cpu"` on an Apple Silicon Mac, verify:
- macOS version is 12.3+
- PyTorch is installed (`uv pip install torch`)
- You're running native ARM Python (not Rosetta x86)

**[한국어]**

Apple Silicon Mac에서 `"cpu"`가 출력되면 다음을 확인하십시오:
- macOS 버전이 12.3 이상인지
- PyTorch가 설치되어 있는지 (`uv pip install torch`)
- 네이티브 ARM Python을 실행 중인지 (Rosetta x86이 아닌지)