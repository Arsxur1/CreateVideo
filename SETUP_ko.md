# OpenMontage 한국어 실행 가이드

이 가이드는 개발자가 Windows(PowerShell) 및 macOS/Linux(bash) 환경에서 파이썬 가상환경(venv) 생성부터 의존성 설치(`pip install`)까지 순서대로 따라하여 OpenMontage 프로젝트를 실행할 수 있도록 안내합니다. 본문의 모든 명령·버전·패키지 이름·경로·환경변수는 프로젝트 파일(`setup.py`, `requirements*.txt`, `Makefile`, `README_ko.md`, `.env.example`)을 근거로 작성되었으며, 추측 내용은 포함하지 않습니다.

> 한 줄 요약: `make setup` 한 번이면 가상환경 생성 → 파이썬 의존성 설치 → Remotion/HyperFrames 런타임 준비 → `.env` 생성까지 끝납니다. `make`가 없거나 단계별로 직접 제어하고 싶다면 아래 1~5단계를 따르세요.

> 영문 원본 구조가 필요한 경우 [README_ko.md](README_ko.md)의 이중 언어 규약을 참고하세요.

---

## 사전 준비

OpenMontage는 파이썬 패키지 매니저로 **pip + setuptools**를 사용합니다. 프로젝트 루트에 `pyproject.toml`·`Pipfile`·`poetry.lock`·`uv.lock`·`pdm.lock`·`setup.cfg`·`environment.yml`이 모두 없고, `setup.py` + `requirements.txt` / `requirements-gpu.txt` / `requirements-dev.txt`만 존재합니다. 따라서 모든 설치는 `pip install -r requirements*.txt` 형태로 수행합니다. (`uv`는 Makefile이 가상환경 생성 시에만 선택적으로 사용하며 패키지 설치에는 쓰지 않습니다.)

| 항목 | 요구 버전 | 비고 |
|---|---|---|
| Python | **3.10+** | `.python-version` 파일이 `3.10`으로 고정, `setup.py`의 `python_requires=">=3.10"`, README “Python 3.10+”와 일치 |
| FFmpeg | 안정 버전 | 영상 인코딩에 필수. 코덱 기본값은 `libx264` |
| Node.js | **18+ (권장 22+ LTS)** | `remotion-composer` 의존성 설치 및 Remotion 구동에 필요. HyperFrames 합성 엔진은 Node.js 22+를 요구하므로 최신 LTS 권장 |
| npm / npx | Node.js에 포함 | Remotion/HyperFrames 실행(`npx remotion render`, `npx hyperframes`)에 사용 |
| (선택) NVIDIA GPU | — | 로컬 영상/이미지 생성 모델(WAN 2.1, Hunyuan, CogVideo, LTX-Video, Stable Diffusion) 사용 시 |
| (선택) `make` | — | Makefile 래퍼 사용 시. Windows는 기본 설치되지 않으므로 Git Bash/WSL 또는 별도 설치 필요 |

설치 전 각 도구가 PATH에 잡혀 있는지 확인합니다.

다음은 Windows PowerShell에서 버전을 확인하는 명령입니다.

```powershell
py -3 --version
ffmpeg -version
node --version
npm --version
```

다음은 macOS/Linux(bash)에서 버전을 확인하는 명령입니다.

```bash
python3 --version
ffmpeg -version
node --version
npm --version
```

> Windows에서 FFmpeg가 없으면 `winget install FFmpeg`로 설치할 수 있고, macOS는 `brew install ffmpeg`, Linux는 `sudo apt install ffmpeg`를 사용합니다.

> 작업 디렉터리는 프로젝트 루트(예: `D:\ysj\OpenMontage`)로 이동한 상태에서 아래 명령들을 실행한다고 가정합니다. 경로에 한글이나 공백이 있을 수 있으므로 따옴표 사용을 권장합니다.

---

## 1. 가상환경 생성

프로젝트 의존성을 시스템 파이썬과 분리하기 위해 `.venv` 가상환경을 생성합니다. Python 3.10 이상이 설치되어 있어야 합니다.

다음은 Windows PowerShell에서 가상환경을 생성하는 명령입니다(`py -3` 런처 사용).

```powershell
py -3 -m venv .venv
```

다음은 macOS/Linux(bash)에서 가상환경을 생성하는 명령입니다.

```bash
python3 -m venv .venv
```

> Makefile은 `uv`가 감지되면 `uv venv --python 3.10 .venv`으로 가상환경을 만들고, 없으면 `python -m venv`로 폴백합니다. 본 가이드는 표준 `venv`를 기준으로 합니다. 이미 `.venv\Scripts\python.exe`(Windows) 또는 `.venv/bin/python`(macOS, Linux)이 존재하면 이 단계는 건너뛰어도 됩니다.

---

## 2. 가상환경 활성화

생성한 `.venv`를 활성화합니다. 이후의 모든 `pip install` / `python` 명령은 활성화된 가상환경 안에서 실행합니다.

다음은 Windows PowerShell에서 활성화하는 명령입니다.

```powershell
.\.venv\Scripts\Activate.ps1
```

다음은 Windows CMD에서 활성화하는 명령입니다.

```cmd
.venv\Scripts\activate.bat
```

다음은 macOS/Linux(bash)에서 활성화하는 명령입니다.

```bash
source .venv/bin/activate
```

> PowerShell에서 `Activate.ps1` 실행이 스크립트 실행 정책으로 차단되면 [문제 해결](#문제-해결troubleshooting)을 참고하세요.

---

## 3. pip 업그레이드

의존성 설치 전 pip를 최신으로 유지합니다.

다음은 pip를 업그레이드하는 명령입니다(모든 플랫폼 공통).

```powershell
python -m pip install --upgrade pip
```

---

## 4. 의존성 설치

### 4-1. 코어 의존성 (필수)

프로젝트의 정규 설치 경로는 `requirements.txt`입니다. 이 파일에는 `pyyaml>=6.0`, `pydantic>=2.0`, `jsonschema>=4.20`, `python-dotenv>=1.0`, `Pillow>=10.0`, `numpy>=1.24`, `requests>=2.31`, `google-auth>=2.0`, `google-genai>=1.0.0`, `openai>=2.44.0`, `fastapi>=0.110`, `uvicorn>=0.29`, `watchfiles>=0.21`이 포함되어 있습니다(뒤의 세 패키지는 로컬 Backlot 스토리보드 보드 서버용).

다음은 코어 의존성을 설치하는 명령입니다.

```powershell
python -m pip install -r requirements.txt
```

> 주의: `setup.py`의 `install_requires`는 `requirements.txt`의 진부분집합입니다(`google-auth`, `numpy`, `fastapi`, `uvicorn`, `watchfiles`가 빠져 있음). 따라서 `pip install -e .`만 실행하면 런타임 import가 실패할 수 있으므로, 반드시 위 `requirements.txt` 설치가 기본이 되어야 합니다.

### 4-2. (선택) GPU 의존성

NVIDIA GPU로 로컬 영상/이미지 생성 모델을 구동할 때 추가합니다. `requirements-gpu.txt`는 `torch>=2.0`, `torchaudio>=2.0`, `torchvision>=0.15`를 포함하며, 파일 헤더에 “Install these in addition to requirements.txt when GPU is available”라고 명시되어 있습니다.

다음은 GPU 의존성을 추가 설치하는 명령입니다. **반드시 4-1의 코어 설치 이후에 실행**합니다.

```powershell
python -m pip install -r requirements-gpu.txt
```

> 주의: `requirements-gpu.txt`에는 `-r requirements.txt` 줄이 없으므로 코어와 별도로 먼저 코어를 설치해야 합니다. 또한 CUDA 버전에 맞는 PyTorch 인덱스(`--index-url https://download.pytorch.org/whl/cuXXX`) 사용 여부는 파일에 명시되어 있지 않으므로, 로컬 CUDA 환경에 맞춰 별도로 지정해야 합니다.

**로컬 영상 생성(diffusers 기반)을 사용할 경우 추가 패키지**

`.env.example`에 `VIDEO_GEN_LOCAL_ENABLED=true` 시 “needs GPU + diffusers”라고 명시되어 있습니다. 즉 WAN 2.1/Hunyuan/CogVideo/LTX-Video 같은 diffusers 기반 로컬 모델을 구동하려면 위 PyTorch 설치 다음에 `diffusers`, `transformers`, `accelerate`를 추가로 설치해야 합니다. 이 패키지 세트는 Makefile의 `install-gpu` 타깃(Makefile: `$(PIP) install diffusers transformers accelerate`)이 `requirements-gpu.txt` 직후에 수행하는 것과 동일합니다. 수동 pip 경로에서 이 단계를 빠뜨리면 `VIDEO_GEN_LOCAL_ENABLED=true`로 로컬 영상 생성을 켤 때 런타임에 모듈 import가 실패합니다.

다음은 diffusers 계열 런타임 패키지를 추가 설치하는 명령입니다(위 `requirements-gpu.txt` 설치 직후).

```powershell
python -m pip install diffusers transformers accelerate
```

> 요약: Makefile `make install-gpu` 한 번에 해당하는 수동 절차는 `pip install -r requirements-gpu.txt` → `pip install diffusers transformers accelerate` 두 단계입니다.

### 4-3. (선택) 개발 의존성

테스트/개발 도구를 추가합니다. `requirements-dev.txt`는 `-r requirements.txt` 줄을 포함하므로 코어 패키지를 함께 설치합니다. `pytest>=8.0`, `pytest-asyncio>=0.23`, `httpx2>=2.0`을 포함합니다.

다음은 개발 의존성을 설치하는 명령입니다.

```powershell
python -m pip install -r requirements-dev.txt
```

> 주의: `requirements-dev.txt`에 `httpx2>=2.0`이 그대로 적혀 있습니다. 이는 PyPI의 `httpx` 오타로 보이나 파일을 있는 그대로 인용합니다. `pip install httpx2` 시 존재하지 않는 패키지일 수 있으니 사용자 확인이 필요합니다([문제 해결](#문제-해결troubleshooting) 참고).

### 4-4. (선택) 로컬 TTS — piper-tts

로컬 음성 합성(piper-tts)을 추가합니다. Makefile은 이 설치가 실패해도 `[skip]` 처리하고 클라우드 TTS로 폴백하므로, 실패는 에러가 아닙니다.

다음은 piper-tts를 설치하는 명령입니다.

```powershell
python -m pip install piper-tts
```

### 4-5. (선택) openmontage 패키지 에디터블 설치

`setup.py`(`name='openmontage'`, `version='0.1.0'`, `python_requires='>=3.10'`)를 에디터블 모드로 설치합니다. 단, `setup.py`에 `extras_require`가 정의되어 있지 않으므로 `pip install -e ".[gpu,dev]"` 형태는 이 프로젝트에 유효하지 않고 **오직 bare `-e .`만 유효**합니다. 또한 이 설치는 `requirements.txt`를 대체하지 않는 보조 설치입니다.

다음은 패키지 자체를 에디터블 설치하는 명령입니다(4-1 이후 보조용).

```powershell
pip install -e .
```

### 4-6. Node.js 서브프로젝트 — remotion-composer

Remotion 합성 런타임의 의존성을 설치합니다. 이 서브프로젝트는 별도의 `package.json`을 가지며 파이썬 의존성이 아닙니다.

다음은 Windows PowerShell에서 remotion-composer 의존성을 설치하는 명령입니다.

```powershell
cd remotion-composer
npm install
cd ..
```

다음은 macOS/Linux(bash)에서 동일하게 설치하는 명령입니다.

```bash
cd remotion-composer && npm install && cd ..
```

> Windows에서 `npm install`이 `ERR_INVALID_ARG_TYPE`로 실패하면 `npx --yes npm install`을 대신 사용하세요.

### 4-7. (선택) HyperFrames 런타임 캐시 웜

HyperFrames 합성 엔진은 첫 렌더 시 `npx hyperframes`로 패키지를 가져오므로, 미리 캐시를 웜해두면 첫 렌더의 30~60초 cold-fetch 페널티를 피할 수 있습니다(Makefile `setup` 타깃이 자동 수행하는 단계). 설치 단계에서 미리 웜해두려면 아래 명령을 실행합니다.

```powershell
npx --yes hyperframes --version
```

다음은 macOS/Linux(bash)에서 동일하게 캐시를 웜하는 명령입니다.

```bash
npx --yes hyperframes --version
```

> 실패해도 에러가 아닙니다. Makefile은 “offline or npm unavailable; first render will fetch on demand”로 `[skip]` 처리하며, 첫 렌더 시 필요시 자동으로 가져옵니다. 런타임 전체 검증은 `make hyperframes-doctor`를 사용하세요.

---

## 5. 환경변수 설정

`.env.example`을 `.env`로 복사합니다. `.env.example`에 “Copy this to .env and fill in your keys”라고 명시되어 있으며, Makefile의 `setup` 타깃이 `.env`가 없을 때 자동 복사합니다. 수동 설치 흐름에서는 아래 명령으로 복사합니다.

다음은 Windows PowerShell에서 `.env`를 생성하는 명령입니다.

```powershell
Copy-Item .env.example .env
```

다음은 macOS/Linux(bash)에서 `.env`를 생성하는 명령입니다.

```bash
cp .env.example .env
```

> 핵심: 모든 실행에 반드시 필요한 API 키는 없습니다. 프로젝트는 zero-key 데모로 동작하며(Makefile `demo` 타깃: “Rendering zero-key demo videos (no API keys needed)”), 각 키는 특정 클라우드 프로바이더/기능을 잠금 해제하는 opt-in 용도입니다. 데모 렌더링만 확인하려면 키를 채우지 않아도 됩니다.

대표적인 선택 키(전체 목록은 `.env.example` 참고):

| 변수명 | 필수 여부 | 용도 |
|---|---|---|
| FAL_KEY | 선택 | fal.ai 이미지/영상 게이트웨이(FLUX 이미지, Google Veo/Kling/MiniMax 영상, Recraft 이미지). `FAL_AI_API_KEY`는 별칭 |
| GOOGLE_API_KEY | 선택 | Google Imagen 이미지, Cloud TTS(700+ 음성/50+ 언어), Gemini Omni 영상. `GEMINI_API_KEY`는 별칭(둘 다 설정 시 이쪽이 우선) |
| OPENAI_API_KEY | 선택 | OpenAI TTS 폴백, GPT Image 2 이미지 생성 |
| ELEVENLABS_API_KEY | 선택 | ElevenLabs TTS 내레이션, 음악, 효과음 |
| KLING_API_KEY | 선택 | Kling direct API(영상/이미지/TTS/아바타/립싱크) |
| REPLICATE_API_TOKEN | 선택 | Replicate 호스팅 영상 생성(seedance_replicate) |
| SUNO_API_KEY | 선택 | Suno AI 음악 생성 |
| PEXELS_API_KEY / PIXABAY_API_KEY / UNSPLASH_ACCESS_KEY | 선택 | 무료 스톡 영상/이미지 |
| VIDEO_GEN_LOCAL_ENABLED | 선택 | 로컬 영상 생성 토글(`true` 시 GPU + diffusers 필요 — 4-2 참고) |
| VIDEO_GEN_LOCAL_MODEL | 선택 | 로컬 모델 지정: `wan2.1-1.3b` / `wan2.1-14b` / `hunyuan-1.5` / `ltx2-local` / `cogvideo-5b` |

> 조건부 필수: Vertex AI 경유 Imagen 사용 시 `GOOGLE_CLOUD_PROJECT`(GCP 프로젝트 ID)가 필요하며, 서비스 계정 JSON 경로(`GOOGLE_APPLICATION_CREDENTIALS`)를 사용할 때도 함께 필요합니다.
> 페어 규칙: `HIGGSFIELD_API_KEY` 사용 시 `HIGGSFIELD_API_SECRET`이 필수이며, 단일 `HIGGSFIELD_KEY="<key>:<secret>"` 형태로 대체할 수 있습니다. `AZURE_SPEECH_KEY` 사용 시 `AZURE_SPEECH_REGION` 페어가 필요합니다.
> `.gitignore`가 `.env` 등을 커밋에서 제외하므로 실수로 커밋될 위험은 낮습니다.
> Piper 로컬 TTS는 환경변수가 필요 없습니다.

---

## 6. 실행하기

OpenMontage는 에이전트 주도(agent-first) 아키텍처로, 별도의 단일 CLI 진입점이 없습니다. 다음은 설치 완료 후 가장 단순하게 동작을 확인할 수 있는 방법들입니다.

### 6-1. 데모 렌더 (가장 단순한 동작 확인)

`render_demo.py`는 체크인된 Remotion JSON props로부터 zero-key 데모 영상(MP4)을 렌더링합니다. 렌더링 자체는 Node.js의 Remotion이 수행하므로 Node.js/npm/npx가 PATH에 있어야 합니다.

다음은 사용 가능한 데모 목록을 확인하는 명령입니다(Windows PowerShell).

```powershell
python render_demo.py --list
```

다음은 단일 데모를 렌더하는 명령입니다(`<name>` 예: `world-in-numbers`, `code-to-screen`, `focusflow-pitch`).

```powershell
python render_demo.py world-in-numbers
```

다음은 모든 데모를 렌더하는 명령입니다(인자 생략).

```powershell
python render_demo.py
```

다음은 macOS/Linux에서 bash 래퍼 스크립트를 사용하는 명령입니다.

```bash
bash render-demo.sh --list
bash render-demo.sh code-to-screen
```

> 산출물 MP4는 `projects/demos/renders/<name>.mp4`에 생성되며 출력 디렉터리는 자동 생성됩니다.

### 6-2. Makefile 타깃 (make가 있는 환경)

Makefile은 `.DEFAULT_GOAL := setup`이며 다음 타깃을 제공합니다. Makefile은 bash 셸 문법을 가정하므로 Windows에서는 Git Bash/WSL/MSYS 환경에서 실행합니다.

다음은 한 번에 전체 환경을 구축하는 명령입니다(venv + pip 코어 설치 + remotion-composer npm install + piper-tts + HyperFrames npx 캐시 웜/검사 + .env 복사).

```bash
make setup
```

다음은 코어 의존성만 설치하는 명령입니다.

```bash
make install
```

다음은 개발/GPU 의존성을 추가하는 명령입니다.

```bash
make install-dev
make install-gpu
```

> 참고: `make install-gpu`는 `requirements-gpu.txt` 설치 후 추가로 `diffusers transformers accelerate`를 설치합니다. 수동 pip 경로에서 동일하게 맞추려면 [4-2](#4-2-선택-gpu-의존성)의 두 단계를 그대로 따르세요.

다음은 데모를 렌더하고 테스트를 돌리는 명령들입니다.

```bash
make demo         # = python render_demo.py (전체 렌더, API 키 불필요)
make demo-list    # = python render_demo.py --list
make test-contracts   # 계약 테스트 (API 키 불필요)
make test             # 전체 테스트
```

### 6-3. 전체 영상 제작 (에이전트 구동)

설치 후 AI 코딩 어시스턴트(Claude Code, Cursor, Copilot, Windsurf, Codex 중 하나)에서 프로젝트 폴더를 열고(File → Open Folder) 채팅에 프롬프트를 입력하면 에이전트가 정의된 파이프라인(`pipeline_defs/`의 매니페스트 + 스테이지 디렉터 스킬)을 구동합니다. 별도의 CLI 실행 명령은 없으며, 임의 파이썬 스크립트로 도구를 직접 호출하는 방식은 권장되지 않습니다([AGENT_GUIDE.md](AGENT_GUIDE.md)의 “Rule Zero” 참고).

```
"신경망이 어떻게 학습하는지 설명하는 60초 애니메이션 영상을 만들어 주세요"
```

---

## 7. 설치/동작 확인

다음 명령으로 코어 패키지 import가 정상적으로 완료되었는지 확인합니다(모든 플랫폼 공통).

```powershell
python -c "import fastapi, uvicorn, watchfiles, numpy, google.auth, pydantic, openai; print('core deps OK')"
```

다음 명령으로 데모 목록이 정상 출력되는지 확인합니다(가장 단순한 동작 확인).

```powershell
python render_demo.py --list
```

성공 시 예상 동작:

- `--list`는 `remotion-composer/public/demo-props/*.json`에서 발견된 데모(예: `world-in-numbers`, `code-to-screen`, `focusflow-pitch`) 목록을 출력합니다.
- 단일 데모 렌더는 `projects/demos/renders/<name>.mp4` 파일을 생성합니다.
- 렌더 내부적으로 `npx remotion render src/index.tsx Explainer <output> --props <json> --codec h264`(작업 디렉터리 `remotion-composer`)가 실행됩니다.

---

## 문제 해결(Troubleshooting)

**PowerShell에서 `Activate.ps1` 실행이 차단됨 (실행 정책)**
스크립트 실행 권한 문제입니다. 현재 세션에만 허용하려면 아래 명령을 실행한 뒤 다시 활성화를 시도합니다.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

또는 사용자 범위로 영구 허용하려면 `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`를 사용합니다.

**파이썬 버전이 안 맞음**
`py -3 --version`으로 버전을 확인합니다. `.python-version`이 `3.10`, `setup.py`가 `python_requires=">=3.10"`이므로 3.10 미만이면 가상환경 생성 단계부터 실패합니다. Python 3.10+를 설치하세요.

**`pip install -e .`만 실행 후 런타임 import 실패**
`setup.py`의 `install_requires`가 `requirements.txt`의 진부분집합(`google-auth`, `numpy`, `fastapi`, `uvicorn`, `watchfiles` 누락)이기 때문입니다. 반드시 `python -m pip install -r requirements.txt`를 먼저 실행하세요. `-e .`는 보조 설치입니다.

**`VIDEO_GEN_LOCAL_ENABLED=true` 설정 후 로컬 영상 생성 모델 import 실패**
PyTorch(`requirements-gpu.txt`)만 설치하고 diffusers 계열 패키지를 빠뜨린 경우입니다. `.env.example`이 “needs GPU + diffusers”로 명시하고 있듯, `pip install -r requirements-gpu.txt` 다음에 반드시 `pip install diffusers transformers accelerate`를 추가로 실행하세요. 이는 `make install-gpu`가 수행하는 것과 동일한 패키지 세트입니다.

**`httpx2` 패키지 설치 실패 (requirements-dev.txt)**
파일에 `httpx2>=2.0`으로 적혀 있으나 PyPI의 `httpx` 오타로 보입니다. 사용자가 직접 확인해야 하며, 필요하다면 `httpx`로 수정 후 재설치를 고려하세요. 본 가이드는 파일 내용을 있는 그대로 인용합니다.

**Windows에서 `npm install`이 `ERR_INVALID_ARG_TYPE`로 실패**
`remotion-composer` 디렉터리 안에서 아래 명령을 대신 사용합니다(README 권장).

```powershell
cd remotion-composer
npx --yes npm install
cd ..
```

**`make` 명령을 찾을 수 없음 (Windows)**
Windows에는 기본 설치되어 있지 않습니다. Git Bash/WSL에서 make를 설치하거나, 본 가이드의 PowerShell 직접 명령(1~5단계)으로 동일한 결과를 얻을 수 있습니다.

**`piper-tts` 설치 실패**
정상 동작입니다. Makefile은 실패 시 `[skip]` 처리하고 클라우드 TTS로 폴백합니다. 에러로 다루지 마세요.

**PyTorch CUDA wheel 관련 오류 (requirements-gpu.txt)**
`requirements-gpu.txt`에 CUDA 인덱스 URL이 명시되어 있지 않습니다. 로컬 CUDA 버전에 맞춰 PyTorch 인덱스(`--index-url https://download.pytorch.org/whl/cuXXX`)를 별도로 지정해야 합니다.

**`render_demo.py` 실행 시 “No demo prop files were found” 오류**
데모 탐색이 `remotion-composer/public/demo-props/*.json`을 glob하므로 해당 폴더가 없거나 비어 있으면 종료됩니다. 먼저 `python render_demo.py --list`로 실제 사용 가능한 데모를 확인하세요.

**경로에 한글/공백이 포함된 경우**
명령줄 인자와 경로를 따옴표로 감싸세요. `.venv`의 파이썬은 절대 경로로 직접 지정할 수도 있습니다. 예: `"D:\ysj\OpenMontage\.venv\Scripts\python.exe"`.

---

## 참고

- [README_ko.md](README_ko.md) — 프로젝트 전체 한국어 번역 본문(이중 언어 구조, Quick Start 포함)
- [docs/ko/USAGE.md](docs/ko/USAGE.md) — Windows 11 사용자 대상 한국어 사용법 가이드(설치·실행 절차, 이중 언어)
- [docs/ko/MODEL-SETUP.md](docs/ko/MODEL-SETUP.md) — 모델 두뇌 교체 가이드
- [docs/ko/KIMI-SETUP.md](docs/ko/KIMI-SETUP.md) — Kimi 연결 가이드
- [docs/ko/PROVIDERS.md](docs/ko/PROVIDERS.md) — 클라우드 프로바이더/기능 매트릭스(한국어)
- [AGENT_GUIDE.md](AGENT_GUIDE.md) — 에이전트 동작 규칙(Rule Zero, 파이프라인 강제)
- 저장소: [github.com/calesthio/OpenMontage](https://github.com/calesthio/OpenMontage) (라이선스 AGPLv3)
