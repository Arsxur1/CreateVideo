"""7 Habits half, films 22-24 of 25: Habit 5 / Habit 6 / Habit 7."""
import sys
import filmgen as G
from mindset_e import cbase, SRC, SHOES

# ---------------------------------------------------------------- FILM 22
FILM22 = {**cbase(22, "diana-habits-try-my-glasses", "DianaTryMyGlasses", "Try My Glasses", "Habit 5",
                  "The 7 Habits, Habit 5 'Empathic Listening' - direct excerpt read for this film"),
    "topic": "Seek first to understand, from Habit 5, told through the book's optometrist who hands you his own glasses before he has looked at your eyes",
    "summary": ("Film 22. Habit 5, Seek First to Understand, Then to Be Understood. Covey opens with an optometrist "
                "who listens briefly, takes off his own glasses and hands them over: they have worked for him for "
                "ten years. When everything goes blurry he says they work great for him, try harder, think "
                "positively. His point is that we prescribe before we diagnose. Most people, he writes, do not "
                "listen with the intent to understand; they listen with the intent to reply."),
    "existing": [{"title": "'Be a good listener' classroom posters", "url": SRC, "source": "classroom material", "angle": "Look at the speaker, nod",
                  "what_it_covers": "Teaches the appearance of listening without touching what listening is actually for"},
                 {"title": "Conflict-resolution scripts for children", "url": SRC, "source": "classroom material", "angle": "Use I-statements",
                  "what_it_covers": "Focuses on being understood, which the book says is the half everyone already does"},
                 {"title": "'Give good advice to your friends' guidance", "url": SRC, "source": "web", "angle": "Help them fix it",
                  "what_it_covers": "Rewards jumping straight to a solution, which is precisely prescribing before diagnosing"}],
    "saturated": ["Good-listener posters that teach nodding and eye contact rather than understanding"],
    "gaps": ["Showing a child what it feels like to be handed somebody else's answer before they understood your problem",
             "Naming the specific habit of listening while preparing your reply"],
    "data_points": [("The book opens Habit 5 with an optometrist who hands over his own glasses after listening only briefly, saying he has worn them for ten years and they have really helped him.", SRC, "The 7 Habits, Habit 5", "primary_source", "surprising", "the whole device"),
                     ("When the patient says everything is a blur, the optometrist replies that they work great for him, tells him to try harder, and then to think positively.", SRC, "The 7 Habits, Habit 5", "primary_source", "surprising", "the comic beats a child will recognise from real life"),
                     ("Covey's claim is that most people do not listen with the intent to understand, but with the intent to reply: they are either speaking or preparing to speak.", SRC, "The 7 Habits, 'Empathic Listening'", "primary_source", "expected", "the film's core sentence"),
                     ("He describes listening at levels: ignoring, pretending, selective listening, attentive listening, and above all of those, listening with the intent to understand.", SRC, "The 7 Habits, 'Empathic Listening'", "primary_source", "expected", "the ladder the film climbs")],
    "questions": ["Why does advice sometimes feel annoying even when it's kind?", "How do I actually listen properly?", "Why do people not seem to get what I mean?"],
    "misconceptions": [("Listening means waiting quietly until they finish", "That's usually preparing your reply, which the book says is a different thing entirely.", "Habit 5"),
                        ("Good advice helps regardless of when it's given", "Advice before understanding is somebody else's glasses on your face.", "Habit 5")],
    "pain_points": ["Getting advice that doesn't fit her actual problem", "Rehearsing her answer instead of hearing her friend"],
    "angles": [("Somebody Else's Glasses", "narrative", "He handed over his own glasses before he ever looked at your eyes.", "One comic image that makes a subtle mistake instantly obvious.", ["Habit 5"]),
               ("Listening To Reply", "contrarian", "Most people aren't listening. They're waiting, with their answer already loaded.", "Names a habit she does constantly and has never had pointed out.", ["Habit 5"]),
               ("Look Through Theirs", "evergreen", "The move is to borrow their glasses instead of handing over yours.", "Turns the diagnosis into something she can actually do.", ["Habit 5"])],
    "kahneman": "Most people do not listen with the intent to understand; they listen with the intent to reply, either speaking or preparing to speak.",
    "excluded": ["The adult workplace and marriage examples, and the technical discussion of active and reflective listening techniques."],
    "concepts": [
        {"id": "c1", "title": "Try My Glasses", "hook": "Diana, imagine you go to the eye doctor because things look blurry.", "narrative_structure": "story",
         "visual_approach": "One plain pair of round spectacles, handed over, worn, and finally set down so a second pair can be looked through instead.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 145,
         "key_points": ["He hands over his own glasses without looking at your eyes", "They work perfectly for him and not at all for you", "He tells you to try harder and think positively", "That's what advice before understanding feels like", "Borrow their glasses instead of handing over yours"],
         "core_message": "Advice before understanding is handing somebody your own glasses. Look through theirs first.", "cta": "Before you answer a friend, ask one more question.", "tone": "Comic at first, then quietly serious.",
         "why_this_works": "The joke lands first and the lesson arrives underneath it, which is how an eight-year-old actually takes something in.", "grounded_in": ["Habit 5"]},
        {"id": "c2", "title": "Listening To Reply", "hook": "Most people aren't listening. They're loading their answer.", "narrative_structure": "myth_busting",
         "visual_approach": "Two plain figures facing each other, one with a speech shape already forming before the other has finished.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 75,
         "key_points": ["Silence is not the same as listening", "Preparing your reply feels like listening from the inside"],
         "core_message": "Quiet isn't listening if your answer is already written.", "cta": "Notice when your reply is already loaded.", "tone": "Clear.",
         "why_this_works": "Names a habit she has never had pointed out, folded into c1 as its hinge.", "grounded_in": ["Habit 5"]},
        {"id": "c3", "title": "Look Through Theirs", "hook": "Borrow their glasses instead of handing over yours.", "narrative_structure": "tutorial",
         "visual_approach": "A second, different pair of spectacles being picked up and carefully looked through.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 70,
         "key_points": ["One more question before answering is the whole technique", "You cannot prescribe until you have looked"],
         "core_message": "Ask one more question before you answer.", "cta": "Try one extra question today.", "tone": "Practical and warm.",
         "why_this_works": "Reduces the habit to a single doable move, folded into c1 as its close.", "grounded_in": ["Habit 5"]}],
    "rationale": "c1 carries the optometrist from the joke to the lesson; c2 and c3 are its hinge and its tool, all three using the same pair of spectacles.",
    "device_short": "a pair of plain spectacles handed over before anyone looked at your eyes",
    "art_direction": "New device: one plain pair of round spectacles on cream paper, handed over, worn, set down, and a second differently shaped pair looked through instead.",
    "device_lock": ("Plain simple round spectacles with thin wire frames, drawn flat on cream paper. A second pair "
                    "has a clearly different frame shape. Blur is shown as soft smudging of a plain shape behind "
                    "the lenses. No eye charts, no letters, no numerals, no writing anywhere. Figures are plain "
                    "solid silhouettes with no facial features."),
    "tradeoffs": [{"tradeoff": "Drawing an optometrist's eye chart as the book's setting implies, versus omitting it", "recommendation": "Omit it",
                   "quality_impact": "An eye chart is nothing but letters, which no illustration in this series may contain; the spectacles alone carry the story."}],
    "energy_curve": "Comic through the optometrist. A quiet turn when it stops being funny. Honest at the listening-to-reply beat. Practical and warm at the close.",
    "sample_section": "s8", "human_note": "Section s8 is where the joke turns serious. Let the smile drop out of the voice.",
    "pause_beats": [{"section": "s5", "purpose": "She sits in the absurdity of being told to try harder"}, {"section": "s10", "purpose": "She catches herself loading a reply"}, {"section": "s13", "purpose": "She practises the extra question"}],
    "grounded_in": {"s1_to_s5": "Habit 5, the optometrist story", "s6_to_s9": "Habit 5, prescribing before diagnosing", "s10_to_s12": "Habit 5, listening to reply", "s13_to_s15": "Habit 5 corrective, borrow their glasses"},
    "sections": [
        ("s1", "Setup", "Diana, imagine you go to the eye doctor because things look blurry.", "Diana, imagine you go to the eye doctor because things look blurry.", 1.4, "measured", "warm", ["blurry"], "Easy, story-telling."),
        ("s2", "He barely listens", "You start explaining. He listens for about four seconds. Then he takes off his own glasses and hands them to you.", "You start explaining. <break time=\"0.4s\"/> He listens for about four seconds. <break time=\"0.4s\"/> Then he takes off his own glasses and hands them to you.", 1.4, "measured", "curious", ["his own glasses"], "Let the oddness build."),
        ("s3", "His pitch", "Put these on, he says. I've worn them for ten years. They've really helped me.", "Put these on, he says. <break time=\"0.4s\"/> I've worn them for ten years. <break time=\"0.4s\"/> They've really helped me.", 1.4, "measured", "wry", ["helped me"], "Cheerful, oblivious."),
        ("s4", "It's worse", "So you put them on. And now you can't see anything at all. Everything's a blur.", "So you put them on. <break time=\"0.4s\"/> And now you can't see anything at all. <break time=\"0.3s\"/> Everything's a blur.", 1.4, "measured", "steady", ["a blur"], "Deadpan."),
        ("s5", "His answer", "And do you know what he says? They work great for me. Try harder. And then: think positively.", "And do you know what he says? <break time=\"0.5s\"/> They work great for me. <break time=\"0.3s\"/> Try harder. <break time=\"0.4s\"/> And then: think positively. <break time=\"2.5s\"/>", 2.5, "slow", "wry", ["think positively"], "Pause beat one. Let the absurdity sit. She should laugh."),
        ("s6", "It's ridiculous", "It's silly, isn't it. Nobody would ever do that with eyes.", "It's silly, isn't it. <break time=\"0.4s\"/> Nobody would ever do that with eyes.", 1.4, "measured", "warm", ["nobody would"], "Still light."),
        ("s7", "But", "And yet. That's very nearly what people do to each other all day long, with everything except eyes.", "And yet. <break time=\"0.5s\"/> That's very nearly what people do to each other all day long, <break time=\"0.4s\"/> with everything except eyes.", 1.4, "measured", "steady", ["all day long"], "The turn begins."),
        ("s8", "The real thing", "Somebody tells you they're sad. And out comes your answer, ready made, before you've had a proper look at what's actually wrong. Your glasses. On their face.", "Somebody tells you they're sad. <break time=\"0.5s\"/> And out comes your answer, ready made, <break time=\"0.4s\"/> before you've had a proper look at what's actually wrong. <break time=\"0.5s\"/> Your glasses. <break time=\"0.3s\"/> On their face.", 1.4, "slow", "steady", ["on their face"], "Where the joke turns serious. Drop the smile."),
        ("s9", "It comes from kindness", "And the strange bit is it's almost always meant kindly. Nobody's being horrible. They just answered before they understood.", "And the strange bit is it's almost always meant kindly. <break time=\"0.4s\"/> Nobody's being horrible. <break time=\"0.4s\"/> They just answered before they understood.", 1.4, "measured", "gentle", ["meant kindly"], "No blame anywhere in this."),
        ("s10", "Her turn", "Now here's the uncomfortable one. When a friend is talking, are you listening? Or are you just waiting, with your answer already loaded?", "Now here's the uncomfortable one. <break time=\"0.5s\"/> When a friend is talking, are you listening? <break time=\"0.4s\"/> Or are you just waiting, with your answer already loaded? <break time=\"2.5s\"/>", 2.5, "slow", "gentle", ["already loaded"], "Pause beat two. Honest, not accusing."),
        ("s11", "Everyone does it", "I do it. Constantly. Being quiet and listening turn out to be two completely different things.", "I do it. <break time=\"0.3s\"/> Constantly. <break time=\"0.4s\"/> Being quiet and listening turn out to be two completely different things.", 1.4, "measured", "warm", ["two different things"], "Genuine admission."),
        ("s12", "The other way", "So the move isn't to hand over your glasses faster. It's to borrow theirs for a minute. To have a look out of their window before you say anything.", "So the move isn't to hand over your glasses faster. <break time=\"0.5s\"/> It's to borrow theirs for a minute. <break time=\"0.4s\"/> To have a look out of their window before you say anything.", 1.4, "measured", "steady", ["borrow theirs"], "The corrective."),
        ("s13", "The tool", "And there's a very small way to do it. Ask one more question before you answer. Just one more. That's the whole habit.", "And there's a very small way to do it. <break time=\"0.4s\"/> Ask one more question before you answer. <break time=\"0.4s\"/> Just one more. <break time=\"0.3s\"/> That's the whole habit. <break time=\"2.5s\"/>", 2.5, "measured", "encouraging", ["one more question"], "Pause beat three. The actual tool."),
        ("s14", "What it does", "It's amazing what one more question does. People change what they're telling you when they realise you actually want to know.", "It's amazing what one more question does. <break time=\"0.4s\"/> People change what they're telling you when they realise you actually want to know.", 1.4, "measured", "warm", ["actually want to know"], "Warm, a little surprised."),
        ("s15", "Landing", "I'll try to keep my glasses off your face, Diana. And when you tell me something, I'll ask one more question first.", "I'll try to keep my glasses off your face, Diana. <break time=\"0.5s\"/> And when you tell me something, <break time=\"0.4s\"/> I'll ask one more question first.", 0.0, "slow", "tender", ["one more question first"], "Personal, warm, unhurried close."),
    ],
    "spec": [
        ("sc1", "s1", "DIANA", "The girl squints slightly at something in the distance, trying to focus."),
        ("sc2", "s2", "NONE", "Exactly ONE single pair of plain round wire spectacles held out toward the viewer by an unseen hand, only the hand and forearm visible, no face and no body. There is exactly one pair of spectacles in the picture and nothing else at all."),
        ("sc3", "s3", "NONE", "Exactly ONE single pair of plain round wire spectacles lying alone on the cream page, ordinary and unremarkable, with nothing else at all in the picture."),
        ("sc4", "s4", "NONE", "One plain simple solid circle shape seen THROUGH the lenses of a single pair of round spectacles, the circle soft and badly smudged and clearly out of focus. Exactly one pair of spectacles in the picture."),
        ("sc5", "s5", "DIANA", "The girl looks baffled and a little exasperated, eyebrows raised."),
        ("sc6", "s6", "DIANA", "The girl laughs quietly, amused, with both hands empty and relaxed at her sides. She is holding nothing at all and there are no objects anywhere in the picture."),
        ("sc7", "s7", "NONE", "Two plain solid human figure silhouettes facing each other, the left one holding out a single small pair of spectacles toward the face of the right one. Exactly one pair of spectacles in the picture and nothing floating anywhere."),
        ("sc8", "s8", "NONE", "One plain solid HUMAN figure silhouette of an adult person, standing slightly hunched and uncertain and wearing a single pair of spectacles that plainly do not suit it. It is a person and NOT an animal. Exactly one pair of spectacles in the picture and nothing else."),
        ("sc9", "s9", "DIANA", "The girl looks thoughtful and a bit sorry, recognising something."),
        ("sc10", "s10", "DIANA", "The girl stands listening with her mouth slightly open, plainly about to speak, caught mid-thought."),
        ("sc11", "s11", "DIANA", "The girl looks honest and a little sheepish, admitting something."),
        ("sc12", "s12", "NONE", "A second pair of spectacles with a clearly different frame shape, resting on the cream page beside the first pair."),
        ("sc13", "s13", "NONE", "A single pair of plain spectacles with a square frame shape held up carefully by an unseen hand, and one plain simple solid circle shape seen sharply and clearly through its lenses. Exactly one pair of spectacles in the picture."),
        ("sc14", "s14", "DIANA", "The girl leans in with genuine interest, attentive and curious, really listening."),
        ("sc15", "s15", "DIANA", "The girl stands calm and warm in soft evening light."),
        ("sc16", "s4", "NONE", "A close view of ONE single pair of round spectacles filling the frame, with one plain solid circle shape behind the lenses drawn very soft, smudged and out of focus. Exactly one pair of spectacles."),
        ("sc17", "s13", "NONE", "A close view of ONE single pair of square-framed spectacles filling the frame, with one plain solid circle shape behind the lenses drawn crisp, sharp and perfectly clear. Exactly one pair of spectacles and no decoration of any kind."),
        ("sc18", "s15", "NONE", "The two different pairs of spectacles resting side by side in warm evening light, calm and settled."),
    ],
    "heroes": {"sc13", "sc16", "sc17", "sc18"}, "wides": set(),
}
FILM22["clauses"] = {
    "OPEN": (G.OPEN, {"sc1", "sc5", "sc6", "sc9", "sc10", "sc11", "sc14", "sc15"}),
    "NOICON": (G.NOICON, {"sc1", "sc5", "sc6", "sc9", "sc10", "sc11", "sc14", "sc15"}),
    "SHOES": (SHOES, {"sc1", "sc5", "sc6", "sc9", "sc10", "sc11", "sc14", "sc15"}),
    "GLASSES": (("Spectacles are drawn plainly and flatly on cream paper with thin simple frames. Draw ONLY the "
                 "objects named in the description and nothing else: if the description names one pair of "
                 "spectacles, exactly ONE pair appears in the picture and there is no second pair anywhere in "
                 "the frame. Absolutely NO eye chart, NO letters, NO numerals, NO writing, NO stars, NO "
                 "decorative symbols, NO animals, NO toys and NO sea creatures. Figures are plain solid HUMAN "
                 "silhouettes with no facial features. No scenery, no background, nothing floating."),
                {"sc2", "sc3", "sc4", "sc7", "sc8", "sc12", "sc13", "sc16", "sc17", "sc18"}),
}

# ---------------------------------------------------------------- FILM 23
FILM23 = {**cbase(23, "diana-habits-one-and-one", "DianaOneAndOne", "One and One Makes Four", "Habit 6",
                  "The 7 Habits, Habit 6 'Valuing the Differences' - direct excerpt read for this film"),
    "topic": "Synergy and valuing differences, from Habit 6, told through two colours that together make one neither could make alone",
    "summary": ("Film 23. Habit 6, Synergize. Covey's line is that one plus one usually equals two, but that people "
                "who value their differences can make one plus one equal four: the whole becomes greater than the "
                "sum of the parts. He calls valuing the differences the essence of synergy, and says the key to it "
                "is realising that people see the world not as it is, but as they are."),
    "existing": [{"title": "'Teamwork makes the dream work' classroom slogans", "url": SRC, "source": "classroom material", "angle": "Work together",
                  "what_it_covers": "Asks children to cooperate without explaining what cooperation actually produces"},
                 {"title": "Group-project role charts", "url": SRC, "source": "classroom material", "angle": "Divide the work",
                  "what_it_covers": "Splits a task into parts, which is addition, not the thing the book is describing"},
                 {"title": "'Everyone is different and that's okay' picture books", "url": SRC, "source": "web", "angle": "Tolerate difference",
                  "what_it_covers": "Asks a child to put up with differences rather than showing what they are for"}],
    "saturated": ["Teamwork slogans that ask for cooperation without showing what it produces"],
    "gaps": ["Showing that difference is the ingredient, not the obstacle",
             "Distinguishing dividing up a job from actually making something neither person could make alone"],
    "data_points": [("Covey's formulation is that one plus one usually equals two, but people who value their differences can make one plus one equal four.", SRC, "The 7 Habits, Habit 6", "primary_source", "surprising", "the hook, which a child will immediately object to"),
                     ("He defines synergy as the whole being greater than the sum of the parts.", SRC, "The 7 Habits, Habit 6", "primary_source", "expected", "the principle underneath the colours"),
                     ("He calls valuing the differences the essence of synergy: the mental, emotional and psychological differences between people.", SRC, "The 7 Habits, 'Valuing the Differences'", "primary_source", "expected", "why sameness produces nothing new"),
                     ("His key to valuing differences is realising that all people see the world not as it is, but as they are.", SRC, "The 7 Habits, 'Valuing the Differences'", "primary_source", "surprising", "the link back to the glasses film")],
    "questions": ["Why do I have to work with someone who does everything differently?", "Isn't it easier to just do it my way?", "What's the point of disagreeing?"],
    "misconceptions": [("Working together means splitting the job up", "That's addition. Synergy is making something neither of you could have made alone.", "Habit 6"),
                        ("Differences are the annoying part of working together", "The book says the differences are the actual ingredient.", "Habit 6")],
    "pain_points": ["Getting frustrated with someone whose approach differs from hers", "Wanting to take over a group task and do it alone"],
    "angles": [("Two Colours, One New One", "narrative", "Blue and yellow make a green neither of them could make alone.", "Makes an abstract idea physical and instantly verifiable.", ["Habit 6"]),
               ("Sameness Makes Nothing", "contrarian", "Mix two identical colours and you get the colour you started with.", "Shows why difference is the ingredient rather than the obstacle.", ["Habit 6"]),
               ("Not Splitting, Making", "evergreen", "Dividing a job is addition. This is something else entirely.", "Corrects the version of teamwork she is actually taught at school.", ["Habit 6"])],
    "kahneman": "One plus one usually equals two, but where differences are valued the whole becomes greater than the sum of the parts.",
    "excluded": ["The adult business negotiation and organisational examples, and the discussion of left and right brain theory."],
    "concepts": [
        {"id": "c1", "title": "One and One Makes Four", "hook": "Diana, I'm going to say something wrong on purpose. One and one makes four.", "narrative_structure": "story",
         "visual_approach": "Two plain blobs of paint, one blue and one yellow, running together into a green that neither contained.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 145,
         "key_points": ["Blue and yellow make a green neither one had", "Two of the same colour make nothing new", "The difference was the ingredient", "Splitting a job in half is only addition", "Disagreeing is where the new colour comes from"],
         "core_message": "The difference between you isn't the problem with working together. It's the entire point of it.", "cta": "Next time someone does it differently, ask what colour you'd make together.", "tone": "Playful, then genuinely curious.",
         "why_this_works": "She can verify the paint claim herself, which makes the human version credible.", "grounded_in": ["Habit 6"]},
        {"id": "c2", "title": "Sameness Makes Nothing", "hook": "Mix two of the same colour and you get that colour.", "narrative_structure": "comparison",
         "visual_approach": "Two identical blue blobs running together into exactly the same blue.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 70,
         "key_points": ["Agreement produces nothing that wasn't already there", "The new thing needs two genuinely different starting points"],
         "core_message": "Two the same makes one the same.", "cta": "Stop wishing everyone agreed with you.", "tone": "Dry and clear.",
         "why_this_works": "Proves the necessity of difference in one image, folded into c1 as its hinge.", "grounded_in": ["Habit 6"]},
        {"id": "c3", "title": "Not Splitting, Making", "hook": "Dividing a job in half is only addition.", "narrative_structure": "myth_busting",
         "visual_approach": "Two paint blobs sitting neatly side by side without touching, unchanged.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 70,
         "key_points": ["Side by side and unchanged is not working together", "The colours have to actually meet"],
         "core_message": "If nothing new came out, you only shared the work.", "cta": "Let the ideas actually touch.", "tone": "Practical.",
         "why_this_works": "Corrects the school version of teamwork, folded into c1 as its close.", "grounded_in": ["Habit 6"]}],
    "rationale": "c1 carries the two colours from separate to mixed; c2 and c3 are its proof and its correction, all three using the same two blobs of paint.",
    "device_short": "two colours of paint running together into a third neither one had",
    "art_direction": "New device: two plain soft blobs of paint on cream paper, one blue and one warm yellow, shown apart, meeting, and merged into a clear green.",
    "device_lock": ("Two plain soft rounded blobs of paint on cream paper, one clear blue and one warm yellow, with "
                    "a soft painted edge. Where they meet the overlap is a clear distinct green. No brushes, no "
                    "palettes, no jars, no scenery, no numerals, no writing, no arrows and no labels."),
    "tradeoffs": [{"tradeoff": "Showing the sum in numerals as the book writes it, versus keeping it spoken only", "recommendation": "Spoken only",
                   "quality_impact": "No illustration in this series may contain a numeral; the arithmetic lives entirely in the narration and the picture carries the colours."}],
    "energy_curve": "Playful and provocative at the wrong sum. Delighted at the green. Dry at the sameness beat. Warm and encouraging at the close.",
    "sample_section": "s6", "human_note": "Section s6 is the green arriving. Genuine delight, as if seeing it for the first time.",
    "pause_beats": [{"section": "s5", "purpose": "She watches the two colours actually meet"}, {"section": "s10", "purpose": "She thinks of someone who does things differently"}, {"section": "s13", "purpose": "She considers what they'd make together"}],
    "grounded_in": {"s1_to_s5": "Habit 6, the wrong sum and the two colours", "s6_to_s9": "Habit 6, the whole greater than the parts", "s10_to_s12": "Habit 6, valuing the differences", "s13_to_s15": "Habit 6 corrective, letting ideas meet"},
    "sections": [
        ("s1", "Setup", "Diana, I'm going to say something wrong on purpose. One and one makes four.", "Diana, I'm going to say something wrong on purpose. <break time=\"0.5s\"/> One and one makes four.", 1.4, "measured", "playful", ["makes four"], "Cheeky. She will object."),
        ("s2", "She objects", "I know. I know. Hold on, though. I want to show you something.", "I know. <break time=\"0.3s\"/> I know. <break time=\"0.4s\"/> Hold on, though. <break time=\"0.4s\"/> I want to show you something.", 1.4, "measured", "warm", ["hold on"], "Enjoying himself."),
        ("s3", "Two colours", "Here's a blob of blue paint. And here's a blob of yellow.", "Here's a blob of blue paint. <break time=\"0.4s\"/> And here's a blob of yellow.", 1.4, "measured", "curious", ["blue", "yellow"], "Simple, clear."),
        ("s4", "Neither is green", "Now, there's no green in the blue one. And there's no green in the yellow one. Have a proper look.", "Now, there's no green in the blue one. <break time=\"0.4s\"/> And there's no green in the yellow one. <break time=\"0.4s\"/> Have a proper look.", 1.4, "measured", "steady", ["no green"], "Set it up honestly."),
        ("s5", "Let them meet", "Now let them run into each other. Watch the middle bit.", "Now let them run into each other. <break time=\"0.4s\"/> Watch the middle bit. <break time=\"2.5s\"/>", 2.5, "slow", "curious", ["the middle bit"], "Pause beat one. Genuine looking time."),
        ("s6", "The green", "Green. Out of nowhere. Something that was in neither one of them, and now it's just there.", "Green. <break time=\"0.4s\"/> Out of nowhere. <break time=\"0.5s\"/> Something that was in neither one of them, <break time=\"0.4s\"/> and now it's just there.", 1.4, "slow", "delighted", ["out of nowhere"], "Real delight. As if seeing it fresh."),
        ("s7", "That's the four", "That's my four. Not two blobs sitting next to each other. A thing that didn't exist until they met.", "That's my four. <break time=\"0.4s\"/> Not two blobs sitting next to each other. <break time=\"0.4s\"/> A thing that didn't exist until they met.", 1.4, "measured", "warm", ["until they met"], "Land the metaphor."),
        ("s8", "Now the test", "Now try it the other way. Two blobs of blue. Same blue. Run them together.", "Now try it the other way. <break time=\"0.4s\"/> Two blobs of blue. <break time=\"0.3s\"/> Same blue. <break time=\"0.4s\"/> Run them together.", 1.4, "measured", "curious", ["same blue"], "Set up the contrast."),
        ("s9", "Nothing", "And you get blue. A bit more of it. But nothing new. Nothing at all.", "And you get blue. <break time=\"0.4s\"/> A bit more of it. <break time=\"0.4s\"/> But nothing new. <break time=\"0.3s\"/> Nothing at all.", 1.4, "measured", "dry", ["nothing new"], "Dry, definite."),
        ("s10", "The point", "So it was the difference that made the green. Not the agreeing. The difference. Think about somebody who does things nothing like you do.", "So it was the difference that made the green. <break time=\"0.4s\"/> Not the agreeing. <break time=\"0.3s\"/> The difference. <break time=\"0.5s\"/> Think about somebody who does things nothing like you do. <break time=\"2.5s\"/>", 2.5, "slow", "steady", ["the difference"], "Pause beat two. Let her picture a real person."),
        ("s11", "The annoying one", "Probably somebody a bit annoying, if I'm honest. The one who wants to do the whole thing backwards.", "Probably somebody a bit annoying, if I'm honest. <break time=\"0.4s\"/> The one who wants to do the whole thing backwards.", 1.4, "measured", "wry", ["a bit annoying"], "Light and knowing."),
        ("s12", "Reframe", "That person is your yellow, Diana. They're not the problem with working together. They're the reason it's worth doing at all.", "That person is your yellow, Diana. <break time=\"0.5s\"/> They're not the problem with working together. <break time=\"0.4s\"/> They're the reason it's worth doing at all.", 1.4, "slow", "warm", ["your yellow"], "The heart of the film. Warm."),
        ("s13", "Not splitting", "One warning though. Splitting a job in half isn't this. Two blobs sitting politely side by side make nothing. The colours have to actually touch.", "One warning though. <break time=\"0.4s\"/> Splitting a job in half isn't this. <break time=\"0.4s\"/> Two blobs sitting politely side by side make nothing. <break time=\"0.5s\"/> The colours have to actually touch. <break time=\"2.5s\"/>", 2.5, "measured", "steady", ["actually touch"], "Pause beat three. Important correction."),
        ("s14", "So argue", "Which means the disagreeing bit isn't the failure. It's the part where the green happens.", "Which means the disagreeing bit isn't the failure. <break time=\"0.4s\"/> It's the part where the green happens.", 1.4, "measured", "encouraging", ["where the green happens"], "Bright, freeing."),
        ("s15", "Landing", "You and me are different colours too, Diana. I've always rather liked what we make.", "You and me are different colours too, Diana. <break time=\"0.5s\"/> I've always rather liked what we make.", 0.0, "slow", "tender", ["what we make"], "Personal, warm, unhurried close."),
    ],
    "spec": [
        ("sc1", "s1", "DIANA", "The girl looks up sharply with a sceptical raised eyebrow, about to object."),
        ("sc2", "s2", "DIANA", "The girl folds her arms with an amused doubtful expression, waiting to be convinced."),
        ("sc3", "s3", "NONE", "One soft rounded blob of clear blue paint and one soft rounded blob of warm yellow paint, well apart on cream paper."),
        ("sc4", "s4", "NONE", "A close view of the blue blob alone, plainly and entirely blue."),
        ("sc5", "s5", "NONE", "The blue and yellow blobs flowing toward each other, their edges just beginning to touch."),
        ("sc6", "s6", "NONE", "The two blobs overlapping, a clear distinct green appearing in the middle where they meet."),
        ("sc7", "s7", "DIANA", "The girl looks genuinely delighted and surprised, eyes wide."),
        ("sc8", "s8", "NONE", "TWO separate blobs of paint well apart from each other, and BOTH of them are exactly the same clear blue. There is no yellow anywhere in the picture and no green anywhere in the picture. Only two blue blobs and nothing else."),
        ("sc9", "s9", "NONE", "ONE single large blob of clear blue paint alone in the middle of the cream page. There is no yellow anywhere in the picture and no green anywhere in the picture. Only one blue blob and nothing else."),
        ("sc10", "s10", "DIANA", "The girl looks thoughtful, considering a particular person."),
        ("sc11", "s11", "DIANA", "The girl gives a small wry smile, recognising somebody."),
        ("sc12", "s12", "DIANA", "The girl's expression softens with understanding, warm and a little surprised."),
        ("sc13", "s13", "NONE", "One blue blob and one warm yellow blob sitting neatly side by side with a clear empty gap between them so that they do NOT touch at any point. There is no green anywhere in the picture because nothing overlaps."),
        ("sc14", "s14", "DIANA", "The girl looks bright and encouraged, ready to try something."),
        ("sc15", "s15", "DIANA", "The girl stands calm and warm in soft evening light."),
        ("sc16", "s6", "NONE", "A close view of the green where the blue and yellow overlap, rich and clear."),
        ("sc17", "s9", "NONE", "A close view of ONE single blob of clear blue paint, flat and unremarkable, filling much of the frame. There is no yellow anywhere in the picture and no green anywhere in the picture."),
        ("sc18", "s15", "NONE", "The blue and yellow blobs overlapping in warm evening light with a broad clear green between them, calm and settled."),
    ],
    "heroes": {"sc6", "sc16", "sc18"}, "wides": set(),
}
FILM23["clauses"] = {
    "OPEN": (G.OPEN, {"sc1", "sc2", "sc7", "sc10", "sc11", "sc12", "sc14", "sc15"}),
    "NOICON": (G.NOICON, {"sc1", "sc2", "sc7", "sc10", "sc11", "sc12", "sc14", "sc15"}),
    "SHOES": (SHOES, {"sc1", "sc2", "sc7", "sc10", "sc11", "sc12", "sc14", "sc15"}),
    "PAINT": (("Paint blobs are plain soft rounded shapes with soft painted edges, drawn flat on cream paper. Draw "
               "ONLY the blobs named in the description, in exactly the colours named, and nothing else: no "
               "extra blobs, no extra colours and no stray circles anywhere in the frame. No brushes, no "
               "palettes, no jars, no hands, no scenery, no background, no numerals, no writing, no arrows "
               "and no labels."),
              {"sc3", "sc4", "sc5", "sc6", "sc8", "sc9", "sc13", "sc16", "sc17", "sc18"}),
}

# ---------------------------------------------------------------- FILM 24
FILM24 = {**cbase(24, "diana-habits-too-busy-sawing", "DianaTooBusySawing", "Too Busy Sawing", "Habit 7",
                  "The 7 Habits, Habit 7 'Sharpen the Saw' - direct excerpt read for this film"),
    "topic": "Sharpen the Saw, from Habit 7, told through the book's exhausted woodcutter who has no time to sharpen because he is too busy sawing",
    "summary": ("Film 24. Habit 7, Sharpen the Saw, and the last of the teaching films. Covey's story is of a man "
                "sawing feverishly at a tree for over five hours, exhausted. Asked why he does not stop and sharpen "
                "the saw, he answers that he has no time, he is too busy sawing. Covey calls Habit 7 personal PC: "
                "preserving and enhancing the greatest asset you have, which is you. It sits at the centre of the "
                "Circle of Influence, so nobody else can do it for you."),
    "existing": [{"title": "'Push through and finish' encouragement", "url": SRC, "source": "web", "angle": "Don't stop now",
                  "what_it_covers": "Rewards continuing at any cost and treats stopping as weakness"},
                 {"title": "Homework-stamina advice for children", "url": SRC, "source": "classroom material", "angle": "Build your concentration",
                  "what_it_covers": "Treats effort as a quantity to increase rather than a tool that goes blunt"},
                 {"title": "Screen-time and rest guidance for kids", "url": SRC, "source": "web", "angle": "Take breaks",
                  "what_it_covers": "Prescribes breaks as a rule without ever explaining what a break is actually doing"}],
    "saturated": ["Push-through encouragement that treats stopping as a failure of will"],
    "gaps": ["Explaining what a break is actually for, rather than prescribing one",
             "Showing that the tool going blunt is invisible from inside the sawing"],
    "data_points": [("The book's story is of a man sawing feverishly at a tree, exhausted, who has been at it over five hours.", SRC, "The 7 Habits, Habit 7", "primary_source", "expected", "the device"),
                     ("Asked why he does not pause to sharpen the saw, he replies that he has no time because he is too busy sawing.", SRC, "The 7 Habits, Habit 7", "primary_source", "surprising", "the film's central line, and one a child recognises instantly"),
                     ("Covey calls Habit 7 personal PC: preserving and enhancing the greatest asset you have, which is you.", SRC, "The 7 Habits, Habit 7", "primary_source", "expected", "the direct callback to the goose film"),
                     ("He notes that sharpening the saw is a Quadrant II activity and sits at the centre of your Circle of Influence, so no one else can do it for you.", SRC, "The 7 Habits, Habit 7", "primary_source", "expected", "callbacks to the four-boxes film and the circles film")],
    "questions": ["Why do I get slower the longer I work?", "Is stopping the same as giving up?", "What is a break actually for?"],
    "misconceptions": [("Stopping means you're not committed", "The man who wouldn't stop was the one getting nowhere.", "Habit 7"),
                        ("If it's getting harder you just need to push harder", "It may be getting harder because the tool has gone blunt, and pushing makes that worse.", "Habit 7")],
    "pain_points": ["Working longer and getting less done", "Feeling guilty for stopping when there's more to do"],
    "angles": [("Too Busy Sawing", "narrative", "He can't stop to sharpen it. He's far too busy getting nowhere.", "One image that makes the absurdity of pure persistence visible.", ["Habit 7"]),
               ("The Blunt Tool", "contrarian", "It got harder because the saw went blunt, not because you got weaker.", "Reframes a discouraging feeling as a maintenance problem.", ["Habit 7"]),
               ("Nobody Else Can Sharpen It", "evergreen", "This one sits inside your own circle. Nobody can do it for you.", "Deliberately ties Habit 7 back to the circle film.", ["Habit 7"])],
    "kahneman": "Asked why he does not stop and sharpen the saw, the exhausted man replies that he has no time, because he is too busy sawing.",
    "excluded": ["The adult exercise physiology, heart-rate arithmetic and the spiritual dimension's religious framing, which need adult context."],
    "concepts": [
        {"id": "c1", "title": "Too Busy Sawing", "hook": "Diana, there's a man in the woods sawing a tree, and he's been at it five hours.", "narrative_structure": "story",
         "visual_approach": "A plain saw and a partly cut tree, the saw shown sharp, then blunt and struggling, then sharpened again.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 150,
         "key_points": ["Five hours of sawing and barely through", "Asked to sharpen it, he says he has no time", "The saw went blunt, he didn't get weaker", "Sharpening feels like stopping and isn't", "Nobody else can sharpen yours"],
         "core_message": "He wasn't getting weaker. The saw was getting blunt. Stopping to sharpen it is the fastest thing he could do.", "cta": "When it gets harder, ask whether the saw needs sharpening.", "tone": "Warm, wry, then genuinely caring.",
         "why_this_works": "It gives her a reason to rest that is about effectiveness, not permission, which is much easier to accept.", "grounded_in": ["Habit 7"]},
        {"id": "c2", "title": "The Blunt Tool", "hook": "It got harder because the saw went blunt.", "narrative_structure": "myth_busting",
         "visual_approach": "A close view of a saw's teeth, worn flat and dull.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 75,
         "key_points": ["Getting slower is information about the tool, not the person", "You cannot see a blunt saw from inside the sawing"],
         "core_message": "You didn't get worse. The tool went dull.", "cta": "Read the slowdown as a signal, not a verdict.", "tone": "Reassuring.",
         "why_this_works": "Turns a discouraging feeling into a diagnosis, folded into c1 as its hinge.", "grounded_in": ["Habit 7"]},
        {"id": "c3", "title": "Nobody Else Can Sharpen It", "hook": "This one is inside your own circle.", "narrative_structure": "analogy",
         "visual_approach": "One saw resting alone, waiting, with nobody else in the frame.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 70,
         "key_points": ["Nobody can rest or sharpen on your behalf", "It sits squarely inside the circle you can reach"],
         "core_message": "Nobody else can sharpen your saw for you.", "cta": "Put it in your own circle and do it.", "tone": "Steady and warm.",
         "why_this_works": "Ties Habit 7 back to the circle film and hands her ownership, folded into c1 as its close.", "grounded_in": ["Habit 7"]}],
    "rationale": "c1 carries the woodcutter from exhaustion to a sharp saw; c2 and c3 are its diagnosis and its ownership, all three using the same saw.",
    "device_short": "a saw that goes blunt while its owner is too busy to sharpen it",
    "art_direction": "New device: one plain simple handsaw and a partly cut tree trunk on cream paper, the saw shown sharp, blunt, and sharpened again.",
    "device_lock": ("One plain simple handsaw with a plain wooden handle and a straight blade with simple triangular "
                    "teeth, drawn flat on cream paper. One plain tree trunk with a shallow cut in it. Blunt teeth "
                    "are drawn worn flat and rounded. No forest scenery, no leaves, no numerals, no writing, no "
                    "sparkles. Figures are plain solid silhouettes with no facial features."),
    "tradeoffs": [{"tradeoff": "Showing the four dimensions of renewal as the book lists them, versus keeping one saw", "recommendation": "One saw",
                   "quality_impact": "The book's four dimensions include a spiritual one framed for adults; a single saw carries the principle at a scale an eight-year-old can act on today."}],
    "energy_curve": "Wry through the woodcutter. A turn at the blunt teeth. Warm and caring at the ownership beat. Settled at the close of the teaching films.",
    "sample_section": "s9", "human_note": "Section s9 is the reframe from weakness to bluntness. This is the reassuring line. Warm.",
    "pause_beats": [{"section": "s5", "purpose": "She sits with the absurdity of the answer"}, {"section": "s10", "purpose": "She thinks of a time she got slower and blamed herself"}, {"section": "s13", "purpose": "She picks how she'll sharpen hers"}],
    "grounded_in": {"s1_to_s5": "Habit 7, the woodcutter", "s6_to_s9": "Habit 7, the blunt saw", "s10_to_s12": "Habit 7, personal PC and the circle", "s13_to_s15": "Habit 7 corrective, sharpening yours"},
    "sections": [
        ("s1", "Setup", "Diana, there's a man in the woods sawing a tree, and he's been at it five hours.", "Diana, there's a man in the woods sawing a tree, <break time=\"0.4s\"/> and he's been at it five hours.", 1.4, "measured", "warm", ["five hours"], "Storyteller's ease."),
        ("s2", "He's finished", "He's absolutely worn out. Sweating. Barely moving the blade. And he's hardly got through the trunk at all.", "He's absolutely worn out. <break time=\"0.3s\"/> Sweating. <break time=\"0.3s\"/> Barely moving the blade. <break time=\"0.4s\"/> And he's hardly got through the trunk at all.", 1.4, "measured", "steady", ["hardly got through"], "Sympathetic."),
        ("s3", "The suggestion", "So somebody walks past and says, why don't you stop for a few minutes and sharpen the saw? It'd go much faster.", "So somebody walks past and says, <break time=\"0.3s\"/> why don't you stop for a few minutes and sharpen the saw? <break time=\"0.4s\"/> It'd go much faster.", 1.4, "measured", "curious", ["sharpen the saw"], "Reasonable, gentle."),
        ("s4", "His answer", "And the man says: I haven't got time to sharpen the saw. I'm too busy sawing.", "And the man says: <break time=\"0.5s\"/> I haven't got time to sharpen the saw. <break time=\"0.4s\"/> I'm too busy sawing.", 1.4, "slow", "wry", ["too busy sawing"], "Deliver it straight. It should land as funny and sad at once."),
        ("s5", "Let it sit", "Have a think about that one for a second.", "Have a think about that one for a second. <break time=\"2.5s\"/>", 2.5, "slow", "steady", ["think about that"], "Pause beat one. Let her get it."),
        ("s6", "It's us", "It's ridiculous. And I do it about twice a week.", "It's ridiculous. <break time=\"0.4s\"/> And I do it about twice a week.", 1.4, "measured", "wry", ["twice a week"], "Dry, self-deprecating."),
        ("s7", "The blade", "Here's what's actually happening to him. Every hour he saws, the teeth on that blade get a little more worn down.", "Here's what's actually happening to him. <break time=\"0.4s\"/> Every hour he saws, the teeth on that blade get a little more worn down.", 1.4, "measured", "curious", ["worn down"], "Explain the mechanism."),
        ("s8", "He can't see it", "And he can't see it. From where he's standing it just feels like the tree's getting harder. Or he's getting weaker.", "And he can't see it. <break time=\"0.4s\"/> From where he's standing it just feels like the tree's getting harder. <break time=\"0.4s\"/> Or he's getting weaker.", 1.4, "measured", "gentle", ["getting weaker"], "This is the key misreading."),
        ("s9", "The reframe", "But he isn't getting weaker, Diana. The saw is going blunt. Those are two completely different problems, and only one of them is about him.", "But he isn't getting weaker, Diana. <break time=\"0.5s\"/> The saw is going blunt. <break time=\"0.5s\"/> Those are two completely different problems, <break time=\"0.4s\"/> and only one of them is about him.", 1.4, "slow", "warm", ["going blunt"], "The reassuring line. Warm and certain."),
        ("s10", "Her turn", "Think of a time something got harder and harder and you decided it was you. That you'd got worse at it.", "Think of a time something got harder and harder and you decided it was you. <break time=\"0.4s\"/> That you'd got worse at it. <break time=\"2.5s\"/>", 2.5, "slow", "gentle", ["decided it was you"], "Pause beat two. She'll have one."),
        ("s11", "Probably blunt", "Might have been a blunt saw. Tired. Hungry. Hadn't slept. Hadn't stopped in weeks. Blunt isn't broken.", "Might have been a blunt saw. <break time=\"0.3s\"/> Tired. <break time=\"0.3s\"/> Hungry. <break time=\"0.3s\"/> Hadn't slept. <break time=\"0.3s\"/> Hadn't stopped in weeks. <break time=\"0.4s\"/> Blunt isn't broken.", 1.4, "measured", "tender", ["blunt isn't broken"], "Gentle. This may be a real relief."),
        ("s12", "Your circle", "And remember the two circles? This one sits right in the middle of the small one. Nobody else can sharpen your saw. Not me, not anybody.", "And remember the two circles? <break time=\"0.4s\"/> This one sits right in the middle of the small one. <break time=\"0.5s\"/> Nobody else can sharpen your saw. <break time=\"0.3s\"/> Not me, not anybody.", 1.4, "measured", "steady", ["nobody else"], "Callback to film 16. Firm and warm."),
        ("s13", "The move", "So when something starts getting harder, ask the question. Is this me, or is this a blunt saw? And then go and sharpen it.", "So when something starts getting harder, ask the question. <break time=\"0.4s\"/> Is this me, or is this a blunt saw? <break time=\"0.5s\"/> And then go and sharpen it. <break time=\"2.5s\"/>", 2.5, "measured", "encouraging", ["blunt saw"], "Pause beat three. The actual tool."),
        ("s14", "It feels wrong", "It'll feel like you're wasting time. It always does. It's the fastest thing you could possibly do.", "It'll feel like you're wasting time. <break time=\"0.4s\"/> It always does. <break time=\"0.4s\"/> It's the fastest thing you could possibly do.", 1.4, "measured", "warm", ["fastest thing"], "Definite."),
        ("s15", "Landing", "That's the last one from this book, Diana. Sharp saw. Full jar. Look after the goose. I think you're going to be alright.", "That's the last one from this book, Diana. <break time=\"0.5s\"/> Sharp saw. <break time=\"0.3s\"/> Full jar. <break time=\"0.3s\"/> Look after the goose. <break time=\"0.5s\"/> I think you're going to be alright.", 0.0, "slow", "tender", ["going to be alright"], "Closes the teaching films. Callbacks to 19 and 20. Proud and warm."),
    ],
    "spec": [
        ("sc1", "s1", "NONE", "A plain simple handsaw resting against a plain tree trunk with a shallow cut in it, on cream paper."),
        ("sc2", "s2", "NONE", "A plain figure silhouette hunched over the saw mid-stroke, posture heavy and tired."),
        ("sc3", "s3", "NONE", "Two plain solid human figure silhouettes beside one plain upright tree trunk: one crouched low and sawing at the trunk with a single handsaw, and a second standing nearby with one hand raised slightly, plainly offering a suggestion."),
        ("sc4", "s4", "NONE", "The first figure silhouette still sawing, head down, not looking up at all."),
        ("sc5", "s5", "DIANA", "The girl looks puzzled and then amused, working out the joke."),
        ("sc6", "s6", "DIANA", "The girl gives a knowing wry smile, recognising something familiar."),
        ("sc7", "s7", "NONE", "A VERY CLOSE view of a short section of a saw blade seen at a slight angle and filling the whole frame, showing a row of sharp clean pointed triangular teeth with crisp points. No handle, no tree, no trunk, no hands and no other objects at all."),
        ("sc8", "s8", "NONE", "A VERY CLOSE view of a short section of a saw blade seen straight on from the side and filling the whole frame, showing a row of teeth that are completely worn down: each tooth is a low rounded bump, flat on top, with no sharp point at all. No handle, no tree, no trunk, no hands and no other objects at all."),
        ("sc9", "s9", "NONE", "The worn saw beside the plain tree trunk, the cut in the trunk barely deeper than before."),
        ("sc10", "s10", "DIANA", "The girl looks down in honest thought, remembering something discouraging."),
        ("sc11", "s11", "DIANA", "The girl looks up with visible relief, a weight lifting from her expression."),
        ("sc12", "s12", "NONE", "ONE single plain handsaw lying alone in the middle of a completely empty expanse of cream paper. There is nothing else at all in the picture: no tree, no trunk, no stone, no people and no objects of any kind."),
        ("sc13", "s13", "NONE", "A plain sharpening stone being drawn along the saw's teeth by an unseen hand, only the hand and forearm visible, no face and no body."),
        ("sc14", "s14", "NONE", "ONE single plain handsaw with clean sharp teeth, its blade cut deep into one plain upright tree trunk, the cut clearly more than halfway through. Exactly one saw in the picture."),
        ("sc15", "s15", "DIANA", "The girl stands calm and warm in soft evening light."),
        ("sc16", "s8", "NONE", "A VERY CLOSE view of a short section of a saw blade seen at a slight angle and filling the whole frame, its teeth worn down into low rounded flat-topped bumps with no points at all. Nothing else in the picture."),
        ("sc17", "s14", "NONE", "A VERY CLOSE view of a short section of a saw blade seen straight on from the side and filling the whole frame, its teeth freshly sharpened into crisp bright pointed triangles. Nothing else in the picture."),
        ("sc18", "s15", "NONE", "The sharpened saw resting beside the tree trunk in warm evening light, calm and ready."),
    ],
    "heroes": {"sc13", "sc14", "sc17", "sc18"}, "wides": {"sc12"},
}
FILM24["clauses"] = {
    "OPEN": (G.OPEN, {"sc5", "sc6", "sc10", "sc11", "sc15"}),
    "NOICON": (G.NOICON, {"sc5", "sc6", "sc10", "sc11", "sc15"}),
    "SHOES": (SHOES, {"sc5", "sc6", "sc10", "sc11", "sc15"}),
    "SAW": (("The saw is a plain simple handsaw with a plain wooden handle and a straight steel blade, drawn flat "
             "on cream paper. Draw ONLY the objects named in the description and nothing else: exactly ONE saw "
             "appears in the picture and there is never a second saw anywhere in the frame. Blunt teeth are "
             "drawn worn flat and rounded; sharp teeth are drawn as crisp pointed triangles. No forest scenery, "
             "no leaves, no grass, no sky, no numerals, no writing, no sparkles. Figures are plain solid human "
             "silhouettes with no facial features."),
            {"sc1", "sc2", "sc3", "sc4", "sc7", "sc8", "sc9", "sc12", "sc13", "sc14", "sc16", "sc17", "sc18"}),
}

if __name__ == "__main__":
    G_FILMS = {"m22": FILM22, "m23": FILM23, "m24": FILM24}
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
