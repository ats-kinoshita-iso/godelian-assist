"""Phase A integration tests: lsp-setup and screenshot-review skills, MCP cookbook recipes."""

from __future__ import annotations

from pathlib import Path

PLUGIN_DIR = Path(__file__).parent.parent.parent / "plugins" / "godot-code-quality"
COOKBOOK_MCP = Path(__file__).parent.parent.parent / "cookbook" / "mcp"


def _read_skill(skill_name: str) -> str:
    path = PLUGIN_DIR / "skills" / skill_name / "SKILL.md"
    assert path.exists(), f"SKILL.md not found for skill: {skill_name}"
    return path.read_text(encoding="utf-8")


def _body_lines(skill_name: str) -> list[str]:
    """Return non-blank body lines (after YAML frontmatter)."""
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


# ---------------------------------------------------------------------------
# lsp-setup skill
# ---------------------------------------------------------------------------


class TestLspSetupSkill:
    def test_skill_exists(self) -> None:
        assert (PLUGIN_DIR / "skills" / "lsp-setup" / "SKILL.md").exists()

    def test_skill_has_frontmatter_name(self) -> None:
        content = _read_skill("lsp-setup")
        assert "name: lsp-setup" in content

    def test_skill_body_depth(self) -> None:
        lines = _body_lines("lsp-setup")
        assert len(lines) >= 15, f"lsp-setup body too short: {len(lines)} lines"

    def test_skill_mentions_lsp_port(self) -> None:
        content = _read_skill("lsp-setup")
        assert "--lsp-port" in content

    def test_skill_mentions_bridge_architecture(self) -> None:
        content = _read_skill("lsp-setup")
        assert "bridge" in content.lower() or "tcp" in content.lower()

    def test_skill_mentions_verification_step(self) -> None:
        content = _read_skill("lsp-setup")
        assert "verify" in content.lower()

    def test_skill_compares_lsp_vs_gdlint(self) -> None:
        content = _read_skill("lsp-setup")
        assert "gdlint" in content.lower()


# ---------------------------------------------------------------------------
# screenshot-review skill
# ---------------------------------------------------------------------------


class TestScreenshotReviewSkill:
    def test_skill_exists(self) -> None:
        assert (PLUGIN_DIR / "skills" / "screenshot-review" / "SKILL.md").exists()

    def test_skill_has_frontmatter_name(self) -> None:
        content = _read_skill("screenshot-review")
        assert "name: screenshot-review" in content

    def test_skill_body_depth(self) -> None:
        lines = _body_lines("screenshot-review")
        assert len(lines) >= 15, f"screenshot-review body too short: {len(lines)} lines"

    def test_skill_mentions_gdai_mcp(self) -> None:
        content = _read_skill("screenshot-review")
        assert "gdai" in content.lower() or "GDAI" in content

    def test_skill_mentions_design_intent(self) -> None:
        content = _read_skill("screenshot-review")
        assert "design intent" in content.lower()

    def test_skill_mentions_debug_output(self) -> None:
        content = _read_skill("screenshot-review")
        assert "debug output" in content.lower() or "debug_output" in content.lower()

    def test_skill_has_correct_tool_names(self) -> None:
        content = _read_skill("screenshot-review")
        assert "get_editor_screenshot" in content
        assert "get_running_scene_screenshot" in content

    def test_skill_mentions_limitations(self) -> None:
        """Skill must clarify what screenshot review cannot catch."""
        content = _read_skill("screenshot-review")
        assert "not" in content.lower() and (
            "replacement" in content.lower() or "substitute" in content.lower() or "cannot" in content.lower()
        )


# ---------------------------------------------------------------------------
# MCP cookbook recipes
# ---------------------------------------------------------------------------


class TestMcpCookbookRecipes:
    def test_gdai_mcp_recipe_exists(self) -> None:
        assert (COOKBOOK_MCP / "gdai-mcp.md").exists()

    def test_gdai_mcp_recipe_length(self) -> None:
        lines = (COOKBOOK_MCP / "gdai-mcp.md").read_text(encoding="utf-8").splitlines()
        assert len(lines) >= 40, f"gdai-mcp.md too short: {len(lines)} lines"

    def test_gdai_mcp_recipe_has_settings_json_block(self) -> None:
        content = (COOKBOOK_MCP / "gdai-mcp.md").read_text(encoding="utf-8")
        assert "mcpServers" in content
        assert "gdai-mcp" in content

    def test_gdai_mcp_recipe_mentions_correct_screenshot_tools(self) -> None:
        content = (COOKBOOK_MCP / "gdai-mcp.md").read_text(encoding="utf-8")
        assert "get_editor_screenshot" in content
        assert "get_running_scene_screenshot" in content

    def test_gdai_mcp_recipe_has_windows_notes(self) -> None:
        content = (COOKBOOK_MCP / "gdai-mcp.md").read_text(encoding="utf-8")
        assert "windows" in content.lower()

    def test_godot_mcp_minimal_recipe_exists(self) -> None:
        assert (COOKBOOK_MCP / "godot-mcp-minimal.md").exists()

    def test_godot_mcp_minimal_recipe_length(self) -> None:
        lines = (COOKBOOK_MCP / "godot-mcp-minimal.md").read_text(encoding="utf-8").splitlines()
        assert len(lines) >= 25, f"godot-mcp-minimal.md too short: {len(lines)} lines"

    def test_godot_mcp_minimal_has_npm_install(self) -> None:
        content = (COOKBOOK_MCP / "godot-mcp-minimal.md").read_text(encoding="utf-8")
        assert "npx" in content or "npm" in content

    def test_godot_mcp_minimal_has_comparison_table(self) -> None:
        content = (COOKBOOK_MCP / "godot-mcp-minimal.md").read_text(encoding="utf-8")
        assert "gdai" in content.lower() and "|" in content

    def test_gdscript_lsp_recipe_exists(self) -> None:
        assert (COOKBOOK_MCP / "gdscript-lsp.md").exists()

    def test_gdscript_lsp_recipe_length(self) -> None:
        lines = (COOKBOOK_MCP / "gdscript-lsp.md").read_text(encoding="utf-8").splitlines()
        assert len(lines) >= 30, f"gdscript-lsp.md too short: {len(lines)} lines"

    def test_gdscript_lsp_recipe_mentions_lsp_port(self) -> None:
        content = (COOKBOOK_MCP / "gdscript-lsp.md").read_text(encoding="utf-8")
        assert "--lsp-port" in content

    def test_gdscript_lsp_recipe_has_settings_env_block(self) -> None:
        content = (COOKBOOK_MCP / "gdscript-lsp.md").read_text(encoding="utf-8")
        assert "GODOT_EDITOR_PATH" in content or "mcpServers" in content
