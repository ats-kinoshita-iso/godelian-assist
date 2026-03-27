# godot-mcp (Minimal) — Setup Guide

<!-- last-updated: 2026-03-27 -->

`@coding-solo/godot-mcp` is the free, headless-friendly Godot MCP server. It launches Godot
as a subprocess on demand — no editor needs to be open first. Great for CI-style verification
and debug output capture. Does not include screenshot tools.

**Package**: `@coding-solo/godot-mcp` (npm)
**Node.js**: >= 18.0.0
**Cost**: Free, open source

---

## Step 1: Add to Claude Code settings.json

No global install required — Claude Code runs it via `npx`. Add to `.claude/settings.json`:

```json
{
  "mcpServers": {
    "godot": {
      "command": "npx",
      "args": ["-y", "@coding-solo/godot-mcp"],
      "env": {
        "GODOT_PATH": "C:/Users/akino/Desktop/Godot_v4.6.1-stable_win64.exe",
        "DEBUG": "false"
      }
    }
  }
}
```

**`GODOT_PATH`** — full path to your Godot executable. Optional if `godot` is on your system PATH.
Use forward slashes on Windows inside JSON values.

**`DEBUG`** — set `"true"` to enable verbose server-side logging when troubleshooting.

---

## Step 2: Verify

```bash
# In Claude Code terminal
/mcp   # should show "godot" server as connected
```

Ask Claude: "Use get_godot_version to confirm Godot is reachable."

---

## Available Tools (14)

| Tool | What it does |
|---|---|
| `launch_editor` | Open the Godot editor for a project path |
| `run_project` | Run a project in Godot debug mode (launches Godot subprocess) |
| `get_debug_output` | Retrieve console and debug messages from the running project |
| `stop_project` | Stop a running project |
| `get_godot_version` | Check the Godot version of the configured executable |
| `list_projects` | Find Godot projects under a directory |
| `get_project_info` | Read project structure and metadata |
| `create_scene` | Generate a new scene file |
| `add_node` | Add a node to an existing scene |
| `load_sprite` | Import a texture as a Sprite2D node |
| `export_mesh_library` | Convert 3D content for GridMap |
| `save_scene` | Persist a scene to disk |
| `get_uid` | Retrieve a file's UID (Godot 4.4+ required) |
| `update_project_uids` | Refresh all UID references in a project |

---

## Typical Workflow

```
1. Claude: use list_projects to find the game project
2. Claude: use run_project to launch the scene
3. Claude: use get_debug_output to read errors and print statements
4. Claude: fix the code, save, re-run
5. Claude: use stop_project when done
```

---

## godot-mcp vs GDAI MCP

| Feature | godot-mcp (this) | GDAI MCP |
|---|---|---|
| Cost | Free | Paid |
| Setup | npm / settings.json only | Godot plugin + Python server |
| Editor must be open | No — launches subprocess | Yes — required |
| Screenshot tools | None | `get_editor_screenshot`, `get_running_scene_screenshot` |
| Scene node manipulation | Basic (create, add node) | Full (40 tools) |
| Debug output capture | `get_debug_output` | `clear_output_logs` + error list |
| Script edit in editor | No | Yes (`edit_file`, `attach_script`) |
| Best for | Headless verify, CI, debug loops | Full autonomous editor control |

**Use godot-mcp when**: you need to run the game and read debug output without keeping the editor open.
**Use GDAI MCP when**: you need screenshots, live scene editing, or full editor control.

---

## Windows Notes

- Pure Node.js — works on Windows without modification
- Set `GODOT_PATH` to the full path with forward slashes
- `npx -y` auto-installs the package on first use; no separate `npm install` needed

---

## See Also

- `cookbook/mcp/gdai-mcp.md` — full editor control with screenshots
- `cookbook/mcp/gdscript-lsp.md` — inline GDScript diagnostics in Claude Code
