"""Integration tests for the game-backlog plugin."""

from __future__ import annotations

import json
from pathlib import Path

PLUGIN_DIR = Path(__file__).parent.parent.parent / "plugins" / "game-backlog"
EXPECTED_SKILLS = ["backlog-init", "backlog-status", "next-feature", "add-feature"]


def _read_skill(skill_name: str) -> str:
    path = PLUGIN_DIR / "skills" / skill_name / "SKILL.md"
    assert path.exists(), f"SKILL.md not found: {skill_name}"
    return path.read_text(encoding="utf-8")


def _body_lines(skill_name: str) -> list[str]:
    content = _read_skill(skill_name)
    marker_count = 0
    body: list[str] = []
    for line in content.split("\n"):
        if line.strip() == "---":
            marker_count += 1
            continue
        if marker_count >= 2:
            body.append(line)
    return [ln for ln in body if ln.strip()]


class TestGameBacklogStructure:
    def test_plugin_json_valid(self) -> None:
        data = json.loads(
            (PLUGIN_DIR / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        assert data["name"] == "game-backlog"
        assert data["license"] == "MIT"
        assert "backlog" in data["keywords"] or "planning" in data["keywords"]

    def test_all_skills_exist(self) -> None:
        for skill in EXPECTED_SKILLS:
            path = PLUGIN_DIR / "skills" / skill / "SKILL.md"
            assert path.exists(), f"Missing skill: {skill}"

    def test_readme_exists(self) -> None:
        assert (PLUGIN_DIR / "README.md").exists()


class TestBacklogInitSkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("backlog-init")
        assert len(lines) >= 15, f"backlog-init body too short: {len(lines)} lines"

    def test_contains_json_schema(self) -> None:
        content = _read_skill("backlog-init")
        assert '"status"' in content
        assert '"priority"' in content
        assert '"brief"' in content

    def test_schema_has_status_values(self) -> None:
        content = _read_skill("backlog-init")
        assert "queued" in content
        assert "in_progress" in content
        assert "done" in content

    def test_mentions_priority_confirmation(self) -> None:
        content = _read_skill("backlog-init")
        assert "priority" in content.lower() and "confirm" in content.lower()


class TestBacklogStatusSkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("backlog-status")
        assert len(lines) >= 12, f"backlog-status body too short: {len(lines)} lines"

    def test_mentions_in_progress(self) -> None:
        content = _read_skill("backlog-status")
        assert "in_progress" in content

    def test_mentions_one_at_a_time_rule(self) -> None:
        content = _read_skill("backlog-status")
        assert "one" in content.lower() and (
            "at a time" in content.lower() or "in_progress" in content.lower()
        )


class TestNextFeatureSkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("next-feature")
        assert len(lines) >= 12, f"next-feature body too short: {len(lines)} lines"

    def test_mentions_pending_approval(self) -> None:
        content = _read_skill("next-feature")
        assert "pending_approval" in content

    def test_mentions_active_spec(self) -> None:
        content = _read_skill("next-feature")
        assert "ACTIVE_SPEC" in content


class TestAddFeatureSkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("add-feature")
        assert len(lines) >= 10, f"add-feature body too short: {len(lines)} lines"

    def test_mentions_priority(self) -> None:
        content = _read_skill("add-feature")
        assert "priority" in content.lower()

    def test_mentions_queued_status(self) -> None:
        content = _read_skill("add-feature")
        assert "queued" in content.lower()
