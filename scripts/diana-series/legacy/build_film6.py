"""One-shot: build film 6, It'll Only Take Five Minutes (planning fallacy + premortem)."""
import json
import re
import subprocess
import sys
from pathlib import Path

import jsonschema

from tools.tool_registry import registry

SLUG = "diana-planning"
PROJ = Path("projects") / SLUG
(PROJ / "artifacts").mkdir(parents=True, exist_ok=True)


def validate(obj, name):
    schema = json.load(open(f"schemas/artifacts/{name}.schema.json", encoding="utf-8"))
    jsonschema.validate(obj, schema)
    json.dump(obj, open(PROJ / f"artifacts/{name}.json", "w", encoding="utf-8"), indent=2)
    print(f"{name} SCHEMA-VALID", flush=True)


research = {
    "version": "1.0",
    "topic": "The planning fallacy and the premortem from Thinking, Fast and Slow, told for an 8-year-old as why everything takes longer than she says",
    "research_date": "2026-09-09",
    "research_summary": (
        "Film 6 of the series. Chapters 23 and 24. The inside view builds a forecast from the details of the "
        "case at hand and lands near a best case; the outside view asks what happened in the reference class of "
        "similar completed cases. People who possess both still forecast from the inside, and the planning "
        "fallacy is the systematic result. Kahneman's corrective is reference class forecasting, which for a "
        "child reduces to one usable instruction: do not guess, remember. Chapter 24 adds the premortem, which "
        "suits a child unusually well because it is a game rather than a discipline."
    ),
    "landscape": {
        "existing_content": [
            {"title": "Children's homework and organisation guidance", "url": "https://www.scholastic.com/parents/family-life/social-emotional-learning/development-milestones/emotional-lives-8-10-year-olds.html",
             "source": "web", "angle": "Use a timer, break tasks up",
             "what_it_covers": "Techniques for doing the work, never why the estimate was wrong"},
            {"title": "Jane the Brain (NIMH)", "url": "https://www.nimh.nih.gov/get-involved/science-education/video-series-jane-the-brain",
             "source": "government site", "angle": "Coping with frustration",
             "what_it_covers": "The feeling of running out of time, not the forecasting error underneath it"},
            {"title": "The Decision Lab - System 1 and System 2", "url": "https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking",
             "source": "reference site", "angle": "Adult reference explainer",
             "what_it_covers": "Planning fallacy explained through construction projects and software budgets"}
        ],
        "saturated_angles": ["Timers, checklists and homework routines",
                             "Adult megaproject and budget-overrun examples"],
        "underserved_gaps": [
            "Explaining that the estimate was a best case, not a lie or a character flaw",
            "Reference class forecasting reduced to remember instead of guess",
            "The premortem given to a child as a game they can actually play"
        ]
    },
    "data_points": [
        {"claim": "The inside view builds a forecast from the details of the present case and lands near a best case, ignoring the ways things usually go wrong.",
         "source_url": "https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking",
         "source_name": "Thinking, Fast and Slow, Ch 23", "credibility": "secondary_source",
         "surprise_factor": "counterintuitive", "usable_as": "core concept spine"},
        {"claim": "The outside view asks what actually happened in similar completed cases, and people who possess both views still forecast from the inside.",
         "source_url": "https://www.sparknotes.com/lit/thinking-fast-and-slow/section1/",
         "source_name": "Thinking, Fast and Slow, Ch 23", "credibility": "secondary_source",
         "surprise_factor": "notable", "usable_as": "the corrective, expressed as remember rather than guess"},
        {"claim": "The premortem projects forward to a declared failure and asks for its history, which legitimises doubt and surfaces suppressed risks.",
         "source_url": "https://www.sparknotes.com/lit/thinking-fast-and-slow/section1/",
         "source_name": "Thinking, Fast and Slow, Ch 24", "credibility": "secondary_source",
         "surprise_factor": "surprising", "usable_as": "the second tool, given as a game"},
        {"claim": "By age 8 to 9 children regulate thinking through explicit strategies, so remember-instead-of-guess and a pretend-it-failed game are both usable.",
         "source_url": "https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/bjep.12305",
         "source_name": "Pennequin et al., British Journal of Educational Psychology (2020)",
         "credibility": "primary_source", "surprise_factor": "expected",
         "usable_as": "justifies giving two tools rather than one"}
    ],
    "audience_insights": {
        "knowledge_level": "Age 8. Has seen films 1 to 5 and owns fast one, story machine, memory shelf, separate boxes and the bouncing dot.",
        "common_questions": [
            "Why does everything take longer than I said?",
            "Why do I always run out of time?",
            "Am I just bad at time?"
        ],
        "misconceptions": [
            {"myth": "I said five minutes because I was not paying attention",
             "reality": "You genuinely believed it. You timed a smooth imaginary version of the job.", "source": "Ch 23"},
            {"myth": "Next time I will just try to be more realistic",
             "reality": "Trying harder from the inside does not work. You have to look at what actually happened before.", "source": "Ch 23"},
            {"myth": "Being slow means I am bad at things",
             "reality": "You are good at imagining things going well. That is a different problem and a fixable one.", "source": "Ch 23"}
        ],
        "pain_points": [
            "Being told off for an estimate she believed when she gave it",
            "Feeling disorganised rather than mis-calibrated"
        ]
    },
    "angles_discovered": [
        {"name": "The Film In Your Head", "type": "narrative",
         "hook": "Five minutes, she said. It took forty. And she was not lying.",
         "why_now": "A daily experience at this age, and the smooth-imaginary-version idea is easy to draw and easy to hold.",
         "grounded_in": ["Ch 23 inside view"]},
        {"name": "Do Not Guess, Remember", "type": "evergreen",
         "hook": "How long did it take last Tuesday? And the Tuesday before?",
         "why_now": "Reference class forecasting compressed into one instruction a child can carry out unaided.",
         "grounded_in": ["Ch 23 outside view and reference class forecasting"]},
        {"name": "Pretend It Went Wrong", "type": "contrarian",
         "hook": "Imagine it is finished and it went horribly. Now say why.",
         "why_now": "The premortem works as a game rather than a discipline, which is exactly why it suits a child.",
         "grounded_in": ["Ch 24 premortem"]}
    ],
    "expert_voices": [
        {"name": "Daniel Kahneman", "title_or_affiliation": "Nobel laureate, author",
         "position": "Forecasts made from the inside view land near a best case; the outside view and the premortem are the correctives.",
         "source_url": "https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking",
         "contrarian": False}
    ],
    "sources": [
        {"url": "https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking",
         "title": "System 1 and System 2 Thinking - The Decision Lab", "used_for": "Inside and outside view", "reliability": "secondary"},
        {"url": "https://www.sparknotes.com/lit/thinking-fast-and-slow/section1/",
         "title": "Thinking, Fast and Slow Summary", "used_for": "Chapters 23 and 24", "reliability": "secondary"},
        {"url": "https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/bjep.12305",
         "title": "Metacognition and emotional regulation in children 8 to 12", "used_for": "Age appropriateness of two tools", "reliability": "primary"},
        {"url": "https://www.nimh.nih.gov/get-involved/science-education/video-series-jane-the-brain",
         "title": "Jane the Brain - NIMH", "used_for": "Format benchmark", "reliability": "primary"},
        {"url": "https://www.scholastic.com/parents/family-life/social-emotional-learning/development-milestones/emotional-lives-8-10-year-olds.html",
         "title": "Social and Emotional Lives of 8- to 10-Year-Olds", "used_for": "Homework and time pressure at this age", "reliability": "secondary"}
    ],
    "metadata": {
        "series": "Film 6 of 18.",
        "excluded_claims": [
            "Megaproject and budget-overrun statistics, the standard adult framing.",
            "Any suggestion that she is disorganised or lazy.",
            "Anything from the priming or ego-depletion chapters."
        ]
    }
}
validate(research, "research_brief")

proposal = {
    "version": "1.0",
    "concept_options": [
        {"id": "c1", "title": "It'll Only Take Five Minutes",
         "hook": "How long will your homework take? Five minutes. It took forty. And she was not lying.",
         "narrative_structure": "story",
         "visual_approach": "The established storybook world. New device: two paths on cream paper, a clean straight arrow for the job she imagined and a long looping tangled path with snags for the job as it happened, then three small worn paper slips for what really happened the last three times.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old, watched with her dad",
         "target_platform": "generic", "target_duration_seconds": 185,
         "key_points": ["The estimate was sincere; she timed a smooth imaginary version",
                        "Real jobs always contain a something, and never the same something",
                        "The fix is not to try harder but to look at the last three times",
                        "The premortem: pretend it went badly and say why",
                        "She is not bad at time, she is good at imagining things going well"],
         "core_message": "You did not lie about five minutes. You timed a film of everything going perfectly. To guess better, do not guess, remember.",
         "cta": "Before you say how long something will take, ask how long it took the last three times.",
         "tone": "Warm, wry, entirely on her side.",
         "why_this_works": "A daily experience, it removes an accusation she is used to receiving, and it hands her two tools she can use unaided.",
         "grounded_in": ["Ch 23 inside and outside view", "Ch 24 premortem"]},
        {"id": "c2", "title": "Do Not Guess, Remember",
         "hook": "How long did it take last Tuesday?",
         "narrative_structure": "tutorial",
         "visual_approach": "Three worn paper slips laid side by side.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 120,
         "key_points": ["Guessing uses imagination", "Remembering uses evidence", "Three past times beat one feeling"],
         "core_message": "Look backwards, not forwards.", "cta": "Check the last three times.", "tone": "Practical",
         "why_this_works": "The most usable instruction but an instruction without a story, so it becomes the third act of c1.",
         "grounded_in": ["Ch 23 reference class forecasting"]},
        {"id": "c3", "title": "Pretend It Went Wrong",
         "hook": "It is finished, and it went horribly. Now tell me why.",
         "narrative_structure": "tutorial",
         "visual_approach": "A finished-but-disastrous scene, then three small causes floating out of it.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 120,
         "key_points": ["Imagining failure is easier than predicting it", "Three causes arrive instantly", "Fix those now"],
         "core_message": "Look at the disaster before it happens.", "cta": "Play the game before anything big.",
         "tone": "Playful", "why_this_works": "A delightful game for a child, but it needs the planning error established first, so it becomes the fourth act of c1.",
         "grounded_in": ["Ch 24 premortem"]}
    ],
    "selected_concept": {
        "concept_id": "c1",
        "rationale": "c1 opens on a daily accusation, explains why the estimate was sincere, and hands over both correctives in turn. The other two are the tools without the exoneration that makes a child willing to use them.",
        "modifications": ["All production decisions carry over from films 1 to 5",
                          "New device: the straight imagined path against the tangled real one",
                          "Two tools this film rather than one"]
    },
    "production_plan": {
        "pipeline": "animated-explainer", "playbook": "custom-atelier-storybook",
        "renderer_family": "explainer-teacher", "render_runtime": "remotion", "composition_mode": "atelier",
        "delivery_promise": {"promise_type": "teacher_explainer", "motion_required": False, "source_required": False,
                             "tone_mode": "intimate and wry, a bedtime storybook read aloud",
                             "quality_floor": "presentable", "approved_fallback": "still_led"},
        "art_direction": "Unchanged series house style. New device: a clean straight arrow for the imagined job and a long looping tangled path with snags for the real one, plus three small worn paper slips for the past times.",
        "taste_profile": {
            "design_read": "The same bedtime picture book, five chapters on",
            "visual_variance": 8, "motion_intensity": 3, "information_density": 2,
            "palette_discipline": "Unchanged. Cream ground, muted warm palette, gold and blue as the only accents.",
            "layout_variation": "Each scene composed for its beat. The two paths give this film its geometry.",
            "reference_strategy": "Series continuity only.",
            "anti_patterns": ["clocks with readable numerals, since the model cannot draw reliable digits",
                              "charts, axes or gridlines",
                              "a clause pasted into prompts it does not belong to",
                              "implying she is lazy, slow or disorganised"],
            "quality_gates": ["Contact sheet of all illustrations reviewed before render",
                              "Every script section has at least one scene, asserted at build time",
                              "No numerals anywhere in any illustration"]
        },
        "music_source": {"source_type": "ai_generated", "provider": "reused from film 1 (Google Lyria)",
                         "mood_direction": "The same bed as films 1 to 5.", "estimated_cost_usd": 0.0},
        "voice_selection": {"provider": "elevenlabs", "voice_id": "JBFqnCBsd6RMkjVDRZzb",
                            "rationale": "The same warm storyteller voice as films 1 to 5.",
                            "estimated_cost_usd": 0.85,
                            "delivery_style": "warm parent reading a bedtime story, wry and entirely on her side",
                            "pacing_policy": "Roughly 110 words per minute with three genuine silences.",
                            "sample_approval_required": False},
        "stages": [
            {"stage": "script", "approach": "Around 400 words at an 8-year-old listening level, three pause beats.", "tools": []},
            {"stage": "scene_plan", "approach": "Eighteen scenes covering all fifteen sections, the two paths carrying the middle.", "tools": []},
            {"stage": "assets", "approach": "Same image model and character lock, same voice, music reused.",
             "tools": [{"tool_name": "google_imagen", "role": "illustration", "available": True},
                       {"tool_name": "elevenlabs_tts", "role": "narration", "available": True}]},
            {"stage": "edit", "approach": "Timeline rebuilt from measured narration durations.", "tools": []},
            {"stage": "compose", "approach": "Atelier Remotion render reusing the series composition.",
             "tools": [{"tool_name": "video_compose", "role": "render", "available": True}]}
        ],
        "quality_tradeoffs": [
            {"tradeoff": "Two tools in one film versus the usual one",
             "recommendation": "Two", "quality_impact": "The two correctives are complementary and short, and the premortem is a game rather than another rule."},
            {"tradeoff": "Showing clocks and times versus keeping it qualitative",
             "recommendation": "No clocks with numerals", "quality_impact": "The image model cannot draw reliable digits. Times are spoken, never drawn."}
        ],
        "alternative_paths": [
            {"description": "Planning fallacy only, premortem deferred", "total_cost_usd": 1.57, "quality_level": "standard"},
            {"description": "Reuse everything from films 1 to 5", "total_cost_usd": 1.57, "quality_level": "standard"}
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
                 "user_notes": "User replied next, selecting film 6, under a standing instruction to fix defects without asking."},
    "metadata": {"series_position": "6 of 18",
                 "carried_over": ["character lock", "style lock", "voice", "runtime", "composition mode", "music bed"],
                 "new_this_film": ["straight versus tangled path device", "two tools instead of one"],
                 "lesson_applied": "Scene coverage asserted before generation; no numerals requested in any illustration."}
}
validate(proposal, "proposal_packet")

S = [
    ("s1", "Five minutes",
     "How long will your homework take, Diana? Five minutes. It took forty.",
     'How long will your homework take, Diana? <break time="0.6s"/> Five minutes. <break time="0.7s"/> It took forty.',
     1.2, "measured", "wry", ["forty"], "Light and affectionate. The joke is gentle, never mocking."),
    ("s2", "She was not lying",
     "And here is the important bit. She was not lying. She properly, honestly believed it.",
     'And here is the important bit. <break time="0.5s"/> She was not lying. <break time="0.5s"/> She properly, honestly believed it.',
     1.4, "slow", "tender", ["believed"], "This is the exoneration. It must sound completely sincere."),
    ("s3", "The perfect version",
     "Because when you work out how long something will take, you picture it going perfectly.",
     'Because when you work out how long something will take, <break time="0.4s"/> you picture it going perfectly.',
     1.2, "measured", "curious", ["perfectly"], "The explanation opens."),
    ("s4", "Nothing goes wrong in the film",
     "No lost pencil. No missing sheet. Nobody talking to you. Nothing spilled. Nothing forgotten.",
     'No lost pencil. <break time="0.3s"/> No missing sheet. <break time="0.3s"/> Nobody talking to you. <break time="0.3s"/> Nothing spilled. <break time="0.3s"/> Nothing forgotten.',
     1.2, "conversational", "rolling", ["nothing"], "A list that gathers speed and gets funnier as it goes."),
    ("s5", "Timing the film",
     "Your brain makes a tiny film of the job going smoothly, and then it times the film.",
     'Your brain makes a tiny film of the job going smoothly, <break time="0.5s"/> and then it times the film.',
     1.4, "slow", "gentle", ["film"], "The hinge. Slow right down."),
    ("s6", "Real jobs are not the film",
     "But real jobs are never the film. There is always a something.",
     'But real jobs are never the film. <break time="0.5s"/> There is always a something.',
     1.2, "measured", "steady", ["always"], "Plain and calm."),
    ("s7", "Never the same something",
     "And it is never the same something twice. That is exactly why you cannot see it coming.",
     'And it is never the same something twice. <break time="0.5s"/> That is exactly why you cannot see it coming. <break time="2.5s"/>',
     2.5, "measured", "steady", ["never"], "Pause beat one. She should recognise the pattern."),
    ("s8", "The question",
     "So here is a much better question. How long did it take last Tuesday?",
     'So here is a much better question. <break time="0.5s"/> How long did it take last Tuesday? <break time="2.5s"/>',
     2.5, "measured", "curious", ["Tuesday"], "Pause beat two. Let her actually try to remember."),
    ("s9", "And the one before",
     "And the Tuesday before that? And the one before that?",
     'And the Tuesday before that? <break time="0.4s"/> And the one before that?',
     1.2, "measured", "curious", ["before"], "Gentle insistence."),
    ("s10", "That is the answer",
     "That is your answer. Not the little film in your head. The three real times it actually took.",
     'That is your answer. <break time="0.5s"/> Not the little film in your head. <break time="0.5s"/> The three real times it actually took.',
     1.4, "slow", "steady", ["three"], "Land the corrective firmly."),
    ("s11", "Grown-ups too",
     "And grown-ups are worse at this than you are. Much worse. They do it with bridges and kitchens and whole houses.",
     'And grown-ups are worse at this than you are. <break time="0.4s"/> Much worse. <break time="0.5s"/> They do it with bridges and kitchens and whole houses.',
     1.4, "measured", "wry", ["worse"], "She should enjoy this line."),
    ("s12", "The first trick",
     "So here is your sixth trick. When you guess how long something will take, do not guess. Remember.",
     'So here is your sixth trick. <break time="0.5s"/> When you guess how long something will take, <break time="0.4s"/> do not guess. <break time="0.5s"/> Remember.',
     1.4, "measured", "encouraging", ["Remember"], "Bright and clear."),
    ("s13", "The second trick",
     "And here is a second one, for something big. Pretend it is already finished, and it went horribly wrong. Then ask yourself why.",
     'And here is a second one, for something big. <break time="0.5s"/> Pretend it is already finished, <break time="0.4s"/> and it went horribly wrong. <break time="0.5s"/> Then ask yourself why.',
     1.4, "measured", "playful", ["horribly"], "Make it sound like a game, because it is one."),
    ("s14", "Three things instantly",
     "You will think of three things straight away. You always do. And those three things are the ones to sort out now, while there is still time.",
     'You will think of three things straight away. <break time="0.4s"/> You always do. <break time="0.5s"/> And those three things are the ones to sort out now, <break time="0.4s"/> while there is still time. <break time="2.5s"/>',
     2.5, "measured", "encouraging", ["three"], "Pause beat three. She should try it on something real."),
    ("s15", "Landing",
     "So you are not bad at time, Diana. You are just very, very good at imagining things going well. Which is a lovely thing to be good at. It just needs checking.",
     'So you are not bad at time, Diana. <break time="0.5s"/> You are just very, very good at imagining things going well. <break time="0.5s"/> Which is a lovely thing to be good at. <break time="0.4s"/> It just needs checking.',
     0.0, "slow", "warm", ["not bad"], "The reframe. End warm, then stop."),
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
    "version": "1.0", "title": "It'll Only Take Five Minutes",
    "total_duration_seconds": round(t, 2),
    "voice_performance": {
        "performance_intent": "The same parent and child, five chapters on. Affectionate and wry, and a defence of her rather than a correction. The narrator is plainly worse at this than she is.",
        "pacing_profile": "contemplative",
        "energy_curve": "Wry at the opening. Sincere and warm at she was not lying. Rolling and comic through the list. Slowest at timing the film. Playful at the premortem. Warmest at the reframe.",
        "pause_policy": "Three genuine silences: after never the same something, after how long did it take last Tuesday, and after the three things to sort out now.",
        "sample_section_id": "s2",
        "provider_notes": {
            "all": "Roughly 110 words per minute. Section s2 is the exoneration and the sample section.",
            "elevenlabs": "Same voice as films 1 to 5, George. Stability 0.75, similarity 0.9, style 0.15, speed 0.9.",
            "human_recording": "Section 11 about grown-ups being worse should sound like an admission, not a joke at anyone else's expense."
        }
    },
    "sections": sections,
    "metadata": {
        "series_position": "6 of 18",
        "word_count_approx": sum(len(s["text"].split()) for s in sections),
        "target_wpm": 110,
        "reading_age": "Written for a listener of 8. Planning fallacy, inside view, outside view and premortem never appear as words.",
        "pause_beats": [
            {"section": "s7", "purpose": "She recognises that the obstacle is never the same one"},
            {"section": "s8", "purpose": "She actually tries to remember last Tuesday"},
            {"section": "s14", "purpose": "She tries the premortem on something real"}
        ],
        "grounded_in": {
            "s1_to_s5": "Ch 23, the inside view producing a best-case forecast",
            "s6_to_s7": "Ch 23, unforeseen obstacles that differ every time",
            "s8_to_s11": "Ch 23, the outside view and reference class forecasting",
            "s12_to_s14": "Ch 23 corrective plus Ch 24 premortem",
            "s15": "Reframe grounded in the same chapters, plus Pennequin on strategy instruction"
        },
        "accuracy_guardrails_applied": [
            "The estimate is treated as sincere throughout; the film never implies dishonesty, laziness or disorganisation.",
            "No megaproject or budget statistics.",
            "Times are spoken only, never drawn, because the image model cannot render reliable numerals.",
            "No priming or ego-depletion material."
        ]
    }
}
validate(script, "script")

spec = [
    ("sc1", "s1", "DIANA", "The girl stands in a doorway holding a school bag, answering a question over her shoulder, cheerful and confident."),
    ("sc2", "s1", "DIANA", "The same girl much later at a kitchen table surrounded by scattered papers and pencils, looking tired and surprised, evening light at the window."),
    ("sc3", "s2", "DIANA", "The girl looks directly ahead with an open honest expression, hands turned slightly outward, entirely sincere."),
    ("sc4", "s3", "NONE", "One clean straight arrow drawn confidently from left to right across an empty cream page. Nothing else at all, no obstacles, no scenery."),
    ("sc5", "s4", "NONE", "Four small ordinary objects float separately on cream paper, each with a soft grey cross beside it to show it is absent: a pencil, a paper sheet, a cup, a school folder."),
    ("sc6", "s5", "DIANA", "The girl sits with her chin on her hand, eyes up, a small softly glowing rectangle floating beside her head like a tiny picture playing."),
    ("sc7", "s6", "NONE", "One long looping tangled path winds across a cream page from left to right, with small snags, knots and stumbling points along the way."),
    ("sc8", "s7", "NONE", "A clean short straight arrow drawn above, and a very long looping tangled path drawn below it, on the same cream page for comparison."),
    ("sc9", "s7", "NONE", "Three different small snags drawn separately on cream paper: a tangled knot, a small puddle, and a dropped pencil. Each one different from the others."),
    ("sc10", "s8", "DIANA", "The girl looks upward and to the side, trying hard to remember something, one finger touching her chin."),
    ("sc11", "s9", "NONE", "Three small pieces of torn paper lie in a neat row on cream ground, each slightly creased and worn, like old notes kept from before. Completely blank, no writing."),
    ("sc12", "s10", "DIANA", "The girl holds three small worn paper slips in her hands, looking at them thoughtfully."),
    ("sc13", "s11", "NONE", "A half-finished house with scaffolding around it and a half-finished kitchen beside it, both clearly taking far longer than expected, drawn warmly and comically."),
    ("sc14", "s12", "DIANA", "The girl stands with a small determined smile, holding up one finger as if remembering a rule."),
    ("sc15", "s13", "NONE", "A small scene of cheerful disaster on cream paper: a toppled tower of books, a spilled pot of pencils, a paper aeroplane stuck in a plant. Comic, not distressing."),
    ("sc16", "s14", "NONE", "Three small simple blank cards float upward out of a jumbled heap on cream paper. The cards are completely blank with no writing or letters."),
    ("sc17", "s14", "DIANA", "The girl crouches down and picks up one small blank card from the floor, focused and purposeful."),
    ("sc18", "s15", "DIANA", "The girl sits on a low wall in warm late afternoon light, relaxed and content, her school bag beside her."),
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
        "narrative_role": "deliver_payload" if scid in ("sc6", "sc8", "sc11") else "evidence",
        "hero_moment": scid in ("sc6", "sc8", "sc11", "sc18"),
        "transition_in": "cut", "transition_out": "cut",
        "shot_language": {"shot_size": "wide" if scid in ("sc7", "sc8") else "medium",
                          "camera_movement": "static", "lighting_key": "natural",
                          "depth_of_field": "medium", "color_temperature": "warm"},
        "overlay_notes": "No text in the illustration."
    })

scene_plan = {
    "version": "1.0", "style_playbook": "custom-atelier-storybook", "scenes": scenes,
    "metadata": {
        "character_lock": "Diana: a girl of eight, Vietnamese-Australian, straight black shoulder-length hair with a soft fringe, warm light skin, dark almond eyes, round friendly face, mustard-yellow knitted jumper, denim pinafore dress, red canvas shoes. Identical to films 1 to 5.",
        "one_child_rule": "Every frame containing a person contains exactly one child. No frame in this film shows two children.",
        "device_lock": "A clean straight arrow is the imagined job. A long looping tangled path with snags is the real one. Three small worn blank paper slips are the past times. No numerals appear anywhere.",
        "style_lock": "Unchanged from films 1 to 5.",
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
STYLE = ("Children's picture-book illustration, soft gouache painting, plain warm cream paper background with "
         "visible paper grain, soft pencil linework, rounded organic shapes, muted warm palette, flat 2D storybook "
         "art, not 3D, no text, no lettering, no words, no numbers, no digits, no clock faces.")
ONE = "EXACTLY ONE CHILD in the frame, a single child alone. Do not draw two children."
NOPE = ("There are NO people and NO animals at all in this picture. The background is plain empty cream paper "
        "with no scenery, no landscape and no decorative shapes.")

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
    parts += [ONE, DIANA] if WHO[sid] == "DIANA" else [NOPE]
    parts.append(by_id[sid]["description"])
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
         "titles": [{"kind": "title", "text": "It'll Only Take Five Minutes",
                     "startSec": round(last["startSec"] + 1.0, 3),
                     "durSec": round(max(2.0, min(8.0, last["durSec"] - 1.0)), 3)}]}
(PROJ / "composition").mkdir(parents=True, exist_ok=True)
json.dump(props, open(PROJ / "composition/props.json", "w", encoding="utf-8"), indent=2)

print(f"\nDONE images_failed={img_fail} narration_failed={aud_fail}")
print(f"total {TOTAL}s ({int(TOTAL//60)}m {TOTAL%60:.1f}s) frames={props['durationInFrames']} scenes={len(pscenes)} captions={len(captions)}")
sys.exit(0 if not img_fail and not aud_fail else 1)
