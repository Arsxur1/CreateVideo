# Running OpenMontage with a Different Model Brain

OpenMontage's "AI agent" is whichever coding assistant reads this repo's
instruction files (`CLAUDE.md` / `AGENT_GUIDE.md`) and drives the Python
tools in `tools/`. That assistant's backend LLM — Claude by default — can
be swapped for any other model that exposes an Anthropic-Messages-API-
compatible endpoint, without touching any code or instruction file in
this repo.

This document explains the general pattern once, then gives the exact
settings for each model OpenMontage has been run with. For a full,
step-by-step walkthrough (installing Claude Code from scratch, verifying
the connection, troubleshooting), see
[`docs/ko/KIMI-SETUP.md`](ko/KIMI-SETUP.md) — it's written for Kimi but
the installation and verification steps apply to every model on this
page.

## How the Brain Works

The "brain" and the media-generation providers are two completely
separate things, and mixing them up is the most common point of
confusion:

- **The brain** is the LLM that reads `AGENT_GUIDE.md`, picks a pipeline,
  runs preflight, and drives the Python tools stage by stage. Changing
  the brain is an environment-variable change to your coding assistant —
  nothing in this repo needs to change.
- **Media generation** (video, image, TTS, music) is handled by separate
  provider APIs configured with their own keys in the project's `.env`
  (for example `FAL_KEY`, `ELEVENLABS_API_KEY`). Those keys are
  completely independent of which brain you use.

So "switching to Kimi" or "switching to GLM" only changes who is
directing the production — it does not unlock or change any media
provider, and it does not require a different `.env`.

## The Universal Pattern

Every model that exposes an Anthropic-Messages-API-compatible endpoint
needs the same three settings:

1. **`ANTHROPIC_BASE_URL`** — the provider's compatible endpoint.
2. **`ANTHROPIC_AUTH_TOKEN`** — the provider's API key. Note the variable
   name: it is `ANTHROPIC_AUTH_TOKEN`, not `ANTHROPIC_API_KEY`. Using the
   wrong variable name is the single most common setup mistake.
3. **Tier mapping** — Claude Code requests models by tier
   (`ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL`,
   `ANTHROPIC_DEFAULT_OPUS_MODEL`). Without mapping these to real model
   names on the target provider, Claude Code will ask for a model that
   doesn't exist there and every request will fail.

Set these as environment variables, or persist them in
`~/.claude/settings.json` under an `"env"` object. Either way, restart
your terminal (or Claude Code) after changing them — settings read at
startup will not pick up a mid-session edit.

## Claude (Default)

No configuration needed. If none of the variables above are set, Claude
Code talks to Anthropic directly and uses Claude models. This is the
baseline every other section below is a variation of.

## Kimi (Moonshot)

```bash
ANTHROPIC_BASE_URL="https://api.moonshot.ai/anthropic"
ANTHROPIC_AUTH_TOKEN="<your Moonshot API key>"
ANTHROPIC_MODEL="kimi-k2.5"
ANTHROPIC_SMALL_FAST_MODEL="kimi-k2.5"
```

If you're in mainland China, use
`https://api.moonshot.cn/anthropic` instead of the `.ai` endpoint.

Get a key from the Kimi Open Platform console at
`https://platform.kimi.ai`. Full walkthrough, including installing
Claude Code from scratch and a CLI-only alternative path:
[`docs/ko/KIMI-SETUP.md`](ko/KIMI-SETUP.md).

## GLM (Z.AI)

```bash
ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
ANTHROPIC_AUTH_TOKEN="<your Z.AI API key>"
ANTHROPIC_DEFAULT_SONNET_MODEL="glm-4.7"
ANTHROPIC_DEFAULT_OPUS_MODEL="glm-4.7"
ANTHROPIC_DEFAULT_HAIKU_MODEL="glm-4.5-air"
API_TIMEOUT_MS="3000000"
```

Get a key from the Z.AI console, under the GLM Coding Plan. Three
mistakes to avoid, in order of how often they happen:

1. Using the general `api/paas/v4` API path instead of the
   Anthropic-compatible `api/anthropic` path shown above.
2. Putting the key in `ANTHROPIC_API_KEY` instead of
   `ANTHROPIC_AUTH_TOKEN`.
3. Editing `~/.claude/settings.json` and not restarting the terminal —
   the running process keeps using whatever it read at startup.

## Any Other Compatible Model

If a provider advertises an "Anthropic-compatible" or
"Claude-compatible" endpoint, it fits the same three-variable pattern:

```bash
ANTHROPIC_BASE_URL="<the provider's compatible endpoint>"
ANTHROPIC_AUTH_TOKEN="<the provider's API key>"
ANTHROPIC_DEFAULT_SONNET_MODEL="<a real model name on that provider>"
ANTHROPIC_DEFAULT_HAIKU_MODEL="<a real, faster/cheaper model name on that provider>"
```

Verify the connection with the same command as every other model — see
"Switching and Verifying" below — before starting real production work
with it.

## Switching and Verifying

To confirm which brain is currently active, ask the assistant directly
inside a session — for example "what model are you and what endpoint are
you using" — or check which environment variables are currently set:

```bash
echo $ANTHROPIC_BASE_URL
echo $ANTHROPIC_AUTH_TOKEN
```

An empty `ANTHROPIC_BASE_URL` means you're on the Claude default. To
switch back to Claude, unset the three variables (or remove them from
`~/.claude/settings.json`) and restart the terminal.

## Caveats

- **Gate compliance is not guaranteed to be uniform across models.**
  `AGENT_GUIDE.md`'s checkpoint and human-approval gates
  (`## Human Checkpoint Protocol`) rely on the brain actually following
  the instructions in that file. A weaker or less-instruction-following
  model may skip a gate it should have stopped at.
- **This is not unmonitored, though.** Backlot's board derivation
  (`backlot/state.py`) computes a `gate_skipped` flag per stage — a gated
  stage that reached `completed` without ever passing through
  `awaiting_human` or recording `human_approved` gets flagged on the
  board regardless of which model drove the run. Check the board after a
  run with a new model, not just the terminal output.
- **Before trusting a new model with real production work**, run it
  through the `framework-smoke` pipeline first (`pipeline_defs/framework-smoke.yaml`)
  — a minimal 2-stage pipeline built for exactly this: a fast check that
  pipeline selection, preflight, and stage gating behave correctly before
  you spend a real run's worth of tokens and provider cost finding out
  they don't.

## Sources

- [Z.AI — Claude Code developer docs](https://docs.z.ai/scenario-example/develop-tools/claude)
- [Claude Code + GLM Coding Plan — 2026 Integration Guide](https://codingplan.run/guides/claude-code-with-glm)
- [ClaudeLog — How to Use Z.AI in Claude Code](https://claudelog.com/faqs/how-to-use-z-ai-in-claude-code/)
- [Using Kimi K2.5 inside Claude Code](https://kimi-k25.com/blog/kimi-k2-5-claude-code)
- [Moonshot AI forum — official guide for K2 in Claude Code](https://forum.moonshot.ai/t/do-we-have-offical-guide-for-using-k2-in-claude-code/84)
