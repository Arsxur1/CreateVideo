"""Film 25 of 25: the finale, walking back through both books using the locked devices."""
import sys
import filmgen as G
from mindset_a import base, SRC, FILM1
from mindset_b import FILM2
from mindset_d import FILM13
from mindset_e import CSRC, SHOES, FILM14, FILM15, FILM17
from mindset_f import FILM18, FILM19, FILM20, FILM21
from mindset_g import FILM22, FILM23, FILM24

# Reuse the exact locked device text from each source film so every callback is drawn
# the way its own film drew it.
DOOR = FILM1["clauses"]["DOOR"][0]
WALL = FILM2["clauses"]["WALL"][0]
CREATURE = FILM13["clauses"]["CREATURE"][0]
MAP = FILM14["clauses"]["MAP"][0]
STONES = FILM15["clauses"]["STONES"][0]
LADDER = FILM17["clauses"]["LADDER"][0]
GRID = FILM18["clauses"]["GRID"][0]
GOOSE = FILM19["clauses"]["GOOSE"][0]
JAR = FILM20["clauses"]["JAR"][0]
SEESAW = FILM21["clauses"]["SEESAW"][0]

# sc18 is the payoff shot: the plank OFF the pivot. The film 21 clause mandates a pivot, which is
# exactly what keeps reappearing underneath the plank, so the finale uses a plank-only clause.
FLAT = ("One plain simple wooden plank drawn flat on cream paper and NOTHING ELSE AT ALL. There is no "
        "triangle, no wedge, no fulcrum, no pivot, no block, no support, no stand, no leg and no object "
        "of any kind underneath the plank or anywhere else in the picture. No playground scenery, no "
        "grass, no sky, no handles, no seats, no decoration, no numerals and no writing.")
GLASSES = FILM22["clauses"]["GLASSES"][0]
PAINT = FILM23["clauses"]["PAINT"][0]
SAW = FILM24["clauses"]["SAW"][0]

# The court clause is rewritten rather than reused: the original under-specified wording drifted
# into basketball blueprints and phantom crowds on the two films that shared it.
COURT = ("The court is one single plain flat warm-toned open floor shape, like a bare empty stage, "
         "drawn simply on cream paper with nothing on it and nothing around it. Absolutely NO hoops, "
         "NO nets, NO backboards, NO free-throw arcs, NO painted key or court markings, NO lines of "
         "any kind, NO stands, NO seats, NO crowd, NO spectators, NO walls, NO ceiling, NO numerals "
         "and NO writing.")

BOOKS = ("The books are two plain simple closed hardback books lying flat on cream paper, one a soft "
         "faded blue and one a soft faded sand colour. Their covers and spines are COMPLETELY BLANK: "
         "absolutely no title, no letters, no words, no writing, no numbers, no symbols, no emblems "
         "and no decoration of any kind. No shelf, no table, no scenery, no background.")

FINALE_GUARD = [
    "No numeral appears in any illustration.",
    "Every scene with a person contains exactly one child.",
    "Each callback is drawn with the same locked device text used by the film it comes from, so the "
    "picture matches what she already watched.",
    "The film claims nothing new from either book; it only revisits ideas already grounded and "
    "delivered in the twenty-four films before it.",
]

FILM25 = {**base(25, "diana-two-books", "DianaTwoBooks", "Diana and the Two Books", "Both books"),
    "source_url_secondary": CSRC,
    "source_title_secondary": "The 7 Habits of Highly Effective People - Stephen R. Covey",
    "guardrails": FINALE_GUARD,
    "topic": "The closing film of the series: Dad walks back through both books, picking up each device the earlier films built, and says what he actually wants for her",
    "summary": ("Film 25, the finale. A recap film that mirrors the closer of the first series. It walks "
                "back through the two books in order, picking up the door still being built, the word yet, "
                "the empty court, the small grey creature, the map, the gap between the stones, the ladder, "
                "the four boxes, the goose, the jar, the glasses, the two colours, the blunt saw and the "
                "plank laid flat. Nothing new is taught. It gathers what was taught and hands it over."),
    "existing": [
        {"title": "End-of-course recap videos for children", "url": SRC, "source": "web", "angle": "Let's review what we learned",
         "what_it_covers": "Quizzes the child on the content rather than handing the ideas over as hers"},
        {"title": "Motivational 'you can do anything' send-offs", "url": SRC, "source": "web", "angle": "Believe in yourself",
         "what_it_covers": "Ends on encouragement with nothing underneath it to hold on to"},
        {"title": "Summary chapters at the end of self-help books", "url": CSRC, "source": "primary source", "angle": "Key takeaways",
         "what_it_covers": "Compresses the ideas back into a list, which is the form a child forgets fastest"}],
    "saturated": ["Recap videos that quiz the child instead of giving the ideas back to them"],
    "gaps": ["Closing a long series by returning each idea to its own picture, so the memory has something to hold",
             "A parent saying plainly what they actually want for their child, at the end and not as a slogan"],
    "data_points": [
        ("Dweck's central claim across the book is that believing your qualities can be developed changes what effort and failure mean to you.", SRC, "Mindset - Dr Carol S. Dweck", "primary_source", "expected", "the spine of the first half"),
        ("She describes the word 'yet' as the difference between a verdict and a path, in her account of a school that graded work 'not yet'.", SRC, "Mindset, on 'not yet'", "primary_source", "surprising", "the callback in section four"),
        ("Covey's frame is that between what happens to you and what you do about it there is a space, and in that space you choose.", CSRC, "The 7 Habits, Habit 1", "primary_source", "expected", "the hinge of the second half"),
        ("He places the private victory of Habits 1 to 3 before the public victory of Habits 4 to 6, in that order.", CSRC, "The 7 Habits, 'The Maturity Continuum'", "primary_source", "expected", "why the film walks the callbacks in this order"),
        ("Covey's last habit, sharpening the saw, is the one he places at the centre of your own circle of influence.", CSRC, "The 7 Habits, Habit 7", "primary_source", "expected", "the final callback before the close")],
    "questions": ["What was all of that actually for?", "How am I supposed to remember twenty-four films?", "What does Dad actually want from me?"],
    "misconceptions": [("A series like this is a set of rules to follow", "It is a set of pictures to reach for, and she can only reach for the ones she remembers.", "Both books"),
                        ("The ending should be a summary", "A list is the form she forgets fastest; the pictures are the form she keeps.", "Both books")],
    "pain_points": ["Trying to hold twenty-four separate ideas at once", "Wondering whether she is measuring up to all of it"],
    "angles": [("The Whole Shelf At Once", "narrative", "Every picture we built, laid out one after another.", "Recognition is effortless where recall is hard; she has seen all of these.", ["Both books"]),
               ("Nothing New Tonight", "contrarian", "This one teaches you nothing. It just hands things over.", "Removes the pressure of a final lesson and lets the film be a goodbye instead.", ["Both books"]),
               ("What I Actually Want", "evergreen", "Not that she gets it all right. Something much smaller.", "Gives the whole series a human landing rather than a moral.", ["Both books"])],
    "kahneman": "Between what happens to you and what you do about it there is a space, and in that space is your freedom to choose.",
    "excluded": ["Any new claim from either book; the finale only revisits what the earlier twenty-four films already grounded."],
    "concepts": [
        {"id": "c1", "title": "Diana and the Two Books", "hook": "Twenty-four times now, Diana. That's every one of them.", "narrative_structure": "journey",
         "visual_approach": "A procession of the locked devices from the earlier films, each drawn exactly as its own film drew it, bookended by two plain blank books.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old, at the end of the series", "target_platform": "generic", "target_duration_seconds": 195,
         "key_points": ["The door still being built, and the word yet", "The empty court and the small grey creature", "The map, the space between the stones, the ladder and the quiet box", "The goose, the jar, the glasses, the two colours and the blunt saw", "The plank laid flat, and what he actually wants for her"],
         "core_message": "None of it was about getting things right. It was about knowing you are not finished, and being able to choose what happens next.", "cta": "Keep the pictures. Reach for whichever one fits.", "tone": "Unhurried, warm, and at the end, quietly moved.",
         "why_this_works": "Recognition carries what recall cannot; she has already watched every one of these pictures, so the finale costs her nothing to follow.", "grounded_in": ["Both books"]},
        {"id": "c2", "title": "Nothing New Tonight", "hook": "This one doesn't teach you anything.", "narrative_structure": "myth_busting",
         "visual_approach": "The two plain blank books lying closed and unopened.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 60,
         "key_points": ["A final film does not need a final lesson", "Handing the ideas over is the whole job"],
         "core_message": "The last one is a goodbye, not a test.", "cta": "Just listen to this one.", "tone": "Gentle.",
         "why_this_works": "Removes the pressure of a closing lesson, folded into c1 as its opening move.", "grounded_in": ["Both books"]},
        {"id": "c3", "title": "What I Actually Want", "hook": "Not that you get all of this right.", "narrative_structure": "story",
         "visual_approach": "The girl in warm evening light, and the unfinished door still being built.", "suggested_playbook": "custom-atelier-storybook",
         "target_audience": "The same 8-year-old", "target_platform": "generic", "target_duration_seconds": 70,
         "key_points": ["The wish is smaller and more specific than doing well", "Being unfinished is the good news, not the problem"],
         "core_message": "I want you to know you are not finished.", "cta": "Remember that on the hard days.", "tone": "Quietly moved.",
         "why_this_works": "Lands the whole series on a person rather than a principle, folded into c1 as its close.", "grounded_in": ["Both books"]}],
    "rationale": "c1 walks the whole shelf in order; c2 is its opening permission and c3 its landing, all three carried by the devices the earlier films already locked.",
    "device_short": "every device from the twenty-four earlier films, walked through in order between two plain blank books",
    "art_direction": ("No new device. Each callback is drawn with the exact locked clause text from the film it comes "
                      "from, so the picture matches what she already watched. Two plain blank books open and close the film."),
    "device_lock": ("Each device is drawn exactly as its own film drew it, using that film's own locked description. "
                    "The only new object is two plain closed books with completely blank covers and spines."),
    "tradeoffs": [{"tradeoff": "Naming all twenty-four films versus walking only the strongest devices", "recommendation": "Walk fourteen devices",
                   "quality_impact": "Twenty-four callbacks at eight seconds each is a list, not a film; fourteen leaves room for the ending to breathe."}],
    "energy_curve": "Quiet and unhurried at the open. Steady momentum through the two halves, one picture at a time. A pause at the plank. Quietly moved at the close.",
    "sample_section": "s19", "human_note": "Section s19 is the whole series landing. Slow right down. It is allowed to sound like it matters.",
    "pause_beats": [{"section": "s7", "purpose": "She sits with the first book being over"}, {"section": "s17", "purpose": "She looks at the plank lying flat"}, {"section": "s19", "purpose": "She hears what he actually wants"}],
    "grounded_in": {"s1_to_s7": "Mindset, the first half of the series", "s8_to_s17": "The 7 Habits, the second half", "s18_to_s20": "Both books, the close"},
    "sections": [
        ("s1", "Open", "Twenty-four times now, Diana. That's every one of them.", "Twenty-four times now, Diana. <break time=\"0.5s\"/> That's every one of them.", 1.4, "slow", "warm", ["every one"], "Unhurried. He is not in a rush tonight."),
        ("s2", "Nothing new", "And this last one doesn't teach you anything. There's nothing new in it. I just want to walk back through and hand it all to you.", "And this last one doesn't teach you anything. <break time=\"0.4s\"/> There's nothing new in it. <break time=\"0.5s\"/> I just want to walk back through and hand it all to you.", 1.4, "slow", "gentle", ["hand it all to you"], "Take the pressure off immediately."),
        ("s3", "The door", "We started with two doorways. One shut, made of stone, finished. And one still being built, with the scaffolding up. You are the second one. You have always been the second one.", "We started with two doorways. <break time=\"0.4s\"/> One shut, made of stone, finished. <break time=\"0.4s\"/> And one still being built, with the scaffolding up. <break time=\"0.5s\"/> You are the second one. <break time=\"0.3s\"/> You have always been the second one.", 1.4, "measured", "warm", ["still being built"], "Film 1. Certain and warm."),
        ("s4", "Yet", "Then that wall, remember. Solid all the way across. And one small word put on the end of it, and the whole thing swung open like a door. Yet. Three letters. Still the best thing in this series.", "Then that wall, remember. <break time=\"0.4s\"/> Solid all the way across. <break time=\"0.4s\"/> And one small word put on the end of it, and the whole thing swung open like a door. <break time=\"0.5s\"/> Yet. <break time=\"0.4s\"/> Three letters. Still the best thing in this series.", 1.4, "measured", "encouraging", ["yet"], "Film 2. A little bit of delight."),
        ("s5", "The court", "The empty court. Early, before anyone was watching. That's where the thing actually got built. Nobody claps for that part, and that's the part that counts.", "The empty court. <break time=\"0.4s\"/> Early, before anyone was watching. <break time=\"0.4s\"/> That's where the thing actually got built. <break time=\"0.5s\"/> Nobody claps for that part, <break time=\"0.3s\"/> and that's the part that counts.", 1.4, "measured", "steady", ["nobody was watching"], "Films 5 and 8."),
        ("s6", "The creature", "And that small grey thing that turns up whenever something is hard. You didn't chase it off. You gave it a name, and then you taught it a better sentence, and now it walks along beside you.", "And that small grey thing that turns up whenever something is hard. <break time=\"0.5s\"/> You didn't chase it off. <break time=\"0.4s\"/> You gave it a name, <break time=\"0.3s\"/> and then you taught it a better sentence, <break time=\"0.4s\"/> and now it walks along beside you.", 1.4, "measured", "gentle", ["beside you"], "Films 12 and 13. Fond."),
        ("s7", "First book done", "That's the first book. All of it, really, comes down to one thing: you are not finished. Neither am I.", "That's the first book. <break time=\"0.5s\"/> All of it, really, comes down to one thing: <break time=\"0.4s\"/> you are not finished. <break time=\"0.4s\"/> Neither am I. <break time=\"2.5s\"/>", 2.5, "slow", "warm", ["not finished"], "Pause beat one. Let the first half close."),
        ("s8", "The map", "Then the second book, and the map. The one drawn wrong, that no amount of walking faster could fix. Sometimes the problem isn't your effort. It's the map.", "Then the second book, and the map. <break time=\"0.4s\"/> The one drawn wrong, <break time=\"0.4s\"/> that no amount of walking faster could fix. <break time=\"0.5s\"/> Sometimes the problem isn't your effort. <break time=\"0.3s\"/> It's the map.", 1.4, "measured", "steady", ["it's the map"], "Film 14."),
        ("s9", "The space", "And then the two stones, with that gap opening up between them. Something happens, and then something you do about it, and in between there's a space you can stand in. That space is yours. Nobody else gets to be in there.", "And then the two stones, with that gap opening up between them. <break time=\"0.4s\"/> Something happens, <break time=\"0.3s\"/> and then something you do about it, <break time=\"0.4s\"/> and in between there's a space you can stand in. <break time=\"0.5s\"/> That space is yours. <break time=\"0.3s\"/> Nobody else gets to be in there.", 1.4, "slow", "warm", ["that space is yours"], "Film 15. The most important one in the second half."),
        ("s10", "The ladder", "The ladder against the wall. Climbing brilliantly is no good at all if it's leaning on the wrong wall. Check the wall first. It takes about a minute.", "The ladder against the wall. <break time=\"0.4s\"/> Climbing brilliantly is no good at all if it's leaning on the wrong wall. <break time=\"0.5s\"/> Check the wall first. <break time=\"0.3s\"/> It takes about a minute.", 1.4, "measured", "wry", ["the wrong wall"], "Film 17."),
        ("s11", "The boxes", "The four boxes. The spilled cup and the ringing bell shouting at you, and that quiet little seedling in the corner that never shouts and matters more than all of it.", "The four boxes. <break time=\"0.4s\"/> The spilled cup and the ringing bell shouting at you, <break time=\"0.5s\"/> and that quiet little seedling in the corner that never shouts <break time=\"0.3s\"/> and matters more than all of it.", 1.4, "measured", "steady", ["never shouts"], "Film 18."),
        ("s12", "The goose", "The goose and the golden egg. Look after the thing that makes the thing. That's you, by the way. You're the goose.", "The goose and the golden egg. <break time=\"0.4s\"/> Look after the thing that makes the thing. <break time=\"0.5s\"/> That's you, by the way. <break time=\"0.3s\"/> You're the goose.", 1.4, "measured", "warm", ["you're the goose"], "Film 19. Let the last line land lightly."),
        ("s13", "The jar", "The jar between you and somebody else, filling up one small pebble at a time. Turning up. Remembering. Saying sorry properly. That's how it fills, and it's the only way it fills.", "The jar between you and somebody else, filling up one small pebble at a time. <break time=\"0.4s\"/> Turning up. <break time=\"0.3s\"/> Remembering. <break time=\"0.3s\"/> Saying sorry properly. <break time=\"0.5s\"/> That's how it fills, <break time=\"0.3s\"/> and it's the only way it fills.", 1.4, "measured", "gentle", ["one small pebble"], "Film 20."),
        ("s14", "The glasses", "The glasses, handed over before anyone looked at your eyes. Ask one more question before you answer. It's such a small thing and it changes everything.", "The glasses, handed over before anyone looked at your eyes. <break time=\"0.5s\"/> Ask one more question before you answer. <break time=\"0.4s\"/> It's such a small thing <break time=\"0.3s\"/> and it changes everything.", 1.4, "measured", "warm", ["one more question"], "Film 22."),
        ("s15", "The colours", "The blue and the yellow running into each other and making a green that neither one had. The person who does it differently to you isn't the problem. They're the green.", "The blue and the yellow running into each other and making a green that neither one had. <break time=\"0.5s\"/> The person who does it differently to you isn't the problem. <break time=\"0.4s\"/> They're the green.", 1.4, "measured", "delighted", ["they're the green"], "Film 23."),
        ("s16", "The saw", "And the man sawing away for five hours, far too busy to stop and sharpen it. When something starts getting harder, ask whether it's you or whether it's a blunt saw. It's usually the saw.", "And the man sawing away for five hours, far too busy to stop and sharpen it. <break time=\"0.5s\"/> When something starts getting harder, ask whether it's you <break time=\"0.3s\"/> or whether it's a blunt saw. <break time=\"0.4s\"/> It's usually the saw.", 1.4, "measured", "wry", ["blunt saw"], "Film 24."),
        ("s17", "The plank", "And then the see-saw. The one from years ago, where one end could only go up if the other went down. And you lifted the plank right off and laid it flat on the ground, and both ends were up. You don't have to win for me to be pleased with you.", "And then the see-saw. <break time=\"0.4s\"/> The one from years ago, where one end could only go up if the other went down. <break time=\"0.5s\"/> And you lifted the plank right off and laid it flat on the ground, <break time=\"0.4s\"/> and both ends were up. <break time=\"0.5s\"/> You don't have to win for me to be pleased with you. <break time=\"2.5s\"/>", 2.5, "slow", "tender", ["both ends were up"], "Pause beat two. Film 21. The emotional turn."),
        ("s18", "The shelf", "That's the lot. Two books, twenty-five films, and about fourteen pictures. And I don't need you to remember the books, Diana. Just keep the pictures. Reach for whichever one fits.", "That's the lot. <break time=\"0.4s\"/> Two books, twenty-five films, <break time=\"0.3s\"/> and about fourteen pictures. <break time=\"0.5s\"/> And I don't need you to remember the books, Diana. <break time=\"0.4s\"/> Just keep the pictures. <break time=\"0.3s\"/> Reach for whichever one fits.", 1.4, "measured", "warm", ["keep the pictures"], "Practical and affectionate."),
        ("s19", "What I want", "And I should tell you what I actually want, because it isn't that you get all of this right. It's much smaller than that. I want you to know, on the hard days, the ones where nothing goes your way, that you're not finished. That's it. That's the whole thing.", "And I should tell you what I actually want, <break time=\"0.4s\"/> because it isn't that you get all of this right. <break time=\"0.5s\"/> It's much smaller than that. <break time=\"0.5s\"/> I want you to know, on the hard days, <break time=\"0.4s\"/> the ones where nothing goes your way, <break time=\"0.4s\"/> that you're not finished. <break time=\"0.5s\"/> That's it. <break time=\"0.3s\"/> That's the whole thing. <break time=\"2.5s\"/>", 2.5, "slow", "tender", ["you're not finished"], "Pause beat three. Slow right down. The whole series lands here."),
        ("s20", "Landing", "The scaffolding's still up on your door. Good. Mine too. Goodnight, Diana. I'm glad I got to be the one who told you.", "The scaffolding's still up on your door. <break time=\"0.4s\"/> Good. <break time=\"0.3s\"/> Mine too. <break time=\"0.6s\"/> Goodnight, Diana. <break time=\"0.5s\"/> I'm glad I got to be the one who told you.", 0.0, "slow", "tender", ["goodnight, Diana"], "The last line of the whole series. Quiet, unhurried, genuinely moved."),
    ],
    "spec": [
        ("sc1", "s1", "DIANA", "The girl sits calmly with her hands in her lap, settled and listening, quite at ease."),
        ("sc2", "s2", "NONE", "Two plain closed books lying flat side by side on cream paper, covers and spines entirely blank."),
        ("sc3", "s3", "NONE", "Two plain stone doorway shapes side by side on cream paper. The LEFT one is completely filled in and solid, a shut finished stone door with no opening through it at all. The RIGHT one is still under construction, with simple wooden scaffolding poles and planks around it and part of its stonework missing. Nothing else in the picture."),
        ("sc4", "s4", "NONE", "One plain flat RECTANGULAR stone slab with straight edges and square corners, standing upright and seen face on, with one small plain wooden hinge fitted at its left edge and the whole slab swung slightly open like a door, so a narrow wedge of cream paper shows behind it. Nothing else in the picture."),
        ("sc5", "s5", "NONE", "One plain flat warm-toned open floor shape, completely bare and empty, in soft early light."),
        ("sc6", "s6", "NONE", "The small round soft grey creature walking along a plain simple path beside a plain figure silhouette, calm and companionable."),
        ("sc7", "s7", "DIANA", "The girl looks quietly moved, taking something in."),
        ("sc8", "s8", "NONE", "A plain paper map held open, its drawn shape plainly not matching the simple land shape beside it."),
        ("sc9", "s9", "NONE", "Two plain stones on cream paper with a clear open gap between them, wide enough for a person to stand in."),
        ("sc10", "s10", "NONE", "A plain simple wooden ladder leaning against a plain flat wall shape."),
        ("sc11", "s11", "NONE", "The grid of exactly four plain equal squares in a two-by-two arrangement, holding a tipped-over cup with a small spill, a plain handbell with a few short motion lines, a small seedling in a plain pot, and a loose tangle of string."),
        ("sc12", "s12", "NONE", "A plain goose standing calmly beside one single plain golden egg."),
        ("sc13", "s13", "NONE", "A plain clear glass jar standing between two plain figure silhouettes, most of the way full of small warm-toned pebbles."),
        ("sc14", "s13", "DIANA", "The girl leans down and carefully places one single small warm-toned pebble on the ground with her fingertips, gentle and deliberate. She holds nothing else and there are no other objects in the picture."),
        ("sc15", "s14", "NONE", "Exactly TWO pairs of plain spectacles resting side by side on cream paper, one with a round frame and one with a square frame. Both pairs have plain empty lenses. No spirals, no rings, no patterns, no decoration and nothing drawn inside the lenses."),
        ("sc16", "s15", "NONE", "A soft blue paint blob and a soft warm yellow paint blob overlapping, with a clear distinct green where they meet."),
        ("sc17", "s16", "NONE", "ONE single plain handsaw with clean sharp teeth lying beside one plain tree trunk, with one plain rectangular sharpening stone next to it. Exactly one saw in the picture and no second saw anywhere."),
        ("sc18", "s17", "NONE", "A plain simple wooden plank lying DIRECTLY ON THE FLAT GROUND along its entire length, both of its ends resting level on the ground. There is NOTHING underneath the plank. Do NOT draw a triangle, a wedge, a fulcrum or a pivot anywhere in the picture."),
        ("sc19", "s18", "DIANA", "The girl stands looking steady and clear-eyed, understanding something. She is the only thing in the picture; there are no other objects on the ground or anywhere else."),
        ("sc20", "s18", "NONE", "The same two plain blank books lying flat side by side, closed, slightly worn at the corners."),
        ("sc21", "s19", "DIANA", "The girl's expression softens completely, warm and a little overwhelmed."),
        ("sc22", "s20", "DIANA", "The girl stands calm and warm in soft evening light."),
        ("sc23", "s20", "NONE", "ONE single plain stone doorway still under construction, standing alone in the middle of the page with its simple wooden scaffolding poles and planks still in place, in warm evening light. There is exactly one doorway and there are no other arches, stones or stonework anywhere else in the frame."),
        ("sc24", "s20", "NONE", "The two plain blank books lying closed side by side in warm evening light, calm and settled."),
    ],
    "heroes": {"sc3", "sc9", "sc18", "sc23"}, "wides": {"sc5"},
}
_D = {"sc1", "sc7", "sc14", "sc19", "sc21", "sc22"}
FILM25["clauses"] = {
    "OPEN": (G.OPEN, _D), "NOICON": (G.NOICON, _D), "SHOES": (SHOES, _D),
    "BOOKS": (BOOKS, {"sc2", "sc20", "sc24"}),
    "DOOR": (DOOR, {"sc3", "sc23"}),
    "WALL": (WALL, {"sc4"}),
    "COURT": (COURT, {"sc5"}),
    "CREATURE": (CREATURE, {"sc6"}),
    "MAP": (MAP, {"sc8"}),
    "STONES": (STONES, {"sc9"}),
    "LADDER": (LADDER, {"sc10"}),
    "GRID": (GRID, {"sc11"}),
    "GOOSE": (GOOSE, {"sc12"}),
    "JAR": (JAR, {"sc13"}),
    "GLASSES": (GLASSES, {"sc15"}),
    "PAINT": (PAINT, {"sc16"}),
    "SAW": (SAW, {"sc17"}),
    "FLAT": (FLAT, {"sc18"}),
}

if __name__ == "__main__":
    args = sys.argv[1:]
    if "init" in args:
        G.init(FILM25)
    if "build" in args:
        G.build(FILM25)
    if "sheet" in args:
        G.sheet(FILM25)
