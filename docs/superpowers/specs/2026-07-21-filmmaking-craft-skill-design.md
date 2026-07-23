# Design — `filmmaking-craft` Skill (+ Korean Reading Companion)

> Date: 2026-07-21
> Source material: `docs/forskills/ko/642627554-The-Basics-of-Filmmaking.ko.summary.md`
> (Blain Brown, *The Basics of Filmmaking*, Routledge 2020)
> Status: approved design, pending implementation plan

## Goal

Add one new Layer 2 creative skill that injects **classical dramatic film craft** into
OpenMontage's AI-generation pipeline, plus a Korean reading copy for the user. The skill
fills gaps that no existing skill covers: coverage/cutability discipline, Murch's editing
hierarchy, dramatic 3-act structure, continuity, and room-tone/audio translation.

The core value is **translation**: every physical-shoot rule is re-expressed as a concrete
AI-generation constraint the pipeline stages can act on. The skill is a curated translation,
not a copy of the source summary.

## Non-Goals (YAGNI)

- No director-skill cross-reference edits (wiring is deferred — "file only").
- No `reviewer.md` / `review_focus` injection.
- No pipeline manifest edits.
- No producing / crew / safety / slating / permitting / 1st-AD protocol content — physical-set
  logistics irrelevant to AI generation.
- No duplication of cinematography vocabulary (cross-reference `video-gen-prompting.md`) or
  finishing craft (cross-reference `cinematic.md`).

## Deliverables

| File | Language | Purpose | Registered in INDEX.md |
|---|---|---|---|
| `skills/creative/filmmaking-craft.md` | English | Canonical Layer 2 craft skill (integration-ready) | Yes — Creative Skills table |
| `docs/filmmaking-craft.ko.md` | Korean | User reading companion | No (doc, not a skill) |

Rationale for Korean doc location: `docs/` already hosts the user-facing
`movie_making_skills.md`. `docs/forskills/ko/` holds raw translation-pipeline output and is a
different concern, so it is left untouched.

## Architecture

The skill is a single Layer 2 creative skill in the same pattern as `storytelling.md`: a
cross-stage craft reference that directors read when the brief is narrative or cinematic. It
is **passive** (read when relevant), not an enforced gate. It organizes content by pipeline
stage so a director can jump to its slice.

### Layer placement

- Layer 2 (`skills/creative/`) — "how OpenMontage uses this craft."
- Cross-references (not duplicates) Layer 2 peers: `storytelling.md`, `video-editing.md`,
  `cinematic.md`, `sound-design.md`, and the cinematography vocabulary in
  `video-gen-prompting.md`.

## Skill Body Structure (English canonical file)

```
# Filmmaking Craft for OpenMontage — Classical Film Discipline, Translated to AI-Generated Video

> Source: Blain Brown, The Basics of Filmmaking (Routledge, 2020) — curated for the AI-gen pipeline.

## When to Use
  Any multi-shot narrative or cinematic brief — pipelines: cinematic, hybrid, animation
  (narrative), character-animation — plus any scene needing cuttability.

## How to Use This Skill (Stage Map)
  | Stage       | Read section                        |
  | script      | §1 Narrative Structure & Dialogue   |
  | scene_plan  | §2 Coverage & Continuity  (core)    |
  | edit        | §3 Editing Decisions (Murch)        |
  | assets      | §4 Audio Craft (translated)         |
  | review      | §5 Anti-Pattern Checklist           |

## What This Skill Is NOT (pruning scope)
  Excluded: producing, crew, safety, slating, permits, 1st-AD protocol — physical-set
  logistics, irrelevant to AI generation.
  Cross-reference only (do not duplicate): cinematography vocabulary (video-gen-prompting.md),
  finishing (cinematic.md).

## §1 Narrative Structure & Dialogue  (→ script)
  - 3-act structure: setup / Plot Point 1 / Midpoint / Plot Point 2 / emotionally satisfying
    ending (contrast with the explainer arc in storytelling.md).
  - Plot vs story (causality: "queen died, then king died" vs "...of grief").
  - Conflict: external (person/person, person/society, person/nature/machine) + internal.
  - Short-form efficiency: every scene essential.
  - Subtext; avoid "on-the-nose" dialogue.
  - Show-don't-tell exposition (map background info to visuals).
  - [Translation table: screenwriting rule → OpenMontage script artifact field]

## §2 Coverage & Continuity  (→ scene_plan)   ← CORE SECTION
  - Coverage = cuttability; the #1 way movies fail.
  - Master scene method + coverage set (master / over-the-shoulder / close-up / cutaway).
  - The Line (180° rule) and how to cross it (show camera move, cutaway, neutral angle).
  - 30° / 20% rule; two-lens-sizes rule (cutability between adjacent shots).
  - Shot types for coverage (cross-ref video-gen-prompting.md vocabulary).
  - Continuity types: wardrobe, screen direction, props, time.
  - Match cuts, jump-cut avoidance, establishing shots, ellipsis.
  - [Translation table — the killer feature]:
      "shoot coverage for every scene"
        → "scene_plan declares ≥3 angles per narrative scene: master + 2 coverage
           (OTS / CU / cutaway) so edit has cutability."
      "the Line / 180°"
        → "all shots of one scene share a screen-direction axis; flag any axis flip."
      "30° rule"
        → "adjacent generated shots differ ≥30° horizontally/vertically or by two lens
           sizes, else jump-cut risk — regenerate or reframe."

## §3 Editing Decisions  (→ edit)
  - Walter Murch's Rule of Six, in priority order:
      emotion > story > rhythm > eye-trace > 2D-place-on-screen > 3D-space.
  - Six-pass editorial process: logging → first assembly → rough cut → first cut → fine cut
    → final cut (mapped onto edit_decisions fields).
  - J-cut / L-cut (extends the basics in video-editing.md).
  - Hidden cuts, match cuts, cross-cutting, ellipsis; establishing geography (wide shot first).
  - [Decision framework: when two candidate cuts compete, Murch priority settles it.]

## §4 Audio Craft — Translated  (→ assets)
  - Rule #1 "get the mic close" → TTS is the dialogue; no boom-distance problem, but ensure a
    clean, isolated narration take.
  - Rule #2 "always record" → always generate an ambient bed.
  - Room tone (≥15 s per location) → one consistent ambient/room-tone track per location,
    reused across cuts.
  - ADR avoidance → get the TTS take right the first time; regeneration is the AI equivalent of
    expensive ADR.
  - Scratch track → rough TTS for timing before the final voice.
  - [Translation table]

## §5 Anti-Pattern Checklist — "Top Ten Ways to Screw Up Your Movie"  (→ review / self-eval)
  Each screw-up re-expressed as an AI-gen check:
  - "not enough coverage"      → "does scene_plan declare ≥3 angles per narrative scene?"
  - "no cutaways"              → "does each scene include at least one cutaway/reaction?"
  - "bad audio"                → "is there a consistent ambient bed per location?"
  - "no establishing shot"     → "does each scene open with geographic orientation?"
  - "we'll fix it in post"     → "is anything being deferred to edit that should be fixed at
                                  scene_plan / assets?"
  - "weak script"              → "does the script have conflict + causality, not just events?"
  (Coverage, audio, establishing, post-deferral, script — the subset that maps to AI gen.
   Physical-only items like "bad focus", "camera shake", "room tone not recorded on set" are
   pruned or translated.)

## Self-Evaluation Rubric  (1–5 scoring table, per skill-creator convention)

## Common Pitfalls  (bullet list)

## Sources & Cross-References
  - Blain Brown, *The Basics of Filmmaking* (source).
  - storytelling.md (narrative — complementary, explainer-focused).
  - video-editing.md (editing — complementary, talking-head-focused).
  - video-gen-prompting.md (cinematography vocabulary — cross-reference).
  - cinematic.md (finishing — complementary).
  - sound-design.md (audio mixing — complementary).
```

## Korean Reading Companion (`docs/filmmaking-craft.ko.md`)

Same structure as the English skill, written in Korean. Sourced from the already-Korean
`.ko.summary.md` plus the English skill's translation logic re-expressed in Korean. This is a
reading document, not a pipeline-loaded skill, so it is not registered in `INDEX.md` and does
not need the self-eval/pitfalls scaffolding (though it may keep them for completeness).

## Content Fidelity

Curated translation, not a copy of the summary:

1. Prune physical-set logistics (producing, crew, safety, slating, permits, AD protocol).
2. Keep craft principles.
3. Add the AI-generation translation for each principle.
4. Each section ends with: principle → AI constraint → checklist item.

## Validation (no code)

Per `skills/meta/skill-creator.md` validation checklist:

- [ ] Well-formed markdown with clear headers.
- [ ] All cross-referenced skills exist: `storytelling.md`, `video-editing.md`,
      `video-gen-prompting.md`, `cinematic.md`, `sound-design.md` (verified present).
- [ ] Process steps are numbered and actionable.
- [ ] Self-evaluation rubric present.
- [ ] Common pitfalls present.
- [ ] No orphan references.
- [ ] `INDEX.md` Creative Skills table row added for `filmmaking-craft.md`.

## INDEX.md Entry (to add)

Under **Creative Skills** table:

```
| Filmmaking Craft | `creative/filmmaking-craft.md` | Classical film craft translated to AI-gen: coverage/cutability, 180° line, Murch editing hierarchy, dramatic 3-act structure, continuity, room-tone audio | storytelling, video-editing, cinematic, sound-design |
```

## Open Questions

None blocking. Wiring (director-skill cross-references, optional `review_focus` adoption) is
deferred per the "file only" decision and can be a follow-up task.

## Out of Scope (follow-ups)

- Cross-reference this skill from `cinematic`, `animation`, `hybrid`, `character-animation`
  script / scene / edit director skills.
- Adopt the §5 anti-pattern list as `review_focus` items in narrative pipeline manifests.
- Possibly add a `coverage_planning` hint to scene-director skills.
