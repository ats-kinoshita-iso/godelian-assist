"""Integration tests for the test-quality plugin."""

from __future__ import annotations

import json
from pathlib import Path

PLUGIN_DIR = Path(__file__).parent.parent.parent / "plugins" / "test-quality"


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


class TestTestQualityPlugin:
    def test_plugin_json_valid(self) -> None:
        data = json.loads(
            (PLUGIN_DIR / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        assert "name" in data
        assert "license" in data

    def test_test_gen_godot_skill_exists(self) -> None:
        path = PLUGIN_DIR / "skills" / "test-gen-godot" / "SKILL.md"
        assert path.exists()

    def test_test_gen_godot_body_depth(self) -> None:
        lines = _body_lines("test-gen-godot")
        assert len(lines) >= 15, f"test-gen-godot body too short: {len(lines)} lines"

    def test_test_gen_godot_mentions_gdunit4_suite(self) -> None:
        content = _read_skill("test-gen-godot")
        assert "GdUnitTestSuite" in content

    def test_test_gen_godot_mentions_signal_testing(self) -> None:
        content = _read_skill("test-gen-godot")
        assert "monitor_signals" in content or "assert_signal" in content

    def test_test_gen_godot_mentions_before_test(self) -> None:
        content = _read_skill("test-gen-godot")
        assert "before_test" in content

    def test_test_gen_godot_mentions_assert_methods(self) -> None:
        content = _read_skill("test-gen-godot")
        assert "assert_float" in content or "assert_int" in content or "assert_bool" in content
