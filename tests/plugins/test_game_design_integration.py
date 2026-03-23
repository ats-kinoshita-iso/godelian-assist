"""Integration tests for the game-design plugin."""

from __future__ import annotations

import json
from pathlib import Path

PLUGIN_DIR = Path(__file__).parent.parent.parent / "plugins" / "game-design"
EXPECTED_SKILLS = ["systems-design", "game-loop", "balance-design"]


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


class TestGameDesignStructure:
    def test_plugin_json_valid(self) -> None:
        data = json.loads(
            (PLUGIN_DIR / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        assert data["name"] == "game-design"
        assert "action-rpg" in data["keywords"] or "game-design" in data["keywords"]

    def test_all_skills_exist(self) -> None:
        for skill in EXPECTED_SKILLS:
            path = PLUGIN_DIR / "skills" / skill / "SKILL.md"
            assert path.exists(), f"Missing skill: {skill}"

    def test_all_skills_body_depth(self) -> None:
        for skill in EXPECTED_SKILLS:
            lines = _body_lines(skill)
            assert len(lines) >= 10, f"{skill} body too short: {len(lines)} lines"

    def test_game_loop_covers_all_three_levels(self) -> None:
        content = _read_skill("game-loop")
        assert "micro" in content.lower()
        assert "macro" in content.lower()

    def test_balance_design_has_numeric_formula_or_ttk(self) -> None:
        content = _read_skill("balance-design")
        assert "TTK" in content or "formula" in content.lower() or "=" in content

    def test_systems_design_mentions_state_machine_or_signal(self) -> None:
        content = _read_skill("systems-design")
        assert "state" in content.lower() or "signal" in content.lower()

    def test_game_loop_mentions_feedback(self) -> None:
        content = _read_skill("game-loop")
        assert "feedback" in content.lower() or "feel" in content.lower()
