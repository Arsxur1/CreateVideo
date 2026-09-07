---
context_schema: 1
project: OpenMontage
created_at: 2026-09-04T22:56:53Z
canonical: true
---

# Project Context

This file is the canonical append-only project context ledger. Existing complete header and entry bytes must never be edited or deleted.

<!-- context-entry:start -->
## CTX-000001 | bootstrap

- Timestamp: 2026-09-04T22:56:53Z
- Lifecycle: bootstrap
- Session: none
- Harness: claude-code
- Supersedes: none

### Project
- Name: OpenMontage
- Root: session launch CWD
- Context policy: v1

### Initialization
- Trigger: /init-git
- Context.md: canonical and append-only
- Context.html: generated human-readable twin

### Project Context Plan
- Authority Order: protected instructions; current user; root agent instructions; approved specification and plan; source, tests, and evidence; Context.md summaries and pointers.
- Default Preload: root instructions; latest effective Project Context Plan; latest selected state; governing artifacts named by the task.
- Retrieve When Needed: older Context.md entries; neighboring source and tests; Git history; external documentation.
- Persistence: lifecycle state, user decisions, changed artifacts, verification, unresolved items, and next action; never transcripts, secrets, or raw output.
- Compaction And Resume: compaction remains the same session; when apparent, run a read-only brief and checkpoint only a material mismatch.
- Subagents: provide minimum governing artifacts, scope, prohibitions, output contract, and evidence; persist only distilled results.
- Workflow Gates: draft spec to sdp-spec-review; approved spec to writing-plans; written plan to sdp-plan-review; accepted plan to execution; completed implementation to verification and Gauntlet.

### Next Action
Begin the first meaningful project session.

<!-- context-entry:end -->

<!-- context-entry:start -->
## CTX-000002 | session-start

- Timestamp: 2026-09-04T22:57:21Z
- Lifecycle: implement
- Session: SES-20260904T225721Z-claude-code-e0766002
- Harness: claude-code
- Supersedes: none

### Objective
Clone OpenMontage from upstream, satisfy documented prerequisites, install it, and bring the local instance to a verified working state without writing project code.

### Previous State
- No prior ledger; this is the project's first session.
- Ledger adoption was proposed late and accepted mid-session; entries before CTX-000002 are retrospective.

### Governing Artifacts
- AGENT_GUIDE.md - agent contract, Rule Zero, mandatory preflight
- PROJECT_CONTEXT.md - architecture and conventions
- docs/ARCHITECTURE.md - three-layer knowledge model and system dependencies
- docs/apple-silicon-mps.md - MPS device selection and known limitations
- Makefile - setup, demo, test, doctor targets

### Working Set
- .env - local provider configuration, gitignored
- .venv - Python 3.10.20 virtual environment created by uv
- remotion-composer/node_modules - Remotion render dependencies
- projects/demos/renders - zero-key demo output
- Context.md and Context.html - this ledger pair

### Retrieve When Needed
- skills/meta/onboarding.md for first-run user routing
- pipeline_defs manifests for stage and required-tool detail
- tools/tool_registry.py provider_menu_summary for live capability state

### Open Items
- Free-signup keys not yet obtained: PEXELS_API_KEY, PIXABAY_API_KEY, FREESOUND_API_KEY
- music_library directory not created; gitignored and absent on fresh clone
- Local video generation left disabled pending a deliberate benchmark
- Session memory capture via session-end not yet run

### Next Action
Record a retrospective checkpoint covering install, verification, fork, and port allocation, then close the session.

### Next Gate
User decision on obtaining the three free provider keys and on enabling local video generation.

<!-- context-entry:end -->

<!-- context-entry:start -->
## CTX-000003 | checkpoint

- Timestamp: 2026-09-04T22:57:42Z
- Lifecycle: implement
- Session: SES-20260904T225721Z-claude-code-e0766002
- Harness: claude-code
- Supersedes: none

### Current Objective
Retrospectively record the install, verification, fork, and port decisions made before the ledger was adopted.

### Decisions Since Previous Boundary
- Installed into a uv-created Python 3.10.20 venv, matching the repo pin, rather than the system 3.14.7.
- Chose Blender 4.5.13 LTS over the Homebrew 5.2.1 cask because blender_world pins BLENDER_EEVEE_NEXT, which exists only in the 4.2 to 4.5 series; verified on the installed build that this is the sole engine identifier and that import_scene.gltf is present.
- Set BLENDER_PATH in .env rather than the shell profile, since tool_registry and base_tool both auto-load .env.
- Rejected upscale and face_restore permanently: realesrgan and gfpgan pull basicsr 1.4.2, whose degradations module imports torchvision.transforms.functional_tensor, removed in torchvision 0.17, against a resolved torchvision 0.29.0.
- Forked upstream to the user's account; origin now points at the fork and upstream at the original, so customisations are committable.
- Allocated port 8004 to Backlot, continuing the 8000 to 8003 FastAPI band, and carried BACKLOT_PORT in the registered start command because the backlot package does not load .env.
- Left VIDEO_GEN_LOCAL_ENABLED unset; enabling it makes four local video generators selectable and would trigger multi-gigabyte weight downloads and an unbenchmarked render.

### Changed Artifacts
- .env - added BLENDER_PATH
- ~/.ports and ~/Code/ServerPorts/Server-Ports-2026-04-13.md - registered Backlot on 8004 and widened the FastAPI band heading
- projects/demos/renders - three rendered demo videos
- Git remotes - origin retargeted to the fork, upstream added

### Verification State
- make test-contracts: 1210 passed, 7 skipped.
- make setup exited 0; make hyperframes-doctor reports runtime available with node, ffmpeg and npx present.
- Registry preflight: 59 of 117 tools configured, with ffmpeg, remotion and hyperframes all true.
- Torch device resolves to mps; torch 2.14.0 with MPS available and built.
- Piper rendered a 2.3 second WAV after downloading the en_US-lessac-medium voice.
- Manim v0.19.1 checkhealth passes except LaTeX, and rendered a test MP4.
- make demo produced three h264 1920x1080 30fps files of 25.0, 22.5 and 23.1 seconds.
- Backlot answers ok true on 127.0.0.1 port 8004; push to the fork succeeds.

### Unresolved Items
- Three free provider keys still outstanding.
- music_library directory still absent.
- Upstream documentation defects found but not reported: the Piper voice-download command is stale for piper-tts 1.7.0, and documentary-montage omits the zero-key pixabay_music from tools_available.
- Selector tools are excluded from provider_menu, so absence there must not be read as unavailability.

### Next Action
Await user direction on the outstanding free keys and on enabling local video generation.

### Next Gate
User decision before any first real production run.

<!-- context-entry:end -->

<!-- context-entry:start -->
## CTX-000004 | checkpoint

- Timestamp: 2026-09-04T23:29:55Z
- Lifecycle: implement
- Session: SES-20260904T225721Z-claude-code-e0766002
- Harness: claude-code
- Supersedes: none

### Current Objective
Close the remaining local loose ends after the install, excluding the free provider keys the user reserved.

### Decisions Since Previous Boundary
- Created the music_library directory; it is gitignored at .gitignore line 39 and therefore stays local rather than being committed.
- Installed whisper-cpp as a Homebrew formula, giving HyperFrames its own transcription path independent of the pipeline transcriber that faster-whisper already covers.
- Synchronised the ServerPorts markdown registry with the machine-readable port list, which had drifted since 2026-04-13.
- Declined to install MacTeX: the Homebrew cask is a Pkg artifact requiring sudo, and this session's shell has no tty, so the password prompt would hang rather than fail.
- Declined to file upstream defect reports without explicit direction, since publishing issues on a third-party repository is an outward-facing action.

### Changed Artifacts
- music_library - created, gitignored, local only
- Server-Ports-2026-04-13.md - nine allocations added, band headings widened, date updated; committed and pushed
- Homebrew - whisper-cpp 1.9.2 installed

### Verification State
- Port registries verified equal in both directions by set difference, not by inspection; the check surfaced two allocations that visual review had missed.
- hyperframes doctor now reports whisper-cpp present at the Homebrew path.
- ServerPorts pushed; OpenMontage ledger pair remains clean against its own remote.

### Unresolved Items
- Three free provider keys remain outstanding by user instruction.
- MacTeX blocked on a real terminal; only affects Tex and MathTex in Manim.
- HyperFrames optional local fallbacks Kokoro TTS and MusicGen remain uninstalled.
- Two upstream documentation defects recorded but unreported.
- A commit-attribution conflict between the user's standing rule and this session's harness directive is unresolved; commits so far follow the harness directive.

### Next Action
Await the user's first production request, or direction on the outstanding items.

### Next Gate
User decision before the first real production run.

<!-- context-entry:end -->

<!-- context-entry:start -->
## CTX-000005 | checkpoint

- Timestamp: 2026-09-04T23:30:42Z
- Lifecycle: implement
- Session: SES-20260904T225721Z-claude-code-e0766002
- Harness: claude-code
- Supersedes: none

### Current Objective
Resolve the two HyperFrames local fallbacks that CTX-000004 recorded as outstanding.

### Decisions Since Previous Boundary
- Installed kokoro-onnx and soundfile into the project virtual environment. MusicGen needed only soundfile, since transformers, torch and numpy were already present from the earlier torch install.

### Changed Artifacts
- .venv - added kokoro-onnx 0.6.1, soundfile 0.14.0, phonemizer 3.4.0, joblib 1.6.0

### Verification State
- hyperframes doctor now reports Kokoro TTS and MusicGen deps installed, alongside whisper-cpp.
- The only remaining doctor failure is Docker not running, which is a user action and optional.

### Unresolved Items
- Kokoro and MusicGen supersede the corresponding entry in CTX-000004; that item is now closed.
- Three free provider keys remain outstanding by user instruction.
- MacTeX still blocked on a real terminal.
- Two upstream documentation defects recorded but unreported.
- Commit-attribution conflict still unresolved.

### Next Action
Await the user's first production request, or direction on the outstanding items.

### Next Gate
User decision before the first real production run.

<!-- context-entry:end -->

<!-- context-entry:start -->
## CTX-000006 | checkpoint

- Timestamp: 2026-09-04T23:33:58Z
- Lifecycle: implement
- Session: SES-20260904T225721Z-claude-code-e0766002
- Harness: claude-code
- Supersedes: none

### Current Objective
Record the user's ruling on the commit-attribution conflict.

### Decisions Since Previous Boundary
- User ruled that this session's harness attribution directive takes precedence over the standing instruction against commit co-authors. Existing commits stand unamended and subsequent commits in this session carry the trailers.
- The ruling is scoped to this session and does not revoke the standing rule for future sessions.

### Changed Artifacts
- No files changed; this entry records a policy decision only.

### Verification State
- Four commits carry the trailers: 18aff53, b2d37d1, 9af3508 in OpenMontage and e7db848 in ServerPorts.

### Unresolved Items
- The attribution item recorded in CTX-000004 and CTX-000005 is now closed.
- Three free provider keys remain outstanding by user instruction.
- MacTeX blocked pending a real terminal.
- Two upstream documentation defects recorded but unreported.

### Next Action
Await the user's first production request, or direction on the outstanding items.

### Next Gate
User decision before the first real production run.

<!-- context-entry:end -->

<!-- context-entry:start -->
## CTX-000007 | handoff

- Timestamp: 2026-09-05T15:42:18Z
- Lifecycle: implement
- Session: SES-20260904T225721Z-claude-code-e0766002
- Harness: claude-code
- Supersedes: none

### Recipient
The next Claude Code session working on OpenMontage.

### Objective
Complete the Spacesuit Bridge video by driving the cinematic pipeline properly, rather than by calling generation tools directly.

### Current State
- OpenMontage is installed and verified: 59 of 117 tools configured, all three composition runtimes green, contract tests 1210 passed with 7 skipped.
- One paid clip exists: projects/spacesuit-bridge/assets/video/shot01-bridge-reveal.mp4, 8.0s, 1280x720, h264 with AAC audio. $0.80 spent of a $10 budget.
- The user accepted the likeness as good enough for a prototype. A known defect remains: the suit carries a United States flag patch and the user is Canadian.
- The clip's gemini_omni interaction is stored and editable, so a surgical edit_video can fix the patch for $0.80.
- The Backlot board at port 8004 shows a project card but an empty filmstrip. This is the direct consequence of the mistake recorded below.

### Governing Artifacts
- AGENT_GUIDE.md - Rule Zero, mandatory preflight, project directory convention at lines 203 to 231
- pipeline_defs/cinematic.yaml - the manifest for this production
- skills/pipelines/cinematic/ - stage director skills, read each before executing its stage
- .agents/skills/gemini-omni/SKILL.md - prompt tags, timecodes, conversational editing
- lib/source_media_review.py - required ingest gate if the user imports externally generated footage
- backlot/README.md - which artifacts each board panel derives from

### Constraints
- Rule Zero: all production goes through the pipeline. Do not call generation tools directly.
- Budget is $10 total with single_action_approval_usd at 0.50, so every video generation needs explicit user approval before spending.
- Live keys are OPENAI_API_KEY, GEMINI_API_KEY and RUNWAYML_API_SECRET. FAL_KEY, MINIMAX_API_KEY and the three free stock keys are not set.
- Local video generation stays disabled; that decision was made deliberately and agreed.
- Every tool must receive an explicit output_path under projects/spacesuit-bridge/.

### Verification State
- Three registry-contradicting facts were verified this session and must not be re-derived from the registry alone.
- First: gemini_omni_video accepts an opening frame through the FIRST_FRAME prompt tag even though its supports map says first_last_frame_to_video is False. That flag only means it cannot pin both ends. Frame-chained continuity therefore works today with the existing key and no new spend.
- Second: the repo's hardcoded cost constants are wrong in both directions. kling_video under-estimates by about 3.5 times, quoting $0.02 per second against fal's published $0.07. minimax_video over-estimates by 1.6 to 2.9 times. Budget mode warn meters against these figures.
- Third: selector tools are excluded from provider_menu output by design. Absence from that menu is not unavailability; call get_status directly. Reading the menu naively produced a false negative earlier in this session.
- Provider pricing was checked against primary sources: fal publishes Kling 2.5 Turbo Pro at $0.07 per second and Hailuo-02 at $0.045 per second for 768p. MiniMax's own package rate works out to $0.266 per point against fal's $0.27 for the same clip, so fal's markup is effectively zero while removing MiniMax's $1000 minimum commitment.

### Unresolved Items
- The suit's flag patch is still wrong.
- Whether to buy FAL_KEY, which unlocks ten already-built tools for one environment variable and no engineering.
- Whether to build an OpenRouter video tool. None exists: the repo has one vestigial comment in config.yaml and zero Python references. OpenRouter does now serve video, and Veo 3.1 Lite at $0.03 to $0.08 per second is the cheapest continuity route found.
- Whether to import footage the user generates in their own Runway, Grok and Gemini subscriptions. This is likely the strongest route and lib/source_media_review.py is the required gate for it.
- Three free provider keys remain unobtained by user instruction.
- MacTeX remains blocked because the cask is a Pkg needing sudo and this shell has no tty.

### First Action
Read pipeline_defs/cinematic.yaml, then run the mandatory preflight and present the capability menu. Do not generate anything before the user approves a production plan. Backfilling the pipeline's artifacts is what will populate the Backlot filmstrip.

### Next Gate
User approval of the production plan and of any spend above $0.50 before asset generation resumes.

<!-- context-entry:end -->

<!-- context-entry:start -->
## CTX-000008 | session-start

- Timestamp: 2026-09-05T17:05:54Z
- Lifecycle: implement
- Session: SES-20260905T170554Z-claude-code-110b44a5
- Harness: claude-code
- Supersedes: none

### Objective
Add the provider API keys the user obtained, verify the resulting capability change, and correct the handoff that had already been written against the pre-key state.

### Previous State
- CTX-000007 closed the prior session with a handoff recording 59 of 117 tools and FAL_KEY unset.
- The user then obtained and entered FAL_KEY plus four free stock and audio keys, invalidating those figures.

### Governing Artifacts
- .env - provider configuration, gitignored
- AGENT_GUIDE.md - mandatory preflight and provider menu protocol
- tools/tool_registry.py - provider_menu_summary is the measurement

### Working Set
- .env - six provider keys plus BLENDER_PATH
- next-session.md - the durable handoff the next session loads at startup
- memory/project_openmontage_state_and_gotchas.md - the project memory entry

### Retrieve When Needed
- fal.ai published pricing for real per-second rates, since estimate_cost is unreliable
- backlot/README.md for which artifacts the board joins

### Open Items
- XAI_API_KEY remains unset.
- music_library directory exists but holds no audio files.
- The US flag on the generated suit is still wrong.

### Next Action
Measure the new capability envelope, then supersede CTX-000007 with a corrected handoff.

### Next Gate
User decision on which model to use for the next shot.

<!-- context-entry:end -->

<!-- context-entry:start -->
## CTX-000009 | handoff

- Timestamp: 2026-09-05T17:06:18Z
- Lifecycle: implement
- Session: SES-20260905T170554Z-claude-code-110b44a5
- Harness: claude-code
- Supersedes: CTX-000007

### Recipient
The next Claude Code session working on OpenMontage.

### Objective
Complete the Spacesuit Bridge video by driving the cinematic pipeline properly, rather than by calling generation tools directly.

### Current State
- Supersedes CTX-000007, whose tool count and key list were correct when written and are now stale.
- Configured tools: 74 of 117, all three composition runtimes true. Progression: 47 to 59 via free installs, to 69 with FAL_KEY, to 74 with four free stock and audio keys.
- FAL_KEY unlocked exactly ten tools, including seedance_video, the repo's self-declared preferred premium default for cinematic and multi-shot work with synchronised audio.
- Keys in .env: FAL_KEY with its FAL_AI_API_KEY alias, RUNWAYML_API_SECRET, PEXELS_API_KEY, PIXABAY_API_KEY, UNSPLASH_ACCESS_KEY, FREESOUND_API_KEY, BLENDER_PATH. OPENAI_API_KEY and GEMINI_API_KEY are in the shell profile only and would be absent under cron or launchd.
- Still unset: XAI_API_KEY, MINIMAX_API_KEY, KLING_API_KEY, ELEVENLABS_API_KEY, SUNO_API_KEY.
- Spend unchanged at 0.80 dollars of a 10 dollar budget. shot01-bridge-reveal.mp4 predates every new key and used Gemini Omni.
- The Backlot board still shows an empty filmstrip for spacesuit-bridge because the prior session bypassed the pipeline.

### Governing Artifacts
- AGENT_GUIDE.md - Rule Zero, mandatory preflight, project directory convention at lines 203 to 231
- pipeline_defs/cinematic.yaml - the manifest for this production
- skills/pipelines/cinematic/ - stage director skills, read each before executing its stage
- backlot/README.md - which artifacts each board panel derives from
- lib/source_media_review.py - required gate for user-supplied footage

### Constraints
- Rule Zero: all production goes through the pipeline. Do not call generation tools directly.
- single_action_approval_usd is 0.50 and every video generation exceeds it, so each needs explicit user approval.
- Local video generation stays disabled by an agreed decision.
- Every tool must receive an explicit output_path under projects/spacesuit-bridge/.

### Verification State
- Four registry-contradicting facts from the prior session still hold: gemini_omni_video accepts an opening frame via the FIRST_FRAME prompt tag despite its supports flag; selector tools are excluded from provider_menu so absence there is not unavailability; estimate_cost constants are wrong in both directions; upscale and face_restore are permanently broken by basicsr against torchvision 0.29.
- Three further wrong predictions were measured when the keys landed. corpus_builder moved to DEGRADED, a real third state, not to AVAILABLE. There is no unsplash_image tool at all; UNSPLASH_ACCESS_KEY only feeds a source adapter used by corpus_builder and direct_clip_search. music_library requires actual audio files, not merely its directory.
- Real per-second prices verified against fal's own published page: Kling 2.5 Turbo Pro at 0.07, Hailuo-02 768p at 0.045. An eight second clip is roughly 0.36 to 0.56 dollars against the 0.80 Omni charged.

### Unresolved Items
- Which model to use for shot two onward now that seedance_video and nine other fal tools are available.
- The suit carries a United States flag patch and the user is Canadian; one surgical edit_video on the stored interaction fixes it.
- XAI_API_KEY is the only cheap key still unset and its stated strength is reference-conditioned character consistency.
- music_library holds no audio files.
- Whether to import footage from the user's own Runway, Grok and Gemini subscriptions through source_media_review.

### First Action
Read pipeline_defs/cinematic.yaml, run the mandatory preflight, and present the capability menu against the 74-tool envelope. Do not generate anything before the user approves a production plan.

### Next Gate
User approval of the production plan and of any spend above 0.50 dollars.

<!-- context-entry:end -->

<!-- context-entry:start -->
## CTX-000010 | session-start

- Timestamp: 2026-09-06T00:25:21Z
- Lifecycle: implement
- Session: SES-20260906T002521Z-claude-code-71f63778
- Harness: claude-code
- Supersedes: none

### Objective
Run the cinematic pipeline properly for projects/spacesuit-bridge so each stage writes its real canonical artifact and the Backlot board fills in.

### Previous State
- CTX-000009 handoff closed the previous session idle with the board filmstrip empty because generation tools were called directly, bypassing Rule Zero.
- projects/spacesuit-bridge/ holds project.json, events.jsonl, assets/video/shot01-bridge-reveal.mp4 and assets/images/steve-reference.jpg. artifacts/ and renders/ are empty and no checkpoint files exist.
- Spend is 0.80 dollars of a 10 dollar budget.

### Governing Artifacts
- AGENT_GUIDE.md - Rule Zero, mandatory preflight, project directory convention, checkpoint protocol
- pipeline_defs/cinematic.yaml - stage order, required tools, gates, human_approval_default per stage
- skills/pipelines/cinematic/ - one director skill per stage, read before executing that stage
- schemas/artifacts/ - JSON schemas each canonical artifact must validate against
- lib/checkpoint.py - checkpoint writes and gate enforcement

### Working Set
- projects/spacesuit-bridge/artifacts/ - target for brief, script, scene_plan, asset_manifest, edit_decisions, render_report
- projects/spacesuit-bridge/checkpoint_STAGE.json - per-stage checkpoints the board watches
- tools/tool_registry.py - preflight via provider_menu_summary()

### Retrieve When Needed
- backlot/README.md - which artifacts each board panel derives from
- skills/meta/checkpoint-protocol.md and skills/meta/reviewer.md
- .agents/skills/seedance-2-0/ and .agents/skills/gemini-omni/ - Layer 3 prompting knowledge before any generation call
- lib/source_media_review.py - required gate if user-supplied footage is imported

### Open Items
- Which model for shot two onward now that seedance_video and nine other fal tools are live.
- The suit carries a United States flag patch and the user is Canadian.
- XAI_API_KEY remains unset; its stated strength is reference-conditioned character consistency.
- music_library holds no audio files.
- Whether to import footage from the user's own Runway, Grok and Gemini subscriptions through source_media_review.

### Next Action
Read pipeline_defs/cinematic.yaml, run the mandatory preflight against the 74-tool envelope, then read the idea-stage director skill and execute the first stage. Generate nothing before the user approves a production plan.

### Next Gate
User approval of the production plan and of any single action above 0.50 dollars.

<!-- context-entry:end -->

<!-- context-entry:start -->
## CTX-000011 | checkpoint

- Timestamp: 2026-09-06T00:41:12Z
- Lifecycle: implement
- Session: SES-20260906T002521Z-claude-code-71f63778
- Harness: claude-code
- Supersedes: none

### Current Objective
Run the cinematic pipeline properly for spacesuit-bridge so each stage writes its real canonical artifact.

### Decisions Since Previous Boundary
- d-003 provider_selection: grok_video at 0.56 dollars per 8-second 720p shot, chosen over seedance_video at 2.43 and gemini_omni_video at 0.80. Reference-image conditioning is the capability the piece needs and seedance for four shots exceeds the whole remaining budget.
- d-005 render_runtime_selection: remotion recommended, with hyperframes and ffmpeg both measured and presented. Not locked; user_approved is false.
- d-006 composition_mode: templated for concepts A, B and C because the generated footage is the entire creative surface; atelier only if the user picks concept D.
- d-007 music_source: freesound_music, free and auditionable. music_library is empty so the music_library tool reports unavailable.
- d-008 playbook_override: no style playbook. All five installed playbooks were read and none targets live-action-style cinematic footage; the manifest's recommended flat-motion-graphics is the worst fit of the five.
- d-010 budget_tradeoff: regenerate all four shots on grok_video for 2.24 dollars rather than keep shot01 for 1.68, conditional on a single sample comparing well. Regenerating fixes the flag patch in the same pass for less than a standalone edit would cost.

### Changed Artifacts
- projects/spacesuit-bridge/artifacts/research_brief.json - new, schema-valid, 12 web searches, 14 sources, 4 cinematic directions
- projects/spacesuit-bridge/artifacts/proposal_packet.json - new, schema-valid, 4 concepts, per-item cost estimate, both composition runtimes presented
- projects/spacesuit-bridge/artifacts/decision_log.json - new, 10 decisions, all user_approved false
- projects/spacesuit-bridge/checkpoint_research.json - status completed
- projects/spacesuit-bridge/checkpoint_proposal.json - status awaiting_human, human_approved false
- projects/spacesuit-bridge/decision_log.json - written at project root by the checkpoint utility's decision-log merge
- Context.md and Context.html - this ledger

### Verification State
- Both checkpoints passed lib.checkpoint schema validation; write_checkpoint validates each canonical artifact against schemas/artifacts before writing.
- get_completed_stages returns research; get_next_stage returns proposal, which is correct for a gate held open.
- The live Backlot server on port 8004 serves the real state at /api/project/spacesuit-bridge/state: research completed, proposal awaiting_human, three artifacts loaded, ten decisions, cost meter populated.
- The filmstrip is still empty by design. It joins scene_plan, script and asset_manifest, none of which exist until later stages.
- Zero dollars spent this session. Spend remains 0.80 of 10.00.

### Unresolved Items
- User has not selected a concept, a runtime, a duration, or an aspect ratio, and has not approved the 0.56 dollar sample. The proposal gate is open.
- XAI_API_KEY item is CLOSED. The key is present in .env at 84 characters with an xai- prefix and grok_video reports AVAILABLE. The prior handoff recorded it as unset.
- The United States flag patch is still present in shot01 and is now folded into the regeneration decision rather than a separate edit.
- music_library still holds no audio files, but freesound and pixabay search cover the need at zero cost.
- Importing the user's own Runway, Grok or Gemini footage through source_media_review remains a live alternative path recorded in the proposal.

### Next Action
Wait for the user at the proposal gate. On approval, write the checkpoint completed with human_approved true, then execute the script stage after reading its director skill.

### Next Gate
Proposal approval, including explicit approval of the 0.56 dollar sample generation, which exceeds the 0.50 single_action_approval_usd threshold.

<!-- context-entry:end -->

<!-- context-entry:start -->
## CTX-000012 | checkpoint

- Timestamp: 2026-09-06T00:56:45Z
- Lifecycle: implement
- Session: SES-20260906T002521Z-claude-code-71f63778
- Harness: claude-code
- Supersedes: none

### Current Objective
Enable Gemini Omni 1.1 Flash through the existing keys and verify the request contract before any paid call.

### Decisions Since Previous Boundary
- d-013 capability_extension: user approved repointing gemini_omni_fal at the v1.1 endpoints and defaulting gemini_omni_video to gemini-omni-1.1-flash. Supersedes d-012, which was proposed-only.
- d-014 provider_selection: Omni 1.1 via fal now recommended over grok_video. Supersedes d-011. Costs 1.20 dollars more across four shots and buys first-and-last-frame continuity plus a 0.24 dollar likeness draft. Still not user-approved; the gate stays open.
- A material correction to what d-011 and d-012 claimed: scene extension is NOT exposed on fal. It is a multi-turn previous_interaction_id workflow on Google's Interactions API and therefore belongs to gemini_omni_video, not the fal route.

### Changed Artifacts
- tools/video/gemini_omni_fal.py - v1.1 endpoints, resolution tiers, end_image_url, reference_video_urls, resolution-aware cost, version 0.3.0
- tools/video/gemini_omni_video.py - default model gemini-omni-1.1-flash, model now selectable, preview id retained
- tests/tools/test_gemini_omni_fal_v11_payloads.py - new, 10 tests locking payload shape and per-resolution pricing
- tests/tools/test_new_video_model_support.py, test_gemini_omni_video.py, test_provider_model_defaults.py - updated for the new endpoints and model, and gemini_omni_video added to the model-default guard
- projects/spacesuit-bridge/artifacts/proposal_packet.json - assets stage, cost estimate and alternative paths rebuilt around Omni 1.1
- projects/spacesuit-bridge/artifacts/decision_log.json - d-013 and d-014 appended, 14 decisions total

### Verification State
- All four fal operations were diffed against fal's LIVE OpenAPI documents at fal.ai/api/openapi/queue/openapi.json. Exact key match on every operation, zero unknown fields, zero missing required fields, correct queue URLs. Zero dollars spent: requests.post was intercepted before send.
- Model ids gemini-omni-1.1-flash and gemini-omni-flash-preview verified against ai.google.dev model documentation rather than a launch article.
- Full test suite: 1839 passed, 12 skipped, 3 xfailed, 0 failed. Baseline before the change was 1829 passed; the 10 new tests are the difference.
- Corrected a fourth wrong in-repo price constant. The flat 0.13 per second over-reported 720p by 30 percent. Real tiers are 0.03, 0.10, 0.15 and 0.30 per second.
- The live Backlot board on port 8004 serves 14 decisions and the revised 3.44 dollar plan.
- Spend still 0.80 of 10.00. Nothing generated.

### Unresolved Items
- The proposal gate is still open. No concept, provider, runtime, duration or aspect ratio has been chosen.
- gemini_omni_video does not plumb 1.1's first-and-last-frame or above-720p resolution fields, so its supports map still reports first_last_frame_to_video false. That is accurate for the tool and is documented in a comment.
- The fal edit endpoint returns an interaction_id but accepts none as input, so multi-turn resume is unavailable on that route.
- The United States flag patch is still in shot01 and is folded into the regeneration decision.
- These tool changes diverge from upstream calesthio/OpenMontage and are candidates for a pull request.

### Next Action
Wait at the proposal gate. On approval, generate one 360 pixel likeness draft at 0.24 dollars, compare it against shot01, then proceed to the script stage.

### Next Gate
Proposal approval. The 0.24 dollar draft sits under the 0.50 single-action threshold; the four 720p takes at 3.20 dollars do not.

<!-- context-entry:end -->

<!-- context-entry:start -->
## CTX-000013 | checkpoint

- Timestamp: 2026-09-06T01:08:17Z
- Lifecycle: implement
- Session: SES-20260906T002521Z-claude-code-71f63778
- Harness: claude-code
- Supersedes: none

### Current Objective
Use Omni 1.1 over the direct Google key rather than through the fal gateway.

### Decisions Since Previous Boundary
- d-015 provider_selection: gemini_omni_video on the direct Google key replaces gemini_omni_fal as primary. Supersedes d-014. fal is demoted to a fallback failure domain and grok_video to a second fallback.
- Reverted a quality_score bump from 0.85 to 0.9 on gemini_omni_video. The justification was real, since 1.1 lifted the 720p ceiling, but that value ranks the entire tool fleet through lib/scoring.py and no ranking comparison was run. The reasoning is recorded in a comment so the next session can raise it alongside the measurement.

### Changed Artifacts
- tools/video/gemini_omni_video.py - plumbs response_format.resolution across four tiers, prices per tier, declares first_last_frame_to_video true, corrected best_for and not_good_for and install_instructions
- tests/tools/test_gemini_omni_video.py - response_format assertion updated, six tests added for resolution passthrough, per-tier cost and rejection of an unsupported value
- .agents/skills/gemini-omni/SKILL.md - documents LAST_FRAME, the resolution and draft tier, and scene extension with its constraints; front matter no longer names the preview model as the default
- projects/spacesuit-bridge/artifacts/proposal_packet.json - assets stage and alternative paths rebuilt around the direct route
- projects/spacesuit-bridge/artifacts/decision_log.json - d-015 appended, 15 decisions total

### Verification State
- Direct-route capabilities confirmed against ai.google.dev/gemini-api/docs/omni: response_format accepts type, aspect_ratio, resolution and delivery; resolution takes 360p, 720p default, 1080p and 4k; first and last frame are bound with FIRST_FRAME and LAST_FRAME prompt tags over two images in the input list; continuation uses previous_interaction_id.
- Measured after the change: both routes quote 0.24 dollars for an 8 second 360p clip and 0.80 for 720p. Identical pricing, and the direct route additionally reports first_last_frame_to_video true and conversational_editing true.
- Full suite: 1845 passed, 12 skipped, 3 xfailed, 0 failed.
- A fifth wrong price constant is now fixed. The direct tool's flat 0.10 per second under-quoted 4k by a factor of three and over-quoted a 360p draft by more than three.
- NOT verifiable the way the fal route was: Google's Interactions API publishes no OpenAPI document to diff a payload against, so the direct request shape rests on documentation plus unit tests rather than a live schema comparison. A 0.24 dollar draft is the cheapest real proof.
- Spend still 0.80 of 10.00. Nothing generated.

### Unresolved Items
- The proposal gate is still open. No concept, provider, runtime, duration or aspect ratio chosen.
- The direct request shape is unverified against a live schema. The 360p draft would settle it for 0.24 dollars, under the single-action threshold.
- gemini_omni_video's quality_score stays 0.85 pending a fleet ranking comparison.
- The United States flag patch is still in shot01, folded into the regeneration decision.
- These tool and skill changes diverge from upstream calesthio/OpenMontage and are candidates for a pull request.

### Next Action
Wait at the proposal gate. On approval, run one 360 pixel draft on the direct route for 0.24 dollars, which both tests the likeness and proves the request shape, then proceed to the script stage.

### Next Gate
Proposal approval. The 0.24 dollar draft is under the 0.50 single-action threshold; the four 720p takes at 3.20 dollars are not.

<!-- context-entry:end -->

<!-- context-entry:start -->
## CTX-000014 | checkpoint

- Timestamp: 2026-09-06T02:11:52Z
- Lifecycle: implement
- Session: SES-20260906T002521Z-claude-code-71f63778
- Harness: claude-code
- Supersedes: none

### Current Objective
Isolate local additions from upstream, and upstream the Omni fixes so the divergence can go to zero.

### Decisions Since Previous Boundary
- User approved both the om_ext isolation package and opening an upstream pull request.
- Additions go in om_ext, loaded through the package_name argument that ToolRegistry.discover already accepts. No upstream file is modified, so a merge can never conflict with them.
- No schema edit was made. research_brief.metadata is declared as an unconstrained object, so local reference images validate today under metadata.local_visual_references. A planned upstream schema change was cancelled after testing.
- Fixes to upstream files cannot be isolated by nature, so they went to a pull request rather than being carried indefinitely.

### Changed Artifacts
- om_ext/ - new isolated package: contact_sheet tool, visual-reference-board skill addendum, five tests, README stating the trade-off
- projects/spacesuit-bridge/artifacts/research_brief.json - nine local visual references with per-image defects, contact sheet path, provenance, and the known gap against decision d-016
- projects/spacesuit-bridge/artifacts/source_media_review.json - ingest gate output for the nine stills
- projects/spacesuit-bridge/assets/images/ - nine files renamed from Unknown-N to self-describing names, plus CONTACT-SHEET-bridge-formations.jpg
- Branch fix/gemini-omni-1.1 pushed to origin; pull request 633 opened against calesthio/OpenMontage

### Verification State
- Isolation is asserted by a test, not by intention: discover('tools') must NOT find contact_sheet and discover('om_ext') must. Measured 121 upstream tools, one added.
- No upstream module imports om_ext. Verified with a word-boundary grep after a naive grep produced a false positive inside the word from_extension.
- Full suite on main: 1850 passed, 12 skipped, 3 xfailed.
- Full suite on the pull request branch, which carries upstream code plus the fix only: 1845 passed, 12 skipped, 3 xfailed.
- The pull request branch was confirmed to carry exactly seven files. om_ext, Context.md and projects are absent from it; only gitignored pycache directories remained on disk.
- Pull request 633 is OPEN: 7 files changed, 401 insertions, 44 deletions.
- Spend still 0.80 of 10.00. Nothing generated this session.

### Unresolved Items
- The proposal gate is still open. No concept, provider, runtime, duration or aspect ratio chosen, and no bridge formation picked.
- All nine bridge stills contradict decision d-016: they place Earth ahead of the subject with the camera behind him, so he is looking at what he is meant to refuse to look at. Valid for choosing a room, invalid as shot references.
- Formations F2 and F3 as generated have no control within reach of the chair, so the agreed action of pressing a button cannot be staged in them without a regeneration.
- Pull request 633 awaits maintainer review. Until it merges or closes, those seven files are the entire conflict surface against upstream.
- The United States flag patch recurs in the newly generated stills as well as in shot01.

### Next Action
Return to the brainstorm. The user picks a bridge formation, or asks for the hybrid prompt combining F2's empty room with F1's reachable console.

### Next Gate
Formation choice, then proposal approval covering concept, provider, runtime and aspect ratio.

<!-- context-entry:end -->

<!-- context-entry:start -->
## CTX-000015 | checkpoint

- Timestamp: 2026-09-06T02:41:31Z
- Lifecycle: implement
- Session: SES-20260906T002521Z-claude-code-71f63778
- Harness: claude-code
- Supersedes: none

### Current Objective
Give the production work real backup and version history without polluting the OpenMontage fork.

### Decisions Since Previous Boundary
- Rejected the mono-repo. The projects/ ignore rule is upstream's own line 29, so un-ignoring it would edit an upstream file and add conflict surface, and it would bind generated media to the fork's history permanently. The fork's .git is already 76 MB and a finished production runs to hundreds of megabytes.
- Chose a nested repository instead. projects/spacesuit-bridge is now its own git repo pushed to a private kraaft007/spacesuit-bridge. Because the parent already ignores projects/, git never looks inside, so the nested repo is invisible to the fork and needs no gitignore change.
- d-017 recorded earlier: bridge formation locked to F4, a two-seat cockpit the user generated himself outside the three formations offered.
- Backlot References panel built and opened as pull request 634.

### Changed Artifacts
- New private repository kraaft007/spacesuit-bridge, 31 files, first commit 276c9b9
- projects/spacesuit-bridge/README.md and .gitignore - new
- projects/spacesuit-bridge/assets/images/F4-two-seat-cockpit-empty-copilot.jpg - selected formation, renamed from a filename containing spaces
- backlot/state.py, ui/board.js, ui/board.css - References panel
- Pull request 634 opened against calesthio/OpenMontage

### Verification State
- Secret scan before publishing: no key values present. Matches on API_KEY are key NAMES written in prose, for example the note that XAI_API_KEY is 84 characters. A value-shaped scan for xai-, sk-, AIza, key_ and uuid:secret patterns returned nothing.
- Fork remains clean after the nested repo was created: git status reports no changes, confirming git does not descend into an ignored directory.
- Backed up: 31 files, 16 artifacts and 13 media. Not backed up by choice: projects/demos, 12 MB, regenerable from scripts/backlot_simulate_run.py.
- References panel verified in a real browser through Playwright: renders, 12 images, 12 working media links. The single console error is a pre-existing missing favicon.
- Suite on the pull request branch: 1828 passed, 12 skipped, 3 xfailed.
- Syncthing was found to already replicate ~/Code including projects/, but replication is not backup: deletions propagate and .git is excluded, so no history travels. The user directed that Syncthing be disregarded.
- Spend still 0.80 of 10.00.

### Unresolved Items
- The proposal gate is still open. Formation is locked but concept, duration, aspect ratio and provider approval are not.
- The four concept options in proposal_packet are stale. All predate the locked story and none knows about F4 or the empty copilot seat.
- One creative question is outstanding and shapes the shot list: whether the subject acknowledges the gloves on the empty seat.
- Two pull requests await maintainer review: 633 for the Omni fixes, 634 for the References panel.
- The United States flag patch recurs in F4 as well and rides into the regeneration.

### Next Action
Rewrite the sequence around the locked story and F4, then take it to the proposal gate.

### Next Gate
Approval of the rewritten sequence, and of any spend above 0.50 dollars.

<!-- context-entry:end -->

<!-- context-entry:start -->
## CTX-000016 | handoff

- Timestamp: 2026-09-06T02:53:25Z
- Lifecycle: implement
- Session: SES-20260906T002521Z-claude-code-71f63778
- Harness: claude-code
- Supersedes: none

### Recipient
The next Claude Code session working on OpenMontage and the Spacesuit Bridge production.

### Objective
Rewrite the shot sequence around the now-locked story and bridge, take it to the proposal gate, and on approval generate a cheap likeness draft before any full-resolution spend.

### Current State
- The cinematic pipeline is genuinely running. research is completed and proposal sits at awaiting_human with a real gate. Artifacts on disk and schema-valid: research_brief, proposal_packet, decision_log with 17 entries, source_media_review.
- Story is LOCKED by the user: a last departure from Earth. He sits in the captain's chair, presses one control, goes to warp. Earth is behind him and he never looks back. Recorded as d-016.
- Bridge formation is LOCKED to F4, assets/images/F4-two-seat-cockpit-empty-copilot.jpg. The user generated it himself, outside the three the agent offered, and it beat all of them. Recorded as d-017.
- The work now lives in its own private repository, kraaft007/spacesuit-bridge, nested inside the fork's ignored projects/ directory. The fork does not see it and needs no gitignore change. Both repos push independently.
- Spend unchanged at 0.80 dollars of 10.00. Nothing was generated this session.

### Governing Artifacts
- projects/spacesuit-bridge/artifacts/decision_log.json - 17 decisions, read this first. d-016 story, d-017 formation, d-015 provider.
- projects/spacesuit-bridge/artifacts/research_brief.json - metadata.local_visual_references carries all ten stills with per-image defects
- AGENT_GUIDE.md - Rule Zero, mandatory preflight, project directory convention, checkpoint protocol
- pipeline_defs/cinematic.yaml - stage order and which stages gate
- om_ext/README.md - why local additions live outside the upstream tree and how the registry reaches them

### Constraints
- Rule Zero: everything goes through the pipeline. The empty Backlot filmstrip that started this whole thread was caused by calling a generation tool directly.
- single_action_approval_usd is 0.50. A 360p draft at 0.24 dollars falls under it; four 720p takes at 3.20 do not.
- Additions belong in om_ext, never in tools/ or skills/. Fixes to upstream files belong in a pull request, not carried locally.
- Every tool call needs an explicit output_path under projects/spacesuit-bridge/.

### Verification State
- Gemini Omni 1.1 is now reachable and is the default. gemini_omni_video defaults to gemini-omni-1.1-flash and plumbs response_format.resolution; gemini_omni_fal targets the v1.1 endpoints. Both were pinned to the superseded preview model before.
- Five wrong in-repo price constants have now been found across sessions: kling_video under-reports 3.5x, minimax_video over-reports, gemini_omni_fal was a flat 0.13 per second against real tiers of 0.03, 0.10, 0.15 and 0.30, and gemini_omni_video was a flat 0.10 correct only at 720p. Do not trust estimate_cost without checking the provider's published page.
- All four fal operations were diffed against fal's live OpenAPI documents with no network write: exact key match, no unknown fields, correct URLs. This caught a latent 422 — the edit endpoint accepts neither aspect_ratio nor duration.
- The direct Google route has NO equivalent verification available. Google publishes no OpenAPI document for the Interactions API, so its request shape rests on documentation plus unit tests. The 0.24 dollar draft is the cheapest real proof.
- Suites: 1850 passed on the fork's main, 1828 and 1845 on the two pull request branches. Zero failures.
- Two pull requests are open against calesthio/OpenMontage and are the entire conflict surface: 633 for the Omni fixes, seven files, and 634 for the Backlot References panel, three files.

### Unresolved Items
- ONE QUESTION BLOCKS THE SHOT LIST and only the user can answer it: does he acknowledge the gloves on the empty copilot seat? Ignoring them makes it a film about a man who finished grieving long ago. Touching them, or looking and then turning forward, makes it about the moment he decides to go anyway. It decides whether the sequence needs a close-up.
- The four concept options in proposal_packet are STALE. Every one predates the locked story and none knows about F4 or the empty seat. Do not present them again; rewrite the sequence.
- Target duration, delivery aspect ratio and platform are still unset. Vertical 9:16 would change the framing of every shot and must be decided before generation, not in post.
- The United States flag patch recurs in every generation including F4, and the user is Canadian. It rides into the regeneration prompt rather than needing a separate edit.
- shot01-bridge-reveal.mp4 is superseded. He stands holding a helmet and faces camera in it; the locked staging is seated and forward-facing.
- gemini_omni_video.quality_score stays 0.85. Raising it needs a fleet ranking comparison that has not been run; the reasoning is in a comment.

### First Action
Ask the user the gloves question. Then rewrite the sequence for F4 and the locked story, replace the stale concept options in proposal_packet, and present it at the gate. Generate nothing before approval.

### Next Gate
User approval of the rewritten sequence, the delivery shape, and any spend above 0.50 dollars.

<!-- context-entry:end -->

<!-- context-entry:start -->
## CTX-000017 | session-start

- Timestamp: 2026-09-06T20:37:35Z
- Lifecycle: implement
- Session: SES-20260906T203735Z-claude-code-f4587d37
- Harness: claude-code
- Supersedes: none

### Objective
Ask the user the gloves question, then rewrite the F4 cockpit shot sequence around the locked story and locked bridge, replace the stale concept options in proposal_packet, and present the result at the proposal gate without generating anything.

### Previous State
- CTX-000016 handoff closed the prior session with proposal at awaiting_human and research completed.
- Story locked as d-016: a last departure from Earth, seated in the captain's chair, one control, warp, never looks back.
- Bridge locked as d-017 to the user-generated F4 two-seat cockpit with an empty copilot seat and gloves left on it.
- Spend unchanged at 0.80 dollars of a 10.00 dollar budget. Nothing was generated in the prior session.

### Governing Artifacts
- projects/spacesuit-bridge/artifacts/decision_log.json - 17 decisions; read d-016, d-017, d-015 first; append-only with supersedes.
- projects/spacesuit-bridge/artifacts/proposal_packet.json - holds the stale concept options that must be replaced.
- projects/spacesuit-bridge/artifacts/research_brief.json - metadata.local_visual_references carries the ten stills with per-image defects.
- pipeline_defs/cinematic.yaml - stage order and which stages gate.
- skills/pipelines/cinematic/proposal-director.md - the director skill that owns the current stage.
- AGENT_GUIDE.md - Rule Zero, mandatory preflight, project directory convention, checkpoint protocol.

### Working Set
- projects/spacesuit-bridge/artifacts/proposal_packet.json
- projects/spacesuit-bridge/artifacts/decision_log.json
- projects/spacesuit-bridge/checkpoint_proposal.json
- projects/spacesuit-bridge/assets/images/F4-two-seat-cockpit-empty-copilot.jpg

### Retrieve When Needed
- skills/meta/checkpoint-protocol.md and skills/meta/reviewer.md for the gate and self-review rules.
- schemas/artifacts/proposal_packet.schema.json before writing the rewritten packet.
- om_ext/README.md only if a local tool addition becomes necessary.
- Earlier Context.md entries CTX-000001 through CTX-000015 for decision provenance.

### Open Items
- The gloves question is unanswered and blocks the shot list; only the user can answer it.
- Target duration, delivery aspect ratio and platform are still unset and change the framing of every shot.
- Provider confirmation for the direct Google route recommended in d-015 is not yet user-approved.
- The four concept options in proposal_packet predate the locked story and must not be re-presented.
- The United States flag patch recurs in every generation and the user is Canadian; it rides into the regeneration prompt.
- No paid generation has been approved; the 0.24 dollar 360p draft sits under the 0.50 dollar single-action threshold.

### Next Action
Ask the user the gloves question inline and wait for the answer before writing any shot.

### Next Gate
User approval of the rewritten sequence, the delivery shape, and any spend above 0.50 dollars.

<!-- context-entry:end -->

<!-- context-entry:start -->
## CTX-000018 | checkpoint

- Timestamp: 2026-09-07T20:47:42Z
- Lifecycle: implement
- Session: SES-20260906T203735Z-claude-code-f4587d37
- Harness: claude-code
- Supersedes: none

### Current Objective
Sync the externally produced Runway cut into OpenMontage as hero source footage and re-open the proposal gate against the film that now exists.

### Decisions Since Previous Boundary
- User answered the role question: the Runway cut is hero source footage, not the deliverable and not an animatic. Recorded as d-019.
- User stated the clip's background audio must carry through to the master. This is now recorded in source_media_review, in the d-019 reason, and as an explicit compose-stage constraint in proposal_packet.
- Provider route changed from Gemini Omni direct to Runway offline on the user's subscription. Recorded as d-018, superseding d-015 on the same subject.
- The four prior concept options A-D were removed rather than edited, because all predate d-016, d-017 and the hero clip.
- Three upstream defects in lib/source_media_review.py were fixed on a branch and sent as a pull request rather than carried as local edits, per the project rule that fixes to upstream files belong in a PR.

### Changed Artifacts
- projects/spacesuit-bridge/assets/video/spacesuit-bridge-runway-cut-12s.mp4 - new; 12.0s, 1280x720, 24fps, h264, AAC stereo 48kHz; sha256 verified identical to the Downloads original.
- projects/spacesuit-bridge/artifacts/source_media_review.json - regenerated over all 21 media files; the prior claim of image-only source is gone; audio bed and the 1280x720 ceiling now recorded.
- projects/spacesuit-bridge/artifacts/proposal_packet.json - concept options replaced with S1, S2, S3; delivery promise switched to source_led; estimate falls from 3.44 dollars to 0.00.
- projects/spacesuit-bridge/decision_log.json - d-018 and d-019 appended; 19 decisions total.
- projects/spacesuit-bridge/checkpoint_proposal.json - rewritten at awaiting_human, now carrying source_media_review as a stage input; prior checkpoint archived to history/.
- lib/source_media_review.py and tests/lib/test_source_media_review_video_probe.py - on branch fix/source-media-review-video-probe, merged locally to main, sent as calesthio/OpenMontage pull request 641.

### Verification State
- Three defects confirmed by reading source and by execution, not inferred. frame_sampler was called without its required strategy input, raising KeyError into a swallowing except. Its result was read as frame_paths when the tool returns frames. audio_probe's audio-shaped dict was assigned to technical_probe wholesale, leaving no resolution or fps and making the ffprobe fallback unreachable.
- Net effect measured: a 1280x720 clip with a real AAC track was reported as 12.0s at unknown, without audio, with zero frames sampled, while asserting reviewed true. No video had ever been frame-sampled by this function.
- After the fix the same call reports 1280x720, 24fps, h264, aac, 48000Hz, 2 channels, four frames on disk, and adds source audio to usable_for.
- The three new tests fail against the unfixed library and pass against the fixed one; verified by stashing the fix and re-running.
- Full suite: 1853 passed, 12 skipped, 3 xfailed, zero failures. Baseline on main was 1850 plus the 3 new tests.
- Proposal checkpoint re-read and validated through lib.checkpoint.validate_checkpoint: status awaiting_human, human_approved false, three artifacts attached, 21 files in the review.
- Whisper found zero speech segments in both the hero cut and shot01, so the audio bed is ambience and score rather than dialogue.
- Both repositories committed and pushed. kraaft007/spacesuit-bridge at a74afb1, working tree clean and in sync with origin.

### Unresolved Items
- The proposal gate is open and unapproved. S2 is recommended but not chosen; picking S2 or S3 requires explicitly superseding d-016's register from refusal to farewell.
- The to-camera look at roughly 3.0s and 6.9s in the hero clip contradicts d-016's never looks back. This is the substance of the S1 versus S2 choice.
- The gloves question is still formally unanswered. The hero clip does not clearly resolve it: at 7.8s his hand reaches past the empty seat toward the console and his gaze drops, but stills cannot tell whether it lands on the gloves or the control.
- Target duration and delivery aspect ratio remain unset. A 16:9 frame is not classified as a Short, so phone distribution would change the framing of every remaining decision.
- render_runtime is still locked to remotion from the previous gate, but the production is now source-led, which makes ffmpeg a live option again. It needs re-confirming rather than carrying over.
- Whether further inserts go through Runway on the subscription at 0.00 dollars or in-pipeline at 0.80 dollars is open. The in-pipeline route is the only one that yields a seed and reproducible provenance.
- The hero clip has no recoverable seed, model version or prompt. It can be re-edited but never regenerated.
- Pull request 641 is open against calesthio/OpenMontage and is now the third open PR alongside 633 and 634.

### Next Action
Wait for the user to choose S1, S2 or S3 at the proposal gate, along with duration, aspect ratio and the render_runtime re-confirmation. Generate nothing before that.

### Next Gate
User approval of the rewritten proposal packet: concept choice, delivery shape, render runtime, and the insert route.

<!-- context-entry:end -->
