---
name: lsp-setup
description: >-
  Configure and verify the GDScript Language Server bridge so Claude Code sees
  type errors, undefined variables, and completions in .gd files in real time.
---

> **Godot version**: Godot 4.6+ (GDScript 2.0). Never use Godot 3 syntax.
> Godot 3 → 4 quick-ref: `KinematicBody`→`CharacterBody3D`, `yield()`→`await`,
> `move_and_slide(vel, UP)`→`velocity` property + `move_and_slide()`,
> `connect("s", self, "cb")`→`signal.connect(callback)`, `Spatial`→`Node3D`,
> `onready var`→`@onready var`, `export var`→`@export var`.

## What the LSP setup gives you

Without the LSP bridge, Claude Code reads `.gd` files as plain text — no type information,
no error detection. With the bridge active, Claude sees a live diagnostic feed from Godot's
own GDScript compiler: the same errors you'd see in the editor Output panel, available
before the game ever runs.

- Type mismatch errors caught the moment code is written
- Undefined variable and missing method references flagged inline
- Auto-completions for Godot node methods, signals, and `@export` fields
- Go-to-definition for classes and functions across the project

## Architecture

```
Godot editor process
  └─ LSP server (TCP :6005)
       └─ bridge process (stdio ↔ TCP adapter)
            └─ Claude Code plugin system
```

The bridge is a thin adapter — it translates between Claude Code's stdio-based plugin
protocol and Godot's TCP language server. No separate language intelligence is added;
all analysis comes from Godot itself.

## Setup (follow cookbook/mcp/gdscript-lsp.md)

Refer to `cookbook/mcp/gdscript-lsp.md` for the complete install guide. The short version:

**Option A — Auto-launch (recommended):**
```bash
claude plugin marketplace add twaananen/claude-code-gdscript
claude plugin install gdscript@claude-code-gdscript --scope project
```
Add to `.claude/settings.json`:
```json
{ "env": { "GODOT_EDITOR_PATH": "C:/Users/akino/Desktop/Godot_v4.6.1-stable_win64.exe" } }
```

**Option B — Zero-deps bridge (manual Godot start):**
Clone Sods2/claude-code-gdscript-lsp, build with `npm install && npm run build`, link, install.
Start Godot's LSP manually: `godot --editor --lsp-port 6005`

## Verify the bridge is working

1. Open a `.gd` file that has a deliberate type error:
   ```gdscript
   var speed: int = "too fast"  # wrong type
   ```
2. Without asking Claude anything, check if it mentions or flags the error.
3. If Claude catches it unprompted — the bridge is live. Remove the error.

If Claude does not catch it:
- Check that Godot is running (Option B) or that `GODOT_EDITOR_PATH` is set (Option A)
- Run `claude plugin list` — confirm the plugin appears
- Check the Claude Code plugin debug log for LSP connection errors

## LSP vs gdlint — which catches what

| Check | LSP bridge | gdlint |
|---|---|---|
| Type mismatches | Yes | No |
| Undefined variables | Yes | No |
| Wrong method signatures | Yes | No |
| Style violations (snake_case etc.) | No | Yes |
| Line length | No | Yes |
| Missing `class_name` | No | Yes (configurable) |

Run both: LSP for type correctness during editing, gdlint before committing.

## Restarting the bridge

If the bridge drops connection (Godot restarts, project changes):
- Option A: the bridge auto-reconnects when Godot restarts — no action needed
- Option B: restart the `godot --editor --lsp-port 6005` process; the bridge reconnects automatically
