"""Film 16: You Already Spent It (sunk cost and mental accounting, Ch 32)."""
import sys
import filmgen as G

DL = "https://thedecisionlab.com/biases"

FILM = {
    "slug": "diana-sunk-cost", "comp_id": "DianaSunkCost",
    "title": "You Already Spent It", "position": "16 of 18", "chapters": "Ch 32",
    "source_url": DL, "source_title": "Cognitive Biases - The Decision Lab",
    "topic": "The sunk-cost fallacy and mental accounting, told for an 8-year-old as why finishing something horrible feels compulsory",
    "summary": ("Film 16 of the series. Chapter 32. People keep investing in a failing course of action to avoid "
                "closing a mental account at a loss, which is the sunk-cost fallacy. The money, time or effort "
                "already spent is gone whatever happens next, so it cannot rationally bear on the choice, yet it "
                "dominates. The corrective Kahneman gives is to ask whether you would start this today, at this "
                "price, with no history. For a child this covers the film she is not enjoying, the club she "
                "dreads, and the model she has stopped wanting to build."),
    "existing": [
        {"title": "Jane the Brain (NIMH)", "url": G.NIMH, "source": "government site",
         "angle": "Coping with big feelings", "what_it_covers": "Feelings, not the accounting behind a reluctance to stop"},
        {"title": "Children's perseverance material", "url": G.SCH, "source": "web",
         "angle": "Never give up, finish what you start",
         "what_it_covers": "Treats stopping as a character failure and never distinguishes quitting from correcting"},
        {"title": "Cognitive Biases - The Decision Lab", "url": DL, "source": "reference site",
         "angle": "Adult reference explainer", "what_it_covers": "Sunk cost through business, investment and project framings"}],
    "saturated": ["Never-give-up and finish-what-you-start messaging",
                  "Adult business, investment and failing-project framings"],
    "gaps": ["Separating stopping something that is not working from giving up on yourself",
             "Explaining that what has been spent is gone whichever choice she makes",
             "A test she can run out loud: would I start this now"],
    "data_points": [
        ("People continue investing in failing ventures to avoid closing a mental account at a loss.",
         DL, "Thinking, Fast and Slow, Ch 32", "secondary_source", "counterintuitive",
         "the whole spine and the spent-coins device"),
        ("Costs already incurred are unrecoverable and therefore irrelevant to the decision about what to do next.",
         G.SN, "Thinking, Fast and Slow, Ch 32", "secondary_source", "expected",
         "the gone-either-way beat"),
        ("The corrective is to ask whether you would begin this today, at this cost, with no prior history.",
         G.SN, "Thinking, Fast and Slow, Ch 32", "secondary_source", "expected", "the would-I-start-now tool"),
        ("By age 8 to 9 children can apply an explicit counterfactual question to their own choices.",
         G.PQ, "Pennequin et al., British Journal of Educational Psychology (2020)", "primary_source",
         "expected", "age appropriateness of the fresh-start question")],
    "knowledge_level": ("Age 8. Has seen films 1 to 15 and owns the fast one, the story machine, the anchor, the "
                        "see-saw, the tiny spoon, the ordinary street, the shrinking circle, the worn path, the fog "
                        "and the two door handles."),
    "questions": ["Why do I have to finish something I am not enjoying?",
                  "Why does stopping feel like wasting it?",
                  "Is stopping the same as giving up?"],
    "misconceptions": [
        ("If I stop now, everything I spent is wasted", "It is spent either way. Stopping does not waste it; it was already gone.", "Ch 32"),
        ("Finishing gets the value back", "Finishing spends more on top of what is already gone.", "Ch 32"),
        ("Stopping means I am a quitter", "Stopping something that is not working is a correction, not a character flaw.", "Ch 32 corrective")],
    "pain_points": ["Sitting through things she is not enjoying out of a sense of obligation",
                    "Feeling ashamed of wanting to stop"],
    "angles": [
        ("The Coins Are Already Gone", "narrative",
         "Whatever you choose next, the coins in the slot are not coming back.",
         "A jar of coins already dropped through a slot is concrete and settles the whole argument in one image.",
         ["Ch 32"]),
        ("Would You Start Now", "evergreen", "If this were being offered to you fresh today, would you say yes?",
         "The chapter's own corrective, and one a child can ask out loud.", ["Ch 32 corrective"]),
        ("Stopping Is Not Quitting", "contrarian", "Changing your mind when the facts changed is not giving up.",
         "Directly contradicts the finish-what-you-start message she receives constantly.", ["Ch 32"])],
    "kahneman": "People throw good money after bad to avoid closing a mental account at a loss.",
    "excluded": ["Business and investment examples, which need adult context.",
                 "Any suggestion that she should abandon commitments to other people.",
                 "Anything from the priming or ego-depletion chapters."],
    "concepts": [
        {"id": "c1", "title": "You Already Spent It",
         "hook": "You are not enjoying it. But you have to finish, because you already started. Have you though?",
         "narrative_structure": "story",
         "visual_approach": "A row of coins dropping one by one through a slot into a sealed box that cannot be opened, whatever happens next.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 150,
         "key_points": ["What you spent is gone whichever way you choose",
                        "Finishing does not get it back, it spends more",
                        "The pull you feel is about closing the account, not about the thing",
                        "Stopping something that is not working is a correction",
                        "Ask whether you would start it today"],
         "core_message": "The coins are already in the box. The only real question is what happens to the next hour.",
         "cta": "When you feel you must finish something, ask whether you would start it today.",
         "tone": "Freeing, and careful about the difference between things and people.",
         "why_this_works": "It gives her permission that is grounded in arithmetic rather than indulgence, and it draws a line she can hold at commitments to other people.",
         "grounded_in": ["Ch 32"]},
        {"id": "c2", "title": "Would You Start Now", "hook": "Would you say yes to this today?",
         "narrative_structure": "tutorial", "visual_approach": "An open hand being offered a small wrapped parcel.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 95,
         "key_points": ["Imagine no history", "Answer honestly", "Then decide"],
         "core_message": "Would you start now?", "cta": "Ask it.", "tone": "Practical",
         "why_this_works": "The actionable core with nothing behind it, so it becomes the payoff of c1.",
         "grounded_in": ["Ch 32 corrective"]},
        {"id": "c3", "title": "Stopping Is Not Quitting", "hook": "Changing course is not the same as giving up.",
         "narrative_structure": "comparison", "visual_approach": "Two paths from one point, one continuing and one turning, both drawn equally.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 100,
         "key_points": ["Correcting is not failing", "Promises are different", "Know which one it is"],
         "core_message": "Stopping is a decision.", "cta": "Name which kind it is.", "tone": "Fair",
         "why_this_works": "Necessary for safety, but it is the qualifier rather than the idea, so it becomes the late middle of c1.",
         "grounded_in": ["Ch 32"]}],
    "rationale": ("c1 settles the arithmetic with the coin box before offering any permission, so the permission is "
                  "earned rather than indulgent. The others are its ending and its qualifier."),
    "device_short": "the coins already dropped through the slot of a sealed box",
    "art_direction": ("Series house style. New device: a plain sealed wooden box with a coin slot, and coins that "
                      "have already dropped through it and cannot be got back."),
    "device_lock": ("One plain sealed wooden box with a narrow slot in the top, drawn flat on cream paper. Simple "
                    "round coins are effort already spent. Once through the slot they are never shown again. "
                    "Nothing is counted and no numeral appears."),
    "anti_patterns": ["asking the image model for an exact count of coins",
                      "two children in one frame", "numerals, coin values, labels or lettering",
                      "implying she may break promises to people",
                      "a fully painted background"],
    "tradeoffs": [
        {"tradeoff": "Coins with values on them versus plain blank discs",
         "recommendation": "Plain blank discs",
         "quality_impact": "No numeral may appear in an illustration, and a value would invite counting. Blank discs carry spent-effort without arithmetic."},
        {"tradeoff": "Giving blanket permission to stop versus carving out promises",
         "recommendation": "Carve out promises",
         "quality_impact": "A film that told an 8-year-old to abandon anything she stopped enjoying would be irresponsible. The distinction between a thing and a promise to a person is stated explicitly."}],
    "delivery_style": "warm parent reading a bedtime story, freeing but careful",
    "performance_intent": ("The same parent and child, fifteen chapters on. This one hands back a choice she thinks "
                           "she does not have, while keeping the one obligation that genuinely holds."),
    "energy_curve": ("Sympathetic at the opening. Curious through the coins. Firm at it is gone either way. Careful "
                     "at the promise qualifier. Bright and freeing at the tool."),
    "pause_policy": "Three genuine silences: after have you though, after they are not coming back, and after only still doing because you started it.",
    "sample_section": "s11",
    "human_note": "Section s11 is the promise qualifier. It must not sound like a catch or a take-back.",
    "reading_age": "Written for a listener of 8. Sunk cost and mental accounting never appear as terms.",
    "pause_beats": [{"section": "s2", "purpose": "She questions the obligation for the first time"},
                    {"section": "s7", "purpose": "She absorbs that it is gone whichever way she chooses"},
                    {"section": "s14", "purpose": "She asks the question about something real"}],
    "grounded_in": {"s1_to_s3": "Ch 32, the felt obligation to finish what has been paid for",
                    "s4_to_s7": "Ch 32, unrecoverable costs are irrelevant to the next decision",
                    "s8_to_s10": "Ch 32, the pull is about closing the account rather than the activity",
                    "s11_to_s12": "the promise qualifier, added for safety rather than from the chapter",
                    "s13_to_s15": "Ch 32 corrective, the would-you-start-today question, plus Pennequin"},
    "guardrails": ["The film explicitly excludes promises to people from the permission it gives.",
                   "It never says effort does not matter, only that spent effort cannot be recovered by spending more.",
                   "No numeral or coin value appears in any illustration.",
                   "No priming or ego-depletion material."],
    "sections": [
        ("s1", "Not enjoying it", "You are halfway through something. And you are not enjoying it. Not even slightly.",
         'You are halfway through something. <break time="0.4s"/> And you are not enjoying it. <break time="0.4s"/> Not even slightly.',
         1.4, "measured", "gentle", ["not"], "Sympathetic."),
        ("s2", "But you started", "But you have to finish. Because you already started. Have you though?",
         'But you have to finish. <break time="0.4s"/> Because you already started. <break time="0.5s"/> Have you though? <break time="2.5s"/>',
         2.5, "measured", "curious", ["have you"], "Pause beat one. A real question."),
        ("s3", "The box", "Picture a plain wooden box with a slot in the top. And every bit of time you have spent on this thing is a coin.",
         'Picture a plain wooden box with a slot in the top. <break time="0.5s"/> And every bit of time you have spent on this thing is a coin.',
         1.4, "measured", "warm", ["coin"], "Picture-building."),
        ("s4", "Dropping in", "You have been dropping them in, one by one, all afternoon.",
         'You have been dropping them in, <break time="0.3s"/> one by one, <break time="0.3s"/> all afternoon.',
         1.4, "measured", "steady", ["one by one"], "Steady rhythm."),
        ("s5", "Sealed", "And the box does not open. There is no lid. Whatever you do next, those coins are staying in there.",
         'And the box does not open. <break time="0.4s"/> There is no lid. <break time="0.5s"/> Whatever you do next, those coins are staying in there.',
         1.4, "slow", "steady", ["whatever"], "Firm. The hinge."),
        ("s6", "Both ways", "If you keep going. They are gone. If you stop right now. They are gone.",
         'If you keep going. <break time="0.4s"/> They are gone. <break time="0.5s"/> If you stop right now. <break time="0.4s"/> They are gone.',
         1.4, "slow", "steady", ["gone"], "Even weight on both."),
        ("s7", "Exactly the same", "Exactly the same either way. They are not coming back.",
         'Exactly the same either way. <break time="0.5s"/> They are not coming back. <break time="2.5s"/>',
         2.5, "slow", "steady", ["not coming back"], "Pause beat two. Let the arithmetic land."),
        ("s8", "So what is left", "So the only thing you are actually choosing is what happens to the next hour. That is it. That is the whole choice.",
         'So the only thing you are actually choosing is what happens to the next hour. <break time="0.4s"/> That is it. <break time="0.4s"/> That is the whole choice.',
         1.4, "measured", "curious", ["next hour"], "Clarifying and freeing."),
        ("s9", "What the pull is", "That heavy feeling that says you must finish? It is not about the thing. It is about not wanting to put a cross in the box.",
         'That heavy feeling that says you must finish? <break time="0.5s"/> It is not about the thing. <break time="0.5s"/> It is about not wanting to put a cross in the box.',
         1.4, "measured", "steady", ["cross"], "Name the real driver."),
        ("s10", "Finishing costs more", "And finishing does not get the coins back. It just puts more coins in.",
         'And finishing does not get the coins back. <break time="0.5s"/> It just puts more coins in.',
         1.4, "measured", "steady", ["more"], "Plain."),
        ("s11", "But promises", "Now. This is different if you promised somebody. A promise to a person is not a coin in a box. That one you keep.",
         'Now. <break time="0.4s"/> This is different if you promised somebody. <break time="0.5s"/> A promise to a person is not a coin in a box. <break time="0.4s"/> That one you keep.',
         1.4, "measured", "steady", ["promise"], "Warm and clear, never a catch."),
        ("s12", "Not quitting", "But stopping a thing that is not working is not giving up. It is changing your mind, because you know more now than you did at the start.",
         'But stopping a thing that is not working is not giving up. <break time="0.5s"/> It is changing your mind, <break time="0.4s"/> because you know more now than you did at the start.',
         1.4, "measured", "encouraging", ["changing"], "Give her the words."),
        ("s13", "The tool", "So here is your sixteenth trick. When you feel you have to finish something, ask this. If nobody had started it, and somebody offered it to me right now, would I say yes?",
         'So here is your sixteenth trick. <break time="0.5s"/> When you feel you have to finish something, ask this. <break time="0.5s"/> If nobody had started it, and somebody offered it to me right now, <break time="0.4s"/> would I say yes?',
         1.4, "measured", "encouraging", ["right now"], "Bright."),
        ("s14", "Try it", "Have a go. Think of something you are only still doing because you started it.",
         'Have a go. <break time="0.4s"/> Think of something you are only still doing because you started it. <break time="2.5s"/>',
         2.5, "measured", "encouraging", ["only"], "Pause beat three. She will have one."),
        ("s15", "Landing", "The coins are already in the box. The only thing left to decide is what happens next.",
         'The coins are already in the box. <break time="0.5s"/> The only thing left to decide is what happens next.',
         0.0, "slow", "tender", ["next"], "Settled and freeing. End soft."),
    ],
    "spec": [
        ("sc1", "s1", "DIANA", "The girl sits slumped with her chin propped on one hand, bored and flat, looking down at nothing in particular."),
        ("sc2", "s2", "DIANA", "The girl lifts her head and looks straight ahead, a question forming on her face."),
        ("sc3", "s3", "NONE", "One plain sealed wooden box with a narrow slot cut in its top, drawn simply in the middle of the page, with no lid and no opening."),
        ("sc4", "s4", "NONE", "One plain round blank coin held between finger and thumb just above the slot of the wooden box. Only the hand and forearm are visible, with no face and no body."),
        ("sc5", "s4", "NONE", "Several plain round blank coins falling in a line down towards the slot of the plain wooden box."),
        ("sc6", "s5", "NONE", "The plain wooden box seen close, completely sealed, with no lid, no hinges and no way to open it."),
        ("sc7", "s6", "NONE", "The plain sealed box in the middle of the page with one simple path leading away to the left and another leading away to the right, both looking exactly the same."),
        ("sc8", "s7", "NONE", "The plain sealed wooden box standing alone in the middle of a large empty page, quiet and final."),
        ("sc9", "s8", "NONE", "One simple hourglass shape drawn on the page with its upper chamber still full of sand and its lower chamber empty, and no markings or numbers on it."),
        ("sc10", "s9", "DIANA", "The girl holds one hand against her chest with a slightly heavy, reluctant expression, as if something is weighing on her."),
        ("sc11", "s10", "NONE", "A hand dropping one more plain blank coin into the slot of the sealed box. Only the hand and forearm are visible, with no face and no body."),
        ("sc12", "s11", "NONE", "Two open hands reaching towards each other and almost touching in the middle of the page, warm and steady. Only the hands and forearms are visible, with no faces and no bodies."),
        ("sc13", "s12", "DIANA", "The girl stands and turns to face a new direction, calm and decided, one foot already stepping that way."),
        ("sc14", "s13", "NONE", "One open upturned palm with a small plain wrapped parcel resting on it, being offered forward. Only the hand and forearm are visible, with no face and no body."),
        ("sc15", "s13", "DIANA", "The girl looks at something being offered to her, weighing it up thoughtfully with her head tilted."),
        ("sc16", "s14", "DIANA", "The girl sits cross-legged thinking carefully, one finger tapping her chin, calm and unhurried."),
        ("sc17", "s15", "NONE", "The plain sealed wooden box sitting quietly off to one side of the page, with a clear open path leading away from it into empty space."),
        ("sc18", "s15", "DIANA", "The girl walks away lightly along an open path in warm golden light, unburdened and easy."),
    ],
    "heroes": {"sc6", "sc8", "sc11", "sc17", "sc18"},
    "wides": {"sc7", "sc8", "sc17"},
}

BOX = ("The box is one plain simple wooden box with a narrow rectangular slot cut in the top, drawn flat and "
       "simply on plain empty cream paper. It has no lid, no hinges, no lock and no opening. Any coins are plain "
       "round blank discs with completely smooth faces: no faces, no heads, no symbols, no writing and no numbers "
       "on them.")

FILM["clauses"] = {
    "OPEN": (G.OPEN, {"sc1", "sc2", "sc9", "sc10", "sc12", "sc13", "sc14", "sc15", "sc16", "sc18"}),
    "NOICON": (G.NOICON, {"sc1", "sc2", "sc9", "sc10", "sc13", "sc15", "sc16", "sc18"}),
    "BOX": (BOX, {"sc3", "sc4", "sc5", "sc6", "sc7", "sc8", "sc11", "sc17"}),
}

if __name__ == "__main__":
    if "init" in sys.argv:
        G.init(FILM)
    if "build" in sys.argv:
        G.build(FILM)
    if "sheet" in sys.argv:
        G.sheet(FILM)
