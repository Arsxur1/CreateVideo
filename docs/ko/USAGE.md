> 안내: 이 문서는 이중 언어 문서입니다. 각 섹션에서 영어 원문이 먼저 나오고, **[한국어]** 표시 아래에 한국어 번역이 이어집니다.

> 원본: (한국어 오리지널 — 대응 원본 없음)

# OpenMontage Usage Guide (OpenMontage 사용 가이드)

Related guides: [Kimi Setup Guide (KIMI-SETUP.md)](KIMI-SETUP.md) · [Bilingual Korean README (README_ko.md)](../../README_ko.md)

관련 문서: [Kimi 설정 가이드 (KIMI-SETUP.md)](KIMI-SETUP.md) · [이중언어 한국어 README (README_ko.md)](../../README_ko.md)

---

## 1. What OpenMontage Is (OpenMontage란)

OpenMontage is a free, open-source system that turns an AI coding assistant (Claude Code, Cursor, Copilot, Windsurf, or Codex) into a full video production studio. You describe the video you want in plain language — Korean works fine — and the agent researches the topic, writes the script, generates or finds the visuals, records narration, edits, and renders a finished MP4. It can animate still images, but it can also cut together real motion footage from free stock sites and open archives into an actual video. You approve every creative decision before anything is spent or rendered.

**[한국어]**

OpenMontage는 Claude Code, Cursor, Copilot, Windsurf, Codex 같은 AI 코딩 어시스턴트를 영상 제작 스튜디오로 바꿔 주는 무료 오픈소스 프로젝트입니다. 만들고 싶은 영상을 말로 설명하면(한국어도 됩니다) 에이전트가 자료 조사, 대본 작성, 시각 자료 준비, 내레이션 녹음, 편집, 최종 MP4 렌더링까지 전부 처리합니다. 이미지를 움직여 만드는 영상뿐 아니라, 무료 스톡 사이트와 공개 아카이브에서 실제 영상 클립을 모아 편집한 진짜 영상도 만들 수 있습니다. 비용이 들거나 렌더링이 시작되기 전에는 항상 사용자의 승인을 받습니다.

---

## 2. Requirements (준비물)

You need four things installed on your Windows 11 machine:

- **Python 3.10+** — download the Windows installer from [python.org/downloads](https://www.python.org/downloads/). During installation, tick the **"Add python.exe to PATH"** checkbox.
- **FFmpeg** — download from [ffmpeg.org/download.html](https://ffmpeg.org/download.html), or install from PowerShell with `winget install FFmpeg`.
- **Node.js 18+** — download the LTS installer from [nodejs.org](https://nodejs.org/). Pick the newest LTS: the HyperFrames render engine needs Node.js 22+, and the current LTS covers both.
- **An AI coding assistant** — Claude Code, Cursor, Copilot, Windsurf, or Codex. This is what actually drives OpenMontage; there is no separate app to open.

**[한국어]**

Windows 11 컴퓨터에 네 가지가 설치되어 있어야 합니다.

- **Python 3.10 이상** — [python.org/downloads](https://www.python.org/downloads/)에서 Windows 설치 파일을 받습니다. 설치할 때 **"Add python.exe to PATH"** 체크박스를 꼭 선택하세요.
- **FFmpeg** — [ffmpeg.org/download.html](https://ffmpeg.org/download.html)에서 받거나, PowerShell에서 `winget install FFmpeg`를 실행하면 됩니다.
- **Node.js 18 이상** — [nodejs.org](https://nodejs.org/)에서 LTS 설치 파일을 받습니다. HyperFrames 렌더링 엔진은 Node.js 22 이상을 요구하니, 최신 LTS를 설치하는 게 안전합니다.
- **AI 코딩 어시스턴트** — Claude Code, Cursor, Copilot, Windsurf, Codex 중 하나입니다. OpenMontage는 별도 앱을 여는 방식이 아니라, 이 어시스턴트가 직접 구동합니다.

---

## 3. Install on Windows (Windows에 설치하기)

Open PowerShell, clone the repository, and enter it:

```powershell
git clone https://github.com/calesthio/OpenMontage.git
cd OpenMontage
```

Then run this one line in PowerShell (from the README):

```powershell
py -3 -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt; cd remotion-composer; npm install; cd ..; python -m pip install piper-tts; Copy-Item .env.example .env
```

That single line creates a virtual environment, activates it, installs the Python dependencies, installs the Remotion composer (Node.js side), installs the free Piper TTS, and creates your `.env` file from `.env.example`.

On macOS/Linux the equivalent is:

```bash
python3 -m venv .venv && source .venv/bin/activate && python -m pip install -r requirements.txt && cd remotion-composer && npm install && cd .. && python -m pip install piper-tts && cp .env.example .env
```

If `npm install` fails on Windows with `ERR_INVALID_ARG_TYPE`, use `npx --yes npm install` instead (inside the `remotion-composer` folder).

Where `make` is available (macOS/Linux by default, Windows if you installed make), `make setup` is the shortcut that does the whole sequence for you.

**[한국어]**

PowerShell을 열고 저장소를 복제한 뒤 해당 폴더로 들어갑니다.

```powershell
git clone https://github.com/calesthio/OpenMontage.git
cd OpenMontage
```

그다음 PowerShell에서 아래 한 줄을 그대로 실행합니다(README에 있는 명령어입니다).

```powershell
py -3 -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt; cd remotion-composer; npm install; cd ..; python -m pip install piper-tts; Copy-Item .env.example .env
```

이 한 줄이 가상환경 생성, 활성화, Python 의존성 설치, Remotion composer 설치(Node.js 쪽), 무료 Piper TTS 설치, `.env.example`을 복사한 `.env` 생성까지 전부 해 줍니다.

macOS/Linux에서는 아래 명령이 같은 일을 합니다.

```bash
python3 -m venv .venv && source .venv/bin/activate && python -m pip install -r requirements.txt && cd remotion-composer && npm install && cd .. && python -m pip install piper-tts && cp .env.example .env
```

Windows에서 `npm install`이 `ERR_INVALID_ARG_TYPE` 오류로 실패하면, (`remotion-composer` 폴더 안에서) `npx --yes npm install`을 대신 실행하세요.

`make`가 있는 환경(macOS/Linux는 기본, Windows는 make를 따로 설치한 경우)에서는 `make setup` 한 번이 이 전체 과정을 대신해 줍니다.

---

## 4. API Keys (API 키 설정)

Keys live in the `.env` file in the OpenMontage folder. Setup already created it by copying `.env.example`; open it in any editor and paste keys in, one per line, like `PEXELS_API_KEY=your-key-here`. Every key is optional — add only what you have.

**Start with zero keys.** Out of the box, `make setup` (or the one-liner above) already gives you a complete free toolchain:

| Capability | Free Tool | What It Does |
|-----------|-----------|-------------|
| **Narration** | Piper TTS | Free offline text-to-speech — real human-sounding narration |
| **Open footage** | Archive.org + NASA + Wikimedia Commons | Free/open archival footage, educational media, and documentary texture |
| **Extra stock** | Pexels + Unsplash + Pixabay | Free stock footage/images (developer keys are free to get) |
| **Composition (React)** | Remotion | React-based rendering — spring-animated image scenes, text cards, stat cards, charts, TikTok-style word-level captions, TalkingHead |
| **Composition (HTML/GSAP)** | HyperFrames | HTML/CSS/GSAP rendering — kinetic typography, product promos, launch reels, registry blocks, website-to-video, rigged SVG character animation |
| **Post-production** | FFmpeg | Encoding, subtitle burn-in, audio mixing, color grading |
| **Subtitles** | Built-in | Auto-generated captions with word-level timing |

**Free keys worth getting.** These three cost nothing and noticeably improve the footage the agent can pull:

- `PEXELS_API_KEY` — create a free account at [pexels.com/join](https://www.pexels.com/join/), then get your key at [pexels.com/api](https://www.pexels.com/api/). Completely free (200 requests/hour, 20,000/month).
- `PIXABAY_API_KEY` — register free at [pixabay.com/accounts/register](https://pixabay.com/accounts/register/); your key is shown at the top of [pixabay.com/api/docs](https://pixabay.com/api/docs/) after login. Completely free.
- `UNSPLASH_ACCESS_KEY` — a free developer key from Unsplash (register an app on the Unsplash developer portal at [unsplash.com/developers](https://unsplash.com/developers)).

**Paid keys, if you want AI-generated visuals or premium voices.** One table, pick what you need:

| Env var | What it unlocks | Cost |
|---------|-----------------|------|
| `FAL_KEY` | FLUX images + Kling/Veo/MiniMax video + Recraft images via fal.ai | Pay-as-you-go, images from ~$0.03 |
| `GOOGLE_API_KEY` | Google TTS (700+ voices, 50+ languages incl. Korean), Imagen images, Lyria music, Veo/Gemini Omni video | TTS free tier 1M chars/month + paid; $300 new-account credit |
| `ELEVENLABS_API_KEY` | Premium TTS, AI music, sound effects | 10K chars/month free, paid plans from $5/month |
| `OPENAI_API_KEY` | OpenAI TTS, GPT Image 2 images | Paid only (TTS from $12/1M chars, images from ~$0.005) |
| `XAI_API_KEY` | Grok image generation/editing + Grok video | Paid only |
| `KLING_API_KEY` | Official Kling video, image, TTS, avatar, lip sync | Pay-as-you-go |
| `RUNWAY_API_KEY` | Runway Gen-4 video | Subscription from $12/month |
| `HEYGEN_API_KEY` | HeyGen multi-model video gateway | Pay-as-you-go |
| `SUNO_API_KEY` | Suno full-song music generation | Pay-as-you-go |

The full provider guide with signup links and pricing is in [`docs/PROVIDERS.md`](../PROVIDERS.md).

**[한국어]**

키는 OpenMontage 폴더의 `.env` 파일에 넣습니다. 설치 과정에서 `.env.example`을 복사해 `.env`가 이미 만들어져 있으니, 메모장이나 편집기로 열어서 `PEXELS_API_KEY=발급받은키`처럼 한 줄에 하나씩 붙여 넣으면 됩니다. 모든 키는 선택 사항이고, 가진 것만 적으면 됩니다.

**키 없이 시작하기.** `make setup`(또는 위의 한 줄 설치)만 끝나도 아래 표의 무료 도구들이 전부 준비됩니다.

| 기능 | 무료 도구 | 하는 일 |
|------|-----------|---------|
| **내레이션** | Piper TTS | 무료 오프라인 TTS — 실제 사람 같은 내레이션 |
| **공개 영상 소스** | Archive.org + NASA + Wikimedia Commons | 무료/공개 아카이브 영상, 교육용 미디어, 다큐멘터리 소재 |
| **추가 스톡** | Pexels + Unsplash + Pixabay | 무료 스톡 영상/이미지(개발자 키는 무료로 발급 가능) |
| **컴포지션 (React)** | Remotion | React 기반 렌더링 — 스프링 애니메이션 이미지 씬, 텍스트 카드, 스탯 카드, 차트, TikTok 스타일 단어 단위 자막, TalkingHead |
| **컴포지션 (HTML/GSAP)** | HyperFrames | HTML/CSS/GSAP 렌더링 — 키네틱 타이포그래피, 제품 프로모, 론치 릴, 레지스트리 블록, 웹사이트-투-비디오, 리깅된 SVG 캐릭터 애니메이션 |
| **후반 작업** | FFmpeg | 인코딩, 자막 입히기, 오디오 믹싱, 색 보정 |
| **자막** | 내장 | 단어 단위 타이밍이 있는 자동 자막 |

**받아 두면 좋은 무료 키 3개.** 세 개 다 비용이 없고, 에이전트가 가져올 수 있는 영상 소스가 눈에 띄게 넓어집니다.

- `PEXELS_API_KEY` — [pexels.com/join](https://www.pexels.com/join/)에서 무료 계정을 만들고, [pexels.com/api](https://www.pexels.com/api/)에서 키를 발급받습니다. 완전 무료입니다(시간당 200건, 월 20,000건 요청 가능).
- `PIXABAY_API_KEY` — [pixabay.com/accounts/register](https://pixabay.com/accounts/register/)에서 무료 가입 후, [pixabay.com/api/docs](https://pixabay.com/api/docs/) 페이지 상단에 표시되는 키를 복사합니다. 완전 무료입니다.
- `UNSPLASH_ACCESS_KEY` — Unsplash 개발자 포털([unsplash.com/developers](https://unsplash.com/developers))에서 앱을 등록하면 무료로 발급됩니다.

**유료 키 — AI 생성 비주얼이나 고품질 음성이 필요할 때.** 필요한 것만 선택해 쓰면 됩니다.

| 환경 변수 | 열리는 기능 | 비용 |
|-----------|-------------|------|
| `FAL_KEY` | fal.ai를 통한 FLUX 이미지 + Kling/Veo/MiniMax 영상 + Recraft 이미지 | 종량제, 이미지 장당 약 $0.03부터 |
| `GOOGLE_API_KEY` | Google TTS(음성 700개 이상, 언어 50개 이상 — 한국어 포함), Imagen 이미지, Lyria 음악, Veo/Gemini Omni 영상 | TTS는 월 100만 자 무료 + 유료, 신규 계정 $300 크레딧 |
| `ELEVENLABS_API_KEY` | 프리미엄 TTS, AI 음악, 효과음 | 월 1만 자 무료, 유료는 $5/월부터 |
| `OPENAI_API_KEY` | OpenAI TTS, GPT Image 2 이미지 | 유료 전용(TTS 100만 자당 $12부터, 이미지 장당 약 $0.005부터) |
| `XAI_API_KEY` | Grok 이미지 생성/편집 + Grok 영상 | 유료 전용 |
| `KLING_API_KEY` | Kling 공식 영상, 이미지, TTS, 아바타, 립싱크 | 종량제 |
| `RUNWAY_API_KEY` | Runway Gen-4 영상 | 구독 $12/월부터 |
| `HEYGEN_API_KEY` | HeyGen 멀티모델 영상 게이트웨이 | 종량제 |
| `SUNO_API_KEY` | Suno 완곡 음악 생성 | 종량제 |

가입 링크와 가격이 정리된 전체 프로바이더 가이드는 [`docs/PROVIDERS.md`](../PROVIDERS.md)에 있습니다.

---

## 5. How to Actually Make a Video (실제로 영상 만들기)

Open the OpenMontage folder in your AI coding assistant (File → Open Folder), then type what you want in the chat. Korean requests work — the agent understands them and runs the same pipeline.

Copy any of these prompts:

1. **Zero-key animated explainer** (free, works immediately):

> "Make a 45-second animated explainer about why the sky is blue"

2. **Real-footage documentary montage** (free, uses stock/archival clips):

> "Make a 75-second documentary montage about city life in the rain. Use real footage only, no narration, elegiac tone, with music."

3. **Start from a reference video** (paste a YouTube/Shorts/Reels/TikTok link with it):

> "Here's a YouTube short I love. Make me something like this, but about CRISPR for high school students."

4. **Korean-narration explainer:**

> "Create a 60-second video about the history of the internet, with Korean narration and Korean captions"

Korean narration needs a TTS provider whose voices cover Korean. Google TTS explicitly lists Korean among its 50+ languages and has a generous free tier (1M characters/month), so it is the safest pick. ElevenLabs' multilingual voices are the premium alternative. Piper — the free, offline default — documents English plus a few European languages, and Korean is not on that list, so don't count on Piper for Korean voiceover.

5. **Data-driven explainer** (zero-key friendly):

> "Make a data-driven explainer about coffee consumption around the world"

6. **Product teaser** (needs one image provider, e.g. `FAL_KEY`):

> "Make a product launch teaser for a fictional smart water bottle called AquaPulse"

**[한국어]**

AI 코딩 어시스턴트에서 OpenMontage 폴더를 열고(File → Open Folder), 채팅창에 만들고 싶은 영상을 적으면 됩니다. 한국어로 써도 됩니다. 에이전트가 알아듣고 같은 파이프라인을 돌립니다.

아래 프롬프트 중 아무거나 복사해 쓰세요.

1. **키 없이 만드는 애니메이션 설명 영상**(무료, 바로 실행 가능):

> "하늘이 파란 이유를 설명하는 45초짜리 애니메이션 영상 만들어 줘"

2. **실사 다큐멘터리 몽타주**(무료, 스톡/아카이브 클립 사용):

> "비 오는 도시의 모습을 담은 75초 다큐멘터리 몽타주 만들어 줘. 실사 영상만 쓰고, 내레이션 없이, 음악은 넣고, 애수 어린 분위기로."

3. **레퍼런스 영상에서 출발하기**(YouTube/Shorts/Reels/TikTok 링크를 함께 붙여 넣기):

> "이 유튜브 쇼츠가 마음에 들어. 고등학생에게 CRISPR를 설명하는 영상으로 비슷하게 만들어 줘."

4. **한국어 내레이션 설명 영상:**

> "인터넷의 역사를 다루는 60초 영상을 만들어 줘. 한국어 내레이션과 한국어 자막을 넣어 줘."

한국어 내레이션을 쓰려면 한국어 음성을 지원하는 TTS 프로바이더가 필요합니다. Google TTS는 50개 이상 언어 목록에 한국어가 명시되어 있고 무료 한도도 넉넉해서(월 100만 자) 가장 안전한 선택입니다. ElevenLabs의 다국어 음성이 프리미엄 대안입니다. 무료 오프라인 기본값인 Piper는 영어와 일부 유럽 언어 중심이라 한국어가 목록에 없으니, 한국어 내레이션에 Piper를 기대하면 안 됩니다.

5. **데이터 기반 설명 영상**(키 없이 가능):

> "전 세계 커피 소비에 대한 데이터 기반 설명 영상 만들어 줘"

6. **제품 티저**(이미지 프로바이더 하나 필요, 예: `FAL_KEY`):

> "AquaPulse라는 가상의 스마트 물병 출시 티저 영상 만들어 줘"

---

## 6. What Happens During a Run (실행 중에 일어나는 일)

Every request runs through the same pipeline:

```
research -> proposal -> script -> scene_plan -> assets -> edit -> compose
```

- **research** — the agent searches YouTube, Reddit, Hacker News, news sites, and academic sources, then cites everything in a research brief.
- **proposal** — you get concept directions, the recommended pipeline and tool path, and a cost estimate. **Gate: waits for your OK.**
- **script** — the narration script is written with voice direction. **Gate.**
- **scene_plan** — ordered scenes with timings and asset requirements. **Gate.**
- **assets** — images, clips, narration, and music are generated or fetched. Generation pauses on a scene-by-scene contact sheet so you approve the visuals before the render. **Gate.**
- **edit** — cuts, transitions, captions, and music placement (usually auto-proceeds).
- **compose** — a pre-compose validation gate, then the render (Remotion, HyperFrames, or FFmpeg), then a post-render self-review: ffprobe validation, frame sampling, audio-level analysis, and subtitle checks. If the review fails, the video is not presented.

At every gate the agent stops and waits. You answer in chat — "approved", "looks good", "승인", or ask for changes. An early "go ahead" never covers later gates.

**The Backlot board.** When a production starts, the agent opens a local visual board in your browser (`python -m backlot open <project-id>`). It fills itself in as the pipeline runs: stages light up, the script lands as a screenplay page, scene cards show takes and per-asset cost, and every provider decision and dollar spent is on the wall. The board is an observer, never a blocker — if it fails to open, production continues. When a run is done, hit **REPLAY RUN** to replay the whole production from its timestamps.

**[한국어]**

어떤 요청이든 같은 파이프라인을 따라 진행됩니다.

```
research -> proposal -> script -> scene_plan -> assets -> edit -> compose
```

- **research** — 에이전트가 YouTube, Reddit, Hacker News, 뉴스 사이트, 학술 자료를 검색하고, 결과를 출처와 함께 리서치 브리프로 정리합니다.
- **proposal** — 콘셉트 방향, 추천 파이프라인과 도구 경로, 예상 비용을 받습니다. **게이트: 사용자의 승인을 기다립니다.**
- **script** — 낭독 지시가 포함된 내레이션 대본을 작성합니다. **게이트.**
- **scene_plan** — 씬 순서, 길이, 필요한 에셋을 정리합니다. **게이트.**
- **assets** — 이미지, 클립, 내레이션, 음악을 생성하거나 가져옵니다. 렌더링 전에 씬별 콘택트 시트에서 시각 자료를 승인하도록 생성이 멈춥니다. **게이트.**
- **edit** — 컷, 전환, 자막, 음악 배치를 결정합니다(보통 자동 진행).
- **compose** — 사전 검증 게이트를 거쳐 렌더링(Remotion, HyperFrames 또는 FFmpeg)하고, 렌더 후 자체 검토를 합니다. ffprobe 검증, 프레임 샘플링, 음량 분석, 자막 확인이 포함되고, 검토에 실패하면 영상을 보여 주지 않습니다.

각 게이트에서 에이전트는 멈추고 기다립니다. 채팅에 "승인", "좋아요", "진행해"처럼 답하거나 수정을 요청하면 됩니다. 앞 게이트에서 한 승인이 뒤 게이트까지 적용되지는 않습니다.

**Backlot 보드.** 프로덕션이 시작되면 에이전트가 로컬 시각 보드를 브라우저에 자동으로 열어 줍니다(`python -m backlot open <프로젝트-id>`). 파이프라인이 진행되면서 단계가 하나씩 켜지고, 대본이 시나리오 페이지로 표시되고, 씬 카드에 테이크와 에셋별 비용이 뜨고, 어떤 프로바이더를 골랐는지와 지출액이 전부 보드에 남습니다. 보드는 관찰자일 뿐 진행을 막지 않으므로, 열리지 않아도 프로덕션은 계속됩니다. 실행이 끝나면 **REPLAY RUN**을 눌러 전체 과정을 타임스탬프 순서대로 다시 볼 수 있습니다.

---

## 7. Where the Result Lands (결과물 위치)

Every production run creates a project workspace under `projects/`:

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

The finished video is `projects/<project-name>/renders/final.mp4`. The `assets/` subfolders hold everything that went into it, so you can re-edit or reuse pieces later. The `projects/` folder is gitignored — everything in it can be regenerated.

**[한국어]**

프로덕션을 한 번 실행할 때마다 `projects/` 아래에 프로젝트 작업 폴더가 생깁니다.

```
projects/<project-name>/
├── artifacts/          # 각 단계의 JSON 산출물 (research_brief, script, scene_plan 등)
├── assets/
│   ├── images/         # 생성된 이미지 (PNG)
│   ├── video/          # 생성된 영상 클립 (MP4)
│   ├── audio/          # 내레이션 조각 + 최종 믹스 (MP3/WAV)
│   ├── music/          # 배경 음악 (MP3)
│   └── subtitles.srt   # 생성된 자막
└── renders/
    └── final.mp4       # 최종 렌더링 영상 (완성품)
```

완성된 영상은 `projects/<프로젝트-이름>/renders/final.mp4`입니다. `assets/` 하위 폴더에 제작에 쓰인 재료가 전부 남으니, 나중에 다시 편집하거나 재사용할 수 있습니다. `projects/` 폴더는 git 추적 대상이 아니며, 안의 내용은 전부 다시 생성할 수 있습니다.

---

## 8. Cost Expectations (예상 비용)

| Setup | Typical cost per video | Real examples from the README |
|-------|------------------------|-------------------------------|
| **Zero keys** | $0 | Free stock/archival footage, Piper narration, Remotion/HyperFrames rendering — all free |
| **One image provider** (e.g. `FAL_KEY` or `GOOGLE_API_KEY`) | ~$0.15–$1.50 | "Afternoon in Candyland" $0.15, "VOID" $0.69 |
| **Full setup** (AI video clips + premium voice + music) | ~$1–$3 | "THE LAST BANANA" $1.33 |

A near-zero outlier: "The Library at Alexandria" cost just $0.02 — it was built in atelier mode with OpenAI 'ash' TTS narration and a free Pixabay score (five hand-authored scenes, no image provider).

Budget governance is built in, so there are no surprise bills:

- The agent **estimates** the cost before spending anything.
- **Per-action approval**: any single call above a threshold pauses for your confirmation (default: $0.50).
- **Total budget cap**: default $10, fully configurable.
- Modes are configurable: `observe` (track only), `warn` (log overruns), `cap` (hard limit).

**[한국어]**

| 설정 | 영상 한 편 예상 비용 | README에 있는 실제 사례 |
|------|----------------------|--------------------------|
| **키 없음** | $0 | 무료 스톡/아카이브 영상, Piper 내레이션, Remotion/HyperFrames 렌더링 — 전부 무료 |
| **이미지 프로바이더 1개**(예: `FAL_KEY` 또는 `GOOGLE_API_KEY`) | 약 $0.15–$1.50 | "Afternoon in Candyland" $0.15, "VOID" $0.69 |
| **풀 세팅**(AI 영상 클립 + 프리미엄 음성 + 음악) | 약 $1–$3 | "THE LAST BANANA" $1.33 |

거의 무료에 가까운 사례도 있습니다. "The Library at Alexandria"는 단 $0.02로 제작된 영상으로, 이미지 프로바이더 없이 atelier 모드로 직접 만든 다섯 개의 장면에 OpenAI 'ash' TTS 내레이션과 무료 Pixabay 스코어를 얹은 작품입니다.

예산 관리 기능이 내장되어 있어서 예상 못 한 청구서가 나오지 않습니다.

- 에이전트가 돈을 쓰기 전에 **예상 비용을 먼저** 알려 줍니다.
- **건당 승인**: 기준액을 넘는 호출은 사용자 확인을 받을 때까지 멈춥니다(기본값 $0.50).
- **총예산 상한**: 기본값 $10이고 변경할 수 있습니다.
- 모드 설정 가능: `observe`(기록만), `warn`(초과 시 로그), `cap`(하드 리미트).

---

## 9. Troubleshooting (문제 해결)

- **`npm install` fails with `ERR_INVALID_ARG_TYPE` (Windows):** inside the `remotion-composer` folder, run `npx --yes npm install` instead.
- **`make` is not recognized (Windows):** normal — Windows doesn't ship with make. Use the PowerShell one-liner in Section 3; it does everything `make setup` does.
- **FFmpeg not found / missing from PATH:** install with `winget install FFmpeg` (or from [ffmpeg.org](https://ffmpeg.org/download.html)), then close and reopen PowerShell. Verify with `ffmpeg -version`.
- **Python not found:** reinstall Python 3.10+ from [python.org](https://www.python.org/downloads/) and tick **"Add python.exe to PATH"** this time; the `py -3` launcher comes with the official installer.
- **Where the logs and checkpoints live:** everything a run writes is under `projects/<project-name>/` — per-stage `checkpoint_<stage>.json` files, stage outputs in `artifacts/`, and superseded checkpoints archived in `history/`. When something breaks, open that folder, or paste the newest checkpoint file's contents to your AI assistant and ask what went wrong.

**[한국어]**

- **`npm install`이 `ERR_INVALID_ARG_TYPE` 오류로 실패할 때(Windows):** `remotion-composer` 폴더 안에서 `npx --yes npm install`을 대신 실행합니다.
- **`make` 명령을 찾을 수 없을 때(Windows):** 정상입니다. Windows에는 make가 기본 설치되어 있지 않습니다. 3번 섹션의 PowerShell 한 줄 명령이 `make setup`과 같은 일을 합니다.
- **FFmpeg를 찾을 수 없거나 PATH에 없을 때:** `winget install FFmpeg`로 설치하거나 [ffmpeg.org](https://ffmpeg.org/download.html)에서 받은 뒤, PowerShell을 닫았다가 다시 엽니다. `ffmpeg -version`으로 확인합니다.
- **Python을 찾을 수 없을 때:** [python.org](https://www.python.org/downloads/)에서 Python 3.10 이상을 다시 설치하면서 이번에는 **"Add python.exe to PATH"**를 체크하세요. 공식 설치 파일에 `py -3` 런처가 포함되어 있습니다.
- **로그와 체크포인트 위치:** 실행 중 남는 모든 기록은 `projects/<프로젝트-이름>/` 아래에 있습니다. 단계별 `checkpoint_<stage>.json`, 각 단계 산출물 `artifacts/`, 지나간 체크포인트 보관함 `history/`입니다. 뭔가 깨지면 이 폴더를 열어 보거나, 가장 최근 체크포인트 파일 내용을 AI 어시스턴트에 붙여 넣고 원인을 물어보세요.

---

## 10. Useful Commands Cheat-Sheet (유용한 명령어 모음)

Run these from the OpenMontage folder with the virtual environment activated (PowerShell: `.\.venv\Scripts\Activate.ps1`).

| Command | What it does |
|---------|-------------|
| `python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu_summary(), indent=2))"` | Preflight: shows which providers and capabilities are configured on your machine, plus quick setup offers |
| `python -m backlot open` | Opens the Backlot library — every project on disk |
| `python -m backlot open <project-id>` | Opens one production's live board |
| `make test-contracts` | Runs the contract tests (no API keys needed) |
| `make demo` | Renders zero-key demo videos instantly (Remotion-only: animated charts, text, data viz) |

**[한국어]**

OpenMontage 폴더에서 가상환경을 활성화한 상태로 실행합니다(PowerShell: `.\.venv\Scripts\Activate.ps1`).

| 명령어 | 하는 일 |
|--------|---------|
| `python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu_summary(), indent=2))"` | 사전 점검: 이 컴퓨터에 설정된 프로바이더와 기능을 보여 주고, 바로 추가할 수 있는 설정도 알려 줍니다 |
| `python -m backlot open` | Backlot 라이브러리를 엽니다 — 디스크에 있는 모든 프로젝트 |
| `python -m backlot open <project-id>` | 특정 프로덕션의 라이브 보드를 엽니다 |
| `make test-contracts` | 계약 테스트를 실행합니다(API 키 불필요) |
| `make demo` | 키 없이 데모 영상을 바로 렌더링합니다(Remotion 전용: 애니메이션 차트, 텍스트, 데이터 시각화) |
