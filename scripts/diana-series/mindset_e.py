"""7 Habits half, films 14-17 of 25: The Map / The Space In Between / The Circle You Can Reach / The Ladder and the Wall."""
import sys
import filmgen as G
from mindset_a import base

# --- Covey overrides: base() supplies Dweck/mindsetworks, which would be a false attribution here.
CSRC = "https://www.franklincovey.com/the-7-habits/"
CSRC_T = "The 7 Habits of Highly Effective People - Stephen R. Covey"
CAUTHOR = {"author_name": "Stephen R. Covey", "author_title": "Author, The 7 Habits of Highly Effective People",
           "author_claim": "Between what happens to you and what you do about it, there is a space, and in that space you choose."}
CGUARD = ["No numeral appears in any illustration.", "Every scene with a person contains exactly one child.",
          "Nothing from the book's adult examples reaches the film: no death-camp material, no funeral visualisation, "
          "no workplace or marriage content. The principle is carried by a plain object instead.",
          "Every chapter claim in this film was read directly from the book's own text, not inferred from its "
          "reputation or structure."]


def cbase(pos, slug, comp_id, title, chapters, secondary_title):
    """base() with the Mindset source/author swapped for Covey's."""
    f = base(pos, slug, comp_id, title, chapters)
    f.update({"source_url": CSRC, "source_title": CSRC_T, "source_url_secondary": CSRC,
              "source_title_secondary": secondary_title, **CAUTHOR, "guardrails": CGUARD})
    return f


SRC = CSRC
SHOES = ("Her shoes are simple solid maroon-red slip-on canvas flats with a plain white sole and absolutely no "
         "laces, no eyelets, no stripes and no markings of any kind, like a plain child's house shoe.")

# ---------------------------------------------------------------- FILM 14
FILM14 = {**cbase(14, "diana-habits-the-map", "DianaTheMap", "The Map In Your Head", "Part One, Inside-Out",
                  "The 7 Habits, 'The Power of a Paradigm' - direct excerpt read for this film"),
    "topic": "Paradigms as the maps we navigate by, from the book's 'The Power of a Paradigm' section, told as Dad opening a second book with the idea that trying harder cannot fix a wrong map",
    "summary": ("Film 14 opens the second half of the series, from Covey's 7 Habits. His foundational image: if you "
                "are handed the wrong map of a city, working harder only gets you to the wrong place faster, and a "
                "better attitude only makes you happier while still lost. The problem is neither effort nor "
                "attitude; it is the map. We each carry many maps we never chose and never checked."),
    "existing": [{"title": "'Try harder' encouragement for children", "url": SRC, "source": "web", "angle": "Effort solves everything",
                  "what_it_covers": "Treats effort as the answer to every stuck moment, with no way to notice when the approach itself is wrong"},
                 {"title": "Positive-thinking material for kids", "url": SRC, "source": "web", "angle": "Stay positive",
                  "what_it_covers": "Improves how the situation feels without ever checking whether the underlying picture is accurate"},
                 {"title": "Optical-illusion explainers for children", "url": SRC, "source": "web", "angle": "Look, your eyes trick you",
                  "what_it_covers": "Shows that seeing can differ, but treats it as a novelty rather than as something that shapes daily decisions"}],
    "saturated": ["Try-harder encouragement with no way to question the approach itself"],
    "gaps": ["Showing a child that effort and attitude cannot correct a wrong starting picture",
             "Naming that we carry pictures we never chose and never checked"],
    "data_points": [("The book's map example is explicit: with the wrong map, working harder and being more diligent only succeeds in getting you to the wrong place faster.", SRC, "The 7 Habits, 'The Power of a Paradigm'", "primary_source", "surprising", "the whole premise of the film"),
                     ("It adds that improving your attitude does not fix it either: you would still be lost, just happier about being lost.", SRC, "The 7 Habits, 'The Power of a Paradigm'", "primary_source", "surprising", "closes the second obvious escape route"),
                     ("Its conclusion is that the fundamental problem has nothing to do with your behaviour or your attitude, and everything to do with having a wrong map.", SRC, "The 7 Habits, 'The Power of a Paradigm'", "primary_source", "expected", "the film's core sentence"),
                     ("The book states we each carry many maps in our heads, that we seldom question their accuracy, and that we are usually unaware we even have them.", SRC, "The 7 Habits, 'The Power of a Paradigm'", "primary_source", "expected", "why checking the map is a real skill, not an obvious one")],
    "questions": ["Why doesn't trying harder always work?", "How can two people see the same thing differently?", "What do I do when I'm stuck and effort isn't helping?"],
    "misconceptions": [("If something isn't working, you just aren't trying hard enough", "With the wrong map, more effort only gets you to the wrong place faster.", "Inside-Out"),
                        ("A good attitude fixes any problem", "A good attitude while lost just means you're cheerful and still lost.", "Inside-Out")],
    "pain_points": ["Trying harder and harder at something that isn't working", "Not knowing how to question her own picture of a situation"],
    "angles": [("The Wrong Map", "narrative", "Hand someone the wrong map and their effort works perfectly against them.", "One concrete image that undoes two pieces of advice she's already been given.", ["Inside-Out"]),
               ("Effort Isn't Always the Answer", "contrarian", "Sometimes the honest problem is the picture you started from, not how hard you tried.", "Directly challenges the try-harder message she hears everywhere.", ["Inside-Out"]),
               ("Maps You Never Chose", "evergreen", "You're carrying pictures nobody handed you on purpose, and you've never checked them.", "Introduces self-examination as an ordinary, unshaming habit.", ["Inside-Out"])],
    "kahneman": "With the wrong map, effort and attitude both fail: the fundamental problem is neither behaviour nor attitude, it is the map.",
    "excluded": ["The adult business and marriage examples, and the character-ethic history, which need adult framing."],
    "concepts": [
        {"id": "c1", "title": "The Map In Your Head", "hook": "Diana, I've started a second book. It opens with somebody being given the wrong map.", "narrative_structure": "story",
         "visual_approach": "A plain sheet of paper with a few simple drawn lines and a dotted route, held up beside a landform whose shape is clearly different.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 145,
         "key_points": ["A wrong map makes effort work against you", "Being cheerful about it doesn't help either", "The problem was never how hard you tried", "We all carry maps we never chose", "When stuck, check the map before checking the effort"],
         "core_message": "If the map is wrong, running faster just gets you lost faster. Check the map.", "cta": "Next time you're stuck, ask what picture you started from.", "tone": "Curious, warm, a little conspiratorial.",
         "why_this_works": "It gives her a legitimate alternative to 'try harder', which is the only tool most children are handed.", "grounded_in": ["Inside-Out"]},
        {"id": "c2", "title": "Effort Isn't Always the Answer", "hook": "Sometimes the problem isn't how hard you tried.", "narrative_structure": "myth_busting",
         "visual_approach": "A small figure walking briskly and confidently along a dotted route that leads away from where it meant to go.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 75,
         "key_points": ["Speed in the wrong direction is worse than slowness in the right one", "Effort is a good tool applied to the wrong question here"],
         "core_message": "Faster isn't better if the direction is wrong.", "cta": "Check direction before speed.", "tone": "Clear and kind.",
         "why_this_works": "Names the specific trap, folded into c1 as its hinge.", "grounded_in": ["Inside-Out"]},
        {"id": "c3", "title": "Maps You Never Chose", "hook": "You're carrying pictures nobody handed you on purpose.", "narrative_structure": "analogy",
         "visual_approach": "Several plain folded papers stacked together, ordinary and unremarkable, quietly carried.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 70,
         "key_points": ["Most of our pictures arrived without being checked", "Noticing you have one is most of the work"],
         "core_message": "You have maps you've never once looked at properly.", "cta": "Notice one picture you've never questioned.", "tone": "Gentle and curious.",
         "why_this_works": "Turns the metaphor inward without shame, folded into c1 as its closing beat.", "grounded_in": ["Inside-Out"]}],
    "rationale": "c1 carries the whole map arc from the wrong map to checking your own; c2 and c3 are its hinge and its close, all three using the same single sheet of paper.",
    "device_short": "a plain paper map whose drawn shape does not match the land beside it",
    "art_direction": "New device: a plain sheet of paper with a few simple drawn lines and a dotted route, shown beside a simple landform of a clearly different shape.",
    "device_lock": ("The map is one plain rectangular sheet of cream paper with a few simple thin drawn lines and a "
                    "dotted route on it. It has absolutely NO words, NO letters, NO place names, NO numbers, NO "
                    "compass, NO legend, NO grid and NO labels of any kind. The land is one plain simple flat "
                    "shape. Nothing else in the frame."),
    "tradeoffs": [{"tradeoff": "Using the book's ambiguous young-woman/old-woman picture versus the map", "recommendation": "The map",
                   "quality_impact": "A genuinely bistable illustration cannot be produced reliably by an image model; the map carries the same principle with a shape an eight-year-old can read instantly."}],
    "energy_curve": "Curious and conspiratorial at the new book. Building through the two failed escapes. Quietly serious at the core sentence. Warm and inviting at the close.",
    "sample_section": "s8", "human_note": "Section s8 is the core sentence. Slow, and let it be a genuine relief rather than a scolding.",
    "pause_beats": [{"section": "s5", "purpose": "She sees the drawn shape and the real shape don't match"}, {"section": "s10", "purpose": "She thinks of something she kept trying harder at"}, {"section": "s13", "purpose": "She picks a picture she's never checked"}],
    "grounded_in": {"s1_to_s4": "Inside-Out, the wrong map handed over", "s5_to_s8": "Inside-Out, effort and attitude both fail", "s9_to_s11": "Inside-Out applied to her own stuck moments", "s12_to_s15": "Inside-Out, the maps we never chose"},
    "sections": [
        ("s1", "Setup", "Diana, I've started a second book. It opens with somebody being given the wrong map.", "Diana, I've started a second book. <break time=\"0.4s\"/> It opens with somebody being given the wrong map.", 1.4, "measured", "curious", ["wrong map"], "Conspiratorial, like sharing a discovery."),
        ("s2", "The setup", "Imagine you're trying to find somewhere, and I hand you a map. Only it's a map of the wrong place entirely.", "Imagine you're trying to find somewhere, and I hand you a map. <break time=\"0.4s\"/> Only it's a map of the wrong place entirely.", 1.4, "measured", "curious", ["wrong place"], "Set the scene simply."),
        ("s3", "You don't know", "And you don't know that. It looks like a perfectly good map. Lines, little roads, all of it.", "And you don't know that. <break time=\"0.4s\"/> It looks like a perfectly good map. <break time=\"0.4s\"/> Lines, little roads, all of it.", 1.4, "measured", "steady", ["perfectly good"], "This is the important bit. Neutral."),
        ("s4", "Try harder", "So off you go. And when it isn't working, you do the sensible thing. You try harder. Walk faster.", "So off you go. <break time=\"0.4s\"/> And when it isn't working, you do the sensible thing. <break time=\"0.4s\"/> You try harder. <break time=\"0.3s\"/> Walk faster.", 1.4, "measured", "steady", ["try harder"], "Sympathetic, not mocking."),
        ("s5", "It gets worse", "And now look. All that effort just got you to the wrong place faster.", "And now look. <break time=\"0.5s\"/> All that effort just got you to the wrong place faster. <break time=\"2.5s\"/>", 2.5, "slow", "curious", ["faster"], "Pause beat one. Let the unfairness of it land."),
        ("s6", "The second try", "So you try the other thing everyone tells you. You cheer up. Better attitude. Nice and positive.", "So you try the other thing everyone tells you. <break time=\"0.4s\"/> You cheer up. <break time=\"0.3s\"/> Better attitude. <break time=\"0.3s\"/> Nice and positive.", 1.4, "measured", "wry", ["cheer up"], "A little dry."),
        ("s7", "Still lost", "And now you're happy. Genuinely happy. And still completely lost.", "And now you're happy. <break time=\"0.4s\"/> Genuinely happy. <break time=\"0.4s\"/> And still completely lost.", 1.4, "measured", "wry", ["still lost"], "Let the joke land, then go quiet."),
        ("s8", "The core", "So here's the sentence I keep thinking about. The problem was never how hard you tried, or how you felt about it. The problem was the map.", "So here's the sentence I keep thinking about. <break time=\"0.5s\"/> The problem was never how hard you tried, <break time=\"0.3s\"/> or how you felt about it. <break time=\"0.5s\"/> The problem was the map.", 1.4, "slow", "steady", ["the map"], "The heart of the film. Slow. A relief, not a telling-off."),
        ("s9", "Why it matters", "Which means sometimes, when something isn't working, the honest answer isn't do more. It's look again.", "Which means sometimes, when something isn't working, the honest answer isn't do more. <break time=\"0.4s\"/> It's look again.", 1.4, "measured", "warm", ["look again"], "Offer it as permission."),
        ("s10", "Her turn", "Think of something you kept trying harder and harder at, and it just kept not working.", "Think of something you kept trying harder and harder at, <break time=\"0.4s\"/> and it just kept not working. <break time=\"2.5s\"/>", 2.5, "slow", "gentle", ["kept not working"], "Pause beat two. She'll have one."),
        ("s11", "Maybe a map", "Maybe that wasn't an effort problem at all. Maybe you were reading a map that didn't match.", "Maybe that wasn't an effort problem at all. <break time=\"0.5s\"/> Maybe you were reading a map that didn't match.", 1.4, "measured", "tender", ["didn't match"], "Kind. This may be a genuine relief to her."),
        ("s12", "We all have them", "And here's the part that got me. We're all carrying maps like that. Lots of them. Pictures of how things are.", "And here's the part that got me. <break time=\"0.5s\"/> We're all carrying maps like that. <break time=\"0.3s\"/> Lots of them. <break time=\"0.4s\"/> Pictures of how things are.", 1.4, "measured", "curious", ["lots of them"], "Genuine wonder."),
        ("s13", "Never checked", "Nobody handed them to us on purpose. We just picked them up. And we almost never check them.", "Nobody handed them to us on purpose. <break time=\"0.4s\"/> We just picked them up. <break time=\"0.4s\"/> And we almost never check them. <break time=\"2.5s\"/>", 2.5, "slow", "steady", ["never check"], "Pause beat three. Let her consider one of hers."),
        ("s14", "The move", "So that's the move. When you're stuck, before you try harder, have a proper look at the map.", "So that's the move. <break time=\"0.5s\"/> When you're stuck, before you try harder, <break time=\"0.4s\"/> have a proper look at the map.", 1.4, "measured", "encouraging", ["look at the map"], "The tool, plainly."),
        ("s15", "Landing", "You're allowed to check, Diana. It isn't giving up. It's the opposite. Off we go into a new book, you and me.", "You're allowed to check, Diana. <break time=\"0.4s\"/> It isn't giving up. <break time=\"0.3s\"/> It's the opposite. <break time=\"0.5s\"/> Off we go into a new book, you and me.", 0.0, "slow", "tender", ["you and me"], "Warm. Opens the second half of the series."),
    ],
    "spec": [
        ("sc1", "s1", "DIANA", "The girl stands holding a closed plain book, curious and interested, ready to begin."),
        ("sc2", "s2", "NONE", "One plain rectangular sheet of cream paper with a few simple thin drawn lines and a dotted route on it, lying flat."),
        ("sc3", "s3", "NONE", "The same plain paper map shown close, its simple lines neat and convincing, nothing unusual about it."),
        ("sc4", "s4", "NONE", "A small plain figure silhouette walking briskly along a dotted route, moving with confidence."),
        ("sc5", "s5", "NONE", "The paper map beside a plain simple landform of a clearly different shape, the two shapes plainly not matching."),
        ("sc6", "s6", "DIANA", "The girl smiles determinedly, chin up, cheerfully pressing on."),
        ("sc7", "s7", "NONE", "The small plain figure silhouette standing alone at the far edge of the page, arms slightly out, plainly in the wrong place."),
        ("sc8", "s8", "NONE", "The plain paper map held up on its own, calm and central, the clear focus of the frame."),
        ("sc9", "s9", "DIANA", "The girl pauses and looks down thoughtfully, reconsidering something."),
        ("sc10", "s10", "DIANA", "The girl looks tired but honest, remembering effort that went nowhere."),
        ("sc11", "s11", "DIANA", "The girl's face eases with relief, a weight lifting, gentle and quiet."),
        ("sc12", "s12", "NONE", "Several plain folded paper sheets stacked loosely together, ordinary and unremarkable."),
        ("sc13", "s13", "DIANA", "The girl looks curious and reflective, considering something about herself."),
        ("sc14", "s14", "DIANA", "The girl holds a plain sheet of paper up and studies it carefully, deliberate and calm."),
        ("sc15", "s15", "DIANA", "The girl stands calm and warm in soft evening light."),
        ("sc16", "s5", "NONE", "A close view of the paper map and the differently shaped land side by side, the mismatch unmistakable."),
        ("sc17", "s8", "NONE", "The plain paper map alone, warmly lit, quiet and central."),
        ("sc18", "s15", "NONE", "The plain paper map resting open in warm evening light beside a plain closed book, calm and settled."),
    ],
    "heroes": {"sc5", "sc8", "sc16", "sc18"}, "wides": {"sc7"},
}
FILM14["clauses"] = {
    "OPEN": (G.OPEN, {"sc1", "sc6", "sc9", "sc10", "sc11", "sc13", "sc14", "sc15"}),
    "NOICON": (G.NOICON, {"sc1", "sc6", "sc9", "sc10", "sc11", "sc13", "sc14", "sc15"}),
    "SHOES": (SHOES, {"sc1", "sc6", "sc9", "sc10", "sc11", "sc13", "sc14", "sc15"}),
    "MAP": (("The map is one plain rectangular sheet of cream paper with a few simple thin drawn lines and a dotted "
             "route. It has absolutely NO words, NO letters, NO place names, NO numbers, NO compass, NO legend, "
             "NO grid and NO labels of any kind. Land is one plain simple flat shape. Figures are plain solid "
             "silhouettes with no facial features. No scenery, no background."),
            {"sc2", "sc3", "sc4", "sc5", "sc7", "sc8", "sc12", "sc16", "sc17", "sc18"}),
}

# ---------------------------------------------------------------- FILM 15
FILM15 = {**cbase(15, "diana-habits-the-space", "DianaTheSpace", "The Space In Between", "Habit 1",
                  "The 7 Habits, 'Between Stimulus and Response' - direct excerpt read for this film"),
    "topic": "The gap between what happens and what you do, from Habit 1's 'Between Stimulus and Response', told as Dad showing her a space she can stand in",
    "summary": ("Film 15. Habit 1, Be Proactive. The book's central discovery is that between what happens to you "
                "and your response to it there is a space, and in that space lies your freedom to choose. Covey "
                "describes finding this idea in a library paragraph and says the key to growth and happiness is how "
                "we use that space. He also notes the freedom is exercised like a muscle: small at first, growing "
                "larger and larger with use."),
    "existing": [{"title": "'Count to ten when you're angry' advice", "url": SRC, "source": "web", "angle": "Pause before reacting",
                  "what_it_covers": "Gives the technique without explaining what the pause is actually for or why it works"},
                 {"title": "Children's emotional-regulation worksheets", "url": SRC, "source": "classroom material", "angle": "Name your feelings",
                  "what_it_covers": "Handles identifying the feeling but not the moment of choosing what to do next"},
                 {"title": "'Don't let them get to you' encouragement", "url": SRC, "source": "web", "angle": "Ignore it",
                  "what_it_covers": "Asks a child to feel nothing rather than showing her the actual point where a choice exists"}],
    "saturated": ["Count-to-ten advice with no explanation of what the pause is for"],
    "gaps": ["Showing a child the specific place where a choice actually exists, rather than telling her to pause",
             "Explaining that the space starts tiny and grows with use, so a small one isn't failure"],
    "data_points": [("The book's core principle is that between stimulus and response, a person has the freedom to choose.", SRC, "The 7 Habits, 'Between Stimulus and Response'", "primary_source", "expected", "the whole device"),
                     ("Covey describes reading a single library paragraph saying there is a gap or space between stimulus and response, and that the key to both growth and happiness is how we use that space.", SRC, "The 7 Habits, Habit 1", "primary_source", "surprising", "the idea arrived in one paragraph, which is a story a child can hold"),
                     ("The book describes exercising this freedom until it grew larger and larger, so the space behaves like something trained rather than something you have or don't.", SRC, "The 7 Habits, Habit 1", "primary_source", "surprising", "why a tiny gap at first is not failure"),
                     ("It reframes responsibility as 'response-ability', the ability to choose your response, and says behaviour is a function of decisions rather than conditions.", SRC, "The 7 Habits, 'Proactivity Defined'", "primary_source", "expected", "the wordplay the film hands her")],
    "questions": ["Why do I say things I don't mean when I'm cross?", "Is there actually a moment where I get to choose?", "What if my pause is really short?"],
    "misconceptions": [("Your reaction just happens to you and can't be helped", "There is a space between the thing and your answer, and the choice lives in there.", "Habit 1"),
                        ("If you can't pause for long you've failed", "The space starts small and grows with use; a one-breath gap is a real gap.", "Habit 1")],
    "pain_points": ["Snapping back instantly and regretting it", "Believing her reactions are simply her personality"],
    "angles": [("The Space You Can Stand In", "narrative", "There's a gap between what happens and what you do. You can stand in it.", "Turns an abstract moment into a physical place she can picture.", ["Habit 1"]),
               ("It Starts Tiny", "evergreen", "The gap is a crack at first. It widens every time you use it.", "Stops a small pause from feeling like failure.", ["Habit 1"]),
               ("Your Answer Is Yours", "contrarian", "What happened isn't yours to pick. Your answer always is.", "Separates the event from the response, which is the whole habit.", ["Habit 1"])],
    "kahneman": "Between what happens to you and what you do about it there is a space, and in that space lies your freedom to choose.",
    "excluded": ["Viktor Frankl's imprisonment and the death-camp material entirely: true, central to the book, and far too heavy for an eight-year-old. The principle is carried by the stones instead."],
    "concepts": [
        {"id": "c1", "title": "The Space In Between", "hook": "Diana, there's a space between something happening and what you do about it.", "narrative_structure": "story",
         "visual_approach": "Two plain upright stones with a gap between them, the gap starting as a thin crack and widening until a small figure can stand in it comfortably.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 150,
         "key_points": ["Something happens, then you answer, and there's a space in between", "The choice lives in that space", "At first it's barely a crack", "It gets wider every single time you use it", "You don't choose what happens, you always choose the answer"],
         "core_message": "There's a space between the thing and your answer. You get to stand in it, and it grows.", "cta": "Next time something happens, find the gap before you answer.", "tone": "Steady, practical, quietly empowering.",
         "why_this_works": "It locates the choice in a specific place she can picture, instead of asking her to be calmer.", "grounded_in": ["Habit 1"]},
        {"id": "c2", "title": "It Starts Tiny", "hook": "Yours will be a crack at first. That's fine.", "narrative_structure": "problem_solution",
         "visual_approach": "The two stones almost touching, the thinnest possible line of light between them.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 75,
         "key_points": ["A tiny gap is a real gap, not a failed one", "It widens with use like anything else you practise"],
         "core_message": "One breath is a real gap.", "cta": "Use the small one; it grows.", "tone": "Reassuring.",
         "why_this_works": "Prevents the first small attempt from reading as failure, folded into c1 as its middle beat.", "grounded_in": ["Habit 1"]},
        {"id": "c3", "title": "Your Answer Is Yours", "hook": "You don't get to pick what happens. You always pick the answer.", "narrative_structure": "comparison",
         "visual_approach": "One stone plain and unchangeable, the other clearly shaped by hand.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 70,
         "key_points": ["The event is not yours to choose", "The response is always yours"],
         "core_message": "Half of it isn't up to you. The other half always is.", "cta": "Own the half that's yours.", "tone": "Firm and warm.",
         "why_this_works": "Draws the line cleanly between what she controls and what she doesn't, folded into c1 as its close.", "grounded_in": ["Habit 1"]}],
    "rationale": "c1 carries the gap from a crack to a room she can stand in; c2 and c3 are its reassurance and its dividing line, all three using the same two stones.",
    "device_short": "two plain stones with a gap between them that widens until she can stand in it",
    "art_direction": "New device: two plain upright stones on cream paper with a gap between them, the gap widening across the film from a thin crack to a space a small figure stands in.",
    "device_lock": ("Two plain simple upright stone shapes drawn flat on cream paper, smooth and unadorned, with a "
                    "clear gap between them. No faces on the stones, no carving, no scenery, no numerals, no "
                    "writing. Figures are plain solid silhouettes with no facial features."),
    "tradeoffs": [{"tradeoff": "Including Frankl's story as the book does versus carrying the principle on the stones alone", "recommendation": "The stones alone",
                   "quality_impact": "Frankl's imprisonment is the book's own catalytic story but is entirely unsuitable for an eight-year-old; the principle survives the removal intact."}],
    "energy_curve": "Steady and practical at the opening. Curious as the gap appears. Reassuring at the tiny-crack beat. Firm at the dividing line. Warm at the close.",
    "sample_section": "s6", "human_note": "Section s6 is the discovery of the gap. Let it feel like showing her a real place.",
    "pause_beats": [{"section": "s5", "purpose": "She looks for the gap for the first time"}, {"section": "s10", "purpose": "She thinks of a time she answered too fast"}, {"section": "s13", "purpose": "She practises one breath of gap"}],
    "grounded_in": {"s1_to_s4": "Habit 1, the instant reaction", "s5_to_s8": "Habit 1, the gap located", "s9_to_s11": "Habit 1 applied to her own snapping", "s12_to_s15": "Habit 1, the gap widening with use"},
    "sections": [
        ("s1", "Setup", "Diana, there's a space between something happening and what you do about it. I want to show you where it is.", "Diana, there's a space between something happening and what you do about it. <break time=\"0.4s\"/> I want to show you where it is.", 1.4, "measured", "steady", ["where it is"], "Practical, like showing her a real place."),
        ("s2", "The instant answer", "Somebody says something unkind. And your answer is already out of your mouth. Before you even decided.", "Somebody says something unkind. <break time=\"0.4s\"/> And your answer is already out of your mouth. <break time=\"0.4s\"/> Before you even decided.", 1.4, "measured", "steady", ["already out"], "Describe it without judgement."),
        ("s3", "It feels automatic", "It feels like there was no moment. Like the thing happened and your answer just came with it.", "It feels like there was no moment. <break time=\"0.4s\"/> Like the thing happened and your answer just came with it.", 1.4, "measured", "gentle", ["no moment"], "Validate how it honestly feels."),
        ("s4", "Two stones", "But picture two stones. One is the thing that happened. The other is what you did.", "But picture two stones. <break time=\"0.4s\"/> One is the thing that happened. <break time=\"0.4s\"/> The other is what you did.", 1.4, "measured", "curious", ["two stones"], "Picture-building."),
        ("s5", "Look between", "Now look at the space between them. Go on, look properly.", "Now look at the space between them. <break time=\"0.4s\"/> Go on, look properly. <break time=\"2.5s\"/>", 2.5, "slow", "curious", ["the space"], "Pause beat one. Genuine looking time."),
        ("s6", "It's there", "There's always a gap there, Diana. Always. Even when it's so thin you can barely see it.", "There's always a gap there, Diana. <break time=\"0.4s\"/> Always. <break time=\"0.5s\"/> Even when it's so thin you can barely see it.", 1.4, "slow", "warm", ["always a gap"], "The discovery. Warm and certain."),
        ("s7", "What lives there", "And that gap is the only place in the whole business where you get to choose. That's where you live.", "And that gap is the only place in the whole business where you get to choose. <break time=\"0.5s\"/> That's where you live.", 1.4, "measured", "steady", ["get to choose"], "The core claim."),
        ("s8", "Yours is small", "Yours will be a crack at first. Barely a breath wide. That's completely fine. Mine was too.", "Yours will be a crack at first. <break time=\"0.4s\"/> Barely a breath wide. <break time=\"0.4s\"/> That's completely fine. <break time=\"0.3s\"/> Mine was too.", 1.4, "measured", "warm", ["completely fine"], "Head off the failure feeling early."),
        ("s9", "It grows", "Because here's the good bit. Every single time you use it, it gets a little wider.", "Because here's the good bit. <break time=\"0.4s\"/> Every single time you use it, <break time=\"0.4s\"/> it gets a little wider.", 1.4, "measured", "encouraging", ["a little wider"], "Genuine good news."),
        ("s10", "Her turn", "Think of a time you answered too fast and wished you hadn't. Everyone's got one.", "Think of a time you answered too fast and wished you hadn't. <break time=\"0.4s\"/> Everyone's got one. <break time=\"2.5s\"/>", 2.5, "slow", "gentle", ["too fast"], "Pause beat two. Solidarity, not correction."),
        ("s11", "Not a flaw", "That wasn't your personality, Diana. That was just a very narrow gap. And gaps can be widened.", "That wasn't your personality, Diana. <break time=\"0.5s\"/> That was just a very narrow gap. <break time=\"0.4s\"/> And gaps can be widened.", 1.4, "measured", "tender", ["not your personality"], "Important reframe. Warm."),
        ("s12", "What's not yours", "Now, you don't get to choose the first stone. What happens, happens. That one isn't yours.", "Now, you don't get to choose the first stone. <break time=\"0.4s\"/> What happens, happens. <break time=\"0.4s\"/> That one isn't yours.", 1.4, "measured", "steady", ["isn't yours"], "Honest about the limit."),
        ("s13", "What is", "But the second one always is. Always. So next time, find the gap first. Even one breath of it.", "But the second one always is. <break time=\"0.3s\"/> Always. <break time=\"0.5s\"/> So next time, find the gap first. <break time=\"0.4s\"/> Even one breath of it. <break time=\"2.5s\"/>", 2.5, "measured", "encouraging", ["find the gap"], "Pause beat three. The actual tool."),
        ("s14", "Standing in it", "And one day you'll notice the gap has got wide enough to stand in properly. To have a look around before you answer.", "And one day you'll notice the gap has got wide enough to stand in properly. <break time=\"0.4s\"/> To have a look around before you answer.", 1.4, "measured", "warm", ["stand in"], "Hopeful, forward-looking."),
        ("s15", "Landing", "What happens to you isn't up to you, Diana. What you do next always is. That bit is yours. It always was.", "What happens to you isn't up to you, Diana. <break time=\"0.4s\"/> What you do next always is. <break time=\"0.4s\"/> That bit is yours. <break time=\"0.3s\"/> It always was.", 0.0, "slow", "tender", ["always was"], "Personal, warm, unhurried close."),
    ],
    "spec": [
        ("sc1", "s1", "DIANA", "The girl stands attentive and calm, ready to be shown something."),
        ("sc2", "s2", "DIANA", "The girl's mouth is open mid-word, eyes slightly wide, caught in the middle of answering too quickly."),
        ("sc3", "s3", "NONE", "Two plain upright stone shapes pressed almost together, no visible space between them at all."),
        ("sc4", "s4", "NONE", "The same two plain upright stones standing apart, one on the left, one on the right."),
        ("sc5", "s5", "NONE", "A close view of the narrow gap between the two stones, a thin line of warm light showing through it."),
        ("sc6", "s6", "NONE", "The two stones with a clearly visible gap between them, the gap warmly lit."),
        ("sc7", "s7", "NONE", "A small plain figure silhouette standing inside the gap between the two stones."),
        ("sc8", "s8", "DIANA", "The girl looks reassured and steadier, tension easing from her shoulders."),
        ("sc9", "s9", "NONE", "The gap between the stones noticeably wider than before, warm light filling it."),
        ("sc10", "s10", "DIANA", "The girl looks down in honest thought, remembering something she regrets slightly."),
        ("sc11", "s11", "DIANA", "The girl looks up, relieved and gently surprised, a weight lifting."),
        ("sc12", "s12", "NONE", "The left stone shown alone, plain and immovable, clearly not going to change."),
        ("sc13", "s13", "NONE", "The right stone shown alone, plainly being shaped by an unseen hand, only the hand and forearm visible, no face and no body."),
        ("sc14", "s14", "NONE", "The two stones now widely apart, a generous open warmly lit space between them."),
        ("sc15", "s15", "DIANA", "The girl stands calm and warm in soft evening light."),
        ("sc16", "s5", "NONE", "A very close view of the thinnest line of warm light between the two stones."),
        ("sc17", "s14", "NONE", "A small plain figure silhouette standing comfortably in the wide warm gap, unhurried, with room to spare."),
        ("sc18", "s15", "NONE", "The two stones in warm evening light with a wide calm space between them, settled and open."),
    ],
    "heroes": {"sc7", "sc14", "sc17", "sc18"}, "wides": {"sc14", "sc17"},
}
FILM15["clauses"] = {
    "OPEN": (G.OPEN, {"sc1", "sc2", "sc8", "sc10", "sc11", "sc15"}),
    "NOICON": (G.NOICON, {"sc1", "sc2", "sc8", "sc10", "sc11", "sc15"}),
    "SHOES": (SHOES, {"sc1", "sc2", "sc8", "sc10", "sc11", "sc15"}),
    "STONES": (("The stones are two plain simple smooth upright stone shapes drawn flat on cream paper, unadorned, "
                "with no faces, no carving, no cracks and no texture detail. Figures are plain solid silhouettes "
                "with no facial features. No scenery, no background, no numerals, no writing."),
               {"sc3", "sc4", "sc5", "sc6", "sc7", "sc9", "sc12", "sc13", "sc14", "sc16", "sc17", "sc18"}),
}

# ---------------------------------------------------------------- FILM 16
FILM16 = {**cbase(16, "diana-habits-circle-you-can-reach", "DianaCircleYouCanReach", "The Circle You Can Reach", "Habit 1",
                  "The 7 Habits, 'Circle of Concern / Circle of Influence' - direct excerpt read for this film"),
    "topic": "Circle of Concern and Circle of Influence, from Habit 1, told as Dad showing her which worries are worth her energy",
    "summary": ("Film 16. Habit 1's second half. Covey separates everything we worry about (the Circle of Concern) "
                "from the smaller set of things we can actually do something about (the Circle of Influence). Where "
                "you spend your energy decides which circle grows: energy spent inside the reachable circle makes "
                "it expand, while energy spent on what you cannot touch produces blame and helplessness and makes "
                "the reachable circle shrink."),
    "existing": [{"title": "'Don't worry about it' reassurance for children", "url": SRC, "source": "web", "angle": "Stop worrying",
                  "what_it_covers": "Tells a child to stop a feeling without giving her any way to sort her worries"},
                 {"title": "Worry-jar and worry-box classroom activities", "url": SRC, "source": "classroom material", "angle": "Put your worries away",
                  "what_it_covers": "Contains the worry but never distinguishes the ones she could actually act on"},
                 {"title": "News-literacy material for young children", "url": SRC, "source": "web", "angle": "Understanding big world events",
                  "what_it_covers": "Explains large frightening things without addressing what a child can do with the feeling"}],
    "saturated": ["Don't-worry reassurance that never sorts worries into actionable and not"],
    "gaps": ["Giving a child a way to sort her worries by whether she can reach them",
             "Explaining that energy spent on what she can reach actually expands what she can reach"],
    "data_points": [("The book separates the Circle of Concern, everything we worry about, from a smaller Circle of Influence, the things we can actually do something about.", SRC, "The 7 Habits, 'Circle of Concern / Circle of Influence'", "primary_source", "expected", "the two-circles device"),
                     ("It states that proactive people work inside the Circle of Influence, and that this positive energy causes that circle to increase.", SRC, "The 7 Habits, Habit 1", "primary_source", "surprising", "the circle grows, which is the film's payoff"),
                     ("It states that focusing on the outer circle produces blaming and accusing attitudes and increased feelings of victimisation, and causes the Circle of Influence to shrink.", SRC, "The 7 Habits, Habit 1", "primary_source", "surprising", "the cost, shown as the circle shrinking"),
                     ("Its summary line is that as long as we work in the Circle of Concern, we empower the things within it to control us.", SRC, "The 7 Habits, Habit 1", "primary_source", "expected", "why this is about freedom, not just efficiency")],
    "questions": ["What do I do with a worry I can't fix?", "Why does worrying make me feel worse and worse?", "Which of my worries can I actually do something about?"],
    "misconceptions": [("Caring more about a problem helps solve it", "Energy spent where you can't reach produces blame and helplessness, not change.", "Habit 1"),
                        ("The things you can affect are fixed", "Working inside the reachable circle is what makes it grow.", "Habit 1")],
    "pain_points": ["Lying awake over something she has no control over", "Feeling helpless and blaming others when a worry is out of reach"],
    "angles": [("Two Circles", "narrative", "One circle holds everything you worry about. A smaller one holds what you can reach.", "Turns a swirl of worry into a sortable picture.", ["Habit 1"]),
               ("The Circle That Grows", "data_driven", "Energy spent inside the reachable circle makes it bigger. Energy spent outside shrinks it.", "Gives a reason to choose that isn't just 'calm down'.", ["Habit 1"]),
               ("What You Feed Controls You", "contrarian", "Whatever you pour your energy into gets to decide how you feel.", "Reframes worry as something with a cost rather than something virtuous.", ["Habit 1"])],
    "kahneman": "Energy spent inside the circle you can reach makes that circle grow; energy spent outside it produces blame and helplessness and makes it shrink.",
    "excluded": ["The adult examples of national debt, nuclear war and workplace problems, and Covey's account of his son's schooling, which need adult framing."],
    "concepts": [
        {"id": "c1", "title": "The Circle You Can Reach", "hook": "Diana, some worries you can reach and some you can't. Here's how to tell.", "narrative_structure": "story",
         "visual_approach": "A large plain outer circle holding many small shapes, with a smaller inner circle that visibly grows or shrinks depending on where a warm glow is placed.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 145,
         "key_points": ["The big circle holds everything you worry about", "The small one holds what you can actually reach", "Energy poured into the small circle makes it grow", "Energy poured outside it makes it shrink", "Sorting them is a skill, not a feeling"],
         "core_message": "Put your energy where your hands can reach, and what you can reach gets bigger.", "cta": "Sort one worry today: can I reach it, or not?", "tone": "Practical, calm, empowering.",
         "why_this_works": "It gives her something to DO with a worry, which reassurance never does.", "grounded_in": ["Habit 1"]},
        {"id": "c2", "title": "The Circle That Grows", "hook": "The reachable circle isn't a fixed size.", "narrative_structure": "data_narrative",
         "visual_approach": "The inner circle expanding outward as warm light fills it.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 75,
         "key_points": ["Working inside it makes it expand", "So today's limit isn't tomorrow's limit"],
         "core_message": "What you can reach today isn't what you'll be able to reach later.", "cta": "Work the inside and watch it widen.", "tone": "Encouraging.",
         "why_this_works": "Turns the idea from a limit into a growth story, folded into c1 as its payoff.", "grounded_in": ["Habit 1"]},
        {"id": "c3", "title": "What You Feed Controls You", "hook": "Whatever you pour your energy into gets to decide how you feel.", "narrative_structure": "problem_solution",
         "visual_approach": "The inner circle shrinking as the warm glow drifts out into the crowded outer ring.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 75,
         "key_points": ["Energy spent out of reach turns into blame and helplessness", "The cost is real, not just wasted time"],
         "core_message": "Feed the things you can't reach, and they start running you.", "cta": "Notice when your energy has drifted out of reach.", "tone": "Honest and steady.",
         "why_this_works": "Names the actual cost, folded into c1 as its warning beat.", "grounded_in": ["Habit 1"]}],
    "rationale": "c1 carries the sorting and both outcomes; c2 and c3 are its payoff and its warning, all three drawn on the same pair of circles.",
    "device_short": "two circles, the inner reachable one growing or shrinking with where the glow goes",
    "art_direction": "New device: one large plain outer circle holding small plain shapes, and a smaller inner circle that grows or shrinks as a warm glow moves between them.",
    "device_lock": ("Two plain simple concentric circle outlines drawn flat on cream paper, one large and one "
                    "smaller inside it. Worries are plain small round or pebble shapes with no faces and no detail. "
                    "Absolutely NO labels, NO words, NO letters, NO numbers, NO arrows, NO diagram annotations and "
                    "NO legend. This is a picture, never a diagram."),
    "tradeoffs": [{"tradeoff": "Labelling the two circles as the book does versus leaving them unlabelled", "recommendation": "Unlabelled",
                   "quality_impact": "The book names them for adult readers, but no illustration in this series may contain lettering; the narration names them and the picture carries only shape and size."}],
    "energy_curve": "Calm and practical at the sorting. Bright at the circle growing. Honest at the shrinking. Encouraging and settled at the close.",
    "sample_section": "s8", "human_note": "Section s8 is the growth reveal. Genuine good news, not a lecture.",
    "pause_beats": [{"section": "s5", "purpose": "She sorts her own worries into the two circles"}, {"section": "s10", "purpose": "She notices a worry that's been running her"}, {"section": "s13", "purpose": "She picks one reachable thing"}],
    "grounded_in": {"s1_to_s4": "Habit 1, the two circles introduced", "s5_to_s8": "Habit 1, the inner circle grows", "s9_to_s11": "Habit 1, the cost of the outer circle", "s12_to_s15": "Habit 1 corrective, sorting one worry"},
    "sections": [
        ("s1", "Setup", "Diana, some worries you can reach and some you can't. Here's how to tell them apart.", "Diana, some worries you can reach and some you can't. <break time=\"0.4s\"/> Here's how to tell them apart.", 1.4, "measured", "steady", ["reach"], "Practical and calm."),
        ("s2", "The big circle", "Picture a big circle. Everything you've ever worried about goes in it. All of it.", "Picture a big circle. <break time=\"0.4s\"/> Everything you've ever worried about goes in it. <break time=\"0.4s\"/> All of it.", 1.4, "measured", "curious", ["big circle"], "Picture-building."),
        ("s3", "It's crowded", "It's a crowded circle, isn't it. Some big things in there. Some you couldn't change if you tried for a hundred years.", "It's a crowded circle, isn't it. <break time=\"0.4s\"/> Some big things in there. <break time=\"0.4s\"/> Some you couldn't change if you tried for a hundred years.", 1.4, "measured", "gentle", ["crowded"], "Sympathetic."),
        ("s4", "The small circle", "Now draw a smaller circle inside it. And into this one goes only the things your own hands can actually reach.", "Now draw a smaller circle inside it. <break time=\"0.5s\"/> And into this one goes only the things your own hands can actually reach.", 1.4, "measured", "curious", ["can actually reach"], "The key distinction."),
        ("s5", "Sort them", "Have a go. Which of your worries goes in the small one?", "Have a go. <break time=\"0.4s\"/> Which of your worries goes in the small one? <break time=\"2.5s\"/>", 2.5, "slow", "curious", ["small one"], "Pause beat one. Real sorting time."),
        ("s6", "Fewer than you thought", "Probably fewer than you expected. That's normal. It's a small circle for everybody.", "Probably fewer than you expected. <break time=\"0.4s\"/> That's normal. <break time=\"0.4s\"/> It's a small circle for everybody.", 1.4, "measured", "warm", ["for everybody"], "Reassure, don't diminish."),
        ("s7", "Where the energy goes", "Now here's the whole thing. Wherever you pour your energy is what decides what happens next.", "Now here's the whole thing. <break time=\"0.5s\"/> Wherever you pour your energy is what decides what happens next.", 1.4, "measured", "steady", ["pour your energy"], "Build to the reveal."),
        ("s8", "The growth", "Pour it into the small circle, into things you can actually reach, and the small circle grows. It gets bigger. You can reach more than you could before.", "Pour it into the small circle, into things you can actually reach, <break time=\"0.4s\"/> and the small circle grows. <break time=\"0.4s\"/> It gets bigger. <break time=\"0.4s\"/> You can reach more than you could before.", 1.4, "slow", "encouraging", ["the small circle grows"], "Genuine good news. Bright."),
        ("s9", "The other way", "But pour it out into the big ring, into things you can't touch, and something sad happens.", "But pour it out into the big ring, into things you can't touch, <break time=\"0.4s\"/> and something sad happens.", 1.4, "measured", "gentle", ["can't touch"], "Set up the cost honestly."),
        ("s10", "It shrinks", "The small circle shrinks. And you end up cross, and blaming people, and feeling like nothing's up to you.", "The small circle shrinks. <break time=\"0.5s\"/> And you end up cross, and blaming people, <break time=\"0.4s\"/> and feeling like nothing's up to you. <break time=\"2.5s\"/>", 2.5, "slow", "gentle", ["shrinks"], "Pause beat two. She may recognise this feeling."),
        ("s11", "Not lazy", "That isn't you being lazy or ungrateful. It's just what happens when your energy goes somewhere it can't do anything.", "That isn't you being lazy or ungrateful. <break time=\"0.5s\"/> It's just what happens when your energy goes somewhere it can't do anything.", 1.4, "measured", "tender", ["isn't you"], "Remove the shame."),
        ("s12", "Not ignoring", "This doesn't mean you stop caring about the big things. You're allowed to care. Caring is good.", "This doesn't mean you stop caring about the big things. <break time=\"0.4s\"/> You're allowed to care. <break time=\"0.3s\"/> Caring is good.", 1.4, "measured", "warm", ["allowed to care"], "Important guard. Warm."),
        ("s13", "The move", "It just means your hands go to work in the small circle. So pick one thing you can reach today. Just one.", "It just means your hands go to work in the small circle. <break time=\"0.5s\"/> So pick one thing you can reach today. <break time=\"0.4s\"/> Just one. <break time=\"2.5s\"/>", 2.5, "measured", "encouraging", ["one thing"], "Pause beat three. The actual tool."),
        ("s14", "Watch it widen", "Do that enough times and you'll look down one day and find the small circle isn't small any more.", "Do that enough times and you'll look down one day and find the small circle isn't small any more.", 1.4, "measured", "warm", ["isn't small any more"], "Hopeful."),
        ("s15", "Landing", "You can't reach everything, Diana. Nobody can. But what you can reach gets bigger every time you use it.", "You can't reach everything, Diana. <break time=\"0.4s\"/> Nobody can. <break time=\"0.5s\"/> But what you can reach gets bigger every time you use it.", 0.0, "slow", "tender", ["gets bigger"], "Personal, warm, unhurried close."),
    ],
    "spec": [
        ("sc1", "s1", "DIANA", "The girl stands calm and attentive, ready to sort something out."),
        ("sc2", "s2", "NONE", "One large plain circle outline on cream paper, holding many small plain pebble shapes scattered inside it."),
        ("sc3", "s3", "NONE", "The same large circle, its small shapes crowded closely together, a few noticeably larger than the rest."),
        ("sc4", "s4", "NONE", "The large circle with a smaller plain circle outline drawn inside it, a few small shapes sitting within the inner one."),
        ("sc5", "s5", "DIANA", "The girl looks thoughtfully downward, sorting something in her mind."),
        ("sc6", "s6", "NONE", "The inner circle shown clearly, holding only a small handful of plain shapes."),
        ("sc7", "s7", "NONE", "A soft warm glow hovering between the inner circle and the outer ring, not yet settled in either."),
        ("sc8", "s8", "NONE", "The inner circle filled with warm glow and clearly expanded, noticeably larger than before."),
        ("sc9", "s9", "NONE", "The warm glow drifting outward into the crowded outer ring, away from the inner circle."),
        ("sc10", "s10", "NONE", "The inner circle visibly shrunken and dim, the outer ring crowded and bright around it."),
        ("sc11", "s11", "DIANA", "The girl looks weary and a little cross, honestly frustrated rather than upset."),
        ("sc12", "s12", "DIANA", "The girl looks openly caring and gentle, warm-hearted."),
        ("sc13", "s13", "DIANA", "The girl reaches out steadily with one hand toward something within reach, purposeful."),
        ("sc14", "s14", "NONE", "The inner circle much larger than at the start, warmly glowing, nearly filling the outer circle."),
        ("sc15", "s15", "DIANA", "The girl stands calm and warm in soft evening light."),
        ("sc16", "s8", "NONE", "A close view of the inner circle glowing warmly as it expands outward."),
        ("sc17", "s10", "NONE", "A close view of the small dim shrunken inner circle, quiet and pale."),
        ("sc18", "s15", "NONE", "The two circles in warm evening light, the inner one large, warm and settled."),
    ],
    "heroes": {"sc8", "sc14", "sc16", "sc18"}, "wides": set(),
}
FILM16["clauses"] = {
    "OPEN": (G.OPEN, {"sc1", "sc5", "sc11", "sc12", "sc13", "sc15"}),
    "NOICON": (G.NOICON, {"sc1", "sc5", "sc11", "sc12", "sc13", "sc15"}),
    "SHOES": (SHOES, {"sc1", "sc5", "sc11", "sc12", "sc13", "sc15"}),
    "CIRCLES": (("Two plain simple circle outlines drawn flat on cream paper, one large and one smaller inside it. "
                 "Worries are plain small round pebble shapes with no faces and no detail. Absolutely NO labels, "
                 "NO words, NO letters, NO numbers, NO arrows, NO annotations and NO legend anywhere. This is a "
                 "plain picture, never a diagram or an infographic. No scenery, no background."),
                {"sc2", "sc3", "sc4", "sc6", "sc7", "sc8", "sc9", "sc10", "sc14", "sc16", "sc17", "sc18"}),
}

# ---------------------------------------------------------------- FILM 17
FILM17 = {**cbase(17, "diana-habits-ladder-and-wall", "DianaLadderAndWall", "The Ladder and the Wall", "Habit 2",
                  "The 7 Habits, Habit 2 'Begin with the End in Mind' - direct excerpt read for this film"),
    "topic": "Beginning with the end in mind, from Habit 2, told as Dad explaining that speed is worthless if the ladder is against the wrong wall",
    "summary": ("Film 17. Habit 2, Begin with the End in Mind. Covey's image is a person climbing the ladder of "
                "success only to discover it has been leaning against the wrong wall the whole time, and his line "
                "is that if the ladder is not against the right wall, every step just gets you to the wrong place "
                "faster. It is possible, he says, to be very busy without being very effective. A deliberate echo "
                "of the map film: direction before speed."),
    "existing": [{"title": "Goal-setting worksheets for children", "url": SRC, "source": "classroom material", "angle": "Write down your goals",
                  "what_it_covers": "Captures targets without ever asking whether the target is the right one"},
                 {"title": "'Work hard and you'll get there' encouragement", "url": SRC, "source": "web", "angle": "Effort wins",
                  "what_it_covers": "Rewards climbing speed and never mentions which wall the ladder is on"},
                 {"title": "Productivity and star-chart systems for kids", "url": SRC, "source": "classroom material", "angle": "Get more done",
                  "what_it_covers": "Optimises busyness, which is precisely the trap the book names"}],
    "saturated": ["Work-hard encouragement that rewards climbing speed without asking about direction"],
    "gaps": ["Asking a child what she wants to be true at the end, before she starts",
             "Naming that being very busy and being effective are different things"],
    "data_points": [("The book's image is climbing the ladder of success only to discover it is leaning against the wrong wall.", SRC, "The 7 Habits, Habit 2", "primary_source", "surprising", "the whole device"),
                     ("Its line is that if the ladder is not leaning against the right wall, every step we take just gets us to the wrong place faster.", SRC, "The 7 Habits, Habit 2", "primary_source", "surprising", "the film's core sentence, and a deliberate echo of the map film"),
                     ("It states plainly that it is possible to be busy, very busy, without being very effective.", SRC, "The 7 Habits, Habit 2", "primary_source", "expected", "separates busyness from progress"),
                     ("Beginning with the end in mind means starting with a clear understanding of your destination, so that the steps you take are always in the right direction.", SRC, "The 7 Habits, Habit 2", "primary_source", "expected", "the corrective the film hands her")],
    "questions": ["Why do I sometimes finish something and feel flat?", "How do I know if I'm working on the right thing?", "What should I ask before I start?"],
    "misconceptions": [("Being busy means you're getting somewhere", "You can be very busy without being effective at all.", "Habit 2"),
                        ("You should just start and figure out the point later", "Starting without a destination means every step could be in the wrong direction.", "Habit 2")],
    "pain_points": ["Working hard on something and feeling empty when it's done", "Starting without knowing what she actually wants from it"],
    "angles": [("The Wrong Wall", "narrative", "You can climb beautifully, all the way to the top of the wrong wall.", "One image that reframes effort as secondary to direction.", ["Habit 2"]),
               ("Busy Isn't The Same As Getting Somewhere", "contrarian", "Very busy and very effective are two different things.", "Challenges the busyness she'll be rewarded for at school.", ["Habit 2"]),
               ("Ask Before You Climb", "evergreen", "Before you start, ask what you want to be true when it's finished.", "A single question she can use on anything, for life.", ["Habit 2"])],
    "kahneman": "If the ladder is not leaning against the right wall, every step you take just gets you to the wrong place faster.",
    "excluded": ["The book's funeral visualisation exercise, in which the reader imagines their own funeral: central to Habit 2 for adults and entirely unsuitable for an eight-year-old. Replaced with asking what she wants to be true at the end of the thing she's doing."],
    "concepts": [
        {"id": "c1", "title": "The Ladder and the Wall", "hook": "Diana, you can climb a ladder beautifully and still end up somewhere you never wanted to be.", "narrative_structure": "story",
         "visual_approach": "A plain ladder leaning against a plain wall, climbed to the top, then the same ladder moved to lean against a different wall.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 145,
         "key_points": ["You can climb well and still reach the wrong place", "Speed makes a wrong direction worse, not better", "Busy and effective are not the same thing", "Moving the ladder feels like losing time and isn't", "Ask what you want to be true at the end, before you start"],
         "core_message": "Check the wall before you climb. A fast climb up the wrong wall is just a faster way to the wrong place.", "cta": "Before you start something, ask what you want to be true when it's done.", "tone": "Warm, practical, unhurried.",
         "why_this_works": "It hands her a single question that works on homework, friendships and everything after.", "grounded_in": ["Habit 2"]},
        {"id": "c2", "title": "Busy Isn't Getting Somewhere", "hook": "Very busy and very effective are two different things.", "narrative_structure": "myth_busting",
         "visual_approach": "A small figure climbing rapidly, rungs blurring, the wall behind entirely unremarkable.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 70,
         "key_points": ["Busyness can look exactly like progress from the outside", "Only the direction decides whether it was progress"],
         "core_message": "You can be busy all day and have gone nowhere you wanted.", "cta": "Stop scoring yourself on how busy you were.", "tone": "Clear.",
         "why_this_works": "Challenges the reward she gets for looking busy, folded into c1 as its hinge.", "grounded_in": ["Habit 2"]},
        {"id": "c3", "title": "Ask Before You Climb", "hook": "One question, before you start anything.", "narrative_structure": "tutorial",
         "visual_approach": "A ladder lying flat on the ground beside two different walls, not yet placed against either.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 70,
         "key_points": ["Deciding the wall takes a moment and saves the whole climb", "The question works on anything, at any size"],
         "core_message": "What do I want to be true when this is finished?", "cta": "Ask it before your next big thing.", "tone": "Practical and warm.",
         "why_this_works": "Reduces the habit to one usable sentence, folded into c1 as its closing tool.", "grounded_in": ["Habit 2"]}],
    "rationale": "c1 carries the climb, the discovery and the move; c2 and c3 are its hinge and its tool, all three using the same single ladder.",
    "device_short": "a plain ladder leaning against a wall, then moved to a different one",
    "art_direction": "New device: one plain simple wooden ladder and plain flat wall shapes on cream paper, the ladder shown climbed, then lifted and re-leaned against a different wall.",
    "device_lock": ("One plain simple wooden ladder with plain straight rungs, and plain flat rectangular wall "
                    "shapes, drawn flat on cream paper. No brick detail, no windows, no doors, no scenery, no "
                    "numerals, no writing. Figures are plain solid silhouettes with no facial features."),
    "tradeoffs": [{"tradeoff": "Using the book's funeral visualisation versus asking what she wants true at the end of a task", "recommendation": "The end of a task",
                   "quality_impact": "The funeral exercise is Habit 2's centrepiece for adults and would frighten an eight-year-old; the same question at task scale gives her the habit without the weight."}],
    "energy_curve": "Warm and steady at the climb. A quiet drop at the discovery. Honest through the busy beat. Practical and encouraging at the question. Warm at the close.",
    "sample_section": "s7", "human_note": "Section s7 is the core sentence, echoing film 14 deliberately. Slow.",
    "pause_beats": [{"section": "s5", "purpose": "She sits with reaching the top of the wrong wall"}, {"section": "s10", "purpose": "She thinks of something that felt flat when finished"}, {"section": "s13", "purpose": "She tries the question on something real"}],
    "grounded_in": {"s1_to_s4": "Habit 2, the climb", "s5_to_s8": "Habit 2, the wrong wall discovered", "s9_to_s11": "Habit 2, busy versus effective", "s12_to_s15": "Habit 2 corrective, the question before starting"},
    "sections": [
        ("s1", "Setup", "Diana, you can climb a ladder beautifully and still end up somewhere you never wanted to be.", "Diana, you can climb a ladder beautifully and still end up somewhere you never wanted to be.", 1.4, "measured", "warm", ["beautifully"], "Warm, intriguing."),
        ("s2", "The climb", "Picture somebody climbing. Really going for it. Strong, steady, rung after rung.", "Picture somebody climbing. <break time=\"0.4s\"/> Really going for it. <break time=\"0.4s\"/> Strong, steady, rung after rung.", 1.4, "measured", "steady", ["rung after rung"], "Genuine admiration for the effort."),
        ("s3", "Doing it right", "And they're doing everything right. Not stopping. Not complaining. Everyone would be proud of them.", "And they're doing everything right. <break time=\"0.4s\"/> Not stopping. <break time=\"0.3s\"/> Not complaining. <break time=\"0.4s\"/> Everyone would be proud of them.", 1.4, "measured", "warm", ["everything right"], "No irony yet."),
        ("s4", "The top", "And then they get to the top. And they look around.", "And then they get to the top. <break time=\"0.5s\"/> And they look around.", 1.4, "measured", "curious", ["the top"], "Let it hang."),
        ("s5", "Wrong wall", "And the ladder was against the wrong wall the whole time.", "And the ladder was against the wrong wall the whole time. <break time=\"2.5s\"/>", 2.5, "slow", "gentle", ["wrong wall"], "Pause beat one. Quiet. Let it be a real loss."),
        ("s6", "Not their fault", "Nobody told them to check. They were just told to climb. So they climbed.", "Nobody told them to check. <break time=\"0.4s\"/> They were just told to climb. <break time=\"0.4s\"/> So they climbed.", 1.4, "measured", "gentle", ["told to climb"], "Compassionate, not mocking."),
        ("s7", "The core", "And here's the hard bit, Diana. All that climbing? It didn't help. If the ladder's on the wrong wall, every step just gets you to the wrong place faster.", "And here's the hard bit, Diana. <break time=\"0.5s\"/> All that climbing? <break time=\"0.4s\"/> It didn't help. <break time=\"0.5s\"/> If the ladder's on the wrong wall, every step just gets you to the wrong place faster.", 1.4, "slow", "steady", ["wrong place faster"], "The core sentence. Deliberate echo of the map film. Slow."),
        ("s8", "You've heard that", "You've heard me say that before, haven't you. About the map. Same idea, different book, same trap.", "You've heard me say that before, haven't you. <break time=\"0.4s\"/> About the map. <break time=\"0.4s\"/> Same idea, different book, <break time=\"0.3s\"/> same trap.", 1.4, "measured", "warm", ["same trap"], "Callback to film 14. Pleased she'd notice."),
        ("s9", "Busy", "And it's sneaky, because busy looks exactly like getting somewhere. From the outside they look identical.", "And it's sneaky, because busy looks exactly like getting somewhere. <break time=\"0.4s\"/> From the outside they look identical.", 1.4, "measured", "curious", ["look identical"], "Name the trap."),
        ("s10", "Her turn", "Think of a time you worked really hard on something and felt oddly flat when it was done.", "Think of a time you worked really hard on something and felt oddly flat when it was done. <break time=\"2.5s\"/>", 2.5, "slow", "gentle", ["oddly flat"], "Pause beat two. She'll recognise the feeling."),
        ("s11", "That's the tell", "That flat feeling is the tell. That's usually the wrong wall, not a lack of effort.", "That flat feeling is the tell. <break time=\"0.4s\"/> That's usually the wrong wall, <break time=\"0.4s\"/> not a lack of effort.", 1.4, "measured", "tender", ["the tell"], "Useful and kind."),
        ("s12", "Moving it", "Now, moving a ladder feels like wasting time. It always does. It never is.", "Now, moving a ladder feels like wasting time. <break time=\"0.4s\"/> It always does. <break time=\"0.4s\"/> It never is.", 1.4, "measured", "steady", ["never is"], "Firm."),
        ("s13", "The question", "So here's the question. Before you start something, ask what you want to be true when it's finished. That's it. That's the whole habit.", "So here's the question. <break time=\"0.5s\"/> Before you start something, ask what you want to be true when it's finished. <break time=\"0.4s\"/> That's it. <break time=\"0.3s\"/> That's the whole habit. <break time=\"2.5s\"/>", 2.5, "measured", "encouraging", ["want to be true"], "Pause beat three. The actual tool. Let her try it."),
        ("s14", "It's small", "It takes about ten seconds. And it decides everything the next few hours are worth.", "It takes about ten seconds. <break time=\"0.4s\"/> And it decides everything the next few hours are worth.", 1.4, "measured", "warm", ["ten seconds"], "Emphasise how cheap it is."),
        ("s15", "Landing", "You're a wonderful climber, Diana. I just want you standing at the top of a wall you actually chose.", "You're a wonderful climber, Diana. <break time=\"0.5s\"/> I just want you standing at the top of a wall you actually chose.", 0.0, "slow", "tender", ["actually chose"], "Personal, warm, unhurried close."),
    ],
    "spec": [
        ("sc1", "s1", "DIANA", "The girl stands attentive and warm, listening with interest."),
        ("sc2", "s2", "NONE", "A plain simple wooden ladder leaning against a plain flat wall, with a small plain figure silhouette partway up it."),
        ("sc3", "s3", "NONE", "The small figure silhouette climbing steadily, higher up the same ladder, posture strong and determined."),
        ("sc4", "s4", "NONE", "The small figure silhouette standing at the very top of the ladder, looking outward."),
        ("sc5", "s5", "NONE", "A wide view showing the ladder against one plain wall, with a clearly different plain wall standing some distance away."),
        ("sc6", "s6", "DIANA", "The girl looks sympathetic and a little sad on someone else's behalf."),
        ("sc7", "s7", "NONE", "The ladder against the plain wall with faint upward motion lines along it, showing speed that leads nowhere useful."),
        ("sc8", "s8", "DIANA", "The girl looks up with recognition, connecting this to something she already knows."),
        ("sc9", "s9", "NONE", "Two plain walls side by side, one with a ladder against it, both looking equally ordinary."),
        ("sc10", "s10", "DIANA", "The girl looks quietly flat and tired, honestly deflated rather than upset."),
        ("sc11", "s11", "DIANA", "The girl looks up, understanding something, expression clearing."),
        ("sc12", "s12", "NONE", "The plain ladder lifted away from the wall and held upright in mid-air, being carried."),
        ("sc13", "s13", "NONE", "The plain ladder lying flat on the ground between two plain walls, not yet leaning against either."),
        ("sc14", "s14", "DIANA", "The girl looks thoughtful and decisive, choosing deliberately."),
        ("sc15", "s15", "DIANA", "The girl stands calm and warm in soft evening light."),
        ("sc16", "s5", "NONE", "A close view of the top of the ladder against the plain wall, the different wall visible in the distance beyond it."),
        ("sc17", "s13", "NONE", "The plain ladder newly leaning against the second wall, freshly and deliberately placed."),
        ("sc18", "s15", "NONE", "The plain ladder leaning securely against a plain wall in warm evening light, settled and deliberately chosen."),
    ],
    "heroes": {"sc5", "sc16", "sc17", "sc18"}, "wides": {"sc5", "sc9"},
}
FILM17["clauses"] = {
    "OPEN": (G.OPEN, {"sc1", "sc6", "sc8", "sc10", "sc11", "sc14", "sc15"}),
    "NOICON": (G.NOICON, {"sc1", "sc6", "sc8", "sc10", "sc11", "sc14", "sc15"}),
    "SHOES": (SHOES, {"sc1", "sc6", "sc8", "sc10", "sc11", "sc14", "sc15"}),
    "LADDER": (("One plain simple wooden ladder with plain straight rungs, and plain flat rectangular wall shapes, "
                "drawn flat on cream paper. No brick detail, no windows, no doors, no roofs, no scenery, no "
                "background, no numerals, no writing. Figures are plain solid silhouettes with no facial features."),
               {"sc2", "sc3", "sc4", "sc5", "sc7", "sc9", "sc12", "sc13", "sc16", "sc17", "sc18"}),
}

if __name__ == "__main__":
    G_FILMS = {"m14": FILM14, "m15": FILM15, "m16": FILM16, "m17": FILM17}
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
