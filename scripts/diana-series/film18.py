"""Film 18: Nothing Is As Big As It Seems (the focusing illusion, Ch 38). Series capstone."""
import sys
import filmgen as G

DL = "https://thedecisionlab.com/biases"

FILM = {
    "slug": "diana-focusing", "comp_id": "DianaFocusing",
    "title": "Nothing Is As Big As It Seems", "position": "18 of 18", "chapters": "Ch 38",
    "source_url": DL, "source_title": "Cognitive Biases - The Decision Lab",
    "topic": "The focusing illusion, told for an 8-year-old as why whatever she is thinking about swells to fill the whole picture",
    "summary": ("Film 18 of the series, and its ending. Chapter 38. Kahneman's formulation is that nothing in life "
                "is as important as you think it is while you are thinking about it. Attention inflates whatever "
                "it lands on, which is why anticipated changes feel life-altering and rarely are, and why a "
                "present worry crowds out everything else that is also true. For a child this is the mechanism "
                "behind the ruined evening, the dreaded event, and the discovery that the size of a thing and the "
                "size of her attention are two different measurements."),
    "existing": [
        {"title": "Jane the Brain (NIMH)", "url": G.NIMH, "source": "government site",
         "angle": "Coping with big feelings", "what_it_covers": "Techniques for calming down, not why the thing looks enormous"},
        {"title": "Children's mindfulness material", "url": G.SCH, "source": "web",
         "angle": "Notice your thoughts and let them pass",
         "what_it_covers": "Teaches noticing without explaining that attention itself is doing the magnifying"},
        {"title": "Cognitive Biases - The Decision Lab", "url": DL, "source": "reference site",
         "angle": "Adult reference explainer", "what_it_covers": "The focusing illusion through income, climate and life-satisfaction research"}],
    "saturated": ["Mindfulness and notice-your-thoughts exercises",
                  "Adult happiness, income and life-satisfaction framings"],
    "gaps": ["Naming attention as the magnifier, rather than the thing itself being big",
             "A physical demonstration a child can perform with her own thumb",
             "An ending that ties the whole series together without moralising"],
    "data_points": [
        ("Nothing in life is as important as you think it is while you are thinking about it.",
         DL, "Thinking, Fast and Slow, Ch 38", "secondary_source", "counterintuitive",
         "the whole spine, and the closing line of the series"),
        ("Attention inflates the perceived importance of whatever it is directed at.",
         G.SN, "Thinking, Fast and Slow, Ch 38", "secondary_source", "surprising",
         "the thumb-over-the-moon demonstration"),
        ("Anticipated life changes are predicted to matter far more than they turn out to.",
         G.SN, "Thinking, Fast and Slow, Ch 38", "secondary_source", "expected",
         "the dreaded event that turns out to be an ordinary afternoon"),
        ("By age 8 to 9 children can carry out a simple physical self-test and draw a conclusion from it.",
         G.PQ, "Pennequin et al., British Journal of Educational Psychology (2020)", "primary_source",
         "expected", "the thumb experiment as something she actually does")],
    "knowledge_level": ("Age 8. Has seen films 1 to 17 and owns every device in the series: the fast one, the story "
                        "machine, the anchor, the see-saw, the tiny spoon, the ordinary street, the shrinking "
                        "circle, the worn path, the fog, the two door handles, the sealed box and the two windows."),
    "questions": ["Why does one thing take up my whole head?",
                  "Why was the thing I dreaded so ordinary when it came?",
                  "How do I make something feel smaller without pretending it does not matter?"],
    "misconceptions": [
        ("If it fills my head it must be enormous", "Size in your head measures attention, not importance.", "Ch 38"),
        ("Thinking harder about it will shrink it", "Thinking about it is what is making it big.", "Ch 38"),
        ("Making it smaller means it does not matter", "It can matter and still not be the whole picture.", "Ch 38")],
    "pain_points": ["One worry swallowing a whole evening",
                    "Dreading something that turns out to be unremarkable"],
    "angles": [
        ("Your Thumb And The Moon", "narrative",
         "Hold your thumb up and it covers the moon. Your thumb did not grow.",
         "A demonstration she can perform in the room, which makes the idea physical rather than verbal.",
         ["Ch 38"]),
        ("Say What Else Is True", "evergreen", "Name three other things that are also true right now.",
         "Widens attention without denying the thing, which is the only honest corrective.", ["Ch 38"]),
        ("It Will Be Ordinary", "contrarian", "The thing you are dreading will mostly be an ordinary afternoon.",
         "Contradicts the anticipation rather than the feeling, which is where the error actually lives.",
         ["Ch 38"])],
    "kahneman": "Nothing in life is as important as you think it is while you are thinking about it.",
    "excluded": ["The income and life-satisfaction research, which needs adult framing.",
                 "Any suggestion that her worries are unimportant or that she should stop having them.",
                 "Anything from the priming or ego-depletion chapters."],
    "concepts": [
        {"id": "c1", "title": "Nothing Is As Big As It Seems",
         "hook": "Hold your thumb up at arm's length. You have just covered the moon.",
         "narrative_structure": "story",
         "visual_approach": "A thumb held at arm's length against a small moon, and a soft magnifying lens that makes whatever falls under it swell.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 155,
         "key_points": ["Attention magnifies whatever it lands on",
                        "Size in your head is not size in the world",
                        "The dreaded thing is usually an ordinary afternoon",
                        "You cannot shrink it by thinking harder about it",
                        "Name what else is also true right now"],
         "core_message": "Nothing is ever as big as it seems while you are looking straight at it.",
         "cta": "When one thing fills your head, say out loud three other things that are also true right now.",
         "tone": "Warm, spacious and, as the last film, quietly conclusive.",
         "why_this_works": "It ends the series on the mechanism that sits underneath most of the others, and it does it with a demonstration she can perform in her own bedroom.",
         "grounded_in": ["Ch 38"]},
        {"id": "c2", "title": "Say What Else Is True", "hook": "Name three other true things.",
         "narrative_structure": "tutorial", "visual_approach": "A lens lifting away and the whole page becoming visible again.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 95,
         "key_points": ["Do not argue with it", "Add to it", "Let the picture widen"],
         "core_message": "Add, do not argue.", "cta": "Name three.", "tone": "Practical",
         "why_this_works": "The actionable core with nothing behind it, so it becomes the payoff of c1.",
         "grounded_in": ["Ch 38 corrective"]},
        {"id": "c3", "title": "It Will Be Ordinary", "hook": "The dreaded day is mostly an ordinary afternoon.",
         "narrative_structure": "comparison", "visual_approach": "An enormous shape shrinking to an ordinary small one as it is walked past.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 100,
         "key_points": ["Anticipation inflates", "Arrival deflates", "Neither is a lie"],
         "core_message": "It shrinks when you get there.", "cta": "Remember the last one.", "tone": "Reassuring",
         "why_this_works": "The most immediately useful consequence, but it needs the thumb first, so it becomes the middle of c1.",
         "grounded_in": ["Ch 38"]}],
    "rationale": ("c1 opens with a demonstration she performs herself, which is the strongest possible way to end "
                  "the series: the last idea arrives in her own hand rather than in a sentence."),
    "device_short": "the thumb that covers the moon, and the lens that swells whatever falls under it",
    "art_direction": ("Series house style. New device: a thumb held at arm's length against a small moon, and a "
                      "plain round magnifying lens under which whatever lies beneath swells enormously."),
    "device_lock": ("One plain round glass lens with a simple handle, drawn flat on cream paper. Whatever lies "
                    "under it appears greatly enlarged; everything outside it stays small and ordinary. A raised "
                    "thumb against a small moon is the same idea in the body. Nothing is counted and no numeral "
                    "appears."),
    "anti_patterns": ["asking the image model for an exact count of stars or objects",
                      "two children in one frame", "numerals, labels or lettering of any kind",
                      "anything frightening; the dreaded thing is always a soft neutral shape",
                      "a fully painted night sky; the moon sits on plain cream paper"],
    "tradeoffs": [
        {"tradeoff": "Ending the series with a summary of all seventeen tricks versus one last idea",
         "recommendation": "One last idea",
         "quality_impact": "A recap would turn the final film into homework. The focusing illusion sits underneath most of the earlier films, so it closes the series by implication rather than by listing."},
        {"tradeoff": "Telling her the worry is small versus telling her attention is doing the magnifying",
         "recommendation": "Attention is doing the magnifying",
         "quality_impact": "Calling a real worry small would be dismissive and untrue. Naming the magnifier leaves the worry its actual size while removing the distortion."}],
    "delivery_style": "warm parent reading a bedtime story, spacious and conclusive",
    "performance_intent": ("The same parent and child, seventeen chapters on, and the last one. It should feel like "
                           "the end of a book rather than the end of a lesson: unhurried, and slightly reluctant to "
                           "finish."),
    "energy_curve": ("Playful at the thumb. Wondering at the moon. Gentle and slow through the worry. Warm at the "
                     "tool. Very spacious and slightly wistful at the close of the whole series."),
    "pause_policy": "Three genuine silences: after you have just covered the moon, after your thumb did not grow, and after name three.",
    "sample_section": "s15",
    "human_note": "Section s15 ends the whole series. Leave a long silence after it before the music fades.",
    "reading_age": "Written for a listener of 8. Focusing illusion and affective forecasting never appear as terms.",
    "pause_beats": [{"section": "s2", "purpose": "She actually holds her thumb up and does it"},
                    {"section": "s4", "purpose": "She works out for herself which thing really is bigger"},
                    {"section": "s14", "purpose": "She names three other true things out loud"}],
    "grounded_in": {"s1_to_s4": "Ch 38, attention inflates whatever it lands on",
                    "s5_to_s7": "Ch 38, the lens as the mechanism of the focusing illusion",
                    "s8_to_s10": "Ch 38, anticipated events are predicted to matter more than they do",
                    "s11_to_s12": "Ch 38, the thing keeps its real size while losing the distortion",
                    "s13_to_s15": "Ch 38 corrective, widening attention rather than arguing, plus Pennequin"},
    "guardrails": ["The film never says her worry is small or unimportant, only that attention magnifies it.",
                   "The dreaded thing is always drawn as a soft neutral shape and is never frightening.",
                   "No numeral appears in any illustration.",
                   "No priming or ego-depletion material."],
    "sections": [
        ("s1", "Hold it up", "Hold your thumb up, Diana. Right out at arm's length, in front of your face.",
         'Hold your thumb up, Diana. <break time="0.4s"/> Right out at arm\'s length, <break time="0.3s"/> in front of your face.',
         1.4, "measured", "playful", ["thumb"], "Instructional and light. She should actually do it."),
        ("s2", "The moon", "Now close one eye, and put your thumb over the moon. There. You have just covered the moon.",
         'Now close one eye, and put your thumb over the moon. <break time="0.5s"/> There. <break time="0.4s"/> You have just covered the moon. <break time="2.5s"/>',
         2.5, "measured", "warm", ["covered"], "Pause beat one. Let her enjoy it."),
        ("s3", "Which is bigger", "So. Which one is bigger? Your thumb, or the moon?",
         'So. <break time="0.4s"/> Which one is bigger? <break time="0.4s"/> Your thumb, <break time="0.3s"/> or the moon?',
         1.4, "measured", "curious", ["bigger"], "Genuinely asking."),
        ("s4", "It did not grow", "Your thumb did not grow. It just got very close to your eye.",
         'Your thumb did not grow. <break time="0.5s"/> It just got very close to your eye. <break time="2.5s"/>',
         2.5, "slow", "steady", ["did not grow"], "Pause beat two. The whole film is in this line."),
        ("s5", "Thoughts do it too", "And thoughts do exactly the same thing. Whatever you are looking straight at goes enormous.",
         'And thoughts do exactly the same thing. <break time="0.5s"/> Whatever you are looking straight at goes enormous.',
         1.4, "measured", "curious", ["enormous"], "The hinge."),
        ("s6", "The lens", "It is like carrying a magnifying glass around. Whatever you put under it swells right up and fills the page.",
         'It is like carrying a magnifying glass around. <break time="0.5s"/> Whatever you put under it swells right up and fills the page.',
         1.4, "measured", "warm", ["swells"], "Picture-building."),
        ("s7", "Everything else", "And everything else on the page is still there. It is just outside the glass, so you cannot see it.",
         'And everything else on the page is still there. <break time="0.5s"/> It is just outside the glass, <break time="0.4s"/> so you cannot see it.',
         1.4, "measured", "steady", ["still there"], "Important. Keep it gentle."),
        ("s8", "The dreaded thing", "Which is why the thing you are dreading looks so gigantic the night before.",
         'Which is why the thing you are dreading looks so gigantic the night before.',
         1.4, "slow", "gentle", ["gigantic"], "She will recognise this immediately."),
        ("s9", "And then", "And then it happens. And it turns out to be an afternoon. A perfectly ordinary afternoon, with a bit in the middle you did not enjoy.",
         'And then it happens. <break time="0.5s"/> And it turns out to be an afternoon. <break time="0.4s"/> A perfectly ordinary afternoon, <break time="0.4s"/> with a bit in the middle you did not enjoy.',
         1.4, "measured", "warm", ["ordinary"], "Almost amused, kindly."),
        ("s10", "Same thing", "It was never gigantic. It was just very close to your eye.",
         'It was never gigantic. <break time="0.5s"/> It was just very close to your eye.',
         1.4, "slow", "steady", ["close"], "Callback. Land it."),
        ("s11", "Not pretending", "Now. This does not make the thing not matter. Some things really do matter. It can matter, and still not be the whole picture.",
         'Now. <break time="0.4s"/> This does not make the thing not matter. <break time="0.4s"/> Some things really do matter. <break time="0.5s"/> It can matter, <break time="0.4s"/> and still not be the whole picture.',
         1.4, "measured", "tender", ["whole picture"], "The honesty guard. Do not skip it."),
        ("s12", "Thinking harder", "And you cannot shrink it by thinking about it harder. Thinking about it is the thing making it big.",
         'And you cannot shrink it by thinking about it harder. <break time="0.5s"/> Thinking about it is the thing making it big.',
         1.4, "measured", "steady", ["making it big"], "Plain."),
        ("s13", "The tool", "So here is your last trick. Do not argue with it. Just add to it. Say three other things that are also true right now.",
         'So here is your last trick. <break time="0.5s"/> Do not argue with it. <break time="0.4s"/> Just add to it. <break time="0.5s"/> Say three other things that are also true right now.',
         1.4, "measured", "encouraging", ["add"], "Warm and simple."),
        ("s14", "Try it", "The lamp is on. The dog is asleep. It is nearly the weekend. Go on. Name three.",
         'The lamp is on. <break time="0.3s"/> The dog is asleep. <break time="0.3s"/> It is nearly the weekend. <break time="0.5s"/> Go on. <break time="0.3s"/> Name three. <break time="2.5s"/>',
         2.5, "measured", "encouraging", ["three"], "Pause beat three. She must actually say them."),
        ("s15", "Landing", "Nothing is ever quite as big as it seems while you are looking straight at it. Not even the moon. Goodnight, Diana.",
         'Nothing is ever quite as big as it seems while you are looking straight at it. <break time="0.5s"/> Not even the moon. <break time="0.7s"/> Goodnight, Diana.',
         0.0, "slow", "tender", ["not even the moon"], "The end of the whole series. Unhurried, warm, slightly reluctant to stop."),
    ],
    "spec": [
        ("sc1", "s1", "DIANA", "The girl stands with one arm stretched straight out in front of her and her thumb raised upright, one eye closed, concentrating."),
        ("sc2", "s2", "NONE", "One raised thumb at arm's length exactly covering a small pale moon on plain cream paper. Only the thumb, hand and forearm are visible, with no face and no body."),
        ("sc3", "s2", "DIANA", "The girl looks past her own raised thumb with one eye closed, delighted by what she has just discovered."),
        ("sc4", "s3", "NONE", "One small pale moon drawn alone and quite small in the middle of a large empty cream page."),
        ("sc5", "s4", "NONE", "One raised thumb drawn very large in the near foreground, with the same small pale moon far away behind it and clearly much further off."),
        ("sc6", "s5", "DIANA", "The girl sits with her chin on her knees, one single thought clearly occupying her, looking straight ahead."),
        ("sc7", "s6", "NONE", "One plain round magnifying glass with a simple handle lying on the cream page, with one small soft shape beneath it swollen enormously large."),
        ("sc8", "s6", "NONE", "A close view of the round magnifying glass with one soft rounded grey shape underneath it, hugely enlarged and filling the whole lens."),
        ("sc9", "s7", "NONE", "The round magnifying glass sitting over one part of the page, with many other small soft warm shapes scattered clearly visible all around it outside the glass."),
        ("sc10", "s8", "DIANA", "The girl lies in bed at night with her eyes open, one large soft grey rounded shape hanging above her, filling most of the space above the bed."),
        ("sc11", "s9", "DIANA", "The girl walks along calmly in daylight with one small soft grey shape, now quite small, floating along beside her shoulder."),
        ("sc12", "s10", "NONE", "One soft grey rounded shape drawn small and unremarkable in the middle of a large empty cream page."),
        ("sc13", "s11", "NONE", "One soft grey rounded shape of moderate size resting among several warm coloured shapes on the page, plainly present but not dominant."),
        ("sc14", "s12", "NONE", "One round magnifying glass being held very close over one small shape, with the rest of the page dark and unseen beyond it."),
        ("sc15", "s13", "NONE", "The round magnifying glass lifting away and rising off the page, revealing the whole spread of small soft warm shapes beneath it."),
        ("sc16", "s14", "DIANA", "The girl sits up in bed counting something off on her fingers, calm and occupied, with a small lamp glowing beside her."),
        ("sc17", "s14", "NONE", "A wide gentle spread of many small soft warm shapes filling the page evenly, calm and open, with nothing enlarged."),
        ("sc18", "s15", "DIANA", "The girl sleeps peacefully with her head on the pillow in warm low lamplight, one small pale moon visible in the window beside her, the whole picture settled and quiet."),
    ],
    "heroes": {"sc5", "sc9", "sc15", "sc17", "sc18"},
    "wides": {"sc4", "sc9", "sc15", "sc17"},
}

LENS = ("The magnifying glass is one plain round glass lens with a simple plain handle, drawn flat and simply on "
        "plain empty cream paper. Whatever lies under the lens appears greatly enlarged; everything outside it "
        "stays small. Do not draw any writing, markings or numbers.")
MOON = ("The moon is one plain pale simple circle on empty cream paper. There is no night sky, no stars, no "
        "clouds and no landscape. Do not draw a face on the moon.")
SOFT = ("Any grey shape is a plain soft rounded blob with no face, no eyes, no teeth and nothing frightening about "
        "it whatsoever. It is calm and neutral, never a monster and never a creature.")

FILM["clauses"] = {
    "OPEN": (G.OPEN, {"sc1", "sc2", "sc3", "sc6", "sc10", "sc11", "sc16", "sc18"}),
    "NOICON": (G.NOICON, {"sc1", "sc3", "sc6", "sc11", "sc16", "sc18"}),
    "LENS": (LENS, {"sc7", "sc8", "sc9", "sc14", "sc15", "sc17"}),
    "MOON": (MOON, {"sc2", "sc4", "sc5", "sc18"}),
    "SOFT": (SOFT, {"sc8", "sc10", "sc11", "sc12", "sc13"}),
}

if __name__ == "__main__":
    if "init" in sys.argv:
        G.init(FILM)
    if "build" in sys.argv:
        G.build(FILM)
    if "sheet" in sys.argv:
        G.sheet(FILM)
