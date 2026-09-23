"""Channel themes: a saved look (palette, fonts, captions, motion, audio, voice).

A theme lets a series of videos share one identity. Each video either applies
a saved theme or goes fresh (atelier). Applying a theme copies a snapshot into
the project (``artifacts/theme.json``), so editing or deleting the theme later
never changes a video that was already made.

Themes live in ``themes/<name>.yaml`` (personal, gitignored).

CLI::

    python -m lib.themes list
    python -m lib.themes show <name>
    python -m lib.themes new <name> [--description TEXT]
    python -m lib.themes save <name> --from-project <slug> | --from-file <path> [--force]
    python -m lib.themes update <name> --set palette.accent=#FFB547 [--set captions.size=60 ...]
    python -m lib.themes delete <name> --yes
    python -m lib.themes apply <name> --project <slug>
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import jsonschema
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
THEMES_DIR = REPO_ROOT / "themes"
PROJECTS_DIR = REPO_ROOT / "projects"
SCHEMA_PATH = REPO_ROOT / "schemas" / "styles" / "theme.schema.json"
NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{1,48}$")

# Fonts the review-reel template can load. Adding one means adding a static
# import in templates/review-reel/fonts.ts as well.
TEMPLATE_FONTS = (
    "BricolageGrotesque", "Manrope", "Outfit", "Sora", "SpaceGrotesk", "PlusJakartaSans",
    "Anton", "Syne", "Unbounded", "InstrumentSerif", "Fraunces", "DMSerifDisplay",
)

DEFAULT_THEME: dict[str, Any] = {
    "version": "1.0",
    "name": "",
    "description": "",
    "palette": {"background": "#07080A", "text": "#F2EEE4", "muted": "#9A968C", "accent": "#FFB547"},
    "fonts": {"display": "BricolageGrotesque", "text": "Manrope"},
    "captions": {"size": 58, "weight": 800, "top": 1340, "left": 90, "right": 150, "max_chars": 52, "scrim": True},
    "tags": {"size": 56},
    "motion": {"spring_damping": 18, "whip_frames": 4, "vignette": True},
    "signature": {"open": "aperture", "close": "aperture"},
    "intro": {"cover_seconds": 0.0},
    "audio": {"music_volume": 0.16, "music_ducked_volume": 0.07, "loudness_lufs": -14, "sfx": True},
    "voice": {"provider": "fish_audio", "model": "s2.1-pro-free", "reference_id": "", "temperature": 0.9,
              "tempo": 1.06, "gap_seconds": 0.35, "lead_seconds": 0.4},
}


class ThemeError(Exception):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _path(name: str, themes_dir: Path | None = None) -> Path:
    if not NAME_PATTERN.match(name):
        raise ThemeError(f"Theme name {name!r} must be lowercase letters, digits and dashes (2-49 chars).")
    return (themes_dir or THEMES_DIR) / f"{name}.yaml"


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def validate_theme(theme: dict[str, Any]) -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    try:
        jsonschema.validate(theme, schema)
    except jsonschema.ValidationError as exc:
        where = ".".join(str(p) for p in exc.absolute_path) or "(root)"
        raise ThemeError(f"Invalid theme at {where}: {exc.message}") from exc
    for role, font in theme["fonts"].items():
        if font not in TEMPLATE_FONTS:
            raise ThemeError(f"fonts.{role}={font!r} is not loadable by the template. Choose one of: {', '.join(TEMPLATE_FONTS)}")


def list_themes(themes_dir: Path | None = None) -> list[dict[str, Any]]:
    root = themes_dir or THEMES_DIR
    if not root.exists():
        return []
    out = []
    for path in sorted(root.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        out.append({"name": data.get("name", path.stem), "description": data.get("description", ""),
                    "updated_at": data.get("updated_at", "")})
    return out


def load_theme(name: str, themes_dir: Path | None = None) -> dict[str, Any]:
    path = _path(name, themes_dir)
    if not path.exists():
        raise ThemeError(f"No theme named {name!r}. Run `python -m lib.themes list`.")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def save_theme(name: str, data: dict[str, Any], *, force: bool = False, themes_dir: Path | None = None) -> Path:
    path = _path(name, themes_dir)
    if path.exists() and not force:
        raise ThemeError(f"Theme {name!r} already exists. Use `update`, or `save --force` to replace it.")
    theme = _deep_merge(DEFAULT_THEME, data)
    theme["name"] = name
    theme.setdefault("created_at", _now())
    if path.exists():
        theme["created_at"] = (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("created_at", theme["created_at"])
    theme["updated_at"] = _now()
    validate_theme(theme)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(theme, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return path


def _parse_value(raw: str) -> Any:
    try:
        return yaml.safe_load(raw)
    except yaml.YAMLError:
        return raw


def update_theme(name: str, assignments: list[str], themes_dir: Path | None = None) -> dict[str, Any]:
    theme = load_theme(name, themes_dir)
    for item in assignments:
        key, sep, raw = item.partition("=")
        if not sep:
            raise ThemeError(f"--set expects key=value, got {item!r}")
        node = theme
        parts = key.strip().split(".")
        for part in parts[:-1]:
            node = node.setdefault(part, {})
            if not isinstance(node, dict):
                raise ThemeError(f"{key}: {part!r} is not a section")
        # Hex colours start with '#', which YAML reads as a comment.
        node[parts[-1]] = raw if raw.startswith("#") else _parse_value(raw)
    save_theme(name, theme, force=True, themes_dir=themes_dir)
    return load_theme(name, themes_dir)


def delete_theme(name: str, themes_dir: Path | None = None) -> None:
    path = _path(name, themes_dir)
    if not path.exists():
        raise ThemeError(f"No theme named {name!r}.")
    path.unlink()


def apply_theme(name: str, project: str, themes_dir: Path | None = None, projects_dir: Path | None = None) -> Path:
    """Snapshot the theme into projects/<project>/artifacts/theme.json."""
    theme = load_theme(name, themes_dir)
    art = (projects_dir or PROJECTS_DIR) / project / "artifacts"
    if not art.parent.exists():
        raise ThemeError(f"Project {project!r} not found under projects/.")
    art.mkdir(parents=True, exist_ok=True)
    snapshot = dict(theme, applied_at=_now())
    out = art / "theme.json"
    out.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m lib.themes", description="Manage channel themes.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    p = sub.add_parser("show"); p.add_argument("name")
    p = sub.add_parser("new"); p.add_argument("name"); p.add_argument("--description", default="")
    p = sub.add_parser("save"); p.add_argument("name"); p.add_argument("--from-project"); p.add_argument("--from-file")
    p.add_argument("--force", action="store_true"); p.add_argument("--description")
    p = sub.add_parser("update"); p.add_argument("name"); p.add_argument("--set", action="append", default=[], dest="sets")
    p = sub.add_parser("delete"); p.add_argument("name"); p.add_argument("--yes", action="store_true")
    p = sub.add_parser("apply"); p.add_argument("name"); p.add_argument("--project", required=True)
    args = ap.parse_args(argv)

    try:
        if args.cmd == "list":
            rows = list_themes()
            if not rows:
                print("No themes yet. Create one with `python -m lib.themes new <name>`.")
            for r in rows:
                print(f"{r['name']:<24} {r['updated_at'][:10]:<11} {r['description']}")
        elif args.cmd == "show":
            print(yaml.safe_dump(load_theme(args.name), sort_keys=False, allow_unicode=True))
        elif args.cmd == "new":
            print(save_theme(args.name, {"description": args.description}))
        elif args.cmd == "save":
            if bool(args.from_project) == bool(args.from_file):
                raise ThemeError("Give exactly one of --from-project or --from-file.")
            if args.from_project:
                src = PROJECTS_DIR / args.from_project / "artifacts" / "theme.json"
                if not src.exists():
                    raise ThemeError(f"{src} not found. The project has no theme snapshot to save.")
                data = json.loads(src.read_text(encoding="utf-8"))
            else:
                data = yaml.safe_load(Path(args.from_file).read_text(encoding="utf-8"))
            for k in ("name", "created_at", "updated_at", "applied_at"):
                data.pop(k, None)
            if args.description:
                data["description"] = args.description
            print(save_theme(args.name, data, force=args.force))
        elif args.cmd == "update":
            if not args.sets:
                raise ThemeError("Nothing to update. Pass one or more --set key=value.")
            update_theme(args.name, args.sets)
            print(f"updated {args.name}")
        elif args.cmd == "delete":
            if not args.yes:
                raise ThemeError(f"Deleting {args.name!r} cannot be undone. Re-run with --yes to confirm.")
            delete_theme(args.name)
            print(f"deleted {args.name}")
        elif args.cmd == "apply":
            print(apply_theme(args.name, args.project))
    except ThemeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
