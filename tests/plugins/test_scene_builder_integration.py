"""Integration tests for the scene-builder plugin."""

from __future__ import annotations

import json
from pathlib import Path

PLUGIN_DIR = Path(__file__).parent.parent.parent / "plugins" / "scene-builder"
EXPECTED_SKILLS = ["create-scene", "add-node", "wire-signals", "scene-from-brief", "scene-audit"]


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


class TestSceneBuilderStructure:
    def test_plugin_json_valid(self) -> None:
        data = json.loads(
            (PLUGIN_DIR / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        assert data["name"] == "scene-builder"
        assert data["license"] == "MIT"
        assert "scene" in data["keywords"] or "tscn" in data["keywords"]

    def test_all_skills_exist(self) -> None:
        for skill in EXPECTED_SKILLS:
            path = PLUGIN_DIR / "skills" / skill / "SKILL.md"
            assert path.exists(), f"Missing skill: {skill}"

    def test_readme_optional_but_plugin_json_required(self) -> None:
        assert (PLUGIN_DIR / ".claude-plugin" / "plugin.json").exists()


class TestCreateSceneSkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("create-scene")
        assert len(lines) >= 25, f"create-scene body too short: {len(lines)} lines"

    def test_mentions_generation_algorithm(self) -> None:
        content = _read_skill("create-scene")
        assert "algorithm" in content.lower() or "generation" in content.lower()

    def test_mentions_load_steps_formula(self) -> None:
        content = _read_skill("create-scene")
        assert "load_steps" in content
        assert "ext_resource" in content
        assert "sub_resource" in content

    def test_mentions_uid_charset(self) -> None:
        content = _read_skill("create-scene")
        # Must reference the base-34 charset or the exclusions
        assert "base-34" in content or ("z" in content and "9" in content)

    def test_mentions_collisionshape_rule(self) -> None:
        content = _read_skill("create-scene")
        assert "CollisionShape3D" in content
        assert "shape" in content.lower()

    def test_mentions_parent_path_rules(self) -> None:
        content = _read_skill("create-scene")
        assert 'parent="."' in content or "parent path" in content.lower()

    def test_mentions_headless_validation(self) -> None:
        content = _read_skill("create-scene")
        assert "--headless" in content or "headless" in content.lower()

    def test_contains_tscn_example(self) -> None:
        content = _read_skill("create-scene")
        assert "[gd_scene" in content
        assert "[node" in content


class TestAddNodeSkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("add-node")
        assert len(lines) >= 18, f"add-node body too short: {len(lines)} lines"

    def test_mentions_path_preservation(self) -> None:
        content = _read_skill("add-node")
        assert "preserv" in content.lower() or "verbatim" in content.lower()

    def test_mentions_load_steps_update(self) -> None:
        content = _read_skill("add-node")
        assert "load_steps" in content

    def test_mentions_collisionshape_rule(self) -> None:
        content = _read_skill("add-node")
        assert "CollisionShape3D" in content

    def test_mentions_id_assignment(self) -> None:
        content = _read_skill("add-node")
        assert "sequential" in content.lower() or "next" in content.lower()


class TestWireSignalsSkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("wire-signals")
        assert len(lines) >= 15, f"wire-signals body too short: {len(lines)} lines"

    def test_mentions_connection_syntax(self) -> None:
        content = _read_skill("wire-signals")
        assert "[connection" in content

    def test_mentions_required_fields(self) -> None:
        content = _read_skill("wire-signals")
        assert "signal" in content
        assert "from" in content
        assert "to" in content
        assert "method" in content

    def test_mentions_optional_flags(self) -> None:
        content = _read_skill("wire-signals")
        assert "flags" in content

    def test_mentions_path_convention(self) -> None:
        content = _read_skill("wire-signals")
        assert '"."' in content or "root" in content.lower()


class TestSceneFromBriefSkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("scene-from-brief")
        assert len(lines) >= 20, f"scene-from-brief body too short: {len(lines)} lines"

    def test_mentions_active_spec(self) -> None:
        content = _read_skill("scene-from-brief")
        assert "ACTIVE_SPEC" in content

    def test_mentions_generation_order(self) -> None:
        content = _read_skill("scene-from-brief")
        assert "order" in content.lower() or "step" in content.lower()

    def test_mentions_collisionshape_rule(self) -> None:
        content = _read_skill("scene-from-brief")
        assert "CollisionShape3D" in content

    def test_mentions_scope_boundary(self) -> None:
        content = _read_skill("scene-from-brief")
        assert "scope" in content.lower() or "GDScript" in content


class TestSceneAuditSkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("scene-audit")
        assert len(lines) >= 15, f"scene-audit body too short: {len(lines)} lines"

    def test_mentions_uid_validation(self) -> None:
        content = _read_skill("scene-audit")
        assert "uid" in content.lower() or "UID" in content

    def test_mentions_load_steps_check(self) -> None:
        content = _read_skill("scene-audit")
        assert "load_steps" in content

    def test_mentions_collisionshape_check(self) -> None:
        content = _read_skill("scene-audit")
        assert "CollisionShape3D" in content

    def test_has_severity_levels(self) -> None:
        content = _read_skill("scene-audit")
        assert "error" in content.lower() or "ERROR" in content
        assert "warning" in content.lower() or "WARNING" in content

    def test_mentions_dangling_resources(self) -> None:
        content = _read_skill("scene-audit")
        assert "dangling" in content.lower() or "unreferenced" in content.lower() or "never referenced" in content.lower()
