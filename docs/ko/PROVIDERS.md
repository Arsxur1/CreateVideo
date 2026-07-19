> 이 문서는 이중 언어 문서입니다. 각 섹션에서 영어 원문이 먼저 나오고, **[한국어]** 표시 아래에 한국어 번역이 이어집니다.

> 원본: docs/PROVIDERS.md @ f8d94632ea9bd0057da31904acca1cefecf005dd

# OpenMontage Provider Guide (OpenMontage 프로바이더 가이드)

Everything you need to know about every provider in OpenMontage — setup instructions, pricing, free tiers, and what each unlocks.

**[한국어]**

OpenMontage의 모든 프로바이더에 관한 모든 정보 — 설정 방법, 가격, 무료 플랜, 각 프로바이더로 가능한 작업.

---

## Quick Start: What Should I Set Up? (퀵 스타트: 무엇을 설정해야 할까요?)

**Start free, add paid providers as you need them.** Here's the recommended order:

**[한국어]**

**무료로 시작하고, 필요에 따라 유료 프로바이더를 추가하십시오.** 추천 순서는 다음과 같습니다.

| Step | Cost | What to set up | What it unlocks |
|------|------|----------------|-----------------|
| 1 | **$0** | Pexels + Pixabay | Stock photos and videos — enough to produce basic videos |
| 2 | **$0** | Google API key | TTS with 700+ voices (1M chars/month free) + $300 new account credit |
| 3 | **$0** | ElevenLabs | Premium TTS + music + SFX (10K chars/month free) |
| 4 | **$0** | Piper (local install) | Fully offline TTS — no API key, no cost, no network |
| 5 | **~$0.03/image** | fal.ai | FLUX images + Kling/Veo/MiniMax video + Recraft — broad single-key image + video coverage |
| 6 | **~$0.05/image** | OpenAI | GPT Image 2 images + OpenAI TTS |
| 7 | **~$0.04/image** | Google Imagen | Imagen 4 images (shares the Google API key) |
| 8 | **pay-as-you-go** | Kling Official | Official direct Kling video, image, TTS, avatar, and lip-sync API, separate from fal.ai Kling |
| 9 | **$12/month** | Runway | Gen-4 video — highest quality AI video |
| 10 | **pay-as-you-go** | HeyGen | Avatar videos, multi-model video gateway |
| 11 | **pay-as-you-go** | Suno | Full song generation with vocals and lyrics |
| 12 | **$0 + GPU** | Local video gen | WAN 2.1, Hunyuan, CogVideo, LTX — free, offline |
| 13 | **$0 + GPU** | Local Diffusion | Stable Diffusion images — free, offline |

**[한국어]**

| 단계 | 비용 | 설정 항목 | 가능해지는 작업 |
|------|------|----------------|-----------------|
| 1 | **$0** | Pexels + Pixabay | 스톡 사진 및 영상 — 기본 영상 제작에 충분 |
| 2 | **$0** | Google API 키 | TTS 700개 이상 음성 (월 100만 자 무료) + 신규 계정 $300 크레딧 |
| 3 | **$0** | ElevenLabs | 프리미엄 TTS + 음악 + 효과음 (월 1만 자 무료) |
| 4 | **$0** | Piper (로컬 설치) | 완전히 오프라인 TTS — API 키 불필요, 비용 무료, 네트워크 불필요 |
| 5 | **~$0.03/이미지** | fal.ai | FLUX 이미지 + Kling/Veo/MiniMax 영상 + Recraft — 단일 키로 광범위한 이미지+영상 커버리지 |
| 6 | **~$0.05/이미지** | OpenAI | GPT Image 2 이미지 + OpenAI TTS |
| 7 | **~$0.04/이미지** | Google Imagen | Imagen 4 이미지 (Google API 키와 공유) |
| 8 | **종량제** | Kling Official | Kling 공식 직접 API (영상, 이미지, TTS, 아바타, 립싱크), fal.ai Kling과 별도 |
| 9 | **$12/월** | Runway | Gen-4 영상 — 최고 품질 AI 영상 |
| 10 | **종량제** | HeyGen | 아바타 영상, 멀티모델 영상 게이트웨이 |
| 11 | **종량제** | Suno | 보컬과 가사가 있는 완곡 생성 |
| 12 | **$0 + GPU** | 로컬 영상 생성 | WAN 2.1, Hunyuan, CogVideo, LTX — 무료, 오프라인 |
| 13 | **$0 + GPU** | 로컬 Diffusion | Stable Diffusion 이미지 — 무료, 오프라인 |

### Environment Variable Summary (환경 변수 요약)

```bash
# .env — add your keys here

# FREE (no cost, ever)
PEXELS_API_KEY=              # Stock photos + videos
PIXABAY_API_KEY=             # Stock photos + videos

# GOOGLE (one key, multiple tools, generous TTS free tier)
GOOGLE_API_KEY=              # Google TTS + Imagen + Lyria music + Gemini Omni/Veo video

# VOICE + MUSIC
ELEVENLABS_API_KEY=          # TTS, music, sound effects (10K chars/month free)
OPENAI_API_KEY=              # OpenAI TTS + GPT Image 2 images
XAI_API_KEY=                 # xAI Grok image generation/editing + Grok video generation
DOUBAO_SPEECH_API_KEY=       # Volcengine Doubao Speech TTS (strong Mandarin narration)
DOUBAO_SPEECH_VOICE_TYPE=    # Default Doubao speaker/voice type
DASHSCOPE_API_KEY=           # Alibaba DashScope (Qwen image gen, TTS, ASR with word timestamps)

# SPEECH-TO-TEXT (optional cloud transcription; local whisper is the default)
AZURE_SPEECH_KEY=            # Azure AI Speech — Fast Transcription (word-level timestamps)
AZURE_SPEECH_REGION=         # Speech resource region, e.g. eastus

# MULTI-MODEL GATEWAY (one key, 6+ tools)
FAL_KEY=                     # FLUX, Recraft, Kling, Veo, MiniMax video

# KLING OFFICIAL DIRECT API
KLING_API_KEY=               # Official Kling video, image, TTS, avatar, lip sync
KLING_API_BASE_URL=          # Optional; default https://api-singapore.klingai.com

# VIDEO
HEYGEN_API_KEY=              # HeyGen avatar video gateway
RUNWAY_API_KEY=              # Runway Gen-4 video (direct)
SUNO_API_KEY=                # Suno music generation

# LOCAL (no keys needed — just GPU + install)
VIDEO_GEN_LOCAL_ENABLED=     # Set to "true" for local video gen
VIDEO_GEN_LOCAL_MODEL=       # wan2.1-1.3b, wan2.1-14b, hunyuan-1.5, ltx2-local, cogvideo-5b
```

**[한국어]**

환경 변수에 대한 한국어 설명이 위 코드 블록 내 주석으로 포함되어 있습니다.

---

## Cloud Providers (클라우드 프로바이더)

### xAI — Grok Image + Video

> **Best if you want one provider for image edits and reference-conditioned short video.** Grok covers both image generation/editing and video generation under one key.

**[한국어]**

> **이미지 편집과 레퍼런스 기반 단편 영상을 한 프로바이더로 원할 때 최적.** Grok는 이미지 생성/편집과 영상 생성을 하나의 키로 모두 처리합니다.

**Tools unlocked:** `grok_image`, `grok_video`
**Env var:** `XAI_API_KEY`

**[한국어]**

**활성화 도구:** `grok_image`, `grok_video`
**환경 변수:** `XAI_API_KEY`

#### Setup (설정)

1. Create an xAI developer account
2. Generate an API key in the xAI developer console
3. Add to `.env`: `XAI_API_KEY=xai-...`

**[한국어]**

1. xAI 개발자 계정 생성
2. xAI 개발자 콘솔에서 API 키 생성
3. `.env`에 추가: `XAI_API_KEY=xai-...`

#### What it's best for (최적 용도)

- Image editing and style transfer
- Multi-image composites into one generated frame
- Short reference-image videos where a person, garment, or product must carry into motion

**[한국어]**

- 이미지 편집과 스타일 전이
- 여러 이미지를 하나의 생성 프레임으로 합성
- 인물, 의류, 제품이 영상에서 그대로 이동해야 하는 레퍼런스 이미지 기반 단편 영상

#### Pricing (가격)

Current xAI docs pricing for the Grok media models:

**[한국어]**

현재 xAI 문서 기준 Grok 미디어 모델 가격:

| Model | Price |
|------|-------|
| `grok-imagine-image` | $0.02 per generated image |
| `grok-imagine-image` input images (edits/composites) | $0.002 per input image |
| `grok-imagine-video` at 480p | $0.05/sec |
| `grok-imagine-video` at 720p | $0.07/sec |
| `grok-imagine-video` input images | $0.002 per input image |

**[한국어]**

| 모델 | 가격 |
|------|-------|
| `grok-imagine-image` | 생성 이미지당 $0.02 |
| `grok-imagine-image` 입력 이미지 (편집/합성) | 입력 이미지당 $0.002 |
| `grok-imagine-video` 480p | 초당 $0.05 |
| `grok-imagine-video` 720p | 초당 $0.07 |
| `grok-imagine-video` 입력 이미지 | 입력 이미지당 $0.002 |

OpenMontage now uses those published rates in the Grok tool estimators.

**[한국어]**

OpenMontage는 이제 Grok 도구 추산에서 공개된 요금을 사용합니다.

---

### Alibaba DashScope — Qwen Image + TTS + ASR

> **Best for Chinese-language production.** One key unlocks Qwen-Image generation, Qwen-TTS Mandarin narration, and Qwen-ASR with word-level timestamps — the only DashScope path that provides word-level granularity for subtitle alignment.

**[한국어]**

> **중국어 제작에 최적.** 하나의 키로 Qwen-Image 생성, Qwen-TTS 중국어 내레이션, 단어 단위 타임스탬프가 있는 Qwen-ASR을 활성화합니다 — 자막 정렬을 위한 단어 단위 세분성을 제공하는 유일한 DashScope 경로입니다.

**Tools unlocked:** `dashscope_image`, `dashscope_tts`, `dashscope_asr`
**Env var:** `DASHSCOPE_API_KEY`

**[한국어]**

**활성화 도구:** `dashscope_image`, `dashscope_tts`, `dashscope_asr`
**환경 변수:** `DASHSCOPE_API_KEY`

#### Setup (설정)

1. Go to [dashscope.aliyun.com](https://dashscope.aliyun.com/)
2. Create an Alibaba Cloud account if you don't have one
3. Generate an API key in the DashScope console
4. Add to `.env`: `DASHSCOPE_API_KEY=sk-...`

**[한국어]**

1. [dashscope.aliyun.com](https://dashscope.aliyun.com/) 방문
2. Alibaba Cloud 계정이 없다면 생성
3. DashScope 콘솔에서 API 키 생성
4. `.env`에 추가: `DASHSCOPE_API_KEY=sk-...`

#### What it's best for (최적 용도)

- Chinese-language image generation with strong prompt understanding (Qwen-Image)
- Natural Mandarin narration (Qwen-TTS, Cherry voice)
- Word-level timestamp transcription for subtitle alignment (Qwen-ASR filetrans)
- Replacing the broken `whisperx` slot for ASR

**[한국어]**

- 강력한 프롬프트 이해를 갖춘 중국어 이미지 생성 (Qwen-Image)
- 자연스러운 중국어 내레이션 (Qwen-TTS, Cherry 음성)
- 자막 정렬을 위한 단어 단위 타임스탬프 전사 (Qwen-ASR filetrans)
- 깨진 `whisperx` ASR 슬롯 대체

#### API notes (API 참고 사항)

DashScope's `/compatible-mode/v1/` only supports `/chat/completions` and `/embeddings`. Image gen, TTS, and ASR all use DashScope-native endpoints with nested `{model, input, parameters}` request shape — not OpenAI-compatible paths.

**[한국어]**

DashScope의 `/compatible-mode/v1/`은 `/chat/completions`와 `/embeddings`만 지원합니다. 이미지 생성, TTS, ASR은 모두 중첩된 `{model, input, parameters}` 요청 형태를 사용하는 DashScope 네이티브 엔드포인트를 사용합니다 — OpenAI 호환 경로가 아닙니다.

The ASR tool (`qwen3-asr-flash-filetrans`) uses an async submit-poll pattern. Audio must be at a publicly accessible URL (local files are not supported). Word timestamps are in milliseconds, normalized to seconds by the tool.

**[한국어]**

ASR 도구(`qwen3-asr-flash-filetrans`)는 비동기 제출-폴링 패턴을 사용합니다. 오디오는 공개적으로 접근 가능한 URL이어야 합니다(로컬 파일은 지원되지 않음). 단어 타임스탬프는 밀리초 단위이며, 도구에서 초 단위로 정규화합니다.

#### Pricing (가격)

| Model | Price |
|------|-------|
| `qwen-image-2.0-pro` | ~$0.02 per image (check console for current rates) |
| `qwen3-tts-flash` | ~$0.000015 per character |
| `qwen3-asr-flash-filetrans` | Per-minute billing (check console) |

**[한국어]**

| 모델 | 가격 |
|------|-------|
| `qwen-image-2.0-pro` | 이미지당 ~$0.02 (현재 요금은 콘솔 확인) |
| `qwen3-tts-flash` | 문자당 ~$0.000015 |
| `qwen3-asr-flash-filetrans` | 분당 청구 (콘솔 확인) |

---

### fal.ai — Multi-Model Gateway

> **Broad single-key coverage.** One API key unlocks image and video providers across multiple models.

**[한국어]**

> **광범위한 단일 키 커버리지.** 하나의 API 키로 여러 모델의 이미지와 영상 프로바이더를 활성화합니다.

**Tools unlocked:** `flux_image`, `recraft_image`, `kling_video`, `veo_video`, `minimax_video`
**Env var:** `FAL_KEY`

**[한국어]**

**활성화 도구:** `flux_image`, `recraft_image`, `kling_video`, `veo_video`, `minimax_video`
**환경 변수:** `FAL_KEY`

#### Setup (설정)

1. Go to [fal.ai](https://fal.ai/) and click **Sign up** (GitHub or Google)
2. Navigate to [fal.ai/dashboard/keys](https://fal.ai/dashboard/keys)
3. Click **Create Key**, copy it
4. Add to `.env`: `FAL_KEY=your-key-here`

**[한국어]**

1. [fal.ai](https://fal.ai/) 방문 후 **Sign up** 클릭 (GitHub 또는 Google)
2. [fal.ai/dashboard/keys](https://fal.ai/dashboard/keys)로 이동
3. **Create Key** 클릭 후 복사
4. `.env`에 추가: `FAL_KEY=your-key-here`

#### Pricing (가격)

No subscription — pure pay-as-you-go, no minimum spend.

**[한국어]**

구독 없음 — 순수 종량제, 최소 소요 비용 없음.

**Image generation:**

**[한국어]**

**이미지 생성:**

| Model | Price | Per $1 |
|-------|-------|--------|
| FLUX Pro v1.1 | $0.05/image | 20 images |
| FLUX Dev | $0.03/image | 33 images |
| Recraft v3 | ~$0.04/image | 25 images |

**[한국어]**

| 모델 | 가격 | $1당 |
|-------|-------|--------|
| FLUX Pro v1.1 | 이미지당 $0.05 | 20개 이미지 |
| FLUX Dev | 이미지당 $0.03 | 33개 이미지 |
| Recraft v3 | 이미지당 ~$0.04 | 25개 이미지 |

**Video generation:**

**[한국어]**

**영상 생성:**

| Model | Price | Per $1 |
|-------|-------|--------|
| Kling 2.5 Turbo Pro | $0.07/sec | 14 seconds |
| MiniMax | ~$0.05/sec | 20 seconds |
| Veo 3 | $0.40/sec | 2.5 seconds |
| WAN 2.5 | $0.05/sec | 20 seconds |

**[한국어]**

| 모델 | 가격 | $1당 |
|-------|-------|--------|
| Kling 2.5 Turbo Pro | 초당 $0.07 | 14초 |
| MiniMax | 초당 ~$0.05 | 20초 |
| Veo 3 | 초당 $0.40 | 2.5초 |
| WAN 2.5 | 초당 $0.05 | 20초 |

**Free tier:** None — but $0 to start, you only pay for what you use.

**[한국어]**

**무료 플랜:** 없음 — 하지만 시작 비용은 $0이며, 사용하는 만큼만 지불합니다.

---

### Kling Official — Direct API

> **Official Kling path.** This is separate from `kling_video` via fal.ai: it uses Kling's official `Authorization: Bearer <KLING_API_KEY>` API, provider name `kling_official`, and direct Classic/Turbo/Omni task protocols.

**[한국어]**

> **Kling 공식 경로.** fal.ai의 `kling_video`와 별개입니다. Kling의 공식 `Authorization: Bearer <KLING_API_KEY>` API, 프로바이더 이름 `kling_official`, 직접 Classic/Turbo/Omni 작업 프로토콜을 사용합니다.

**Tools unlocked:** `kling_official_video`, `kling_official_image`, `kling_tts`, `kling_avatar`, `kling_lip_sync`
**Env vars:** `KLING_API_KEY`, optional `KLING_API_BASE_URL`

**[한국어]**

**활성화 도구:** `kling_official_video`, `kling_official_image`, `kling_tts`, `kling_avatar`, `kling_lip_sync`
**환경 변수:** `KLING_API_KEY`, 선택 사항 `KLING_API_BASE_URL`

#### Setup (설정)

1. Create or open a Kling AI Open Platform account.
2. Generate an official API key in the Kling API console.
3. Add to `.env`:
   ```bash
   KLING_API_KEY=your-key-here
   # Optional, defaults to Singapore:
   KLING_API_BASE_URL=https://api-singapore.klingai.com
   ```

**[한국어]**

1. Kling AI Open Platform 계정 생성 또는 오픈.
2. Kling API 콘솔에서 공식 API 키 생성.
3. `.env`에 추가:
   ```bash
   KLING_API_KEY=your-key-here
   # 선택 사항, 기본값은 싱가포르:
   KLING_API_BASE_URL=https://api-singapore.klingai.com
   ```

#### What It Is Best For (최적 용도)

- Direct official Kling API provenance rather than fal.ai gateway routing
- Text-to-video, image-to-video, and deep Video Omni reference workflows via `kling_official_video`
- Text-to-image, image edit/reference, and Image Omni multi-reference or series workflows via `kling_official_image`
- Text-to-speech via `kling_tts` when you already know the official Kling `voice_id`
- Cloud avatar presenter clips via `kling_avatar`, without replacing local `talking_head`
- Cloud lip-sync via `kling_lip_sync`, with explicit face selection for multi-person videos
- Accounts that need to use official Kling model permissions, resource packs, or regional endpoints

**[한국어]**

- fal.ai 게이트웨이 라우팅이 아닌 직접적인 Kling 공식 API 출처
- `kling_official_video`를 통한 텍스트-투-비디오, 이미지-투-비디오, 심도 있는 Video Omni 레퍼런스 워크플로우
- `kling_official_image`를 통한 텍스트-투-이미지, 이미지 편집/레퍼런스, Image Omni 다중 레퍼런스 또는 시리즈 워크플로우
- 공식 Kling `voice_id`를 이미 알고 있을 때 `kling_tts`를 통한 텍스트-투-스피치
- 로컬 `talking_head`를 대체하지 않으면서 `kling_avatar`를 통한 클라우드 아바타 프레젠터 클립
- 다중 인물 영상에서 명시적인 얼굴 선택이 가능한 `kling_lip_sync`를 통한 클라우드 립싱크
- 공식 Kling 모델 권한, 리소스 팩, 리전별 엔드포인트를 사용해야 하는 계정

#### Notes (참고 사항)

- `provider="kling_official"` is intentionally different from fal.ai's `provider="kling"`.
- Official Kling is a paid remote API. OpenMontage uses conservative cost estimates and includes high-cost factors such as Omni references, series output, 4k mode, and native sound.
- Local image paths are sent as raw base64 for supported Classic/image-generation fields. Turbo image-to-video requires a URL and will not silently upload through fal.ai.
- Video Omni and Image Omni can pass official `element_id` references through `element_list`; Elements remain an internal Kling Official helper, not a standalone OpenMontage capability.
- Account Usage is available as a low-frequency diagnostic helper under `tools/_kling/account.py`; it is not a selector or pipeline tool.
- `callback_url` is passed through and recorded when supplied, but OpenMontage still polls tasks by default.
- `kling_tts` requires an explicit `voice_id`; OpenMontage does not guess a default official voice.
- `kling_avatar` and `kling_lip_sync` register under the existing `avatar` capability and coexist with local SadTalker/Wav2Lip tools. Current avatar pipelines must opt into them explicitly; registry discovery alone does not replace local tools.
- Official Kling audio effects and video effects are documented but intentionally not registered as OpenMontage tools yet, because current pipelines do not have a stable sound-effects or video-effects capability slot for them.

**[한국어]**

- `provider="kling_official"`은 fal.ai의 `provider="kling"`과 의도적으로 다릅니다.
- Kling 공식은 유료 원격 API입니다. OpenMontage는 보수적인 비용 추정을 사용하며 Omni 레퍼런스, 시리즈 출력, 4k 모드, 네이티브 사운드 같은 고비용 요소를 포함합니다.
- 로컬 이미지 경로는 지원되는 Classic/이미지 생성 필드를 위해 원시 base64로 전송됩니다. Turbo 이미지-투-비디오는 URL이 필요하며 fal.ai를 통해 자동 업로드되지 않습니다.
- Video Omni와 Image Omni는 `element_list`를 통해 공식 `element_id` 레퍼런스를 전달할 수 있습니다. Elements는 내부 Kling Official 도우미로만 남으며 독립적인 OpenMontage 기능이 아닙니다.
- Account Usage는 `tools/_kling/account.py` 하위의 저빈도 진단 도우미로 제공됩니다. 선택자나 파이프라인 도구가 아닙니다.
- `callback_url`은 제공될 때 통과되어 기록되지만, OpenMontage는 여전히 기본적으로 작업을 폴링합니다.
- `kling_tts`는 명시적인 `voice_id`가 필요합니다. OpenMontage는 기본 공식 음성을 추측하지 않습니다.
- `kling_avatar`와 `kling_lip_sync`는 기존 `avatar` 기능으로 등록되며 로컬 SadTalker/Wav2Lip 도구와 공존합니다. 현재 아바타 파이프라인은 명시적으로 이들을 선택해야 합니다. 레지스트리 발견만으로는 로컬 도구를 대체하지 않습니다.
- Kling 공식 오디오 효과와 비디오 효과는 문서화되어 있지만 의도적으로 아직 OpenMontage 도구로 등록되지 않습니다. 현재 파이프라인에는 이들을 위한 안정적인 사운드 효과 또는 비디오 효과 기능 슬롯이 없기 때문입니다.

---

### ElevenLabs — Voice, Music, Sound Effects

> **Premium voice quality.** Best TTS for narration-heavy videos. Also generates music and sound effects.

**[한국어]**

> **프리미엄 음성 품질.** 내레이션이 많은 영상에 최고의 TTS. 음악과 효과음도 생성합니다.

**Tools unlocked:** `elevenlabs_tts`, `music_gen`
**Env var:** `ELEVENLABS_API_KEY`

**[한국어]**

**활성화 도구:** `elevenlabs_tts`, `music_gen`
**환경 변수:** `ELEVENLABS_API_KEY`

#### Setup (설정)

1. Go to [elevenlabs.io](https://elevenlabs.io) and click **Sign up**
2. Go to **Profile** (bottom-left) > **API Keys**, or visit [elevenlabs.io/app/settings/api-keys](https://elevenlabs.io/app/settings/api-keys)
3. Click **Create API Key**, name it, copy it
4. Add to `.env`: `ELEVENLABS_API_KEY=xi_your-key-here`

**[한국어]**

1. [elevenlabs.io](https://elevenlabs.io) 방문 후 **Sign up** 클릭
2. **Profile**(좌측 하단) > **API Keys**로 이동하거나 [elevenlabs.io/app/settings/api-keys](https://elevenlabs.io/app/settings/api-keys) 방문
3. **Create API Key** 클릭 후 이름 지정, 복사
4. `.env`에 추가: `ELEVENLABS_API_KEY=xi_your-key-here`

#### Pricing (가격)

| Plan | Price | Characters/month | Key features |
|------|-------|-------------------|--------------|
| **Free** | $0 | 10,000 | 3 custom voices, API access, attribution required |
| Starter | $5/mo | 30,000 | No attribution |
| Creator | $22/mo | 100,000 | Professional voice cloning |
| Pro | $99/mo | 500,000 | 96kbps audio, usage analytics |
| Scale | $330/mo | 2,000,000 | Priority support |

**[한국어]**

| 플랜 | 가격 | 월별 문자 수 | 주요 기능 |
|------|-------|-------------------|--------------|
| **Free** | $0 | 10,000 | 맞춤 음성 3개, API 액세스, 저작자 표시 필요 |
| Starter | $5/월 | 30,000 | 저작자 표시 불필요 |
| Creator | $22/월 | 100,000 | 전문 음성 클로닝 |
| Pro | $99/월 | 500,000 | 96kbps 오디오, 사용량 분석 |
| Scale | $330/월 | 2,000,000 | 우선 지원 |

**Free tier:** 10,000 characters/month (roughly 2-3 minutes of narration). API access included. Music generation and sound effects also available on free tier with limited credits.

**[한국어]**

**무료 플랜:** 월 10,000 자(내레이션 약 2-3분). API 액세스 포함. 음악 생성과 효과음도 제한된 크레딧으로 무료 플랜에서 제공됩니다.

---

### Doubao Speech — Mandarin TTS

> **Strong Mandarin narration.** Volcengine Doubao Speech is a good choice for Chinese explainer voiceovers and long-form narration that needs subtitle timing metadata.

**[한국어]**

> **강력한 중국어 내레이션.** Volcengine Doubao Speech는 중국어 설명 영화 음성과 자막 타이밍 메타데이터가 필요한 장편 내레이션에 좋은 선택입니다.

**Tools unlocked:** `doubao_tts`
**Env vars:** `DOUBAO_SPEECH_API_KEY`, `DOUBAO_SPEECH_VOICE_TYPE`

**[한국어]**

**활성화 도구:** `doubao_tts`
**환경 변수:** `DOUBAO_SPEECH_API_KEY`, `DOUBAO_SPEECH_VOICE_TYPE`

#### Setup (설정)

1. Open the Volcengine Doubao Speech console and enable Speech Synthesis 2.0.
2. Create a new-console API Key.
3. Choose a Speech 2.0 voice type, for example `zh_female_vv_uranus_bigtts`.
4. Add to `.env`:
   ```bash
   DOUBAO_SPEECH_API_KEY=your-api-key
   DOUBAO_SPEECH_VOICE_TYPE=zh_female_vv_uranus_bigtts
   ```

**[한국어]**

1. Volcengine Doubao Speech 콘솔을 열고 Speech Synthesis 2.0 활성화.
2. new-console API 키 생성.
3. Speech 2.0 음성 타입 선택, 예: `zh_female_vv_uranus_bigtts`.
4. `.env`에 추가:
   ```bash
   DOUBAO_SPEECH_API_KEY=your-api-key
   DOUBAO_SPEECH_VOICE_TYPE=zh_female_vv_uranus_bigtts
   ```

#### API Notes (API 참고 사항)

OpenMontage uses the new-console API key flow:

**[한국어]**

OpenMontage는 new-console API 키 플로우를 사용합니다:

```text
X-Api-Key: ${DOUBAO_SPEECH_API_KEY}
X-Api-Resource-Id: seed-tts-2.0
```

Do not pass a new-console API Key as `X-Api-App-Id` or `X-Api-Access-Key`. That mismatch can produce `load grant: requested grant not found`.

**[한국어]**

new-console API 키를 `X-Api-App-Id`나 `X-Api-Access-Key`로 전달하지 마십시오. 이 불일치로 `load grant: requested grant not found` 오류가 발생할 수 있습니다.

#### What It Is Best For (최적 용도)

- Natural Mandarin narration for Chinese-language explainers
- Async long-form narration via `/api/v3/tts/submit` and `/api/v3/tts/query`
- Character-level timing metadata for subtitle alignment
- Calm educational pacing where the video duration can follow the approved voice rhythm

**[한국어]**

- 중국어 설명 영화를 위한 자연스러운 중국어 내레이션
- `/api/v3/tts/submit`과 `/api/v3/tts/query`를 통한 비동기 장편 내레이션
- 자막 정렬을 위한 문자 수준 타이밍 메타데이터
- 승인된 음성 리듬을 따르는 비디오 길이가 가능한 차분한 교육적 페이싱

#### Pacing (페이싱)

Start with `speech_rate: 0` for natural Mandarin delivery. If the approved format needs a tighter runtime, compare short samples at `speech_rate: 25` or `50` before generating the full narration. Do not force Doubao to match another provider's duration unless the user explicitly wants that tradeoff.

**[한국어]**

자연스러운 중국어 전달을 위해 `speech_rate: 0`으로 시작하십시오. 승인된 형식이 더 타이트한 런타임을 필요로 한다면 전체 내레이션을 생성하기 전에 `speech_rate: 25` 또는 `50`에서 짧은 샘플을 비교하십시오. 사용자가 명시적으로 그 타협을 원하지 않는 한 Doubao가 다른 프로바이더의 길이와 일치하도록 강요하지 마십시오.

#### Pricing (가격)

Doubao Speech 2.0 is billed by character package or usage in Volcengine. OpenMontage estimates cost from text length and prefers provider-returned usage metadata when available.

**[한국어]**

Doubao Speech 2.0은 Volcengine에서 문자 패키지 또는 사용량별로 청구됩니다. OpenMontage는 텍스트 길이에서 비용을 추정하며 가능한 경우 프로바이더가 반환하는 사용량 메타데이터를 선호합니다.

---

### Azure AI Speech — Speech-to-Text

> **Cloud transcription.** Azure AI Speech Fast Transcription turns local audio into text with word-level timestamps, speaker diarization, and multi-language identification — no GPU required. Optional: the local faster-whisper `transcriber` remains the default offline STT path. When `AZURE_SPEECH_KEY` is set, the agent prefers `azure_stt` for cloud transcription.

**[한국어]**

> **클라우드 전사.** Azure AI Speech Fast Transcription은 로컬 오디오를 단어 단위 타임스탬프, 스피커 다이어리제이션, 다중 언어 식별이 있는 텍스트로 변환합니다 — GPU 불필요. 선택 사항: 로컬 faster-whisper `transcriber`가 기본 오프라인 STT 경로로 남습니다. `AZURE_SPEECH_KEY`가 설정되면 에이전트는 클라우드 전사를 위해 `azure_stt`를 선호합니다.

**Tools unlocked:** `azure_stt`
**Env vars:** `AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION` (or `AZURE_SPEECH_ENDPOINT`)

**[한국어]**

**활성화 도구:** `azure_stt`
**환경 변수:** `AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION` (또는 `AZURE_SPEECH_ENDPOINT`)

#### Setup (설정)

1. In the [Azure portal](https://portal.azure.com), create a **Speech** resource (Azure AI services → Speech service).
2. Open the resource's **Keys and Endpoint** page.
3. Copy **KEY 1** and the **Location/Region** (e.g. `eastus`).
4. Add to `.env`:
   ```bash
   AZURE_SPEECH_KEY=your-speech-resource-key
   AZURE_SPEECH_REGION=eastus
   # AZURE_SPEECH_ENDPOINT=https://<custom>...  # optional, overrides region
   ```

**[한국어]**

1. [Azure 포털](https://portal.azure.com)에서 **Speech** 리소스 생성 (Azure AI services → Speech service).
2. 리소스의 **Keys and Endpoint** 페이지 열기.
3. **KEY 1**과 **Location/Region** 복사 (예: `eastus`).
4. `.env`에 추가:
   ```bash
   AZURE_SPEECH_KEY=your-speech-resource-key
   AZURE_SPEECH_REGION=eastus
   # AZURE_SPEECH_ENDPOINT=https://<custom>...  # 선택 사항, 리전 오버라이드
   ```

#### API Notes (API 참고 사항)

OpenMontage uses the **Fast Transcription** REST endpoint, which accepts a local
audio file directly (multipart upload) and returns a synchronous result — no
Azure Blob storage, SAS URLs, or async job polling:

**[한국어]**

OpenMontage는 **Fast Transcription** REST 엔드포인트를 사용합니다. 로컬 오디오 파일을 직접 (multipart 업로드로) 받아 동기 결과를 반환합니다 — Azure Blob 저장소, SAS URL, 비동기 작업 폴링 불필요:

```text
POST https://{region}.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2024-11-15
Ocp-Apim-Subscription-Key: ${AZURE_SPEECH_KEY}
```

For files longer than ~2 hours or bulk jobs, use Azure Batch Transcription instead (not wired into OpenMontage).

**[한국어]**

약 2시간 이상 파일이나 대량 작업의 경우 대신 Azure Batch Transcription을 사용하십시오 (OpenMontage에 연결되지 않음).

#### What It Is Best For (최적 용도)

- Cloud transcription with word-level timestamps and no local GPU
- Multi-language auto-detection across a candidate locale set
- Speaker diarization without a HuggingFace token
- Subtitle timing metadata that flows straight into `subtitle_gen`

**[한국어]**

- 로컬 GPU 없이 단어 단위 타임스탬프가 있는 클라우드 전사
- 후보 로케일 세트 across 다중 언어 자동 감지
- HuggingFace 토큰 없는 스피커 다이어리제이션
- `subtitle_gen`으로 직접 흘러가는 자막 타이밍 메타데이터

#### Pricing (가격)

Azure AI Speech Standard (S0) bills speech-to-text by audio-hour (roughly
$1.00/audio-hour at time of writing; a free F0 tier includes a limited monthly
allowance). OpenMontage estimates cost from the transcribed audio duration. See
[Azure AI Speech pricing](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/) for current rates.

**[한국어]**

Azure AI Speech Standard (S0)는 오디오 시간별로 음성-투-텍스트를 청구합니다 (작성 시점 기준 대략 오디오 시간당 $1.00; 무료 F0 티어에는 제한된 월 할당량 포함). OpenMontage는 전사된 오디오 지속 시간에서 비용을 추정합니다. 현재 요금은 [Azure AI Speech pricing](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/)를 참조하십시오.

---

### Google — TTS + Imagen + Music + Video (Shared Key)

> **One key, five tools.** Google Cloud TTS has 700+ voices in 50+ languages — the strongest localization option. Imagen 4 generates high-quality images. Google Lyria generates high-quality background music. Gemini Omni Flash supports conversational video editing, and direct Veo generation covers premium short video clips.

**[한국어]**

> **하나의 키, 다섯 가지 도구.** Google Cloud TTS는 50개 이상 언어로 700개 이상의 음성을 제공합니다 — 가장 강력한 현지화 옵션. Imagen 4는 고품질 이미지를 생성합니다. Google Lyria는 고품질 배경 음악을 생성합니다. Gemini Omni Flash는 대화형 비디오 편집을 지원하며, 직접 Veo 생성은 프리미엄 단편 비디오 클립을 처리합니다.

**Tools unlocked:** `google_tts`, `google_imagen`, `google_music`, `gemini_omni_video`, `veo_video`
**Env var:** `GOOGLE_API_KEY` (or `GEMINI_API_KEY` — either works; `GEMINI_API_KEY` takes precedence)

**[한국어]**

**활성화 도구:** `google_tts`, `google_imagen`, `google_music`, `gemini_omni_video`, `veo_video`
**환경 변수:** `GOOGLE_API_KEY` (또는 `GEMINI_API_KEY` — 둘 다 작동; `GEMINI_API_KEY`가 우선)

#### Setup (설정)

1. Go to [Google AI Studio](https://aistudio.google.com/) and sign in
2. Navigate to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
3. Click **Create API Key**, select a Google Cloud project
4. Copy the key
5. Add to `.env`: `GOOGLE_API_KEY=AIza...` (or `GEMINI_API_KEY=AIza...`)

**[한국어]**

1. [Google AI Studio](https://aistudio.google.com/) 방문 후 로그인
2. [aistudio.google.com/apikey](https://aistudio.google.com/apikey)로 이동
3. **Create API Key** 클릭 후 Google Cloud 프로젝트 선택
4. 키 복사
5. `.env`에 추가: `GOOGLE_API_KEY=AIza...` (또는 `GEMINI_API_KEY=AIza...`)

**For TTS specifically**, you also need to enable the Text-to-Speech API:
1. Visit [console.cloud.google.com/apis/library/texttospeech.googleapis.com](https://console.cloud.google.com/apis/library/texttospeech.googleapis.com)
2. Click **Enable**
3. Make sure your API key's restrictions allow the Text-to-Speech API

**[한국어]**

**TTS의 경우**, Text-to-Speech API도 활성화해야 합니다:
1. [console.cloud.google.com/apis/library/texttospeech.googleapis.com](https://console.cloud.google.com/apis/library/texttospeech.googleapis.com) 방문
2. **Enable** 클릭
3. API 키 제한이 Text-to-Speech API를 허용하는지 확인

**For Imagen, Lyria Music, Gemini Omni video, and direct Veo video**, enable the Generative Language API:
1. Visit [console.cloud.google.com/apis/library/generativelanguage.googleapis.com](https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com)
2. Click **Enable**

**[한국어]**

**Imagen, Lyria Music, Gemini Omni video, 직접 Veo video의 경우**, Generative Language API 활성화:
1. [console.cloud.google.com/apis/library/generativelanguage.googleapis.com](https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com) 방문
2. **Enable** 클릭

#### Google TTS Pricing (Google TTS 가격)

| Voice Type | Free tier | Paid (per 1M chars) | Notes |
|-----------|-----------|---------------------|-------|
| **Standard** | 1M chars/month | $4.00 | Basic quality, fast |
| **WaveNet** | 1M chars/month | $16.00 | Natural-sounding |
| **Neural2** | 1M chars/month | $16.00 | Best quality |
| **Studio** | — | $24.00 | Professional studio voices |
| **Chirp** | — | $4.00 | Conversational style |

**[한국어]**

| 음성 타입 | 무료 플랜 | 유료 (100만 자당) | 참고 |
|-----------|-----------|---------------------|-------|
| **Standard** | 월 100만 자 | $4.00 | 기본 품질, 빠름 |
| **WaveNet** | 월 100만 자 | $16.00 | 자연스러운 소리 |
| **Neural2** | 월 100만 자 | $16.00 | 최고 품질 |
| **Studio** | — | $24.00 | 전문 스튜디오 음성 |
| **Chirp** | — | $4.00 | 대화형 스타일 |

The free tiers apply *independently* — you get 1M Standard AND 1M WaveNet AND 1M Neural2 characters per month free. That's roughly 250+ minutes of narration per month at zero cost.

**[한국어]**

무료 플랜은 *독립적으로* 적용됩니다 — 월 1M Standard AND 1M WaveNet AND 1M Neural2 문자를 무료로 받습니다. 이는 비용 제로로 월 약 250분 이상의 내레이션입니다.

#### Google Imagen Pricing (Google Imagen 가격)

| Model | Price per image |
|-------|----------------|
| Imagen 4 Fast | $0.02 |
| Imagen 4 Standard | $0.04 |
| Imagen 4 Ultra | $0.06 |

**[한국어]**

| 모델 | 이미지당 가격 |
|-------|----------------|
| Imagen 4 Fast | $0.02 |
| Imagen 4 Standard | $0.04 |
| Imagen 4 Ultra | $0.06 |

**Free tier for Imagen:** None. Paid tier only.

**[한국어]**

**Imagen 무료 플랜:** 없음. 유료 플랜만.

#### Gemini Omni Video Pricing (Gemini Omni Video 가격)

| Model | Price | Notes |
|-------|-------|-------|
| `gemini-omni-flash-preview` | ~$0.10 per second of video | Billed as 5,792 output tokens/sec of 720p video at $17.50/1M tokens |

**[한국어]**

| 모델 | 가격 | 참고 |
|-------|-------|-------|
| `gemini-omni-flash-preview` | 초당 ~$0.10 | $17.50/1M 토큰의 720p 비디오 5,792 출력 토큰/초로 청구 |

Generates 3–10 second clips at 720p/24fps with synthesized audio, plus stateful conversational editing (`edit_video` via `previous_interaction_id`). **Paid tier only — no free tier.** A typical 8-second clip costs ~$0.80; each edit turn generates a new clip and bills again.

**[한국어]**

합성된 오디오가 있는 720p/24fps의 3~10초 클립을 생성하며 상태 유지 대화형 편집 제공 (`edit_video` via `previous_interaction_id`). **유료 플랜만 — 무료 플랜 없음.** 일반적인 8초 클립은 ~$0.80 비용. 편집 턴마다 새 클립을 생성하고 다시 청구됩니다.

#### Google Music (Lyria) Pricing (Google Music (Lyria) 가격)

| Model | Price per generation request |
|-------|-----------------------------|
| `lyria-3-pro-preview` | $0.08 (flat rate, up to 184s duration) |

**[한국어]**

| 모델 | 생성 요청당 가격 |
|-------|-----------------------------|
| `lyria-3-pro-preview` | $0.08 (정액, 최대 184초 지속 시간) |

**Free tier for Music:** None. Paid tier only.

**[한국어]**

**Music 무료 플랜:** 없음. 유료 플랜만.

**New account bonus:** Google Cloud offers **$300 in free credits** for new accounts (90-day trial), applicable to TTS, Imagen, Music, Gemini Omni video, and direct Veo video.

**[한국어]**

**신규 계정 보너스:** Google Cloud는 신규 계정에 **$300 무료 크레딧**을 제공합니다 (90일 평가판), TTS, Imagen, Music, Gemini Omni video, 직접 Veo video에 적용 가능합니다.

#### Google TTS Voice Types (Google TTS 음성 타입)

Google TTS offers 700+ voices across 50+ languages. Voice names follow the pattern `{language}-{type}-{letter}`:

**[한국어]**

Google TTS는 50개 이상 언어로 700개 이상의 음성을 제공합니다. 음성 이름은 `{language}-{type}-{letter}` 패턴을 따릅니다:

| Type | Example | Quality | Cost |
|------|---------|---------|------|
| **Chirp 3 HD** | `en-US-Chirp3-HD-Orus` | **Best (2024, most natural)** | **Mid — default** |
| Standard | `en-US-Standard-A` | Good | Cheapest |
| WaveNet | `en-US-WaveNet-D` | Very good | Mid |
| Neural2 | `en-US-Neural2-D` | Excellent | Mid |
| Studio | `en-US-Studio-O` | Professional | Highest |
| Journey | `en-US-Journey-D` | Conversational (long-form) | Mid |

**[한국어]**

| 타입 | 예 | 품질 | 비용 |
|------|---------|---------|------|
| **Chirp 3 HD** | `en-US-Chirp3-HD-Orus` | **최고 (2024, 가장 자연스러운)** | **중간 — 기본값** |
| Standard | `en-US-Standard-A` | 좋음 | 가장 저렴 |
| WaveNet | `en-US-WaveNet-D` | 매우 좋음 | 중간 |
| Neural2 | `en-US-Neural2-D` | 우수함 | 중간 |
| Studio | `en-US-Studio-O` | 전문적 | 가장 높음 |
| Journey | `en-US-Journey-D` | 대화형 (장편) | 중간 |

**Recommended voices:** `en-US-Chirp3-HD-Orus` (male, rich/cinematic), `en-US-Chirp3-HD-Aoede` (female, warm). These are Google's newest tier — most natural-sounding, uses the v1beta1 endpoint automatically.

**[한국어]**

**추천 음성:** `en-US-Chirp3-HD-Orus` (남성, 풍부한/영화적), `en-US-Chirp3-HD-Aoede` (여성, 따뜻한). 이들은 Google의 최신 티어 — 가장 자연스러운 소리, 자동으로 v1beta1 엔드포인트를 사용합니다.

**Languages include:** English (US, UK, AU, IN), Spanish, French, German, Italian, Portuguese, Japanese, Korean, Chinese (Mandarin, Cantonese), Arabic, Hindi, Russian, Dutch, Polish, Turkish, Vietnamese, Thai, Indonesian, and 30+ more.

**[한국어]**

**지원 언어:** 영어 (미국, 영국, 호주, 인도), 스페인어, 프랑스어, 독일어, 이탈리아어, 포르투갈어, 일본어, 한국어, 중국어 (만다린, 광둥어), 아랍어, 힌디어, 러시아어, 네덜란드어, 폴란드어, 터키어, 베트남어, 태국어, 인도네시아어, 30개 이상 추가 언어.

---

### OpenAI — TTS + Image Generation

> **Solid all-rounder.** GPT Image 2 handles complex multi-element compositions and in-image text well. TTS is fast and affordable.

**[한국어]**

> **튼튼한 올라운더.** GPT Image 2는 복잡한 다중 요소 구성과 이미지 내 텍스트를 잘 처리합니다. TTS는 빠르고 저렴합니다.

**Tools unlocked:** `openai_tts`, `openai_image`
**Env var:** `OPENAI_API_KEY`

**[한국어]**

**활성화 도구:** `openai_tts`, `openai_image`
**환경 변수:** `OPENAI_API_KEY`

#### Setup (설정)

1. Go to [platform.openai.com/signup](https://platform.openai.com/signup) and create an account
2. Add a payment method at [platform.openai.com/account/billing](https://platform.openai.com/account/billing)
3. Navigate to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
4. Click **Create new secret key**, name it, copy it
5. Add to `.env`: `OPENAI_API_KEY=sk-...`

**[한국어]**

1. [platform.openai.com/signup](https://platform.openai.com/signup) 방문 후 계정 생성
2. [platform.openai.com/account/billing](https://platform.openai.com/account/billing)에서 결제 방법 추가
3. [platform.openai.com/api-keys](https://platform.openai.com/api-keys)로 이동
4. **Create new secret key** 클릭 후 이름 지정, 복사
5. `.env`에 추가: `OPENAI_API_KEY=sk-...`

#### TTS Pricing (TTS 가격)

| Model | Price per 1M characters |
|-------|------------------------|
| tts-1 | $15.00 |
| tts-1-hd | $30.00 |
| gpt-4o-mini-tts | $12.00 |

**[한국어]**

| 모델 | 100만 자당 가격 |
|-------|------------------------|
| tts-1 | $15.00 |
| tts-1-hd | $30.00 |
| gpt-4o-mini-tts | $12.00 |

#### Image Pricing (이미지 가격)

| Model | Size | Quality | Price per image |
|-------|------|---------|----------------|
| GPT Image 2 | 1024x1024 | low | $0.006 |
| GPT Image 2 | 1024x1024 | medium | $0.053 |
| GPT Image 2 | 1024x1024 | high | $0.211 |
| GPT Image 2 | 1024x1536 / 1536x1024 | low | $0.005 |
| GPT Image 2 | 1024x1536 / 1536x1024 | medium | $0.041 |
| GPT Image 2 | 1024x1536 / 1536x1024 | high | $0.165 |

**[한국어]**

| 모델 | 크기 | 품질 | 이미지당 가격 |
|-------|------|---------|----------------|
| GPT Image 2 | 1024x1024 | low | $0.006 |
| GPT Image 2 | 1024x1024 | medium | $0.053 |
| GPT Image 2 | 1024x1024 | high | $0.211 |
| GPT Image 2 | 1024x1536 / 1536x1024 | low | $0.005 |
| GPT Image 2 | 1024x1536 / 1536x1024 | medium | $0.041 |
| GPT Image 2 | 1024x1536 / 1536x1024 | high | $0.165 |

> **Note:** DALL-E 2/3 were shut down by OpenAI on 2026-05-12, and the `gpt-image-1` family (`gpt-image-1-mini`, `gpt-image-1.5`) retires 2026-12-01 — `gpt-image-2` is OpenAI's recommended replacement ([deprecations](https://developers.openai.com/api/docs/deprecations)).

**[한국어]**

> **참고:** DALL-E 2/3는 2026-05-12에 OpenAI에서 종료되었으며, `gpt-image-1` 패밀리(`gpt-image-1-mini`, `gpt-image-1.5`)는 2026-12-01에 은퇴합니다 — `gpt-image-2`가 OpenAI의 권장 대체품입니다 ([deprecations](https://developers.openai.com/api/docs/deprecations)).

**Free tier:** None. Requires prepaid billing. Previously offered $5 in free credits for new accounts (discontinued for most signups).

**[한국어]**

**무료 플랜:** 없음. 선불 결제 필요. 이전 신규 계정 $5 무료 크레딧 제공 (대부분의 가입에 대해 중단됨).

---

### Runway — Gen-3/Gen-4 Video

> **Highest-rated AI video quality.** #1 on Elo rankings. Professional-grade video generation with Gen-3 Alpha Turbo, Gen-4 Turbo, and Gen-4 Aleph models.

**[한국어]**

> **최고 등급 AI 영상 품질.** Elo 순위 1위. Gen-3 Alpha Turbo, Gen-4 Turbo, Gen-4 Aleph 모델로 전문급 영상 생성.

**Tools unlocked:** `runway_video`
**Env var:** `RUNWAY_API_KEY`

**[한국어]**

**활성화 도구:** `runway_video`
**환경 변수:** `RUNWAY_API_KEY`

#### Setup (설정)

1. Go to [dev.runwayml.com](https://dev.runwayml.com/) and create a developer account
2. Subscribe to a paid plan (Standard or above — API requires subscription)
3. Generate an API key from the developer portal
4. Add to `.env`: `RUNWAY_API_KEY=key_...`

**[한국어]**

1. [dev.runwayml.com](https://dev.runwayml.com/) 방문 후 개발자 계정 생성
2. 유료 플랜 구독 (Standard 이상 — API는 구독 필요)
3. 개발자 포털에서 API 키 생성
4. `.env`에 추가: `RUNWAY_API_KEY=key_...`

#### Pricing (가격)

| Plan | Price | Credits/month | Video capacity |
|------|-------|---------------|----------------|
| **Free** | $0 | 125 one-time | ~5 seconds Gen-4 |
| Standard | $12/mo | 625 | ~25 seconds Gen-4 |
| Pro | $28/mo | 2,250 | ~90 seconds Gen-4 |
| Unlimited | $76/mo | Unlimited (Explore Mode) | Unlimited Gen-4 Turbo |

**[한국어]**

| 플랜 | 가격 | 월별 크레딧 | 비디오 용량 |
|------|-------|---------------|----------------|
| **Free** | $0 | 125 일회용 | Gen-4 약 5초 |
| Standard | $12/월 | 625 | Gen-4 약 25초 |
| Pro | $28/월 | 2,250 | Gen-4 약 90초 |
| Unlimited | $76/월 | 무제한 (Explore Mode) | Gen-4 Turbo 무제한 |

**API pricing (approximate):**

**[한국어]**

**API 가격 (대략적):**

| Model | Price per second |
|-------|-----------------|
| Gen-3 Alpha Turbo | ~$0.05 |
| Gen-4 Turbo | ~$0.05 |
| Gen-4 Aleph | ~$0.15 |

**[한국어]**

| 모델 | 초당 가격 |
|-------|-----------------|
| Gen-3 Alpha Turbo | ~$0.05 |
| Gen-4 Turbo | ~$0.05 |
| Gen-4 Aleph | ~$0.15 |

**Free tier:** 125 one-time credits (no monthly renewal). Enough for about 5 seconds of Gen-4 video. API access requires a paid subscription.

**[한국어]**

**무료 플랜:** 125 일회용 크레딧 (월간 갱신 없음). Gen-4 영상 약 5초분. API 액세스는 유료 구독이 필요합니다.

---

### Higgsfield — Multi-Model Video Orchestrator

> **Multi-model video platform.** Routes to Kling 3.0, Veo 3.1, Sora 2, WAN 2.5, and proprietary Soul Cinema through a single API. Includes Soul ID for character consistency across clips.

**[한국어]**

> **멀티모델 영상 플랫폼.** 단일 API를 통해 Kling 3.0, Veo 3.1, Sora 2, WAN 2.5, 독점 Soul Cinema로 라우팅합니다. 클립 간 캐릭터 일관성을 위한 Soul ID 포함.

**Tools unlocked:** `higgsfield_video`
**Env vars:** `HIGGSFIELD_API_KEY` + `HIGGSFIELD_API_SECRET` (or combined `HIGGSFIELD_KEY=key:secret`)

**[한국어]**

**활성화 도구:** `higgsfield_video`
**환경 변수:** `HIGGSFIELD_API_KEY` + `HIGGSFIELD_API_SECRET` (또는 결합된 `HIGGSFIELD_KEY=key:secret`)

#### Setup (설정)

1. Go to [cloud.higgsfield.ai](https://cloud.higgsfield.ai/) and create an account
2. Subscribe to a plan (Starter or above for API access)
3. Navigate to API Keys section at [cloud.higgsfield.ai/api-keys](https://cloud.higgsfield.ai/api-keys)
4. Generate an API key and secret
5. Add to `.env`: / 5. `.env`에 추가:
   ```
   HIGGSFIELD_API_KEY=your-api-key
   HIGGSFIELD_API_SECRET=your-api-secret
   ```

**[한국어]**

1. [cloud.higgsfield.ai](https://cloud.higgsfield.ai/) 방문 후 계정 생성
2. 플랜 구독 (API 액세스용 Starter 이상)
3. [cloud.higgsfield.ai/api-keys](https://cloud.higgsfield.ai/api-keys)의 API Keys 섹션으로 이동
4. API 키와 시크릿 생성
5. `.env`에 추가:

#### Pricing (가격)

| Plan | Price | Notes |
|------|-------|-------|
| Free | $0 | Limited credits |
| Starter | $15/mo | Basic allocation |
| Plus | $34/mo | Mid-tier, ~33-56 Kling 3.0 clips |
| Ultra | $84/mo | High volume |

**[한국어]**

| 플랜 | 가격 | 참고 |
|------|-------|-------|
| Free | $0 | 제한된 크레딧 |
| Starter | $15/월 | 기본 할당 |
| Plus | $34/월 | 중간 티어, Kling 3.0 클립 약 33-56개 |
| Ultra | $84/월 | 대량 |

**Per-generation costs (approximate, via credits):**

**[한국어]**

**생성당 비용 (대략적, 크레딧 경유):**

| Model | Cost per clip |
|-------|--------------|
| Kling 3.0 | ~$0.10 (cheapest) |
| WAN 2.5 | ~$0.10 |
| Soul Cinema | ~$0.15 |
| Veo 3.1 | ~$0.50 |
| Sora 2 | ~$0.50 |

**[한국어]**

| 모델 | 클립당 비용 |
|-------|--------------|
| Kling 3.0 | ~$0.10 (가장 저렴) |
| WAN 2.5 | ~$0.10 |
| Soul Cinema | ~$0.15 |
| Veo 3.1 | ~$0.50 |
| Sora 2 | ~$0.50 |

**Free tier:** Limited credits on signup. No monthly renewal on free plan.

**[한국어]**

**무료 플랜:** 가입 시 제한된 크레딧. 무료 플랜에서는 월간 갱신 없음.

---

### HeyGen — Avatar Video Gateway

> **Multi-model video gateway.** Access VEO, Sora, Runway, Kling, and Seedance through a single API.

**[한국어]**

> **멀티모델 영상 게이트웨이.** 단일 API로 VEO, Sora, Runway, Kling, Seedance에 액세스합니다.

**Tools unlocked:** `heygen_video`
**Env var:** `HEYGEN_API_KEY`

**[한국어]**

**활성화 도구:** `heygen_video`
**환경 변수:** `HEYGEN_API_KEY`

#### Setup (설정)

1. Go to [app.heygen.com/register](https://app.heygen.com/register) and create an account
2. Navigate to the API section in settings
3. Generate your API key
4. Add API balance (prepaid, separate from web plan credits)
5. Add to `.env`: `HEYGEN_API_KEY=your-key-here`

**[한국어]**

1. [app.heygen.com/register](https://app.heygen.com/register) 방문 후 계정 생성
2. 설정의 API 섹션으로 이동
3. API 키 생성
4. API 잔액 추가 (선불, 웹 플랜 크레딧과 별개)
5. `.env`에 추가: `HEYGEN_API_KEY=your-key-here`

#### Pricing (가격)

| Service | Price |
|---------|-------|
| Avatar video (Engine III) | $0.017/sec |
| Avatar video (Engine IV) | $0.10/sec |
| Prompt to Video | $0.033/sec |
| Video Translation (Speed) | $0.05/sec |
| Video Translation (Precision) | $0.10/sec |

**[한국어]**

| 서비스 | 가격 |
|---------|-------|
| 아바타 영상 (Engine III) | 초당 $0.017 |
| 아바타 영상 (Engine IV) | 초당 $0.10 |
| 프롬프트 투 비디오 | 초당 $0.033 |
| 비디오 번역 (Speed) | 초당 $0.05 |
| 비디오 번역 (Precision) | 초당 $0.10 |

**Web plans:**

**[한국어]**

**웹 플랜:**

| Plan | Price | Notes |
|------|-------|-------|
| Free | $0 | 1 credit (demo) |
| Creator | $24/mo | Limited credits |
| Business | $72/mo | API access, more credits |

**[한국어]**

| 플랜 | 가격 | 참고 |
|------|-------|-------|
| Free | $0 | 1 크레딧 (데모) |
| Creator | $24/월 | 제한된 크레딧 |
| Business | $72/월 | API 액세스, 더 많은 크레딧 |

**Free tier:** 1 credit on web platform. API is pay-as-you-go with prepaid balance.

**[한국어]**

**무료 플랜:** 웹 플랫폼에서 1 크레딧. API는 선불 잔액이 있는 종량제입니다.

---

### Suno — AI Music Generation

> **Full songs with vocals and lyrics.** Any genre, up to 8 minutes. Instrumentals or vocal tracks.

**[한국어]**

> **보컬과 가사가 있는 완전한 곡.** 모든 장르, 최대 8분. instrumental 또는 보컬 트랙.

**Tools unlocked:** `suno_music`
**Env var:** `SUNO_API_KEY`

**[한국어]**

**활성화 도구:** `suno_music`
**환경 변수:** `SUNO_API_KEY`

#### Setup (설정)

1. Go to [suno.com](https://suno.com) and create a Suno account
2. For API access, go to [sunoapi.org](https://sunoapi.org) and create an account
3. Navigate to the dashboard and copy your API key
4. Add credits (1 credit = $0.005 USD)
5. Add to `.env`: `SUNO_API_KEY=your-key-here`

**[한국어]**

1. [suno.com](https://suno.com) 방문 후 Suno 계정 생성
2. API 액세스를 위해 [sunoapi.org](https://sunoapi.org) 방문 후 계정 생성
3. 대시보드로 이동 후 API 키 복사
4. 크레딧 추가 (1 크레딧 = $0.005 USD)
5. `.env`에 추가: `SUNO_API_KEY=your-key-here`

#### Pricing (가격)

**Suno platform:**

**[한국어]**

**Suno 플랫폼:**

| Plan | Price | Credits | Notes |
|------|-------|---------|-------|
| Free | $0 | 50/day | ~10 songs/day, non-commercial only |
| Pro | $10/mo | 2,500/mo | Commercial license |
| Premier | $30/mo | 10,000/mo | Commercial license |

**[한국어]**

| 플랜 | 가격 | 크레딧 | 참고 |
|------|-------|---------|-------|
| Free | $0 | 50/일 | 하루 ~10곡, 비상업용만 |
| Pro | $10/월 | 2,500/월 | 상업적 라이선스 |
| Premier | $30/월 | 10,000/월 | 상업적 라이선스 |

**API (via sunoapi.org):** Pay-as-you-go, 1 credit = $0.005. Each generation produces 2 tracks.

**[한국어]**

**API (sunoapi.org 경유):** 종량제, 1 크레딧 = $0.005. 생성마다 2개 트랙 생성.

---

### Pexels — Free Stock Media

> **Completely free.** No cost, no attribution required, commercial use allowed.

**[한국어]**

> **완전히 무료.** 비용 없음, 저작자 표시 불필요, 상업적 사용 허용.

**Tools unlocked:** `pexels_image`, `pexels_video`
**Env var:** `PEXELS_API_KEY`

**[한국어]**

**활성화 도구:** `pexels_image`, `pexels_video`
**환경 변수:** `PEXELS_API_KEY`

#### Setup (설정)

1. Go to [pexels.com/join](https://www.pexels.com/join/) and create a free account
2. Navigate to [pexels.com/api](https://www.pexels.com/api/)
3. Click **Your API Key** or request API access
4. Copy your key from the dashboard
5. Add to `.env`: `PEXELS_API_KEY=your-key-here`

**[한국어]**

1. [pexels.com/join](https://www.pexels.com/join/) 방문 후 무료 계정 생성
2. [pexels.com/api](https://www.pexels.com/api/)로 이동
3. **Your API Key** 클릭 또는 API 액세스 요청
4. 대시보드에서 키 복사
5. `.env`에 추가: `PEXELS_API_KEY=your-key-here`

#### Pricing (가격)

**Completely free.** No paid tiers. No attribution required. Commercial use allowed.

**[한국어]**

**완전히 무료.** 유료 플랜 없음. 저작자 표시 불필요. 상업적 사용 허용.

- 200 requests/hour
- 20,000 requests/month
- Photo and video search + download

**[한국어]**

- 시간당 200 요청
- 월 20,000 요청
- 사진 및 비디오 검색 + 다운로드

---

### Pixabay — Free Stock Media

> **Completely free.** 5M+ royalty-free images and videos.

**[한국어]**

> **완전히 무료.** 500만 개 이상의 로열티 무료 이미지와 비디오.

**Tools unlocked:** `pixabay_image`, `pixabay_video`
**Env var:** `PIXABAY_API_KEY`

**[한국어]**

**활성화 도구:** `pixabay_image`, `pixabay_video`
**환경 변수:** `PIXABAY_API_KEY`

#### Setup (설정)

1. Go to [pixabay.com/accounts/register](https://pixabay.com/accounts/register/) and create a free account
2. Navigate to [pixabay.com/api/docs](https://pixabay.com/api/docs/)
3. Your API key is displayed at the top of the docs page (after login)
4. Copy the key
5. Add to `.env`: `PIXABAY_API_KEY=your-key-here`

**[한국어]**

1. [pixabay.com/accounts/register](https://pixabay.com/accounts/register/) 방문 후 무료 계정 생성
2. [pixabay.com/api/docs](https://pixabay.com/api/docs/)로 이동
3. API 키는 문서 페이지 상단에 표시됨 (로그인 후)
4. 키 복사
5. `.env`에 추가: `PIXABAY_API_KEY=your-key-here`

#### Pricing (가격)

**Completely free.** No paid tiers. No attribution required. Commercial use allowed.

**[한국어]**

**완전히 무료.** 유료 플랜 없음. 저작자 표시 불필요. 상업적 사용 허용.

- ~100 requests/minute
- 5,000 requests/hour
- Photo and video search + download
- Standard API limited to 1280px images (full resolution requires editorial API)

**[한국어]**

- 분당 ~100 요청
- 시간당 5,000 요청
- 사진 및 비디오 검색 + 다운로드
- 표준 API는 1280px 이미지로 제한됨 (전체 해상도는 편집 API 필요)

---

## Local Providers (Free, No API Key) (로컬 프로바이더 - 무료, API 키 불필요)

These providers run entirely on your machine. No network, no API key, no cost. Some require a GPU.

**[한국어]**

이 프로바이더들은 완전히 당신의 머신에서 실행됩니다. 네트워크 불필요, API 키 불필요, 비용 무료. 일부는 GPU가 필요합니다.

### Remotion — Programmatic Video Composition

> **React-based video rendering.** Turns still images into animated video with spring physics, animated text cards, stat cards, charts, and transitions. **This is the key fallback when no video generation providers are configured** — the agent generates images and Remotion animates them into professional-looking video.

**[한국어]**

> **React 기반 비디오 렌더링.** 스프링 물리, 애니메이션 텍스트 카드, 스탯 카드, 차트, 전환으로 정지 이미지를 애니메이션 비디오로 변환합니다. **비디오 생성 프로바이더가 설정되지 않았을 때 핵심 대안입니다** — 에이전트가 이미지를 생성하고 Remotion이 전문적인 모습의 비디오로 애니메이션합니다.

**Tool:** `video_compose` (with `operation="render"` — auto-routes to Remotion when needed)
**Runtime:** CPU (Node.js required)
**Env var:** None

**[한국어]**

**도구:** `video_compose` (`operation="render"` 포함 — 필요할 때 자동으로 Remotion으로 라우팅)
**런타임:** CPU (Node.js 필요)
**환경 변수:** 없음

#### Setup (설정)

```bash
# Included in make setup, or install manually:
cd remotion-composer && npm install && cd ..
```

Requires **Node.js 18+** and `npx`. The `remotion-composer/` project is included in the repo.

**[한국어]**

**Node.js 18+**와 `npx` 필요. `remotion-composer/` 프로젝트는 저장소에 포함되어 있습니다.

#### What Remotion Renders (Remotion 렌더링 내용)

| Component | What it produces |
|-----------|-----------------|
| **TextCard** | Animated title/body text with spring physics entrance |
| **StatCard** | Animated statistics with count-up animations |
| **ProgressBar** | Animated progress indicators |
| **CalloutBox** | Highlighted callout panels with icon animations |
| **ComparisonCard** | Side-by-side comparison layouts |
| **BarChart / LineChart / PieChart** | Animated data visualizations |
| **KPIGrid** | Multi-metric dashboard cards |
| **Image scenes** | Still images with spring-animated motion (replaces Ken Burns) |

**[한국어]**

| 컴포넌트 | 생성 내용 |
|-----------|-----------------|
| **TextCard** | 스프링 물리 진입 애니메이션이 있는 제목/본문 텍스트 |
| **StatCard** | 카운트 업 애니메이션이 있는 애니메이션 통계 |
| **ProgressBar** | 애니메이션 진행 표시기 |
| **CalloutBox** | 아이콘 애니메이션이 있는 강조된 호출 패널 |
| **ComparisonCard** | 나란히 비교 레이아웃 |
| **BarChart / LineChart / PieChart** | 애니메이션 데이터 시각화 |
| **KPIGrid** | 다중 메트릭 대시보드 카드 |
| **이미지 장면** | 스프링 애니메이션 모션이 있는 정지 이미지 (Ken Burns 대체) |

#### When Does Remotion Activate? (Remotion이 활성화되는 시기)

The `video_compose` tool's `render` operation auto-detects when Remotion is needed:
- Cuts contain still images (`.png`, `.jpg`, etc.)
- Cuts have `type` set to `text_card`, `stat_card`, `chart`, etc.
- Cuts specify `animation` or `transition_in`/`transition_out`

**[한국어]**

`video_compose` 도구의 `render` 작업은 Remotion이 필요한 시기를 자동 감지합니다:
- 컷이 정지 이미지(`.png`, `.jpg` 등)를 포함할 때
- 컷의 `type`이 `text_card`, `stat_card`, `chart` 등으로 설정되었을 때
- 컷이 `animation` 또는 `transition_in`/`transition_out`을 지정할 때

If Remotion is not installed, compositions fall back to FFmpeg Ken Burns pan-and-zoom — functional but less engaging.

**[한국어]**

Remotion이 설치되지 않으면 컴포지션은 FFmpeg Ken Burns 팬 앤 줌으로 대체됩니다 — 기능적이지만 덜 매력적입니다.

**Cost:** Free. Always local.

**[한국어]**

**비용:** 무료. 항상 로컬.

---

### HyperFrames - HTML/CSS/GSAP Video Composition

> **GSAP-native local rendering.** HyperFrames is the preferred runtime for motion-graphics-heavy HTML compositions and the `character-animation` pipeline's rigged SVG character acting.

**[한국어]**

> **GSAP 네이티브 로컬 렌더링.** HyperFrames는 모션 그래픽이 많은 HTML 컴포지션과 `character-animation` 파이프라인의 리깅된 SVG 캐릭터 연기에 선호되는 런타임입니다.

**Tool:** `hyperframes_compose` directly, or `video_compose` with `edit_decisions.render_runtime="hyperframes"`
**Runtime:** CPU (Node.js >= 22, FFmpeg, and `npx` required)
**Env var:** None

**[한국어]**

**도구:** 직접 `hyperframes_compose`, 또는 `edit_decisions.render_runtime="hyperframes"`가 있는 `video_compose`
**런타임:** CPU (Node.js >= 22, FFmpeg, `npx` 필요)
**환경 변수:** 없음

#### Setup (설정)

```bash
node --version
ffmpeg -version
npx --yes hyperframes doctor
```

The CLI is consumed as `npx hyperframes`. Do not use `npx @hyperframes/cli`; that package name is not the OpenMontage runtime path.

**[한국어]**

CLI는 `npx hyperframes`로 사용합니다. `npx @hyperframes/cli`를 사용하지 마십시오; 해당 패키지 이름은 OpenMontage 런타임 경로가 아닙니다.

#### What HyperFrames Renders (HyperFrames 렌더링 내용)

| Use case | What it produces |
|----------|------------------|
| **Kinetic typography** | HTML/CSS text animation driven by GSAP timelines |
| **Product / launch videos** | Structured HTML scenes, registry blocks, and transitions |
| **Website-to-video** | Browser-captured site compositions with HyperFrames validation |
| **Character animation** | SVG character rigs, pose/action timelines, and GSAP acting beats rendered to `renders/final.mp4` |

**[한국어]**

| 사용 사례 | 생성 내용 |
|----------|------------------|
| **키네틱 타이포그래피** | GSAP 타임라인에 의해 구동되는 HTML/CSS 텍스트 애니메이션 |
| **제품/런치 비디오** | 구조화된 HTML 장면, 레지스트리 블록, 전환 |
| **웹사이트-투-비디오** | HyperFrames 검증이 있는 브라우저 캡처 사이트 컴포지션 |
| **캐릭터 애니메이션** | SVG 캐릭터 리그, 포즈/액션 타임라인, `renders/final.mp4`로 렌더링된 GSAP 연기 비트 |

HyperFrames workspaces live under `projects/<project-name>/hyperframes/`. Final videos still follow the normal OpenMontage convention: `projects/<project-name>/renders/final.mp4`.

**[한국어]**

HyperFrames 워크스페이스는 `projects/<project-name>/hyperframes/` 아래에 있습니다. 최종 비디오는 여전히 일반 OpenMontage 규칙을 따릅니다: `projects/<project-name>/renders/final.mp4`.

**Cost:** Free. Always local.

**[한국어]**

**비용:** 무료. 항상 로컬.

---

### Piper TTS — Offline Text-to-Speech

> **Completely free, fully offline TTS.** No network required. Good quality for drafts and budget-constrained projects.

**[한국어]**

> **완전히 무료, 완전히 오프라인 TTS.** 네트워크 불필요. 초안과 예산 제한 프로젝트에 좋은 품질.

**Tool:** `piper_tts`
**Runtime:** CPU (no GPU needed)
**Env var:** None

**[한국어]**

**도구:** `piper_tts`
**런타임:** CPU (GPU 불필요)
**환경 변수:** 없음

#### Setup (설정)

```bash
# Install via pip
pip install piper-tts

# Or download the binary from GitHub
# https://github.com/rhasspy/piper/releases

# Download a voice model (first run downloads automatically)
piper --download-dir ~/.piper/models --model en_US-lessac-medium
```

**Available voices:** ~30 English voices plus voices for German, French, Spanish, Italian, and other languages. Lower variety than cloud providers but completely free and offline.

**[한국어]**

**사용 가능한 음성:** 약 30개 영어 음성 plus 독일어, 프랑스어, 스페인어, 이탈리아어, 기타 언어 음성. 클라우드 프로바이더보다 다양성은 낮지만 완전히 무료이고 오프라인입니다.

**Quality:** Good for drafts, internal videos, and budget projects. For client-facing narration, use ElevenLabs or Google TTS.

**[한국어]**

**품질:** 초안, 내부 비디오, 예산 프로젝트에 좋음. 클라이언트 대면 내레이션에는 ElevenLabs 또는 Google TTS를 사용하십시오.

---

### Local Video Generation (GPU Required) (로컬 영상 생성 - GPU 필요)

> **Free AI video generation.** Requires an NVIDIA GPU with sufficient VRAM.

**[한국어]**

> **무료 AI 영상 생성.** 충분한 VRAM이 있는 NVIDIA GPU 필요.

**Tools:** `wan_video`, `hunyuan_video`, `cogvideo_video`, `ltx_video_local`
**Runtime:** Local GPU (CUDA required)
**Env vars:** `VIDEO_GEN_LOCAL_ENABLED=true`, `VIDEO_GEN_LOCAL_MODEL=<model>`

**[한국어]**

**도구:** `wan_video`, `hunyuan_video`, `cogvideo_video`, `ltx_video_local`
**런타임:** 로컬 GPU (CUDA 필요)
**환경 변수:** `VIDEO_GEN_LOCAL_ENABLED=true`, `VIDEO_GEN_LOCAL_MODEL=<model>`

#### Setup (설정)

```bash
# 1. Install the GPU stack
make install-gpu
# Or manually:
pip install diffusers transformers accelerate torch pillow requests

# 2. Enable local generation in .env
VIDEO_GEN_LOCAL_ENABLED=true

# 3. Choose a model based on your GPU VRAM
VIDEO_GEN_LOCAL_MODEL=wan2.1-1.3b      # 6GB+ VRAM (entry-level)
VIDEO_GEN_LOCAL_MODEL=wan2.1-14b       # 24GB+ VRAM (best local quality)
VIDEO_GEN_LOCAL_MODEL=hunyuan-1.5      # 12GB+ VRAM
VIDEO_GEN_LOCAL_MODEL=ltx2-local       # 8GB+ VRAM (fastest)
VIDEO_GEN_LOCAL_MODEL=cogvideo-5b      # 10GB+ VRAM
VIDEO_GEN_LOCAL_MODEL=cogvideo-2b      # 6GB+ VRAM (lightest)
```

**[한국어]**

```bash
# 1. Install the GPU stack / 1. GPU 스택 설치
make install-gpu
# Or manually: / 또는 수동:
pip install diffusers transformers accelerate torch pillow requests

# 2. Enable local generation in .env / 2. .env에서 로컬 생성 활성화
VIDEO_GEN_LOCAL_ENABLED=true

# 3. Choose a model based on your GPU VRAM / 3. GPU VRAM에 따라 모델 선택
VIDEO_GEN_LOCAL_MODEL=wan2.1-1.3b      # 6GB+ VRAM (entry-level/입문급)
VIDEO_GEN_LOCAL_MODEL=wan2.1-14b       # 24GB+ VRAM (best local quality/최고 로컬 품질)
VIDEO_GEN_LOCAL_MODEL=hunyuan-1.5      # 12GB+ VRAM
VIDEO_GEN_LOCAL_MODEL=ltx2-local       # 8GB+ VRAM (fastest/가장 빠름)
VIDEO_GEN_LOCAL_MODEL=cogvideo-5b      # 10GB+ VRAM
VIDEO_GEN_LOCAL_MODEL=cogvideo-2b      # 6GB+ VRAM (lightest/가장 가벼움)
```

#### Model Comparison (모델 비교)

| Model | VRAM | Quality | Speed | Best for |
|-------|------|---------|-------|----------|
| **WAN 2.1 (1.3B)** | 6GB | Good | Fast | Entry-level GPU, quick iteration |
| **WAN 2.1 (14B)** | 24GB | Excellent | Slow | Best quality-to-VRAM ratio |
| **Hunyuan 1.5** | 12GB | Very good | Medium | Mid-range GPUs |
| **LTX-2** | 8GB | Good | Fastest | Quick drafts, lowest latency |
| **CogVideo (5B)** | 10GB | Good | Medium | Balanced option |
| **CogVideo (2B)** | 6GB | Fair | Fast | Low-VRAM experimentation |

**[한국어]**

| 모델 | VRAM | 품질 | 속도 | 최적 용도 |
|-------|------|---------|-------|----------|
| **WAN 2.1 (1.3B)** | 6GB | 좋음 | 빠름 | 입문급 GPU, 빠른 반복 |
| **WAN 2.1 (14B)** | 24GB | 우수함 | 느림 | 최고 VRAM 대비 품질 |
| **Hunyuan 1.5** | 12GB | 매우 좋음 | 중간 | 중간 범위 GPU |
| **LTX-2** | 8GB | 좋음 | 가장 빠름 | 빠른 초안, 최저 지연 시간 |
| **CogVideo (5B)** | 10GB | 좋음 | 중간 | 균형적 옵션 |
| **CogVideo (2B)** | 6GB | 양호 | 빠름 | 저 VRAM 실험 |

**All local models support:** Image-to-video, text-to-video, offline generation, seeded reproducibility.

**[한국어]**

**모든 로컬 모델 지원:** 이미지-투-비디오, 텍스트-투-비디오, 오프라인 생성, 시드된 재현성.

---

### Local Diffusion — Offline Image Generation (GPU Required) (로컬 Diffusion - 오프라인 이미지 생성 - GPU 필요)

> **Free Stable Diffusion image generation.** No API cost, fully offline.

**[한국어]**

> **무료 Stable Diffusion 이미지 생성.** API 비용 없음, 완전히 오프라인.

**Tool:** `local_diffusion`
**Runtime:** Local GPU (CUDA required)
**Env var:** None (enable by installing dependencies)

**[한국어]**

**도구:** `local_diffusion`
**런타임:** 로컬 GPU (CUDA 필요)
**환경 변수:** 없음 (의존성 설치로 활성화)

#### Setup (설정)

```bash
pip install diffusers transformers accelerate torch
```

First run downloads the model (~4GB). Subsequent runs use the cached model.

**[한국어]**

첫 실행은 모델을 다운로드합니다 (~4GB). 이후 실행은 캐시된 모델을 사용합니다.

**VRAM requirement:** 4GB+ (8GB recommended for 1024x1024 images)

**[한국어]**

**VRAM 요구 사항:** 4GB+ (1024x1024 이미지에는 8GB 권장)

**Supports:** Negative prompts, seeds, custom sizes. Quality is lower than FLUX or GPT Image 2 but completely free and offline.

**[한국어]**

**지원:** 부정 프롬프트, 시드, 사용자 정의 크기. FLUX나 GPT Image 2보다 품질은 낮지만 완전히 무료이고 오프라인입니다.

---

### LTX-2 on Modal — Self-Hosted Cloud GPU

> **Run LTX-2 on Modal's cloud GPUs.** Your own endpoint, your own scale. More consistent than local GPU, cheaper than commercial APIs.

**[한국어]**

> **Modal의 클라우드 GPU에서 LTX-2 실행.** 당신 자신의 엔드포인트, 당신 자신의 규모. 로컬 GPU보다 더 일관적, 상업 API보다 저렴.

**Tool:** `ltx_video_modal`
**Runtime:** Cloud (self-hosted)
**Env var:** `MODAL_LTX2_ENDPOINT_URL`

**[한국어]**

**도구:** `ltx_video_modal`
**런타임:** 클라우드 (셀프 호스트)
**환경 변수:** `MODAL_LTX2_ENDPOINT_URL`

#### Setup (설정)

1. Create a [Modal](https://modal.com) account
2. Deploy the LTX-2 endpoint (see Modal docs)
3. Set the endpoint URL in `.env`: `MODAL_LTX2_ENDPOINT_URL=https://your-modal-endpoint`

**[한국어]**

1. [Modal](https://modal.com) 계정 생성
2. LTX-2 엔드포인트 배포 (Modal 문서 참조)
3. `.env`에 엔드포인트 URL 설정: `MODAL_LTX2_ENDPOINT_URL=https://your-modal-endpoint`

**Modal pricing:** ~$0.99/hour for A100 GPU time. Cost per video depends on generation time.

**[한국어]**

**Modal 가격:** A100 GPU 시간당 ~$0.99. 비디오당 비용은 생성 시간에 따라 다릅니다.

---

### Other Local Tools (Always Available) (기타 로컬 도구 - 항상 사용 가능)

These tools require only FFmpeg or Python packages — no GPU, no API key.

**[한국어]**

이 도구들은 FFmpeg나 Python 패키지만 필요로 합니다 — GPU 불필요, API 키 불필요.

| Tool | Install | What it does |
|------|---------|-------------|
| **FFmpeg tools** (video_compose, video_stitch, video_trimmer, audio_mixer, audio_enhance, color_grade, face_enhance, frame_sampler, scene_detect) | `brew install ffmpeg` / `sudo apt install ffmpeg` / `winget install FFmpeg` | Video editing, audio processing, color grading, analysis |
| **Transcriber** | `pip install faster-whisper` | Speech-to-text with word-level timestamps |
| **Background Remove** | `pip install rembg` (CPU) or `pip install rembg[gpu]` | Remove image/video backgrounds |
| **Upscale** | `pip install realesrgan` (requires PyTorch + CUDA) | Real-ESRGAN image/video upscaling |
| **Face Restore** | `pip install gfpgan` (requires PyTorch) | CodeFormer/GFPGAN face restoration |
| **Code Snippet** | `pip install Pygments Pillow` | Syntax-highlighted code images |
| **Diagram Gen** | `npm install -g @mermaid-js/mermaid-cli` | Mermaid diagram rendering |
| **Math Animate** | `pip install manim` | ManimCE mathematical animations |
| **Subtitle Gen** | No install needed | SRT/VTT subtitle file generation |
| **Video Understand** | `pip install transformers torch` | CLIP/BLIP-2 visual analysis |
| **Talking Head** | Clone [SadTalker](https://github.com/OpenTalker/SadTalker) | Avatar animation from photo + audio |
| **Lip Sync** | Clone [Wav2Lip](https://github.com/Rudrabha/Wav2Lip) | Audio-driven lip synchronization |

**[한국어]**

| 도구 | 설치 | 기능 |
|------|---------|-------------|
| **FFmpeg 도구** (video_compose, video_stitch, video_trimmer, audio_mixer, audio_enhance, color_grade, face_enhance, frame_sampler, scene_detect) | `brew install ffmpeg` / `sudo apt install ffmpeg` / `winget install FFmpeg` | 비디오 편집, 오디오 처리, 색 보정, 분석 |
| **Transcriber** | `pip install faster-whisper` | 단어 단위 타임스탬프가 있는 음성-투-텍스트 |
| **Background Remove** | `pip install rembg` (CPU) 또는 `pip install rembg[gpu]` | 이미지/비디오 배경 제거 |
| **Upscale** | `pip install realesrgan` (PyTorch + CUDA 필요) | Real-ESRGAN 이미지/비디오 업스케일링 |
| **Face Restore** | `pip install gfpgan` (PyTorch 필요) | CodeFormer/GFPGAN 얼굴 복원 |
| **Code Snippet** | `pip install Pygments Pillow` | 구문 강조 코드 이미지 |
| **Diagram Gen** | `npm install -g @mermaid-js/mermaid-cli` | Mermaid 다이어그램 렌더링 |
| **Math Animate** | `pip install manim` | ManimCE 수학 애니메이션 |
| **Subtitle Gen** | 설치 불필요 | SRT/VTT 자막 파일 생성 |
| **Video Understand** | `pip install transformers torch` | CLIP/BLIP-2 시각적 분석 |
| **Talking Head** | [SadTalker](https://github.com/OpenTalker/SadTalker) 복제 | 사진 + 오디오에서 아바타 애니메이션 |
| **Lip Sync** | [Wav2Lip](https://github.com/Rudrabha/Wav2Lip) 복제 | 오디오 구동 립 싱크 |

---

## Provider-to-Tool Mapping (프로바이더-도구 매핑)

| Provider | Env Var | Tools Unlocked | Cost |
|----------|---------|---------------|------|
| **Pexels** | `PEXELS_API_KEY` | `pexels_image`, `pexels_video` | Free |
| **Pixabay** | `PIXABAY_API_KEY` | `pixabay_image`, `pixabay_video` | Free |
| **Piper** | — (install only) | `piper_tts` | Free |
| **Google** | `GOOGLE_API_KEY` (or `GEMINI_API_KEY`) | `google_tts`, `google_imagen`, `google_music`, `gemini_omni_video`, `veo_video` | Free tier (TTS) + paid |
| **ElevenLabs** | `ELEVENLABS_API_KEY` | `elevenlabs_tts`, `music_gen` | Free tier + paid |
| **fal.ai** | `FAL_KEY` | `flux_image`, `recraft_image`, `kling_video`, `veo_video`, `minimax_video` | Pay-as-you-go |
| **Kling Official** | `KLING_API_KEY` | `kling_official_video`, `kling_official_image`, `kling_tts`, `kling_avatar`, `kling_lip_sync` | Pay-as-you-go |
| **OpenAI** | `OPENAI_API_KEY` | `openai_tts`, `openai_image` | Paid only |
| **xAI** | `XAI_API_KEY` | `grok_image`, `grok_video` | Paid only |
| **Runway** | `RUNWAY_API_KEY` | `runway_video` | Free trial + paid |
| **Higgsfield** | `HIGGSFIELD_API_KEY` + `HIGGSFIELD_API_SECRET` | `higgsfield_video` | Subscription ($15-84/mo) |
| **HeyGen** | `HEYGEN_API_KEY` | `heygen_video` | Pay-as-you-go |
| **Suno** | `SUNO_API_KEY` | `suno_music` | Pay-as-you-go |
| **Local GPU** | `VIDEO_GEN_LOCAL_ENABLED` | `wan_video`, `hunyuan_video`, `cogvideo_video`, `ltx_video_local` | Free (GPU required) |
| **Local Diffusion** | — (install only) | `local_diffusion` | Free (GPU required) |
| **Modal** | `MODAL_LTX2_ENDPOINT_URL` | `ltx_video_modal` | Self-hosted cloud |

**[한국어]**

| 프로바이더 | 환경 변수 | 활성화 도구 | 비용 |
|----------|---------|---------------|------|
| **Pexels** | `PEXELS_API_KEY` | `pexels_image`, `pexels_video` | 무료 |
| **Pixabay** | `PIXABAY_API_KEY` | `pixabay_image`, `pixabay_video` | 무료 |
| **Piper** | — (설치만) | `piper_tts` | 무료 |
| **Google** | `GOOGLE_API_KEY` (또는 `GEMINI_API_KEY`) | `google_tts`, `google_imagen`, `google_music`, `gemini_omni_video`, `veo_video` | 무료 플랜 (TTS) + 유료 |
| **ElevenLabs** | `ELEVENLABS_API_KEY` | `elevenlabs_tts`, `music_gen` | 무료 플랜 + 유료 |
| **fal.ai** | `FAL_KEY` | `flux_image`, `recraft_image`, `kling_video`, `veo_video`, `minimax_video` | 종량제 |
| **Kling Official** | `KLING_API_KEY` | `kling_official_video`, `kling_official_image`, `kling_tts`, `kling_avatar`, `kling_lip_sync` | 종량제 |
| **OpenAI** | `OPENAI_API_KEY` | `openai_tts`, `openai_image` | 유료 전용 |
| **xAI** | `XAI_API_KEY` | `grok_image`, `grok_video` | 유료 전용 |
| **Runway** | `RUNWAY_API_KEY` | `runway_video` | 무료 체험 + 유료 |
| **Higgsfield** | `HIGGSFIELD_API_KEY` + `HIGGSFIELD_API_SECRET` | `higgsfield_video` | 구독 ($15-84/월) |
| **HeyGen** | `HEYGEN_API_KEY` | `heygen_video` | 종량제 |
| **Suno** | `SUNO_API_KEY` | `suno_music` | 종량제 |
| **로컬 GPU** | `VIDEO_GEN_LOCAL_ENABLED` | `wan_video`, `hunyuan_video`, `cogvideo_video`, `ltx_video_local` | 무료 (GPU 필요) |
| **로컬 Diffusion** | — (설치만) | `local_diffusion` | 무료 (GPU 필요) |
| **Modal** | `MODAL_LTX2_ENDPOINT_URL` | `ltx_video_modal` | 셀프 호스트 클라우드 |

---

## Capability Coverage (기능 커버리지)

How many providers cover each capability:

**[한국어]**

각 기능을 커버하는 프로바이더 수:

| Capability | Cloud Providers | Local Providers | Free Options |
|-----------|----------------|-----------------|--------------|
| **Image Generation** | FLUX, Kling Official, Grok, Google Imagen, GPT Image 2, Recraft | Local Diffusion | Pexels, Pixabay (stock) |
| **Video Generation** | Grok, Kling Official, Kling via fal.ai, Runway, Veo, Gemini Omni, Higgsfield, MiniMax, HeyGen | WAN, Hunyuan, CogVideo, LTX | Pexels, Pixabay (stock) |
| **Text-to-Speech** | ElevenLabs, Google TTS, Kling Official, OpenAI | Piper | Piper, Google free tier, ElevenLabs free tier |
| **Music Generation** | ElevenLabs, Suno, Google Lyria | — | ElevenLabs free tier |
| **Post-Production** | — | FFmpeg (compose, stitch, trim, mix, enhance, grade) | All free |
| **Analysis** | — | WhisperX, Scene Detect, Frame Sampler, CLIP/BLIP-2 | All free |
| **Enhancement** | — | Upscale, BG Remove, Face Enhance, Face Restore | All free |
| **Avatar** | Kling Official | SadTalker, Wav2Lip | Local tools are free |

**[한국어]**

| 기능 | 클라우드 프로바이더 | 로컬 프로바이더 | 무료 옵션 |
|-----------|----------------|-----------------|--------------|
| **이미지 생성** | FLUX, Kling Official, Grok, Google Imagen, GPT Image 2, Recraft | Local Diffusion | Pexels, Pixabay (스톡) |
| **영상 생성** | Grok, Kling Official, fal.ai 경유 Kling, Runway, Veo, Gemini Omni, Higgsfield, MiniMax, HeyGen | WAN, Hunyuan, CogVideo, LTX | Pexels, Pixabay (스톡) |
| **텍스트-투-스피치** | ElevenLabs, Google TTS, Kling Official, OpenAI | Piper | Piper, Google 무료 플랜, ElevenLabs 무료 플랜 |
| **음악 생성** | ElevenLabs, Suno, Google Lyria | — | ElevenLabs 무료 플랜 |
| **후반 작업** | — | FFmpeg (compose, stitch, trim, mix, enhance, grade) | 전부 무료 |
| **분석** | — | WhisperX, Scene Detect, Frame Sampler, CLIP/BLIP-2 | 전부 무료 |
| **향상** | — | Upscale, BG Remove, Face Enhance, Face Restore | 전부 무료 |
| **아바타** | Kling Official | SadTalker, Wav2Lip | 로컬 도구는 무료 |

---

## FAQ

**Q: What's the absolute minimum I need to produce a video?**
A: FFmpeg + Node.js (both free, local). FFmpeg handles video assembly, audio mixing, and subtitles. With Node.js, Remotion renders still images into animated video — so even without any video generation API, the agent generates images and Remotion turns them into professional-looking video with spring animations, text cards, and transitions. Add Piper TTS for free narration and Pexels/Pixabay for free stock footage.

**[한국어]**

**Q: 영상을 만드는 데 절대 최소한으로 필요한 것은 무엇인가요?**
A: FFmpeg + Node.js (둘 다 무료, 로컬). FFmpeg는 비디오 조립, 오디오 믹싱, 자막을 처리합니다. Node.js가 있으면 Remotion이 정지 이미지를 애니메이션 비디오로 렌더링합니다 — 따라서 비디오 생성 API가 없어도 에이전트가 이미지를 생성하고 Remotion이 스프링 애니메이션, 텍스트 카드, 전환으로 전문적인 모습의 비디오로 만듭니다. 무료 내레이션에는 Piper TTS, 무료 스톡 영상에는 Pexels/Pixabay를 추가하십시오.

**Q: I don't have any video generation providers. Can I still make videos?**
A: Yes. The agent generates still images (via any image provider — even free stock from Pexels/Pixabay) and Remotion composes them into animated video with spring physics transitions, text cards, stat cards, and charts. This is the default path for explainer and animation pipelines when no video gen is configured.

**[한국어]**

**Q: 비디오 생성 프로바이더가 없습니다. 그래도 비디오를 만들 수 있나요?**
A: 네. 에이전트가 정지 이미지를 생성(어떤 이미지 프로바이더라도 가능 — Pexels/Pixabay의 무료 스톡도)하고 Remotion이 스프링 물리 전환, 텍스트 카드, 스탯 카드, 차트로 애니메이션 비디오로 구성합니다. 비디오 생성이 설정되지 않은 경우 설명 및 애니메이션 파이프라인의 기본 경로입니다.

**Q: What's one low-friction way to get AI-generated images and video?**
A: fal.ai (`FAL_KEY`) is one pay-as-you-go option with broad single-key coverage. It unlocks FLUX images plus multiple video providers. No subscription — pay only for what you generate.

**[한국어]**

**Q: AI 생성 이미지와 비디오를 얻는 한 가지 저마찰 방법은 무엇인가요?**
A: fal.ai (`FAL_KEY`)는 광범위한 단일 키 커버리지가 있는 종량제 옵션입니다. FLUX 이미지와 여러 비디오 프로바이더를 활성화합니다. 구독 없음 — 생성하는 것에 대해서만 지불하십시오.

**Q: I have a GPU. What can I run locally for free?**
A: Set `VIDEO_GEN_LOCAL_ENABLED=true` and install `diffusers`. You get WAN 2.1, Hunyuan, CogVideo, and LTX video generation plus Stable Diffusion image generation — all free, all offline.

**[한국어]**

**Q: GPU가 있습니다. 로컬에서 무료로 무엇을 실행할 수 있나요?**
A: `VIDEO_GEN_LOCAL_ENABLED=true`로 설정하고 `diffusers`를 설치하십시오. WAN 2.1, Hunyuan, CogVideo, LTX 비디오 생성과 Stable Diffusion 이미지 생성을 얻습니다 — 전부 무료, 전부 오프라인.

**Q: Which TTS provider should I use?**
A: For quality → ElevenLabs. For localization (50+ languages) → Google TTS. For budget → Google free tier (1M chars/month). For offline → Piper.

**[한국어]**

**Q: 어떤 TTS 프로바이더를 사용해야 하나요?**
A: 품질 → ElevenLabs. 현지화 (50개 이상 언어) → Google TTS. 예산 → Google 무료 플랜 (월 100만 자). 오프라인 → Piper.

**Q: Do I need all these providers?**
A: No. Start with what you have. The selector pattern auto-routes to whatever's available. Missing a provider? The system falls through to the next one automatically.

**[한국어]**

**Q: 이 모든 프로바이더가 필요한가요?**
A: 아니요. 가진 것으로 시작하십시오. 선택자 패턴은 사용 가능한 것으로 자동 라우팅합니다. 프로바이더가 없나요? 시스템이 자동으로 다음 것으로 넘어갑니다.