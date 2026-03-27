"""Integration tests for the godot-physics plugin."""

from __future__ import annotations

import json
from pathlib import Path

PLUGIN_DIR = Path(__file__).parent.parent.parent / "plugins" / "godot-physics"
EXPECTED_SKILLS = [
    "character-movement",
    "collision-layers",
    "area-detection",
    "rigidbody-patterns",
    "projectile-system",
]


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


class TestGodotPhysicsStructure:
    def test_plugin_json_valid(self) -> None:
        data = json.loads(
            (PLUGIN_DIR / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        assert data["name"] == "godot-physics"
        assert data["license"] == "MIT"
        assert "physics" in data["keywords"] or "movement" in data["keywords"]

    def test_all_skills_exist(self) -> None:
        for skill in EXPECTED_SKILLS:
            assert (PLUGIN_DIR / "skills" / skill / "SKILL.md").exists()

    def test_readme_exists(self) -> None:
        assert (PLUGIN_DIR / "README.md").exists()


class TestCharacterMovementSkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("character-movement")
        assert len(lines) >= 22, f"character-movement body too short: {len(lines)} lines"

    def test_mentions_coyote_time(self) -> None:
        content = _read_skill("character-movement")
        assert "coyote" in content.lower()

    def test_mentions_jump_buffering(self) -> None:
        content = _read_skill("character-movement")
        assert "jump buffer" in content.lower() or "jump_buffer" in content.lower()

    def test_mentions_air_acceleration(self) -> None:
        content = _read_skill("character-movement")
        assert "air_acceleration" in content or "air acceleration" in content.lower()

    def test_contains_typed_gdscript(self) -> None:
        content = _read_skill("character-movement")
        assert "class_name" in content
        assert "CharacterBody3D" in content


class TestCollisionLayersSkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("collision-layers")
        assert len(lines) >= 15

    def test_has_constants_class(self) -> None:
        content = _read_skill("collision-layers")
        assert "class_name" in content or "const" in content
        assert "CollisionLayer" in content

    def test_mentions_layer_names(self) -> None:
        content = _read_skill("collision-layers")
        assert "PLAYER" in content or "WORLD" in content


class TestAreaDetectionSkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("area-detection")
        assert len(lines) >= 15

    def test_mentions_ghost_frames(self) -> None:
        content = _read_skill("area-detection")
        assert "ghost" in content.lower()

    def test_mentions_deferred(self) -> None:
        content = _read_skill("area-detection")
        assert "deferred" in content.lower() or "CONNECT_DEFERRED" in content


class TestRigidbodyPatternsSkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("rigidbody-patterns")
        assert len(lines) >= 15

    def test_mentions_integrate_forces(self) -> None:
        content = _read_skill("rigidbody-patterns")
        assert "_integrate_forces" in content

    def test_mentions_freeze_modes(self) -> None:
        content = _read_skill("rigidbody-patterns")
        assert "freeze" in content.lower()


class TestProjectileSystemSkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("projectile-system")
        assert len(lines) >= 15

    def test_mentions_pooling(self) -> None:
        content = _read_skill("projectile-system")
        assert "pool" in content.lower()

    def test_mentions_pool_size_formula(self) -> None:
        content = _read_skill("projectile-system")
        assert "pool_size" in content or "fire_rate" in content
