"""Integration tests for the project-bootstrap plugin."""

from __future__ import annotations

import json
from pathlib import Path

PLUGIN_DIR = Path(__file__).parent.parent.parent / "plugins" / "project-bootstrap"
EXPECTED_SKILLS = ["new-project", "configure-quality", "setup-autoloads", "setup-directories"]


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


class TestProjectBootstrapStructure:
    def test_plugin_json_valid(self) -> None:
        data = json.loads(
            (PLUGIN_DIR / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        assert data["name"] == "project-bootstrap"
        assert data["license"] == "MIT"
        assert "bootstrap" in data["keywords"] or "setup" in data["keywords"]

    def test_all_skills_exist(self) -> None:
        for skill in EXPECTED_SKILLS:
            path = PLUGIN_DIR / "skills" / skill / "SKILL.md"
            assert path.exists(), f"Missing skill: {skill}"

    def test_readme_exists(self) -> None:
        assert (PLUGIN_DIR / "README.md").exists()


class TestNewProjectSkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("new-project")
        assert len(lines) >= 25, f"new-project body too short: {len(lines)} lines"

    def test_mentions_seven_steps(self) -> None:
        content = _read_skill("new-project")
        # Must enumerate 7 steps
        assert "Step 7" in content or "7 " in content or "seven" in content.lower()

    def test_mentions_project_godot(self) -> None:
        content = _read_skill("new-project")
        assert "project.godot" in content

    def test_mentions_gitignore(self) -> None:
        content = _read_skill("new-project")
        assert ".gitignore" in content

    def test_mentions_game_backlog_json(self) -> None:
        content = _read_skill("new-project")
        assert "game-backlog.json" in content

    def test_mentions_claude_md(self) -> None:
        content = _read_skill("new-project")
        assert "CLAUDE.md" in content

    def test_mentions_headless_verification(self) -> None:
        content = _read_skill("new-project")
        assert "--headless" in content


class TestConfigureQualitySkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("configure-quality")
        assert len(lines) >= 18, f"configure-quality body too short: {len(lines)} lines"

    def test_contains_gdlintrc(self) -> None:
        content = _read_skill("configure-quality")
        assert ".gdlintrc" in content

    def test_mentions_gdtoolkit_install(self) -> None:
        content = _read_skill("configure-quality")
        assert "gdtoolkit" in content or "pip install" in content

    def test_mentions_gdunit4(self) -> None:
        content = _read_skill("configure-quality")
        assert "gdunit4" in content.lower() or "GdUnit4" in content


class TestSetupAutoloadsSkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("setup-autoloads")
        assert len(lines) >= 20, f"setup-autoloads body too short: {len(lines)} lines"

    def test_contains_eventbus(self) -> None:
        content = _read_skill("setup-autoloads")
        assert "EventBus" in content
        assert "class_name" in content

    def test_contains_game_manager(self) -> None:
        content = _read_skill("setup-autoloads")
        assert "GameManager" in content

    def test_contains_save_manager(self) -> None:
        content = _read_skill("setup-autoloads")
        assert "SaveManager" in content

    def test_skeletons_use_static_typing(self) -> None:
        content = _read_skill("setup-autoloads")
        # Static typing evidenced by typed declarations
        assert "String" in content and ("int" in content or "bool" in content or "Node" in content)

    def test_contains_autoload_registration(self) -> None:
        content = _read_skill("setup-autoloads")
        assert "[autoload]" in content


class TestSetupDirectoriesSkill:
    def test_body_depth(self) -> None:
        lines = _body_lines("setup-directories")
        assert len(lines) >= 12, f"setup-directories body too short: {len(lines)} lines"

    def test_mentions_gdignore(self) -> None:
        content = _read_skill("setup-directories")
        assert ".gdignore" in content

    def test_mentions_src_directory(self) -> None:
        content = _read_skill("setup-directories")
        assert "src/" in content or "src\\" in content

    def test_mentions_plans_directory(self) -> None:
        content = _read_skill("setup-directories")
        assert "plans/" in content
