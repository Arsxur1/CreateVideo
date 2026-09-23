import json

import pytest

from lib import themes
from lib.themes import ThemeError


@pytest.fixture
def dirs(tmp_path):
    themes_dir = tmp_path / "themes"
    projects_dir = tmp_path / "projects"
    (projects_dir / "demo" / "artifacts").mkdir(parents=True)
    return themes_dir, projects_dir


def test_new_theme_fills_defaults_and_lists(dirs) -> None:
    themes_dir, _ = dirs
    themes.save_theme("night", {"description": "dark"}, themes_dir=themes_dir)

    theme = themes.load_theme("night", themes_dir)
    assert theme["palette"]["accent"] == themes.DEFAULT_THEME["palette"]["accent"]
    assert theme["created_at"] and theme["updated_at"]
    assert [t["name"] for t in themes.list_themes(themes_dir)] == ["night"]


def test_save_refuses_to_overwrite_without_force(dirs) -> None:
    themes_dir, _ = dirs
    themes.save_theme("night", {}, themes_dir=themes_dir)
    with pytest.raises(ThemeError, match="already exists"):
        themes.save_theme("night", {}, themes_dir=themes_dir)
    themes.save_theme("night", {"description": "v2"}, force=True, themes_dir=themes_dir)
    assert themes.load_theme("night", themes_dir)["description"] == "v2"


def test_update_sets_nested_values_and_keeps_hex_colours(dirs) -> None:
    themes_dir, _ = dirs
    themes.save_theme("night", {}, themes_dir=themes_dir)

    updated = themes.update_theme("night", ["palette.accent=#12AB34", "captions.size=64", "captions.scrim=false"], themes_dir)

    assert updated["palette"]["accent"] == "#12AB34"
    assert updated["captions"]["size"] == 64
    assert updated["captions"]["scrim"] is False


def test_update_rejects_invalid_values(dirs) -> None:
    themes_dir, _ = dirs
    themes.save_theme("night", {}, themes_dir=themes_dir)
    with pytest.raises(ThemeError, match="palette.accent"):
        themes.update_theme("night", ["palette.accent=orange"], themes_dir)
    with pytest.raises(ThemeError, match="not loadable"):
        themes.update_theme("night", ["fonts.display=ComicSans"], themes_dir)
    # A rejected update leaves the saved theme untouched.
    assert themes.load_theme("night", themes_dir)["palette"]["accent"] == themes.DEFAULT_THEME["palette"]["accent"]


def test_delete_removes_theme(dirs) -> None:
    themes_dir, _ = dirs
    themes.save_theme("night", {}, themes_dir=themes_dir)
    themes.delete_theme("night", themes_dir)
    assert themes.list_themes(themes_dir) == []
    with pytest.raises(ThemeError):
        themes.delete_theme("night", themes_dir)


def test_apply_snapshots_so_later_edits_do_not_change_the_project(dirs) -> None:
    themes_dir, projects_dir = dirs
    themes.save_theme("night", {}, themes_dir=themes_dir)
    out = themes.apply_theme("night", "demo", themes_dir, projects_dir)

    themes.update_theme("night", ["palette.accent=#000000"], themes_dir)

    snapshot = json.loads(out.read_text(encoding="utf-8"))
    assert snapshot["palette"]["accent"] == themes.DEFAULT_THEME["palette"]["accent"]
    assert snapshot["applied_at"]


def test_bad_names_are_rejected(dirs) -> None:
    themes_dir, _ = dirs
    for name in ("Night", "a", "../escape", "has space"):
        with pytest.raises(ThemeError, match="Theme name"):
            themes.save_theme(name, {}, themes_dir=themes_dir)


def test_cli_delete_needs_confirmation(dirs, monkeypatch, capsys) -> None:
    themes_dir, _ = dirs
    monkeypatch.setattr(themes, "THEMES_DIR", themes_dir)
    themes.save_theme("night", {}, themes_dir=themes_dir)

    assert themes.main(["delete", "night"]) == 2
    assert "--yes" in capsys.readouterr().err
    assert themes.main(["delete", "night", "--yes"]) == 0
    assert themes.list_themes(themes_dir) == []
