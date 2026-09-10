"""Mindset series, films 1-5 of 25: The Two Mindsets / Yet / Mistakes / Effort / No Natural."""
import sys
import filmgen as G

SRC = "https://www.mindsetworks.com/science/"
SRC_T = "Mindset - Dr Carol S. Dweck (Robinson, revised edition 2017)"
SRC2 = "https://www.mindsetworks.com/science/"
SRC2_T = "Mindset, Ch 1 'The Mindsets' - direct excerpt read for this film"
AUTHOR = {"author_name": "Dr Carol S. Dweck", "author_title": "Psychologist, Stanford University",
          "author_claim": "Believing your qualities can be developed changes what failure and effort mean to you."}

ANTI = ["asking the image model for an exact count of anything", "two children in one frame",
        "numerals, labels or lettering of any kind", "a fully painted background; most of the page stays plain cream paper",
        "icon clip-art: lightbulbs, cogs, sparkles, question marks, floating symbols",
        "implying she is behind, not clever enough, or being compared to another real child"]
GUARD = ["No numeral appears in any illustration.", "Every scene with a person contains exactly one child.",
         "The film never says a fixed mindset is a character flaw; it says it is a belief, and beliefs can change.",
         "Claims beyond Chapter 1 are marked secondary_source: grounded in the book's own contents page and Dweck's "
         "consistent public description of this work, not claimed as a verbatim quote."]

DAD_STYLE = "warm, direct, first person, a father speaking straight to his daughter, not a narrator describing her"
DAD_INTENT = ("Part of a second series, made after the thinking-fast-and-slow films. This one is a letter as much "
              "as a lesson: Dad speaking to Diana directly about who she is becoming, not just how her mind works.")


def base(pos, slug, comp_id, title, chapters):
    return {
        "slug": slug, "comp_id": comp_id, "title": title, "position": f"{pos} of 25", "chapters": chapters,
        "source_url": SRC, "source_title": SRC_T, "source_url_secondary": SRC2, "source_title_secondary": SRC2_T,
        **AUTHOR,
        "knowledge_level": ("Age 8. Has watched the earlier eighteen-film series on how her brain works and is used "
                            "to short calm storybook films. This series is about who she is becoming, not how her "
                            "brain processes things."),
        "delivery_style": DAD_STYLE, "performance_intent": DAD_INTENT,
        "reading_age": "Written for a listener of 8. Fixed mindset, growth mindset and psychological terms never appear; the ideas are given in plain words.",
        "anti_patterns": ANTI, "guardrails": GUARD,
        "pause_policy": "Three genuine silences per film, placed where she needs to actually think or answer.",
        "heroes": set(), "wides": set(),
    }


FILM1 = {**base(1, "diana-mindset-two-mindsets", "DianaTwoMindsets", "The Two Mindsets", "Ch 1"),
    "topic": "The fixed mindset and the growth mindset, told as a message from Dad about two different beliefs a person can hold about themselves",
    "summary": ("Film 1 of a new series. Chapter 1. Dweck's central finding: believing your qualities are fixed "
                "creates urgency to prove yourself over and over, while believing they can be developed creates a "
                "passion for learning instead. Both feel equally real from the inside. The belief itself is the "
                "thing that changes everything downstream of it, including how a setback feels."),
    "existing": [
        {"title": "Growth mindset classroom posters", "url": SRC, "source": "school material",
         "angle": "Have a growth mindset!", "what_it_covers": "Names the idea as a slogan without showing what a fixed mindset actually feels like from inside"},
        {"title": "Generic confidence-building books for children", "url": SRC, "source": "web",
         "angle": "Believe in yourself", "what_it_covers": "Encouragement without explaining that there are two different beliefs underneath it"},
        {"title": "Mindset - mindsetworks.com", "url": SRC, "source": "author's own organisation",
         "angle": "Adult and school-leadership framing", "what_it_covers": "The two mindsets, aimed at educators and adults, not spoken directly to a child"}],
    "saturated": ["Growth-mindset posters and slogans with no underlying mechanism"],
    "gaps": ["Telling a child what a fixed mindset actually feels like from the inside, not just naming the alternative",
             "A father speaking about his own belief rather than instructing hers",
             "Showing that both mindsets feel completely real and certain, which is why the difference matters"],
    "data_points": [
        ("Believing your qualities are fixed creates urgency to prove yourself over and over in every situation.",
         SRC, "Mindset, Ch 1", "primary_source", "expected", "the locked-door device"),
        ("Believing your qualities can be developed through effort and strategy creates a passion for learning instead of proving.",
         SRC, "Mindset, Ch 1", "primary_source", "expected", "the door still being built"),
        ("People with the growth mindset are not claiming everyone can become an Einstein; they believe true potential is unknown and unknowable in advance.",
         SRC, "Mindset, Ch 1", "primary_source", "surprising", "removes the false idea that growth mindset means limitless talent"),
        ("Darwin and Tolstoy were considered ordinary children; many later-exceptional people were not flagged as gifted early.",
         SRC, "Mindset, Ch 1", "primary_source", "surprising", "grounds the idea in real, checkable examples rather than only theory")],
    "questions": ["Why do some people give up the moment something is hard?", "What does believing in yourself actually mean?", "Can a belief really change how a day feels?"],
    "misconceptions": [
        ("A fixed mindset means someone doesn't try", "People with a fixed mindset often try very hard, at proving rather than at learning.", "Ch 1"),
        ("Growth mindset means everyone can become anything", "It means potential is unknown in advance, not that talent doesn't exist.", "Ch 1"),
        ("This is about intelligence only", "The book applies the same idea to personality and character too.", "Ch 1")],
    "pain_points": ["Freezing up rather than trying when something feels hard", "Treating one bad result as proof of who she is"],
    "angles": [
        ("The Locked Door and the Door Still Being Built", "narrative", "One door is finished and must never crack. One door is still being built, on purpose.",
         "A door under construction is something she can picture immediately and it does not need the word mindset at all.", ["Ch 1"]),
        ("Both Feel Completely Real", "contrarian", "Neither belief feels like a belief. Both feel like the plain truth.",
         "The book's own insight that this is invisible from the inside is the part no poster captures.", ["Ch 1"]),
        ("Dad's Own Two Doors", "evergreen", "Even grown-ups carry both doors, for different parts of their life.",
         "Makes it personal rather than a lesson delivered from above.", ["Ch 1"])],
    "kahneman": "Believing your qualities are fixed or can be developed changes what failure and effort mean to you.",
    "excluded": ["The workplace and Enron material from Chapter 5, which needs adult business context.",
                 "Detailed sports biographies from Chapter 4, saved for a later film."],
    "concepts": [
        {"id": "c1", "title": "The Two Mindsets", "hook": "Diana, I want to tell you about two doors that live inside every single person, including me.",
         "narrative_structure": "story", "visual_approach": "A locked stone door that must never show a crack, beside a door still openly under construction, both on cream paper.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old, spoken to directly by her father", "target_platform": "generic", "target_duration_seconds": 150,
         "key_points": ["One belief says your qualities are fixed and must be defended", "One belief says qualities can be built", "Both feel completely true from the inside", "Neither is about how much talent you started with", "You get to notice which door you're standing at"],
         "core_message": "The finished door has to be defended. The door still being built is allowed to have scaffolding on it.",
         "cta": "When something goes wrong, notice which door you just stepped through.", "tone": "Warm, personal, a father speaking plainly.",
         "why_this_works": "It opens the whole new series on the belief underneath everything else in it, spoken as Dad rather than taught as a lesson.", "grounded_in": ["Ch 1"]},
        {"id": "c2", "title": "Prove It or Build It", "hook": "Every day you either try to prove something or try to build something.",
         "narrative_structure": "comparison", "visual_approach": "A trophy held under glass beside an open toolbox.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 100,
         "key_points": ["Proving is about looking good now", "Building is about being different later", "Both take real effort"],
         "core_message": "Proving protects. Building grows.", "cta": "Ask which one today was about.", "tone": "Curious",
         "why_this_works": "A sharp restatement, but it needs the two-doors picture first, so it becomes the middle of c1.", "grounded_in": ["Ch 1"]},
        {"id": "c3", "title": "Nobody Starts Knowing", "hook": "Darwin was an ordinary child.",
         "narrative_structure": "myth_busting", "visual_approach": "A small acorn beside a tall oak, same object, different moment.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 90,
         "key_points": ["Being ordinary at the start proves nothing about later", "Potential is unknown in advance"],
         "core_message": "You cannot see the oak in the acorn.", "cta": "Stop guessing your own ceiling.", "tone": "Encouraging",
         "why_this_works": "True and grounding, but it is evidence for c1's claim rather than a film of its own, so it becomes a scene inside c1.", "grounded_in": ["Ch 1"]}],
    "rationale": "c1 opens the whole new series on the belief underneath every other film in it, told as Dad speaking directly rather than a lesson about her. c2 and c3 are folded in as its middle and its evidence.",
    "device_short": "the locked stone door beside the door still being built",
    "art_direction": "Series house style continued. New device for this series: a stone door that must stay unmarked, beside an identical door frame still openly under construction with visible scaffolding.",
    "device_lock": "One stone doorway sealed and polished, no cracks allowed to show. One identical doorway with wooden scaffolding across it, clearly still being built. Same size, same shape, drawn side by side or singly per scene. No numerals.",
    "tradeoffs": [{"tradeoff": "Naming the two mindsets with Dweck's own terms versus describing them only in image",
                   "recommendation": "Describe only in image, name nothing", "quality_impact": "An 8-year-old does not need the vocabulary; the two doors carry the entire idea without jargon."}],
    "energy_curve": "Warm and direct from the first line. Curious through the two doors. Grounding at the Darwin evidence. Settled and personal at the close.",
    "sample_section": "s1", "human_note": "Section s1 sets the whole series' register: this is Dad talking, not a show.",
    "pause_beats": [{"section": "s3", "purpose": "She notices a time she defended rather than tried"}, {"section": "s9", "purpose": "She pictures her own version of the two doors"}, {"section": "s14", "purpose": "She decides which door she wants to stand at tomorrow"}],
    "grounded_in": {"s1_to_s4": "Ch 1, the two mindsets introduced directly", "s5_to_s8": "Ch 1, both feel equally real from the inside", "s9_to_s11": "Ch 1, Darwin and Tolstoy as ordinary children", "s12_to_s15": "Ch 1 corrective: potential is unknown in advance"},
    "sections": [
        ("s1", "Direct address", "Diana, I want to tell you about two doors that live inside every single person. Including me.",
         'Diana, I want to tell you about two doors that live inside every single person. <break time="0.5s"/> Including me.', 1.4, "measured", "warm", ["two doors"], "This line sets the whole series. Slow and personal."),
        ("s2", "The locked door", "One door is made of stone. It's finished. And it can never, ever show a crack.",
         "One door is made of stone. <break time=\"0.4s\"/> It's finished. <break time=\"0.5s\"/> And it can never, ever show a crack.", 1.4, "measured", "steady", ["never"], "A little ominous, on purpose."),
        ("s3", "The built door", "The other door is exactly the same shape. But it still has scaffolding all over it. It's allowed to still be being built.",
         "The other door is exactly the same shape. <break time=\"0.4s\"/> But it still has scaffolding all over it. <break time=\"0.5s\"/> It's allowed to still be being built. <break time=\"2.5s\"/>", 2.5, "slow", "warm", ["allowed"], "Pause beat one. Let the relief of that word land."),
        ("s4", "Which one you defend", "If you believe you're the stone door, every hard thing is a threat. One crack and the whole thing might be seen.",
         "If you believe you're the stone door, <break time=\"0.4s\"/> every hard thing is a threat. <break time=\"0.5s\"/> One crack and the whole thing might be seen.", 1.4, "measured", "steady", ["threat"], "Name the fear plainly."),
        ("s5", "Which one you build", "If you believe you're the door still being built, a hard thing isn't a threat. It's just the next bit of scaffolding.",
         "If you believe you're the door still being built, <break time=\"0.4s\"/> a hard thing isn't a threat. <break time=\"0.5s\"/> It's just the next bit of scaffolding.", 1.4, "measured", "warm", ["next bit"], "Give the relief a shape."),
        ("s6", "Both feel true", "And here's the strange part. Both of those feel completely true while you're standing at them. Neither one feels like a belief you chose.",
         "And here's the strange part. <break time=\"0.5s\"/> Both of those feel completely true while you're standing at them. <break time=\"0.4s\"/> Neither one feels like a belief you chose.", 1.4, "slow", "curious", ["chose"], "The hinge."),
        ("s7", "Not about talent", "And it isn't about how good you already are at something. It's about whether you think good is a fixed number, or a place you're travelling to.",
         "And it isn't about how good you already are at something. <break time=\"0.5s\"/> It's about whether you think good is a fixed number, <break time=\"0.4s\"/> or a place you're travelling to.", 1.4, "measured", "steady", ["travelling"], "Clarify the misconception directly."),
        ("s8", "Even me", "I carry both doors too, Diana. For some things I'm still the stone door, if I'm honest.",
         "I carry both doors too, Diana. <break time=\"0.4s\"/> For some things I'm still the stone door, <break time=\"0.4s\"/> if I'm honest.", 1.4, "measured", "gentle", ["honest"], "Genuine vulnerability, not performed."),
        ("s9", "Her own doors", "So have a think. Is there something in your life right now where you're guarding a stone door?",
         "So have a think. <break time=\"0.5s\"/> Is there something in your life right now where you're guarding a stone door? <break time=\"2.5s\"/>", 2.5, "slow", "gentle", ["guarding"], "Pause beat two. Real reflection time."),
        ("s10", "Nobody starts finished", "Here's something that might surprise you. Darwin was thought to be a completely ordinary child.",
         "Here's something that might surprise you. <break time=\"0.5s\"/> Darwin was thought to be a completely ordinary child.", 1.4, "measured", "curious", ["ordinary"], "Genuine surprise in the delivery."),
        ("s11", "Not a small acorn", "You can't look at a small acorn and see the oak tree that's coming. Nobody can. Not even you, about you.",
         "You can't look at a small acorn and see the oak tree that's coming. <break time=\"0.4s\"/> Nobody can. <break time=\"0.4s\"/> Not even you, about you.", 1.4, "slow", "tender", ["not even you"], "Land this one softly. It's the point."),
        ("s12", "Not everyone Einstein", "This doesn't mean anyone can become anyone. It means nobody, including you, actually knows your ceiling yet.",
         "This doesn't mean anyone can become anyone. <break time=\"0.5s\"/> It means nobody, including you, actually knows your ceiling yet.", 1.4, "measured", "steady", ["ceiling"], "Guard against overclaiming."),
        ("s13", "The choice", "So here's your first trick in this new set. When something goes wrong, notice which door you just stepped through.",
         "So here's your first trick in this new set. <break time=\"0.5s\"/> When something goes wrong, notice which door you just stepped through.", 1.4, "measured", "encouraging", ["notice"], "Bright and useful."),
        ("s14", "Try it", "Think about tomorrow. Which door do you want to walk through first?",
         "Think about tomorrow. <break time=\"0.5s\"/> Which door do you want to walk through first? <break time=\"2.5s\"/>", 2.5, "measured", "encouraging", ["tomorrow"], "Pause beat three. A real choice, not rhetorical."),
        ("s15", "Landing", "You don't have to be finished, Diana. You're allowed to still have scaffolding on. I love watching you build.",
         "You don't have to be finished, Diana. <break time=\"0.5s\"/> You're allowed to still have scaffolding on. <break time=\"0.5s\"/> I love watching you build.", 0.0, "slow", "tender", ["love watching"], "The first closing line of the new series. Warm and unhurried."),
    ],
    "spec": [
        ("sc1", "s1", "DIANA", "The girl sits close, listening intently, head tilted, warm attentive expression."),
        ("sc2", "s2", "NONE", "One tall stone doorway, polished and sealed, standing alone on the page, flawless and closed."),
        ("sc3", "s3", "NONE", "An identical stone doorway beside it, but this one has simple wooden scaffolding crossing its front, clearly still under construction."),
        ("sc4", "s4", "NONE", "The stone doorway with a single fine crack beginning to show near its base, subtle and small."),
        ("sc5", "s5", "NONE", "The scaffolded doorway with one more plank of wood being calmly added to it."),
        ("sc6", "s6", "NONE", "The two doorways side by side, drawn identically in shape and size, one sealed, one scaffolded."),
        ("sc7", "s7", "NONE", "A simple road forking into two paths: one ending at a flag planted in the ground, one continuing on into the distance."),
        ("sc8", "s8", "DIANA", "The girl looks thoughtful, hand near her chin, gentle and reflective, not performing."),
        ("sc9", "s9", "DIANA", "The girl sits quietly with her hands in her lap, eyes distant, genuinely thinking."),
        ("sc10", "s10", "NONE", "A small plain acorn resting alone on the cream page."),
        ("sc11", "s11", "NONE", "The same small acorn beside a tall, fully grown oak tree silhouette, both on the same page."),
        ("sc12", "s12", "NONE", "A single tall stem growing upward off the top edge of the page, its top not visible, suggesting no ceiling."),
        ("sc13", "s13", "DIANA", "The girl stands with one hand raised slightly, alert, catching a thought."),
        ("sc14", "s14", "DIANA", "The girl looks ahead down a path with calm curiosity, considering which way to go."),
        ("sc15", "s15", "NONE", "The scaffolded doorway standing warmly lit at dusk, plainly still being built and entirely at peace with that."),
        ("sc16", "s7", "NONE", "The scaffolded doorway alone, warm light glowing through the gaps in its wooden supports."),
        ("sc17", "s4", "NONE", "A close view of the fine crack in the stone doorway, small but unmistakably there."),
        ("sc18", "s15", "DIANA", "The girl walking away calmly along an open path in soft evening light, unhurried and content."),
    ],
    "heroes": {"sc3", "sc11", "sc15", "sc18"}, "wides": {"sc6", "sc7", "sc18"},
}
FILM1["clauses"] = {
    "OPEN": (G.OPEN, {"sc1", "sc4", "sc7", "sc8", "sc9", "sc10", "sc11", "sc12", "sc13", "sc14", "sc16", "sc17", "sc18"}),
    "NOICON": (G.NOICON, {"sc1", "sc4", "sc7", "sc8", "sc9", "sc10", "sc11", "sc12", "sc13", "sc14", "sc18"}),
    "DOOR": (("The doorways are plain stone doorway shapes drawn flat and simply on cream paper, no walls, no room, "
              "no background scenery. Scaffolding is simple wooden planks and poles, nothing decorative."),
             {"sc2", "sc3", "sc4", "sc5", "sc6", "sc15", "sc16", "sc17"}),
}

if __name__ == "__main__":
    G_FILMS = {"m01": FILM1}
    args = sys.argv[1:]
    slugs = [a for a in args if a in G_FILMS] or list(G_FILMS)
    for key in slugs:
        f = G_FILMS[key]
        if "init" in args:
            G.init(f)
        if "build" in args:
            G.build(f)
        if "sheet" in args:
            G.sheet(f)
