"""One-shot: build film 8, Why Losing Hurts More (loss aversion, negativity dominance)."""
import json
import re
import subprocess
import sys
from pathlib import Path

import jsonschema

from tools.tool_registry import registry

SLUG = "diana-loss-aversion"
PROJ = Path("projects") / SLUG
(PROJ / "artifacts").mkdir(parents=True, exist_ok=True)
DL = "https://thedecisionlab.com/biases/loss-aversion"
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
    "topic": "Loss aversion and negativity dominance from Thinking, Fast and Slow, told for an 8-year-old as why losing weighs about twice as much as winning",
    "research_date": "2026-09-09",
    "research_summary": (
        "Film 8 of the series. Chapters 26 to 28. Losses loom larger than matching gains, with a ratio commonly "
        "measured between 1.5 and 2.5, so the same object felt as a loss hurts roughly twice as much as it "
        "pleases when felt as a gain. Bad events also dominate good ones of equal size, which is why one bad "
        "moment can outweigh a day of small good ones. For a child this explains both why she clings to things "
        "and why a spoiled afternoon feels heavier than it should, and it hands her the endowment-effect "
        "corrective: would I want this if I did not already have it?"
    ),
    "landscape": {
        "existing_content": [
            {"title": "Jane the Brain (NIMH)", "url": NIMH, "source": "government site",
             "angle": "Naming and coping with big feelings",
             "what_it_covers": "Feelings themselves, not why gains and losses are weighed unequally"},
            {"title": "Children's sharing and generosity material", "url": SCH, "source": "web",
             "angle": "Be kind, share your things",
             "what_it_covers": "Treats reluctance to give things up as a character flaw rather than a weighting effect"},
            {"title": "The Decision Lab - Loss Aversion", "url": DL, "source": "reference site",
             "angle": "Adult reference explainer",
             "what_it_covers": "Loss aversion through investing, insurance and gambling framings"}
        ],
        "saturated_angles": ["Sharing is caring and generosity lessons",
                             "Adult money, investing and gambling framings"],
        "underserved_gaps": [
            "Telling a child that holding on tightly is a measurement effect, not greed or ingratitude",
            "Connecting loss aversion to why one bad moment outweighs a whole good day",
            "The would-I-want-it-if-I-did-not-have-it question, given to a child as a usable move"
        ]
    },
    "data_points": [
        {"claim": "Losses loom larger than corresponding gains, with the loss aversion ratio commonly measured between 1.5 and 2.5.",
         "source_url": DL, "source_name": "Thinking, Fast and Slow, Ch 26",
         "credibility": "secondary_source", "surprise_factor": "surprising",
         "usable_as": "the about-twice figure and the see-saw device"},
        {"claim": "Outcomes are felt as gains or losses relative to a reference point, not as absolute states.",
         "source_url": SN, "source_name": "Thinking, Fast and Slow, Ch 25 and 26",
         "credibility": "secondary_source", "surprise_factor": "counterintuitive",
         "usable_as": "why the same star feels different found versus dropped"},
        {"claim": "Bad events dominate good ones of equal magnitude; negativity gets processed faster and weighs more.",
         "source_url": SN, "source_name": "Thinking, Fast and Slow, Ch 28",
         "credibility": "secondary_source", "surprise_factor": "expected",
         "usable_as": "why one bad thing outweighs a good day"},
        {"claim": "Ownership converts a potential gain into a felt loss, so selling prices run far above buying prices.",
         "source_url": DL, "source_name": "Thinking, Fast and Slow, Ch 27",
         "credibility": "secondary_source", "surprise_factor": "counterintuitive",
         "usable_as": "justifies the would-I-want-it question"},
        {"claim": "By age 8 to 9 children can reflect on their own feelings explicitly, so a self-directed question is usable.",
         "source_url": PQ, "source_name": "Pennequin et al., British Journal of Educational Psychology (2020)",
         "credibility": "primary_source", "surprise_factor": "expected",
         "usable_as": "age appropriateness of both tools"}
    ],
    "audience_insights": {
        "knowledge_level": "Age 8. Has seen films 1 to 7 and owns the fast one, the story machine, the memory shelf, separate boxes, the bouncing dot, remember-do-not-guess and protect-the-ending.",
        "common_questions": [
            "Why do I mind losing things so much?",
            "Why did one bad thing spoil the whole day again?",
            "Why is it so hard to give something away even when I never play with it?"
        ],
        "misconceptions": [
            {"myth": "Not wanting to give something up means I am greedy",
             "reality": "Giving up is weighed on a heavier scale than getting. It is a measurement effect, not a character flaw.",
             "source": "Ch 26 and 27"},
            {"myth": "Winning and losing the same thing should cancel out",
             "reality": "They do not. Losing weighs roughly twice as much.", "source": "Ch 26"},
            {"myth": "If one bad thing ruins my day I am being ungrateful",
             "reality": "Bad events dominate good ones of the same size. The scale is built that way.", "source": "Ch 28"}
        ],
        "pain_points": ["Feeling ashamed of not wanting to give something up",
                        "A single bad moment outweighing a day of good ones"]
    },
    "angles_discovered": [
        {"name": "The See-Saw That Will Not Balance", "type": "narrative",
         "hook": "Finding one is nice. Losing one is horrible. They do not weigh the same.",
         "why_now": "A see-saw is a thing every 8-year-old has physically felt, so the asymmetry lands in the body rather than as an idea.",
         "grounded_in": ["Ch 26 loss aversion ratio"]},
        {"name": "The One You Carry Home", "type": "evergreen",
         "hook": "A day full of good little things, then one bad one, and that is the one you carry home.",
         "why_now": "Names an experience she has had repeatedly and has probably been told she is being ungrateful about.",
         "grounded_in": ["Ch 28 negativity dominance"]},
        {"name": "Would I Want It If I Did Not Have It", "type": "contrarian",
         "hook": "Ask whether you would choose it today, with no history.",
         "why_now": "The endowment-effect corrective, and the only actionable move in this territory a child can actually run.",
         "grounded_in": ["Ch 27 endowment effect"]}
    ],
    "expert_voices": [
        {"name": "Daniel Kahneman", "title_or_affiliation": "Nobel laureate, author",
         "position": "Losses loom larger than gains, and bad dominates good of equal size.",
         "source_url": DL, "contrarian": False}
    ],
    "sources": [
        {"url": DL, "title": "Loss Aversion - The Decision Lab", "used_for": "Ratio and framing", "reliability": "secondary"},
        {"url": SN, "title": "Thinking, Fast and Slow Summary", "used_for": "Chapters 25 to 28", "reliability": "secondary"},
        {"url": PQ, "title": "Metacognition and emotional regulation in children 8 to 12", "used_for": "Age appropriateness", "reliability": "primary"},
        {"url": NIMH, "title": "Jane the Brain - NIMH", "used_for": "Format benchmark", "reliability": "primary"},
        {"url": SCH, "title": "Social and Emotional Lives of 8- to 10-Year-Olds", "used_for": "Sharing and self-judgement at this age", "reliability": "secondary"}
    ],
    "metadata": {
        "series": "Film 8 of 18.",
        "excluded_claims": [
            "The fourfold pattern and decision weights, which need probability and belong in a later film.",
            "Any framing of loss aversion as an evolutionary just-so story stated as settled fact; the film says only that the setting is old and once mattered more.",
            "Anything from the priming or ego-depletion chapters."],
        "corrected_plan_note": ("Film 8 was previously announced as a what-you-see-is-all-there-is film. That is "
                                "already film 2, The Story Machine, grounded in Ch 7 including the never-registers-"
                                "what-is-missing beat. Loss aversion replaces it as the next uncovered territory.")}
}
validate(research, "research_brief")

proposal = {
    "version": "1.0",
    "concept_options": [
        {"id": "c1", "title": "Why Losing Hurts More",
         "hook": "Imagine you find a little gold star on the path. Now imagine you drop one you already had.",
         "narrative_structure": "story",
         "visual_approach": "The established storybook world. New device: a plain wooden see-saw on cream paper carrying one small star at each end. It never balances. The losing end goes down and stays down.",
         "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old, watched with her dad",
         "target_platform": "generic", "target_duration_seconds": 155,
         "key_points": ["The same object feels different found than dropped",
                        "Losing weighs about twice as much as getting",
                        "Which is why holding on tightly is not greed",
                        "One bad thing outweighs a day of good ones for the same reason",
                        "The moves: ask whether you would want it if you did not have it, and put the good things back on the see-saw"],
         "core_message": "Your see-saw is built with a heavy end. That is not a fault in you. You just do not have to let the heavy end be the only end you can see.",
         "cta": "When you cannot bear to lose something, ask whether you would want it if you did not already have it.",
         "tone": "Warm, matter-of-fact, forgiving.",
         "why_this_works": "It removes shame from something she has been told off for, and it explains a second thing she already feels, which makes the idea earn its keep twice.",
         "grounded_in": ["Ch 26 loss aversion", "Ch 27 endowment effect", "Ch 28 negativity dominance"]},
        {"id": "c2", "title": "The One You Carry Home",
         "hook": "A whole good day, one bad thing, and that is the one you take to bed.",
         "narrative_structure": "comparison",
         "visual_approach": "A row of small warm suns across the page with a single dark cloud drawn far larger than any of them.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 120,
         "key_points": ["Bad outweighs good of the same size", "It is not ingratitude", "Say the good ones out loud"],
         "core_message": "Bad weighs more.", "cta": "Put the good things back.", "tone": "Gentle",
         "why_this_works": "True and useful, but it is the consequence rather than the mechanism, so it becomes the middle of c1.",
         "grounded_in": ["Ch 28 negativity dominance"]},
        {"id": "c3", "title": "Would You Want It?",
         "hook": "If you did not already have it, would you choose it today?",
         "narrative_structure": "tutorial",
         "visual_approach": "An open empty hand, palm up, on cream paper.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 100,
         "key_points": ["Ownership inflates value", "Ask the question fresh", "Decide from today"],
         "core_message": "Choose it again or let it go.", "cta": "Ask the question.", "tone": "Practical",
         "why_this_works": "The most actionable piece, but an instruction with no explanation behind it, so it becomes the payoff of c1.",
         "grounded_in": ["Ch 27 endowment effect"]}
    ],
    "selected_concept": {
        "concept_id": "c1",
        "rationale": "c1 opens on a single object felt two ways, which is the cleanest possible demonstration of a reference point, then uses the see-saw to carry both the clinging and the spoiled-day consequences. The others are each one third of it.",
        "modifications": ["All production decisions carry over from films 1 to 7",
                          "New device: the wooden see-saw that will not balance",
                          "Scene coverage asserted before generation",
                          "Render must use video_compose operation 'render', not 'remotion_render'"]},
    "production_plan": {
        "pipeline": "animated-explainer", "playbook": "custom-atelier-storybook",
        "renderer_family": "explainer-teacher", "render_runtime": "remotion", "composition_mode": "atelier",
        "delivery_promise": {"promise_type": "teacher_explainer", "motion_required": False, "source_required": False,
                             "tone_mode": "intimate and forgiving, a bedtime storybook read aloud",
                             "quality_floor": "presentable", "approved_fallback": "still_led"},
        "art_direction": "Unchanged series house style. New device: a plain wooden see-saw carrying one small star at each end, which never balances.",
        "taste_profile": {"design_read": "The same bedtime picture book, seven chapters on",
                          "visual_variance": 8, "motion_intensity": 3, "information_density": 2,
                          "palette_discipline": "Unchanged. Cream ground, muted warm palette, gold and grey accents.",
                          "layout_variation": "Each scene composed for its beat. The see-saw gives this film its geometry.",
                          "reference_strategy": "Series continuity only.",
                          "anti_patterns": ["asking the image model for an exact count of anything",
                                            "two children in one frame",
                                            "numerals, scales with markings, or measuring dials",
                                            "faces or patterns drawn inside the star tokens",
                                            "implying she is greedy, or that she should simply be more grateful"],
                          "quality_gates": ["Contact sheet reviewed before render",
                                            "Every script section mapped to a scene, asserted at build time",
                                            "ffprobe the rendered file against the props frame count before encoding"]},
        "music_source": {"source_type": "ai_generated", "provider": "reused from film 1 (Google Lyria)",
                         "mood_direction": "The same bed as films 1 to 7.", "estimated_cost_usd": 0.0},
        "voice_selection": {"provider": "elevenlabs", "voice_id": "JBFqnCBsd6RMkjVDRZzb",
                            "rationale": "The same warm storyteller voice as films 1 to 7.",
                            "estimated_cost_usd": 0.85,
                            "delivery_style": "warm parent reading a bedtime story, forgiving rather than instructive",
                            "pacing_policy": "Roughly 110 words per minute with three genuine silences.",
                            "sample_approval_required": False},
        "stages": [
            {"stage": "script", "approach": "Around 330 words at an 8-year-old listening level, three pause beats.", "tools": []},
            {"stage": "scene_plan", "approach": "Eighteen scenes covering all fifteen sections, the see-saw carrying the spine.", "tools": []},
            {"stage": "assets", "approach": "Same image model and character lock, same voice, music reused.",
             "tools": [{"tool_name": "google_imagen", "role": "illustration", "available": True},
                       {"tool_name": "elevenlabs_tts", "role": "narration", "available": True}]},
            {"stage": "edit", "approach": "Timeline rebuilt from measured narration durations.", "tools": []},
            {"stage": "compose", "approach": "Atelier Remotion render via video_compose operation 'render'.",
             "tools": [{"tool_name": "video_compose", "role": "render", "available": True}]}
        ],
        "quality_tradeoffs": [
            {"tradeoff": "Saying about twice versus giving no figure",
             "recommendation": "About twice",
             "quality_impact": "The measured ratio runs 1.5 to 2.5. About twice is honest, memorable and spoken rather than shown, so no numeral reaches an illustration."},
            {"tradeoff": "Explaining why the setting exists versus leaving it unexplained",
             "recommendation": "One gentle sentence",
             "quality_impact": "Saying only that the setting is old and once mattered more avoids stating an evolutionary story as settled fact while still answering the obvious child question."}
        ],
        "alternative_paths": [
            {"description": "Negativity dominance only, endowment tool deferred", "total_cost_usd": 1.57, "quality_level": "standard"},
            {"description": "Reuse everything from films 1 to 7", "total_cost_usd": 1.57, "quality_level": "standard"}
        ]
    },
    "cost_estimate": {"total_estimated_usd": 1.57, "budget_cap_usd": 2.5, "budget_verdict": "within_budget",
                      "line_items": [
                          {"tool": "google_imagen", "operation": "storybook illustrations", "quantity": 18,
                           "estimated_usd": 0.72, "notes": "0.04 USD each"},
                          {"tool": "elevenlabs_tts", "operation": "narration", "quantity": 1,
                           "estimated_usd": 0.85, "notes": "Zero if Daniel records it"},
                          {"tool": "video_compose", "operation": "local render", "quantity": 1,
                           "estimated_usd": 0.0, "notes": "No API cost"}],
                      "savings_options": ["Daniel records the narration", "Music already reused at no cost"]},
    "approval": {"status": "approved", "approved_budget_usd": 2.5,
                 "user_notes": "User replied next, selecting the next film in the approved series, under a standing instruction to fix defects without asking."},
    "metadata": {"series_position": "8 of 18",
                 "carried_over": ["character lock", "style lock", "voice", "runtime", "composition mode", "music bed"],
                 "new_this_film": ["the wooden see-saw that will not balance"],
                 "chapters_now_covered": "1-3, 7, 12-13, 17, 23-24, 26-28, 35-36"}
}
validate(proposal, "proposal_packet")

S = [
    ("s1", "The star on the path",
     "Imagine you are walking home, Diana, and there on the path is a little gold star. Nobody's. Yours now.",
     'Imagine you are walking home, Diana, <break time="0.4s"/> and there on the path is a little gold star. <break time="0.5s"/> Nobody\'s. <break time="0.4s"/> Yours now. <break time="2.5s"/>',
     2.5, "measured", "warm", ["yours"], "Pause beat one. Let her enjoy finding it."),
    ("s2", "The one you drop",
     "Now imagine instead that you already had a little gold star. And somewhere on the way home, you dropped it.",
     'Now imagine instead that you already had a little gold star. <break time="0.5s"/> And somewhere on the way home, <break time="0.4s"/> you dropped it.',
     1.4, "slow", "gentle", ["dropped"], "Land the last two words softly."),
    ("s3", "Not the same size",
     "Same star. One star either way. But those two do not feel the same size at all, do they?",
     'Same star. <break time="0.4s"/> One star either way. <break time="0.5s"/> But those two do not feel the same size at all, do they?',
     1.4, "measured", "curious", ["size"], "A real question, not rhetorical."),
    ("s4", "Nice and horrible",
     "Finding one is nice. Losing one is horrible. And horrible is much bigger than nice.",
     'Finding one is nice. <break time="0.4s"/> Losing one is horrible. <break time="0.5s"/> And horrible is much bigger than nice.',
     1.4, "measured", "steady", ["bigger"], "Plain and certain."),
    ("s5", "It tips",
     "If you put them on a see-saw, they would not balance. The losing end would go straight down, and stay there.",
     'If you put them on a see-saw, they would not balance. <break time="0.5s"/> The losing end would go straight down, <break time="0.4s"/> and stay there.',
     1.4, "slow", "steady", ["down"], "Introduce the device clearly."),
    ("s6", "About twice",
     "Losing something weighs about twice as much as getting the very same thing. That is how your brain has always weighed it.",
     'Losing something weighs about twice as much as getting the very same thing. <break time="0.5s"/> That is how your brain has always weighed it.',
     1.4, "measured", "warm", ["twice"], "The hinge. Slow on twice."),
    ("s7", "Why you hold on",
     "Which is why you hold on so tightly to things. Not because you are greedy. Because letting go feels twice as heavy as getting.",
     'Which is why you hold on so tightly to things. <break time="0.5s"/> Not because you are greedy. <break time="0.5s"/> Because letting go feels twice as heavy as getting.',
     1.4, "measured", "tender", ["greedy"], "This is the forgiveness. Mean it."),
    ("s8", "One bad thing",
     "It is the same with days. A day can be full of good little things.",
     'It is the same with days. <break time="0.4s"/> A day can be full of good little things. <break time="2.5s"/>',
     2.5, "measured", "warm", ["good"], "Pause beat two. Let her picture a good day."),
    ("s9", "The one you carry home",
     "And then one bad thing happens. And that is the one you carry home.",
     'And then one bad thing happens. <break time="0.5s"/> And that is the one you carry home.',
     1.4, "slow", "wistful", ["carry"], "Quiet."),
    ("s10", "Not being silly",
     "You are not being silly. You are not being ungrateful. Your see-saw is just built that way.",
     'You are not being silly. <break time="0.4s"/> You are not being ungrateful. <break time="0.5s"/> Your see-saw is just built that way.',
     1.4, "measured", "tender", ["ungrateful"], "The most important line in the film."),
    ("s11", "Very long ago",
     "It was built a long, long time ago, back when losing your food or your warm dry place really was much worse than finding a little extra.",
     'It was built a long, long time ago, <break time="0.4s"/> back when losing your food or your warm dry place really was much worse than finding a little extra.',
     1.4, "slow", "gentle", ["worse"], "Storyteller register."),
    ("s12", "Turned up too high",
     "It kept people safe. It is just turned up much too high for a lost rubber and a wet afternoon.",
     'It kept people safe. <break time="0.5s"/> It is just turned up much too high for a lost rubber and a wet afternoon.',
     1.4, "measured", "wry", ["too high"], "A small smile is allowed here."),
    ("s13", "The first tool",
     "So here is your eighth trick. When you cannot bear to lose something, ask yourself this. If I did not already have it, would I want it?",
     'So here is your eighth trick. <break time="0.5s"/> When you cannot bear to lose something, ask yourself this. <break time="0.5s"/> If I did not already have it, <break time="0.4s"/> would I want it?',
     1.4, "measured", "encouraging", ["want"], "Bright and useful."),
    ("s14", "The second tool",
     "And on a day that one bad thing has spoiled, say the good things out loud. Not to feel better. To put them back on the see-saw where they belong.",
     'And on a day that one bad thing has spoiled, say the good things out loud. <break time="0.5s"/> Not to feel better. <break time="0.5s"/> To put them back on the see-saw where they belong. <break time="2.5s"/>',
     2.5, "measured", "encouraging", ["belong"], "Pause beat three. She should try it on today."),
    ("s15", "Landing",
     "The heavy end will still be heavy. That is alright. You just do not have to let it be the only end you can see.",
     'The heavy end will still be heavy. <break time="0.5s"/> That is alright. <break time="0.5s"/> You just do not have to let it be the only end you can see.',
     0.0, "slow", "tender", ["only end"], "Warm and settled. End soft, then stop."),
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
    "version": "1.0", "title": "Why Losing Hurts More",
    "total_duration_seconds": round(t, 2),
    "voice_performance": {
        "performance_intent": "The same parent and child, seven chapters on. This one is forgiving. Its job is to take shame off something she has probably been told off for, and then hand her a way through.",
        "pacing_profile": "contemplative",
        "energy_curve": "Inviting through the two stars. Steady and certain through the see-saw. Tenderest at you are not being ungrateful. Bright at the tools. Settled at the close.",
        "pause_policy": "Three genuine silences: after yours now, after full of good little things, and after where they belong.",
        "sample_section_id": "s10",
        "provider_notes": {"all": "Roughly 110 words per minute. Section s10 carries the film and is the sample section.",
                           "elevenlabs": "Same voice as films 1 to 7, George. Stability 0.75, similarity 0.9, style 0.15, speed 0.9.",
                           "human_recording": "Section s10 should sound like someone taking the blame off her, not like a fact."}
    },
    "sections": sections,
    "metadata": {
        "series_position": "8 of 18",
        "word_count_approx": sum(len(s["text"].split()) for s in sections),
        "target_wpm": 110,
        "reading_age": "Written for a listener of 8. Loss aversion, reference point, endowment effect and negativity dominance never appear as terms.",
        "pause_beats": [{"section": "s1", "purpose": "She enjoys the found star before it is taken away"},
                        {"section": "s8", "purpose": "She pictures an actual good day of her own"},
                        {"section": "s14", "purpose": "She tries naming today's good things"}],
        "grounded_in": {"s1_to_s3": "Ch 25 and 26, the reference point: the same object as gain or loss",
                        "s4_to_s6": "Ch 26, losses loom larger, ratio commonly 1.5 to 2.5",
                        "s7": "Ch 27, the endowment effect as felt reluctance",
                        "s8_to_s10": "Ch 28, bad events dominate good ones of equal size",
                        "s11_to_s12": "Ch 28, negativity dominance described as an old and once-useful setting",
                        "s13_to_s15": "Ch 27 corrective plus Pennequin on reflection at 8 to 9"},
        "accuracy_guardrails_applied": [
            "About twice is given as approximate; the measured ratio runs 1.5 to 2.5.",
            "The origin sentence says only that the setting is old and once mattered more, never asserting a specific evolutionary account as settled fact.",
            "The film never tells her to feel grateful or that the bad thing did not matter.",
            "No priming or ego-depletion material."]
    }
}
validate(script, "script")

spec = [
    ("sc1", "s1", "DIANA", "The girl walks along a garden path in warm light and notices a single small gold star lying on the ground ahead of her, delighted and leaning towards it."),
    ("sc2", "s2", "DIANA", "The girl looks down at her open empty palm with a dismayed expression, a single small gold star tumbling away out of her hand."),
    ("sc3", "s3", "NONE", "Two identical small star shapes lie side by side in the middle of the cream page. The left star is warm glowing gold. The right star is dull flat grey. Nothing else is in the picture."),
    ("sc4", "s4", "NONE", "A plain wooden see-saw, a simple flat plank balanced across a small triangular wooden block, drawn from the side in the middle of the cream page, perfectly level. One small gold star rests on each end. Nothing else is in the picture."),
    ("sc5", "s4", "NONE", "The same plain wooden see-saw, now tipped steeply. The left end carrying a dull grey star is pressed right down onto the ground. The right end carrying a small gold star is lifted high into the air. Nothing else is in the picture."),
    ("sc6", "s5", "NONE", "A close side view of the low end of a plain wooden see-saw pressing a deep dent into the cream paper beneath it, with one heavy dull grey star sitting on that end. Nothing else is in the picture."),
    ("sc7", "s6", "NONE", "A dull grey star drawn very large on the right of the cream page beside a much smaller gold star on the left. The large grey star casts a heavy soft shadow. Nothing else is in the picture."),
    ("sc8", "s7", "DIANA", "The girl hugs a small soft toy rabbit tightly against her chest with both arms, shoulders drawn in, looking a little anxious."),
    ("sc9", "s8", "NONE", "A gentle row of small warm golden suns spread evenly across the cream page, all of them bright and cheerful and the same size. Nothing else is in the picture."),
    ("sc10", "s8", "DIANA", "The girl sits cross-legged on sunny grass with daisies around her, laughing, in bright warm daylight."),
    ("sc11", "s9", "DIANA", "The girl walks home at dusk with her head down and her hands in her pockets, one small dark rain cloud hovering just above her head, warm evening light."),
    ("sc12", "s10", "NONE", "A tipped plain wooden see-saw on the cream page with one open hand resting gently and lightly on the raised high end, not pressing it down. Only the hand and forearm are visible, no face and no body."),
    ("sc13", "s11", "NONE", "A small crackling campfire and a bundle of food beside the low stone mouth of a shelter at night, warm firelight on the stone. There are no people and no animals anywhere in the picture."),
    ("sc14", "s12", "NONE", "A heavy old dark iron block sits on the low end of a tipped plain wooden see-saw on the cream page. The iron block is completely plain with no markings of any kind on it. Nothing else is in the picture."),
    ("sc15", "s13", "DIANA", "The girl holds a small soft toy rabbit out at arm's length in both hands and looks at it carefully with her head tilted, as if seeing it for the very first time."),
    ("sc16", "s13", "NONE", "One open empty hand, palm upwards and relaxed, in the middle of the cream page. The hand is completely empty. Only the hand and forearm are visible, no face and no body, and there are no other people."),
    ("sc17", "s14", "NONE", "A plain wooden see-saw on the cream page coming back towards level. A dull grey star sits on the lower end, and small warm golden suns are gathered on the rising end, glowing softly. Nothing else is in the picture."),
    ("sc18", "s15", "DIANA", "The girl walks along in warm golden light with her arms swinging freely and her chin up, calm and content."),
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
                   "narrative_role": "deliver_payload" if scid in ("sc5", "sc7", "sc12", "sc17") else "evidence",
                   "hero_moment": scid in ("sc5", "sc7", "sc12", "sc17", "sc18"),
                   "transition_in": "cut", "transition_out": "cut",
                   "shot_language": {"shot_size": "wide" if scid in ("sc4", "sc5", "sc9", "sc17") else "medium",
                                     "camera_movement": "static", "lighting_key": "natural",
                                     "depth_of_field": "medium", "color_temperature": "warm"},
                   "overlay_notes": "No text in the illustration."})

scene_plan = {"version": "1.0", "style_playbook": "custom-atelier-storybook", "scenes": scenes,
              "metadata": {
                  "character_lock": "Diana: a girl of eight, Vietnamese-Australian, straight black shoulder-length hair with a soft fringe, warm light skin, dark almond eyes, round friendly face, mustard-yellow knitted jumper, denim pinafore dress, red canvas shoes. Identical to films 1 to 7.",
                  "one_child_rule": "Every frame containing a person contains exactly one child.",
                  "device_lock": "A plain wooden see-saw, a flat plank on a small triangular block, drawn from the side on empty cream paper. Gold stars are gains, dull grey stars are losses, and the grey end always sits lower. Nothing is ever counted or numbered.",
                  "style_lock": "Unchanged from films 1 to 7.",
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
TOKEN = ("Any star shapes are simple flat star outlines filled with one plain colour and nothing drawn inside them: "
         "no faces, no eyes, no smiles, no patterns.")
SEESAW = ("The see-saw is a plain bare wooden plank resting across a small triangular wooden block, drawn simply "
          "from the side. There is no playground, no frame, no handles and no background scenery, just the plank "
          "and the block on plain empty cream paper. Do NOT draw any markings, scales, dials or measuring marks.")

SEESAW_SCENES = {"sc4", "sc5", "sc6", "sc12", "sc14", "sc17"}
TOKEN_SCENES = {"sc1", "sc2", "sc3", "sc4", "sc5", "sc6", "sc7", "sc17"}

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
    if sid in SEESAW_SCENES:
        parts.append(SEESAW)
    if sid in TOKEN_SCENES:
        parts.append(TOKEN)
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
         "titles": [{"kind": "title", "text": "Why Losing Hurts More",
                     "startSec": round(last["startSec"] + 1.0, 3),
                     "durSec": round(max(2.0, min(8.0, last["durSec"] - 1.0)), 3)}]}
(PROJ / "composition").mkdir(parents=True, exist_ok=True)
json.dump(props, open(PROJ / "composition/props.json", "w", encoding="utf-8"), indent=2)

print(f"\nDONE images_failed={img_fail} narration_failed={aud_fail}")
print(f"total {TOTAL}s ({int(TOTAL//60)}m {TOTAL%60:.1f}s) frames={props['durationInFrames']} scenes={len(pscenes)} captions={len(captions)}")
sys.exit(0 if not img_fail and not aud_fail else 1)
