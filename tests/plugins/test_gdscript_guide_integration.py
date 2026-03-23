"""Integration tests for the gdscript-guide plugin."""

from __future__ import annotations

import json
from pathlib import Path

PLUGIN_DIR = Path(__file__).parent.parent.parent / "plugins" / "gdscript-guide"
EXPECTED_SKILLS = ["typing-guide", "idioms", "performance"]


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


class TestGdscriptGuideStructure:
    def test_plugin_json_valid(self) -> None:
        data = json.loads(
            (PLUGIN_DIR / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        assert data["name"] == "gdscript-guide"
        assert "gdscript" in data["keywords"]

    def test_all_skills_exist(self) -> None:
        for skill in EXPECTED_SKILLS:
            path = PLUGIN_DIR / "skills" / skill / "SKILL.md"
            assert path.exists(), f"Missing skill: {skill}"

    def test_all_skills_body_depth(self) -> None:
        for skill in EXPECTED_SKILLS:
            lines = _body_lines(skill)
            assert len(lines) >= 10, f"{skill} body too short: {len(lines)} lines"

    def test_typing_guide_mentions_export_and_typed_array(self) -> None:
        content = _read_skill("typing-guide")
        assert "@export" in content
        assert "Array[" in content

    def test_idioms_mentions_match_or_await(self) -> None:
        content = _read_skill("idioms")
        assert "match" in content or "await" in content

    def test_performance_mentions_onready_and_process(self) -> None:
        content = _read_skill("performance")
        assert "@onready" in content or "onready" in content
        assert "_process" in content

    def test_performance_mentions_caching(self) -> None:
        content = _read_skill("performance")
        assert "cache" in content.lower() or "get_node" in content.lower()
