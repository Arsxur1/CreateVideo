"""One-shot: build film 9, The First Number You Hear (anchoring, Ch 11)."""
import json
import re
import subprocess
import sys
from pathlib import Path

import jsonschema

from tools.tool_registry import registry

SLUG = "diana-anchoring"
PROJ = Path("projects") / SLUG
(PROJ / "artifacts").mkdir(parents=True, exist_ok=True)
DL = "https://thedecisionlab.com/biases/anchoring-bias"
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
    "topic": "Anchoring from Thinking, Fast and Slow, told for an 8-year-old as why the first number somebody says drags your own guess towards it",
    "research_date": "2026-09-09",
    "research_summary": (
        "Film 9 of the series. Chapter 11. When people estimate an unknown quantity, their answer stays too close "
        "to whatever number arrived first, including numbers they know to be arbitrary. Kahneman reports anchoring "
        "indices commonly in the 30 to 55 per cent range, and stresses that awareness of the effect does not "
        "protect against it, which makes anchoring one of the few biases where the honest lesson is procedural "
        "rather than attitudinal. For a child this explains guessing games, haggling, crossed-out prices and the "
        "friend who says a task only took five minutes, and the corrective is Chapter 11's own: deliberately "
        "search for reasons the anchor is wrong in both directions before answering."
    ),
    "landscape": {
        "existing_content": [
            {"title": "Jane the Brain (NIMH)", "url": NIMH, "source": "government site",
             "angle": "Naming and coping with big feelings",
             "what_it_covers": "Emotions, not estimation or how a first number distorts a judgement"},
            {"title": "Children's money and shopping material", "url": SCH, "source": "web",
             "angle": "Save your pocket money, compare prices",
             "what_it_covers": "Tells children to compare prices without explaining why a crossed-out price works on them"},
            {"title": "The Decision Lab - Anchoring Bias", "url": DL, "source": "reference site",
             "angle": "Adult reference explainer",
             "what_it_covers": "Anchoring through salary negotiation, pricing and legal-damages framings"}
        ],
        "saturated_angles": ["Pocket-money and price-comparison lessons",
                             "Adult negotiation, salary and marketing framings"],
        "underserved_gaps": [
            "Showing a child the effect on herself live, by asking the same question with two different first numbers",
            "Telling her honestly that knowing about it does not switch it off",
            "Giving her the think-the-opposite procedure rather than telling her to be careful"
        ]
    },
    "data_points": [
        {"claim": "Estimates of an unknown quantity stay too close to a number considered beforehand, even a clearly arbitrary one.",
         "source_url": DL, "source_name": "Thinking, Fast and Slow, Ch 11",
         "credibility": "secondary_source", "surprise_factor": "counterintuitive",
         "usable_as": "the whole spine of the film and the two-questions demonstration"},
        {"claim": "Anchoring indices commonly fall in the 30 to 55 per cent range, so the pull is large rather than marginal.",
         "source_url": DL, "source_name": "Thinking, Fast and Slow, Ch 11",
         "credibility": "secondary_source", "surprise_factor": "surprising",
         "usable_as": "justifies much smaller rather than slightly smaller"},
        {"claim": "Knowing about anchoring does not protect you from it.",
         "source_url": SN, "source_name": "Thinking, Fast and Slow, Ch 11 and Conclusions",
         "credibility": "secondary_source", "surprise_factor": "counterintuitive",
         "usable_as": "the honest admission beat, and the reason the tool is a procedure"},
        {"claim": "The effective corrective is deliberately generating reasons the anchor is wrong, in both directions.",
         "source_url": DL, "source_name": "Thinking, Fast and Slow, Ch 11",
         "credibility": "secondary_source", "surprise_factor": "expected",
         "usable_as": "the second tool"},
        {"claim": "By age 8 to 9 children can hold and apply an explicit two-step thinking routine.",
         "source_url": PQ, "source_name": "Pennequin et al., British Journal of Educational Psychology (2020)",
         "credibility": "primary_source", "surprise_factor": "expected",
         "usable_as": "age appropriateness of the notice-then-counter routine"}
    ],
    "audience_insights": {
        "knowledge_level": "Age 8. Has seen films 1 to 8 and owns the fast one, the story machine, the memory shelf, separate boxes, the bouncing dot, remember-do-not-guess, protect-the-ending and the see-saw.",
        "common_questions": [
            "Why did my guess come out so close to the number you said?",
            "Why does a sale price feel like a bargain?",
            "If I know somebody is doing it, why does it still work?"
        ],
        "misconceptions": [
            {"myth": "My guess is my own, made from scratch",
             "reality": "It starts from whatever number arrived first and moves too little from there.", "source": "Ch 11"},
            {"myth": "A number I know is silly cannot affect me",
             "reality": "Arbitrary and obviously wrong numbers still pull estimates towards themselves.", "source": "Ch 11"},
            {"myth": "Once you know about a trick it stops working",
             "reality": "Awareness does not switch anchoring off. Only a deliberate procedure helps.", "source": "Ch 11 and Conclusions"}
        ],
        "pain_points": ["Being talked into a number without noticing",
                        "Guessing badly and not understanding why"]
    },
    "angles_discovered": [
        {"name": "The Anchor and the Boat", "type": "narrative",
         "hook": "Your guess is a little boat. It ties itself to whatever anchor went down first.",
         "why_now": "The book's own metaphor, and it needs no numerals on screen, which matters because the image model cannot draw digits.",
         "grounded_in": ["Ch 11 anchoring"]},
        {"name": "Two Questions, Two Answers", "type": "evergreen",
         "hook": "Same gate, same path, same legs. Different first number.",
         "why_now": "Demonstrates the effect on her live rather than describing it, which is the only way it becomes real at this age.",
         "grounded_in": ["Ch 11 the more-or-less-than manipulation"]},
        {"name": "It Still Works On Me", "type": "contrarian",
         "hook": "Knowing about it does not switch it off.",
         "why_now": "Nearly all children's content on thinking implies awareness is the cure. Kahneman says plainly that it is not.",
         "grounded_in": ["Ch 11", "Conclusions"]}
    ],
    "expert_voices": [
        {"name": "Daniel Kahneman", "title_or_affiliation": "Nobel laureate, author",
         "position": "Estimates stay too close to the first number offered, and awareness does not protect against it.",
         "source_url": DL, "contrarian": False}
    ],
    "sources": [
        {"url": DL, "title": "Anchoring Bias - The Decision Lab", "used_for": "Mechanism and index range", "reliability": "secondary"},
        {"url": SN, "title": "Thinking, Fast and Slow Summary", "used_for": "Chapter 11", "reliability": "secondary"},
        {"url": PQ, "title": "Metacognition and emotional regulation in children 8 to 12", "used_for": "Age appropriateness", "reliability": "primary"},
        {"url": NIMH, "title": "Jane the Brain - NIMH", "used_for": "Format benchmark", "reliability": "primary"},
        {"url": SCH, "title": "Social and Emotional Lives of 8- to 10-Year-Olds", "used_for": "Money and comparison at this age", "reliability": "secondary"}
    ],
    "metadata": {
        "series": "Film 9 of 18.",
        "excluded_claims": [
            "Specific anchoring index percentages, which mean nothing to an 8-year-old and would need numerals.",
            "The adult negotiation and legal-damages experiments.",
            "Anything from the priming or ego-depletion chapters."],
        "production_constraint": ("The house style forbids numerals in illustrations because the image model cannot "
                                  "draw digits reliably. Every number in this film is spoken only. The visual device "
                                  "is the literal anchor and boat, which carries the idea with no digits on screen.")}
}
validate(research, "research_brief")

proposal = {
    "version": "1.0",
    "concept_options": [
        {"id": "c1", "title": "The First Number You Hear",
         "hook": "I am going to say a number to you, and even though you know I am doing it, it is going to stick.",
         "narrative_structure": "story",
         "visual_approach": "The established storybook world. New device: a heavy anchor and a small wooden boat on a single calm band of water. Wherever the anchor lands, the boat ties on and drifts only a short way from it.",
         "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old, watched with her dad",
         "target_platform": "generic", "target_duration_seconds": 150,
         "key_points": ["The first number heard drags the guess towards it",
                        "Same question, different first number, very different answer",
                        "You did not choose the anchor, somebody else dropped it",
                        "It works with obviously silly numbers, and knowing does not stop it",
                        "The moves: name the anchor out loud, then find a reason it could be much bigger and much smaller"],
         "core_message": "You cannot stop people dropping anchors near you. But you can notice the rope, and you can pull your own up.",
         "cta": "When somebody gives you a number, say there is the anchor, then find one reason it could be much bigger and one reason it could be much smaller.",
         "tone": "Playful, then honest, then practical.",
         "why_this_works": "It runs the experiment on her live in the first thirty seconds, so the idea arrives as something she felt rather than something she was told.",
         "grounded_in": ["Ch 11 anchoring", "Ch 11 think-the-opposite corrective"]},
        {"id": "c2", "title": "It Still Works On Me",
         "hook": "Knowing about the trick does not switch it off.",
         "narrative_structure": "comparison",
         "visual_approach": "A heavy anchor sitting in a pool of bright lamplight, fully visible and completely unmoved.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 110,
         "key_points": ["Awareness is not a cure", "Only a procedure helps", "Even the person explaining it is caught"],
         "core_message": "Seeing it does not lift it.", "cta": "Use the procedure, not your willpower.", "tone": "Honest",
         "why_this_works": "The most intellectually honest beat in the territory, but it is a footnote without the demonstration, so it becomes the middle of c1.",
         "grounded_in": ["Ch 11", "Conclusions"]},
        {"id": "c3", "title": "Pull Your Own Anchor Up",
         "hook": "Find one reason it could be much bigger, and one reason it could be much smaller.",
         "narrative_structure": "tutorial",
         "visual_approach": "A boat with its anchor hauled clear of the sea bed, free on open water.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 95,
         "key_points": ["Name the anchor", "Argue both directions", "Then answer"],
         "core_message": "Argue with the anchor before you answer.", "cta": "Run the two reasons.", "tone": "Practical",
         "why_this_works": "The actionable core, but an instruction with nothing behind it, so it becomes the payoff of c1.",
         "grounded_in": ["Ch 11 corrective"]}
    ],
    "selected_concept": {
        "concept_id": "c1",
        "rationale": "c1 performs the effect on her before explaining it, which is the only version where an 8-year-old has direct evidence rather than a claim. The other two are its middle and its ending.",
        "modifications": ["All production decisions carry over from films 1 to 8",
                          "New device: the anchor and the little boat",
                          "Every number spoken only, never drawn",
                          "Scene coverage asserted before generation",
                          "Render via video_compose operation 'render'"]},
    "production_plan": {
        "pipeline": "animated-explainer", "playbook": "custom-atelier-storybook",
        "renderer_family": "explainer-teacher", "render_runtime": "remotion", "composition_mode": "atelier",
        "delivery_promise": {"promise_type": "teacher_explainer", "motion_required": False, "source_required": False,
                             "tone_mode": "intimate and playful, a bedtime storybook read aloud",
                             "quality_floor": "presentable", "approved_fallback": "still_led"},
        "art_direction": "Unchanged series house style. New device: a heavy dark anchor and a small wooden boat on one calm band of water, on otherwise empty cream paper.",
        "taste_profile": {"design_read": "The same bedtime picture book, eight chapters on",
                          "visual_variance": 8, "motion_intensity": 3, "information_density": 2,
                          "palette_discipline": "Unchanged. Cream ground, muted warm palette, with a single soft blue-grey band for water.",
                          "layout_variation": "Each scene composed for its beat. The anchor line gives this film its vertical geometry against the horizontal water band.",
                          "reference_strategy": "Series continuity only.",
                          "anti_patterns": ["any numeral, price tag with writing, clock face, ruler or measuring scale",
                                            "asking the image model for an exact count of anything",
                                            "two children in one frame",
                                            "a full painted seascape; the water is one band on empty cream paper",
                                            "implying that simply knowing about anchoring protects her"],
                          "quality_gates": ["Contact sheet reviewed before render",
                                            "Every script section mapped to a scene, asserted at build time",
                                            "ffprobe the rendered file against the props frame count before encoding"]},
        "music_source": {"source_type": "ai_generated", "provider": "reused from film 1 (Google Lyria)",
                         "mood_direction": "The same bed as films 1 to 8.", "estimated_cost_usd": 0.0},
        "voice_selection": {"provider": "elevenlabs", "voice_id": "JBFqnCBsd6RMkjVDRZzb",
                            "rationale": "The same warm storyteller voice as films 1 to 8.",
                            "estimated_cost_usd": 0.85,
                            "delivery_style": "warm parent reading a bedtime story, playful at the demonstration and candid at the admission",
                            "pacing_policy": "Roughly 110 words per minute with three genuine silences.",
                            "sample_approval_required": False},
        "stages": [
            {"stage": "script", "approach": "Around 320 words at an 8-year-old listening level, three pause beats.", "tools": []},
            {"stage": "scene_plan", "approach": "Eighteen scenes covering all fifteen sections, the anchor carrying the spine.", "tools": []},
            {"stage": "assets", "approach": "Same image model and character lock, same voice, music reused.",
             "tools": [{"tool_name": "google_imagen", "role": "illustration", "available": True},
                       {"tool_name": "elevenlabs_tts", "role": "narration", "available": True}]},
            {"stage": "edit", "approach": "Timeline rebuilt from measured narration durations.", "tools": []},
            {"stage": "compose", "approach": "Atelier Remotion render via video_compose operation 'render'.",
             "tools": [{"tool_name": "video_compose", "role": "render", "available": True}]}
        ],
        "quality_tradeoffs": [
            {"tradeoff": "Numbers on screen versus numbers spoken only",
             "recommendation": "Spoken only",
             "quality_impact": "The image model cannot draw digits reliably, and a wrong numeral in a film about numbers would be fatal. The anchor device carries the whole idea without a single digit."},
            {"tradeoff": "Admitting awareness does not cure it versus ending on a confident tool",
             "recommendation": "Admit it, then give the procedure",
             "quality_impact": "Kahneman is explicit that knowing does not help. Pretending otherwise would teach her to trust a defence she does not have."}
        ],
        "alternative_paths": [
            {"description": "Demonstration only, corrective deferred", "total_cost_usd": 1.57, "quality_level": "standard"},
            {"description": "Reuse everything from films 1 to 8", "total_cost_usd": 1.57, "quality_level": "standard"}
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
                 "user_notes": "User replied NEXT, selecting the next film in the approved series, under a standing instruction to fix defects without asking."},
    "metadata": {"series_position": "9 of 18",
                 "carried_over": ["character lock", "style lock", "voice", "runtime", "composition mode", "music bed"],
                 "new_this_film": ["the anchor and the little boat"],
                 "chapters_now_covered": "1-3, 7, 11, 12-13, 17, 23-24, 25-28, 35-36"}
}
validate(proposal, "proposal_packet")

S = [
    ("s1", "A number will stick",
     "I am going to say a number to you, Diana. And even though you know I am doing it, that number is going to stick to you.",
     'I am going to say a number to you, Diana. <break time="0.5s"/> And even though you know I am doing it, <break time="0.4s"/> that number is going to stick to you. <break time="2.5s"/>',
     2.5, "measured", "playful", ["stick"], "Pause beat one. A little conspiratorial."),
    ("s2", "The gate",
     "Here is the game. How many steps do you think it is, from our front door to the front gate? But before you answer. Do you think it is more than a thousand?",
     'Here is the game. <break time="0.4s"/> How many steps do you think it is, from our front door to the front gate? <break time="0.5s"/> But before you answer. <break time="0.5s"/> Do you think it is more than a thousand?',
     1.4, "measured", "playful", ["thousand"], "Set the trap lightly."),
    ("s3", "Your guess",
     "Go on. Have a proper guess.",
     'Go on. <break time="0.4s"/> Have a proper guess. <break time="2.5s"/>',
     2.5, "slow", "warm", ["guess"], "Pause beat two. She must actually answer for the film to work."),
    ("s4", "The other question",
     "Now imagine I had asked you something different. Do you think it is more than ten? Your guess would have come out smaller. Much, much smaller.",
     'Now imagine I had asked you something different. <break time="0.5s"/> Do you think it is more than ten? <break time="0.5s"/> Your guess would have come out smaller. <break time="0.4s"/> Much, much smaller.',
     1.4, "measured", "curious", ["smaller"], "The reveal. Let it land."),
    ("s5", "Nothing changed",
     "Same door. Same gate. Same legs. The only thing that changed was the number I said first.",
     'Same door. <break time="0.3s"/> Same gate. <break time="0.3s"/> Same legs. <break time="0.5s"/> The only thing that changed was the number I said first.',
     1.4, "measured", "steady", ["first"], "Plain and certain."),
    ("s6", "It is an anchor",
     "That first number is an anchor. And an anchor only does one job. It holds things near itself.",
     'That first number is an anchor. <break time="0.5s"/> And an anchor only does one job. <break time="0.4s"/> It holds things near itself.',
     1.4, "slow", "steady", ["anchor"], "Introduce the device clearly."),
    ("s7", "The boat",
     "Your guess is a little boat. The moment the anchor goes down, your boat ties itself on, and drifts only a little way from it.",
     'Your guess is a little boat. <break time="0.5s"/> The moment the anchor goes down, your boat ties itself on, <break time="0.4s"/> and drifts only a little way from it.',
     1.4, "measured", "warm", ["ties"], "Gentle, picture-building."),
    ("s8", "You did not drop it",
     "And you did not drop that anchor. Somebody else did. Before you had even started thinking.",
     'And you did not drop that anchor. <break time="0.4s"/> Somebody else did. <break time="0.5s"/> Before you had even started thinking.',
     1.4, "measured", "steady", ["somebody else"], "The uncomfortable bit."),
    ("s9", "Even silly ones",
     "It works with silly numbers too. Numbers that could not possibly be right still pull your guess towards them.",
     'It works with silly numbers too. <break time="0.5s"/> Numbers that could not possibly be right still pull your guess towards them.',
     1.4, "measured", "curious", ["silly"], "Slightly amused."),
    ("s10", "Even knowing",
     "And here is the annoying part. Knowing about it does not switch it off. It is happening to me right now, while I am telling you about it.",
     'And here is the annoying part. <break time="0.5s"/> Knowing about it does not switch it off. <break time="0.5s"/> It is happening to me right now, <break time="0.4s"/> while I am telling you about it.',
     1.4, "measured", "wry", ["me"], "Candid. This is the honest beat."),
    ("s11", "Where you will meet it",
     "You will meet anchors everywhere. A price with a bigger crossed-out price beside it. Somebody saying oh, that is easy, it only took me five minutes.",
     'You will meet anchors everywhere. <break time="0.4s"/> A price with a bigger crossed-out price beside it. <break time="0.5s"/> Somebody saying oh, that is easy, <break time="0.3s"/> it only took me five minutes.',
     1.4, "measured", "wry", ["everywhere"], "Everyday and recognisable."),
    ("s12", "Whoever speaks first",
     "Whoever says a number first is steering. Usually without meaning to. Sometimes very much meaning to.",
     'Whoever says a number first is steering. <break time="0.4s"/> Usually without meaning to. <break time="0.5s"/> Sometimes very much meaning to.',
     1.4, "slow", "steady", ["steering"], "Land the last clause a shade darker."),
    ("s13", "The first tool",
     "So here is your ninth trick. When somebody gives you a number, say it to yourself. There is the anchor.",
     'So here is your ninth trick. <break time="0.5s"/> When somebody gives you a number, say it to yourself. <break time="0.5s"/> There is the anchor.',
     1.4, "measured", "encouraging", ["anchor"], "Bright and useful."),
    ("s14", "The second tool",
     "Then, before you answer, find one reason the real answer could be much bigger. And one reason it could be much smaller. That is you pulling your own anchor up.",
     'Then, before you answer, find one reason the real answer could be much bigger. <break time="0.5s"/> And one reason it could be much smaller. <break time="0.5s"/> That is you pulling your own anchor up. <break time="2.5s"/>',
     2.5, "measured", "encouraging", ["bigger", "smaller"], "Pause beat three. She should try both directions."),
    ("s15", "Landing",
     "You cannot stop people dropping anchors near you. But you can always notice the rope.",
     'You cannot stop people dropping anchors near you. <break time="0.5s"/> But you can always notice the rope.',
     0.0, "slow", "tender", ["rope"], "Calm and settled. End soft, then stop."),
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
    "version": "1.0", "title": "The First Number You Hear",
    "total_duration_seconds": round(t, 2),
    "voice_performance": {
        "performance_intent": "The same parent and child, eight chapters on. This one opens as a game played on her, turns candid in the middle when he admits it works on him too, and ends practical.",
        "pacing_profile": "conversational",
        "energy_curve": "Playful and conspiratorial through the guessing game. Steady through the anchor. Candid and slightly rueful at it is happening to me right now. Bright at the tools. Calm at the close.",
        "pause_policy": "Three genuine silences: after it is going to stick to you, after have a proper guess, and after pulling your own anchor up.",
        "sample_section_id": "s10",
        "provider_notes": {"all": "Roughly 110 words per minute. Section s10 is the honest beat and the sample section.",
                           "elevenlabs": "Same voice as films 1 to 8, George. Stability 0.75, similarity 0.9, style 0.15, speed 0.9.",
                           "human_recording": "Section s3 must leave a real silence. If she does not actually guess, the reveal in s4 has nothing to land on."}
    },
    "sections": sections,
    "metadata": {
        "series_position": "9 of 18",
        "word_count_approx": sum(len(s["text"].split()) for s in sections),
        "target_wpm": 110,
        "reading_age": "Written for a listener of 8. Anchoring, anchoring index and adjustment never appear as terms.",
        "pause_beats": [{"section": "s1", "purpose": "She braces for the trick, which makes the failure more striking"},
                        {"section": "s3", "purpose": "She commits to an actual number; the film depends on this"},
                        {"section": "s14", "purpose": "She tries arguing both directions on a real question"}],
        "grounded_in": {"s1_to_s3": "Ch 11, the more-or-less-than manipulation used as a live demonstration",
                        "s4_to_s5": "Ch 11, the same question with a different anchor yields a very different estimate",
                        "s6_to_s8": "Ch 11, insufficient adjustment away from the anchor",
                        "s9": "Ch 11, arbitrary and implausible anchors still pull",
                        "s10": "Ch 11 and Conclusions, awareness does not protect",
                        "s11_to_s12": "Ch 11, everyday anchors in prices and casual claims",
                        "s13_to_s15": "Ch 11 corrective, deliberately arguing against the anchor in both directions"},
        "accuracy_guardrails_applied": [
            "No anchoring index percentage is quoted; the film says much smaller, which is faithful to a 30 to 55 per cent pull without needing a figure.",
            "The film explicitly refuses the comforting claim that knowing about a bias defeats it.",
            "Every number is spoken only. No numeral appears in any illustration.",
            "No priming or ego-depletion material."]
    }
}
validate(script, "script")

spec = [
    ("sc1", "s1", "DIANA", "The girl sits on a low wooden step with her head tilted upwards, listening intently and a little amused, in warm light."),
    ("sc2", "s2", "DIANA", "The girl stands at the near end of a long garden path with one hand shading her eyes, looking towards a small wooden gate far away in the distance."),
    ("sc3", "s2", "NONE", "A long empty winding garden path leads away across the page into the distance and ends at one small closed wooden gate. Only the path, a few blades of grass and the gate are drawn."),
    ("sc4", "s3", "DIANA", "The girl thinks hard with her eyes narrowed and one finger resting against her chin, working something out."),
    ("sc5", "s4", "NONE", "A small wooden rowing boat floats on a calm horizontal band of water at the FAR LEFT of the page, with a taut rope running down from it to a heavy dark anchor resting on the sea bed directly below. The whole right half of the page is empty."),
    ("sc6", "s5", "NONE", "Two separate horizontal bands of calm water drawn one above the other. In the UPPER band a small wooden boat sits at the far right with its rope down to an anchor below it. In the LOWER band an identical boat sits at the far left with its rope down to an identical anchor below it."),
    ("sc7", "s6", "NONE", "One heavy dark anchor resting alone in the middle of the page, its thick rope trailing upwards and off the top edge of the picture. Nothing else is in the picture."),
    ("sc8", "s7", "NONE", "A small wooden rowing boat on a calm band of water with a taut rope running straight down to a heavy anchor on the sea bed, the boat leaning a short way to the left of the rope."),
    ("sc9", "s7", "NONE", "The same small wooden boat on a calm band of water, now leaning a short way to the right of its anchor rope, with a faint soft arc drawn to show the small distance it can travel."),
    ("sc10", "s8", "NONE", "One open hand comes down from the top edge of the picture and lets go of a thick anchor rope that drops away into a calm band of water below. Only the hand and forearm are visible, with no face and no body."),
    ("sc11", "s9", "NONE", "An enormously oversized heavy dark anchor, far too big to make any sense, sits on the sea bed beside a tiny little wooden boat floating above it on a calm band of water."),
    ("sc12", "s10", "NONE", "A heavy dark anchor sits in a warm circular pool of lamplight on the page, completely and clearly lit up, and still resting heavily and unmoved on the ground."),
    ("sc13", "s11", "NONE", "One small blank paper tag hangs from a short string in the middle of the page. The tag is completely blank, with no writing, no marks, no numbers and no symbols of any kind on it."),
    ("sc14", "s11", "NONE", "A simple rounded empty speech bubble drawn in the middle of the page, with one small heavy dark anchor resting inside it instead of any words."),
    ("sc15", "s12", "NONE", "A small wooden rowing boat on a calm band of water being pulled sideways towards the right edge of the page by a taut rope that leads off out of the picture."),
    ("sc16", "s13", "DIANA", "The girl stops mid-step with one hand raised and her eyebrows lifted, alert, as if she has just noticed something."),
    ("sc17", "s14", "NONE", "A small wooden rowing boat on a calm band of open water with its heavy anchor hauled right up out of the water and hanging just below the boat, the sea bed clear and empty beneath it."),
    ("sc18", "s15", "DIANA", "The girl stands at the end of a short wooden jetty looking out over calm open water in warm golden light, steady and clear-eyed."),
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
                   "narrative_role": "deliver_payload" if scid in ("sc6", "sc7", "sc12", "sc17") else "evidence",
                   "hero_moment": scid in ("sc6", "sc7", "sc12", "sc17", "sc18"),
                   "transition_in": "cut", "transition_out": "cut",
                   "shot_language": {"shot_size": "wide" if scid in ("sc3", "sc5", "sc6", "sc17") else "medium",
                                     "camera_movement": "static", "lighting_key": "natural",
                                     "depth_of_field": "medium", "color_temperature": "warm"},
                   "overlay_notes": "No text in the illustration."})

scene_plan = {"version": "1.0", "style_playbook": "custom-atelier-storybook", "scenes": scenes,
              "metadata": {
                  "character_lock": "Diana: a girl of eight, Vietnamese-Australian, straight black shoulder-length hair with a soft fringe, warm light skin, dark almond eyes, round friendly face, mustard-yellow knitted jumper, denim pinafore dress, red canvas shoes. Identical to films 1 to 8.",
                  "one_child_rule": "Every frame containing a person contains exactly one child.",
                  "device_lock": "A heavy dark anchor and a small wooden rowing boat on one calm horizontal band of soft blue-grey water, on otherwise empty cream paper. The boat always sits close to wherever its anchor rests.",
                  "numeral_ban": "No numeral, price, clock face, ruler or measuring scale appears in any illustration. Every number in this film is spoken only.",
                  "style_lock": "Unchanged from films 1 to 8.",
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
NOPE = "There are NO people and NO animals at all in this picture."
OPEN = ("Most of the page must stay plain empty cream paper. Draw only the objects described, floating on that "
        "empty paper. Do NOT fill the frame with scenery, foliage, walls or a painted background of any kind.")
SEA = ("The water is ONE simple calm horizontal band of soft blue-grey across the page, like a strip of paper. "
       "There is no sky, no clouds, no shoreline, no horizon and no seascape; above and below the band the page is "
       "plain empty cream paper. The anchor is a simple traditional anchor shape in flat dark blue-grey with no "
       "markings on it. The boat is a small plain wooden rowing boat seen from the side.")

SEA_SCENES = {"sc5", "sc6", "sc8", "sc9", "sc10", "sc11", "sc15", "sc17"}
OPEN_SCENES = {"sc1", "sc3", "sc4", "sc7", "sc12", "sc13", "sc14", "sc16"}

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
    if sid in SEA_SCENES:
        parts.append(SEA)
    if sid in OPEN_SCENES:
        parts.append(OPEN)
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
         "titles": [{"kind": "title", "text": "The First Number You Hear",
                     "startSec": round(last["startSec"] + 1.0, 3),
                     "durSec": round(max(2.0, min(8.0, last["durSec"] - 1.0)), 3)}]}
(PROJ / "composition").mkdir(parents=True, exist_ok=True)
json.dump(props, open(PROJ / "composition/props.json", "w", encoding="utf-8"), indent=2)

print(f"\nDONE images_failed={img_fail} narration_failed={aud_fail}")
print(f"total {TOTAL}s ({int(TOTAL//60)}m {TOTAL%60:.1f}s) frames={props['durationInFrames']} scenes={len(pscenes)} captions={len(captions)}")
sys.exit(0 if not img_fail and not aud_fail else 1)
