"""Tests for cookbook API reference documents."""

from __future__ import annotations

from pathlib import Path

COOKBOOK_DIR = Path(__file__).parent.parent.parent / "cookbook"
API_REF_DIR = COOKBOOK_DIR / "api-ref"


class TestTscnFormatApiRef:
    def test_file_exists(self) -> None:
        assert (API_REF_DIR / "tscn-format.md").exists()

    def test_minimum_length(self) -> None:
        content = (API_REF_DIR / "tscn-format.md").read_text(encoding="utf-8")
        lines = [ln for ln in content.split("\n") if ln.strip()]
        assert len(lines) >= 60, f"tscn-format.md too short: {len(lines)} non-empty lines"

    def test_covers_uid_charset(self) -> None:
        content = (API_REF_DIR / "tscn-format.md").read_text(encoding="utf-8")
        assert "base-34" in content
        # Must document excluded chars
        assert "z" in content
        assert "9" in content

    def test_covers_uid_length(self) -> None:
        content = (API_REF_DIR / "tscn-format.md").read_text(encoding="utf-8")
        assert "13" in content

    def test_covers_ext_resource_id_format(self) -> None:
        content = (API_REF_DIR / "tscn-format.md").read_text(encoding="utf-8")
        assert "ext_resource" in content
        # ID format pattern N_XXXXX
        assert "_aaaaa" in content or "N_" in content

    def test_covers_sub_resource_id_format(self) -> None:
        content = (API_REF_DIR / "tscn-format.md").read_text(encoding="utf-8")
        assert "sub_resource" in content
        assert "ClassName" in content or "CapsuleShape3D" in content

    def test_covers_load_steps_formula(self) -> None:
        content = (API_REF_DIR / "tscn-format.md").read_text(encoding="utf-8")
        assert "load_steps" in content
        assert "ext_resource" in content
        assert "sub_resource" in content

    def test_covers_parent_path_rules(self) -> None:
        content = (API_REF_DIR / "tscn-format.md").read_text(encoding="utf-8")
        assert 'parent="."' in content
        assert "root" in content.lower()

    def test_covers_connection_syntax(self) -> None:
        content = (API_REF_DIR / "tscn-format.md").read_text(encoding="utf-8")
        assert "[connection" in content
        assert "signal" in content
        assert "method" in content

    def test_covers_headless_validation(self) -> None:
        content = (API_REF_DIR / "tscn-format.md").read_text(encoding="utf-8")
        assert "--headless" in content

    def test_covers_format_version(self) -> None:
        content = (API_REF_DIR / "tscn-format.md").read_text(encoding="utf-8")
        assert "format=3" in content

    def test_contains_complete_example(self) -> None:
        content = (API_REF_DIR / "tscn-format.md").read_text(encoding="utf-8")
        assert "[gd_scene" in content
        assert "CharacterBody3D" in content
        assert "ExtResource" in content
        assert "SubResource" in content

    def test_covers_shape_defaults(self) -> None:
        content = (API_REF_DIR / "tscn-format.md").read_text(encoding="utf-8")
        assert "CapsuleShape3D" in content
        assert "default" in content.lower()


class TestNodeApiRefs:
    """Each node API ref must exist, be >=25 lines, and contain an extends chain + typed example."""

    _REQUIRED_REFS = [
        "CharacterBody3D.md",
        "RigidBody3D.md",
        "Area3D.md",
        "AnimationPlayer.md",
        "NavigationAgent3D.md",
        "AudioStreamPlayer.md",
        "Resource.md",
        "Signal.md",
    ]

    def test_all_ref_files_exist(self) -> None:
        for ref in self._REQUIRED_REFS:
            assert (API_REF_DIR / ref).exists(), f"Missing: {ref}"

    def _read(self, filename: str) -> str:
        return (API_REF_DIR / filename).read_text(encoding="utf-8")

    def _non_blank_lines(self, filename: str) -> int:
        return len([ln for ln in self._read(filename).split("\n") if ln.strip()])

    def test_character_body_3d_length(self) -> None:
        assert self._non_blank_lines("CharacterBody3D.md") >= 25

    def test_character_body_3d_has_extends(self) -> None:
        assert "extends" in self._read("CharacterBody3D.md")

    def test_character_body_3d_has_typed_example(self) -> None:
        assert "class_name" in self._read("CharacterBody3D.md")

    def test_rigid_body_3d_length(self) -> None:
        assert self._non_blank_lines("RigidBody3D.md") >= 25

    def test_rigid_body_3d_has_integrate_forces(self) -> None:
        assert "_integrate_forces" in self._read("RigidBody3D.md")

    def test_area_3d_length(self) -> None:
        assert self._non_blank_lines("Area3D.md") >= 25

    def test_area_3d_mentions_ghost_frames(self) -> None:
        assert "ghost" in self._read("Area3D.md").lower()

    def test_animation_player_length(self) -> None:
        assert self._non_blank_lines("AnimationPlayer.md") >= 25

    def test_animation_player_has_signals(self) -> None:
        assert "animation_finished" in self._read("AnimationPlayer.md")

    def test_navigation_agent_3d_length(self) -> None:
        assert self._non_blank_lines("NavigationAgent3D.md") >= 25

    def test_navigation_agent_3d_has_next_path(self) -> None:
        assert "get_next_path_position" in self._read("NavigationAgent3D.md")

    def test_audio_stream_player_length(self) -> None:
        assert self._non_blank_lines("AudioStreamPlayer.md") >= 25

    def test_resource_md_length(self) -> None:
        assert self._non_blank_lines("Resource.md") >= 25

    def test_resource_md_mentions_export(self) -> None:
        assert "@export" in self._read("Resource.md")

    def test_resource_md_mentions_custom_subclass(self) -> None:
        content = self._read("Resource.md")
        assert "class_name" in content and "extends Resource" in content

    def test_signal_md_length(self) -> None:
        assert self._non_blank_lines("Signal.md") >= 25

    def test_signal_md_mentions_connect(self) -> None:
        assert "connect" in self._read("Signal.md")

    def test_signal_md_mentions_emit(self) -> None:
        assert "emit" in self._read("Signal.md")
