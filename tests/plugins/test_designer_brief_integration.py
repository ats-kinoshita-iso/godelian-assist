"""Integration tests for the designer-brief plugin."""

from __future__ import annotations

import json
from pathlib import Path

PLUGIN_DIR = Path(__file__).parent.parent.parent / "plugins" / "designer-brief"
EXPECTED_SKILLS = ["brief", "spec-review", "iterate", "playtest-debrief", "feature-complete"]


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


class TestDesignerBriefStructure:
    def test_plugin_json_valid(self) -> None:
        data = json.loads(
            (PLUGIN_DIR / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        assert data["name"] == "designer-brief"
        assert data["license"] == "MIT"
        assert "workflow" in data["keywords"] or "designer" in data["keywords"]

    def test_all_skills_exist(self) -> None:
        for skill in EXPECTED_SKILLS:
            path = PLUGIN_DIR / "skills" / skill / "SKILL.md"
            assert path.exists(), f"Missing skill: {skill}"

    def test_hooks_json_valid(self) -> None:
        hooks_path = PLUGIN_DIR / "hooks" / "hooks.json"
        assert hooks_path.exists()
        data = json.loads(hooks_path.read_text(encoding="utf-8"))
        assert "hooks" in data
        assert len(data["hooks"]) >= 1

    def test_hooks_json_has_pretooluse(self) -> None:
        data = json.loads(
            (PLUGIN_DIR / "hooks" / "hooks.json").read_text(encoding="utf-8")
        )
        events = [h["event"] for h in data["hooks"]]
        assert "PreToolUse" in events


class TestBriefSkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("brief")
        assert len(lines) >= 20, f"brief body too short: {len(lines)} lines"

    def test_contains_intent_heading(self) -> None:
        content = _read_skill("brief")
        assert "Intent" in content

    def test_contains_feel_heading(self) -> None:
        content = _read_skill("brief")
        assert "Feel" in content

    def test_contains_constraints_heading(self) -> None:
        content = _read_skill("brief")
        assert "Constraints" in content

    def test_contains_out_of_scope(self) -> None:
        content = _read_skill("brief")
        assert "Out of scope" in content or "out of scope" in content.lower()

    def test_contains_designer_acceptance(self) -> None:
        content = _read_skill("brief")
        assert "acceptance" in content.lower() or "Designer acceptance" in content

    def test_mentions_active_spec(self) -> None:
        content = _read_skill("brief")
        assert "ACTIVE_SPEC" in content

    def test_mentions_approval_rule(self) -> None:
        content = _read_skill("brief")
        assert "approval" in content.lower() or "approved" in content.lower()


class TestSpecReviewSkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("spec-review")
        assert len(lines) >= 15, f"spec-review body too short: {len(lines)} lines"

    def test_mentions_active_spec(self) -> None:
        content = _read_skill("spec-review")
        assert "ACTIVE_SPEC" in content

    def test_has_three_outcomes(self) -> None:
        content = _read_skill("spec-review")
        assert "approved" in content.lower()
        assert "revised" in content.lower() or "revise" in content.lower()
        assert "rejected" in content.lower()


class TestIterateSkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("iterate")
        assert len(lines) >= 15, f"iterate body too short: {len(lines)} lines"

    def test_mentions_minimal_diff(self) -> None:
        content = _read_skill("iterate")
        assert "minimal diff" in content.lower() or "minimal change" in content.lower()

    def test_distinguishes_iterate_vs_brief(self) -> None:
        content = _read_skill("iterate")
        assert "brief" in content.lower()


class TestPlaytestDebriefSkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("playtest-debrief")
        assert len(lines) >= 15, f"playtest-debrief body too short: {len(lines)} lines"

    def test_has_what_worked_heading(self) -> None:
        content = _read_skill("playtest-debrief")
        assert "What worked" in content or "what worked" in content.lower()

    def test_has_what_felt_wrong_heading(self) -> None:
        content = _read_skill("playtest-debrief")
        assert "felt wrong" in content.lower()

    def test_has_bugs_heading(self) -> None:
        content = _read_skill("playtest-debrief")
        assert "Bug" in content or "bug" in content.lower()

    def test_has_open_questions_heading(self) -> None:
        content = _read_skill("playtest-debrief")
        assert "question" in content.lower() or "open" in content.lower()


class TestFeatureCompleteSkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("feature-complete")
        assert len(lines) >= 12, f"feature-complete body too short: {len(lines)} lines"

    def test_mentions_gdlint(self) -> None:
        content = _read_skill("feature-complete")
        assert "gdlint" in content.lower()

    def test_mentions_gdunit4(self) -> None:
        content = _read_skill("feature-complete")
        assert "gdunit4" in content.lower()

    def test_mentions_commit(self) -> None:
        content = _read_skill("feature-complete")
        assert "commit" in content.lower()
