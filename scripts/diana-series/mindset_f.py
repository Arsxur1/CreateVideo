"""7 Habits half, films 18-21 of 25: Habit 3 / P-PC balance / Emotional Bank Account / Think Win-Win."""
import sys
import filmgen as G
from mindset_e import cbase, SRC, SHOES

# ---------------------------------------------------------------- FILM 18
FILM18 = {**cbase(18, "diana-habits-doesnt-shout", "DianaDoesntShout", "The Thing That Doesn't Shout", "Habit 3",
                  "The 7 Habits, Habit 3 'Quadrant II' - direct excerpt read for this film"),
    "topic": "Urgent versus important, from Habit 3's Quadrant II material, told as Dad explaining that the things that matter most are the ones that never make a noise",
    "summary": ("Film 18. Habit 3, Put First Things First. Covey separates two different qualities an activity can "
                "have: urgent and important. Urgent things act on us and demand attention now; a ringing phone is "
                "urgent. Important things that are not urgent, which he calls Quadrant II, include building "
                "relationships, preparation, exercise and preventive maintenance, and he notes these are the "
                "things we know we need to do but seldom get around to precisely because they never shout. This "
                "film builds his Time Management Matrix as four plain boxes, each holding a picture rather than a "
                "written label, so an eight-year-old can read the whole grid at a glance."),
    "existing": [{"title": "Children's homework and chore checklists", "url": SRC, "source": "classroom material", "angle": "Get it all done",
                  "what_it_covers": "Treats every task as equal and rewards finishing, with no way to tell what actually mattered"},
                 {"title": "'Do the hardest thing first' study advice", "url": SRC, "source": "web", "angle": "Eat the frog",
                  "what_it_covers": "Orders tasks by difficulty rather than by whether they matter"},
                 {"title": "Reward-chart and sticker systems", "url": SRC, "source": "classroom material", "angle": "Tick the boxes",
                  "what_it_covers": "Rewards responding to whatever is in front of her, which trains urgency as the only signal"}],
    "saturated": ["Checklist and sticker systems that treat every task as equally worth doing"],
    "gaps": ["Giving a child a way to tell a thing that shouts from a thing that matters",
             "Naming why the important quiet things get skipped, which is that nothing forces them"],
    "data_points": [("The book separates two different qualities an activity can have: urgent and important, and notes these are not the same thing.", SRC, "The 7 Habits, Habit 3 ('Quadrant II')", "primary_source", "expected", "the whole distinction the film teaches"),
                     ("Its definition of urgent is that it requires immediate attention and acts on us; its example is a ringing phone, which most people cannot stand to leave unanswered.", SRC, "The 7 Habits, Habit 3", "primary_source", "surprising", "the bell device comes straight from this"),
                     ("The important-but-not-urgent group includes building relationships, preparation, exercise and preventive maintenance, which the book calls the heart of effective personal management.", SRC, "The 7 Habits, Habit 3", "primary_source", "expected", "what the quiet seedling stands for"),
                     ("The book's own explanation for why these get skipped is that they are things we know we need to do but seldom get around to doing, because they are not urgent.", SRC, "The 7 Habits, Habit 3", "primary_source", "surprising", "the film's core sentence: the quiet thing never asks")],
    "questions": ["Why do I always end up doing the noisy thing first?", "How do I know which thing actually matters?", "Why do the good things keep getting put off?"],
    "misconceptions": [("If something feels urgent it must be important", "Urgent and important are two different things; a ringing bell is urgent and often not important at all.", "Habit 3"),
                        ("The important things will remind you", "They never do. That is exactly why they get skipped.", "Habit 3")],
    "pain_points": ["Answering whatever shouts loudest and running out of day", "Never getting to the thing she actually cares about"],
    "angles": [("The Bell and the Seedling", "narrative", "One rattles until you answer it. The other never says a word, and matters more.", "Turns an abstract distinction into two objects she can hear the difference between.", ["Habit 3"]),
               ("Loud Isn't The Same As Important", "contrarian", "Urgency is a volume setting, not a measure of worth.", "Breaks the reflex that noise equals priority.", ["Habit 3"]),
               ("The Quiet Thing Never Asks", "evergreen", "Nothing will ever force you to do the thing that matters most.", "Names why good intentions keep losing, without blame.", ["Habit 3"])],
    "kahneman": "Urgent things act on us and demand attention now; the important things that are not urgent never shout, which is exactly why they get skipped.",
    "excluded": ["The adult workplace and management examples. The Time Management Matrix itself is kept, but rebuilt as four plain boxes holding pictures instead of the book's written quadrant labels."],
    "concepts": [
        {"id": "c1", "title": "The Thing That Doesn't Shout", "hook": "Diana, the things that matter most almost never make a sound.", "narrative_structure": "story",
         "visual_approach": "A rattling handbell and a silent seedling, which then take their places in a plain two-by-two grid of four boxes, each box holding one picture instead of a written label.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 145,
         "key_points": ["Some things shout at you and demand answering", "Some things matter and say nothing at all", "Two separate questions make four boxes", "The seedling box loses because nothing in it can ask", "You have to go to that box on purpose"],
         "core_message": "The bell will always get answered. The seedling only grows if you decide to go to it.", "cta": "Give the quiet thing a bit of time today, before the bells start.", "tone": "Calm, warm, quietly clear.",
         "why_this_works": "It explains her own daily experience of good intentions losing to noise, without making it a failing.", "grounded_in": ["Habit 3"]},
        {"id": "c2", "title": "Loud Isn't Important", "hook": "Urgency is a volume setting, not a measure of worth.", "narrative_structure": "myth_busting",
         "visual_approach": "The bell rattling hard and bright while nothing of consequence happens around it.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 70,
         "key_points": ["A thing can be extremely loud and not matter at all", "Answering by volume means someone else picks your day"],
         "core_message": "Noise is not a reason.", "cta": "Ask whether it's loud or whether it matters.", "tone": "Clear and dry.",
         "why_this_works": "Breaks the noise-equals-priority reflex, folded into c1 as its hinge.", "grounded_in": ["Habit 3"]},
        {"id": "c3", "title": "The Quiet Thing Never Asks", "hook": "Nothing will ever make you do the thing that matters most.", "narrative_structure": "problem_solution",
         "visual_approach": "The seedling alone in a wide quiet space, patient and unnoticed.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 70,
         "key_points": ["The quiet thing has no way of demanding your attention", "So it only ever happens on purpose"],
         "core_message": "It won't ask. You have to go to it.", "cta": "Go to it before anything rings.", "tone": "Gentle and honest.",
         "why_this_works": "Explains the mechanism of the failure kindly, folded into c1 as its close.", "grounded_in": ["Habit 3"]}],
    "rationale": "c1 carries the bell and the seedling from the contrast to the choice; c2 and c3 are its hinge and its close, all three using the same two objects.",
    "device_short": "four plain boxes, each holding one picture instead of a word",
    "art_direction": ("New device: a rattling handbell and a silent seedling, which then take their places in a "
                      "plain two-by-two grid of four boxes, each box holding one simple object instead of a "
                      "written label."),
    "device_lock": ("One small plain simple handbell with a plain handle, and one small simple seedling with two or "
                    "three plain leaves in a plain undecorated pot, drawn flat on cream paper. The grid is exactly "
                    "four plain thin-outlined squares in a two-by-two arrangement, each holding ONE simple object "
                    "and nothing else. Motion lines are a few short plain curved strokes only. No faces on any "
                    "object, no numerals, no writing, no labels, no titles, no headings, no musical notes, no "
                    "sound symbols, no sparkles."),
    "tradeoffs": [{"tradeoff": "Writing the book's four quadrant labels versus putting a picture in each box", "recommendation": "A picture in each box",
                   "quality_impact": "The book labels its matrix in words, which no illustration in this series may contain and which an eight-year-old would skip anyway; one object per box lets her read the whole grid at a glance and keeps Covey's actual structure."}],
    "energy_curve": "Calm at the opening. A little comic as the bell rattles. Quiet and tender at the seedling. Honest at why it gets skipped. Warm at the close.",
    "sample_section": "s12", "human_note": "Section s12 removes the shame and then lands the instruction. Gentle, never scolding.",
    "pause_beats": [{"section": "s5", "purpose": "She notices the seedling has said nothing this whole time"}, {"section": "s11", "purpose": "She works out which box actually gets her day"}, {"section": "s13", "purpose": "She picks when to go to the seedling box"}],
    "grounded_in": {"s1_to_s5": "Habit 3, urgent defined and the quiet thing introduced", "s6_to_s10": "Habit 3, the matrix built as four boxes", "s11_to_s12": "Habit 3, why Quadrant II loses", "s13_to_s15": "Habit 3 corrective, going to it on purpose"},
    "sections": [
        ("s1", "Setup", "Diana, the things that matter most almost never make a sound.", "Diana, the things that matter most almost never make a sound.", 1.4, "measured", "warm", ["never make a sound"], "Calm, quietly certain."),
        ("s2", "The bell", "Picture a little bell. And it rattles. It jumps about. It will not be ignored.", "Picture a little bell. <break time=\"0.4s\"/> And it rattles. <break time=\"0.3s\"/> It jumps about. <break time=\"0.4s\"/> It will not be ignored.", 1.4, "measured", "curious", ["rattles"], "A bit comic."),
        ("s3", "You answer it", "And what do you do? You answer it. Everybody does. You can't help it.", "And what do you do? <break time=\"0.4s\"/> You answer it. <break time=\"0.3s\"/> Everybody does. <break time=\"0.4s\"/> You can't help it.", 1.4, "measured", "wry", ["you answer it"], "Sympathetic, not mocking."),
        ("s4", "The seedling", "Now, over here, there's a tiny seedling in a pot. And it hasn't said a word this whole time.", "Now, over here, there's a tiny seedling in a pot. <break time=\"0.5s\"/> And it hasn't said a word this whole time.", 1.4, "measured", "gentle", ["not a word"], "Soften the voice here."),
        ("s5", "It never will", "It isn't going to, either. It has no way of asking. It just quietly needs a bit of water.", "It isn't going to, either. <break time=\"0.4s\"/> It has no way of asking. <break time=\"0.4s\"/> It just quietly needs a bit of water. <break time=\"2.5s\"/>", 2.5, "slow", "tender", ["no way of asking"], "Pause beat one. Let the seedling sit there."),
        ("s6", "Two questions", "So there are two separate questions you can ask about anything. Is it shouting? And does it matter? They're not the same question.", "So there are two separate questions you can ask about anything. <break time=\"0.4s\"/> Is it shouting? <break time=\"0.4s\"/> And does it matter? <break time=\"0.4s\"/> They're not the same question.", 1.4, "measured", "steady", ["not the same"], "The core distinction. Clear."),
        ("s7", "Four boxes", "And if you put those two questions together, you get four boxes. Watch, this is the useful bit.", "And if you put those two questions together, you get four boxes. <break time=\"0.4s\"/> Watch, this is the useful bit.", 1.4, "measured", "curious", ["four boxes"], "Bring her in. This is a reveal."),
        ("s8", "Box one and two", "Top left: shouting and it matters. A cut knee. Spilled milk. You deal with those, no argument. Top right: shouting and it doesn't matter at all. That's the bell. That box eats most people's whole day.", "Top left: shouting and it matters. <break time=\"0.3s\"/> A cut knee. <break time=\"0.3s\"/> Spilled milk. <break time=\"0.4s\"/> You deal with those, no argument. <break time=\"0.5s\"/> Top right: shouting and it doesn't matter at all. <break time=\"0.4s\"/> That's the bell. <break time=\"0.4s\"/> That box eats most people's whole day.", 1.4, "measured", "steady", ["eats most people's whole day"], "Brisk through the first two boxes. Land the warning on the second."),
        ("s9", "Box three", "Bottom left. Quiet, and it matters. Practising. Being kind to somebody. Getting ready properly. Looking after yourself. That's your seedling box, and it's the best one there is.", "Bottom left. <break time=\"0.4s\"/> Quiet, and it matters. <break time=\"0.4s\"/> Practising. <break time=\"0.3s\"/> Being kind to somebody. <break time=\"0.3s\"/> Getting ready properly. <break time=\"0.3s\"/> Looking after yourself. <break time=\"0.5s\"/> That's your seedling box, and it's the best one there is.", 1.4, "slow", "warm", ["the best one there is"], "Warm and unhurried. This is the box the film is for."),
        ("s10", "Box four", "And bottom right: quiet, and it doesn't really matter. Mucking about. That one's fine, by the way. Just not all afternoon.", "And bottom right: quiet, and it doesn't really matter. <break time=\"0.4s\"/> Mucking about. <break time=\"0.4s\"/> That one's fine, by the way. <break time=\"0.3s\"/> Just not all afternoon.", 1.4, "measured", "wry", ["that one's fine"], "Light, permission-giving, not a telling-off."),
        ("s11", "Which box wins", "Now look at the four together. Which box do you think gets most of your day? Have a proper think.", "Now look at the four together. <break time=\"0.4s\"/> Which box do you think gets most of your day? <break time=\"0.4s\"/> Have a proper think. <break time=\"2.5s\"/>", 2.5, "slow", "curious", ["most of your day"], "Genuine question. She'll know the answer."),
        ("s12", "Why box three loses", "It's the shouting ones, isn't it. And you're not lazy for that, Diana. Nothing in the seedling box can ask. So there's only one way it ever happens. You go to it on purpose.", "It's the shouting ones, isn't it. <break time=\"0.4s\"/> And you're not lazy for that, Diana. <break time=\"0.5s\"/> Nothing in the seedling box can ask. <break time=\"0.4s\"/> So there's only one way it ever happens. <break time=\"0.4s\"/> You go to it on purpose.", 1.4, "measured", "tender", ["on purpose"], "Remove shame, then land the instruction."),
        ("s13", "The move", "So pick a moment. Before the bells start. Give your quiet thing a little bit of the day, first.", "So pick a moment. <break time=\"0.4s\"/> Before the bells start. <break time=\"0.4s\"/> Give your quiet thing a little bit of the day, first. <break time=\"2.5s\"/>", 2.5, "measured", "encouraging", ["a little bit of the day"], "Pause beat three. The actual tool."),
        ("s14", "It grows", "And the lovely part is, the quiet things are the ones that grow. Slowly. While nobody's making a fuss about them.", "And the lovely part is, the quiet things are the ones that grow. <break time=\"0.4s\"/> Slowly. <break time=\"0.4s\"/> While nobody's making a fuss about them.", 1.4, "measured", "warm", ["the ones that grow"], "Hopeful."),
        ("s15", "Landing", "You were one of those quiet things once, Diana. Nobody made a fuss. You just grew. And look at you now.", "You were one of those quiet things once, Diana. <break time=\"0.4s\"/> Nobody made a fuss. <break time=\"0.3s\"/> You just grew. <break time=\"0.5s\"/> And look at you now.", 0.0, "slow", "tender", ["look at you now"], "Personal, warm, unhurried close."),
    ],
    "spec": [
        ("sc1", "s1", "DIANA", "The girl stands calm and attentive, quietly listening."),
        ("sc2", "s2", "NONE", "One small plain handbell on cream paper with a few short curved motion lines beside it, plainly rattling."),
        ("sc3", "s3", "DIANA", "The girl turns quickly toward something, alert and slightly startled, reacting."),
        ("sc4", "s4", "NONE", "One small simple seedling with two or three plain leaves in a plain undecorated pot, perfectly still."),
        ("sc5", "s5", "NONE", "The small seedling alone in a wide empty expanse of plain cream paper, quiet and patient."),
        ("sc6", "s6", "NONE", "The rattling handbell on the left and the still seedling on the right, side by side on the page."),
        ("sc7", "s7", "NONE", "An empty two-by-two grid of four plain thin-outlined squares on cream paper, all four boxes completely empty."),
        ("sc8", "s8", "NONE", "The two-by-two grid with only the top two boxes filled: the top-left box holds a tipped-over cup with a small spill, the top-right box holds the handbell with motion lines. The bottom two boxes are empty."),
        ("sc9", "s9", "NONE", "The two-by-two grid with the bottom-left box now holding the small seedling in its pot, glowing warmly, while the other three boxes stay plain and unlit."),
        ("sc10", "s10", "NONE", "The complete two-by-two grid with all four boxes filled: tipped cup, handbell, glowing seedling, and a loose tangle of string in the bottom-right box."),
        ("sc11", "s11", "DIANA", "The girl looks thoughtful, hand near her chin, considering something honestly."),
        ("sc12", "s12", "DIANA", "The girl looks reassured, tension easing, a small relieved smile."),
        ("sc13", "s13", "DIANA", "The girl carefully pours a little water from a small plain watering can, gentle and focused."),
        ("sc14", "s14", "NONE", "The same seedling, now noticeably taller and stronger, still perfectly quiet."),
        ("sc15", "s15", "DIANA", "The girl stands calm and warm in soft evening light."),
        ("sc16", "s9", "NONE", "A close view of just the bottom-left box of the grid, holding the seedling and glowing warmly."),
        ("sc17", "s10", "NONE", "The complete four-box grid seen whole and warmly lit, the bottom-left seedling box clearly the brightest of the four."),
        ("sc18", "s15", "NONE", "The grown plant and the quiet handbell resting side by side in warm evening light, the bell still and silent."),
    ],
    "heroes": {"sc9", "sc16", "sc17", "sc18"}, "wides": {"sc5", "sc10", "sc17"},
}
FILM18["clauses"] = {
    "OPEN": (G.OPEN, {"sc1", "sc3", "sc11", "sc12", "sc13", "sc15"}),
    "NOICON": (G.NOICON, {"sc1", "sc3", "sc11", "sc12", "sc13", "sc15"}),
    "SHOES": (SHOES, {"sc1", "sc3", "sc11", "sc12", "sc13", "sc15"}),
    "BELL": (("One small plain simple handbell with a plain handle, and one small simple seedling with two or three "
              "plain leaves in a plain undecorated pot, drawn flat on cream paper. Motion lines are a few short "
              "plain curved strokes only. No faces on any object, no numerals, no writing, no musical notes, no "
              "sound symbols, no sparkles, no background scenery."),
             {"sc2", "sc4", "sc5", "sc6", "sc14", "sc18"}),
    "GRID": (("The grid is EXACTLY four plain squares of equal size in a two-by-two arrangement, drawn as simple "
              "thin hand-drawn outlines on cream paper. Each filled box holds exactly ONE simple object, centred, "
              "and nothing else. Objects are drawn plainly and flatly: a tipped-over cup with a small spill, a "
              "plain handbell with a few short motion lines, a small seedling in a plain pot, and a loose tangle "
              "of string. Absolutely NO words, NO letters, NO labels, NO titles, NO headings, NO numbers and NO "
              "annotations inside, above, below or beside any box. No arrows. No background scenery."),
             {"sc7", "sc8", "sc9", "sc10", "sc16", "sc17"}),
}

# ---------------------------------------------------------------- FILM 19
FILM19 = {**cbase(19, "diana-habits-look-after-the-goose", "DianaLookAfterTheGoose", "Look After the Goose", "P/PC Balance",
                  "The 7 Habits, 'The P/PC Balance' - direct excerpt read for this film"),
    "topic": "The balance between what you produce and the thing that produces it, from the book's P/PC Balance section and Aesop's goose, told as Dad explaining why you look after the maker and not just the made",
    "summary": ("Film 19. The P/PC Balance, which Covey introduces through Aesop's fable of the goose and the "
                "golden egg. A farmer finds his goose laying a golden egg each day and grows rich, but greed and "
                "impatience make him wreck the goose to get them all at once, and afterwards there are none. The "
                "book's conclusion is that true effectiveness is a function of two things: what is produced, the "
                "golden eggs, and the capacity to produce, the goose."),
    "existing": [{"title": "Children's retellings of Aesop's fable", "url": SRC, "source": "web", "angle": "Don't be greedy",
                  "what_it_covers": "Reads the fable as a warning about greed only, missing the balance it actually illustrates"},
                 {"title": "'Work hard now, rest later' encouragement", "url": SRC, "source": "web", "angle": "Push through",
                  "what_it_covers": "Treats the person doing the work as an unlimited resource"},
                 {"title": "Productivity and streak-tracking apps for kids", "url": SRC, "source": "web", "angle": "Never break the chain",
                  "what_it_covers": "Counts output daily and has no measure at all for the condition of whoever is producing it"}],
    "saturated": ["Retellings of the fable that stop at 'don't be greedy'"],
    "gaps": ["Naming the second thing the fable is actually about: looking after the capacity to produce",
             "Applying it to a child herself as the goose, not just to things she owns"],
    "data_points": [("Covey introduces the P/PC Balance through Aesop's fable of the goose and the golden egg, in which a farmer grows rich on one golden egg a day.", SRC, "The 7 Habits, 'The P/PC Balance'", "primary_source", "expected", "the device"),
                     ("In the fable, impatience makes the farmer destroy the goose to get all the eggs at once, and afterwards there are no eggs and no way to get any more.", SRC, "The 7 Habits, 'The P/PC Balance'", "primary_source", "expected", "the cost, told without being depicted"),
                     ("The book's conclusion is that true effectiveness is a function of two things: what is produced, the golden eggs, and the producing asset or capacity to produce, the goose.", SRC, "The 7 Habits, 'The P/PC Balance'", "primary_source", "surprising", "the actual principle, which the usual retelling misses"),
                     ("Covey calls this a natural law and notes that many people break themselves against it, which is what makes it worth teaching early.", SRC, "The 7 Habits, 'The P/PC Balance'", "primary_source", "expected", "why the film exists at all")],
    "questions": ["Why do I feel worn out when I've done everything right?", "Is it wrong to rest when there's more to do?", "What's the difference between what I make and what makes it?"],
    "misconceptions": [("The fable is just about being greedy", "It's about two things mattering: what's produced, and the thing that produces it.", "P/PC Balance"),
                        ("Resting is time taken away from doing well", "The thing that does the work has to be looked after or there is no more work.", "P/PC Balance")],
    "pain_points": ["Pushing until she's worn out and then producing nothing", "Feeling guilty about resting or stopping"],
    "angles": [("Two Things, Not One", "narrative", "There's what you make, and there's the thing that makes it. Both count.", "Reframes a familiar fable into a principle she can apply to herself.", ["P/PC Balance"]),
               ("You Are the Goose", "contrarian", "In your own life you're not the farmer collecting. You're the goose.", "Turns the fable inward, which is the move that makes it useful.", ["P/PC Balance"]),
               ("Impatience Is The Real Danger", "evergreen", "It wasn't greed that ruined it so much as not being able to wait.", "Names the actual mechanism a child will recognise in herself.", ["P/PC Balance"])],
    "kahneman": "True effectiveness is a function of two things: what is produced, the golden eggs, and the capacity to produce, the goose.",
    "excluded": ["The fable's killing of the goose is referred to only obliquely as the farmer ruining it, and is never depicted in any illustration. The book's business and equipment-maintenance examples are also left out."],
    "concepts": [
        {"id": "c1", "title": "Look After the Goose", "hook": "Diana, there's an old story about a farmer, a goose, and a golden egg.", "narrative_structure": "story",
         "visual_approach": "A plain calm goose beside a single golden egg, then the goose alone and well cared for, warmly lit.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 145,
         "key_points": ["One golden egg a day, and the farmer grew rich", "He couldn't wait, so he ruined the goose", "After that there were no eggs at all", "Two things matter: the eggs and the goose", "In your own life you are the goose"],
         "core_message": "Look after the thing that makes the good things. In your life, that's you.", "cta": "Do one thing today that looks after the goose.", "tone": "Warm, story-telling, gentle.",
         "why_this_works": "It gives her permission to rest and look after herself as a matter of good sense, not indulgence.", "grounded_in": ["P/PC Balance"]},
        {"id": "c2", "title": "You Are the Goose", "hook": "In your own life, you're not the farmer. You're the goose.", "narrative_structure": "analogy",
         "visual_approach": "The goose resting comfortably, calm and unhurried, well looked after.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 75,
         "key_points": ["Everything she makes comes out of her", "So looking after herself is not separate from doing well"],
         "core_message": "You're the thing that makes the good things.", "cta": "Treat yourself as the goose, not the eggs.", "tone": "Tender.",
         "why_this_works": "The inward turn that makes the fable usable, folded into c1 as its hinge.", "grounded_in": ["P/PC Balance"]},
        {"id": "c3", "title": "Impatience Is The Danger", "hook": "It wasn't really greed. It was not being able to wait.", "narrative_structure": "myth_busting",
         "visual_approach": "A single golden egg beside an empty nest, quiet and plain.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 70,
         "key_points": ["Wanting it all at once is the trap, not wanting it", "Impatience is something a child can actually notice in herself"],
         "core_message": "Wanting everything now is what breaks the thing that gives it.", "cta": "Notice impatience before it costs something.", "tone": "Honest.",
         "why_this_works": "Names a mechanism she can catch, folded into c1 as its warning.", "grounded_in": ["P/PC Balance"]}],
    "rationale": "c1 carries the fable and its lesson; c2 turns it inward and c3 names the mechanism, all three following the same goose.",
    "device_short": "a plain goose and a single golden egg",
    "art_direction": "New device: one plain simple goose and one plain golden egg on cream paper, the goose always shown calm, whole and well.",
    "device_lock": ("One plain simple white goose with a soft orange beak, drawn flat on cream paper, always whole, "
                    "calm and unharmed, never injured, never distressed, never shown being hurt. One plain smooth "
                    "golden egg. A plain simple nest of straw. No farm scenery, no buildings, no numerals, no "
                    "writing."),
    "tradeoffs": [{"tradeoff": "Depicting the fable's ending versus referring to it in words only", "recommendation": "Words only",
                   "quality_impact": "The goose dies in Aesop's original; for an eight-year-old at bedtime the loss is carried by one gentle line of narration and the goose is only ever drawn alive and well."}],
    "energy_curve": "Warm story-telling at the opening. A quiet drop at the loss. Tender at the inward turn. Encouraging and settled at the close.",
    "sample_section": "s10", "human_note": "Section s10 is the inward turn, telling her she is the goose. This is the emotional centre. Slow and warm.",
    "pause_beats": [{"section": "s6", "purpose": "She sits with the empty nest"}, {"section": "s11", "purpose": "She takes in that she is the goose"}, {"section": "s13", "purpose": "She picks one thing that looks after her"}],
    "grounded_in": {"s1_to_s5": "P/PC Balance, the fable told", "s6_to_s9": "P/PC Balance, the two things that matter", "s10_to_s12": "P/PC Balance turned inward", "s13_to_s15": "P/PC corrective, looking after the goose"},
    "sections": [
        ("s1", "Setup", "Diana, there's an old story about a farmer, a goose, and a golden egg.", "Diana, there's an old story about a farmer, a goose, and a golden egg.", 1.4, "measured", "warm", ["golden egg"], "Storyteller's warmth."),
        ("s2", "The discovery", "One morning he finds an egg in the nest, and it's solid gold. He can hardly believe it.", "One morning he finds an egg in the nest, <break time=\"0.4s\"/> and it's solid gold. <break time=\"0.4s\"/> He can hardly believe it.", 1.4, "measured", "curious", ["solid gold"], "Delight."),
        ("s3", "Every day", "And then it happens again. And again. One golden egg, every single morning.", "And then it happens again. <break time=\"0.3s\"/> And again. <break time=\"0.4s\"/> One golden egg, every single morning.", 1.4, "measured", "warm", ["every morning"], "Steady, pleasant rhythm."),
        ("s4", "Getting rich", "He gets rich. Properly rich. And then something starts to go wrong in him.", "He gets rich. <break time=\"0.3s\"/> Properly rich. <break time=\"0.4s\"/> And then something starts to go wrong in him.", 1.4, "measured", "steady", ["go wrong"], "Turn the tone."),
        ("s5", "Impatience", "One egg a day isn't enough any more. He can't wait. He wants all of them, now.", "One egg a day isn't enough any more. <break time=\"0.4s\"/> He can't wait. <break time=\"0.4s\"/> He wants all of them, now.", 1.4, "measured", "steady", ["can't wait"], "This is the real fault. Name it."),
        ("s6", "The loss", "So he ruins the goose trying to get them all at once. And after that, there are no eggs. Not one. Not ever again.", "So he ruins the goose trying to get them all at once. <break time=\"0.5s\"/> And after that, there are no eggs. <break time=\"0.4s\"/> Not one. <break time=\"0.3s\"/> Not ever again. <break time=\"2.5s\"/>", 2.5, "slow", "gentle", ["not ever again"], "Pause beat one. Quiet and sad, never graphic."),
        ("s7", "The usual lesson", "Now, most people tell that story and say the lesson is don't be greedy.", "Now, most people tell that story and say the lesson is don't be greedy.", 1.4, "measured", "steady", ["don't be greedy"], "Set up the reframe."),
        ("s8", "The real one", "But there's a better one underneath it. There were always two things that mattered. The eggs. And the goose.", "But there's a better one underneath it. <break time=\"0.5s\"/> There were always two things that mattered. <break time=\"0.4s\"/> The eggs. <break time=\"0.3s\"/> And the goose.", 1.4, "measured", "curious", ["two things"], "The actual principle."),
        ("s9", "He only counted one", "He counted the eggs every day. He never once thought about the goose. And you can't have one without the other.", "He counted the eggs every day. <break time=\"0.4s\"/> He never once thought about the goose. <break time=\"0.5s\"/> And you can't have one without the other.", 1.4, "measured", "steady", ["never once"], "Land it."),
        ("s10", "The turn", "And here's what I really want to say, Diana. In your own life, you're not the farmer. You're the goose.", "And here's what I really want to say, Diana. <break time=\"0.5s\"/> In your own life, you're not the farmer. <break time=\"0.5s\"/> You're the goose.", 1.4, "slow", "tender", ["you're the goose"], "The emotional centre. Slow and warm."),
        ("s11", "What that means", "Everything good you'll ever make comes out of you. Your drawings, your kindness, your work. All of it comes out of one girl.", "Everything good you'll ever make comes out of you. <break time=\"0.4s\"/> Your drawings, your kindness, your work. <break time=\"0.4s\"/> All of it comes out of one girl. <break time=\"2.5s\"/>", 2.5, "slow", "tender", ["one girl"], "Pause beat two. Let it land."),
        ("s12", "So resting isn't lazy", "Which means sleeping properly, and eating, and stopping when you're worn out, isn't you being lazy. It's you looking after the goose.", "Which means sleeping properly, and eating, and stopping when you're worn out, <break time=\"0.4s\"/> isn't you being lazy. <break time=\"0.5s\"/> It's you looking after the goose.", 1.4, "measured", "warm", ["looking after the goose"], "Genuine permission."),
        ("s13", "The move", "So do one thing today that looks after the goose. Just one. It counts as work. It really does.", "So do one thing today that looks after the goose. <break time=\"0.4s\"/> Just one. <break time=\"0.4s\"/> It counts as work. <break time=\"0.3s\"/> It really does. <break time=\"2.5s\"/>", 2.5, "measured", "encouraging", ["counts as work"], "Pause beat three. The tool, with permission attached."),
        ("s14", "The patience bit", "And when you want everything at once, and you will, remember it wasn't greed that lost the eggs. It was not being able to wait.", "And when you want everything at once, and you will, <break time=\"0.4s\"/> remember it wasn't greed that lost the eggs. <break time=\"0.4s\"/> It was not being able to wait.", 1.4, "measured", "steady", ["not being able to wait"], "Useful warning, kindly given."),
        ("s15", "Landing", "I'm not in a hurry for your golden eggs, Diana. I've got the goose. That was always the good bit.", "I'm not in a hurry for your golden eggs, Diana. <break time=\"0.5s\"/> I've got the goose. <break time=\"0.4s\"/> That was always the good bit.", 0.0, "slow", "tender", ["the good bit"], "Personal, warm, unhurried close."),
    ],
    "spec": [
        ("sc1", "s1", "DIANA", "The girl sits comfortably listening to a story, warm and settled."),
        ("sc2", "s2", "NONE", "One plain golden egg resting in a simple straw nest on cream paper."),
        ("sc3", "s3", "NONE", "A plain white goose with a soft orange beak standing calmly beside the simple nest."),
        ("sc4", "s4", "NONE", "Several plain golden eggs arranged in a small neat row on the cream page."),
        ("sc5", "s5", "NONE", "A single hand reaching greedily toward the nest, only the hand and forearm visible, no face and no body."),
        ("sc6", "s6", "NONE", "An empty straw nest alone on the cream page, no eggs and no goose, plain and quiet."),
        ("sc7", "s7", "DIANA", "The girl listens thoughtfully, taking in the end of a story."),
        ("sc8", "s8", "NONE", "The plain white goose on the left and a single golden egg on the right, side by side, equally lit."),
        ("sc9", "s9", "NONE", "A neat row of golden eggs in the foreground with the plain white goose small and unattended behind them."),
        ("sc10", "s10", "DIANA", "The girl looks up, surprised and moved, taking in something about herself."),
        ("sc11", "s11", "DIANA", "The girl stands quietly with a small warm smile, calm and valued."),
        ("sc12", "s12", "NONE", "The plain white goose resting comfortably and settled in the straw nest, calm and well."),
        ("sc13", "s13", "DIANA", "The girl rests peacefully with her eyes closed, calm and unhurried."),
        ("sc14", "s14", "DIANA", "The girl looks patient and steady, willing to wait for something."),
        ("sc15", "s15", "DIANA", "The girl stands calm and warm in soft evening light."),
        ("sc16", "s8", "NONE", "A close view of the plain white goose, calm and healthy, warmly lit."),
        ("sc17", "s12", "NONE", "The goose settled comfortably in warm light with one golden egg beside it, both peaceful."),
        ("sc18", "s15", "NONE", "The plain white goose resting in its straw nest in warm evening light, calm, whole and well."),
    ],
    "heroes": {"sc8", "sc16", "sc17", "sc18"}, "wides": set(),
}
FILM19["clauses"] = {
    "OPEN": (G.OPEN, {"sc1", "sc7", "sc10", "sc11", "sc13", "sc14", "sc15"}),
    "NOICON": (G.NOICON, {"sc1", "sc7", "sc10", "sc11", "sc13", "sc14", "sc15"}),
    "SHOES": (SHOES, {"sc1", "sc7", "sc10", "sc11", "sc13", "sc14", "sc15"}),
    "GOOSE": (("One plain simple white goose with a soft orange beak, drawn flat on cream paper, always whole, calm "
               "and unharmed. The goose is NEVER injured, NEVER distressed, NEVER shown being hurt and NEVER shown "
               "dead. Golden eggs are plain smooth ovals. The nest is plain simple straw. No farm scenery, no "
               "buildings, no people, no numerals, no writing."),
              {"sc2", "sc3", "sc4", "sc5", "sc6", "sc8", "sc9", "sc12", "sc16", "sc17", "sc18"}),
}

# ---------------------------------------------------------------- FILM 20
FILM20 = {**cbase(20, "diana-habits-the-jar-between-you", "DianaJarBetweenYou", "The Jar Between You", "Emotional Bank Account",
                  "The 7 Habits, 'The Emotional Bank Account' - direct excerpt read for this film"),
    "topic": "The Emotional Bank Account, from the book's Paradigms of Interdependence section, told as Dad describing a jar of trust that sits between any two people",
    "summary": ("Film 20. The Emotional Bank Account, Covey's metaphor for the amount of trust built up in a "
                "relationship, which he describes as the feeling of safeness you have with another person. Small "
                "deposits of courtesy, kindness, honesty and keeping commitments build a reserve; when the reserve "
                "is high, mistakes are absorbed and meaning gets through even when the words come out wrong. When "
                "it is overdrawn, every single word has to be measured."),
    "existing": [{"title": "'Say sorry and make up' conflict advice for children", "url": SRC, "source": "classroom material", "angle": "Apologise",
                  "what_it_covers": "Handles the moment of rupture but says nothing about what makes a friendship able to survive one"},
                 {"title": "Friendship-skills posters", "url": SRC, "source": "classroom material", "angle": "Share and be kind",
                  "what_it_covers": "Lists good behaviours without explaining what they accumulate into over time"},
                 {"title": "'Be yourself and people will like you' encouragement", "url": SRC, "source": "web", "angle": "Just be authentic",
                  "what_it_covers": "Offers reassurance rather than any account of how trust is actually built or lost"}],
    "saturated": ["Apologise-and-make-up advice that ignores what lets a friendship survive a mistake"],
    "gaps": ["Showing a child that trust is a reserve built from small ordinary acts, not a single grand one",
             "Explaining why the same clumsy sentence lands fine with one person and badly with another"],
    "data_points": [("The book describes the Emotional Bank Account as a metaphor for the amount of trust built up in a relationship, and calls it the feeling of safeness you have with another human being.", SRC, "The 7 Habits, 'The Emotional Bank Account'", "primary_source", "expected", "the jar device"),
                     ("Deposits are made through courtesy, kindness, honesty and keeping commitments, which build a reserve that can be drawn on later.", SRC, "The 7 Habits, 'The Emotional Bank Account'", "primary_source", "expected", "the small ordinary acts that fill the jar"),
                     ("When the reserve is high, the book says you can even make mistakes and the trust will compensate for them, and your meaning gets through even when your words are unclear.", SRC, "The 7 Habits, 'The Emotional Bank Account'", "primary_source", "surprising", "the reassuring payoff for a child who fears saying the wrong thing"),
                     ("When the account is overdrawn the book describes having to measure every word, with no flexibility at all left in the relationship.", SRC, "The 7 Habits, 'The Emotional Bank Account'", "primary_source", "surprising", "why an empty jar feels so tense, explained")],
    "questions": ["Why did my friend get upset at something I didn't mean badly?", "How do I fix a friendship that feels tense?", "What actually makes someone trust you?"],
    "misconceptions": [("Trust is built by one big gesture", "It's a reserve built from many small ordinary deposits over time.", "Emotional Bank Account"),
                        ("If someone takes something the wrong way they're being unfair", "With a full jar the same words land fine; the jar decides how much room your mistakes get.", "Emotional Bank Account")],
    "pain_points": ["Being misunderstood by someone she hasn't built much trust with", "Not knowing how to repair a friendship that feels tight and careful"],
    "angles": [("The Jar Between You", "narrative", "Between any two people there's a jar, and every small kindness is a pebble in it.", "Makes an invisible thing countable and repairable.", ["Emotional Bank Account"]),
               ("A Full Jar Absorbs Mistakes", "evergreen", "When the jar is full you can say it clumsily and still be understood.", "Directly reassures a child who is frightened of getting words wrong.", ["Emotional Bank Account"]),
               ("Nobody Fills It In One Go", "contrarian", "There's no grand gesture that fills it. Only small ordinary pebbles.", "Removes the pressure of the big apology and replaces it with something doable.", ["Emotional Bank Account"])],
    "kahneman": "The Emotional Bank Account is the amount of trust built up in a relationship, and it is the feeling of safeness you have with another person.",
    "excluded": ["The adult workplace, marriage and organisational examples, and the six deposits list, which is adult in framing and too long for one film."],
    "concepts": [
        {"id": "c1", "title": "The Jar Between You", "hook": "Diana, between you and every person you know, there's a jar.", "narrative_structure": "story",
         "visual_approach": "A plain glass jar sitting between two plain figures, filling with small warm pebbles as deposits are made and emptying as they are withdrawn.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 150,
         "key_points": ["Every kindness is a pebble in the jar", "The jar is how safe someone feels with you", "A full jar absorbs your mistakes", "An empty one makes every word risky", "Only small ordinary pebbles fill it"],
         "core_message": "Trust is a jar you fill one small pebble at a time, and a full one gives your mistakes somewhere to land.", "cta": "Put one pebble in someone's jar today.", "tone": "Warm, practical, reassuring.",
         "why_this_works": "It makes an invisible thing visible, countable, and above all repairable.", "grounded_in": ["Emotional Bank Account"]},
        {"id": "c2", "title": "A Full Jar Absorbs Mistakes", "hook": "With a full jar you can say it badly and still be understood.", "narrative_structure": "problem_solution",
         "visual_approach": "A full jar with a small chip taken out of the top layer, still obviously full.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 75,
         "key_points": ["A reserve gives your clumsiness somewhere to land", "It's why the same sentence lands differently with different people"],
         "core_message": "The jar decides how much room your mistakes get.", "cta": "Fill the jar before you need it.", "tone": "Reassuring.",
         "why_this_works": "Speaks directly to the fear of saying the wrong thing, folded into c1 as its payoff.", "grounded_in": ["Emotional Bank Account"]},
        {"id": "c3", "title": "Nobody Fills It In One Go", "hook": "There's no single grand thing that fills it.", "narrative_structure": "myth_busting",
         "visual_approach": "One small pebble held between finger and thumb above a part-filled jar.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 70,
         "key_points": ["Grand gestures don't fill a jar", "Small ordinary acts, repeated, do"],
         "core_message": "One pebble at a time is the only way it has ever worked.", "cta": "Start with one small pebble.", "tone": "Practical.",
         "why_this_works": "Removes the pressure of a big fix and replaces it with something she can do today, folded into c1 as its close.", "grounded_in": ["Emotional Bank Account"]}],
    "rationale": "c1 carries the jar from filling to emptying to repair; c2 and c3 are its payoff and its method, all three using the same single jar.",
    "device_short": "a plain glass jar between two people that fills with small warm pebbles",
    "art_direction": "New device: one plain glass jar on cream paper between two plain figure silhouettes, filling and emptying with small warm pebbles.",
    "device_lock": ("One plain simple clear glass jar with no lid and no decoration, drawn flat on cream paper. "
                    "Pebbles are small plain smooth warm-toned ovals. Figures are plain solid silhouettes with no "
                    "facial features. Absolutely no numerals, no measurement marks, no scale lines, no labels and "
                    "no writing on the jar or anywhere else."),
    "tradeoffs": [{"tradeoff": "Using coins and a money box as the book's banking metaphor does, versus pebbles in a jar", "recommendation": "Pebbles in a jar",
                   "quality_impact": "Coins carry numerals and denominations, which no illustration here may show, and money muddies the point for a child; pebbles keep it about accumulation."}],
    "energy_curve": "Warm at the jar's introduction. Bright through the filling. Honest and quiet at the empty jar. Reassuring at the mistakes beat. Encouraging at the close.",
    "sample_section": "s9", "human_note": "Section s9 is the reassurance about mistakes. This is the line she most needs. Warm.",
    "pause_beats": [{"section": "s5", "purpose": "She thinks about what fills a jar"}, {"section": "s11", "purpose": "She thinks of a jar of hers that's low"}, {"section": "s13", "purpose": "She picks one pebble to put in"}],
    "grounded_in": {"s1_to_s4": "Emotional Bank Account, the jar introduced", "s5_to_s8": "the deposits and the withdrawals", "s9_to_s11": "why a full jar absorbs mistakes", "s12_to_s15": "corrective, one pebble at a time"},
    "sections": [
        ("s1", "Setup", "Diana, between you and every person you know, there's a jar.", "Diana, between you and every person you know, there's a jar.", 1.4, "measured", "warm", ["a jar"], "Intriguing, gentle."),
        ("s2", "What's in it", "You can't see it. But it fills up, or it empties, depending on what happens between you.", "You can't see it. <break time=\"0.4s\"/> But it fills up, or it empties, <break time=\"0.4s\"/> depending on what happens between you.", 1.4, "measured", "curious", ["fills up"], "Picture-building."),
        ("s3", "What it holds", "What's in the jar is how safe that person feels with you. That's all it is. Safeness.", "What's in the jar is how safe that person feels with you. <break time=\"0.4s\"/> That's all it is. <break time=\"0.3s\"/> Safeness.", 1.4, "measured", "tender", ["safeness"], "Slow on the word safeness."),
        ("s4", "Deposits", "And every small kind thing puts a pebble in. Keeping your word. Being decent when nobody's watching. Just listening properly.", "And every small kind thing puts a pebble in. <break time=\"0.4s\"/> Keeping your word. <break time=\"0.3s\"/> Being decent when nobody's watching. <break time=\"0.3s\"/> Just listening properly.", 1.4, "measured", "warm", ["a pebble in"], "Warm list."),
        ("s5", "Small ones", "Not big grand things. Small ones. Small ones are the whole method.", "Not big grand things. <break time=\"0.4s\"/> Small ones. <break time=\"0.4s\"/> Small ones are the whole method. <break time=\"2.5s\"/>", 2.5, "slow", "steady", ["small ones"], "Pause beat one. Let it settle."),
        ("s6", "Withdrawals", "And things take pebbles out too. Breaking a promise. Cutting somebody off. Not listening when they needed you to.", "And things take pebbles out too. <break time=\"0.4s\"/> Breaking a promise. <break time=\"0.3s\"/> Cutting somebody off. <break time=\"0.4s\"/> Not listening when they needed you to.", 1.4, "measured", "gentle", ["out too"], "Honest, not heavy."),
        ("s7", "An empty jar", "And when a jar gets low, everything goes tight. You start measuring every single word before you say it.", "And when a jar gets low, everything goes tight. <break time=\"0.5s\"/> You start measuring every single word before you say it.", 1.4, "measured", "steady", ["measuring every word"], "She'll recognise this feeling."),
        ("s8", "You've felt it", "You know that feeling. Where you can't relax with somebody, and you're not even sure why. That's a low jar.", "You know that feeling. <break time=\"0.4s\"/> Where you can't relax with somebody, and you're not even sure why. <break time=\"0.4s\"/> That's a low jar.", 1.4, "measured", "gentle", ["a low jar"], "Naming something she's felt."),
        ("s9", "The good news", "But here's the lovely bit. When a jar is full, you can get it wrong. You can say it clumsily. And they'll still know what you meant.", "But here's the lovely bit. <break time=\"0.5s\"/> When a jar is full, you can get it wrong. <break time=\"0.4s\"/> You can say it clumsily. <break time=\"0.4s\"/> And they'll still know what you meant.", 1.4, "slow", "warm", ["still know what you meant"], "The most reassuring line in the film."),
        ("s10", "That's the point", "A full jar gives your mistakes somewhere to land. That's what it's for.", "A full jar gives your mistakes somewhere to land. <break time=\"0.4s\"/> That's what it's for.", 1.4, "measured", "tender", ["somewhere to land"], "Warm and definite."),
        ("s11", "Her turn", "Think of somebody whose jar with you might be a bit low right now.", "Think of somebody whose jar with you might be a bit low right now. <break time=\"2.5s\"/>", 2.5, "slow", "gentle", ["a bit low"], "Pause beat two. No guilt in the delivery."),
        ("s12", "Not a big fix", "You don't need a big apology or a grand gesture. Those don't fill jars. They never have.", "You don't need a big apology or a grand gesture. <break time=\"0.4s\"/> Those don't fill jars. <break time=\"0.3s\"/> They never have.", 1.4, "measured", "steady", ["don't fill jars"], "Relieving."),
        ("s13", "The move", "One pebble. That's it. One small ordinary kind thing, today. And then another one tomorrow.", "One pebble. <break time=\"0.3s\"/> That's it. <break time=\"0.4s\"/> One small ordinary kind thing, today. <break time=\"0.4s\"/> And then another one tomorrow. <break time=\"2.5s\"/>", 2.5, "measured", "encouraging", ["one pebble"], "Pause beat three. The actual tool."),
        ("s14", "It's slow", "It's slow. Jars are always slow. But they do fill, and you can feel it when they do.", "It's slow. <break time=\"0.3s\"/> Jars are always slow. <break time=\"0.4s\"/> But they do fill, <break time=\"0.3s\"/> and you can feel it when they do.", 1.4, "measured", "warm", ["they do fill"], "Honest and hopeful."),
        ("s15", "Landing", "Ours is full, Diana. Right to the top. You could say anything to me and it would land somewhere soft.", "Ours is full, Diana. <break time=\"0.4s\"/> Right to the top. <break time=\"0.5s\"/> You could say anything to me and it would land somewhere soft.", 0.0, "slow", "tender", ["somewhere soft"], "Personal, warm, unhurried close."),
    ],
    "spec": [
        ("sc1", "s1", "DIANA", "The girl stands warm and attentive, curious about something new."),
        ("sc2", "s2", "NONE", "One plain empty glass jar standing between two plain figure silhouettes on cream paper."),
        ("sc3", "s3", "NONE", "The plain glass jar shown close and empty, plain and clear."),
        ("sc4", "s4", "NONE", "A single small warm pebble dropping into the plain glass jar, a few pebbles already resting at the bottom."),
        ("sc5", "s5", "NONE", "The jar about a third full of small warm pebbles, quiet and ordinary."),
        ("sc6", "s6", "NONE", "A single small pebble being lifted out of the jar by an unseen hand, only the hand and forearm visible, no face and no body."),
        ("sc7", "s7", "NONE", "The jar nearly empty, only two or three pebbles left at the bottom, between the two plain figures."),
        ("sc8", "s8", "DIANA", "The girl looks tense and careful, holding herself slightly stiffly, uneasy."),
        ("sc9", "s9", "NONE", "The jar full to the top with warm pebbles, glowing gently."),
        ("sc10", "s10", "NONE", "A close view of the full jar with one pebble sitting slightly askew on the top, plainly absorbed by the rest."),
        ("sc11", "s11", "DIANA", "The girl looks thoughtful and honest, considering someone she cares about."),
        ("sc12", "s12", "DIANA", "The girl looks relieved, shoulders easing, a small hopeful expression."),
        ("sc13", "s13", "DIANA", "The girl carefully holds one small pebble between her finger and thumb, deliberate and gentle."),
        ("sc14", "s14", "NONE", "The jar slowly filling, now half full of warm pebbles, steady and unhurried."),
        ("sc15", "s15", "DIANA", "The girl stands calm and warm in soft evening light."),
        ("sc16", "s9", "NONE", "A close view of the full glowing jar of warm pebbles, generous and settled."),
        ("sc17", "s4", "NONE", "A close view of one small warm pebble just about to land among the others in the jar."),
        ("sc18", "s15", "NONE", "The full glass jar of warm pebbles standing in soft evening light between two plain figures, calm and settled."),
    ],
    "heroes": {"sc9", "sc10", "sc16", "sc18"}, "wides": set(),
}
FILM20["clauses"] = {
    "OPEN": (G.OPEN, {"sc1", "sc8", "sc11", "sc12", "sc13", "sc15"}),
    "NOICON": (G.NOICON, {"sc1", "sc8", "sc11", "sc12", "sc13", "sc15"}),
    "SHOES": (SHOES, {"sc1", "sc8", "sc11", "sc12", "sc13", "sc15"}),
    "JAR": (("One plain simple clear glass jar with no lid and no decoration, drawn flat on cream paper. Pebbles "
             "are small plain smooth warm-toned ovals. Figures are plain solid silhouettes with no facial "
             "features. Absolutely NO numerals, NO measurement marks, NO scale lines, NO labels and NO writing on "
             "the jar or anywhere in the frame. No scenery, no background."),
            {"sc2", "sc3", "sc4", "sc5", "sc6", "sc7", "sc9", "sc10", "sc14", "sc16", "sc17", "sc18"}),
}

# ---------------------------------------------------------------- FILM 21
FILM21 = {**cbase(21, "diana-habits-both-ends-up", "DianaBothEndsUp", "Both Ends Up", "Habit 4",
                  "The 7 Habits, Habit 4 'Six Paradigms of Human Interaction' - direct excerpt read for this film"),
    "topic": "Think Win-Win, from Habit 4, told as Dad showing that a see-saw only has one rule and you are allowed to stop playing on one",
    "summary": ("Film 21. Habit 4, Think Win-Win. Covey lists six paradigms of human interaction and argues that "
                "most people think in dichotomies, strong or weak, win or lose, and that this thinking is "
                "fundamentally flawed because it rests on power and position rather than principle. Win-win sees "
                "life as a cooperative rather than a competitive arena, and rests on the belief that there is "
                "plenty for everybody. Deliberately reuses the see-saw device from the first series."),
    "existing": [{"title": "Playground sharing and turn-taking rules", "url": SRC, "source": "classroom material", "angle": "Take turns",
                  "what_it_covers": "Splits a fixed thing more fairly without ever questioning that it has to be split"},
                 {"title": "Competitive games and class ranking", "url": SRC, "source": "classroom material", "angle": "Who won?",
                  "what_it_covers": "Trains a child to read every situation as having a winner and a loser"},
                 {"title": "'Let the other person win' politeness advice", "url": SRC, "source": "web", "angle": "Be the bigger person",
                  "what_it_covers": "Teaches losing on purpose, which the book names as its own separate trap"}],
    "saturated": ["Turn-taking advice that assumes the thing being shared is fixed in size"],
    "gaps": ["Showing a child a third option beyond winning and losing",
             "Naming that giving in every time is its own trap and not the same as kindness"],
    "data_points": [("The book lists six paradigms of human interaction: win-win, win-lose, lose-win, lose-lose, win, and win-win or no deal.", SRC, "The 7 Habits, Habit 4", "primary_source", "expected", "why the film shows more than two options"),
                     ("It states that most people think in dichotomies, strong or weak, win or lose, and that this kind of thinking is fundamentally flawed because it is based on power and position rather than principle.", SRC, "The 7 Habits, Habit 4", "primary_source", "surprising", "the see-saw is exactly this dichotomy made physical"),
                     ("Win-win is defined as a frame of mind that constantly seeks mutual benefit, and the book says it sees life as a cooperative, not a competitive arena.", SRC, "The 7 Habits, Habit 4", "primary_source", "expected", "the corrective the film offers"),
                     ("The Scarcity Mentality is described as seeing life as though there were only one pie, so that a big piece for someone else means less for everybody, while the Abundance Mentality holds that there is plenty out there and enough to spare.", SRC, "The 7 Habits, Habit 4 ('Abundance Mentality')", "primary_source", "surprising", "the belief underneath the whole habit")],
    "questions": ["Does someone always have to lose?", "Is it kind to always let the other person win?", "What if we both want the same thing?"],
    "misconceptions": [("Someone winning means someone else loses", "That's only true of a see-saw. Most real things aren't see-saws.", "Habit 4"),
                        ("Always giving in is the kind thing to do", "The book names that as its own separate trap, not as generosity.", "Habit 4")],
    "pain_points": ["Turning ordinary disagreements into contests", "Giving in every time and quietly resenting it"],
    "angles": [("A See-Saw Has One Rule", "narrative", "One end up means the other end down. That's the only thing a see-saw can do.", "Reuses a device she already knows to make zero-sum thinking physical.", ["Habit 4"]),
               ("You Can Get Off It", "contrarian", "Most things aren't see-saws. You just got in the habit of treating them like one.", "Offers the third option instead of picking a side.", ["Habit 4"]),
               ("Giving In Isn't Kindness", "evergreen", "Losing on purpose every time is its own trap, and the book says so.", "Protects a naturally accommodating child from the opposite error.", ["Habit 4"])],
    "kahneman": "Most people think in dichotomies, win or lose, but win-win sees life as a cooperative rather than a competitive arena, on the belief that there is plenty for everybody.",
    "excluded": ["The adult negotiation, contract and business-agreement examples, and the Win-Win or No Deal option, which needs adult context."],
    "concepts": [
        {"id": "c1", "title": "Both Ends Up", "hook": "Diana, remember the see-saw? It only knows how to do one thing.", "narrative_structure": "story",
         "visual_approach": "The same plain see-saw from the earlier series, tipping one way then the other, then the same plank lifted off and laid flat as a bridge both figures stand on.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 145,
         "key_points": ["A see-saw has exactly one rule: one up, one down", "We treat almost everything like a see-saw", "Most things genuinely aren't", "Always being the down end isn't kindness either", "Take the plank off and both ends can be up"],
         "core_message": "One up means one down, but only on a see-saw. Take the plank off and you can both stand on it.", "cta": "Next disagreement, ask whether it's really a see-saw.", "tone": "Warm, playful, then quietly serious.",
         "why_this_works": "It uses a device she already knows from the first series and turns it into a question she can ask.", "grounded_in": ["Habit 4"]},
        {"id": "c2", "title": "You Can Get Off It", "hook": "Most things aren't see-saws. We just treat them like one.", "narrative_structure": "myth_busting",
         "visual_approach": "The plank being lifted clear of its pivot, the pivot left empty beneath it.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 75,
         "key_points": ["The see-saw rule comes from the shape, not from the situation", "Change the shape and the rule disappears"],
         "core_message": "The rule was in the see-saw, not in the world.", "cta": "Check whether the thing is actually a see-saw.", "tone": "Curious.",
         "why_this_works": "Locates the problem in the framing rather than in either person, folded into c1 as its hinge.", "grounded_in": ["Habit 4"]},
        {"id": "c3", "title": "Giving In Isn't Kindness", "hook": "Being the down end every time isn't generous.", "narrative_structure": "comparison",
         "visual_approach": "One figure permanently at the low end of the see-saw, sitting patiently and going nowhere.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 75,
         "key_points": ["Losing on purpose is its own separate trap", "It looks like kindness and quietly turns into resentment"],
         "core_message": "Always taking the low end isn't kindness, it's just a different way to lose.", "cta": "Notice if you always take the low end.", "tone": "Gentle and honest.",
         "why_this_works": "Protects an accommodating child from over-correcting, folded into c1 as its warning beat.", "grounded_in": ["Habit 4"]}],
    "rationale": "c1 carries the see-saw from its single rule to the plank laid flat; c2 and c3 are its hinge and its warning, all three using the same plank.",
    "device_short": "the see-saw from the earlier series, its plank finally lifted off and laid flat",
    "art_direction": "Reused device: the same plain wooden see-saw plank and simple triangular pivot from the first series, now also shown lifted off the pivot and laid flat as a bridge.",
    "device_lock": ("One plain simple wooden plank and one plain simple triangular wooden pivot, drawn flat on cream "
                    "paper, in the same style as the earlier series. No playground scenery, no grass, no handles, "
                    "no decoration, no numerals, no writing. Figures are plain solid silhouettes with no facial "
                    "features."),
    "tradeoffs": [{"tradeoff": "Inventing a new device versus reusing the see-saw from the first series", "recommendation": "Reuse the see-saw",
                   "quality_impact": "She already knows this object from the loss-aversion film, so the film can spend its time on the idea rather than on establishing a new picture, exactly as Daniel asked."}],
    "energy_curve": "Playful at the see-saw. Curious through the one rule. Gentle and serious at the giving-in beat. Bright and freeing when the plank comes off. Warm at the close.",
    "sample_section": "s11", "human_note": "Section s11 is where the plank comes off. This should feel like a small liberation.",
    "pause_beats": [{"section": "s4", "purpose": "She watches the see-saw do the only thing it can"}, {"section": "s8", "purpose": "She thinks about whether she's always the low end"}, {"section": "s13", "purpose": "She thinks of a see-saw she could get off"}],
    "grounded_in": {"s1_to_s4": "Habit 4, the dichotomy made physical", "s5_to_s8": "Habit 4, win-lose and lose-win", "s9_to_s11": "Habit 4, the cooperative arena", "s12_to_s15": "Habit 4 corrective, plenty for everybody"},
    "sections": [
        ("s1", "Setup", "Diana, remember the see-saw? From the film about losing. It only knows how to do one thing.", "Diana, remember the see-saw? <break time=\"0.4s\"/> From the film about losing. <break time=\"0.4s\"/> It only knows how to do one thing.", 1.4, "measured", "warm", ["one thing"], "Warm callback to the first series."),
        ("s2", "The one rule", "One end goes up. The other end goes down. That's it. That's the whole machine.", "One end goes up. <break time=\"0.3s\"/> The other end goes down. <break time=\"0.4s\"/> That's it. <break time=\"0.3s\"/> That's the whole machine.", 1.4, "measured", "curious", ["whole machine"], "Almost playful."),
        ("s3", "We do it everywhere", "And we treat nearly everything like that. Who's right. Who got more. Who won.", "And we treat nearly everything like that. <break time=\"0.4s\"/> Who's right. <break time=\"0.3s\"/> Who got more. <break time=\"0.3s\"/> Who won.", 1.4, "measured", "steady", ["who won"], "Recognisable, not preachy."),
        ("s4", "Watch it", "Watch it for a second. Up, down. Up, down. Nobody's ever up at the same time.", "Watch it for a second. <break time=\"0.4s\"/> Up, down. <break time=\"0.3s\"/> Up, down. <break time=\"0.4s\"/> Nobody's ever up at the same time. <break time=\"2.5s\"/>", 2.5, "slow", "curious", ["at the same time"], "Pause beat one. Let the rhythm register."),
        ("s5", "Two ways to play", "So on a see-saw there are only two ways to be. Up, while somebody's down. Or down, while somebody's up.", "So on a see-saw there are only two ways to be. <break time=\"0.4s\"/> Up, while somebody's down. <break time=\"0.4s\"/> Or down, while somebody's up.", 1.4, "measured", "steady", ["only two ways"], "Set up the trap."),
        ("s6", "The winning end", "Some people always want the up end. They'll push to get it. You know some of those.", "Some people always want the up end. <break time=\"0.4s\"/> They'll push to get it. <break time=\"0.3s\"/> You know some of those.", 1.4, "measured", "dry", ["the up end"], "Lightly dry."),
        ("s7", "The giving-in end", "And some people always take the down end. Every time. And they call it being nice.", "And some people always take the down end. <break time=\"0.4s\"/> Every time. <break time=\"0.4s\"/> And they call it being nice.", 1.4, "measured", "gentle", ["being nice"], "Careful here. She may be one of these."),
        ("s8", "It isn't", "But that's not kindness, Diana. That's just a quieter way of losing. And it turns into being cross underneath, eventually.", "But that's not kindness, Diana. <break time=\"0.5s\"/> That's just a quieter way of losing. <break time=\"0.4s\"/> And it turns into being cross underneath, eventually. <break time=\"2.5s\"/>", 2.5, "slow", "tender", ["quieter way of losing"], "Pause beat two. Gentle but honest."),
        ("s9", "The question", "So here's the question nobody asks. Why are we on a see-saw at all?", "So here's the question nobody asks. <break time=\"0.5s\"/> Why are we on a see-saw at all?", 1.4, "measured", "curious", ["at all"], "The turn. Genuine curiosity."),
        ("s10", "It's the shape", "Because that rule, one up one down, isn't a rule about life. It's a rule about that shape. The plank and the little triangle.", "Because that rule, one up one down, isn't a rule about life. <break time=\"0.5s\"/> It's a rule about that shape. <break time=\"0.4s\"/> The plank and the little triangle.", 1.4, "measured", "steady", ["about that shape"], "Land the insight."),
        ("s11", "Take it off", "So take the plank off. Just lift it off the triangle and lay it flat. And now look. You can both stand on it.", "So take the plank off. <break time=\"0.4s\"/> Just lift it off the triangle and lay it flat. <break time=\"0.5s\"/> And now look. <break time=\"0.4s\"/> You can both stand on it.", 1.4, "slow", "warm", ["both stand on it"], "A small liberation. Bright."),
        ("s12", "Most things", "Most things in your life are actually like that. Not a see-saw. Just a plank somebody propped up on a triangle out of habit.", "Most things in your life are actually like that. <break time=\"0.4s\"/> Not a see-saw. <break time=\"0.5s\"/> Just a plank somebody propped up on a triangle out of habit.", 1.4, "measured", "curious", ["out of habit"], "Reframe."),
        ("s13", "The move", "So next time you're disagreeing with somebody, ask it. Is this really a see-saw? Or could we both be up?", "So next time you're disagreeing with somebody, ask it. <break time=\"0.4s\"/> Is this really a see-saw? <break time=\"0.4s\"/> Or could we both be up? <break time=\"2.5s\"/>", 2.5, "measured", "encouraging", ["both be up"], "Pause beat three. The actual question."),
        ("s14", "Not always", "Sometimes it really is a see-saw. Sometimes there's one last biscuit. That's fine. But it's rarer than you'd think.", "Sometimes it really is a see-saw. <break time=\"0.4s\"/> Sometimes there's one last biscuit. <break time=\"0.3s\"/> That's fine. <break time=\"0.4s\"/> But it's rarer than you'd think.", 1.4, "measured", "warm", ["rarer than you'd think"], "Honest, a bit light."),
        ("s15", "Landing", "You and me were never a see-saw, Diana. There was never a version of this where I go up and you go down.", "You and me were never a see-saw, Diana. <break time=\"0.5s\"/> There was never a version of this where I go up and you go down.", 0.0, "slow", "tender", ["never a see-saw"], "Personal, warm, unhurried close."),
    ],
    "spec": [
        ("sc1", "s1", "DIANA", "The girl looks up with recognition and a small smile, remembering something."),
        ("sc2", "s2", "NONE", "A plain wooden plank balanced on a plain simple triangular wooden pivot, tilted with one end up."),
        ("sc3", "s3", "NONE", "The same see-saw tilted the other way, the opposite end now up."),
        ("sc4", "s4", "NONE", "The see-saw with a plain figure silhouette at each end, one high and one low."),
        ("sc5", "s5", "NONE", "A close view of the plain triangular pivot alone beneath the tilted plank."),
        ("sc6", "s6", "NONE", "The see-saw with the left figure silhouette high up, arms slightly raised, the right one low."),
        ("sc7", "s7", "NONE", "The see-saw with the same figure silhouette at the low end, sitting patiently and still."),
        ("sc8", "s8", "DIANA", "The girl looks quietly thoughtful and a little uncomfortable, recognising something about herself."),
        ("sc9", "s9", "DIANA", "The girl looks up with genuine curiosity, an idea arriving."),
        ("sc10", "s10", "NONE", "The plain plank and the plain triangular pivot drawn slightly apart from each other, as two separate objects."),
        ("sc11", "s11", "NONE", "The plain plank laid flat on the ground with a plain figure silhouette standing at each end, both level."),
        ("sc12", "s12", "NONE", "The empty triangular pivot alone on the cream page, the plank gone from it."),
        ("sc13", "s13", "DIANA", "The girl stands with one hand raised slightly, asking a question, bright and engaged."),
        ("sc14", "s14", "DIANA", "The girl looks even-handed and calm, accepting something reasonable."),
        ("sc15", "s15", "DIANA", "The girl stands calm and warm in soft evening light."),
        ("sc16", "s11", "NONE", "A close view of the flat plank with both figure silhouettes standing level on it, warmly lit."),
        ("sc17", "s4", "NONE", "The tilted see-saw with both figures, warmly lit, the imbalance clear."),
        ("sc18", "s15", "NONE", "The plain plank lying flat and level in warm evening light with two plain figures standing on it side by side."),
    ],
    "heroes": {"sc11", "sc16", "sc18"}, "wides": {"sc4", "sc17"},
}
FILM21["clauses"] = {
    "OPEN": (G.OPEN, {"sc1", "sc8", "sc9", "sc13", "sc14", "sc15"}),
    "NOICON": (G.NOICON, {"sc1", "sc8", "sc9", "sc13", "sc14", "sc15"}),
    "SHOES": (SHOES, {"sc1", "sc8", "sc9", "sc13", "sc14", "sc15"}),
    "SEESAW": (("One plain simple wooden plank and one plain simple triangular wooden pivot, drawn flat on cream "
                "paper. No playground scenery, no grass, no sky, no handles, no seats, no decoration, no numerals "
                "and no writing. Figures are plain solid silhouettes with no facial features."),
               {"sc2", "sc3", "sc4", "sc5", "sc6", "sc7", "sc10", "sc11", "sc12", "sc16", "sc17", "sc18"}),
}

if __name__ == "__main__":
    G_FILMS = {"m18": FILM18, "m19": FILM19, "m20": FILM20, "m21": FILM21}
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
