"""One-shot: build film 3, What Comes to Mind First (availability heuristic)."""
import json
import re
import subprocess
import sys
from pathlib import Path

import jsonschema

from tools.tool_registry import registry

SLUG = "diana-availability"
PROJ = Path("projects") / SLUG
(PROJ / "artifacts").mkdir(parents=True, exist_ok=True)


def validate(obj, name):
    schema = json.load(open(f"schemas/artifacts/{name}.schema.json", encoding="utf-8"))
    jsonschema.validate(obj, schema)
    json.dump(obj, open(PROJ / f"artifacts/{name}.json", "w", encoding="utf-8"), indent=2)
    print(f"{name} SCHEMA-VALID", flush=True)


research = {
    "version": "1.0",
    "topic": "The availability heuristic from Thinking, Fast and Slow, told for an 8-year-old as why she is frightened of the wrong things",
    "research_date": "2026-09-09",
    "research_summary": (
        "Film 3 of the series. Chapters 12 and 13. Kahneman's claim is that people judge frequency and "
        "probability by the ease with which instances come to mind, and that the ease of retrieval matters "
        "more than the instances retrieved. Retrieval is distorted by vividness, recency and personal "
        "involvement, so frightening single events dominate hundreds of uneventful ones. For a child this "
        "explains a specific and common distress: one barking dog making every dog frightening, one bad "
        "moment in deep water making swimming frightening. The film deliberately avoids all harm statistics "
        "and comparative-danger claims, which are the standard adult framing and are unsuitable here."
    ),
    "landscape": {
        "existing_content": [
            {"title": "Jane the Brain (NIMH)", "url": "https://www.nimh.nih.gov/get-involved/science-education/video-series-jane-the-brain",
             "source": "government site", "angle": "Coping with big feelings",
             "what_it_covers": "Naming fear and calming down; does not explain why a specific fear formed"},
            {"title": "General children's anxiety guidance", "url": "https://www.scholastic.com/parents/family-life/social-emotional-learning/development-milestones/emotional-lives-8-10-year-olds.html",
             "source": "web", "angle": "Reassurance and coping strategies",
             "what_it_covers": "What to do with fear, not where a disproportionate fear came from"},
            {"title": "The Decision Lab - System 1 and System 2", "url": "https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking",
             "source": "reference site", "angle": "Adult reference explainer",
             "what_it_covers": "Availability described accurately but for adults, using risk statistics unsuitable for a child"}
        ],
        "saturated_angles": ["Breathing and calming techniques", "Generic be-brave messaging"],
        "underserved_gaps": [
            "The mechanism behind a disproportionate fear, explained without dismissing the fear",
            "A counting move a child can perform instead of a feeling move",
            "Explaining that quiet uneventful memories are barely stored, so the evidence she can reach is biased"
        ]
    },
    "data_points": [
        {"claim": "People judge frequency and probability by how easily instances come to mind, and the ease of retrieval matters more than the instances actually retrieved.",
         "source_url": "https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking",
         "source_name": "Thinking, Fast and Slow, Ch 12", "credibility": "secondary_source",
         "surprise_factor": "counterintuitive", "usable_as": "core concept spine"},
        {"claim": "Retrieval is distorted by vividness, recency, personal involvement and emotional salience, so dramatic single events crowd out ordinary repeated ones.",
         "source_url": "https://www.sparknotes.com/lit/thinking-fast-and-slow/section1/",
         "source_name": "Thinking, Fast and Slow, Ch 12 and 13", "credibility": "secondary_source",
         "surprise_factor": "notable", "usable_as": "why the barking dog wins over a hundred quiet dogs"},
        {"claim": "Emotion drives risk perception, so how frightening something feels substitutes for how often it happens.",
         "source_url": "https://www.sparknotes.com/lit/thinking-fast-and-slow/section1/",
         "source_name": "Thinking, Fast and Slow, Ch 13, the affect heuristic",
         "credibility": "secondary_source", "surprise_factor": "notable",
         "usable_as": "links back to film 1's feeling-arrives-first idea"},
        {"claim": "By age 8 to 9 children regulate emotion through thoughts about their feelings, so a counting instruction is developmentally usable.",
         "source_url": "https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/bjep.12305",
         "source_name": "Pennequin et al., British Journal of Educational Psychology (2020)",
         "credibility": "primary_source", "surprise_factor": "expected",
         "usable_as": "justifies ending on a counting question rather than a calming technique"}
    ],
    "audience_insights": {
        "knowledge_level": "Age 8. Has seen films 1 and 2 and owns the phrases fast one and story machine.",
        "common_questions": [
            "Why am I still scared of dogs when nothing bad has happened since?",
            "Why does one bad time feel like it happens all the time?",
            "Why can I not just stop being scared?"
        ],
        "misconceptions": [
            {"myth": "If something feels very likely, it must happen often",
             "reality": "Ease of remembering, not frequency, is what the feeling is actually measuring.", "source": "Ch 12"},
            {"myth": "I remember roughly everything that has happened to me",
             "reality": "Quiet uneventful events are barely stored, so the memories available to you are a biased sample.", "source": "Ch 12"},
            {"myth": "Being scared of something harmless means something is wrong with me",
             "reality": "It is the ordinary result of how memory is packed. Loud memories sit at the front.", "source": "Ch 12 and 13"}
        ],
        "pain_points": [
            "Being told there is nothing to be scared of, which does not touch the mechanism",
            "Shame about a fear she knows is out of proportion"
        ]
    },
    "angles_discovered": [
        {"name": "One Barking Dog", "type": "narrative",
         "hook": "One dog barked at her once, years ago. Every dog since has been a little bit scary.",
         "why_now": "Concrete, near-universal at this age, and it makes the mechanism visible without frightening content.",
         "grounded_in": ["Ch 12 availability", "Ch 13 vividness and emotion"]},
        {"name": "The Memory Shelf", "type": "evergreen",
         "hook": "Loud memories sit at the front of the shelf. Quiet ones are in a box at the back under a blanket.",
         "why_now": "Gives a child a physical model of a retrieval bias, otherwise very hard to picture.",
         "grounded_in": ["Ch 12, ease of retrieval"]},
        {"name": "Ask It To Count", "type": "contrarian",
         "hook": "Do not ask how scary it feels. Ask how many times it has actually happened.",
         "why_now": "Replaces a feeling question with a counting question, which is the corrective and is age-appropriate.",
         "grounded_in": ["Ch 12", "Pennequin on metacognition at 8 to 9"]}
    ],
    "expert_voices": [
        {"name": "Daniel Kahneman", "title_or_affiliation": "Nobel laureate, author",
         "position": "Frequency is judged by ease of retrieval, and the ease matters more than what is retrieved.",
         "source_url": "https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking",
         "contrarian": False}
    ],
    "sources": [
        {"url": "https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking",
         "title": "System 1 and System 2 Thinking - The Decision Lab", "used_for": "Availability definition", "reliability": "secondary"},
        {"url": "https://www.sparknotes.com/lit/thinking-fast-and-slow/section1/",
         "title": "Thinking, Fast and Slow Summary", "used_for": "Chapters 12 and 13", "reliability": "secondary"},
        {"url": "https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/bjep.12305",
         "title": "Metacognition and emotional regulation in children 8 to 12", "used_for": "Age appropriateness", "reliability": "primary"},
        {"url": "https://www.nimh.nih.gov/get-involved/science-education/video-series-jane-the-brain",
         "title": "Jane the Brain - NIMH", "used_for": "Format benchmark", "reliability": "primary"},
        {"url": "https://www.scholastic.com/parents/family-life/social-emotional-learning/development-milestones/emotional-lives-8-10-year-olds.html",
         "title": "Social and Emotional Lives of 8- to 10-Year-Olds", "used_for": "Fear salience at this age", "reliability": "secondary"}
    ],
    "metadata": {
        "series": "Film 3 of 18.",
        "excluded_claims": [
            "All comparative danger statistics. Telling a child that one thing hurts more people than another is the adult framing and is unsuitable here.",
            "Availability cascades and media-driven risk, which are adult political content.",
            "Anything from the priming or ego-depletion chapters."
        ]
    }
}
validate(research, "research_brief")

proposal = {
    "version": "1.0",
    "concept_options": [
        {"id": "c1", "title": "What Comes to Mind First",
         "hook": "When Diana was five, a big dog barked at her. Just once. And every dog since has been a little bit scary.",
         "narrative_structure": "story",
         "visual_approach": "The established storybook world. New device: a memory shelf where loud bright memories sit at the front within easy reach and hundreds of pale quiet ones are boxed at the back under a blanket. The gold streak returns, reaching only the front row.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old, watched with her dad",
         "target_platform": "generic", "target_duration_seconds": 190,
         "key_points": ["One loud memory outweighs a hundred quiet ones",
                        "Quiet ordinary events are barely stored at all",
                        "The fast one answers how likely by checking how easily it can picture it",
                        "Easy to remember and likely to happen are two different things",
                        "The move: ask a counting question instead of a feeling question"],
         "core_message": "Your brain keeps the loud memories and loses the quiet ones, so frightening things feel far more common than they are. Ask it to count.",
         "cta": "When something feels frightening, ask how many times it has actually happened to you.",
         "tone": "Warm and gentle. Never dismissive of the fear.",
         "why_this_works": "Near-universal at this age, answers the sharpest audience question, and replaces a feeling instruction with a counting one, which the developmental research supports at 8 to 9.",
         "grounded_in": ["Ch 12 availability", "Ch 13 vividness"]},
        {"id": "c2", "title": "The Memory Shelf",
         "hook": "Some memories sit at the front. Most are in a box at the back, under a blanket.",
         "narrative_structure": "analogy",
         "visual_approach": "The shelf alone, no dog story, as a formal object study.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 150,
         "key_points": ["Loud memories are reachable", "Quiet ones are not stored", "Reachable is not the same as common"],
         "core_message": "What you can reach is not what is true.", "cta": "Look for the memories you cannot reach.",
         "tone": "Cool and curious",
         "why_this_works": "Cleanest model of the mechanism, but abstract without a fear attached, so it becomes the middle act of c1.",
         "grounded_in": ["Ch 12 ease of retrieval"]},
        {"id": "c3", "title": "Ask It To Count",
         "hook": "Do not ask how scary it feels. Ask how many times it has really happened.",
         "narrative_structure": "tutorial",
         "visual_approach": "A counting exercise on the cream page, tally marks appearing.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 130,
         "key_points": ["Feeling questions give feeling answers", "Counting questions give counts", "Usually the answer is once"],
         "core_message": "Swap the question.", "cta": "Count instead of feeling.", "tone": "Practical",
         "why_this_works": "The most directly useful of the three, but lands as an instruction without the story, so it becomes the final act of c1.",
         "grounded_in": ["Ch 12 corrective"]}
    ],
    "selected_concept": {
        "concept_id": "c1",
        "rationale": "c1 opens on a fear she recognises, then absorbs both other concepts as its middle and its ending. The others are true but arrive as lessons rather than as a story, which is the failure mode at this age.",
        "modifications": ["All production decisions carry over from films 1 and 2",
                          "New device: the memory shelf", "No comparative danger statistics anywhere"]
    },
    "production_plan": {
        "pipeline": "animated-explainer", "playbook": "custom-atelier-storybook",
        "renderer_family": "explainer-teacher", "render_runtime": "remotion", "composition_mode": "atelier",
        "delivery_promise": {"promise_type": "teacher_explainer", "motion_required": False, "source_required": False,
                             "tone_mode": "intimate and gentle, a bedtime storybook read aloud",
                             "quality_floor": "presentable", "approved_fallback": "still_led"},
        "art_direction": "Unchanged from films 1 and 2. Warm cream gouache, one recurring girl, gold streak for the fast way of thinking. New device: the memory shelf, front row warm and bright, back rows pale and boxed.",
        "taste_profile": {
            "design_read": "The same bedtime picture book, two chapters on",
            "visual_variance": 8, "motion_intensity": 3, "information_density": 2,
            "palette_discipline": "Unchanged. Cream ground, muted warm palette, gold and blue as the only accents.",
            "layout_variation": "Each scene composed for its beat. The shelf gives this film its own geometry.",
            "reference_strategy": "Series continuity only.",
            "anti_patterns": ["two children in one frame", "asking the image model for an exact count",
                              "any frightening or threatening depiction of the dog",
                              "harm statistics or comparative danger", "implying the fear is silly"],
            "quality_gates": ["Contact sheet of all illustrations reviewed before render",
                              "The dog is never menacing, only loud in the single memory",
                              "Countable objects drawn in composition code, not by the image model"]
        },
        "music_source": {"source_type": "ai_generated", "provider": "reused from film 1 (Google Lyria)",
                         "mood_direction": "The same bed as films 1 and 2, for one series sound.",
                         "estimated_cost_usd": 0.0},
        "voice_selection": {"provider": "elevenlabs", "voice_id": "JBFqnCBsd6RMkjVDRZzb",
                            "rationale": "The same warm storyteller voice as films 1 and 2.",
                            "estimated_cost_usd": 0.85,
                            "delivery_style": "warm parent reading a bedtime story, extra gentle around the fear",
                            "pacing_policy": "Roughly 110 words per minute with three genuine silences.",
                            "sample_approval_required": False},
        "stages": [
            {"stage": "script", "approach": "Around 380 words at an 8-year-old listening level, three pause beats.", "tools": []},
            {"stage": "scene_plan", "approach": "Eighteen scenes, one idea each, the shelf carrying the middle act.", "tools": []},
            {"stage": "assets", "approach": "Same image model and character lock, same voice, music reused.",
             "tools": [{"tool_name": "google_imagen", "role": "illustration", "available": True},
                       {"tool_name": "elevenlabs_tts", "role": "narration", "available": True}]},
            {"stage": "edit", "approach": "Timeline rebuilt from measured narration durations.", "tools": []},
            {"stage": "compose", "approach": "Atelier Remotion render reusing the series composition.",
             "tools": [{"tool_name": "video_compose", "role": "render", "available": True}]}
        ],
        "quality_tradeoffs": [
            {"tradeoff": "Using a dog as the fear versus a neutral invented example",
             "recommendation": "Dog", "quality_impact": "Concrete and near-universal. Mitigated by never drawing the dog as menacing outside the single remembered bark."},
            {"tradeoff": "Including comparative danger facts versus omitting them",
             "recommendation": "Omit", "quality_impact": "The adult version leans on risk statistics. For a child those are frightening and unnecessary, so the film teaches the mechanism without any."}
        ],
        "alternative_paths": [
            {"description": "Neutral invented fear instead of dogs", "total_cost_usd": 1.57, "quality_level": "standard"},
            {"description": "Reuse everything from films 1 and 2", "total_cost_usd": 1.57, "quality_level": "standard"}
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
                 "user_notes": "User replied next, selecting film 3 from the series plan. All production decisions carry over from films 1 and 2."},
    "metadata": {"series_position": "3 of 18",
                 "carried_over": ["character lock", "style lock", "voice", "runtime", "composition mode", "music bed"],
                 "new_this_film": ["memory shelf device"]}
}
validate(proposal, "proposal_packet")

S = [
    ("s1", "The one dog",
     "When Diana was five, a big dog barked at her. Just once. One dog. One bark. A very long time ago.",
     'When Diana was five, a big dog barked at her. <break time="0.5s"/> Just once. <break time="0.4s"/> One dog. One bark. <break time="0.4s"/> A very long time ago.',
     1.2, "measured", "gentle", ["once"], "Matter of fact and kind. Not spooky."),
    ("s2", "Every dog since",
     "And ever since then, every single dog has been a little bit scary.",
     'And ever since then, <break time="0.4s"/> every single dog has been a little bit scary.',
     1.4, "slow", "tender", ["every"], "No judgement at all in this line."),
    ("s3", "How many dogs",
     "So here is a question. How many dogs have you met in your whole life?",
     'So here is a question. <break time="0.5s"/> How many dogs have you met in your whole life? <break time="2.5s"/>',
     2.5, "slow", "curious", ["many"], "Pause beat one. Let her try to count."),
    ("s4", "Hundreds",
     "Hundreds, probably. Dogs in parks. Dogs on leads. Dogs asleep on doorsteps. Hundreds and hundreds of dogs that did absolutely nothing at all.",
     'Hundreds, probably. <break time="0.4s"/> Dogs in parks. Dogs on leads. Dogs asleep on doorsteps. <break time="0.5s"/> Hundreds and hundreds of dogs that did absolutely nothing at all.',
     1.0, "conversational", "warm", ["nothing"], "Light and rolling. The list should feel long."),
    ("s5", "Can you remember them",
     "Can you remember a single one of them?",
     'Can you remember a single one of them? <break time="2.5s"/>',
     2.5, "slow", "curious", ["single"], "Pause beat two. She will find nothing, which is the point."),
    ("s6", "Quiet things do not stick",
     "Of course not. They were quiet. And quiet things do not stick.",
     'Of course not. <break time="0.5s"/> They were quiet. <break time="0.4s"/> And quiet things do not stick.',
     1.2, "slow", "gentle", ["quiet"], "Warm, almost consoling."),
    ("s7", "The shelf",
     "Your brain has a shelf. And it keeps the loud memories right at the front, where you can reach them without even trying.",
     'Your brain has a shelf. <break time="0.5s"/> And it keeps the loud memories right at the front, where you can reach them without even trying.',
     1.2, "measured", "curious", ["loud"], "Introduce the object clearly."),
    ("s8", "Front and back",
     "The barking dog is at the front. The hundreds of sleeping dogs are somewhere at the back. In a box. Under a blanket.",
     'The barking dog is at the front. <break time="0.5s"/> The hundreds of sleeping dogs are somewhere at the back. <break time="0.4s"/> In a box. <break time="0.3s"/> Under a blanket.',
     1.4, "measured", "wry", ["front", "back"], "A little dry humour on the blanket."),
    ("s9", "What the fast one actually does",
     "Now here is the clever, annoying thing your fast one does. When you ask it, is this dangerous, it does not count anything at all. It just checks how easily it can picture it going wrong.",
     'Now here is the clever, annoying thing your fast one does. <break time="0.5s"/> When you ask it, is this dangerous, <break time="0.4s"/> it does not count anything at all. <break time="0.5s"/> It just checks how easily it can picture it going wrong.',
     1.4, "slow", "gentle", ["count", "picture"], "The hinge. Slow right down."),
    ("s10", "So dogs feel dangerous",
     "And the barking dog is very, very easy to picture. So dogs feel dangerous.",
     'And the barking dog is very, very easy to picture. <break time="0.5s"/> So dogs feel dangerous.',
     1.2, "measured", "steady", ["easy"], "Land it plainly."),
    ("s11", "It happens with everything",
     "It happens with everything. One wobbly moment in the deep end, and swimming feels scary. One person laughing, and it feels like everybody laughed.",
     'It happens with everything. <break time="0.4s"/> One wobbly moment in the deep end, and swimming feels scary. <break time="0.5s"/> One person laughing, and it feels like everybody laughed.',
     1.2, "measured", "tender", ["everybody"], "She will recognise at least one of these."),
    ("s12", "Two different things",
     "Easy to remember is not the same as likely to happen. They are two completely different things, and your brain muddles them up all day long.",
     'Easy to remember is not the same as likely to happen. <break time="0.6s"/> They are two completely different things, <break time="0.4s"/> and your brain muddles them up all day long.',
     1.4, "slow", "steady", ["different"], "The transferable idea."),
    ("s13", "The tool",
     "So when something feels frightening, do not ask how scary it feels. Ask it a counting question. How many times has this actually happened to me?",
     'So when something feels frightening, do not ask how scary it feels. <break time="0.5s"/> Ask it a counting question. <break time="0.5s"/> How many times has this actually happened to me? <break time="2.5s"/>',
     2.5, "measured", "encouraging", ["counting"], "Pause beat three. She should actually count."),
    ("s14", "Usually once",
     "Once. Usually the answer is once. Once, and a hundred quiet times you have completely forgotten.",
     'Once. <break time="0.4s"/> Usually the answer is once. <break time="0.5s"/> Once, and a hundred quiet times you have completely forgotten.',
     1.2, "slow", "warm", ["once"], "Gentle relief."),
    ("s15", "Landing",
     "Your brain keeps the loud ones and loses the quiet ones. That is not a mistake. That is just how the shelf is packed. But you can always ask it to count.",
     'Your brain keeps the loud ones and loses the quiet ones. <break time="0.5s"/> That is not a mistake. <break time="0.4s"/> That is just how the shelf is packed. <break time="0.6s"/> But you can always ask it to count.',
     0.0, "slow", "proud", ["mistake"], "End on absolution then agency. Then stop."),
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
    "version": "1.0", "title": "What Comes to Mind First",
    "total_duration_seconds": round(t, 2),
    "voice_performance": {
        "performance_intent": "The same parent and the same child, two chapters on. Extra gentleness around the fear itself: the narrator never suggests it is silly, only that it was built from a biased sample.",
        "pacing_profile": "contemplative",
        "energy_curve": "Quiet and matter of fact at the memory. Warm and rolling through the hundred forgotten dogs. Lowest and gentlest at the hinge. Ends on quiet reassurance rather than triumph.",
        "pause_policy": "Three genuine silences: counting the dogs she has met, failing to remember any, and counting how many times the frightening thing has really happened.",
        "sample_section_id": "s9",
        "provider_notes": {
            "all": "Roughly 110 words per minute. Section s9 is the hinge and the sample section.",
            "elevenlabs": "Same voice as films 1 and 2, George. Stability 0.75, similarity 0.9, style 0.15, speed 0.9.",
            "human_recording": "If Daniel records this, be careful not to sound amused during the first two sections."
        }
    },
    "sections": sections,
    "metadata": {
        "series_position": "3 of 18",
        "word_count_approx": sum(len(s["text"].split()) for s in sections),
        "target_wpm": 110,
        "reading_age": "Written for a listener of 8. The words availability, heuristic, bias and probability never appear.",
        "pause_beats": [
            {"section": "s3", "purpose": "She tries to count the dogs she has met"},
            {"section": "s5", "purpose": "She fails to remember any and notices the failure"},
            {"section": "s13", "purpose": "She actually counts a real frightening thing"}
        ],
        "grounded_in": {
            "s1_to_s6": "Ch 12, ease of retrieval and the non-storage of uneventful instances",
            "s7_to_s10": "Ch 12, retrieval fluency substituting for frequency",
            "s11_to_s12": "Ch 13, vividness and emotional salience distorting perceived risk",
            "s13_to_s15": "Ch 12 corrective, plus Pennequin on age-appropriate cognitive moves"
        },
        "accuracy_guardrails_applied": [
            "No comparative danger statistics anywhere.",
            "The fear is never described as silly, wrong or babyish.",
            "The dog is never depicted as menacing outside the single remembered bark.",
            "No claim that she can decide not to be frightened."
        ]
    }
}
validate(script, "script")

spec = [
    ("sc1", "s1", "A much younger girl of about five stands still on a footpath as a large friendly-looking dog barks once beside her. The dog is not menacing, only sudden and loud, with a small burst of gold lines to show the noise."),
    ("sc2", "s2", "The girl, now eight, walks past a small calm dog sitting quietly on a doorstep. She leans slightly away from it, wary, shoulders raised."),
    ("sc3", "s3", "The girl alone on the cream page, looking up and to the side, trying to count something in her head. Empty warm space around her."),
    ("sc4", "s4", "A long horizontal row of many different dogs across the cream page, all calm and ordinary: sleeping, sitting, walking on leads, dozing on doorsteps. No child in the picture."),
    ("sc5", "s5", "The girl alone with a completely empty pale cream space above her head where a memory would be. Nothing in it at all."),
    ("sc6", "s6", "Many small pale grey dog shapes drifting away and fading softly into the cream paper until they almost vanish. No child in the picture."),
    ("sc7", "s7", "A warm wooden shelf drawn on cream paper. On the front edge sit a few brightly coloured glowing objects, easy to reach. Behind them the shelf recedes into pale dimness. No people."),
    ("sc8", "s8", "The same wooden shelf. At the very front, one bright glowing object shaped like a small barking dog. Far at the back, a large plain cardboard box with a soft blanket draped over it. No people."),
    ("sc9", "s9", "The girl alone, and a quick warm-gold streak loops out from her and reaches only to the very front edge of the wooden shelf, never going deeper."),
    ("sc10", "s10", "One single bright glowing memory object shaped like a small barking dog, lit warmly and floating close to the front of the frame, very easy to see. No people."),
    ("sc11", "s11", "The girl at the edge of a swimming pool, one foot in the water, hesitating, the deep end painted a slightly deeper blue behind her."),
    ("sc12", "s11", "A classroom. One child at the far side laughs at something unrelated while another child looks down at her desk. Exactly two children, clearly different from one another."),
    ("sc13", "s12", "Two simple hand-drawn wooden signposts standing side by side on cream paper, pointing in completely different directions. No words or letters on them. No people."),
    ("sc14", "s12", "The girl alone looking thoughtfully at two wooden signposts, her head tilted."),
    ("sc15", "s13", "The girl alone, stopped still, holding up one hand with her fingers spread, deliberately beginning to count."),
    ("sc16", "s14", "One single bright warm object at the front of the cream page, and behind it a vast soft field of many tiny pale faded shapes stretching away, gently revealed. No people."),
    ("sc17", "s15", "The wooden shelf again, seen calmly and fully, the front row bright and the back rows now softly lit rather than dark. No people."),
    ("sc18", "s15", "The girl sitting comfortably on a doorstep beside a small calm sleeping dog, relaxed and unbothered, warm late afternoon light."),
]

per = {}
for _, sid, _ in spec:
    per[sid] = per.get(sid, 0) + 1
sec_map = {s["id"]: s for s in sections}
scenes, seen = [], {}
for scid, sid, desc in spec:
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
        "narrative_role": "deliver_payload" if scid in ("sc9", "sc16") else "evidence",
        "hero_moment": scid in ("sc8", "sc9", "sc16", "sc18"),
        "transition_in": "cut", "transition_out": "cut",
        "shot_language": {"shot_size": "wide" if scid in ("sc4", "sc16") else "medium",
                          "camera_movement": "dolly_out" if scid == "sc16" else "static",
                          "lighting_key": "natural", "depth_of_field": "medium", "color_temperature": "warm"},
        "overlay_notes": "No text in the illustration."
    })

scene_plan = {
    "version": "1.0", "style_playbook": "custom-atelier-storybook", "scenes": scenes,
    "metadata": {
        "character_lock": "A girl of eight, Vietnamese-Australian, straight black shoulder-length hair with a soft fringe, warm light skin, dark almond-shaped eyes, round friendly face. Mustard-yellow knitted jumper, denim pinafore dress, red canvas shoes. Identical to films 1 and 2.",
        "one_child_rule": "Every frame contains exactly one child except sc12, which has two clearly different children.",
        "dog_rule": "The dog is never drawn as menacing, snarling or threatening. In sc1 it is loud and sudden. Everywhere else it is calm, small and ordinary.",
        "visual_signatures": {"fast_speed": "The same warm-gold streak as films 1 and 2.",
                              "memory_shelf": "New to this film. A warm wooden shelf: bright reachable objects at the front, pale boxed ones at the back."},
        "style_lock": "Unchanged from films 1 and 2.",
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
YOUNGER = ("The child is the same girl but younger, about five, Vietnamese-Australian, straight black hair with a "
           "soft fringe, wearing a mustard-yellow jumper and a denim pinafore dress.")
STYLE = ("Children's picture-book illustration, soft gouache painting, warm cream paper background with visible "
         "paper grain, soft pencil linework, rounded organic shapes, muted warm palette, flat 2D storybook art, "
         "not 3D, no text, no lettering, no words, no numbers, no digits.")
ONE = "EXACTLY ONE CHILD in the frame, a single child alone. Do not draw two children."
NONE = "There are NO people at all in this picture."
KIND_DOG = "Any dog is friendly, soft and gentle looking, never snarling, never menacing, never frightening."

WITH_DIANA = {"sc2", "sc3", "sc5", "sc9", "sc11", "sc14", "sc15", "sc18"}
YOUNG = {"sc1"}
TWO_KIDS = {"sc12"}

img_dir = PROJ / "assets/images"
img_dir.mkdir(parents=True, exist_ok=True)
aud_dir = PROJ / "assets/audio"
aud_dir.mkdir(parents=True, exist_ok=True)
(PROJ / "assets/music").mkdir(parents=True, exist_ok=True)

print("=== illustrations ===", flush=True)
img_fail = []
by_id = {s["id"]: s for s in scenes}
for n in range(1, 19):
    sid = f"sc{n}"
    dest = img_dir / f"{sid}.png"
    if dest.exists() and dest.stat().st_size > 10000:
        print(f"[skip] {sid}", flush=True)
        continue
    parts = [STYLE]
    if sid in YOUNG:
        parts += [ONE, YOUNGER, KIND_DOG]
    elif sid in WITH_DIANA:
        parts += [ONE, DIANA, KIND_DOG]
    elif sid in TWO_KIDS:
        parts += ["Exactly two children, clearly different from one another.", DIANA]
    else:
        parts += [NONE, KIND_DOG]
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
    dest = aud_dir / f"{sid}.mp3"
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
         "titles": [{"kind": "title", "text": "What Comes to Mind First",
                     "startSec": round(last["startSec"] + 1.0, 3),
                     "durSec": round(max(2.0, last["durSec"] - 1.0), 3)}]}
(PROJ / "composition").mkdir(parents=True, exist_ok=True)
json.dump(props, open(PROJ / "composition/props.json", "w", encoding="utf-8"), indent=2)

print(f"\nDONE images_failed={img_fail} narration_failed={aud_fail}")
print(f"total {TOTAL}s ({int(TOTAL//60)}m {TOTAL%60:.1f}s) frames={props['durationInFrames']} scenes={len(pscenes)} captions={len(captions)}")
sys.exit(0 if not img_fail and not aud_fail else 1)
