"""One-shot: build film 5, Lucky Days and Unlucky Days (regression to the mean)."""
import json
import re
import subprocess
import sys
from pathlib import Path

import jsonschema

from tools.tool_registry import registry

SLUG = "diana-regression"
PROJ = Path("projects") / SLUG
(PROJ / "artifacts").mkdir(parents=True, exist_ok=True)


def validate(obj, name):
    schema = json.load(open(f"schemas/artifacts/{name}.schema.json", encoding="utf-8"))
    jsonschema.validate(obj, schema)
    json.dump(obj, open(PROJ / f"artifacts/{name}.json", "w", encoding="utf-8"), indent=2)
    print(f"{name} SCHEMA-VALID", flush=True)


research = {
    "version": "1.0",
    "topic": "Regression to the mean from Thinking, Fast and Slow, told for an 8-year-old as why her best day is usually followed by a worse one",
    "research_date": "2026-09-09",
    "research_summary": (
        "Film 5 of the series. Chapter 17. Whenever two measures correlate imperfectly, extreme scores are "
        "followed by less extreme ones. Kahneman is explicit that this is a mathematical necessity with an "
        "explanation but no cause, and that the mind reliably invents a causal story for it. His flight "
        "instructor example is load-bearing: praise appears not to work and criticism appears to work, purely "
        "because praise follows unusually good performance and criticism follows unusually bad performance, and "
        "both are followed by regression. Translated to a spelling test this is the most useful idea in the book "
        "for a parent as well as the child, because it exposes unfairness children feel keenly and adults "
        "administer unknowingly."
    ),
    "landscape": {
        "existing_content": [
            {"title": "Jane the Brain (NIMH)", "url": "https://www.nimh.nih.gov/get-involved/science-education/video-series-jane-the-brain",
             "source": "government site", "angle": "Coping with big feelings",
             "what_it_covers": "Disappointment as a feeling, never as a statistical artefact"},
            {"title": "General children's growth-mindset material", "url": "https://www.scholastic.com/parents/family-life/social-emotional-learning/development-milestones/emotional-lives-8-10-year-olds.html",
             "source": "web", "angle": "Effort explains outcomes",
             "what_it_covers": "Teaches that effort drives results, which makes an ordinary dip feel like personal failure"},
            {"title": "The Decision Lab - System 1 and System 2", "url": "https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking",
             "source": "reference site", "angle": "Adult reference explainer",
             "what_it_covers": "Regression described through sports and business performance"}
        ],
        "saturated_angles": ["Effort and growth mindset as the explanation for every change in performance",
                             "Adult sports and stock-market regression examples"],
        "underserved_gaps": [
            "Telling a child that a dip after a peak is expected and uncaused",
            "The praise-and-punishment illusion, which affects how adults treat her",
            "Separating a result into steady skill plus bouncing luck, which a child can picture"
        ]
    },
    "data_points": [
        {"claim": "Whenever two measures correlate imperfectly, extreme scores are followed by less extreme ones. This is a mathematical necessity, not a causal event.",
         "source_url": "https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking",
         "source_name": "Thinking, Fast and Slow, Ch 17", "credibility": "secondary_source",
         "surprise_factor": "counterintuitive", "usable_as": "core concept spine"},
        {"claim": "The mind reliably invents a causal story for regression, because it has an explanation but no cause.",
         "source_url": "https://www.sparknotes.com/lit/thinking-fast-and-slow/section1/",
         "source_name": "Thinking, Fast and Slow, Ch 17", "credibility": "secondary_source",
         "surprise_factor": "counterintuitive", "usable_as": "why the dip feels like her fault"},
        {"claim": "Praise appears ineffective and criticism appears effective purely because each follows an extreme result that regresses regardless.",
         "source_url": "https://www.sparknotes.com/lit/thinking-fast-and-slow/section1/",
         "source_name": "Thinking, Fast and Slow, Ch 17, flight instructor example",
         "credibility": "secondary_source", "surprise_factor": "surprising",
         "usable_as": "the turn, and the part that matters to her father too"},
        {"claim": "By age 8 to 9 children regulate emotion through explicit thoughts about it, so a wait-and-look-at-three instruction is usable.",
         "source_url": "https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/bjep.12305",
         "source_name": "Pennequin et al., British Journal of Educational Psychology (2020)",
         "credibility": "primary_source", "surprise_factor": "expected",
         "usable_as": "justifies the ending instruction"}
    ],
    "audience_insights": {
        "knowledge_level": "Age 8. Has seen films 1 to 4 and owns fast one, story machine, memory shelf and separate boxes.",
        "common_questions": [
            "Why did I do worse this week when I tried just as hard?",
            "Did I get worse at it?",
            "Why does getting told off seem to work?"
        ],
        "misconceptions": [
            {"myth": "If my score went down, something went wrong",
             "reality": "After an unusually high score a lower one is expected, and nothing caused it.", "source": "Ch 17"},
            {"myth": "How well I do is all about how good I am",
             "reality": "It is steady skill plus bouncing luck, and only the luck part moves much week to week.", "source": "Ch 17"},
            {"myth": "Being told off works and being praised does not",
             "reality": "Both are followed by a move back toward the middle that would have happened anyway.", "source": "Ch 17"}
        ],
        "pain_points": [
            "Feeling she has gone backwards after a normal fluctuation",
            "Being treated as though an ordinary dip were a failure of effort"
        ]
    },
    "angles_discovered": [
        {"name": "The Bounce", "type": "narrative",
         "hook": "Nineteen out of twenty one week. Fifteen the next. And it felt like going backwards.",
         "why_now": "A weekly experience at this age, and a bouncing dot around a steady line makes an abstract statistical fact concrete.",
         "grounded_in": ["Ch 17 regression to the mean"]},
        {"name": "Two Things Stuck Together", "type": "evergreen",
         "hook": "How well you did is how good you are, plus how lucky you were that day.",
         "why_now": "Separating the steady part from the bouncing part is the whole explanation and a child can hold it.",
         "grounded_in": ["Ch 17, imperfect correlation"]},
        {"name": "Why Telling Off Seems To Work", "type": "contrarian",
         "hook": "Praise looks useless and telling off looks brilliant. Neither did anything.",
         "why_now": "Kahneman's own flight instructor finding, and the half that changes how the adults around her behave.",
         "grounded_in": ["Ch 17, the reward and punishment illusion"]}
    ],
    "expert_voices": [
        {"name": "Daniel Kahneman", "title_or_affiliation": "Nobel laureate, author",
         "position": "Regression to the mean has an explanation but no cause, and the illusion that punishment works and praise does not follows directly from it.",
         "source_url": "https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking",
         "contrarian": False}
    ],
    "sources": [
        {"url": "https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking",
         "title": "System 1 and System 2 Thinking - The Decision Lab", "used_for": "Regression definition", "reliability": "secondary"},
        {"url": "https://www.sparknotes.com/lit/thinking-fast-and-slow/section1/",
         "title": "Thinking, Fast and Slow Summary", "used_for": "Chapter 17 and the flight instructor example", "reliability": "secondary"},
        {"url": "https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/bjep.12305",
         "title": "Metacognition and emotional regulation in children 8 to 12", "used_for": "Age appropriateness", "reliability": "primary"},
        {"url": "https://www.nimh.nih.gov/get-involved/science-education/video-series-jane-the-brain",
         "title": "Jane the Brain - NIMH", "used_for": "Format benchmark", "reliability": "primary"},
        {"url": "https://www.scholastic.com/parents/family-life/social-emotional-learning/development-milestones/emotional-lives-8-10-year-olds.html",
         "title": "Social and Emotional Lives of 8- to 10-Year-Olds", "used_for": "Achievement pressure at this age", "reliability": "secondary"}
    ],
    "metadata": {
        "series": "Film 5 of 18.",
        "excluded_claims": [
            "Correlation coefficients and any numerical treatment of regression.",
            "Sports and stock-market examples, the standard adult framing.",
            "Anything from the priming or ego-depletion chapters."
        ],
        "note_for_the_parent": "The praise-and-punishment section is aimed as much at the adult watching as at the child."
    }
}
validate(research, "research_brief")

proposal = {
    "version": "1.0",
    "concept_options": [
        {"id": "c1", "title": "Lucky Days and Unlucky Days",
         "hook": "Diana got nineteen out of twenty. Her best ever. The next week she got fifteen, and it felt like going backwards.",
         "narrative_structure": "story",
         "visual_approach": "The established storybook world. New device: a steady soft grey line across the cream page for how good she actually is, and a warm gold dot that bounces above and below it, landing far above once and then settling back near the line.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old, watched with her dad",
         "target_platform": "generic", "target_duration_seconds": 185,
         "key_points": ["A result is steady skill plus bouncing luck",
                        "Only the luck part moves much from week to week",
                        "After an unusually high day, a lower one is expected and uncaused",
                        "Praise looks useless and telling off looks brilliant, and neither did anything",
                        "The move: look at three, not one"],
         "core_message": "Your best day was good and lucky at the same time. The luck does not come twice, so the next day drops, and nobody caused it.",
         "cta": "When something goes brilliantly or terribly, wait and look at three of them before deciding anything.",
         "tone": "Warm, matter of fact, quietly liberating.",
         "why_this_works": "It answers a weekly experience, removes blame from an event she reads as personal failure, and its second half changes how the adults around her behave.",
         "grounded_in": ["Ch 17 regression to the mean", "Ch 17 flight instructor"]},
        {"id": "c2", "title": "Two Things Stuck Together",
         "hook": "How well you did is two things added up, and only one of them is you.",
         "narrative_structure": "analogy",
         "visual_approach": "Two jars poured into one glass, a steady one and a wobbly one.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 140,
         "key_points": ["Skill is steady", "Luck bounces", "Results mix both"],
         "core_message": "Separate the steady part from the bouncing part.", "cta": "Ask which part moved.",
         "tone": "Curious", "why_this_works": "Cleanest explanation but no emotional payoff alone, so it becomes the second act of c1.",
         "grounded_in": ["Ch 17 imperfect correlation"]},
        {"id": "c3", "title": "Why Telling Off Seems To Work",
         "hook": "Praise looks useless. Telling off looks brilliant. Neither of them did anything.",
         "narrative_structure": "myth_busting",
         "visual_approach": "The same bouncing dot, with a reaction after each extreme.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old and her father",
         "target_platform": "generic", "target_duration_seconds": 130,
         "key_points": ["Praise follows peaks", "Criticism follows troughs", "Both are followed by regression"],
         "core_message": "The feedback did not cause the change.", "cta": "Do not judge a response by what happened next.",
         "tone": "Wry", "why_this_works": "The most consequential half, but it needs the mechanism established first, so it becomes the third act of c1.",
         "grounded_in": ["Ch 17 reward and punishment illusion"]}
    ],
    "selected_concept": {
        "concept_id": "c1",
        "rationale": "c1 opens on a real spelling test, explains the mechanism in its middle and lands the praise-and-punishment illusion as its payoff. The other two are the same material without a story to carry it.",
        "modifications": ["All production decisions carry over from films 1 to 4",
                          "New device: the steady line and the bouncing dot",
                          "Every script section has at least one scene, with a build-time assertion, fixing what crashed film 4"]
    },
    "production_plan": {
        "pipeline": "animated-explainer", "playbook": "custom-atelier-storybook",
        "renderer_family": "explainer-teacher", "render_runtime": "remotion", "composition_mode": "atelier",
        "delivery_promise": {"promise_type": "teacher_explainer", "motion_required": False, "source_required": False,
                             "tone_mode": "intimate and matter of fact, a bedtime storybook read aloud",
                             "quality_floor": "presentable", "approved_fallback": "still_led"},
        "art_direction": "Unchanged series house style. New device: a steady soft grey horizontal line for how good she is, and a warm gold dot bouncing above and below it.",
        "taste_profile": {
            "design_read": "The same bedtime picture book, four chapters on",
            "visual_variance": 8, "motion_intensity": 3, "information_density": 2,
            "palette_discipline": "Unchanged. Cream ground, muted warm palette, gold and blue as the only accents.",
            "layout_variation": "Each scene composed for its beat. The line and dot give this film its geometry.",
            "reference_strategy": "Series continuity only.",
            "anti_patterns": ["charts, axes, gridlines or anything resembling a graph",
                              "asking the image model for exact counts or numerals",
                              "a clause pasted into prompts it does not belong to",
                              "implying the dip was her fault or that effort was missing"],
            "quality_gates": ["Contact sheet of all illustrations reviewed before render",
                              "Every script section has at least one scene, asserted at build time",
                              "The line-and-dot device never becomes a chart"]
        },
        "music_source": {"source_type": "ai_generated", "provider": "reused from film 1 (Google Lyria)",
                         "mood_direction": "The same bed as films 1 to 4.", "estimated_cost_usd": 0.0},
        "voice_selection": {"provider": "elevenlabs", "voice_id": "JBFqnCBsd6RMkjVDRZzb",
                            "rationale": "The same warm storyteller voice as films 1 to 4.",
                            "estimated_cost_usd": 0.85,
                            "delivery_style": "warm parent reading a bedtime story, matter of fact and unhurried",
                            "pacing_policy": "Roughly 110 words per minute with three genuine silences.",
                            "sample_approval_required": False},
        "stages": [
            {"stage": "script", "approach": "Around 400 words at an 8-year-old listening level, three pause beats.", "tools": []},
            {"stage": "scene_plan", "approach": "Eighteen scenes covering all fifteen sections, the bouncing dot carrying the middle.", "tools": []},
            {"stage": "assets", "approach": "Same image model and character lock, same voice, music reused.",
             "tools": [{"tool_name": "google_imagen", "role": "illustration", "available": True},
                       {"tool_name": "elevenlabs_tts", "role": "narration", "available": True}]},
            {"stage": "edit", "approach": "Timeline rebuilt from measured narration durations.", "tools": []},
            {"stage": "compose", "approach": "Atelier Remotion render reusing the series composition.",
             "tools": [{"tool_name": "video_compose", "role": "render", "available": True}]}
        ],
        "quality_tradeoffs": [
            {"tradeoff": "Including the praise-and-punishment illusion versus keeping the film about her only",
             "recommendation": "Include", "quality_impact": "It is the most consequential part of the chapter and is aimed at the adult watching. Omitting it would leave the unfairness in place."},
            {"tradeoff": "Using two real test scores versus staying wholly qualitative",
             "recommendation": "Two scores", "quality_impact": "Nineteen and fifteen make the drop concrete without requiring any statistics."}
        ],
        "alternative_paths": [
            {"description": "Mechanism only, no praise-and-punishment section", "total_cost_usd": 1.57, "quality_level": "standard"},
            {"description": "Reuse everything from films 1 to 4", "total_cost_usd": 1.57, "quality_level": "standard"}
        ]
    },
    "cost_estimate": {
        "total_estimated_usd": 1.57, "budget_cap_usd": 2.5, "budget_verdict": "within_budget",
        "line_items": [
            {"tool": "google_imagen", "operation": "storybook illustrations", "quantity": 18, "estimated_usd": 0.72, "notes": "0.04 USD each"},
            {"tool": "elevenlabs_tts", "operation": "narration", "quantity": 1, "estimated_usd": 0.85, "notes": "Zero if Daniel records it"},
            {"tool": "video_compose", "operation": "local render", "quantity": 1, "estimated_usd": 0.0, "notes": "No API cost"}
        ],
        "savings_options": ["Daniel records the narration", "Music already reused at no cost"]
    },
    "approval": {"status": "approved", "approved_budget_usd": 2.5,
                 "user_notes": "User replied NEXT, selecting film 5, under a standing instruction to fix defects without asking."},
    "metadata": {"series_position": "5 of 18",
                 "carried_over": ["character lock", "style lock", "voice", "runtime", "composition mode", "music bed"],
                 "new_this_film": ["steady line and bouncing dot device"],
                 "lesson_applied_from_film_4": "Scene coverage of every script section is asserted before generation, and the timeline builder still carries the previous scene across any uncovered section as a safety net."}
}
validate(proposal, "proposal_packet")

S = [
    ("s1", "The best ever",
     "Diana got nineteen out of twenty in her spelling test. Her best ever.",
     'Diana got nineteen out of twenty in her spelling test. <break time="0.5s"/> Her best ever.',
     1.2, "measured", "bright", ["best"], "Genuinely pleased. No irony yet."),
    ("s2", "The next week",
     "The next week she got fifteen. And it felt like falling off a cliff.",
     'The next week she got fifteen. <break time="0.5s"/> And it felt like falling off a cliff.',
     1.2, "slow", "tender", ["fifteen"], "Kind. The feeling is real even though the story is wrong."),
    ("s3", "Nothing went wrong",
     "But nothing went wrong. Nothing at all. Not one single thing.",
     'But nothing went wrong. <break time="0.5s"/> Nothing at all. <break time="0.4s"/> Not one single thing. <break time="2.5s"/>',
     2.5, "slow", "steady", ["nothing"], "Pause beat one. Let the claim sit before explaining it."),
    ("s4", "Two things stuck together",
     "Here is the thing about how well you do at anything. It is two things stuck together. How good you are, and how lucky you were that day.",
     'Here is the thing about how well you do at anything. <break time="0.5s"/> It is two things stuck together. <break time="0.5s"/> How good you are, <break time="0.4s"/> and how lucky you were that day.',
     1.4, "measured", "curious", ["two"], "The explanation begins. Clear and unhurried."),
    ("s5", "Only one of them moves",
     "How good you are barely changes from one week to the next. But luck bounces around like anything.",
     'How good you are barely changes from one week to the next. <break time="0.5s"/> But luck bounces around like anything.',
     1.2, "measured", "curious", ["bounces"], "Contrast the two clearly."),
    ("s6", "What luck is",
     "Which words came up. Whether you slept. Whether the person next to you was sniffing.",
     'Which words came up. <break time="0.3s"/> Whether you slept. <break time="0.3s"/> Whether the person next to you was sniffing.',
     1.2, "conversational", "wry", ["sniffing"], "Light. The sniffing should get a small smile."),
    ("s7", "Good and lucky",
     "So on your very best day, you were good and lucky. Both at the same time.",
     'So on your very best day, <break time="0.4s"/> you were good <break time="0.3s"/> and lucky. <break time="0.4s"/> Both at the same time.',
     1.4, "slow", "gentle", ["both"], "The hinge. Slow right down."),
    ("s8", "Luck does not repeat",
     "And luck does not do the same thing twice. The next week the luck just goes back to ordinary.",
     'And luck does not do the same thing twice. <break time="0.5s"/> The next week the luck just goes back to ordinary.',
     1.2, "measured", "steady", ["ordinary"], "Plain and calm."),
    ("s9", "So the score comes down",
     "So the score comes down. Not because you got worse. Because the lucky part went home.",
     'So the score comes down. <break time="0.5s"/> Not because you got worse. <break time="0.4s"/> Because the lucky part went home.',
     1.4, "slow", "tender", ["worse"], "The absolution. Warmest line so far."),
    ("s10", "It works both ways",
     "It works the other way round too. After your worst day ever, the next one is almost always better. And you did not fix anything either.",
     'It works the other way round too. <break time="0.5s"/> After your worst day ever, the next one is almost always better. <break time="0.5s"/> And you did not fix anything either.',
     1.4, "measured", "steady", ["better"], "Symmetry. Same calm tone."),
    ("s11", "Now the grown-up part",
     "Now here is the part that catches out grown-ups.",
     'Now here is the part that catches out grown-ups. <break time="2.5s"/>',
     2.5, "measured", "conspiratorial", ["grown-ups"], "Pause beat two. She should feel let in on something."),
    ("s12", "Praise looks useless",
     "Imagine somebody praises you after your best day ever. Next week you do a bit worse. So it looks like praising you did not work.",
     'Imagine somebody praises you after your best day ever. <break time="0.4s"/> Next week you do a bit worse. <break time="0.5s"/> So it looks like praising you did not work.',
     1.2, "measured", "wry", ["praises"], "Dry, not bitter."),
    ("s13", "Telling off looks brilliant",
     "And imagine somebody tells you off after your worst day ever. Next week you do a bit better. So it looks like telling you off worked beautifully.",
     'And imagine somebody tells you off after your worst day ever. <break time="0.4s"/> Next week you do a bit better. <break time="0.5s"/> So it looks like telling you off worked beautifully.',
     1.4, "measured", "wry", ["worked"], "Let beautifully land with a little edge."),
    ("s14", "Neither did anything",
     "Neither of them did anything at all. That was just the bouncing.",
     'Neither of them did anything at all. <break time="0.5s"/> That was just the bouncing.',
     1.4, "slow", "steady", ["neither"], "Firm and clean. This is the point of the whole film."),
    ("s15", "The tool and landing",
     "So here is your fifth trick. When something goes brilliantly, or terribly, wait. Look at three of them, not one. Because one day is never the answer. You are somewhere in the middle, and the middle is where you will usually land.",
     'So here is your fifth trick. <break time="0.5s"/> When something goes brilliantly, or terribly, <break time="0.4s"/> wait. <break time="0.6s"/> Look at three of them, not one. <break time="2.5s"/> Because one day is never the answer. <break time="0.5s"/> You are somewhere in the middle, <break time="0.4s"/> and the middle is where you will usually land.',
     0.0, "measured", "encouraging", ["three", "middle"], "Pause beat three sits inside this section. End warm, then stop."),
]

sections, t = [], 0.0
for sid, label, text, prov, pause, pace, energy, emph, note in S:
    dur = round(len(text.split()) / 110 * 60 + pause, 2)
    sections.append({
        "id": sid, "label": label, "text": text,
        "start_seconds": round(t, 2), "end_seconds": round(t + dur, 2),
        "speaker_directions": note,
        "delivery_cues": {"pace": pace, "energy": energy, "emphasis_words": emph,
                          "pause_after_seconds": pause, "delivery_note": note, "provider_text": prov},
        "enhancement_cues": [], "pronunciation_guides": []
    })
    t += dur

script = {
    "version": "1.0", "title": "Lucky Days and Unlucky Days",
    "total_duration_seconds": round(t, 2),
    "voice_performance": {
        "performance_intent": "The same parent and child, four chapters on. Quietly liberating rather than tender: the narrator is removing blame, not offering comfort.",
        "pacing_profile": "contemplative",
        "energy_curve": "Bright at the good score. Gentle at the drop. Clear through the middle. Conspiratorial at the grown-up section. Firm at neither of them did anything. Warm at the close.",
        "pause_policy": "Three genuine silences: after nothing went wrong, after being let in on the grown-up part, and after being told to look at three.",
        "sample_section_id": "s9",
        "provider_notes": {
            "all": "Roughly 110 words per minute. Section s9 is the absolution and the sample section.",
            "elevenlabs": "Same voice as films 1 to 4, George. Stability 0.75, similarity 0.9, style 0.15, speed 0.9.",
            "human_recording": "Sections 12 and 13 are aimed at the adult in the room as much as the child. Dry, never bitter."
        }
    },
    "sections": sections,
    "metadata": {
        "series_position": "5 of 18",
        "word_count_approx": sum(len(s["text"].split()) for s in sections),
        "target_wpm": 110,
        "reading_age": "Written for a listener of 8. Regression, correlation and mean never appear.",
        "pause_beats": [
            {"section": "s3", "purpose": "She sits with the claim that nothing went wrong"},
            {"section": "s11", "purpose": "She is let in on something about adults"},
            {"section": "s15", "purpose": "She considers looking at three instead of one"}
        ],
        "grounded_in": {
            "s1_to_s3": "Ch 17, an extreme score followed by a less extreme one",
            "s4_to_s9": "Ch 17, imperfect correlation as steady skill plus bouncing luck",
            "s10": "Ch 17, regression operating symmetrically from a trough",
            "s11_to_s14": "Ch 17, the flight instructor and the reward and punishment illusion",
            "s15": "Ch 17 corrective, plus Pennequin on age-appropriate instructions"
        },
        "accuracy_guardrails_applied": [
            "Regression is described as having an explanation but no cause, which is Kahneman's own formulation.",
            "No correlation coefficients or numerical treatment.",
            "The film never suggests effort does not matter, only that one result is mostly noise.",
            "No priming or ego-depletion material."
        ]
    }
}
validate(script, "script")

spec = [
    ("sc1", "s1", "DIANA", "The girl holds up a spelling test sheet with a bright happy smile, standing in a warm classroom."),
    ("sc2", "s1", "NONE", "A single warm-gold dot sits high above a soft steady grey horizontal line drawn across cream paper. Nothing else at all."),
    ("sc3", "s2", "DIANA", "The girl looks down at a test sheet with a small crumpled disappointed expression, her shoulders dropped."),
    ("sc4", "s3", "NONE", "A soft grey horizontal line across cream paper, entirely calm and undisturbed, with a warm-gold dot resting quietly just above it."),
    ("sc5", "s4", "NONE", "Two simple hand-drawn wooden blocks stacked on cream paper. The lower block is broad, plain and solid. The upper block is small, tilted and wobbly."),
    ("sc6", "s4", "DIANA", "The girl looks thoughtfully at two stacked wooden blocks, one solid and one wobbly, her head tilted."),
    ("sc7", "s5", "NONE", "On the left of a cream page a broad solid grey block sits perfectly still. On the right a small gold shape is caught mid-bounce with soft motion arcs around it."),
    ("sc8", "s6", "NONE", "Three small ordinary objects float on cream paper: a small word card, a pillow, and a paper tissue. Nothing else."),
    ("sc9", "s7", "NONE", "A single bright warm-gold dot sits very high above a soft steady grey line, glowing, near the top of the cream page."),
    ("sc10", "s8", "NONE", "The same gold dot now sits close to the soft grey line, ordinary and unremarkable, with a faint dotted trail showing where it fell from."),
    ("sc11", "s8", "DIANA", "The girl watches a small gold dot drift gently downward toward a soft grey line, calm and unbothered."),
    ("sc12", "s9", "DIANA", "The girl stands calmly with a small relieved half-smile, hands loose at her sides."),
    ("sc13", "s10", "NONE", "A warm-gold dot sits very low beneath a soft grey line, with a faint dotted trail showing it rising gently back up toward the line."),
    ("sc14", "s11", "DIANA", "The girl leans in slightly with a small conspiratorial smile, as if being told a secret."),
    ("sc15", "s12", "NONE", "A gold dot high above a grey line with a small warm burst of sparkles beside it, and a faint dotted trail already curving downward."),
    ("sc16", "s13", "NONE", "A gold dot low beneath a grey line with a small grey cloud beside it, and a faint dotted trail already curving upward."),
    ("sc17", "s14", "NONE", "A long soft grey horizontal line across cream paper with many warm-gold dots scattered above and below it, clustering most closely around the middle of the line."),
    ("sc18", "s15", "DIANA", "The girl sits comfortably on a low wall in warm late afternoon light, holding a few loose paper sheets in her lap, entirely at ease."),
]

per = {}
for _, sid, _, _ in spec:
    per[sid] = per.get(sid, 0) + 1
missing = [s["id"] for s in sections if s["id"] not in per]
if missing:
    raise SystemExit(f"scene coverage gap for sections {missing}; fix spec before running")
print(f"scene coverage ok: all {len(sections)} sections mapped", flush=True)

sec_map = {s["id"]: s for s in sections}
scenes, seen = [], {}
for scid, sid, who, desc in spec:
    s = sec_map[sid]
    span = s["end_seconds"] - s["start_seconds"]
    n = per[sid]
    i = seen.get(sid, 0)
    seen[sid] = i + 1
    scenes.append({
        "id": scid, "type": "generated", "script_section_id": sid,
        "start_seconds": round(s["start_seconds"] + span * i / n, 3),
        "end_seconds": round(s["start_seconds"] + span * (i + 1) / n, 3),
        "description": desc,
        "narrative_role": "deliver_payload" if scid in ("sc9", "sc10", "sc17") else "evidence",
        "hero_moment": scid in ("sc9", "sc10", "sc17", "sc18"),
        "transition_in": "cut", "transition_out": "cut",
        "shot_language": {"shot_size": "wide" if scid == "sc17" else "medium",
                          "camera_movement": "static", "lighting_key": "natural",
                          "depth_of_field": "medium", "color_temperature": "warm"},
        "overlay_notes": "No text in the illustration."
    })

scene_plan = {
    "version": "1.0", "style_playbook": "custom-atelier-storybook", "scenes": scenes,
    "metadata": {
        "character_lock": "Diana: a girl of eight, Vietnamese-Australian, straight black shoulder-length hair with a soft fringe, warm light skin, dark almond eyes, round friendly face, mustard-yellow knitted jumper, denim pinafore dress, red canvas shoes. Identical to films 1 to 4.",
        "one_child_rule": "Every frame containing a person contains exactly one child. No frame in this film shows two children.",
        "device_lock": "A soft steady grey horizontal line is how good she is. A warm gold dot is one day's result. The line never gains axes, ticks, numbers or gridlines; it must never read as a chart.",
        "style_lock": "Unchanged from films 1 to 4.",
        "scene_count": len(scenes),
        "section_coverage": "All fifteen script sections have at least one scene, asserted before generation.",
        "generation_order": "All eighteen generated, then reviewed on one contact sheet before any render."
    }
}
validate(scene_plan, "scene_plan")

registry.discover()
img = registry._tools["google_imagen"]
tts = registry._tools["elevenlabs_tts"]

DIANA = ("The girl is eight years old, Vietnamese-Australian, with straight black shoulder-length hair and a soft "
         "fringe, warm light skin, dark almond-shaped eyes and a round friendly face. She wears a mustard-yellow "
         "knitted jumper, a denim pinafore dress and red canvas shoes.")
STYLE = ("Children's picture-book illustration, soft gouache painting, warm cream paper background with visible "
         "paper grain, soft pencil linework, rounded organic shapes, muted warm palette, flat 2D storybook art, "
         "not 3D, no text, no lettering, no words, no numbers, no digits.")
ONE = "EXACTLY ONE CHILD in the frame, a single child alone. Do not draw two children."
NOPE = "There are NO people and NO animals at all in this picture."
NOCHART = "This is a simple hand-drawn storybook picture, not a graph. No axes, no tick marks, no gridlines, no labels."

WHO = {scid: who for scid, _, who, _ in spec}
by_id = {s["id"]: s for s in scenes}

for d in (PROJ / "assets/images", PROJ / "assets/audio", PROJ / "assets/music"):
    d.mkdir(parents=True, exist_ok=True)

print("=== illustrations ===", flush=True)
img_fail = []
for n in range(1, 19):
    sid = f"sc{n}"
    dest = PROJ / "assets/images" / f"{sid}.png"
    if dest.exists() and dest.stat().st_size > 10000:
        print(f"[skip] {sid}", flush=True)
        continue
    parts = [STYLE]
    if WHO[sid] == "DIANA":
        parts += [ONE, DIANA]
    else:
        parts += [NOPE, NOCHART]
    parts.append(by_id[sid]["description"])
    ok, err = False, None
    for _ in (1, 2):
        try:
            r = img.execute({"prompt": " ".join(parts), "aspect_ratio": "16:9",
                             "model": "gemini-2.5-flash-image", "number_of_images": 1,
                             "output_path": str(dest)})
            ok, err = bool(r.success), r.error
            if ok:
                break
        except Exception as exc:  # noqa: BLE001
            err = f"{type(exc).__name__}: {exc}"
    size = dest.stat().st_size if dest.exists() else 0
    good = ok and size > 10000
    if not good:
        img_fail.append(sid)
    print(f"[{'ok ' if good else 'FAIL'}] {sid} bytes={size} {err or ''}", flush=True)

print("\n=== narration ===", flush=True)


def probe(p: Path) -> float:
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "csv=p=0", str(p)], capture_output=True, text=True, timeout=60)
        return round(float(out.stdout.strip()), 3)
    except Exception:
        return 0.0


results = {}
for s in sections:
    sid = s["id"]
    dest = PROJ / "assets/audio" / f"{sid}.mp3"
    ok, err = False, None
    for _ in (1, 2):
        try:
            r = tts.execute({"text": s["delivery_cues"]["provider_text"],
                             "voice_id": "JBFqnCBsd6RMkjVDRZzb", "model_id": "eleven_flash_v2_5",
                             "stability": 0.75, "similarity_boost": 0.9, "style": 0.15, "speed": 0.9,
                             "use_speaker_boost": True, "output_path": str(dest)})
            ok, err = bool(r.success), r.error
            if ok:
                break
        except Exception as exc:  # noqa: BLE001
            err = f"{type(exc).__name__}: {exc}"
    secs = probe(dest) if dest.exists() and dest.stat().st_size > 1000 else 0.0
    results[sid] = {"ok": ok and secs > 0, "path": str(dest), "seconds": secs, "error": err}
    print(f"[{'ok ' if results[sid]['ok'] else 'FAIL'}] {sid} {secs}s {err or ''}", flush=True)

total = round(sum(v["seconds"] for v in results.values()), 2)
aud_fail = [k for k, v in results.items() if not v["ok"]]
json.dump({"voice_id": "JBFqnCBsd6RMkjVDRZzb", "model_id": "eleven_flash_v2_5",
           "total_seconds": total, "sections": results},
          open(PROJ / "artifacts/narration_results.json", "w", encoding="utf-8"), indent=2)

FPS, LEAD_IN, GAP, TAIL = 30, 1.0, 1.6, 2.5
dur = {k: v["seconds"] for k, v in results.items()}
by_section = {}
for sc in scenes:
    by_section.setdefault(sc["script_section_id"], []).append(sc)

audio, spans, tt = [], {}, LEAD_IN
for i, sec in enumerate(sections):
    sid = sec["id"]
    d = dur[sid]
    audio.append({"id": sid, "src": f"audio/{sid}.mp3", "startSec": round(tt, 3), "durSec": d})
    end = tt + d + (GAP if i < len(sections) - 1 else TAIL)
    spans[sid] = (tt, end)
    tt = end
TOTAL = round(tt, 3)

pscenes = []
for i, sec in enumerate(sections):
    sid = sec["id"]
    start, end = spans[sid]
    if i == 0:
        start = 0.0
    grp = by_section.get(sid)
    if not grp:
        if pscenes:
            pscenes[-1]["durSec"] = round(pscenes[-1]["durSec"] + (end - start), 3)
        continue
    step = (end - start) / len(grp)
    for j, sc in enumerate(grp):
        pscenes.append({"id": sc["id"], "src": f"images/{sc['id']}.png",
                        "startSec": round(start + j * step, 3), "durSec": round(step, 3),
                        "heroMoment": bool(sc.get("hero_moment")),
                        "movement": sc["shot_language"]["camera_movement"]})

captions = []
for sec in sections:
    start, _ = spans[sec["id"]]
    d = dur[sec["id"]]
    phr = [p.strip() for p in re.split(r"(?<=[.?!])\s+", sec["text"]) if p.strip()]
    chars = sum(len(p) for p in phr) or 1
    acc = start
    for p in phr:
        share = d * (len(p) / chars)
        captions.append({"text": p, "startSec": round(acc, 3), "durSec": round(share, 3)})
        acc += share

last = pscenes[-1]
props = {"fps": FPS, "width": 1920, "height": 1080,
         "durationInFrames": int(round(TOTAL * FPS)), "totalSeconds": TOTAL,
         "music": {"src": "music/bed.wav", "volume": 0.16, "fadeOutStartSec": round(TOTAL - 26, 3)},
         "scenes": pscenes, "audio": audio, "captions": captions,
         "titles": [{"kind": "title", "text": "Lucky Days and Unlucky Days",
                     "startSec": round(last["startSec"] + 1.0, 3),
                     "durSec": round(max(2.0, last["durSec"] - 1.0), 3)}]}
(PROJ / "composition").mkdir(parents=True, exist_ok=True)
json.dump(props, open(PROJ / "composition/props.json", "w", encoding="utf-8"), indent=2)

print(f"\nDONE images_failed={img_fail} narration_failed={aud_fail}")
print(f"total {TOTAL}s ({int(TOTAL//60)}m {TOTAL%60:.1f}s) frames={props['durationInFrames']} scenes={len(pscenes)} captions={len(captions)}")
sys.exit(0 if not img_fail and not aud_fail else 1)
