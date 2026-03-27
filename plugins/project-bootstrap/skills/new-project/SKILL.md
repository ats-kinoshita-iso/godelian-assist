---
name: new-project
description: Initialize a new Godot 4.x project with the full godelian-assist structure.
invocation: /new-project
---

Set up a fresh Godot 4.x game project with every godelian-assist convention in place before writing a single line of gameplay code.

## Input

Provide:
- Project name (used for directory name and `project.godot` `config/name`)
- Game genre or rough description (helps pre-populate CLAUDE.md context)
- Optional: Godot version (defaults to 4.6.x)

## The 7 Initialization Steps

Execute in order. Confirm completion of each before proceeding to the next.

### Step 1 — project.godot

Create `project.godot` with:
```ini
; Engine configuration file.
[gd_resource type="ProjectSettings" load_steps=1 format=3]

[resource]
config/name="ProjectName"
config/features=PackedStringArray("4.6", "Forward Plus")
config/icon="res://icon.svg"
```

Set `application/run/main_scene` once the main scene is created (leave absent until then).

### Step 2 — .gitignore

Create `.gitignore`:
```
# Godot
.godot/
*.translation
export_presets.cfg

# Editor
.nova/
.vscode/settings.json

# OS
.DS_Store
Thumbs.db
```

### Step 3 — Directory Structure

Create the standard layout via `setup-directories` skill. Run `/setup-directories` now.

### Step 4 — CLAUDE.md

Create `CLAUDE.md` in the project root. Include:
- Project name and genre
- Godot executable path (from godelian-assist CLAUDE.md)
- GDScript style rules: static typing everywhere, `class_name` on every script, `snake_case` identifiers
- Quality commands: `gdlint src/`, `gdformat --check src/`, `godot --headless --import`
- Autoload names: EventBus, GameManager, SaveManager
- Active plugin list
- godelian-assist workflow summary (brief → spec → implement → feature-complete)

### Step 5 — Autoloads

Run `/setup-autoloads` to create the three singleton scripts and register them in `project.godot`.

### Step 6 — game-backlog.json

Create `plans/game-backlog.json` with an empty features array:
```json
{
  "project": "ProjectName",
  "features": []
}
```

Run `/backlog-init` to initialize the backlog with the designer's first priorities.

### Step 7 — Verify

Confirm the project opens cleanly:
```bash
godot --headless --import
```

No errors in stdout = initialization complete.

## Completion Report

After all 7 steps, output:
```
Project initialized: ProjectName/
  ✓ project.godot
  ✓ .gitignore
  ✓ Directory structure (see /setup-directories output)
  ✓ CLAUDE.md
  ✓ Autoloads: EventBus, GameManager, SaveManager
  ✓ plans/game-backlog.json
  ✓ Headless import: clean

Next step: run /brief to describe your first feature.
```
