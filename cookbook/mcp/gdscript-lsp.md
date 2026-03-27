# GDScript LSP Bridge — Setup Guide

<!-- last-updated: 2026-03-27 -->

These Claude Code plugins bridge Godot's built-in GDScript Language Server (TCP) to Claude
Code's plugin system, giving Claude inline GDScript diagnostics, completions, hover docs, and
go-to-definition — without calling MCP tools. Claude sees type errors and undefined variables
the moment it writes code, not after running the game.

**Two options**: `twaananen/claude-code-gdscript` (auto-launches Godot) or
`Sods2/claude-code-gdscript-lsp` (zero-deps bridge, manual Godot start).

> These are **Claude Code plugins**, not MCP servers. There is no `settings.json` `mcpServers`
> entry — they install via `claude plugin`.

---

## How it works

```
Godot editor (TCP :6005) ←→ bridge (stdio) ←→ Claude Code plugin system
```

The bridge translates between Claude Code's stdio protocol and Godot's TCP LSP server.
Godot 4.x includes an LSP server that activates via `--lsp-port` flag.

---

## Option A: twaananen/claude-code-gdscript (Recommended — Auto-Launch)

**Godot minimum**: 4.3+ (for `--lsp-port` flag)
**Mode**: `auto` — the plugin launches a headless Godot LSP backend automatically. No manual Godot start required.

### Install

```bash
claude plugin marketplace add twaananen/claude-code-gdscript
claude plugin install gdscript@claude-code-gdscript --scope project
```

Use `--scope user` to enable across all your projects on this machine.

### Configure Godot path

On Windows the Godot executable is not on PATH, so set the environment variable in your project's `.claude/settings.json`:

```json
{
  "env": {
    "GODOT_EDITOR_PATH": "C:/Users/akino/Desktop/Godot_v4.6.1-stable_win64.exe"
  }
}
```

### Key environment variables

| Variable | Default | Notes |
|---|---|---|
| `GODOT_LSP_MODE` | `auto` | `auto` = plugin auto-launches Godot; `attach` = manual |
| `GODOT_EDITOR_PATH` | `godot` | Full path to Godot executable (required on Windows) |
| `GODOT_LSP_PORT` | `6005` | TCP port for LSP |
| `GODOT_PROJECT_ROOT` | (auto) | Override auto-detected project root |

### Verify

Open any `.gd` file in Claude Code. Introduce a deliberate type error:
```gdscript
var x: int = "this is wrong"
```
Claude should see the diagnostic without you asking. Remove the error when done.

### Windows note

If the plugin fails to start on Windows: the `uv_spawn` issue (Claude Code issue #33955) can prevent npm-linked executables from being found. Fix: set `GODOT_EDITOR_PATH` to the absolute path and restart Claude Code.

---

## Option B: Sods2/claude-code-gdscript-lsp (Zero-Deps Bridge)

**Differentiator**: Zero runtime npm dependencies. You control when Godot's LSP is running.
**Node.js**: 18+
**Godot**: 4.x any version

### Install on Windows (manual — install scripts are Unix-only)

```bash
# 1. Clone
git clone https://github.com/Sods2/claude-code-gdscript-lsp.git
cd claude-code-gdscript-lsp/bridge

# 2. Build
npm install
npm run build

# 3. Make globally available
npm link

# 4. Register and install in Claude Code
claude plugin marketplace add /absolute/path/to/claude-code-gdscript-lsp
claude plugin install gdscript-lsp

# 5. Restart Claude Code
```

### Start Godot's LSP server (required before each session)

```bash
# Option 1: Open editor normally — LSP starts automatically on port 6005
"C:/Users/akino/Desktop/Godot_v4.6.1-stable_win64.exe" --editor --path C:/path/to/project

# Option 2: Headless (no window)
"C:/Users/akino/Desktop/Godot_v4.6.1-stable_win64.exe" --editor --headless --lsp-port 6005
```

### Key environment variables

| Variable | Default | Notes |
|---|---|---|
| `GODOT_LSP_PORT` | `6005` | TCP port |
| `GODOT_LSP_HOST` | `127.0.0.1` | Server host |
| `GODOT_LSP_DEBUG` | `false` | Verbose bridge logging |

---

## Comparison: Option A vs Option B

| | twaananen (A) | Sods2 (B) |
|---|---|---|
| Auto-launch Godot | Yes | No — manual start |
| Zero runtime deps | No | Yes |
| Install complexity | Simple (2 commands) | Manual build + link |
| Windows install | Standard | Must use Git Bash / WSL for npm link |
| Godot minimum | 4.3+ | 4.x any |
| Auto-reconnect on restart | Yes | Yes |

**Recommendation**: Start with Option A (twaananen) — simpler setup. Switch to Option B if you want explicit control over the LSP lifecycle.

---

## What the LSP provides (both options)

- **Diagnostics**: type errors, undefined variables, wrong method signatures — shown inline
- **Hover**: type and doc info when Claude reads over a symbol
- **Go-to-definition**: jump to class/function/variable definitions in `.gd` files
- **Completions**: GDScript-aware completions for node methods, signals, exports
- **Symbols**: list all classes, functions, variables in the project

## What it does NOT provide

- MCP tool calls (no `run_project`, no `get_scene_tree`)
- Screenshot capture
- Scene file creation or editing
- Real-time game output

Pair with `godot-mcp` or GDAI MCP for those capabilities.

---

## The --lsp-port flag

Godot 4.3+ supports `--lsp-port <PORT>` to start the LSP server on a specific port.
Both plugins default to port **6005**. Override with `GODOT_LSP_PORT` if port 6005 is in use.

The flag is for the **editor** process: `godot --editor --lsp-port 6005`
Do NOT use `--headless` alone — the LSP requires the editor context.

---

## See Also

- `cookbook/mcp/gdai-mcp.md` — full editor control (scene creation, screenshots)
- `cookbook/mcp/godot-mcp-minimal.md` — run project and capture debug output
- `plugins/godot-code-quality/skills/lsp-setup/SKILL.md` — how to configure and verify
