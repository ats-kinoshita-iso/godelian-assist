"""Integration tests for the godot-code-quality plugin."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

PLUGIN_DIR = Path(__file__).parent.parent.parent / "plugins" / "godot-code-quality"


def _read_skill(skill_name: str) -> str:
    path = PLUGIN_DIR / "skills" / skill_name / "SKILL.md"
    assert path.exists(), f"SKILL.md not found for skill: {skill_name}"
    return path.read_text(encoding="utf-8")


def _body_lines(skill_name: str) -> list[str]:
    """Return non-blank body lines (after frontmatter)."""
    content = _read_skill(skill_name)
    lines = content.split("\n")
    # Skip YAML frontmatter block (between first and second ---)
    in_front = False
    body: list[str] = []
    marker_count = 0
    for line in lines:
        if line.strip() == "---":
            marker_count += 1
            continue
        if marker_count >= 2:
            body.append(line)
    return [l for l in body if l.strip()]


class TestGodotCodeQualityStructure:
    def test_plugin_json_exists(self) -> None:
        assert (PLUGIN_DIR / ".claude-plugin" / "plugin.json").exists()

    def test_plugin_json_valid(self) -> None:
        data = json.loads(
            (PLUGIN_DIR / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        assert data["name"] == "godot-code-quality"
        assert data["license"] == "MIT"

    def test_hooks_json_exists_and_valid(self) -> None:
        hooks_path = PLUGIN_DIR / "hooks" / "hooks.json"
        assert hooks_path.exists()
        data = json.loads(hooks_path.read_text(encoding="utf-8"))
        assert "hooks" in data
        events = [h["event"] for h in data["hooks"]]
        assert "PreToolUse" in events
        assert "Stop" in events

    def test_quality_skill_body_depth(self) -> None:
        lines = _body_lines("quality")
        assert len(lines) >= 10, f"quality skill body too short: {len(lines)} lines"

    def test_quality_skill_mentions_gdlint(self) -> None:
        content = _read_skill("quality")
        assert "gdlint" in content.lower()

    def test_quality_skill_mentions_gdunit4(self) -> None:
        content = _read_skill("quality")
        assert "gdunit4" in content.lower()

    def test_quality_fix_skill_body_depth(self) -> None:
        lines = _body_lines("quality-fix")
        assert len(lines) >= 10, f"quality-fix skill body too short: {len(lines)} lines"

    def test_quality_fix_skill_mentions_gdformat(self) -> None:
        content = _read_skill("quality-fix")
        assert "gdformat" in content.lower()
