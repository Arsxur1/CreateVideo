> 이 문서는 이중 언어 문서입니다. 각 섹션에서 영어 원문이 먼저 나오고, **[한국어]** 표시 아래에 한국어 번역이 이어집니다.
> 원본: PROMPT_GALLERY.md @ b4f7ec4eee03409b4dfcd1297ee41b095c9dcf59

# Prompt Gallery (프롬프트 갤러리)

Tested prompts that produce impressive videos. Copy any prompt into your AI coding assistant after running `make setup`.

**[한국어]**
인상적인 비디오를 생성하는 테스트 완료된 프롬프트입니다. `make setup` 실행 후 AI 코딩 어시스턴트에 아무 프롬프트나 복사하여 붙여넣으십시오.

## Zero-Key Demos (제로 키 데모)

These render pre-built compositions using only Remotion components — animated charts, typography, data visualization. No external services, no cost, no waiting.

**[한국어]**
이 데모들은 Remotion 구성 요소만 사용하여 사전 구축된 컴포지션을 렌더링합니다 — 애니메이션 차트, 타이포그래피, 데이터 시각화. 외부 서비스 없음, 비용 없음, 대기 없음.

```bash
make demo                         # Render all three demos
./render-demo.sh world-in-numbers # Render one specific demo
./render-demo.sh --list           # See all available demos
```

| Demo | Duration | What It Shows |
|------|----------|--------------|
| **world-in-numbers** | 45s | KPI grids, bar charts, pie charts, line charts, comparison cards, stat reveals |
| **code-to-screen** | 50s | Developer education: HTTP request lifecycle with progress bars, charts, callouts |
| **focusflow-pitch** | 40s | Startup pitch deck: traction metrics, revenue donut chart, customer testimonial |

**[한국어]**

| 데모 | 길이 | 설명 |
|------|----------|--------------|
| **world-in-numbers** | 45초 | KPI 그리드, 막대 차트, 원형 차트, 선 차트, 비교 카드, 통계 공개 |
| **code-to-screen** | 50초 | 개발자 교육: 진행률 바, 차트, 콜아웃이 있는 HTTP 요청 수명 주기 |
| **focusflow-pitch** | 40초 | 스타트업 피치 덱: 트랙션 지표, 수익 도넛 차트, 고객 후기 |

---

## Zero-Key Prompts (제로 키 프롬프트)

These use the full agent pipeline — research, scripting, asset generation, composition — using only free tools (Piper TTS, stock media, Remotion).

**[한국어]**
이 프롬프트들은 전체 에이전트 파이프라인을 사용합니다 — 연구, 스크립팅, 자산 생성, 컴포지션 — 무료 도구만 사용 (Piper TTS, 스톡 미디어, Remotion).

### Data Explainer (데이터 설명)

> "Make a 45-second animated explainer about why the sky is blue. Use data visualization and animated text — no images needed, just charts, stat cards, and typography."

**What you get:** Research-grounded script, Piper narration, Remotion-animated scenes with text cards, stat reveals, and callout boxes. Subtitles included.

**[한국어]**

**결과:** 연구 기반 스크립트, Piper 내레이션, 텍스트 카드, 통계 공개, 콜아웃 박스가 있는 Remotion 애니메이션 장면. 자막 포함.

**Estimated time:** 5-10 minutes | **Cost:** $0

**[한국어]**

**예상 시간:** 5-10분 | **비용:** $0

### Quick Fact Video (빠른 사실 비디오)

> "Create a 60-second data-driven video about coffee consumption around the world. Include bar charts comparing countries and a pie chart of coffee types."

**What you get:** Animated data visualization with charts, comparison cards, and narrated facts. All data sourced from the research stage.

**[한국어]**

**결과:** 차트, 비교 카드, 내레이션된 사실이 있는 애니메이션 데이터 시각화. 모든 데이터는 연구 단계에서 소싱됩니다.

**Estimated time:** 8-12 minutes | **Cost:** $0

**[한국어]**

**예상 시간:** 8-12분 | **비용:** $0

### History Explainer (역사 설명)

> "Make a short explainer about how the internet works, with narration and animated captions. Keep it under 60 seconds."

**What you get:** Structured explainer with section titles, text cards, stat reveals, and TikTok-style word-by-word captions synced to narration.

**[한국어]**

**결과:** 섹션 제목, 텍스트 카드, 통계 공개, 내레이션과 동기화된 틱톡 스타일 단어별 자막이 있는 구조화된 설명.

**Estimated time:** 8-12 minutes | **Cost:** $0

**[한국어]**

**예상 시간:** 8-12분 | **비용:** $0

### Developer Education (개발자 교육)

> "Create a 90-second animated explainer about how Git rebase works. Use animated diagrams and comparison cards to show rebase vs merge. Target audience: junior developers."

**What you get:** Technical explainer with comparison cards (rebase vs merge), callout tips, step-by-step animated text, and developer-friendly narration.

**[한국어]**

**결과:** 비교 카드 (rebase vs merge), 콜아웃 팁, 단계별 애니메이션 텍스트, 개발자 친화적 내레이션이 있는 기술적 설명.

**Estimated time:** 10-15 minutes | **Cost:** $0

**[한국어]**

**예상 시간:** 10-15분 | **비용:** $0

---

## One-Key Prompts (원 키 프롬프트)

Adding `FAL_KEY` to your `.env` unlocks FLUX image generation. These prompts combine AI-generated visuals with Remotion animation.

**[한국어]**
`.env`에 `FAL_KEY`를 추가하면 FLUX 이미지 생성이 해제됩니다. 이 프롬프트들은 AI 생성 시각 효과와 Remotion 애니메이션을 결합합니다.

### Science Explainer (과학 설명)

> "Create an animated explainer about how CRISPR gene editing works, with AI-generated visuals of DNA and cell diagrams. Make it 90 seconds, educational but exciting."

**What you get:** Research-backed script, FLUX-generated images with Ken Burns animation, spring-animated transitions, narration, subtitles, and music.

**[한국어]**

**결과:** 연구 기반 스크립트, Ken Burns 애니메이션이 적용된 FLUX 생성 이미지, 스프링 애니메이션 전환, 내레이션, 자막, 음악.

**Estimated time:** 15-20 minutes | **Cost:** ~$0.80

**[한국어]**

**예상 시간:** 15-20분 | **비용:** ~$0.80

### Product Teaser (제품 티저)

> "Make a product launch teaser for a fictional smart water bottle called AquaPulse. 45 seconds, modern and minimal, with AI-generated product shots."

**What you get:** Cinematic product teaser with FLUX-generated visuals, stat reveals (hydration data), comparison cards, and a punchy closing.

**[한국어]**

**결과:** FLUX 생성 시각 효과, 통계 공개 (수분 데이터), 비교 카드, 강력한 마무리가 있는 시네마틱 제품 티저.

**Estimated time:** 12-18 minutes | **Cost:** ~$0.60

**[한국어]**

**예상 시간:** 12-18분 | **비용:** ~$0.60

### Marketing Explainer (마케팅 설명)

> "Build a 90-second explainer about the psychology of color in marketing. Use AI-generated images showing color associations and include data about color impact on purchasing decisions."

**What you get:** Research-grounded explainer with AI-generated color psychology illustrations, bar charts, pie charts, and narrated insights.

**[한국어]**

**결과:** AI 생성 색채 심리학 일러스트레이션, 막대 차트, 원형 차트, 내레이션된 통찰이 있는 연구 기반 설명.

**Estimated time:** 15-20 minutes | **Cost:** ~$1.00

**[한국어]**

**예상 시간:** 15-20분 | **비용:** ~$1.00

---

## Animation Pipeline — Anime/Ghibli Style (애니메이션 파이프라인 — 애니메/지브리 스타일)

These use the **Animation pipeline** with `image_animation` approach — FLUX-generated still images brought to life through multi-image crossfade, cinematic camera motion, particle overlays, and ambient music. No video generation APIs needed. Each 30-second video costs ~$0.15.

**[한국어]**
이 프롬프트들은 `image_animation` 접근 방식을 사용하는 **애니메이션 파이프라인**을 사용합니다 — FLUX 생성 정지 이미지가 다중 이미지 크로스페이드, 시네마틱 카메라 모션, 파티클 오버레이, 앰비언트 음악을 통해 생동감 있게 표현됩니다. 비디오 생성 API는 필요하지 않습니다. 30초 비디오당 비용은 약 $0.15입니다.

### Ghibli Fantasy World (지브리 판타지 월드)

> "Create a 30-second Ghibli-style animated video of a magical floating library in the clouds at golden hour. Books drift between shelves, warm light streams through stained glass windows, and a small cat naps on a reading desk."

**What you get:** 6 anime scenes with 12 FLUX-generated images, camera motion (zoom, pan, Ken Burns, drift), sparkle and light-ray particles, cinematic vignette, hero title overlay, and auto-sourced ambient music with energy-optimized offset.

**[한국어]**

**결과:** 12개의 FLUX 생성 이미지가 있는 6개 애니메이션 장면, 카메라 모션 (줌, 팬, Ken Burns, 드리프트), 반짝임과 광선 파티클, 시네마틱 비네트, 주요 제목 오버레이, 에너지 최적화 오프셋이 적용된 자동 소싱 앰비언트 음악.

**Estimated time:** 10-15 minutes | **Cost:** ~$0.15

**[한국어]**

**예상 시간:** 10-15분 | **비용:** ~$0.15

### Underwater Exploration (수중 탐험)

> "Make a 30-second anime-style animation of an underwater temple with bioluminescent coral, ancient ruins covered in sea moss, luminous jellyfish drifting past stone pillars, and shafts of sunlight piercing the deep blue."

**What you get:** Deep ocean atmosphere with mist and sparkle particles, pan and drift camera motion, blue-green lighting overlays, section title overlays, and oceanic ambient soundtrack.

**[한국어]**

**결과:** 안개와 반짝임 파티클이 있는 심해 분위기, 팬 및 드리프트 카메라 모션, 청록색 조명 오버레이, 섹션 제목 오버레이, 해양 앰비언트 사운드트랙.

**Estimated time:** 10-15 minutes | **Cost:** ~$0.15

**[한국어]**

**예상 시간:** 10-15분 | **비용:** ~$0.15

### Seasonal Journey (계절의 여정)

> "Create a 30-second Ghibli-style animated video showing the four seasons in a Japanese countryside village — cherry blossoms in spring, fireflies in summer, red maple leaves in autumn, and snow-covered thatched roofs in winter."

**What you get:** 6 scenes transitioning through seasons with petal, firefly, sparkle, and mist particles matching each season. Warm-to-cool lighting transitions and ambient seasonal soundtrack.

**[한국어]**

**결과:** 각 계절에 맞는 꽃잎, 반딧불이, 반짝임, 안개 파티클이 있는 6개 계절 전이 장면. 따뜻한에서 차가운 조명 전환과 계절별 앰비언트 사운드트랙.

**Estimated time:** 10-15 minutes | **Cost:** ~$0.15

**[한국어]**

**예상 시간:** 10-15분 | **비용:** ~$0.15

### Steampunk Cityscape (스팀펑크 도시 경관)

> "Make a 30-second anime-style animation of a steampunk city at dusk — airships floating between brass towers, steam rising from street vents, clockwork birds perching on copper lampposts, and a lone inventor walking home through cobblestone streets."

**What you get:** Industrial-fantasy atmosphere with mist and sparkle particles, parallax and zoom camera motion, warm amber lighting overlays, and steampunk-ambient soundtrack.

**[한국어]**

**결과:** 안개와 반짝임 파티클이 있는 산업-판타지 분위기, 패럴랙스 및 줌 카메라 모션, 따뜻한 호박색 조명 오버레이, 스팀펑크 앰비언트 사운드트랙.

**Estimated time:** 10-15 minutes | **Cost:** ~$0.15

**[한국어]**

**예상 시간:** 10-15분 | **비용:** ~$0.15

---

## HyperFrames — HTML/GSAP Motion Graphics (HyperFrames — HTML/GSAP 모션 그래픽)

These use the HyperFrames composition runtime — HTML + CSS + GSAP rendered deterministically to video via headless Chrome + FFmpeg. Perfect for kinetic typography, product promos, launch reels, and website-to-video treatments where the visual grammar is typographic and motion-first.

**[한국어]**
이 프롬프트들은 HyperFrames 컴포지션 런타임을 사용합니다 — 헤드리스 Chrome + FFmpeg를 통해 비디오로 결정론적으로 렌더링되는 HTML + CSS + GSAP. 키네틱 타이포그래피, 제품 프로모션, 출시 릴, 웹사이트-비디오 변환 처리에 완벩니다. 여기서 시각적 문법은 타이포그래피와 모션 우선입니다.

**Requirements:** Node.js ≥ 22, FFmpeg, `npx` — no monorepo checkout, the CLI is fetched via `npx @hyperframes/cli` on first run.

**[한국어]**

**요구사항:** Node.js ≥ 22, FFmpeg, `npx` — 모노레포 체크아웃 불필요, CLI는 첫 실행 시 `npx @hyperframes/cli`를 통해 가져옵니다.

### Kinetic Product Launch (키네틱 제품 출시)

> "Make a 20-second product launch video for a new AI coding assistant called 'Cortex'. Big kinetic typography, three feature callouts, a bold accent color, and a final CTA card. Use the HyperFrames runtime."

**What you get:** HTML/GSAP composition with SplitText-style word reveals, staggered feature callouts, accent-driven color accents from a custom playbook, and `hyperframes lint`/`validate` gates passed before render.

**[한국어]**

**결과:** SplitText 스타일 단어 공개, 계단식 기능 강조, 사용자 정의 플레이북의 악센트 기반 색상 악센트가 있는 HTML/GSAP 컴포지션, 렌더링 전 `hyperframes lint`/`validate` 게이트 통과.

**Estimated time:** 3-5 minutes | **Cost:** $0

**[한국어]**

**예상 시간:** 3-5분 | **비용:** $0

### Website → Video Teaser (웹사이트 → 비디오 티저)

> "Here's my landing page URL: https://example.com. Make me a 15-second social ad for Instagram. Use HyperFrames and pick up the site's real colors and typography."

**What you get:** `website-to-hyperframes` workflow — capture the site, extract colors/typography into a `DESIGN.md`, storyboard 3-4 beats, generate narration, build compositions with GSAP timelines, lint + validate + render.

**[한국어]**

**결과:** `website-to-hyperframes` 워크플로우 — 사이트 캡처, 색상/타이포그래피를 `DESIGN.md`로 추출, 3-4 비트 스토리보드, 내레이션 생성, GSAP 타임라인으로 컴포지션 빌드, lint + validate + render.

**Estimated time:** 8-12 minutes | **Cost:** $0 (or ~$0.05 with premium TTS)

**[한국어]**

**예상 시간:** 8-12분 | **비용:** $0 (또는 프리미엄 TTS로 ~$0.05)

### Launch Reel with Registry Blocks (레지스트리 블록이 포함된 출시 릴)

> "Create a 25-second launch reel for a developer tools startup. Include a data chart block (showing user growth from HyperFrames registry), kinetic title cards, and a shader transition between scenes."

**What you get:** `hyperframes add data-chart` + `hyperframes add shader-transition` installed as sub-compositions, wired into index.html, animated with GSAP timelines. Registry blocks are HyperFrames-only; Remotion can't install them.

**[한국어]**

**결과:** `hyperframes add data-chart` + `hyperframes add shader-transition`가 하위 컴포지션으로 설치되어 index.html에 연결되고 GSAP 타임라인으로 애니메이션됩니다. 레지스트리 블록은 HyperFrames 전용이며 Remotion은 설치할 수 없습니다.

**Estimated time:** 5-10 minutes | **Cost:** $0

**[한국어]**

**예상 시간:** 5-10분 | **비용:** $0

---

## Full Setup Prompts (전체 설정 프롬프트)

With video generation (Veo, Kling, Runway) + premium TTS (ElevenLabs) + music (Suno). These produce broadcast-quality content.

**[한국어]**
비디오 생성 (Veo, Kling, Runway) + 프리미엄 TTS (ElevenLabs) + 음악 (Suno)이 포함됩니다. 이들은 방송 품질 콘텐츠를 생성합니다.

### Cinematic Trailer (시네마틱 트레일러)

> "Create a cinematic 30-second trailer for a sci-fi concept: humanity receives a warning from 1000 years in the future. Use motion video clips, a cinematic soundtrack, and dramatic title cards."

**What you get:** Veo/Kling-generated motion clips, cinematic title cards with signal texture effects, Hans Zimmer-style soundtrack, and dramatic pacing.

**[한국어]**

**결과:** Veo/Kling 생성 모션 클립, 신호 텍스처 효과가 있는 시네마틱 제목 카드, Hans Zimmer 스타일 사운드트랙, 드라마틱 페이싱.

**Estimated time:** 25-40 minutes | **Cost:** ~$2.50

**[한국어]**

**예상 시간:** 25-40분 | **비용:** ~$2.50

### Animated Explainer (Premium) (애니메이션 설명 (프리미엄))

> "Make a 90-second animated explainer about quantum computing for middle school students. Use a fun narrator voice, custom soundtrack, and AI-generated visuals of qubits and quantum gates."

**What you get:** Full production: ElevenLabs narration, FLUX visuals, Suno soundtrack, Remotion composition with animated charts and text overlays.

**[한국어]**

**결과:** 풀 프로덕션: ElevenLabs 내레이션, FLUX 시각 효과, Suno 사운드트랙, 애니메이션 차트 및 텍스트 오버레이가 있는 Remotion 컴포지션.

**Estimated time:** 20-30 minutes | **Cost:** ~$2.00

**[한국어]**

**예상 시간:** 20-30분 | **비용:** ~$2.00

### Avatar Spokesperson (아바타 스포크스퍼슨)

> "Create a 60-second avatar spokesperson video announcing a company rebrand. Professional tone, clean background, with animated text overlays showing the new brand values."

**What you get:** HeyGen avatar video with TTS narration, overlaid section titles, stat reveals, and branded text cards.

**[한국어]**

**결과:** TTS 내레이션, 섹션 제목 오버레이, 통계 공개, 브랜드 텍스트 카드가 있는 HeyGen 아바타 비디오.

**Estimated time:** 15-25 minutes | **Cost:** ~$1.50

**[한국어]**

**예상 시간:** 15-25분 | **비용:** ~$1.50

---

## For Specific Audiences (특정 대상을 위한)

### For Teachers (교사를 위한)

> "Create a 3-minute animated explainer about photosynthesis for 8th graders. Make it fun and visual — use diagrams, charts showing energy conversion, and a friendly narrator voice."

### For Developer Advocates (개발자 어드보켓을 위한)

> "Make a 60-second product demo video for our new REST API. Show the request/response flow with animated diagrams, include latency benchmarks as bar charts, and end with a quick start code snippet."

### For Indie Hackers (인디 해커를 위한)

> "Create a 30-second Product Hunt launch video for my SaaS tool that helps teams track OKRs. Show 3 key features with animated stat cards and comparison views. Upbeat, modern."

### For Content Creators (콘텐츠 크리에이터를 위한)

> "Take my recent blog post about AI trends in 2026 and turn it into a 90-second video. Research current data to ground it, use animated charts for the statistics, and add a conversational narrator."

---

## Tips for Better Results (더 나은 결과를 위한 팁)

**Be specific about visual components.** Instead of "make it look good," say "use bar charts for the comparison, a donut chart for the breakdown, and stat cards for the key numbers."

**[한국어]**
시각적 구성 요소를 구체적으로 지정하십시오. "좋아 보이게 만들어" 대신 "비교에는 막대 차트, 분해에는 도넛 차트, 핵심 숫자에는 통계 카드를 사용하십시오."

**Mention your target audience.** "For junior developers" or "for 8th graders" dramatically changes the script, pacing, and visual style.

**[한국어]**
대상을 명시하십시오. "주니어 개발자용" 또는 "8학년용"은 스크립트, 페이싱, 시각 스타일을 크게 변경합니다.

**Specify duration.** The agent optimizes content density based on your target length. 45 seconds needs ~110 words of narration; 90 seconds needs ~225 words.

**[한국어]**
지속 시간을 지정하십시오. 에이전트는 목표 길이에 따라 콘텐츠 밀도를 최적화합니다. 45초는 내레이션 약 110단어, 90초는 약 225단어가 필요합니다.

**Request specific chart types.** The system has bar charts, line charts, pie/donut charts, KPI grids, progress bars, comparison cards, and callout boxes. Name the ones you want.

**[한국어]**
특정 차트 유형을 요청하십시오. 시스템에는 막대 차트, 선 차트, 파이/도넛 차트, KPI 그리드, 진행률 바, 비교 카드, 콜아웃 박스가 있습니다. 원하는 것을 지정하십시오.

**Ask for the zero-key path.** If you want free results, say "use only free tools" or "no paid APIs." The agent will route to Piper TTS, stock media, and Remotion-only compositions.

**[한국어]**
제로 키 경로를 요청하십시오. 무료 결과를 원하면 "무료 도구만 사용" 또는 "유료 API 없음"이라고 하십시오. 에이전트는 Piper TTS, 스톡 미디어, Remotion 전용 컴포지션으로 라우팅합니다.

**For anime/Ghibli-style videos,** mention the style explicitly: "Ghibli-style" or "anime-style." Describe the atmosphere, lighting, and mood. The agent uses the Animation pipeline with FLUX image generation and Remotion's anime scene engine — multi-image crossfade, camera motion, and particle overlays create the illusion of animation from still images. Cost is minimal (~$0.15 for 30 seconds).

**[한국어]**
애니메/지브리 스타일 비디오의 경우 스타일을 명시적으로 언급하십시오: "지브리 스타일" 또는 "애니메이션 스타일". 분위기, 조명, 무드를 설명하십시오. 에이전트는 FLUX 이미지 생성 및 Remotion의 애니메이션 장면 엔진이 있는 애니메이션 파이프라인을 사용합니다 — 다중 이미지 크로스페이드, 카메라 모션, 파티클 오버레이가 정지 이미지에서 애니메이션의 환상을 만듭니다. 비용은 최소화됩니다 (30초당 약 $0.15).

---

## Contributing Prompts (프롬프트 기여)

Found a prompt that produces great results? Share it:

**[한국어]**
훌륭한 결과를 만드는 프롬프트를 발견했나요? 공유하십시오:

1. Open a [GitHub Discussion](../../discussions) in the "Prompt Exchange" category

**[한국어]**
1. "Prompt Exchange" 카테고리에서 [GitHub 토론](../../discussions) 열기

2. Include: your prompt, a screenshot or description of the output, cost, and which providers you used

**[한국어]**
2. 포함: 프롬프트, 출력의 스크린샷 또는 설명, 비용, 사용한 프로바이더

3. The best prompts get added to this gallery with credit

**[한국어]**
3. 최고의 프롬프트는 크레딧과 함께 이 갤러리에 추가됩니다

---

*This gallery is community-maintained. All prompts have been tested and produce complete videos.*

**[한국어]**
*이 갤러리는 커뮤니티 관리입니다. 모든 프롬프트는 테스트되었으며 완전한 비디오를 생성합니다.*