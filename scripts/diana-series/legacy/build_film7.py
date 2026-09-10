"""One-shot: build film 7, The Holiday You Remember (peak-end rule, two selves)."""
import json
import re
import subprocess
import sys
from pathlib import Path

import jsonschema

from tools.tool_registry import registry

SLUG = "diana-peak-end"
PROJ = Path("projects") / SLUG
(PROJ / "artifacts").mkdir(parents=True, exist_ok=True)
DL = "https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking"
SN = "https://www.sparknotes.com/lit/thinking-fast-and-slow/section1/"
PQ = "https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/bjep.12305"
NIMH = "https://www.nimh.nih.gov/get-involved/science-education/video-series-jane-the-brain"
SCH = "https://www.scholastic.com/parents/family-life/social-emotional-learning/development-milestones/emotional-lives-8-10-year-olds.html"


def validate(obj, name):
    schema = json.load(open(f"schemas/artifacts/{name}.schema.json", encoding="utf-8"))
    jsonschema.validate(obj, schema)
    json.dump(obj, open(PROJ / f"artifacts/{name}.json", "w", encoding="utf-8"), indent=2)
    print(f"{name} SCHEMA-VALID", flush=True)


research = {
    "version": "1.0",
    "topic": "The peak-end rule and the two selves from Thinking, Fast and Slow, told for an 8-year-old as why she remembers a whole day by two moments",
    "research_date": "2026-09-09",
    "research_summary": (
        "Film 7 of the series. Chapters 35 and 36. Memory scores an episode by its peak and its ending and "
        "largely ignores how long it lasted, which Kahneman calls duration neglect and the peak-end rule. The "
        "experiencing self lives through every minute; the remembering self keeps two of them and makes all the "
        "decisions. For a child this explains why a long happy afternoon ruined in its final ten minutes is "
        "recorded as a bad afternoon, and it gives her a reason to protect endings."
    ),
    "landscape": {
        "existing_content": [
            {"title": "Jane the Brain (NIMH)", "url": NIMH, "source": "government site",
             "angle": "Coping with big feelings", "what_it_covers": "Feelings in the moment, not how memory scores them afterwards"},
            {"title": "Children's gratitude and reflection material", "url": SCH, "source": "web",
             "angle": "Count your happy moments", "what_it_covers": "Encourages recall without explaining why recall is biased"},
            {"title": "The Decision Lab - System 1 and System 2", "url": DL, "source": "reference site",
             "angle": "Adult reference explainer", "what_it_covers": "Peak-end described through colonoscopy and holiday studies"}
        ],
        "saturated_angles": ["Gratitude journals and counting happy moments",
                             "Adult medical-procedure and vacation-choice framing"],
        "underserved_gaps": [
            "Telling a child that a bad ending overwrites a good day, and that this is a recording error rather than the truth",
            "The two selves given as two versions of her rather than as psychology",
            "A reason to deliberately protect the last ten minutes of anything"
        ]
    },
    "data_points": [
        {"claim": "Memory scores an episode by its most intense moment and its ending, and largely ignores its duration.",
         "source_url": DL, "source_name": "Thinking, Fast and Slow, Ch 35",
         "credibility": "secondary_source", "surprise_factor": "counterintuitive", "usable_as": "core concept spine"},
        {"claim": "Duration neglect means a longer period of good experience adds almost nothing to the remembered score.",
         "source_url": SN, "source_name": "Thinking, Fast and Slow, Ch 35",
         "credibility": "secondary_source", "surprise_factor": "surprising", "usable_as": "why the long happy afternoon disappears"},
        {"claim": "The experiencing self lives through every moment; the remembering self keeps the summary and makes the decisions.",
         "source_url": SN, "source_name": "Thinking, Fast and Slow, Ch 35 and 36",
         "credibility": "secondary_source", "surprise_factor": "counterintuitive", "usable_as": "the two-selves device"},
        {"claim": "By age 8 to 9 children reflect on their own feelings explicitly, so a check-the-ending instruction is usable.",
         "source_url": PQ, "source_name": "Pennequin et al., British Journal of Educational Psychology (2020)",
         "credibility": "primary_source", "surprise_factor": "expected", "usable_as": "justifies the ending tool"}
    ],
    "audience_insights": {
        "knowledge_level": "Age 8. Has seen films 1 to 6 and owns fast one, story machine, memory shelf, separate boxes, the bouncing dot and remember-do-not-guess.",
        "common_questions": [
            "Why did one bad bit spoil the whole day?",
            "Why do I only remember a few bits of the holiday?",
            "Was it actually a bad day or does it just feel like one?"
        ],
        "misconceptions": [
            {"myth": "If I remember a day as bad, it was bad", "reality": "Memory keeps the peak and the ending. A long good stretch can vanish from the score entirely.", "source": "Ch 35"},
            {"myth": "A longer happy time is remembered as happier", "reality": "Duration is almost ignored. Length barely changes the remembered score.", "source": "Ch 35"},
            {"myth": "There is one me who both lives and remembers", "reality": "The one living it and the one remembering it disagree, and the remembering one decides.", "source": "Ch 35 and 36"}
        ],
        "pain_points": ["A ruined ending erasing a whole good day",
                        "Feeling that her own memory is lying to her without knowing why"]
    },
    "angles_discovered": [
        {"name": "Two of You", "type": "narrative",
         "hook": "There is the you who is there, and the you who remembers. They do not agree about much.",
         "why_now": "The two-selves idea is the clearest device in the chapter and a child can hold it as two versions of herself.",
         "grounded_in": ["Ch 35 experiencing and remembering self"]},
        {"name": "Only Two Bits Get Kept", "type": "evergreen",
         "hook": "The best bit. And how it ended. That is the whole recording.",
         "why_now": "Explains a specific injustice she has felt, that one bad ending overwrote a good day.",
         "grounded_in": ["Ch 35 peak-end rule and duration neglect"]},
        {"name": "Endings Count Double", "type": "contrarian",
         "hook": "So look after the last ten minutes of things.",
         "why_now": "Turns the finding into something she can actually do, which nothing else in the children's landscape offers.",
         "grounded_in": ["Ch 35 corrective", "Pennequin on reflection at 8 to 9"]}
    ],
    "expert_voices": [
        {"name": "Daniel Kahneman", "title_or_affiliation": "Nobel laureate, author",
         "position": "Memory scores by peak and end and neglects duration; the remembering self makes the decisions.",
         "source_url": DL, "contrarian": False}
    ],
    "sources": [
        {"url": DL, "title": "System 1 and System 2 Thinking - The Decision Lab", "used_for": "Peak-end and two selves", "reliability": "secondary"},
        {"url": SN, "title": "Thinking, Fast and Slow Summary", "used_for": "Chapters 35 and 36", "reliability": "secondary"},
        {"url": PQ, "title": "Metacognition and emotional regulation in children 8 to 12", "used_for": "Age appropriateness", "reliability": "primary"},
        {"url": NIMH, "title": "Jane the Brain - NIMH", "used_for": "Format benchmark", "reliability": "primary"},
        {"url": SCH, "title": "Social and Emotional Lives of 8- to 10-Year-Olds", "used_for": "Reflection and memory at this age", "reliability": "secondary"}
    ],
    "metadata": {"series": "Film 7 of 18.",
                 "excluded_claims": ["The colonoscopy and cold-water experiments, which are the standard adult evidence and unsuitable here.",
                                     "Anything from the priming or ego-depletion chapters."]}
}
validate(research, "research_brief")

proposal = {
    "version": "1.0",
    "concept_options": [
        {"id": "c1", "title": "The Holiday You Remember",
         "hook": "Think about last summer. Which bit do you actually remember?",
         "narrative_structure": "story",
         "visual_approach": "The established storybook world. New device: a long ribbon of many small squares laid across the cream page, one square for every minute, and a small hand that reaches down and lifts out exactly two of them, the brightest and the last.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old, watched with her dad",
         "target_platform": "generic", "target_duration_seconds": 175,
         "key_points": ["Memory keeps the best bit and the ending, and almost nothing else",
                        "How long something lasted barely counts at all",
                        "There are two of her: the one living it and the one remembering it",
                        "A bad last ten minutes can overwrite a whole good afternoon",
                        "The move: protect endings, and ask whether the whole day was bad or only the end"],
         "core_message": "Your memory keeps two moments and calls them the whole day. You still had all the other minutes. They just did not get written down.",
         "cta": "When you say a day was rubbish, ask whether the whole day was rubbish or only the end of it.",
         "tone": "Warm, a little wistful, ultimately consoling.",
         "why_this_works": "It explains an injustice she has felt without words, and it gives her something to do about endings, which no children's content offers.",
         "grounded_in": ["Ch 35 peak-end and duration neglect", "Ch 35 and 36 two selves"]},
        {"id": "c2", "title": "Two of You",
         "hook": "There is the you who is there, and the you who remembers.",
         "narrative_structure": "comparison",
         "visual_approach": "Two versions of the same girl on facing halves of the page, one walking a long path and one holding a small frame.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 140,
         "key_points": ["One lives every minute", "One keeps a summary", "The summary one decides"],
         "core_message": "The one who remembers is in charge.", "cta": "Notice which one is talking.", "tone": "Curious",
         "why_this_works": "The strongest device but abstract on its own, so it becomes the middle of c1.",
         "grounded_in": ["Ch 35 two selves"]},
        {"id": "c3", "title": "Endings Count Double",
         "hook": "Look after the last ten minutes of things.",
         "narrative_structure": "tutorial",
         "visual_approach": "The final square of the ribbon glowing twice as bright as the rest.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 110,
         "key_points": ["Endings are weighted", "You can choose them", "Small effort, large effect"],
         "core_message": "Endings are worth protecting.", "cta": "Plan the last bit.", "tone": "Practical",
         "why_this_works": "The most actionable part but an instruction without the explanation, so it becomes the final act of c1.",
         "grounded_in": ["Ch 35 corrective"]}
    ],
    "selected_concept": {"concept_id": "c1",
                         "rationale": "c1 opens on her own memory of last summer, uses the two selves as its middle and endings-count-double as its payoff. The others are the same material without the personal opening that makes it land.",
                         "modifications": ["All production decisions carry over from films 1 to 6",
                                           "New device: the ribbon of minute-squares and the hand that keeps two",
                                           "Scene coverage asserted before generation, as in films 5 and 6"]},
    "production_plan": {
        "pipeline": "animated-explainer", "playbook": "custom-atelier-storybook",
        "renderer_family": "explainer-teacher", "render_runtime": "remotion", "composition_mode": "atelier",
        "delivery_promise": {"promise_type": "teacher_explainer", "motion_required": False, "source_required": False,
                             "tone_mode": "intimate and wistful, a bedtime storybook read aloud",
                             "quality_floor": "presentable", "approved_fallback": "still_led"},
        "art_direction": "Unchanged series house style. New device: a long ribbon of small squares for the minutes, and exactly two of them lifted out and kept.",
        "taste_profile": {"design_read": "The same bedtime picture book, six chapters on",
                          "visual_variance": 8, "motion_intensity": 3, "information_density": 2,
                          "palette_discipline": "Unchanged. Cream ground, muted warm palette, gold and blue accents.",
                          "layout_variation": "Each scene composed for its beat. The ribbon gives this film its geometry.",
                          "reference_strategy": "Series continuity only.",
                          "anti_patterns": ["asking the image model for an exact count of squares",
                                            "two children in one frame",
                                            "charts, timelines with tick marks, or numerals",
                                            "implying the bad ending did not matter or that she should just be positive"],
                          "quality_gates": ["Contact sheet reviewed before render",
                                            "Every script section mapped to a scene, asserted at build time",
                                            "No numerals; the ribbon is many squares, never a counted number"]},
        "music_source": {"source_type": "ai_generated", "provider": "reused from film 1 (Google Lyria)",
                         "mood_direction": "The same bed as films 1 to 6.", "estimated_cost_usd": 0.0},
        "voice_selection": {"provider": "elevenlabs", "voice_id": "JBFqnCBsd6RMkjVDRZzb",
                            "rationale": "The same warm storyteller voice as films 1 to 6.",
                            "estimated_cost_usd": 0.85,
                            "delivery_style": "warm parent reading a bedtime story, a little wistful",
                            "pacing_policy": "Roughly 110 words per minute with three genuine silences.",
                            "sample_approval_required": False},
        "stages": [
            {"stage": "script", "approach": "Around 390 words at an 8-year-old listening level, three pause beats.", "tools": []},
            {"stage": "scene_plan", "approach": "Eighteen scenes covering all fifteen sections, the ribbon carrying the middle.", "tools": []},
            {"stage": "assets", "approach": "Same image model and character lock, same voice, music reused.",
             "tools": [{"tool_name": "google_imagen", "role": "illustration", "available": True},
                       {"tool_name": "elevenlabs_tts", "role": "narration", "available": True}]},
            {"stage": "edit", "approach": "Timeline rebuilt from measured narration durations.", "tools": []},
            {"stage": "compose", "approach": "Atelier Remotion render reusing the series composition.",
             "tools": [{"tool_name": "video_compose", "role": "render", "available": True}]}
        ],
        "quality_tradeoffs": [
            {"tradeoff": "Naming the two selves versus describing them as two versions of her",
             "recommendation": "Two versions of her", "quality_impact": "Experiencing self and remembering self are adult terms. The you who is there and the you who remembers carries the same idea at this age."},
            {"tradeoff": "Using a spoiled day as the example versus a purely positive one",
             "recommendation": "Spoiled day", "quality_impact": "The injustice is the reason the film exists. A positive-only version would explain nothing she needs explained."}
        ],
        "alternative_paths": [
            {"description": "Two selves only, endings tool deferred", "total_cost_usd": 1.57, "quality_level": "standard"},
            {"description": "Reuse everything from films 1 to 6", "total_cost_usd": 1.57, "quality_level": "standard"}
        ]
    },
    "cost_estimate": {"total_estimated_usd": 1.57, "budget_cap_usd": 2.5, "budget_verdict": "within_budget",
                      "line_items": [
                          {"tool": "google_imagen", "operation": "storybook illustrations", "quantity": 18, "estimated_usd": 0.72, "notes": "0.04 USD each"},
                          {"tool": "elevenlabs_tts", "operation": "narration", "quantity": 1, "estimated_usd": 0.85, "notes": "Zero if Daniel records it"},
                          {"tool": "video_compose", "operation": "local render", "quantity": 1, "estimated_usd": 0.0, "notes": "No API cost"}],
                      "savings_options": ["Daniel records the narration", "Music already reused at no cost"]},
    "approval": {"status": "approved", "approved_budget_usd": 2.5,
                 "user_notes": "User replied NEXT, selecting film 7, under a standing instruction to fix defects without asking."},
    "metadata": {"series_position": "7 of 18",
                 "carried_over": ["character lock", "style lock", "voice", "runtime", "composition mode", "music bed"],
                 "new_this_film": ["ribbon of minute-squares device"]}
}
validate(proposal, "proposal_packet")

S = [
    ("s1", "Which bit",
     "Think about last summer, Diana. Which bit do you actually remember?",
     'Think about last summer, Diana. <break time="0.5s"/> Which bit do you actually remember? <break time="2.5s"/>',
     2.5, "slow", "warm", ["remember"], "Pause beat one. Genuinely wait; she will find one or two moments."),
    ("s2", "One good bit and the end",
     "I think it was one really good bit. And the very end.",
     'I think it was one really good bit. <break time="0.5s"/> And the very end.',
     1.2, "measured", "gentle", ["end"], "Quietly confident, like someone who already knows."),
    ("s3", "Not the whole thing",
     "Not the whole holiday. Not all those days. Just those two little pieces.",
     'Not the whole holiday. <break time="0.4s"/> Not all those days. <break time="0.5s"/> Just those two little pieces.',
     1.4, "slow", "wistful", ["two"], "A touch of sadness is allowed here."),
    ("s4", "The one who is there",
     "Here is a strange thing. There are two of you. There is the you who is actually there, in the middle of it, right now.",
     'Here is a strange thing. <break time="0.5s"/> There are two of you. <break time="0.5s"/> There is the you who is actually there, in the middle of it, right now.',
     1.4, "measured", "curious", ["two of you"], "Introduce the device clearly."),
    ("s5", "The one who remembers",
     "And there is the you who remembers it afterwards, later, in bed.",
     'And there is the you who remembers it afterwards, <break time="0.4s"/> later, <break time="0.3s"/> in bed.',
     1.2, "slow", "gentle", ["remembers"], "Softer. This is the one she will recognise."),
    ("s6", "They disagree",
     "And those two do not agree about very much at all.",
     'And those two do not agree about very much at all.',
     1.4, "measured", "steady", ["disagree"], "Plain. Let it sit."),
    ("s7", "Every minute",
     "The one who is there feels every single minute. All of them. Every one counts the same.",
     'The one who is there feels every single minute. <break time="0.4s"/> All of them. <break time="0.4s"/> Every one counts the same.',
     1.2, "measured", "warm", ["every"], "Generous and full."),
    ("s8", "Only two things",
     "But the one who remembers only keeps two things. The very best bit. And how it ended.",
     'But the one who remembers only keeps two things. <break time="0.5s"/> The very best bit. <break time="0.4s"/> And how it ended.',
     1.4, "slow", "gentle", ["two things"], "The hinge. Slow right down."),
    ("s9", "And calls it the day",
     "Then it puts those two together, and calls that the whole day.",
     'Then it puts those two together, <break time="0.4s"/> and calls that the whole day.',
     1.4, "slow", "steady", ["whole day"], "Firm."),
    ("s10", "The spoiled afternoon",
     "Which is why a long, lovely afternoon that goes wrong in the last ten minutes gets remembered as a horrible afternoon.",
     'Which is why a long, lovely afternoon that goes wrong in the last ten minutes <break time="0.5s"/> gets remembered as a horrible afternoon.',
     1.4, "measured", "tender", ["horrible"], "She will have one of these in mind."),
    ("s11", "The short lovely one",
     "And a short one, with one brilliant moment and a happy goodbye, becomes the best day ever.",
     'And a short one, with one brilliant moment and a happy goodbye, <break time="0.5s"/> becomes the best day ever. <break time="2.5s"/>',
     2.5, "measured", "warm", ["best"], "Pause beat two. Let her compare the two days."),
    ("s12", "Even though",
     "Even though the first one had far, far more happy minutes inside it.",
     'Even though the first one had far, far more happy minutes inside it.',
     1.4, "slow", "wistful", ["more"], "The quiet injustice of it."),
    ("s13", "The first tool",
     "So here is your seventh trick, and it comes in two halves. When something is ending, pay attention. Endings count double.",
     'So here is your seventh trick, and it comes in two halves. <break time="0.5s"/> When something is ending, pay attention. <break time="0.5s"/> Endings count double.',
     1.4, "measured", "encouraging", ["double"], "Bright and useful."),
    ("s14", "The second tool",
     "And when you catch yourself saying a day was rubbish, ask this. Was the whole day rubbish? Or just the end of it?",
     'And when you catch yourself saying a day was rubbish, ask this. <break time="0.5s"/> Was the whole day rubbish? <break time="0.5s"/> Or just the end of it? <break time="2.5s"/>',
     2.5, "measured", "encouraging", ["whole"], "Pause beat three. She should test it on a real day."),
    ("s15", "Landing",
     "Because you had all those other minutes too. You really did have them. The you who remembers just forgot to write them down.",
     'Because you had all those other minutes too. <break time="0.5s"/> You really did have them. <break time="0.5s"/> The you who remembers just forgot to write them down.',
     0.0, "slow", "tender", ["really did"], "The consolation. End soft, then stop."),
]

sections, t = [], 0.0
for sid, label, text, prov, pause, pace, energy, emph, note in S:
    dur = round(len(text.split()) / 110 * 60 + pause, 2)
    sections.append({"id": sid, "label": label, "text": text,
                     "start_seconds": round(t, 2), "end_seconds": round(t + dur, 2),
                     "speaker_directions": note,
                     "delivery_cues": {"pace": pace, "energy": energy, "emphasis_words": emph,
                                       "pause_after_seconds": pause, "delivery_note": note, "provider_text": prov},
                     "enhancement_cues": [], "pronunciation_guides": []})
    t += dur

script = {
    "version": "1.0", "title": "The Holiday You Remember",
    "total_duration_seconds": round(t, 2),
    "voice_performance": {
        "performance_intent": "The same parent and child, six chapters on. This one is wistful rather than wry. It is about something being lost, and it ends by giving it back.",
        "pacing_profile": "contemplative",
        "energy_curve": "Quiet and inviting at the opening question. Gentle through the two selves. Slowest at only keeps two things. Warm at the tools. Softest at the final consolation.",
        "pause_policy": "Three genuine silences: after which bit do you remember, after the best day ever comparison, and after was the whole day rubbish.",
        "sample_section_id": "s15",
        "provider_notes": {"all": "Roughly 110 words per minute. Section s15 is the consolation and the sample section.",
                           "elevenlabs": "Same voice as films 1 to 6, George. Stability 0.75, similarity 0.9, style 0.15, speed 0.9.",
                           "human_recording": "The final line should sound like a gift being handed back, not like a lesson."}
    },
    "sections": sections,
    "metadata": {
        "series_position": "7 of 18",
        "word_count_approx": sum(len(s["text"].split()) for s in sections),
        "target_wpm": 110,
        "reading_age": "Written for a listener of 8. Peak-end, duration neglect, experiencing self and remembering self never appear as terms.",
        "pause_beats": [{"section": "s1", "purpose": "She retrieves her own two moments and notices there are only two"},
                        {"section": "s11", "purpose": "She compares the long spoiled day with the short lovely one"},
                        {"section": "s14", "purpose": "She tests the question on a real day"}],
        "grounded_in": {"s1_to_s3": "Ch 35, peak-end recall of an episode",
                        "s4_to_s6": "Ch 35 and 36, experiencing and remembering selves",
                        "s7_to_s9": "Ch 35, duration neglect and the peak-end summary",
                        "s10_to_s12": "Ch 35, a bad ending dominating a longer good period",
                        "s13_to_s15": "Ch 35 corrective plus Pennequin on reflection at 8 to 9"},
        "accuracy_guardrails_applied": [
            "The film never says the bad ending did not matter, only that it is weighted more than it deserves.",
            "No colonoscopy or cold-water experiments.",
            "The two selves are described as two versions of her, never with the adult terms.",
            "No priming or ego-depletion material."]
    }
}
validate(script, "script")

spec = [
    ("sc1", "s1", "DIANA", "The girl sits on her bed at night with the lamp on, looking upward and thinking, a soft warm glow around her."),
    ("sc2", "s2", "NONE", "Two small square photographs float side by side on cream paper. One glows warmly, the other is quieter. Nothing else in the picture."),
    ("sc3", "s3", "NONE", "A very long ribbon of many small pale squares stretches right across the cream page from edge to edge, with only two of the squares warmly coloured and the rest faded."),
    ("sc4", "s4", "DIANA", "The girl runs happily along a sunny beach, entirely absorbed in the moment, sand and sea behind her."),
    ("sc5", "s5", "DIANA", "The same girl lying in bed later that night, eyes open, a small softly glowing frame floating above her."),
    ("sc6", "s6", "NONE", "Two small paper frames on cream paper facing away from one another at slightly different angles, as if disagreeing. Nothing else."),
    ("sc7", "s7", "NONE", "A long ribbon of many small squares across the cream page, every single square warmly and equally coloured, all the same brightness."),
    ("sc8", "s8", "NONE", "The same long ribbon of squares, now mostly faded pale, with exactly one bright square in the middle and one bright square at the very end."),
    ("sc9", "s8", "NONE", "A small hand reaching down and lifting one bright square out of a long faded ribbon on cream paper."),
    ("sc10", "s9", "NONE", "Two bright squares placed together inside a small paper frame on cream paper, with the long faded ribbon lying discarded behind them."),
    ("sc11", "s10", "DIANA", "The girl on a beach at the end of the day, damp and downcast, a dropped ice cream on the sand beside her, warm evening light."),
    ("sc12", "s10", "NONE", "A long ribbon of warmly coloured squares with only the last few squares darkened to grey, and the grey spreading backwards a little into the ones before."),
    ("sc13", "s11", "DIANA", "The girl waving a happy goodbye at a gate in golden late light, cheerful and content."),
    ("sc14", "s12", "NONE", "Two ribbons drawn one above the other on cream paper: a very long one with a dark end, and a very short one that is entirely bright."),
    ("sc15", "s13", "NONE", "A long ribbon of squares where the final square glows noticeably larger and brighter than all the others."),
    ("sc16", "s14", "DIANA", "The girl pauses with her head tilted, one hand raised thoughtfully, as if asking herself a careful question."),
    ("sc17", "s15", "NONE", "A long ribbon of squares on cream paper, all of them gently lighting up again one after another from left to right, warm and full."),
    ("sc18", "s15", "DIANA", "The girl asleep in bed with a small contented smile, the lamp low, warm and peaceful."),
]

per = {}
for _, sid, _, _ in spec:
    per[sid] = per.get(sid, 0) + 1
missing = [s["id"] for s in sections if s["id"] not in per]
if missing:
    raise SystemExit(f"scene coverage gap for sections {missing}")
print(f"scene coverage ok: all {len(sections)} sections mapped", flush=True)

sec_map = {s["id"]: s for s in sections}
scenes, seen = [], {}
for scid, sid, who, desc in spec:
    s = sec_map[sid]
    span = s["end_seconds"] - s["start_seconds"]
    n = per[sid]
    i = seen.get(sid, 0)
    seen[sid] = i + 1
    scenes.append({"id": scid, "type": "generated", "script_section_id": sid,
                   "start_seconds": round(s["start_seconds"] + span * i / n, 3),
                   "end_seconds": round(s["start_seconds"] + span * (i + 1) / n, 3),
                   "description": desc,
                   "narrative_role": "deliver_payload" if scid in ("sc8", "sc10", "sc17") else "evidence",
                   "hero_moment": scid in ("sc8", "sc10", "sc17", "sc18"),
                   "transition_in": "cut", "transition_out": "cut",
                   "shot_language": {"shot_size": "wide" if scid in ("sc3", "sc7", "sc17") else "medium",
                                     "camera_movement": "static", "lighting_key": "natural",
                                     "depth_of_field": "medium", "color_temperature": "warm"},
                   "overlay_notes": "No text in the illustration."})

scene_plan = {"version": "1.0", "style_playbook": "custom-atelier-storybook", "scenes": scenes,
              "metadata": {
                  "character_lock": "Diana: a girl of eight, Vietnamese-Australian, straight black shoulder-length hair with a soft fringe, warm light skin, dark almond eyes, round friendly face, mustard-yellow knitted jumper, denim pinafore dress, red canvas shoes. Identical to films 1 to 6.",
                  "one_child_rule": "Every frame containing a person contains exactly one child.",
                  "device_lock": "A long ribbon of many small squares is all the minutes. Bright squares are remembered, pale ones are not. Exactly two get kept. Squares are never counted or numbered.",
                  "style_lock": "Unchanged from films 1 to 6.",
                  "scene_count": len(scenes),
                  "section_coverage": "All fifteen script sections mapped, asserted before generation.",
                  "generation_order": "All eighteen generated, then reviewed on one contact sheet before any render."}}
validate(scene_plan, "scene_plan")

registry.discover()
img = registry._tools["google_imagen"]
tts = registry._tools["elevenlabs_tts"]

DIANA = ("The girl is eight years old, Vietnamese-Australian, with straight black shoulder-length hair and a soft "
         "fringe, warm light skin, dark almond-shaped eyes and a round friendly face. She wears a mustard-yellow "
         "knitted jumper, a denim pinafore dress and red canvas shoes.")
STYLE = ("Children's picture-book illustration, soft gouache painting, plain warm cream paper background with "
         "visible paper grain, soft pencil linework, rounded organic shapes, muted warm palette, flat 2D storybook "
         "art, not 3D, no text, no lettering, no words, no numbers, no digits.")
ONE = "EXACTLY ONE CHILD in the frame, a single child alone. Do not draw two children."
NOPE = ("There are NO people and NO animals at all in this picture. The background is plain empty cream paper "
        "with no scenery and no decorative shapes.")

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
    parts = [STYLE] + ([ONE, DIANA] if WHO[sid] == "DIANA" else [NOPE]) + [by_id[sid]["description"]]
    ok, err = False, None
    for _ in (1, 2, 3):
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
         "titles": [{"kind": "title", "text": "The Holiday You Remember",
                     "startSec": round(last["startSec"] + 1.0, 3),
                     "durSec": round(max(2.0, min(8.0, last["durSec"] - 1.0)), 3)}]}
(PROJ / "composition").mkdir(parents=True, exist_ok=True)
json.dump(props, open(PROJ / "composition/props.json", "w", encoding="utf-8"), indent=2)

print(f"\nDONE images_failed={img_fail} narration_failed={aud_fail}")
print(f"total {TOTAL}s ({int(TOTAL//60)}m {TOTAL%60:.1f}s) frames={props['durationInFrames']} scenes={len(pscenes)} captions={len(captions)}")
sys.exit(0 if not img_fail and not aud_fail else 1)
