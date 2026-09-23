# HyperFrames Skills: Provenance

The HyperFrames-family skills under `.agents/skills/` are vendored from the HyperFrames monorepo.

- **Source**: https://github.com/Aarul5/hyperframes (fork of https://github.com/heygen-com/hyperframes, identical to upstream `main` at vendor time)
- **Vendored commit**: `b1cf88a` (`ci: generate catalog artifacts through a standing publish PR (#4337)`, 2026-09-23)
- **CLI at vendor time**: `hyperframes` 0.8.65 (`npx hyperframes doctor` passes on Windows with Node 22)
- **Previous vendor**: `3351fb1a` (v0.7.17, 2026-06-27)

## What's vendored

All 21 skills from the upstream `skills/` directory:

`hyperframes`, `hyperframes-core`, `hyperframes-creative`, `hyperframes-animation`, `hyperframes-audio`,
`hyperframes-keyframes`, `hyperframes-cli`, `hyperframes-registry`, `hyperframes-studio`, `media-use`,
`motion-graphics`, `music-to-video`, `remotion-to-hyperframes`, `embedded-captions`, `product-launch-video`,
`talking-head-recut`, `general-video`, `slideshow`, `faceless-explainer`, `pr-to-video`, `figma`.

Changes since v0.7.17:

- `hyperframes-media` was removed upstream. TTS, BGM, SFX, captions, images and grades moved to
  `media-use`; mixing placed tracks moved to the new `hyperframes-audio`.
- New atomic skills: `hyperframes-audio`, `hyperframes-keyframes`, `hyperframes-studio`.
- The 0.8 router (`hyperframes/SKILL.md`) routes fresh creation to the workflow skills
  (`product-launch-video`, `general-video`, ...). v0.7.17 left those out; they are vendored now so the
  router's references resolve.

## Kept from the previous vendor

- `website-to-video` (v0.7.17). Upstream folded it into `product-launch-video` in 0.8. Kept because
  `hyperframes_compose` advertises it in `agent_skills` (see `tests/contracts/test_agent_skill_pointers.py`).

## How OpenMontage uses them

These are Layer 3 reference knowledge. Inside OpenMontage the pipeline decides the workflow
(`AGENT_GUIDE.md`, Rule Zero and "Present Both Composition Runtimes"). The router's line that
HyperFrames is "the default for any video request" does not override that here: an agent reads the
workflow skills for technique inside a pipeline stage, it does not hand the run over to them.

## Local additions (re-apply after every re-vendor)

- `media-use/audio/references/tts.md`: the "Expressive narration contract" section (voice-performance
  plan before TTS). Originally added to `hyperframes-media/references/tts.md` in `5e4943a`.

## Re-sync instructions

```bash
# Windows needs long paths: some music-to-video paths are over 120 chars.
git clone --depth 1 --filter=blob:none --sparse -c core.longpaths=true https://github.com/Aarul5/hyperframes.git hf
cd hf && git sparse-checkout set --no-cone skills/ && cd ..
for d in hf/skills/*/; do n=$(basename "$d"); rm -rf ".agents/skills/$n"; cp -r "$d" ".agents/skills/$n"; done
# Re-apply the local additions above, restore this file, then update the commit/date at the top.
```
