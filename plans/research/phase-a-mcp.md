# Phase A Research: MCP Servers and GDScript LSP Bridge

**Date**: 2026-03-27
**Status**: Complete — ready for implementation

---

## Findings Summary

All configurations below are copy-paste ready and verified against live documentation.

---

## 1. GDAI MCP Server

**Type**: Godot plugin + Python MCP server (NOT npm)
**Version**: 0.3.1 (released February 28, 2026)
**Godot minimum**: 4.1+
**Cost**: Paid — download from gdaimcp.com

### Installation

The MCP server is a Python script (`gdai_mcp_server.py`) bundled inside the Godot plugin.
It runs via `uv`, which is already installed at:
`C:\Users\akino\AppData\Local\Programs\Python\Python312\Scripts\uv.exe`

**Step 1** — Download plugin zip from gdaimcp.com and extract into `res://addons/gdai-mcp-plugin-godot/`
**Step 2** — Enable plugin in Godot: Project → Project Settings → Plugins → GDAI MCP → Enable
**Step 3** — Add MCP entry (global or per-project `.claude/settings.json`):

```json
{
  "mcpServers": {
    "gdai-mcp": {
      "command": "C:\\Users\\akino\\AppData\\Local\\Programs\\Python\\Python312\\Scripts\\uv.exe",
      "args": [
        "run",
        "C:/path/to/your/game/addons/gdai-mcp-plugin-godot/gdai_mcp_server.py"
      ]
    }
  }
}
```

**Step 4** — Open the game project in the Godot editor before using any tools.

### Critical Requirement

**The Godot editor MUST be open.** GDAI MCP communicates with the running editor process. It does NOT work headless.

### Screenshot Tool Names (confirmed)

- `get_editor_screenshot` — captures the full Godot editor window
- `get_running_scene_screenshot` — captures the game viewport when a scene is running

These are NOT `capture_screenshot` or `take_screenshot`.

### Full Tool List (40 tools)

**Project**: get_project_info, get_filesystem_tree, search_files, uid_to_project_path, project_path_to_uid
**Scene**: get_scene_tree, get_scene_file_content, create_scene, open_scene, delete_scene, add_scene, play_scene, stop_running_scene
**Node**: add_node, delete_node, duplicate_node, move_node, update_property, add_resource, set_anchor_preset, set_anchor_values
**Script**: get_open_scripts, view_script, create_script, attach_script, edit_file
**Editor**: get_godot_errors, get_editor_screenshot, get_running_scene_screenshot, execute_editor_script, clear_output_logs

### Windows 11 Notes

- Windows Defender compatibility was fixed in v0.2.9 — use v0.3.0+ (currently 0.3.1)
- v0.3.0 added Windows x64 double precision build support
- Use forward slashes in paths inside the JSON, or escape backslashes
- No Claude Code-specific Windows issues documented

---

## 2. Coding-Solo godot-mcp (Lightweight Alternative)

**Type**: npm MCP server
**Package**: `@coding-solo/godot-mcp`
**Node.js**: >= 18.0.0 (installed: 24.14.1 ✅)

### settings.json Entry

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

`GODOT_PATH` points to our confirmed Godot location: `C:\Users\akino\Desktop\Godot_v4.6.1-stable_win64.exe`

### Does Editor Need to Be Open?

No — tools like `run_project`, `get_debug_output`, `stop_project` launch Godot as a subprocess. `launch_editor` opens the editor on demand. Much more headless-friendly than GDAI MCP.

### All 14 Tools

launch_editor, run_project, get_debug_output, stop_project, get_godot_version, list_projects, get_project_info, create_scene, add_node, load_sprite, export_mesh_library, save_scene, get_uid (requires Godot 4.4+), update_project_uids

**No screenshot tool** — headless only.

### Windows Notes

Pure Node.js, cross-platform. Use forward slashes in `GODOT_PATH` JSON value.

---

## 3. twaananen/claude-code-gdscript (LSP Plugin)

**Type**: Claude Code plugin (NOT an MCP server — no settings.json entry needed)
**Godot minimum**: 4.3+ recommended (for `--lsp-port` support)
**Port**: 6005 (default)

### Install

```bash
# In Claude Code terminal:
claude plugin marketplace add twaananen/claude-code-gdscript
claude plugin install gdscript@claude-code-gdscript --scope project
```

No settings.json change — uses Claude Code's plugin system.

### Key Environment Variables

| Variable | Default | Notes |
|---|---|---|
| `GODOT_LSP_MODE` | `auto` | auto = plugin launches Godot; attach = manual |
| `GODOT_EDITOR_PATH` | `godot` | Must set to full path on Windows |
| `GODOT_LSP_PORT` | `6005` | TCP port |
| `GODOT_PROJECT_ROOT` | (auto) | Override auto-detection |

**Set for this machine**:
```
GODOT_EDITOR_PATH=C:/Users/akino/Desktop/Godot_v4.6.1-stable_win64.exe
```

### Windows Note

LSP plugin may fail on Windows if `uv_spawn` can't find npm-linked executables (known Claude Code issue #33955). Workaround: use full path to Node.js. In `auto` mode the plugin auto-launches Godot — no manual step needed.

### What It Provides

NOT callable MCP tools. Provides inline language intelligence: GDScript diagnostics (type errors, undefined variables), hover docs, go-to-definition, completions. Claude Code sees these automatically when editing `.gd` files.

---

## 4. Sods2/claude-code-gdscript-lsp (Zero-Deps LSP Plugin)

**Type**: Claude Code plugin (NOT MCP server)
**Node.js**: 18+, zero runtime npm dependencies
**Port**: 6005 (default), via `GODOT_LSP_PORT`

### Install on Windows (manual — .sh scripts don't work natively)

```bash
# 1. Clone the repo
git clone https://github.com/Sods2/claude-code-gdscript-lsp.git
cd claude-code-gdscript-lsp/bridge

# 2. Build the bridge
npm install
npm run build

# 3. Link globally
npm link

# 4. Register and install
claude plugin marketplace add /absolute/path/to/claude-code-gdscript-lsp
claude plugin install gdscript-lsp
```

### Godot Must Be Running

Unlike twaananen's plugin, this one does NOT auto-launch Godot. Start Godot manually:

```bash
# Option A: Open editor normally (LSP starts automatically)
"C:/Users/akino/Desktop/Godot_v4.6.1-stable_win64.exe" --editor --path /path/to/project

# Option B: Headless LSP only
"C:/Users/akino/Desktop/Godot_v4.6.1-stable_win64.exe" --editor --headless --lsp-port 6005
```

### Key Environment Variables

| Variable | Default | Notes |
|---|---|---|
| `GODOT_LSP_PORT` | `6005` | TCP port |
| `GODOT_LSP_HOST` | `127.0.0.1` | Server host |
| `GODOT_LSP_DEBUG` | `false` | Verbose bridge logging |
| `GODOT_PATH` | `godot` | Path to Godot (for helper scripts) |

---

## Recommended Stack for godelian-assist Users

| Goal | Tool | Why |
|---|---|---|
| Full editor control + screenshots | GDAI MCP | 40 tools, live editor read/write, screenshots |
| Run game + debug output (no editor) | godot-mcp | Free, npm, headless-friendly, no purchase required |
| GDScript type errors in Claude Code | twaananen/claude-code-gdscript | Auto-launches Godot, simpler setup |
| GDScript LSP with explicit control | Sods2/claude-code-gdscript-lsp | Zero-deps, manual Godot launch |

**Minimum viable setup** (covers 80% of use cases, free):
1. `godot-mcp` for running projects and reading debug output
2. `twaananen/claude-code-gdscript` for inline GDScript diagnostics

**Full setup** (complete autonomous loop):
1. GDAI MCP (paid) for editor control and screenshots
2. Either LSP plugin for inline diagnostics

---

## Environment Confirmed on This Machine

- Godot: `C:\Users\akino\Desktop\Godot_v4.6.1-stable_win64.exe` ✅
- Node.js: 24.14.1 at `C:\Program Files\nodejs\` ✅
- npm: 11.11.0 ✅
- uv: 0.11.2 at `C:\Users\akino\AppData\Local\Programs\Python\Python312\Scripts\uv.exe` ✅
- gdlint: installed ✅
