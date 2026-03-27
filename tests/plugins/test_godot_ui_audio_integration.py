"""Integration tests for godot-ui and godot-audio plugins, and expanded game-design skills."""

from __future__ import annotations

import json
from pathlib import Path

PLUGINS_DIR = Path(__file__).parent.parent.parent / "plugins"
UI_DIR = PLUGINS_DIR / "godot-ui"
AUDIO_DIR = PLUGINS_DIR / "godot-audio"
GAME_DESIGN_DIR = PLUGINS_DIR / "game-design"


def _read_skill(plugin_dir: Path, skill_name: str) -> str:
    path = plugin_dir / "skills" / skill_name / "SKILL.md"
    assert path.exists(), f"SKILL.md not found: {plugin_dir.name}/{skill_name}"
    return path.read_text(encoding="utf-8")


def _body_lines(plugin_dir: Path, skill_name: str) -> list[str]:
    content = _read_skill(plugin_dir, skill_name)
    marker_count = 0
    body: list[str] = []
    for line in content.split("\n"):
        if line.strip() == "---":
            marker_count += 1
            continue
        if marker_count >= 2:
            body.append(line)
    return [ln for ln in body if ln.strip()]


# --- godot-ui ---

class TestGodotUIStructure:
    def test_plugin_json_valid(self) -> None:
        data = json.loads(
            (UI_DIR / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        assert data["name"] == "godot-ui"
        assert data["license"] == "MIT"

    def test_all_skills_exist(self) -> None:
        for skill in ["hud-design", "menu-design", "theme-system", "ui-signals"]:
            assert (UI_DIR / "skills" / skill / "SKILL.md").exists()


class TestHudDesignSkill:
    def test_body_depth(self) -> None:
        assert len(_body_lines(UI_DIR, "hud-design")) >= 15

    def test_mentions_canvas_layer(self) -> None:
        assert "CanvasLayer" in _read_skill(UI_DIR, "hud-design")

    def test_mentions_texture_progress_bar(self) -> None:
        assert "TextureProgressBar" in _read_skill(UI_DIR, "hud-design")


class TestMenuDesignSkill:
    def test_body_depth(self) -> None:
        assert len(_body_lines(UI_DIR, "menu-design")) >= 15

    def test_mentions_tree_paused(self) -> None:
        content = _read_skill(UI_DIR, "menu-design")
        assert "get_tree().paused" in content or "paused" in content

    def test_mentions_focus_mode(self) -> None:
        content = _read_skill(UI_DIR, "menu-design")
        assert "focus" in content.lower() or "FocusMode" in content


class TestThemeSystemSkill:
    def test_body_depth(self) -> None:
        assert len(_body_lines(UI_DIR, "theme-system")) >= 15

    def test_mentions_theme_resource(self) -> None:
        content = _read_skill(UI_DIR, "theme-system")
        assert "Theme" in content


class TestUISignalsSkill:
    def test_body_depth(self) -> None:
        assert len(_body_lines(UI_DIR, "ui-signals")) >= 15

    def test_mentions_eventbus(self) -> None:
        assert "EventBus" in _read_skill(UI_DIR, "ui-signals")


# --- godot-audio ---

class TestGodotAudioStructure:
    def test_plugin_json_valid(self) -> None:
        data = json.loads(
            (AUDIO_DIR / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        assert data["name"] == "godot-audio"
        assert data["license"] == "MIT"

    def test_all_skills_exist(self) -> None:
        for skill in ["audio-architecture", "adaptive-music", "sfx-patterns"]:
            assert (AUDIO_DIR / "skills" / skill / "SKILL.md").exists()


class TestAudioArchitectureSkill:
    def test_body_depth(self) -> None:
        assert len(_body_lines(AUDIO_DIR, "audio-architecture")) >= 15

    def test_mentions_bus_structure(self) -> None:
        content = _read_skill(AUDIO_DIR, "audio-architecture")
        assert "bus" in content.lower() and ("Master" in content or "Music" in content)


class TestAdaptiveMusicSkill:
    def test_body_depth(self) -> None:
        assert len(_body_lines(AUDIO_DIR, "adaptive-music")) >= 15

    def test_mentions_state_machine(self) -> None:
        content = _read_skill(AUDIO_DIR, "adaptive-music")
        assert "state" in content.lower() and ("machine" in content.lower() or "State" in content)

    def test_mentions_transitions(self) -> None:
        content = _read_skill(AUDIO_DIR, "adaptive-music")
        assert "crossfade" in content.lower() or "transition" in content.lower()


class TestSfxPatternsSkill:
    def test_body_depth(self) -> None:
        assert len(_body_lines(AUDIO_DIR, "sfx-patterns")) >= 15


# --- game-design expanded skills ---

class TestCombatDesignSkill:
    def test_body_depth(self) -> None:
        assert len(_body_lines(GAME_DESIGN_DIR, "combat-design")) >= 20

    def test_contains_attack_data_schema(self) -> None:
        assert "AttackData" in _read_skill(GAME_DESIGN_DIR, "combat-design")

    def test_has_typed_gdscript(self) -> None:
        content = _read_skill(GAME_DESIGN_DIR, "combat-design")
        assert "class_name" in content and "extends" in content


class TestInventoryDesignSkill:
    def test_body_depth(self) -> None:
        assert len(_body_lines(GAME_DESIGN_DIR, "inventory-design")) >= 18

    def test_contains_item_data_schema(self) -> None:
        assert "ItemData" in _read_skill(GAME_DESIGN_DIR, "inventory-design")


class TestEnemyDesignSkill:
    def test_mentions_navigation_agent(self) -> None:
        assert "NavigationAgent3D" in _read_skill(GAME_DESIGN_DIR, "enemy-design")

    def test_mentions_state_machine(self) -> None:
        content = _read_skill(GAME_DESIGN_DIR, "enemy-design")
        assert "state machine" in content.lower() or "StateMachine" in content


class TestProgressionDesignSkill:
    def test_mentions_curve_resource(self) -> None:
        content = _read_skill(GAME_DESIGN_DIR, "progression-design")
        assert "Curve" in content
