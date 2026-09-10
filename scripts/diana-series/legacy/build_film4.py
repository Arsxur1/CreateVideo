"""One-shot: build film 4, The Halo (halo effect)."""
import json
import re
import subprocess
import sys
from pathlib import Path

import jsonschema

from tools.tool_registry import registry

SLUG = "diana-halo"
PROJ = Path("projects") / SLUG
(PROJ / "artifacts").mkdir(parents=True, exist_ok=True)


def validate(obj, name):
    schema = json.load(open(f"schemas/artifacts/{name}.schema.json", encoding="utf-8"))
    jsonschema.validate(obj, schema)
    json.dump(obj, open(PROJ / f"artifacts/{name}.json", "w", encoding="utf-8"), indent=2)
    print(f"{name} SCHEMA-VALID", flush=True)


research = {
    "version": "1.0",
    "topic": "The halo effect from Thinking, Fast and Slow, told for an 8-year-old as why one thing she notices about someone colours everything else",
    "research_date": "2026-09-09",
    "research_summary": (
        "Film 4 of the series. Chapter 7, with support from Chapter 19. Kahneman describes the halo effect as "
        "the tendency for an early impression, or one liked attribute, to colour every subsequent judgement of "
        "the same person, producing exaggerated emotional coherence. The corrective he gives is to score "
        "independent traits one at a time, recording each before moving on. That corrective suits a child "
        "unusually well: it is a sorting task rather than an emotional discipline. At eight this governs how "
        "friendships form and how fast a single playground incident hardens into a settled opinion."
    ),
    "landscape": {
        "existing_content": [
            {"title": "Jane the Brain (NIMH)", "url": "https://www.nimh.nih.gov/get-involved/science-education/video-series-jane-the-brain",
             "source": "government site", "angle": "Coping with big feelings",
             "what_it_covers": "Feelings about oneself, not how judgements of other people form"},
            {"title": "General children's friendship guidance", "url": "https://www.scholastic.com/parents/family-life/social-emotional-learning/development-milestones/emotional-lives-8-10-year-olds.html",
             "source": "web", "angle": "Be kind, give people a chance",
             "what_it_covers": "The moral instruction without the mechanism that makes it hard to follow"},
            {"title": "The Decision Lab - System 1 and System 2", "url": "https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking",
             "source": "reference site", "angle": "Adult reference explainer",
             "what_it_covers": "Halo described accurately but through hiring and corporate examples"}
        ],
        "saturated_angles": ["Do not judge a book by its cover, stated as a rule with no mechanism",
                             "Adult hiring and performance-review framing"],
        "underserved_gaps": [
            "Why a first impression spreads, rather than simply that it should not",
            "The both-directions point: halos work for dislike exactly as they work for liking",
            "A sorting move a child can perform instead of an instruction to be fairer"
        ]
    },
    "data_points": [
        {"claim": "An early impression or one liked attribute colours every subsequent judgement of the same person, producing exaggerated emotional coherence.",
         "source_url": "https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking",
         "source_name": "Thinking, Fast and Slow, Ch 7", "credibility": "secondary_source",
         "surprise_factor": "counterintuitive", "usable_as": "core concept spine"},
        {"claim": "System 1 seeks emotional coherence, so it resolves a mixed picture into a single overall impression of good or bad.",
         "source_url": "https://www.sparknotes.com/lit/thinking-fast-and-slow/section1/",
         "source_name": "Thinking, Fast and Slow, Ch 7", "credibility": "secondary_source",
         "surprise_factor": "notable", "usable_as": "the mechanism, why the halo exists at all"},
        {"claim": "The corrective is to score independent traits one at a time and record each before moving on, so judgements do not contaminate each other.",
         "source_url": "https://www.sparknotes.com/lit/thinking-fast-and-slow/section1/",
         "source_name": "Thinking, Fast and Slow, Ch 7 and 21", "credibility": "secondary_source",
         "surprise_factor": "notable", "usable_as": "the tool at the end, expressed as separate boxes"},
        {"claim": "By age 8 to 9 children regulate judgement and emotion through explicit thoughts about them, so a sorting instruction is developmentally usable.",
         "source_url": "https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/bjep.12305",
         "source_name": "Pennequin et al., British Journal of Educational Psychology (2020)",
         "credibility": "primary_source", "surprise_factor": "expected",
         "usable_as": "justifies the separate-boxes move"}
    ],
    "audience_insights": {
        "knowledge_level": "Age 8. Has seen films 1 to 3 and owns fast one, story machine and the memory shelf.",
        "common_questions": [
            "Why did I decide I liked her so quickly?",
            "Why does everything that boy does seem annoying now?",
            "How do I know if someone is actually nice?"
        ],
        "misconceptions": [
            {"myth": "If I like one thing about someone, the rest of them is probably good too",
             "reality": "Being good at one thing tells you almost nothing about anything else. The spread is your brain, not the person.",
             "source": "Ch 7"},
            {"myth": "A halo only happens when you like someone",
             "reality": "It works identically in the other direction. One disliked moment darkens everything after it.",
             "source": "Ch 7"},
            {"myth": "My overall impression of a person is made of lots of evidence",
             "reality": "It is usually made of the first one or two things you happened to notice.",
             "source": "Ch 7"}
        ],
        "pain_points": [
            "Being told to give someone a chance without being told why she already decided",
            "Realising later that she was unfair to somebody and not understanding how it happened"
        ]
    },
    "angles_discovered": [
        {"name": "The Drop of Paint", "type": "narrative",
         "hook": "One brilliant horse drawing, and by lunchtime Diana knew the new girl was clever, kind and fast at running.",
         "why_now": "A first-day moment every child recognises, and it makes the spread visible as a single drop of colour.",
         "grounded_in": ["Ch 7 halo effect", "Ch 7 emotional coherence"]},
        {"name": "It Works Both Ways", "type": "contrarian",
         "hook": "A boy pushed in front once. Now even his laugh sounds mean.",
         "why_now": "The dark halo is the half children are never taught and the half that causes real unfairness at this age.",
         "grounded_in": ["Ch 7 halo in both directions"]},
        {"name": "Keep the Boxes Separate", "type": "evergreen",
         "hook": "Good at drawing is one box. Kind is a different box. Do not let them leak.",
         "why_now": "Kahneman's own corrective, and a sorting task rather than an emotional discipline, which suits an 8-year-old.",
         "grounded_in": ["Ch 7 and Ch 21, scoring traits independently"]}
    ],
    "expert_voices": [
        {"name": "Daniel Kahneman", "title_or_affiliation": "Nobel laureate, author",
         "position": "The halo effect makes an impression of a person more emotionally coherent than the evidence warrants; independent scoring of separate traits is the corrective.",
         "source_url": "https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking",
         "contrarian": False}
    ],
    "sources": [
        {"url": "https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking",
         "title": "System 1 and System 2 Thinking - The Decision Lab", "used_for": "Halo definition", "reliability": "secondary"},
        {"url": "https://www.sparknotes.com/lit/thinking-fast-and-slow/section1/",
         "title": "Thinking, Fast and Slow Summary", "used_for": "Chapters 7 and 19", "reliability": "secondary"},
        {"url": "https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/bjep.12305",
         "title": "Metacognition and emotional regulation in children 8 to 12", "used_for": "Age appropriateness of a sorting move", "reliability": "primary"},
        {"url": "https://www.nimh.nih.gov/get-involved/science-education/video-series-jane-the-brain",
         "title": "Jane the Brain - NIMH", "used_for": "Format benchmark", "reliability": "primary"},
        {"url": "https://www.scholastic.com/parents/family-life/social-emotional-learning/development-milestones/emotional-lives-8-10-year-olds.html",
         "title": "Social and Emotional Lives of 8- to 10-Year-Olds", "used_for": "Friendship formation at this age", "reliability": "secondary"}
    ],
    "metadata": {
        "series": "Film 4 of 18.",
        "excluded_claims": [
            "All hiring, interview and performance-review examples, which are the standard adult framing.",
            "Anything from the priming or ego-depletion chapters."
        ]
    }
}
validate(research, "research_brief")

proposal = {
    "version": "1.0",
    "concept_options": [
        {"id": "c1", "title": "The Halo",
         "hook": "There is a new girl in Diana's class. On her very first day she drew a horse, and it was brilliant.",
         "narrative_structure": "story",
         "visual_approach": "The established storybook world. New device: a single drop of bright gold paint landing on cream paper and spreading until the whole page is that colour, then the identical thing in grey for the dark halo. The corrective is small separate cards that do not touch.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old, watched with her dad",
         "target_platform": "generic", "target_duration_seconds": 175,
         "key_points": ["One good thing spreads over everything else",
                        "It works exactly the same way for dislike",
                        "The fast one wants one simple answer about a whole person",
                        "You can decide about someone's entire self in about four seconds",
                        "The move: keep the boxes separate and leave most of them empty"],
         "core_message": "One thing you notice first spreads out and colours the whole person. Keep the boxes separate, and it is fine not to know yet.",
         "cta": "When you decide you like or dislike someone, ask which one thing you are actually going on.",
         "tone": "Warm, curious, gently self-implicating. The narrator does it too.",
         "why_this_works": "A first-day moment every child recognises, it teaches the dark halo which children are never taught, and its corrective is a sorting task rather than an instruction to be fairer.",
         "grounded_in": ["Ch 7 halo effect", "Ch 7 emotional coherence"]},
        {"id": "c2", "title": "It Works Both Ways",
         "hook": "He pushed in front once. Now even his laugh sounds mean.",
         "narrative_structure": "myth_busting",
         "visual_approach": "A grey drop spreading, and every ordinary thing the boy does seen through the grey.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 150,
         "key_points": ["Dislike halos exist", "One moment recolours everything after it", "Unfairness without anyone intending it"],
         "core_message": "The dark halo is the same machinery as the bright one.",
         "cta": "Ask what you are still assuming about somebody.", "tone": "Serious and fair",
         "why_this_works": "The most socially valuable half, but bleak as a whole film at this age, so it becomes the second act of c1.",
         "grounded_in": ["Ch 7 halo in both directions"]},
        {"id": "c3", "title": "Keep the Boxes Separate",
         "hook": "Good at drawing is one box. Kind is a completely different box.",
         "narrative_structure": "tutorial",
         "visual_approach": "Small cards filled in one at a time on the cream page.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 120,
         "key_points": ["Traits are separate", "Fill them one at a time", "Most stay empty and that is fine"],
         "core_message": "Sort, do not summarise.", "cta": "Fill one box at a time.", "tone": "Practical",
         "why_this_works": "Kahneman's actual corrective and the most usable part, but an instruction without a story, so it becomes the final act of c1.",
         "grounded_in": ["Ch 7 and Ch 21, independent scoring"]}
    ],
    "selected_concept": {
        "concept_id": "c1",
        "rationale": "c1 opens on a recognisable first day, absorbs the dark halo as its second act and the sorting move as its third. The other two land as a lecture and an instruction respectively.",
        "modifications": ["All production decisions carry over from films 1 to 3",
                          "New device: the spreading drop of paint",
                          "Two new locked characters, both clearly distinct from Diana"]
    },
    "production_plan": {
        "pipeline": "animated-explainer", "playbook": "custom-atelier-storybook",
        "renderer_family": "explainer-teacher", "render_runtime": "remotion", "composition_mode": "atelier",
        "delivery_promise": {"promise_type": "teacher_explainer", "motion_required": False, "source_required": False,
                             "tone_mode": "intimate and curious, a bedtime storybook read aloud",
                             "quality_floor": "presentable", "approved_fallback": "still_led"},
        "art_direction": "Unchanged series house style. New device: one drop of paint spreading across the page, gold for the bright halo and grey for the dark one, then separate untouching cards as the corrective.",
        "taste_profile": {
            "design_read": "The same bedtime picture book, three chapters on",
            "visual_variance": 8, "motion_intensity": 3, "information_density": 2,
            "palette_discipline": "Unchanged, with grey introduced only for the dark halo.",
            "layout_variation": "Each scene composed for its beat. The spreading drop gives this film its own geometry.",
            "reference_strategy": "Series continuity only.",
            "anti_patterns": ["a clause that applies to only some scenes being pasted into every prompt, which caused six regenerations in film 3",
                              "two children in one frame unless deliberate and visually distinct",
                              "asking the image model for an exact count",
                              "drawing the boy as a villain; he is an ordinary child seen through grey"],
            "quality_gates": ["Contact sheet of all illustrations reviewed before render",
                              "Per-scene clauses applied only to the scenes they belong to",
                              "The boy is never drawn as menacing or unkind"]
        },
        "music_source": {"source_type": "ai_generated", "provider": "reused from film 1 (Google Lyria)",
                         "mood_direction": "The same bed as films 1 to 3.", "estimated_cost_usd": 0.0},
        "voice_selection": {"provider": "elevenlabs", "voice_id": "JBFqnCBsd6RMkjVDRZzb",
                            "rationale": "The same warm storyteller voice as films 1 to 3.",
                            "estimated_cost_usd": 0.8,
                            "delivery_style": "warm parent reading a bedtime story, gently self-implicating",
                            "pacing_policy": "Roughly 110 words per minute with three genuine silences.",
                            "sample_approval_required": False},
        "stages": [
            {"stage": "script", "approach": "Around 360 words at an 8-year-old listening level, three pause beats.", "tools": []},
            {"stage": "scene_plan", "approach": "Eighteen scenes, the spreading drop carrying the middle.", "tools": []},
            {"stage": "assets", "approach": "Same image model and character lock, same voice, music reused.",
             "tools": [{"tool_name": "google_imagen", "role": "illustration", "available": True},
                       {"tool_name": "elevenlabs_tts", "role": "narration", "available": True}]},
            {"stage": "edit", "approach": "Timeline rebuilt from measured narration durations.", "tools": []},
            {"stage": "compose", "approach": "Atelier Remotion render reusing the series composition.",
             "tools": [{"tool_name": "video_compose", "role": "render", "available": True}]}
        ],
        "quality_tradeoffs": [
            {"tradeoff": "Including the dark halo versus keeping the film positive",
             "recommendation": "Include", "quality_impact": "The dislike direction is where the real unfairness happens at this age. Omitting it would make a pleasant film that fixes nothing."},
            {"tradeoff": "Naming the two other children versus leaving them unnamed",
             "recommendation": "Unnamed", "quality_impact": "Keeps focus on the mechanism and avoids implying anything about real classmates."}
        ],
        "alternative_paths": [
            {"description": "Bright halo only, no dark half", "total_cost_usd": 1.52, "quality_level": "standard"},
            {"description": "Reuse everything from films 1 to 3", "total_cost_usd": 1.52, "quality_level": "standard"}
        ]
    },
    "cost_estimate": {
        "total_estimated_usd": 1.52, "budget_cap_usd": 2.5, "budget_verdict": "within_budget",
        "line_items": [
            {"tool": "google_imagen", "operation": "storybook illustrations", "quantity": 18, "estimated_usd": 0.72, "notes": "0.04 USD each"},
            {"tool": "elevenlabs_tts", "operation": "narration", "quantity": 1, "estimated_usd": 0.8, "notes": "Zero if Daniel records it"},
            {"tool": "video_compose", "operation": "local render", "quantity": 1, "estimated_usd": 0.0, "notes": "No API cost"}
        ],
        "savings_options": ["Daniel records the narration", "Music already reused at no cost"]
    },
    "approval": {"status": "approved", "approved_budget_usd": 2.5,
                 "user_notes": "User replied next, selecting film 4. All production decisions carry over from films 1 to 3."},
    "metadata": {"series_position": "4 of 18",
                 "carried_over": ["character lock", "style lock", "voice", "runtime", "composition mode", "music bed"],
                 "new_this_film": ["spreading drop of paint device", "two new locked child characters"],
                 "lesson_applied_from_film_3": "Per-scene clauses are applied only to the scenes they belong to, never pasted into every prompt."}
}
validate(proposal, "proposal_packet")

S = [
    ("s1", "The new girl",
     "There is a new girl in Diana's class. On her very first day, she drew a horse. And it was brilliant.",
     'There is a new girl in Diana’s class. <break time="0.4s"/> On her very first day, she drew a horse. <break time="0.5s"/> And it was brilliant.',
     1.2, "measured", "warm", ["brilliant"], "Light and admiring. Genuinely impressed."),
    ("s2", "What Diana knew by lunchtime",
     "And by lunchtime, Diana knew a great many things about her. She was clever. She was kind. She would be a very good friend. She was probably fast at running too.",
     'And by lunchtime, Diana knew a great many things about her. <break time="0.5s"/> She was clever. <break time="0.3s"/> She was kind. <break time="0.3s"/> She would be a very good friend. <break time="0.3s"/> She was probably fast at running too.',
     1.2, "conversational", "quickening", ["knew"], "Let the list gather speed and confidence. The confidence is the joke."),
    ("s3", "One thing",
     "But Diana had seen her do exactly one thing. Draw a horse.",
     'But Diana had seen her do exactly one thing. <break time="0.6s"/> Draw a horse. <break time="2.5s"/>',
     2.5, "slow", "wry", ["one"], "Pause beat one. Let the gap between one horse and four conclusions sit."),
    ("s4", "Name it",
     "This is called a halo. One bright thing, glowing away, and the light spreads out over everything standing near it.",
     'This is called a halo. <break time="0.5s"/> One bright thing, glowing away, <break time="0.4s"/> and the light spreads out over everything standing near it.',
     1.2, "measured", "curious", ["halo"], "Introduce the word gently. It is the only technical word in the film."),
    ("s5", "One drop",
     "Your brain does it with a single drop of paint. One drop. And the whole page turns that colour.",
     'Your brain does it with a single drop of paint. <break time="0.5s"/> One drop. <break time="0.4s"/> And the whole page turns that colour.',
     1.2, "slow", "gentle", ["drop"], "Slow. This is the central image."),
    ("s6", "Both ways",
     "And it works exactly the same way backwards.",
     'And it works exactly the same way backwards.',
     1.2, "measured", "steady", ["backwards"], "A small turn. Something colder is coming."),
    ("s7", "The boy",
     "A boy pushed in front of Diana in the line once. Just once. And now everything he does looks a little bit mean.",
     'A boy pushed in front of Diana in the line once. <break time="0.4s"/> Just once. <break time="0.6s"/> And now everything he does looks a little bit mean.',
     1.2, "measured", "tender", ["once"], "Not angry. Just true."),
    ("s8", "Through the grey",
     "He laughs. That is a mean laugh. He runs past. He was probably being rude. He did not even do anything.",
     'He laughs. <break time="0.3s"/> That is a mean laugh. <break time="0.4s"/> He runs past. <break time="0.3s"/> He was probably being rude. <break time="0.6s"/> He did not even do anything. <break time="2.5s"/>',
     2.5, "measured", "quiet", ["anything"], "Pause beat two. She may recognise somebody real here."),
    ("s9", "Why it does it",
     "Here is why your fast one does this. It cannot stand a messy picture. It wants one simple answer. Is this person good, or not good?",
     'Here is why your fast one does this. <break time="0.5s"/> It cannot stand a messy picture. <break time="0.5s"/> It wants one simple answer. <break time="0.4s"/> Is this person good, <break time="0.3s"/> or not good?',
     1.4, "slow", "gentle", ["messy"], "The hinge. Slow right down."),
    ("s10", "So it paints",
     "So it takes the one thing it actually knows, and it paints the whole person with it.",
     'So it takes the one thing it actually knows, <break time="0.4s"/> and it paints the whole person with it.',
     1.2, "measured", "steady", ["whole"], "Land it plainly."),
    ("s11", "Four seconds",
     "Which means you can make up your mind about somebody's entire self in about four seconds.",
     'Which means you can make up your mind about somebody’s entire self <break time="0.4s"/> in about four seconds.',
     1.4, "slow", "wry", ["four"], "A little dry. Not scolding."),
    ("s12", "The tool",
     "So here is your fourth trick. Keep the boxes separate.",
     'So here is your fourth trick. <break time="0.5s"/> Keep the boxes separate.',
     1.0, "measured", "encouraging", ["separate"], "Bright and practical."),
    ("s13", "Separate boxes",
     "Good at drawing is one box. Kind is a completely different box. Funny is another one again. Fill them in one at a time, and do not let them leak into each other.",
     'Good at drawing is one box. <break time="0.4s"/> Kind is a completely different box. <break time="0.4s"/> Funny is another one again. <break time="0.5s"/> Fill them in one at a time, <break time="0.4s"/> and do not let them leak into each other. <break time="2.5s"/>',
     2.5, "measured", "encouraging", ["leak"], "Pause beat three. She should picture her own boxes."),
    ("s14", "You do not know yet",
     "Because mostly, you do not know yet. And not knowing yet is allowed.",
     'Because mostly, you do not know yet. <break time="0.5s"/> And not knowing yet is allowed.',
     1.4, "slow", "tender", ["allowed"], "The kindest line in the film."),
    ("s15", "Landing",
     "People are not one colour. They are lots of little boxes. And most of yours are still beautifully empty.",
     'People are not one colour. <break time="0.5s"/> They are lots of little boxes. <break time="0.5s"/> And most of yours are still beautifully empty.',
     0.0, "slow", "proud", ["empty"], "End warm. Then stop."),
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
    "version": "1.0", "title": "The Halo",
    "total_duration_seconds": round(t, 2),
    "voice_performance": {
        "performance_intent": "The same parent and child, three chapters on. Gently self-implicating: the narrator plainly does this too and never scolds her for it.",
        "pacing_profile": "contemplative",
        "energy_curve": "Bright and admiring at the horse. Gathering confidence through the list, which is the joke. Cooler and quieter through the boy. Lowest at the hinge. Warmest at not knowing yet is allowed.",
        "pause_policy": "Three genuine silences: after one horse and four conclusions, after he did not even do anything, and after being told to keep the boxes separate.",
        "sample_section_id": "s14",
        "provider_notes": {
            "all": "Roughly 110 words per minute. Section s14 is the emotional centre and the sample section.",
            "elevenlabs": "Same voice as films 1 to 3, George. Stability 0.75, similarity 0.9, style 0.15, speed 0.9.",
            "human_recording": "The list in section 2 should sound increasingly certain, because the certainty is the point."
        }
    },
    "sections": sections,
    "metadata": {
        "series_position": "4 of 18",
        "word_count_approx": sum(len(s["text"].split()) for s in sections),
        "target_wpm": 110,
        "reading_age": "Written for a listener of 8. Halo is the only technical word and it is defined on first use.",
        "pause_beats": [
            {"section": "s3", "purpose": "She notices the gap between one horse and four conclusions"},
            {"section": "s8", "purpose": "She may recognise a real person she has done this to"},
            {"section": "s13", "purpose": "She pictures her own separate boxes"}
        ],
        "grounded_in": {
            "s1_to_s5": "Ch 7, halo effect and emotional coherence",
            "s6_to_s8": "Ch 7, the halo operating identically in the dislike direction",
            "s9_to_s11": "Ch 7, System 1 resolving a mixed picture into one impression",
            "s12_to_s15": "Ch 7 and Ch 21 corrective, scoring traits independently"
        },
        "accuracy_guardrails_applied": [
            "The boy is never described or drawn as a villain. He is an ordinary child seen through a grey halo.",
            "No hiring, interview or performance-review examples.",
            "The film does not claim she can stop forming impressions, only that she can keep them separate.",
            "No priming or ego-depletion material."
        ]
    }
}
validate(script, "script")

spec = [
    ("sc1", "s1", "NEWGIRL", "A girl stands shyly just inside a classroom doorway on her first day, holding a satchel, looking a little uncertain."),
    ("sc2", "s1", "NONE", "A single sheet of paper on cream ground bearing a beautifully drawn horse in pencil. Nothing else in the picture."),
    ("sc3", "s2", "DIANA", "The girl stands looking down at a drawing with a wide impressed smile and raised eyebrows."),
    ("sc4", "s2", "NONE", "Four small square cards float in a row on cream paper, each glowing warm gold, each holding one tiny simple symbol: a pencil, a heart, two clasped hands, a running shoe."),
    ("sc5", "s3", "NONE", "One single small pencil drawing of a horse sits alone in the very centre of a huge expanse of empty cream paper. The emptiness around it is the subject of the picture."),
    ("sc6", "s4", "NONE", "One bright warm-gold circle of light glows on cream paper, with soft golden light radiating outward from it across the page."),
    ("sc7", "s5", "NONE", "A single drop of bright gold paint falls and lands on cream paper with a small splash. Nothing else in the picture."),
    ("sc8", "s5", "NONE", "Gold paint has spread outward and now covers the entire page in a warm gold wash, with only the faintest cream showing at the corners."),
    ("sc9", "s6", "DIANA", "The girl stands in the centre of the cream page. The half of the page behind her on the left is warm gold and the half on the right is cool grey."),
    ("sc10", "s7", "BOY", "A boy steps sideways into a queue, glancing away, entirely ordinary and not unkind."),
    ("sc11", "s7", "NONE", "A single drop of soft grey paint falls and lands on cream paper with a small splash. Nothing else in the picture."),
    ("sc12", "s8", "NONE", "Grey paint has spread outward and now covers the entire page in a flat cool grey wash."),
    ("sc13", "s8", "BOY", "The same boy laughs happily at something off to one side, completely ordinary and cheerful, but the whole picture is washed over in cool grey."),
    ("sc14", "s9", "DIANA", "The girl stands beside a jumbled untidy heap of many differently coloured shapes, looking at it with a slightly overwhelmed expression."),
    ("sc15", "s10", "NONE", "A paintbrush loaded with gold paint sweeps one broad flat stroke across a whole row of otherwise different objects, turning them all the same colour."),
    ("sc16", "s11", "DIANA", "The girl snaps her fingers, decisive and quick, with a small burst of warm gold lines around her hand."),
    ("sc17", "s13", "NONE", "Six small separate cards laid out neatly on cream paper with clear gaps between them, each a completely different colour, none of them touching. Two cards are filled with a small symbol and the other four are empty."),
    ("sc18", "s15", "TWO", "Two girls sit side by side on a low wall drawing together, comfortable and ordinary, in warm late afternoon light."),
]

per = {}
for _, sid, _, _ in spec:
    per[sid] = per.get(sid, 0) + 1
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
        "narrative_role": "deliver_payload" if scid in ("sc8", "sc12", "sc17") else "evidence",
        "hero_moment": scid in ("sc5", "sc8", "sc12", "sc17", "sc18"),
        "transition_in": "cut", "transition_out": "cut",
        "shot_language": {"shot_size": "wide" if scid in ("sc5", "sc8", "sc12") else "medium",
                          "camera_movement": "static", "lighting_key": "natural",
                          "depth_of_field": "medium", "color_temperature": "warm"},
        "overlay_notes": "No text in the illustration."
    })

scene_plan = {
    "version": "1.0", "style_playbook": "custom-atelier-storybook", "scenes": scenes,
    "metadata": {
        "character_lock": "Diana: a girl of eight, Vietnamese-Australian, straight black shoulder-length hair with a soft fringe, warm light skin, dark almond eyes, round friendly face, mustard-yellow knitted jumper, denim pinafore dress, red canvas shoes. Identical to films 1 to 3.",
        "newgirl_lock": "The new girl: long wavy auburn hair, plum-purple cardigan, grey skirt. Clearly distinct from Diana and from the curly-haired friend in film 2.",
        "boy_lock": "The boy: short curly dark hair, red-striped t-shirt, green shorts. Ordinary and never drawn as unkind.",
        "one_child_rule": "Every frame contains exactly one child except sc18, which deliberately shows two visually distinct girls.",
        "visual_signatures": {"halo_bright": "A drop of warm gold paint spreading to fill the page.",
                              "halo_dark": "The identical drop and spread in cool grey.",
                              "corrective": "Small separate cards with clear gaps, never touching."},
        "style_lock": "Unchanged from films 1 to 3.",
        "scene_count": len(scenes),
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
NEWGIRL = ("The girl has long wavy auburn hair, a plum-purple cardigan and a grey skirt. She looks nothing like a "
           "girl in a mustard jumper.")
BOY = ("The boy has short curly dark hair, a red-striped t-shirt and green shorts. He is an ordinary friendly-looking "
       "child and must never look mean, angry or menacing.")
STYLE = ("Children's picture-book illustration, soft gouache painting, warm cream paper background with visible "
         "paper grain, soft pencil linework, rounded organic shapes, muted warm palette, flat 2D storybook art, "
         "not 3D, no text, no lettering, no words, no numbers, no digits.")
ONE = "EXACTLY ONE CHILD in the frame, a single child alone. Do not draw two children."
NOPE = "There are NO people and NO animals at all in this picture."

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
    who = WHO[sid]
    parts = [STYLE]
    if who == "DIANA":
        parts += [ONE, DIANA]
    elif who == "NEWGIRL":
        parts += [ONE, NEWGIRL]
    elif who == "BOY":
        parts += [ONE, BOY]
    elif who == "TWO":
        parts += ["Exactly two girls, clearly different from one another.", DIANA, NEWGIRL]
    else:
        parts += [NOPE]
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
    grp = by_section[sid]
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
         "titles": [{"kind": "title", "text": "The Halo",
                     "startSec": round(last["startSec"] + 1.0, 3),
                     "durSec": round(max(2.0, last["durSec"] - 1.0), 3)}]}
(PROJ / "composition").mkdir(parents=True, exist_ok=True)
json.dump(props, open(PROJ / "composition/props.json", "w", encoding="utf-8"), indent=2)

print(f"\nDONE images_failed={img_fail} narration_failed={aud_fail}")
print(f"total {TOTAL}s ({int(TOTAL//60)}m {TOTAL%60:.1f}s) frames={props['durationInFrames']} scenes={len(pscenes)} captions={len(captions)}")
sys.exit(0 if not img_fail and not aud_fail else 1)
