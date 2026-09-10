"""Validate every film spec in this folder BEFORE running an expensive build.

Catches the failure classes that otherwise surface as a jsonschema traceback minutes into
image generation, or as a SystemExit part way through a build:

  * schema minItems  - research_brief and proposal_packet have minimums that a sparse film misses
  * the two enums    - angle type and narrative_structure are different sets and easily swapped
  * scene coverage   - every section needs a scene, and every scene needs a prompt clause

Run it from this directory:
    PYTHONPATH=<repo root> python preflight.py
"""
import importlib
import sys
from pathlib import Path

ANGLE_TYPES = {"trending", "evergreen", "contrarian", "narrative", "data_driven"}
NARRATIVE_STRUCTURES = {
    "analogy", "problem_solution", "journey", "debate", "myth_busting",
    "timeline", "comparison", "tutorial", "story", "data_narrative",
}
# key -> schema minItems
MIN_ITEMS = {
    "existing": 3, "gaps": 1, "data_points": 3,
    "questions": 3, "angles": 3, "concepts": 3,
}


def load_films():
    """Import every film module beside this file and return {label: film_dict}."""
    here = Path(__file__).resolve().parent
    sys.path.insert(0, str(here))
    films, seen = {}, set()
    for path in sorted(here.glob("*.py")):
        if path.stem in ("preflight", "filmgen"):
            continue
        module = importlib.import_module(path.stem)
        for name in dir(module):
            if not name.startswith("FILM"):
                continue
            film = getattr(module, name)
            if not (isinstance(film, dict) and "clauses" in film and "spec" in film):
                continue
            # A module that reuses another film clause text imports that film too, so the
            # same dict shows up under several modules. Count it once, where it is defined.
            if id(film) in seen:
                continue
            seen.add(id(film))
            films["%s.%s" % (path.stem, name)] = film
    return films


def check(label, film):
    problems = []

    def want(cond, msg):
        if not cond:
            problems.append("%s: %s" % (label, msg))

    for key, minimum in MIN_ITEMS.items():
        got = len(film.get(key, []))
        want(got >= minimum, "%s has %d entries, schema needs %d" % (key, got, minimum))
    for angle in film.get("angles", []):
        want(angle[1] in ANGLE_TYPES, "angle type %r is not an angle type" % (angle[1],))
    for concept in film.get("concepts", []):
        want(concept["narrative_structure"] in NARRATIVE_STRUCTURES,
             "narrative_structure %r is not valid" % (concept["narrative_structure"],))
        want(len(concept.get("key_points", [])) >= 2,
             "concept %s has under 2 key_points" % (concept.get("id"),))

    scene_ids = {s[0] for s in film["spec"]}
    section_ids = {s[0] for s in film["sections"]}
    for scene in film["spec"]:
        want(scene[1] in section_ids, "scene %s points at unknown section %s" % (scene[0], scene[1]))
    covered = set()
    for _text, members in film["clauses"].values():
        covered |= members
    want(not (covered - scene_ids), "clause members not in spec: %s" % sorted(covered - scene_ids))
    want(not (scene_ids - covered), "scenes in no clause set: %s" % sorted(scene_ids - covered))
    for key in ("heroes", "wides"):
        stray = film.get(key, set()) - scene_ids
        want(not stray, "%s not in spec: %s" % (key, sorted(stray)))
    return problems


def main():
    films = load_films()
    failures = []
    for label in sorted(films):
        film = films[label]
        problems = check(label, film)
        failures.extend(problems)
        print("%-24s %-42s %2d sections %2d scenes  %s" % (
            label, film.get("title", "?"), len(film["sections"]), len(film["spec"]),
            "OK" if not problems else "FAIL"))
    print("\n%d films checked" % len(films))
    if failures:
        print("\n%d problems:" % len(failures))
        for f in failures:
            print("  " + f)
        return 1
    print("PREFLIGHT OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
