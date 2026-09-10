"""One-shot: write the awaiting_human proposal checkpoint with a full decision log."""
import json
from pathlib import Path
from lib.checkpoint import write_checkpoint

packet = json.load(open("projects/diana-fast-slow-brain/artifacts/proposal_packet.json", encoding="utf-8"))

decision_log = {
    "version": "1.0",
    "project_id": "diana-fast-slow-brain",
    "decisions": [
        {
            "decision_id": "d1-pipeline",
            "stage": "proposal",
            "category": "pipeline_selection",
            "subject": "Production pipeline",
            "options_considered": [
                {"option_id": "animated-explainer", "label": "animated-explainer", "score": 0.9,
                 "reason": "Production-stable, topic-to-generated-explainer, research-first with approval gates. Matches a fully generated illustrated piece with narration."},
                {"option_id": "animation", "label": "animation (motion-graphics first)", "score": 0.6,
                 "reason": "Production-stable and animation-led.",
                 "rejected_because": "Motion-graphics-first framing pulls toward abstract shapes; this brief needs a recurring human character in a storybook world."},
                {"option_id": "character-animation", "label": "character-animation (rigged puppet)", "score": 0.55,
                 "reason": "Would give a genuinely rigged, walking character, which a child would love.",
                 "rejected_because": "Marked beta in the manifest and adds character_design plus rig_plan stages. Too much surface area for the first run on a freshly configured machine."}
            ],
            "selected": "animated-explainer",
            "reason": "Production-stable pipeline whose stage shape matches the deliverable, with human gates at proposal, script, scene_plan and assets.",
            "user_visible": True,
            "user_approved": False,
            "confidence": 0.85
        },
        {
            "decision_id": "d2-concept",
            "stage": "proposal",
            "category": "concept_selection",
            "subject": "Concept direction",
            "options_considered": [
                {"option_id": "c1", "label": "Diana and the Two Speeds", "score": 0.92,
                 "reason": "Uses the book's own opening demonstration, which the child can perform herself; reaches the emotional goal through the affect heuristic and loss aversion, both genuinely in the book."},
                {"option_id": "c2", "label": "The Story Machine (WYSIATI)", "score": 0.75,
                 "reason": "Largest underserved gap; strongest social payoff.",
                 "rejected_because": "Assumes the two-speeds vocabulary she does not have yet. Better as the follow-up piece."},
                {"option_id": "c3", "label": "Why Losing Feels Twice As Big", "score": 0.7,
                 "reason": "Most concrete and testable of the five.",
                 "rejected_because": "Single-idea and narrow; absorbed as the third act of c1 instead of being made separately."},
                {"option_id": "c4", "label": "One Whole Day Inside Diana's Head", "score": 0.65,
                 "reason": "Broadest coverage of Part I and hits the researched 5-7 minute runtime.",
                 "rejected_because": "Coverage-led rather than payoff-led; risks becoming a tour instead of landing one idea."},
                {"option_id": "c5", "label": "The Guard Dog and the Wise Owl", "score": 0.6,
                 "reason": "Best pure emotion-regulation outcome and the frame teachers already use.",
                 "rejected_because": "It is Dan Siegel's neuroscience, not Kahneman's book. Saturated in the landscape scan, and presenting it as the requested book would be dishonest."}
            ],
            "selected": "c1",
            "reason": "Only option that answers the exact question asked using the book that was actually named, and it is the one an 8-year-old can test on herself within ten seconds.",
            "user_visible": True,
            "user_approved": False,
            "confidence": 0.8
        },
        {
            "decision_id": "d3-render-runtime",
            "stage": "proposal",
            "category": "render_runtime_selection",
            "subject": "Composition render runtime",
            "options_considered": [
                {"option_id": "remotion", "label": "Remotion (React scene stack)", "score": 0.85,
                 "reason": "Available on this machine. Spring-physics animation over illustrated stills, and word-level caption burn, which matters for a child who is still learning to read and can follow the words as they are spoken."},
                {"option_id": "hyperframes", "label": "HyperFrames (HTML/CSS/GSAP)", "score": 0.6,
                 "reason": "Available on this machine, version 0.8.31, doctor passing. Excellent for kinetic typography and HTML-driven motion.",
                 "rejected_because": "This piece is illustration-led rather than typography-led, and word-level caption burn is Remotion-only in the current phase."},
                {"option_id": "ffmpeg", "label": "FFmpeg (Ken Burns over stills)", "score": 0.25,
                 "reason": "Always available, zero dependencies.",
                 "rejected_because": "Pan-and-zoom over stills would make a storybook feel like a slideshow, below the presentable quality floor for this brief."}
            ],
            "selected": "remotion",
            "reason": "Recommendation only, pending user confirmation at the approval gate. Both available runtimes were presented to the user with fit and tradeoff before any lock.",
            "user_visible": True,
            "user_approved": False,
            "confidence": 0.75
        },
        {
            "decision_id": "d4-composition-mode",
            "stage": "proposal",
            "category": "composition_mode",
            "subject": "Composition authoring mode",
            "options_considered": [
                {"option_id": "atelier", "label": "Atelier (hand-authored composition)", "score": 0.88,
                 "reason": "A one-off gift for one child is hero work. The stock scene-type catalogue is corporate infographic furniture and would fight the storybook read."},
                {"option_id": "templated", "label": "Templated (stock Remotion scene types)", "score": 0.5,
                 "reason": "Faster, cheaper in iteration, more reliable.",
                 "rejected_because": "stat_card, bar_chart and kpi_grid would make a children's bedtime piece look like a quarterly report."}
            ],
            "selected": "atelier",
            "reason": "Recommendation only, pending user confirmation. Atelier costs more iteration and the user is told so explicitly before opting in.",
            "user_visible": True,
            "user_approved": False,
            "confidence": 0.75
        },
        {
            "decision_id": "d5-voice",
            "stage": "proposal",
            "category": "voice_selection",
            "subject": "Narration voice",
            "options_considered": [
                {"option_id": "daniel_records", "label": "Daniel records the narration himself", "score": 0.95,
                 "reason": "The product is a father explaining his daughter's own mind to her. His voice is materially better for that than any synthetic voice, and it costs nothing."},
                {"option_id": "elevenlabs", "label": "ElevenLabs premade voice", "score": 0.7,
                 "reason": "Warmest synthetic option available. Approx 1.02 USD. Must name a premade voice because the free plan refuses the tool default Rachel."},
                {"option_id": "openai_tts", "label": "OpenAI TTS", "score": 0.6,
                 "reason": "Approx 0.05 USD, decent quality but flatter delivery."},
                {"option_id": "google_tts", "label": "Google TTS", "score": 0.55,
                 "reason": "Approx 0.03 USD, cheapest synthetic option."},
                {"option_id": "piper", "label": "Piper local offline", "score": 0.3,
                 "reason": "Free and offline.",
                 "rejected_because": "Robotic delivery; wrong for a warm bedtime read to a child."}
            ],
            "selected": "pending_user_selection",
            "reason": "Presented to the user with Daniel recording it himself as the explicit recommendation. Not locked until he answers.",
            "user_visible": True,
            "user_approved": False,
            "confidence": 0.9
        },
        {
            "decision_id": "d6-music",
            "stage": "proposal",
            "category": "music_source",
            "subject": "Music source",
            "options_considered": [
                {"option_id": "music_gen", "label": "Generate via ElevenLabs music_gen", "score": 0.85,
                 "reason": "Approx 0.01 USD, and a generated bed can be shaped to the exact mood and length."},
                {"option_id": "google_lyria", "label": "Generate via Google Lyria", "score": 0.75,
                 "reason": "Approx 0.08 USD, strong music quality."},
                {"option_id": "pixabay_music", "label": "Free royalty-free track via pixabay_music", "score": 0.6,
                 "reason": "Free and licence-clean, but fixed length and generic mood."},
                {"option_id": "user_library", "label": "Daniel drops a track into music_library/", "score": 0.5,
                 "reason": "Full control over the track.",
                 "rejected_because": "No music_library/ folder exists on this machine yet, so this path needs a setup step first."},
                {"option_id": "none", "label": "No music", "score": 0.4,
                 "reason": "Narration-only keeps full attention on the words, which suits a bedtime read."}
            ],
            "selected": "pending_user_selection",
            "reason": "Music plan surfaced at proposal time per the mandatory music protocol. Recommendation is a generated gentle piano and strings bed, ducking under narration.",
            "user_visible": True,
            "user_approved": False,
            "confidence": 0.7
        },
        {
            "decision_id": "d7-accuracy-guardrail",
            "stage": "proposal",
            "category": "visual_accuracy_check",
            "subject": "Depiction of the two systems",
            "options_considered": [
                {"option_id": "motion_and_light", "label": "Two speeds shown as motion and light around one girl", "score": 0.9,
                 "reason": "Honours Kahneman's explicit statement that System 1 and System 2 are styles of thinking, not places in the brain."},
                {"option_id": "two_creatures", "label": "Two characters living inside a cartoon head", "score": 0.2,
                 "reason": "Instantly legible to a child and the most common approach in existing content.",
                 "rejected_because": "Factually wrong and teaches a misconception the research brief explicitly lists. Kahneman calls them different gears of one engine."}
            ],
            "selected": "motion_and_light",
            "reason": "Accuracy guardrail binding on every downstream stage, including every image prompt.",
            "user_visible": True,
            "user_approved": False,
            "confidence": 0.95
        }
    ]
}

path = write_checkpoint(
    Path("projects"),
    "diana-fast-slow-brain",
    "proposal",
    "awaiting_human",
    {"proposal_packet": packet, "decision_log": decision_log},
    human_approval_required=True,
    human_approved=False,
    review={
        "findings": [
            {"severity": "suggestion",
             "note": "The book is about judgement, not emotion regulation. The emotional goal is reached via Ch 7, 9, 13 and 26. Raised with the user explicitly at this gate rather than papered over."},
            {"severity": "suggestion",
             "note": "Character consistency across roughly 22 generated illustrations is the main quality risk. Mitigation is a locked character description reused verbatim plus a character sheet approved before batch generation."},
            {"severity": "nitpick",
             "note": "Four minute runtime sits under the 5-7 minutes the children's format research suggests; deliberate, since this is one idea rather than a series episode."}
        ],
        "rounds": 1,
        "verdict": "pass_with_warnings"
    },
    cost_snapshot={"spent_usd": 0.0, "estimated_remaining_usd": 1.91, "budget_cap_usd": 2.0},
    metadata={
        "gate": "Awaiting user approval on five open questions: concept, narration voice, render runtime, composition mode, music source.",
        "assets_generated_so_far": 0
    }
)
print("checkpoint written:", path)
print("decision log exists:", Path("projects/diana-fast-slow-brain/decision_log.json").exists())
