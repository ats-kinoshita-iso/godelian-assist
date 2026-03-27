# GDAI MCP Server — Setup Guide

<!-- last-updated: 2026-03-27 -->

GDAI MCP gives Claude direct control of the live Godot editor: read and write scene trees,
create and modify scripts, run the game, and capture screenshots. It exposes 40 tools via a
Python server that communicates with a Godot plugin over WebSocket.

**Version**: 0.3.1+ (use this version or later — Windows Defender fix is in 0.2.9+)
**Godot minimum**: 4.1+
**Cost**: Paid — download from https://gdaimcp.com

---

## Prerequisites

- Godot editor installed and a project open (the editor **must be running** — GDAI MCP does not work headless)
- `uv` (Python package manager) — install once per machine:
  ```powershell
  # Windows PowerShell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

---

## Step 1: Install the Godot Plugin

1. Purchase and download the plugin zip from https://gdaimcp.com
2. Extract into your game project: copy `addons/gdai-mcp-plugin-godot/` into `res://addons/`
3. In Godot: **Project → Project Settings → Plugins → GDAI MCP → Enable**
4. A "GDAI MCP" tab appears in the editor — note the path shown for `gdai_mcp_server.py`

---

## Step 2: Add to Claude Code settings.json

Add to your project's `.claude/settings.json` (or global `~/.claude/settings.json`):

```json
{
  "mcpServers": {
    "gdai-mcp": {
      "command": "uv",
      "args": [
        "run",
        "C:/path/to/your/game/addons/gdai-mcp-plugin-godot/gdai_mcp_server.py"
      ]
    }
  }
}
```

**Windows note**: Use forward slashes in the path, or escape backslashes (`C:\\path\\...`).
If `uv` is not on PATH, use the full path: `C:/Users/<you>/AppData/Local/Programs/Python/Python312/Scripts/uv.exe`

---

## Step 3: Verify

1. Open your game project in the Godot editor
2. Start a Claude Code session in the project directory
3. Run `/mcp` to confirm `gdai-mcp` appears in the server list
4. Ask Claude: "Use get_project_info to describe this project"

---

## Available Tool Categories

| Category | Key Tools |
|---|---|
| **Project** | `get_project_info`, `get_filesystem_tree`, `search_files` |
| **Scene** | `get_scene_tree`, `get_scene_file_content`, `create_scene`, `play_scene`, `stop_running_scene` |
| **Node** | `add_node`, `delete_node`, `move_node`, `update_property` |
| **Script** | `view_script`, `create_script`, `attach_script`, `edit_file` |
| **Editor** | `get_godot_errors`, `get_editor_screenshot`, `get_running_scene_screenshot`, `clear_output_logs` |

### Screenshot tools

- `get_editor_screenshot` — captures the full Godot editor window
- `get_running_scene_screenshot` — captures the game viewport while a scene is playing

> Note: the tool names are `get_editor_screenshot` / `get_running_scene_screenshot` —
> not `capture_screenshot` or `take_screenshot`.

---

## Typical Workflow with Claude Code

```
1. Open game project in Godot editor
2. Claude: use get_scene_tree to read the current scene
3. Claude: use create_script / edit_file to write or modify GDScript
4. Claude: use play_scene to launch the scene
5. Claude: use get_running_scene_screenshot to verify visuals
6. Claude: use get_godot_errors to check for runtime errors
7. Claude: fix issues and repeat from 4
```

---

## Windows 11 Notes

- Versions before 0.2.9 had Windows Defender compatibility issues — use 0.3.0+ (current: 0.3.1)
- v0.3.0 added Windows x64 double precision build support
- No Claude Code-specific issues are documented for Windows
- The Godot editor window must remain open throughout the session
- If the WebSocket disconnects, re-enable the plugin in Project Settings and restart Claude Code

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `gdai-mcp` not in `/mcp` list | Check `uv` is on PATH; verify path to `gdai_mcp_server.py` in settings.json |
| Tools return "editor not connected" | Ensure the Godot editor is open with the plugin enabled |
| Screenshot is blank | The game scene must be running (`play_scene` first) before `get_running_scene_screenshot` |
| Path errors on Windows | Use forward slashes or escape backslashes in JSON paths |

---

## See Also

- `cookbook/mcp/godot-mcp-minimal.md` — free, headless-friendly alternative (no screenshots)
- `plugins/godot-code-quality/skills/screenshot-review/SKILL.md` — how to use screenshots in review
