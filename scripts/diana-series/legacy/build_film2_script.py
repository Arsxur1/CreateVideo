"""One-shot: build the script and scene plan for film 2, The Story Machine."""
import json
import jsonschema
from pathlib import Path

PROJ = Path("projects/diana-story-machine")


def validate(obj, name):
    schema = json.load(open(f"schemas/artifacts/{name}.schema.json", encoding="utf-8"))
    jsonschema.validate(obj, schema)
    json.dump(obj, open(PROJ / f"artifacts/{name}.json", "w", encoding="utf-8"), indent=2)
    print(f"{name} SCHEMA-VALID")


def cues(txt, prov, pause, pace, energy, emph, note):
    return {"pace": pace, "energy": energy, "emphasis_words": emph or [],
            "pause_after_seconds": pause, "delivery_note": note,
            "provider_text": prov or txt}


S = [
    ("s1", "Hook - the wave",
     "Diana waved at her friend. Right across the playground. A big wave, both arms. And her friend did not wave back.",
     'Diana waved at her friend. <break time="0.4s"/> Right across the playground. A big wave, both arms. <break time="0.7s"/> And her friend did not wave back.',
     1.2, "measured", "playful", ["wave", "not"], "Open light and ordinary. The drop lands on the last five words."),
    ("s2", "The story arrives",
     "By the time you had taken one more step, it was already finished. She is cross with me. I must have done something. She does not want to be my friend any more.",
     'By the time you had taken one more step, it was already finished. <break time="0.6s"/> She is cross with me. <break time="0.3s"/> I must have done something. <break time="0.3s"/> She does not want to be my friend any more.',
     1.2, "measured", "quickening", ["finished"], "The three thoughts should arrive faster than comfortable. That is the point."),
    ("s3", "One second",
     "One second. A whole story. And you believed every single word of it.",
     'One second. <break time="0.5s"/> A whole story. <break time="0.5s"/> And you believed every single word of it. <break time="2.5s"/>',
     2.5, "slow", "quiet", ["believed"], "Pause beat one. Let her sit with recognising herself."),
    ("s4", "Callback to the fast one",
     "Remember your fast one? The quick one that catches the ball before you have thought about it? This is one of the things it does. It writes stories.",
     'Remember your fast one? <break time="0.5s"/> The quick one that catches the ball before you have thought about it? <break time="0.5s"/> This is one of the things it does. <break time="0.4s"/> It writes stories.',
     1.0, "measured", "warm", ["stories"], "Warm callback. She should feel clever for remembering."),
    ("s5", "It is brilliant at it",
     "And it is brilliant at it. Give your fast one one small thing. One glance. One silence. One door slamming upstairs. And it will hand you a finished story before you can blink.",
     'And it is brilliant at it. <break time="0.4s"/> Give your fast one one small thing. One glance. <break time="0.3s"/> One silence. <break time="0.3s"/> One door slamming upstairs. <break time="0.5s"/> And it will hand you a finished story before you can blink.',
     1.0, "conversational", "admiring", ["brilliant", "blink"], "Never frame the machine as the villain."),
    ("s6", "Try it",
     "Try it now. Somewhere upstairs, a door slams.",
     'Try it now. <break time="0.5s"/> Somewhere upstairs, a door slams. <break time="2.5s"/>',
     2.5, "slow", "curious", ["slams"], "Pause beat two. Genuinely wait. She will build a story."),
    ("s7", "It just arrived",
     "You already have a story, do you not? You did not sit down and choose it. It just arrived.",
     'You already have a story, do you not? <break time="0.6s"/> You did not sit down and choose it. <break time="0.4s"/> It just arrived.',
     1.2, "slow", "gentle", ["arrived"], "Soft. This is the moment she catches her own mind working."),
    ("s8", "It hides the gaps",
     "Now here is the strange bit. Your story machine only uses the pieces it can actually see. And it never tells you about the pieces that are missing.",
     'Now here is the strange bit. <break time="0.5s"/> Your story machine only uses the pieces it can actually see. <break time="0.6s"/> And it never tells you about the pieces that are missing.',
     1.4, "slow", "gentle", ["missing"], "The hinge of the film. Slow right down."),
    ("s9", "What she did not know",
     "So back to the playground. Here is what your machine did not know. That morning, your friend had lost her glasses. She could not see across the playground at all. She was not even looking at you.",
     'So back to the playground. <break time="0.5s"/> Here is what your machine did not know. <break time="0.6s"/> That morning, your friend had lost her glasses. <break time="0.4s"/> She could not see across the playground at all. <break time="0.4s"/> She was not even looking at you.',
     1.2, "measured", "tender", ["glasses"], "Kind, not triumphant. Nobody is being corrected here."),
    ("s10", "Nothing was wrong",
     "Nothing was wrong. There was never anything wrong. But the story felt so real. Did it not?",
     'Nothing was wrong. <break time="0.4s"/> There was never anything wrong. <break time="0.7s"/> But the story felt so real. <break time="0.5s"/> Did it not?',
     1.4, "slow", "tender", ["never", "real"], "The most tender line in the film."),
    ("s11", "Sure is not the same as knowing",
     "That is the part worth remembering. Feeling sure has almost nothing to do with how much you know. Feeling sure is just your story being neat and tidy.",
     'That is the part worth remembering. <break time="0.5s"/> Feeling sure has almost nothing to do with how much you know. <break time="0.6s"/> Feeling sure is just your story being neat and tidy.',
     1.2, "slow", "steady", ["sure", "tidy"], "The transferable idea. Land it plainly."),
    ("s12", "Tidy beats true",
     "A small tidy story feels more true than a big messy one. Even when the messy one is the real one.",
     'A small tidy story feels more true than a big messy one. <break time="0.5s"/> Even when the messy one is the real one.',
     1.2, "measured", "curious", ["tidy", "messy"], "Slight wryness is allowed here."),
    ("s13", "The tool",
     "So here is your second trick. When you are completely sure why somebody did something, stop. And ask your machine for one more story. What else could be true?",
     'So here is your second trick. <break time="0.5s"/> When you are completely sure why somebody did something, <break time="0.4s"/> stop. <break time="0.6s"/> And ask your machine for one more story. <break time="0.5s"/> What else could be true? <break time="2.5s"/>',
     2.5, "measured", "encouraging", ["stop", "else"], "Pause beat three. She should actually try to think of one."),
    ("s14", "There is always another",
     "There is always another story. A lost pair of glasses. A bad morning. Somebody who simply did not see you.",
     'There is always another story. <break time="0.4s"/> A lost pair of glasses. <break time="0.3s"/> A bad morning. <break time="0.3s"/> Somebody who simply did not see you.',
     1.2, "measured", "warm", ["always"], "Gentle list. Each one a small relief."),
    ("s15", "Landing",
     "You cannot switch the machine off. Nobody can, not even grown-ups. But you can always ask it for a second story. And the second one is usually the kinder one.",
     'You cannot switch the machine off. <break time="0.4s"/> Nobody can, not even grown-ups. <break time="0.6s"/> But you can always ask it for a second story. <break time="0.5s"/> And the second one is usually the kinder one.',
     0.0, "slow", "proud", ["kinder"], "End on kindness as a skill, not an instruction. Then stop."),
]

sections, t = [], 0.0
for sid, label, text, prov, pause, pace, energy, emph, note in S:
    dur = round(len(text.split()) / 110 * 60 + pause, 2)
    sections.append({
        "id": sid, "label": label, "text": text,
        "start_seconds": round(t, 2), "end_seconds": round(t + dur, 2),
        "speaker_directions": note,
        "delivery_cues": cues(text, prov, pause, pace, energy, emph, note),
        "enhancement_cues": [], "pronunciation_guides": []
    })
    t += dur

script = {
    "version": "1.0", "title": "The Story Machine",
    "total_duration_seconds": round(t, 2),
    "voice_performance": {
        "performance_intent": "The same parent, the same child, one chapter later. Warm, unhurried, faintly amused, and completely serious at the turn. She has met this narrator before and should recognise him instantly.",
        "pacing_profile": "contemplative",
        "energy_curve": "Light and ordinary at the wave. Quickens deliberately through the three thoughts so the speed itself is the demonstration. Drops low and gentle from the gaps through to nothing was wrong. Lifts slightly into quiet pride at the end.",
        "pause_policy": "Three genuine silences of two and a half seconds: after believing the story, after the door slams, and after asking what else could be true. Each is a place where she is meant to answer out loud.",
        "sample_section_id": "s10",
        "provider_notes": {
            "all": "Roughly 110 words per minute. Section s10 is the emotional hinge and the sample section.",
            "elevenlabs": "Same voice as film 1, George. Stability 0.75, similarity 0.9, style 0.15, speed 0.9.",
            "human_recording": "If Daniel records this, read it to Diana, not to a microphone. Keep all three silences genuinely silent."
        }
    },
    "sections": sections,
    "metadata": {
        "series_position": "2 of 18",
        "word_count_approx": sum(len(s["text"].split()) for s in sections),
        "target_wpm": 110,
        "reading_age": "Written for a listener of 8. No psychology vocabulary. The words bias, heuristic and WYSIATI never appear.",
        "pause_beats": [
            {"section": "s3", "purpose": "She recognises that she has done this"},
            {"section": "s6", "purpose": "She builds a story about the slamming door and catches herself doing it"},
            {"section": "s13", "purpose": "She actually attempts a second story"}
        ],
        "grounded_in": {
            "s1_to_s3": "Ch 7 WYSIATI, a coherent story built instantly from one scrap",
            "s4_to_s7": "Ch 7 plus the System 1 vocabulary film 1 established",
            "s8_to_s10": "Ch 7, the mind never registers what is missing",
            "s11_to_s12": "Ch 7, confidence tracks coherence rather than evidence quality",
            "s13_to_s15": "Ch 7 corrective, plus Pennequin on age-appropriate cognitive moves"
        },
        "accuracy_guardrails_applied": [
            "The machine is never framed as bad or as a fault in her. It is described as brilliant before it is described as misleading.",
            "No claim that she can stop the process; Kahneman is explicit that System 1 cannot be switched off.",
            "No priming or ego-depletion material.",
            "The friend's reason is ordinary and blameless, so the lesson is not that people are secretly kind but that she lacked information."
        ]
    }
}
validate(script, "script")

scenes_spec = [
    ("sc1", "s1", "Diana stands at the edge of a soft playground waving with both arms, bright and open, looking across a wide empty space. Warm afternoon light."),
    ("sc2", "s1", "The far side of the playground. Another child, a friend with curly brown hair, a sage-green cardigan and round glasses, stands turned slightly away, not waving, not looking."),
    ("sc3", "s2", "Three small tidy comic panels print rapidly onto the cream page in warm gold ink, one after another, each showing a tiny simple scene of a friendship going wrong. No child in frame, only the printed panels."),
    ("sc4", "s3", "Diana walking away across the playground with her head down, a single neat little cloud of printed panels floating above her shoulder, already settled and believed."),
    ("sc5", "s4", "Diana mid-stride, and the familiar quick warm-gold streak loops around her, exactly as it did when she caught the ball."),
    ("sc6", "s5", "A small hand-drawn printing press made of warm wood sits on the cream page. A single tiny scrap of paper goes in one end and a long ribbon of finished comic panels streams out the other. No people."),
    ("sc7", "s6", "A quiet hallway inside a house, a door at the end just slammed shut, still trembling, dust motes hanging in the light. Nobody visible."),
    ("sc8", "s7", "Diana alone on the cream page, one finished comic panel already floating beside her head, her expression caught between surprise and recognition."),
    ("sc9", "s8", "Diana alone, holding four small printed panels in her hands like playing cards, looking at them trustingly."),
    ("sc10", "s8", "A vast wall of empty blank unprinted comic panels stretching away across the whole page, with one tiny cluster of four printed panels in the corner. A single very small child stands at the bottom of the frame, dwarfed by the blankness."),
    ("sc11", "s9", "A child with curly brown hair and a sage-green cardigan kneels on a classroom floor, patting the ground with her hands, searching for her lost glasses."),
    ("sc12", "s9", "The same curly-haired child stands in a playground squinting into a blur, everything around her painted soft and out of focus because she cannot see."),
    ("sc13", "s10", "Diana alone on the cream page, one hand over her mouth, eyes soft, the moment of understanding landing gently."),
    ("sc14", "s11", "Two simple hand-drawn glass jars side by side on cream paper. The left jar is brim full and glowing warmly. The right jar is almost completely empty. No people, no charts, no numbers, no lettering."),
    ("sc15", "s12", "Two shapes on cream paper. On the left a small neat tidy square of four panels glowing warmly. On the right a large sprawling messy tangle of many panels, dull and untidy. No people."),
    ("sc16", "s13", "Diana alone, stopped mid-step with one hand raised, deliberately pausing, the gold streak held still beside her for once."),
    ("sc17", "s14", "Three fresh comic panels print gently onto the page in soft blue ink instead of gold: a pair of lost glasses, a grey rainy morning, and a child looking the other way. No people in the frame."),
    ("sc18", "s15", "Diana in her mustard jumper sits on a low wall beside her friend, who has curly brown hair, a sage-green cardigan and round glasses. Warm late afternoon light, both easy and unbothered."),
]

per = {}
for _, sid, _ in scenes_spec:
    per[sid] = per.get(sid, 0) + 1

sec_map = {s["id"]: s for s in sections}
scenes, seen = [], {}
for scid, sid, desc in scenes_spec:
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
        "narrative_role": "deliver_payload" if scid in ("sc10", "sc13") else "evidence",
        "hero_moment": scid in ("sc3", "sc10", "sc13", "sc18"),
        "transition_in": "cut", "transition_out": "cut",
        "shot_language": {"shot_size": "wide" if scid in ("sc1", "sc10") else "medium",
                          "camera_movement": "dolly_out" if scid == "sc10" else "static",
                          "lighting_key": "natural", "depth_of_field": "medium",
                          "color_temperature": "warm"},
        "overlay_notes": "No text in the illustration. Any lettering is added in composition."
    })

scene_plan = {
    "version": "1.0", "style_playbook": "custom-atelier-storybook",
    "scenes": scenes,
    "metadata": {
        "character_lock": "A girl of eight, Vietnamese-Australian, with straight black shoulder-length hair and a soft fringe, warm light skin, dark almond-shaped eyes and a round friendly face. She wears a mustard-yellow knitted jumper, a denim pinafore dress and red canvas shoes. Identical to film 1, appended verbatim to every prompt in which she appears.",
        "friend_lock": "The friend is a different child entirely: curly shoulder-length brown hair, a sage-green cardigan, a cream skirt and round glasses. She must never be mistakeable for Diana. Introducing a distinct second character with a locked description is the fix for the two-girls defects that appeared three times in film 1.",
        "one_child_rule": "Every frame contains exactly one child, except sc18 which deliberately shows both and where the two are visually unmistakeable.",
        "visual_signatures": {
            "fast_speed": "The same quick warm-gold streak as film 1.",
            "story_panels": "New to this film. Printed comic panels in gold ink for the first story, soft blue ink for the second, echoing the gold and blue of film 1.",
            "absence": "Blank unprinted panels. The visual answer to the hardest idea in the film."
        },
        "style_lock": "Unchanged from film 1. Soft gouache, warm cream paper with visible grain, rounded shapes, muted palette, gold and blue as the only accents.",
        "scene_count": len(scenes),
        "generation_order": "All eighteen generated, then reviewed together as a single contact sheet before any render."
    }
}
validate(scene_plan, "scene_plan")
print("sections:", len(sections), "scenes:", len(scenes),
      "words:", script["metadata"]["word_count_approx"],
      "provisional:", script["total_duration_seconds"], "s")
