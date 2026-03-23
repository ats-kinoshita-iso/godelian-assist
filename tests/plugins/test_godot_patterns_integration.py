"""Integration tests for the godot-patterns plugin."""

from __future__ import annotations

import json
from pathlib import Path

PLUGIN_DIR = Path(__file__).parent.parent.parent / "plugins" / "godot-patterns"
EXPECTED_SKILLS = ["scene-architecture", "node-composition", "signal-design"]


def _read_skill(skill_name: str) -> str:
    path = PLUGIN_DIR / "skills" / skill_name / "SKILL.md"
    assert path.exists(), f"SKILL.md not found: {skill_name}"
    return path.read_text(encoding="utf-8")


def _body_lines(skill_name: str) -> list[str]:
    content = _read_skill(skill_name)
    lines = content.split("\n")
    marker_count = 0
    body: list[str] = []
    for line in lines:
        if line.strip() == "---":
            marker_count += 1
            continue
        if marker_count >= 2:
            body.append(line)
    return [l for l in body if l.strip()]


class TestGodotPatternsStructure:
    def test_plugin_json_valid(self) -> None:
        data = json.loads(
            (PLUGIN_DIR / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        assert data["name"] == "godot-patterns"
        assert "godot" in data["keywords"]

    def test_all_skills_exist(self) -> None:
        for skill in EXPECTED_SKILLS:
            path = PLUGIN_DIR / "skills" / skill / "SKILL.md"
            assert path.exists(), f"Missing skill: {skill}"

    def test_all_skills_body_depth(self) -> None:
        for skill in EXPECTED_SKILLS:
            lines = _body_lines(skill)
            assert len(lines) >= 10, f"{skill} body too short: {len(lines)} lines"

    def test_scene_architecture_mentions_collision_or_character(self) -> None:
        content = _read_skill("scene-architecture")
        assert "CharacterBody" in content or "CollisionShape" in content

    def test_node_composition_mentions_composition_pattern(self) -> None:
        content = _read_skill("node-composition")
        assert "composition" in content.lower() or "component" in content.lower()

    def test_signal_design_mentions_event_bus_or_signal(self) -> None:
        content = _read_skill("signal-design")
        assert "EventBus" in content or "signal" in content.lower()

    def test_signal_design_mentions_connection_patterns(self) -> None:
        content = _read_skill("signal-design")
        assert "connect" in content.lower()
