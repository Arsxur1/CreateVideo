"""One-shot: build the pre-production artifacts for film 2, The Story Machine."""
import json
import jsonschema
from pathlib import Path

PROJ = Path("projects/diana-story-machine")
(PROJ / "artifacts").mkdir(parents=True, exist_ok=True)


def validate(obj, name):
    schema = json.load(open(f"schemas/artifacts/{name}.schema.json", encoding="utf-8"))
    jsonschema.validate(obj, schema)
    json.dump(obj, open(PROJ / f"artifacts/{name}.json", "w", encoding="utf-8"), indent=2)
    print(f"{name} SCHEMA-VALID")


research = {
    "version": "1.0",
    "topic": "WYSIATI from Thinking, Fast and Slow, told for an 8-year-old as the story her brain writes about other people",
    "research_date": "2026-09-09",
    "research_summary": (
        "Film 2 of a planned series. The landscape work was done for film 1 and holds: children's explainers "
        "work when character-driven, paired with imagery, with built-in pauses, and age 8-9 is when children "
        "begin regulating emotion through thoughts about their feelings. This film narrows to Chapter 7, WYSIATI. "
        "Kahneman's claim is that System 1 builds the most coherent story available from whatever happens to be "
        "activated and never registers what is missing, so confidence tracks story coherence rather than evidence "
        "quality. For a child this is the single highest-value idea in the book, because it governs playground "
        "social life, where a one-second misreading of a friend becomes a settled belief. The landscape scan for "
        "film 1 found no children's content covering this at all, which remains the largest underserved gap."
    ),
    "landscape": {
        "existing_content": [
            {"title": "Jane the Brain (NIMH)", "url": "https://www.nimh.nih.gov/get-involved/science-education/video-series-jane-the-brain",
             "source": "government site", "angle": "Animated character handles big feelings",
             "what_it_covers": "Naming and coping with feelings; does not cover how beliefs about other people form"},
            {"title": "Dr. Dan Siegel's Hand Model of the Brain", "url": "https://www.youtube.com/watch?v=Kx7PCzg0CGE",
             "source": "youtube", "angle": "Hand as brain model",
             "what_it_covers": "Emotional regulation under stress; silent on social inference"},
            {"title": "The Decision Lab - System 1 and System 2", "url": "https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking",
             "source": "reference site", "angle": "Adult reference explainer",
             "what_it_covers": "WYSIATI described for adults only"}
        ],
        "saturated_angles": [
            "Generic children's content about being kind and assuming the best, with no mechanism given",
            "Adult-facing cognitive bias listicles"
        ],
        "underserved_gaps": [
            "The mechanism, not the moral. Children are told to assume the best but never told why their brain assumes the worst so fast",
            "Confidence as a feeling produced by tidiness rather than by evidence",
            "A usable move a child can actually perform in the moment"
        ]
    },
    "data_points": [
        {"claim": "System 1 builds the most coherent story available from whatever information is activated, and never registers what is missing.",
         "source_url": "https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking",
         "source_name": "Thinking, Fast and Slow, Ch 7", "credibility": "secondary_source",
         "surprise_factor": "counterintuitive", "usable_as": "core concept spine"},
        {"claim": "Confidence tracks the coherence of the story rather than the quality or quantity of the evidence behind it.",
         "source_url": "https://www.sparknotes.com/lit/thinking-fast-and-slow/section1/",
         "source_name": "Thinking, Fast and Slow, Ch 7", "credibility": "secondary_source",
         "surprise_factor": "counterintuitive", "usable_as": "the turn in the middle of the film"},
        {"claim": "A smaller, tidier story can feel more probable than a larger, messier one even when the messier one is correct.",
         "source_url": "https://www.sparknotes.com/lit/thinking-fast-and-slow/section1/",
         "source_name": "Thinking, Fast and Slow, Ch 7 and 15", "credibility": "secondary_source",
         "surprise_factor": "surprising", "usable_as": "why the wrong story wins"},
        {"claim": "By age 8 to 9 children already regulate emotion through thoughts about their own feelings, so a cognitive move is age-appropriate.",
         "source_url": "https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/bjep.12305",
         "source_name": "Pennequin et al., British Journal of Educational Psychology (2020)",
         "credibility": "primary_source", "surprise_factor": "notable",
         "usable_as": "justifies ending on a thinking tool rather than a feeling label"}
    ],
    "audience_insights": {
        "knowledge_level": "Age 8. Has seen film 1 and already owns the phrase fast one and slow one. No other vocabulary assumed.",
        "common_questions": [
            "Why did I think my friend was being mean when she wasn't?",
            "Why was I so sure and so wrong?",
            "How do I stop deciding things about people too fast?"
        ],
        "misconceptions": [
            {"myth": "If I feel certain about why someone did something, I must have good reasons",
             "reality": "Certainty is produced by the story hanging together neatly, not by how much you actually know.",
             "source": "Ch 7"},
            {"myth": "My brain tells me when it is missing information",
             "reality": "It does not. It builds the best story from what is present and never flags the gaps.",
             "source": "Ch 7"},
            {"myth": "Thinking badly of a friend for a moment means I am a bad friend",
             "reality": "The first story is machinery, not character. What she does with it is the part she chooses.",
             "source": "Ch 7 plus film 1 framing"}
        ],
        "pain_points": [
            "Being told to assume the best without being told why the worst arrives first",
            "Shame after being confidently wrong about a friend"
        ]
    },
    "angles_discovered": [
        {"name": "The Story Machine", "type": "narrative",
         "hook": "Diana waved across the playground. Her friend did not wave back. One second later the whole story was written.",
         "why_now": "Directly answers the sharpest question in the audience set and fills the biggest gap in the children's landscape.",
         "grounded_in": ["Ch 7 WYSIATI", "film 1 established the fast one vocabulary"]},
        {"name": "The Missing Panels", "type": "evergreen",
         "hook": "Your brain printed four panels and hid the fact that there were twenty.",
         "why_now": "Makes the invisible absence visible, which is the hard part of teaching WYSIATI to anyone.",
         "grounded_in": ["Ch 7, the mind never registers what is missing"]},
        {"name": "Sure Is Not the Same as Right", "type": "contrarian",
         "hook": "Feeling sure is just the story being tidy.",
         "why_now": "The most transferable idea in the book and the one adults get wrong too.",
         "grounded_in": ["Ch 7, confidence tracks coherence"]}
    ],
    "expert_voices": [
        {"name": "Daniel Kahneman", "title_or_affiliation": "Nobel laureate, author",
         "position": "What you see is all there is. The mind builds a coherent story from available scraps and does not register absence.",
         "source_url": "https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking",
         "contrarian": False}
    ],
    "sources": [
        {"url": "https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking",
         "title": "System 1 and System 2 Thinking - The Decision Lab", "used_for": "WYSIATI definition", "reliability": "secondary"},
        {"url": "https://www.sparknotes.com/lit/thinking-fast-and-slow/section1/",
         "title": "Thinking, Fast and Slow Part I Summary", "used_for": "Chapter 7 content and coherence claim", "reliability": "secondary"},
        {"url": "https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/bjep.12305",
         "title": "Metacognition and emotional regulation in children 8 to 12", "used_for": "Age appropriateness of a cognitive move", "reliability": "primary"},
        {"url": "https://www.nimh.nih.gov/get-involved/science-education/video-series-jane-the-brain",
         "title": "Jane the Brain - NIMH", "used_for": "Format benchmark for the age band", "reliability": "primary"},
        {"url": "https://www.scholastic.com/parents/family-life/social-emotional-learning/development-milestones/emotional-lives-8-10-year-olds.html",
         "title": "Social and Emotional Lives of 8- to 10-Year-Olds", "used_for": "Social salience of peer misreadings", "reliability": "secondary"}
    ],
    "metadata": {
        "series": "Film 2 of a planned 18-film series adapting Thinking, Fast and Slow for one 8-year-old.",
        "reuses_research_from": "projects/diana-fast-slow-brain/artifacts/research_brief.json",
        "excluded_claims": ["Nothing from the priming or ego-depletion chapters, which failed replication."]
    }
}
validate(research, "research_brief")

proposal = {
    "version": "1.0",
    "concept_options": [
        {"id": "c1", "title": "The Story Machine",
         "hook": "Diana waved at her friend right across the playground. And her friend did not wave back.",
         "narrative_structure": "story",
         "visual_approach": "The established storybook world and the same girl. New device for this film: her thoughts print as comic panels on the cream page, four tidy panels that arrive instantly, then the frame pulls back to reveal a wall of blank panels she never saw. The gold streak from film 1 returns as the printer.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old, watched with her dad",
         "target_platform": "generic", "target_duration_seconds": 200,
         "key_points": [
             "One second of evidence becomes a complete, confident story",
             "The machine only uses what it can see and never counts what is missing",
             "The real reason was ordinary and kind, and she never had access to it",
             "Feeling sure comes from the story being tidy, not from knowing enough",
             "The move: ask for a second story"],
         "core_message": "Your brain writes a whole story from almost nothing and hides the gaps. Being sure is not the same as being right, and you can always ask for another story.",
         "cta": "Next time you are certain why somebody did something, stop and ask what else could be true.",
         "tone": "Warm, curious, a little bit detective. Same parent voice as film 1.",
         "why_this_works": "It is the largest gap in the children's content landscape, it answers the sharpest question in the audience set, and it builds directly on the fast one vocabulary film 1 established rather than starting from zero.",
         "grounded_in": ["Ch 7 WYSIATI", "audience question about misreading a friend"]},
        {"id": "c2", "title": "Sure Is Not the Same as Right",
         "hook": "How sure are you? And how much do you actually know? Those are two different questions.",
         "narrative_structure": "myth_busting",
         "visual_approach": "Two meters side by side, one for how sure she feels and one for how much she knows, moving independently.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 170,
         "key_points": ["Certainty and knowledge are separate", "Tidy stories feel truer", "Check the second meter"],
         "core_message": "Certainty is a feeling, not a measurement.",
         "cta": "Ask how much you actually know, separately from how sure you feel.",
         "tone": "Curious and slightly playful",
         "why_this_works": "The most transferable single idea, but abstract without a story to hang it on, which is why it becomes the middle act of c1 instead.",
         "grounded_in": ["Ch 7, confidence tracks coherence"]},
        {"id": "c3", "title": "The Missing Panels",
         "hook": "Your brain printed four pictures. There were twenty. It never mentioned the other sixteen.",
         "narrative_structure": "comparison",
         "visual_approach": "Comic panels only, no playground story, a formal exercise in presence and absence.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 150,
         "key_points": ["What is present feels like everything", "Absence is invisible", "Look for the blanks"],
         "core_message": "You cannot see what you were never shown.",
         "cta": "Ask what you have not been shown.",
         "tone": "Cool and formal",
         "why_this_works": "Cleanest expression of the mechanism, but too abstract to open with at this age, so it becomes the visual centrepiece of c1.",
         "grounded_in": ["Ch 7, the mind never registers what is missing"]}
    ],
    "selected_concept": {
        "concept_id": "c1",
        "rationale": "c1 opens on a real playground moment she has lived, then absorbs both other concepts as its middle and its turn. c2 and c3 are each true but land as lessons rather than stories, which is the failure mode for this age.",
        "modifications": ["Carries every production decision approved for film 1 unchanged",
                          "Adds one new visual device, printed comic panels, for this film only"]
    },
    "production_plan": {
        "pipeline": "animated-explainer", "playbook": "custom-atelier-storybook",
        "renderer_family": "explainer-teacher", "render_runtime": "remotion", "composition_mode": "atelier",
        "delivery_promise": {"promise_type": "teacher_explainer", "motion_required": False,
                             "source_required": False, "tone_mode": "intimate and curious, a bedtime storybook read aloud",
                             "quality_floor": "presentable", "approved_fallback": "still_led"},
        "art_direction": "Identical to film 1 so the series reads as one thing: warm cream gouache, one recurring girl, gold streak for the fast way of thinking, blue glow for the slow one. New for this film only: her thoughts print as comic panels on the page.",
        "taste_profile": {
            "design_read": "The same bedtime picture book, one chapter later",
            "visual_variance": 8, "motion_intensity": 3, "information_density": 2,
            "palette_discipline": "Unchanged from film 1. Cream ground, muted warm palette, gold and blue as the only accents.",
            "layout_variation": "Every scene composed for its own beat. The panel device gives this film its own geometry without breaking the house style.",
            "reference_strategy": "Series continuity with film 1 is the reference. No external imitation.",
            "anti_patterns": ["two children in one frame, which caused three defects in film 1",
                              "asking the image model for an exact count of anything",
                              "corporate infographic furniture",
                              "any frame implying she was unkind for having the first thought"],
            "quality_gates": ["Contact sheet of every illustration reviewed together before render",
                              "Exactly one child in every frame unless an adult is deliberately present and clearly adult",
                              "Any countable object drawn in composition code, never by the image model"]
        },
        "music_source": {"source_type": "ai_generated", "provider": "reused from film 1 (Google Lyria)",
                         "mood_direction": "Identical bed to film 1, deliberately, so the series has one sound.",
                         "estimated_cost_usd": 0.0},
        "voice_selection": {"provider": "elevenlabs", "voice_id": "JBFqnCBsd6RMkjVDRZzb",
                            "rationale": "Same warm storyteller voice as film 1. Series continuity outweighs per-film optimisation. Daniel recording it himself remains the better option and can still be swapped in.",
                            "estimated_cost_usd": 0.95,
                            "delivery_style": "warm parent reading a bedtime story, unhurried",
                            "pacing_policy": "Slow, roughly 110 words per minute, with three deliberate silences where the narrator asks and waits.",
                            "sample_approval_required": False},
        "stages": [
            {"stage": "script", "approach": "Roughly 440 words at an 8-year-old listening level, three pause beats, opening on a lived playground moment.", "tools": []},
            {"stage": "scene_plan", "approach": "Around 18 scenes, one idea each, with the panel device carrying the middle act.", "tools": []},
            {"stage": "assets", "approach": "Illustrations from the same model with the same verbatim character lock; narration from the same voice; music reused from film 1.",
             "tools": [{"tool_name": "google_imagen", "role": "illustration", "available": True},
                       {"tool_name": "elevenlabs_tts", "role": "narration", "available": True}]},
            {"stage": "edit", "approach": "Timeline rebuilt from measured narration durations, as in film 1.", "tools": []},
            {"stage": "compose", "approach": "Atelier Remotion render at 1920x1080 reusing film 1's composition with this film's props.",
             "tools": [{"tool_name": "video_compose", "role": "render", "available": True}]}
        ],
        "quality_tradeoffs": [
            {"tradeoff": "Reusing film 1's composition code and visual language versus authoring a fresh look",
             "recommendation": "Reuse", "quality_impact": "Breaks the atelier rule against reusing creative components, deliberately. For a series the recurring look is the product, not a failure of imagination."},
            {"tradeoff": "Reusing film 1's music bed versus generating a new one",
             "recommendation": "Reuse", "quality_impact": "Saves cost and gives the series one sound. A new bed per film would make eighteen films feel like eighteen unrelated videos."}
        ],
        "alternative_paths": [
            {"description": "Fresh visual language for this film", "total_cost_usd": 1.1, "quality_level": "premium"},
            {"description": "Reuse everything from film 1, change only script, images and narration", "total_cost_usd": 1.67, "quality_level": "standard"}
        ]
    },
    "cost_estimate": {
        "total_estimated_usd": 1.67, "budget_cap_usd": 2.5, "budget_verdict": "within_budget",
        "line_items": [
            {"tool": "google_imagen", "operation": "storybook illustrations", "quantity": 18, "estimated_usd": 0.72, "notes": "0.04 USD per image"},
            {"tool": "elevenlabs_tts", "operation": "narration, approx 3200 characters", "quantity": 1, "estimated_usd": 0.95, "notes": "Zero if Daniel records it"},
            {"tool": "video_compose", "operation": "local render", "quantity": 1, "estimated_usd": 0.0, "notes": "No API cost"}
        ],
        "savings_options": ["Daniel records the narration: removes 0.95 USD",
                            "Music reused from film 1 rather than regenerated: already saves 0.08 USD"]
    },
    "approval": {"status": "approved", "approved_budget_usd": 2.5,
                 "user_notes": "User replied go, selecting film 2 from the eighteen-film series plan. All production decisions carry over from film 1, which was approved and delivered."},
    "metadata": {
        "series_position": "2 of 18",
        "carried_over_from_film_1": ["character lock", "style lock", "voice", "render runtime", "composition mode", "music bed"],
        "new_this_film": ["printed comic panel device", "playground world as the primary setting"],
        "lessons_applied_from_film_1": [
            "One child per frame, enforced in every prompt, because three separate defects in film 1 came from two-figure compositions",
            "Nothing countable generated by the image model",
            "Contact sheet review of all illustrations before rendering",
            "Staged Remotion entry must be re-copied after every edit"
        ]
    }
}
validate(proposal, "proposal_packet")
print("done")
