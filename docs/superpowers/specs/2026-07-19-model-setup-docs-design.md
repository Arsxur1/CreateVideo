# Design: Multi-Model Brain Documentation (Kimi / GLM / Any Anthropic-Compatible Model)

## Problem

OpenMontage already supports swapping the agent "brain" (the LLM driving the harness) away from Claude, because the harness reads plain instruction files (`CLAUDE.md` → `AGENT_GUIDE.md`) regardless of backend model. `docs/ko/KIMI-SETUP.md` proves this works for Kimi, but:

- It's Korean-only, in `docs/ko/`, with no English original — English-speaking users can't discover that model-swapping is even possible.
- GLM (Z.AI), which uses the exact same Anthropic-compatible-endpoint pattern, has no documentation at all.
- There's no single place explaining the *general* pattern, so each new model requires reverse-engineering the Kimi doc instead of following a documented recipe.
- There's no lightweight, personal, step-by-step guide for actually doing the switch on a real machine — KIMI-SETUP is thorough but written as reference documentation, not a "do this now" checklist.

## Goals

1. Make "OpenMontage's brain is swappable" discoverable in English.
2. Document GLM setup to the same standard as Kimi.
3. Establish a reusable pattern section so a third model (Qwen, etc.) can be added later without re-deriving the recipe.
4. Give the user (this repo's maintainer, Windows 11 + Claude Code) a fast personal reference for actually switching brains on their machine.
5. Keep `docs/ko/KIMI-SETUP.md` intact — it works, don't rewrite it.

## Non-Goals

- Promoting `USAGE.md` to an English original (separate, unrelated task).
- Benchmarking Kimi/GLM output quality or gate-compliance — the new doc explains *how* to measure this (via `framework-smoke`) but does not run the measurement.
- Building an automated model-switch script shipped in the repo (rejected in favor of a personal PowerShell-profile snippet — see Alternatives Considered).
- Touching the pending Windows cp949 encoding fixes already sitting in the working tree — unrelated change, will be committed separately, never mixed into the doc commits.

## Approach

### 1. `docs/MODEL-SETUP.md` (English original, new file)

A single reference document built around one universal pattern, with per-model sections that instantiate it. Structure:

1. **How the Brain Works** — restates the separation already established in KIMI-SETUP: the "brain" (harness backend, an env-var swap) is completely independent from media-generation provider keys (`FAL_KEY` etc., configured in `.env`). This is the #1 confusion point and must be stated before anything else.
2. **The Universal Pattern** — every Anthropic-Messages-API-compatible provider needs exactly three things:
   - `ANTHROPIC_BASE_URL` — the provider's compatible endpoint
   - `ANTHROPIC_AUTH_TOKEN` — the provider's API key (not `ANTHROPIC_API_KEY` — a documented common mistake)
   - Tier mapping (`ANTHROPIC_DEFAULT_SONNET_MODEL` / `_HAIKU_MODEL` / `_OPUS_MODEL`) — Claude Code requests tiers by name; without mapping, it requests models that don't exist on the target provider and errors.
3. **Claude (default)** — baseline: no configuration needed, included so the pattern section has a concrete anchor.
4. **Kimi (Moonshot)** — endpoint (`https://api.moonshot.ai/anthropic`, `.cn` alternative), key acquisition, model names, tier mapping. Links to `docs/ko/KIMI-SETUP.md` for the full walkthrough (install steps, Path B alternative CLI, verification) rather than duplicating it.
5. **GLM (Z.AI)** — endpoint (`https://api.z.ai/api/anthropic`), key acquisition via Z.AI console, tier mapping (`glm-4.7` for sonnet/opus tier, `glm-4.5-air` for haiku tier), `API_TIMEOUT_MS` note, three documented common mistakes (wrong URL path, wrong env var name, forgetting to restart terminal after editing `settings.json`).
6. **Any Other Compatible Model** — an empty template (base URL / key / tier mapping / verification command) so a future model is a fill-in-the-blanks addition, not a new doc.
7. **Switching and Verifying** — how to confirm which brain is currently active, how to switch back to Claude cleanly (unset vs. override).
8. **Caveats** — gate-compliance is not guaranteed to be uniform across models; the `gate_skipped` audit flag in Backlot (`backlot/state.py`) is the safety net that surfaces silent gate-skipping regardless of which model is driving; recommend running the `framework-smoke` pipeline after switching to a new model to sanity-check pipeline/gate behavior before trusting it with real production work.
9. **Sources** — links used to verify current endpoint/pricing info.

### 2. `docs/ko/MODEL-SETUP.md` (Korean translation)

Follows the existing bilingual-or-translation convention already used across `docs/ko/`:
- Header: `> 원본: docs/MODEL-SETUP.md @ <40-char-hash>` — same format `check-ko-drift.py` already parses.
- Added as a new pair in `scripts/check-ko-invariants.py`'s `PAIRS` list so code blocks/URLs/paths are verified verbatim against the English original.
- **Commit ordering constraint:** the drift header must record the *actual* commit hash of the English original, which doesn't exist until that commit lands. So this is necessarily two commits: (a) commit `docs/MODEL-SETUP.md`, (b) look up its hash with `git log -1 --format=%H -- docs/MODEL-SETUP.md`, write the Korean file with that hash in the header, commit it. Both checks (`check-ko-drift.py`, `check-ko-invariants.py`) are run after step (b) to confirm.

### 3. Linking work

- `README.md` (English): add a line near wherever Claude Code / harness setup is currently mentioned, pointing to `docs/MODEL-SETUP.md`.
- `README_ko.md`: update its existing Kimi-guide line to also mention `docs/ko/MODEL-SETUP.md` (currently it links `docs/ko/USAGE.md` and `docs/ko/KIMI-SETUP.md` directly).
- `docs/ko/KIMI-SETUP.md`: add one line near the top — "다른 모델(GLM 등)은 docs/ko/MODEL-SETUP.md 참고" — no other change to this file.

### 4. `LOCAL-SETUP-GUIDE.md` (repo root, gitignored, Korean, personal)

Not part of the committed documentation set — a working reference for this specific user's machine (Windows 11, Claude Code already installed). Content:

1. Kimi key acquisition — screen-by-screen, assuming zero prior context.
2. GLM key acquisition — same.
3. **PowerShell profile functions** — `use-kimi`, `use-glm`, `use-claude` — one-word brain switching by setting/clearing the relevant env vars for the current shell session. This is the practical payload of the guide.
4. Verification — what command to run and what output confirms the switch worked.
5. Troubleshooting table — common mistake → symptom → fix (wrong base URL path, key in wrong env var, tier mapping missing, terminal not restarted).

`.gitignore` gets a `LOCAL-*.md` entry so this file (and any future personal-notes files following the same naming convention) never risks being committed.

## File Changes Summary

| File | Change |
|---|---|
| `docs/MODEL-SETUP.md` | New — English original |
| `docs/ko/MODEL-SETUP.md` | New — Korean translation with drift header |
| `scripts/check-ko-invariants.py` | Add `("docs/MODEL-SETUP.md", "docs/ko/MODEL-SETUP.md")` to `PAIRS` |
| `README.md` | Add one link to `docs/MODEL-SETUP.md` |
| `README_ko.md` | Update existing guide-links line to add `docs/ko/MODEL-SETUP.md` |
| `docs/ko/KIMI-SETUP.md` | Add one cross-reference line near the top; no other edits |
| `LOCAL-SETUP-GUIDE.md` | New — gitignored, personal, not committed |
| `.gitignore` | Add `LOCAL-*.md` |

## Testing / Verification

- `python scripts/check-ko-drift.py` — must show `OK` for the new Korean file (or `SKIP` if it ever becomes a Korean-original, which it won't here).
- `python scripts/check-ko-invariants.py` — must show `OK` for the new pair (code blocks and URL/path tokens preserved verbatim).
- `python -m pytest tests/test_check_ko_drift.py tests/test_check_ko_invariants.py -q` — existing test suite must still pass against the updated `PAIRS` list.
- Manual read-through: confirm the GLM section's endpoint/env-var names match what was verified via web search during research (`https://api.z.ai/api/anthropic`, `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_DEFAULT_SONNET_MODEL=glm-4.7`).

## Alternatives Considered

- **Merge Kimi content into MODEL-SETUP.md directly** — rejected. KIMI-SETUP.md is a working, tested, linked document; folding it in means rewriting proven content and breaking its existing inbound links for no benefit over a cross-reference.
- **Ship a `scripts/use-model.py` switcher in the repo** — rejected. Adds a maintenance surface (harness-specific branching, cross-platform shell handling) for something that's a two-line env-var set. A personal PowerShell function in the user's own profile is simpler and doesn't need to survive code review or work on every contributor's machine.
- **Keep everything Korean-only in `docs/ko/`** — rejected per explicit goal: the whole point is English discoverability, since the current setup silently excludes English-speaking users from knowing the feature exists.
