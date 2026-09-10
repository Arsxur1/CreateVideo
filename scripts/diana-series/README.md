# Diana series — storybook film pipeline

Source for 43 short animated storybook films made for one eight-year-old. Each film is a
message from Dad, grounded in a specific chapter of a specific book.

| Series | Films | Books |
|---|---|---|
| One | 18 | *Thinking, Fast and Slow* — Daniel Kahneman |
| Two | 25 | *Mindset* — Carol Dweck, and *The 7 Habits of Highly Effective People* — Stephen Covey |

The rendered videos are **not** in this repo. They live under `projects/`, which `.gitignore`
excludes, and the finished set is collected in `projects/Video for Diana/`. This folder is the
source that produces them.

## Layout

```
filmgen.py        the pipeline. Everything below is a data-only spec fed to it.
mindset_a..h.py   series two, films 1-25 (3-5 films per file)
film10..18.py     series one, films 10-18
preflight.py      validate every spec BEFORE an expensive build
legacy/           series one films 1-9, written before filmgen.py existed
```

`filmgen.py` exposes `init(FILM)`, `build(FILM)`, `fix(FILM, prompts)`, `sheet(FILM)` and
`finish(FILM, regens, reason)`. A film spec is a plain dict: research fields, narration
`sections`, illustration `spec`, and `clauses` (see below).

## Running it

Use the repo virtualenv, not a bare `python` — the system interpreter has no `jsonschema`,
so the import fails before any work starts.

```bash
cd scripts/diana-series
PYTHONPATH=/path/to/OpenMontage /path/to/OpenMontage/.venv/Scripts/python.exe preflight.py
PYTHONPATH=/path/to/OpenMontage /path/to/OpenMontage/.venv/Scripts/python.exe mindset_g.py m22 init build
```

`filmgen.py` finds the repo root from its own location. Override with `OPENMONTAGE_ROOT`.
Contact sheets and frame grabs go to `projects/_review/`; override with `DIANA_REVIEW_DIR`.

## The workflow, in order

1. **Ground it in the book.** Read the actual pages. Working from a book's famous structure
   produces films citing chapters nobody read.
2. **Write the spec**, then run `preflight.py`. It catches schema minimums, the two enums, and
   scene/clause coverage in one pass instead of one traceback per build attempt.
3. **`build()`** — artifacts, illustrations, narration, props.
4. **`sheet()` and review every frame against its own spec text.** Not optional. This step has
   caught a distinct defect class in every single batch.
5. **`fix()`** the defective scenes, then re-review.
6. **`finish()`** — render, ffprobe frame-count assertion, encodes, report.

## Rules learned the expensive way

**A prompt clause must describe style only, never the complete object set.** `_prompt()` puts
clause text *before* the scene description, so a clause that enumerates every object silently
overrides any scene needing a subset of them. A clause reading "one blue blob and one yellow
blob, green where they overlap" broke exactly the scenes whose argument is *two identical blues*
or *not touching*. Put medium, drawing style and blanket prohibitions in the clause; put object
identity and count in the scene description, as "exactly ONE x appears and there is no second x
anywhere in the frame". This one mistake produced every defect in three unrelated films at once.

**A clause that mandates an object cannot be overridden by a scene that forbids it.** No amount
of "do NOT draw a pivot" beats a clause saying the device has a pivot. Give that scene its own
clause.

**Reuse callback devices by reference, not by copy** — `DOOR = FILM1["clauses"]["DOOR"][0]`. The
recap film then draws each callback from byte-identical instructions to the film it recalls, and
fixing a clause upstream fixes every callback for free.

**`build()` skips illustrations that already exist but always regenerates narration.** Re-running
it after editing a script therefore produces new words over stale pictures, with no error and no
warning. After changing any scene description in a built film, regenerate those scenes explicitly
with `fix()`.

**Build the timeline from measured audio, never from script estimates.** Every one of the 43
films overshot its own estimate by 30-50 seconds. Anything user-facing that quotes a duration
must read it from the rendered file.

**Never ask an image model for an exact count** of anything a child will count. Draw it in the
composition code, where the count is deterministic.

**Name the anti-pattern rather than describing the target.** "Do NOT draw a smooth cloth ribbon"
worked where more positive description had failed. Likewise, red laced sneakers reliably
hallucinate fake logo lettering no matter how many times you write "no logos" — the fix is to
describe a completely different shoe, breaking the learned association instead of fighting it.

**A diagram can survive the no-lettering rule by putting a picture in each cell.** Covey's
four-quadrant matrix carries fine as a tipped cup, a handbell, a seedling and a tangle of string.
State grid geometry explicitly; image models resist it.

## Constraints these films are built under

No numeral, letter or word appears in any illustration. Exactly one child per frame. No icon
clip-art. Every claim traces to a chapter actually read, and anything cut for being unsuitable
for a child is recorded in that film's `excluded` field rather than dropped silently.
