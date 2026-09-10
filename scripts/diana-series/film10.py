"""Film 10: Two Is Not Enough (law of small numbers, Ch 10)."""
import sys
import filmgen as G

DL = "https://thedecisionlab.com/biases"

FILM = {
    "slug": "diana-small-numbers", "comp_id": "DianaSmallNumbers",
    "title": "Two Is Not Enough", "position": "10 of 18", "chapters": "Ch 10",
    "source_url": DL, "source_title": "Cognitive Biases - The Decision Lab",
    "topic": "The law of small numbers, told for an 8-year-old as why two examples feel like proof",
    "summary": ("Film 10 of the series. Chapter 10. Small samples produce extreme results far more often than "
                "large ones, yet people treat a result drawn from a handful of cases as though it described the "
                "whole. Worse, a small sample that comes out all one way produces a tidier story and therefore "
                "feels more convincing, not less. For a child this is the machinery behind always, never, and "
                "deciding what she is bad at after two attempts."),
    "existing": [
        {"title": "Jane the Brain (NIMH)", "url": G.NIMH, "source": "government site",
         "angle": "Coping with big feelings", "what_it_covers": "Feelings, not how much evidence a belief rests on"},
        {"title": "Growth-mindset material for children", "url": G.SCH, "source": "web",
         "angle": "Keep trying, you can improve",
         "what_it_covers": "Tells a child to persist without explaining why two attempts told her nothing"},
        {"title": "Cognitive Biases - The Decision Lab", "url": DL, "source": "reference site",
         "angle": "Adult reference explainer", "what_it_covers": "Sample size through polling and research framings"}],
    "saturated": ["Growth mindset and keep-trying encouragement",
                  "Adult polling, statistics and research-design framings"],
    "gaps": ["Telling a child that two examples is a measurement problem, not a fact about her",
             "Explaining why a small all-one-way sample feels more convincing rather than less",
             "Giving her a countable question, how many times, instead of an attitude"],
    "data_points": [
        ("Small samples yield extreme outcomes far more often than large ones, so results from few cases are unreliable.",
         DL, "Thinking, Fast and Slow, Ch 10", "secondary_source", "surprising", "the jar and the small spoon"),
        ("People have far more faith in small samples than is warranted, and read cause into what is only chance.",
         G.SN, "Thinking, Fast and Slow, Ch 10", "secondary_source", "counterintuitive",
         "why two unkind children become an unkind school"),
        ("A tidy, coherent result feels more convincing than a messy one, independently of how much evidence sits behind it.",
         G.SN, "Thinking, Fast and Slow, Ch 7 and 10", "secondary_source", "counterintuitive",
         "why the all-red spoonful is the most persuasive picture in the film"),
        ("By age 8 to 9 children can apply an explicit self-directed question to their own reasoning.",
         G.PQ, "Pennequin et al., British Journal of Educational Psychology (2020)", "primary_source",
         "expected", "the how-many-times tool")],
    "knowledge_level": ("Age 8. Has seen films 1 to 9 and owns the fast one, the story machine, the memory shelf, "
                        "separate boxes, the bouncing dot, remember-do-not-guess, protect-the-ending, the see-saw "
                        "and the anchor."),
    "questions": ["Why do I decide I am bad at something after trying twice?",
                  "Why does one bad experience make a whole place feel bad?",
                  "How many times do I need before I actually know?"],
    "misconceptions": [
        ("If it happened twice, that is what it is like", "Two cases is a tiny sample and tiny samples swing wildly.", "Ch 10"),
        ("A clear, all-one-way result is stronger evidence", "A tidy small result is more persuasive but no more informative.", "Ch 7 and 10"),
        ("Not being sure means I am wrong", "Not yet knowing is a separate state from being wrong.", "Ch 10 corrective")],
    "pain_points": ["Writing herself off after two attempts",
                    "Being told to be positive rather than being told her evidence was thin"],
    "angles": [
        ("The Jar and the Little Spoon", "narrative",
         "Dip a tiny spoon into a mixed jar and you can easily come up all red. The jar is still mixed.",
         "A jar of marbles is physical and immediate, and it removes any need to count.", ["Ch 10 sample size"]),
        ("How Many Times?", "evergreen", "When you say always or never, ask how many times.",
         "Turns an abstract statistical idea into one countable question a child can actually ask.", ["Ch 10 corrective"]),
        ("Tidy Is Not True", "contrarian", "A small spoonful that comes out all one colour is the most convincing picture of all.",
         "Explains why her thin evidence feels strongest, which nothing else in the children's landscape does.",
         ["Ch 7 WYSIATI", "Ch 10"])],
    "kahneman": "People place far too much faith in results drawn from small samples, and read cause into chance.",
    "excluded": ["The hot-hand and cancer-map research examples, which need statistics.",
                 "Anything from the priming or ego-depletion chapters."],
    "concepts": [
        {"id": "c1", "title": "Two Is Not Enough",
         "hook": "Two children were unkind to you. So now the whole school is unkind.",
         "narrative_structure": "story",
         "visual_approach": "A large glass jar of mixed red and blue marbles, a tiny wooden spoon and a big wooden ladle on empty cream paper.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 150,
         "key_points": ["Small samples swing wildly", "The jar stays mixed", "Your brain sees the result, not the spoon",
                        "A tidy small result feels strongest", "Ask how many times, then say not yet"],
         "core_message": "Two times is a tiny spoon. You are allowed to not know yet.",
         "cta": "When you catch yourself saying always or never, ask how many times.",
         "tone": "Warm and steadying.",
         "why_this_works": "It reframes a harsh self-judgement as a measurement problem she can fix.",
         "grounded_in": ["Ch 10"]},
        {"id": "c2", "title": "How Many Times?", "hook": "Ask the number before you believe the sentence.",
         "narrative_structure": "tutorial", "visual_approach": "A tiny spoon alone on the page.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 95,
         "key_points": ["Notice always and never", "Ask the count", "Hold off"],
         "core_message": "Ask the number.", "cta": "Ask how many times.", "tone": "Practical",
         "why_this_works": "The actionable core, but no explanation behind it, so it becomes the payoff of c1.",
         "grounded_in": ["Ch 10 corrective"]},
        {"id": "c3", "title": "Tidy Is Not True", "hook": "The neatest answer is often the thinnest one.",
         "narrative_structure": "comparison", "visual_approach": "A glowing all-red spoonful beside a dull mixed ladleful.",
         "suggested_playbook": "custom-atelier-storybook", "target_audience": "The same 8-year-old",
         "target_platform": "generic", "target_duration_seconds": 105,
         "key_points": ["Coherence is not evidence", "Messy is often truer", "Distrust the tidy result"],
         "core_message": "Tidy is not true.", "cta": "Distrust the neat answer.", "tone": "Wry",
         "why_this_works": "The sharpest idea here, but it lands only after the jar is established, so it becomes the middle of c1.",
         "grounded_in": ["Ch 7", "Ch 10"]}],
    "rationale": ("c1 opens on a real hurt she has felt, converts it into a jar she can picture, and only then "
                  "delivers the tidy-is-not-true twist and the counting tool. The others are its middle and its end."),
    "device_short": "the jar of mixed marbles with a tiny spoon and a big ladle",
    "art_direction": ("Series house style. New device: a large glass jar of mixed red and blue marbles, a tiny wooden "
                      "spoon and a big wooden ladle, on otherwise empty cream paper. Nothing is ever counted."),
    "device_lock": ("A large plain glass jar of small marbles in two colours only, warm red and soft blue, clearly "
                    "mixed. A tiny plain wooden spoon is a small sample; a large plain wooden ladle is a big one. "
                    "No quantity is ever shown as a countable number."),
    "anti_patterns": ["asking the image model for an exact count of marbles or people",
                      "two children in one frame", "numerals, labels or lettering of any kind",
                      "implying she should simply think positively", "a fully painted background"],
    "tradeoffs": [
        {"tradeoff": "Showing two marbles versus showing a small spoon",
         "recommendation": "A small spoon",
         "quality_impact": "The image model cannot be trusted with an exact count. A spoon carries small sample with no counting at all."},
        {"tradeoff": "Ending on you are wrong versus you do not know yet",
         "recommendation": "You do not know yet",
         "quality_impact": "Chapter 10 is about insufficient evidence, not error. Not yet is both accurate and kinder."}],
    "delivery_style": "warm parent reading a bedtime story, steadying rather than corrective",
    "performance_intent": ("The same parent and child, nine chapters on. This one takes a harsh verdict she has "
                           "passed on herself and shows it rests on almost nothing."),
    "energy_curve": ("Quiet and careful at the school. Curious through the jar. Wry at tidy is not true. Bright at "
                     "the tools. Gentle and freeing at the close."),
    "pause_policy": "Three genuine silences: after the whole school is unkind, after think of something you decided, and after not yet.",
    "sample_section": "s15",
    "human_note": "The last line should sound like permission, not instruction.",
    "reading_age": "Written for a listener of 8. Sample size, law of small numbers and variance never appear as terms.",
    "pause_beats": [{"section": "s1", "purpose": "She recognises the feeling before it is questioned"},
                    {"section": "s8", "purpose": "She retrieves a real verdict she has passed on herself"},
                    {"section": "s14", "purpose": "She tries saying not yet about it"}],
    "grounded_in": {"s1_to_s2": "Ch 10, generalising from a handful of cases",
                    "s3_to_s7": "Ch 10, small samples yield extreme results and the sample size goes unnoticed",
                    "s8_to_s11": "Ch 10 applied to her own self-judgements",
                    "s12": "Ch 7 and 10, coherence feels like evidence",
                    "s13_to_s15": "Ch 10 corrective plus Pennequin on self-directed questioning at 8 to 9"},
    "guardrails": ["The film never tells her the school is fine or that she should be positive; it says only that she does not yet know.",
                   "No exact quantity appears in any illustration.",
                   "Not knowing yet is distinguished explicitly from being wrong.",
                   "No priming or ego-depletion material."],
    "sections": [
        ("s1", "The school", "Two children at the big school were unkind to you. And now the whole school is unkind.",
         'Two children at the big school were unkind to you. <break time="0.5s"/> And now the whole school is unkind. <break time="2.5s"/>',
         2.5, "slow", "gentle", ["whole"], "Pause beat one. Say it as she would say it, without judgement."),
        ("s2", "Out of hundreds", "But you have met two people. Out of hundreds and hundreds.",
         'But you have met two people. <break time="0.5s"/> Out of hundreds and hundreds.',
         1.4, "measured", "steady", ["two"], "Plain."),
        ("s3", "The jar", "So picture a big glass jar, filled right up with marbles. Half of them red, half of them blue, all mixed together.",
         'So picture a big glass jar, filled right up with marbles. <break time="0.5s"/> Half of them red, half of them blue, <break time="0.4s"/> all mixed together.',
         1.4, "measured", "warm", ["mixed"], "Picture-building."),
        ("s4", "The little spoon", "Now dip in a tiny little spoon. Just once. You might easily come up with nothing but red.",
         'Now dip in a tiny little spoon. <break time="0.4s"/> Just once. <break time="0.5s"/> You might easily come up with nothing but red.',
         1.4, "measured", "curious", ["easily"], "Light and quick."),
        ("s5", "Is the jar red", "Does that mean the jar is red? Of course not. The jar is mixed. Your spoon was just small.",
         'Does that mean the jar is red? <break time="0.5s"/> Of course not. <break time="0.4s"/> The jar is mixed. <break time="0.4s"/> Your spoon was just small.',
         1.4, "measured", "steady", ["small"], "Firm and clear."),
        ("s6", "Small spoons", "Small spoons give silly answers far more often than big ones do. That is just how spoons work.",
         'Small spoons give silly answers far more often than big ones do. <break time="0.5s"/> That is just how spoons work.',
         1.4, "measured", "steady", ["far more often"], "Matter of fact."),
        ("s7", "Only the result", "But here is the thing. Your brain never looks at the spoon. It only looks at what came out of it.",
         'But here is the thing. <break time="0.5s"/> Your brain never looks at the spoon. <break time="0.5s"/> It only looks at what came out of it.',
         1.4, "slow", "curious", ["spoon"], "The hinge."),
        ("s8", "Your own", "So have a think. What have you decided about yourself, from only one or two times?",
         'So have a think. <break time="0.5s"/> What have you decided about yourself, <break time="0.4s"/> from only one or two times? <break time="2.5s"/>',
         2.5, "slow", "gentle", ["decided"], "Pause beat two. She needs a real example of her own."),
        ("s9", "Rubbish at", "I am rubbish at swimming. How many times, though? Twice?",
         'I am rubbish at swimming. <break time="0.5s"/> How many times, though? <break time="0.4s"/> Twice?',
         1.4, "measured", "warm", ["twice"], "Gently teasing."),
        ("s10", "Always out", "That shop is always out of milk. How many visits was that?",
         'That shop is always out of milk. <break time="0.5s"/> How many visits was that?',
         1.4, "measured", "wry", ["always"], "Everyday."),
        ("s11", "A tiny spoon", "Two times is a tiny spoon.",
         'Two times is a tiny spoon.',
         1.4, "slow", "steady", ["tiny"], "Let it sit alone."),
        ("s12", "Tidy feels true", "And here is the sneaky bit. A small spoonful that comes out all one colour feels more convincing, not less. Because it makes such a tidy little story.",
         'And here is the sneaky bit. <break time="0.5s"/> A small spoonful that comes out all one colour feels more convincing, <break time="0.3s"/> not less. <break time="0.5s"/> Because it makes such a tidy little story.',
         1.4, "measured", "wry", ["more"], "Link back to the story machine."),
        ("s13", "The first tool", "So here is your tenth trick. When you hear yourself say always, or never, stop and ask. How many times?",
         'So here is your tenth trick. <break time="0.5s"/> When you hear yourself say always, <break time="0.3s"/> or never, <break time="0.4s"/> stop and ask. <break time="0.4s"/> How many times?',
         1.4, "measured", "encouraging", ["how many"], "Bright."),
        ("s14", "The second tool", "And if the answer is once, or twice, you do not have to decide anything at all. You can just say, not yet.",
         'And if the answer is once, <break time="0.3s"/> or twice, <break time="0.5s"/> you do not have to decide anything at all. <break time="0.5s"/> You can just say, not yet. <break time="2.5s"/>',
         2.5, "measured", "encouraging", ["not yet"], "Pause beat three. She should try it on her own example."),
        ("s15", "Landing", "Not yet is a perfectly good answer. Not knowing yet is not the same thing as being wrong.",
         'Not yet is a perfectly good answer. <break time="0.5s"/> Not knowing yet is not the same thing as being wrong.',
         0.0, "slow", "tender", ["not the same"], "Warm permission. End soft, then stop."),
    ],
    "spec": [
        ("sc1", "s1", "DIANA", "The girl stands alone with her arms at her sides and her eyes lowered, subdued and quiet."),
        ("sc2", "s1", "NONE", "One simple school building drawn small in the middle of the page with a single grey cloud hanging above it."),
        ("sc3", "s2", "NONE", "A wide band of many tiny simple pale silhouettes of people stretching right across the page, with only a very small cluster at one end tinted grey."),
        ("sc4", "s3", "NONE", "A large glass jar filled right to the top with small round marbles in warm red and soft blue, thoroughly mixed together, standing in the middle of the page."),
        ("sc5", "s4", "NONE", "A tiny wooden spoon lifted just clear of the top of the jar, and every marble sitting on the spoon is warm red."),
        ("sc6", "s5", "NONE", "The same large glass jar, seen close, with its marbles obviously and thoroughly mixed between warm red and soft blue."),
        ("sc7", "s5", "NONE", "A tiny wooden spoon holding only red marbles, drawn very small on the left, beside the large mixed glass jar on the right."),
        ("sc8", "s6", "NONE", "One tiny wooden spoon and one large wooden ladle lying side by side in the middle of the page, both completely empty."),
        ("sc9", "s7", "NONE", "A small cluster of warm red marbles floating alone in the middle of the page, with the tiny wooden spoon beneath them drawn so faintly it is almost invisible."),
        ("sc10", "s8", "DIANA", "The girl sits with her chin resting on her hand, thinking, looking off to one side."),
        ("sc11", "s9", "DIANA", "The girl stands at the edge of a swimming pool in a swimming costume, arms folded, looking doubtful."),
        ("sc12", "s10", "NONE", "One plain wooden shop shelf drawn across the middle of the page with a single empty gap in the row of simple bottles on it."),
        ("sc13", "s11", "NONE", "One tiny wooden spoon drawn very small and alone in the very middle of a large empty page."),
        ("sc14", "s12", "NONE", "A tiny wooden spoonful of marbles that are all warm red, glowing softly and looking neat and satisfying."),
        ("sc15", "s12", "NONE", "On the left a small glowing spoonful of all red marbles; on the right a large dull ladleful of obviously mixed red and blue marbles."),
        ("sc16", "s13", "DIANA", "The girl stops with one hand half raised and her mouth just open, catching herself mid-sentence."),
        ("sc17", "s14", "NONE", "A large wooden ladle being lowered deep down into the large glass jar of mixed marbles."),
        ("sc18", "s15", "DIANA", "The girl stands relaxed and open with a small calm smile, unhurried, in warm light."),
    ],
    "heroes": {"sc5", "sc7", "sc13", "sc15", "sc18"},
    "wides": {"sc3", "sc8", "sc15"},
}

JAR = ("The jar is a large plain round glass jar filled with small round marbles in two colours only, warm red and "
       "soft blue. Draw it simply from the side. Do not label it and do not draw any numbers.")
SPOON = ("The spoon is a small plain wooden spoon and the ladle is a large plain wooden ladle, both drawn simply "
         "from the side with no markings, no writing and no measuring marks of any kind.")

FILM["clauses"] = {
    "OPEN": (G.OPEN, {"sc1", "sc2", "sc3", "sc10", "sc11", "sc12", "sc16", "sc18"}),
    "NOICON": (G.NOICON, {"sc1", "sc2", "sc3", "sc10", "sc12", "sc16"}),
    "JAR": (JAR, {"sc4", "sc5", "sc6", "sc7", "sc15", "sc17"}),
    "SPOON": (SPOON, {"sc5", "sc7", "sc8", "sc9", "sc13", "sc14", "sc15", "sc17"}),
}

if __name__ == "__main__":
    if "init" in sys.argv:
        G.init(FILM)
    if "build" in sys.argv:
        G.build(FILM)
    if "sheet" in sys.argv:
        G.sheet(FILM)
