---
name: setup-directories
description: Create the standard godelian-assist directory layout for a Godot 4.x project.
invocation: /setup-directories
---

Create the canonical directory structure for a godelian-assist Godot project.

## Standard Layout

```
project-root/
├── src/
│   ├── autoloads/          # EventBus, GameManager, SaveManager
│   ├── player/             # Player scenes and scripts
│   ├── enemies/            # Enemy types
│   ├── ui/                 # HUD, menus, overlays
│   ├── environment/        # Level geometry, props, triggers
│   ├── systems/            # Reusable gameplay systems (health, inventory, etc.)
│   └── utils/              # Pure-function helpers, constants
├── assets/
│   ├── textures/
│   ├── audio/
│   │   ├── music/
│   │   └── sfx/
│   ├── fonts/
│   └── models/
├── scenes/
│   ├── levels/             # Full level scenes
│   └── ui/                 # Screen-level UI scenes
├── addons/                 # Godot plugins (GdUnit4, etc.)
├── plans/
│   ├── specs/              # ACTIVE_SPEC.md and approved specs
│   └── research/           # Phase research gate documents
└── tests/                  # GdUnit4 test scenes and scripts
```

## Creation Commands

```bash
mkdir -p src/autoloads src/player src/enemies src/ui src/environment src/systems src/utils
mkdir -p assets/textures assets/audio/music assets/audio/sfx assets/fonts assets/models
mkdir -p scenes/levels scenes/ui
mkdir -p addons
mkdir -p plans/specs plans/research
mkdir -p tests
```

## .gdignore Files

Add a `.gdignore` file to directories Godot should not import as resources. This prevents Godot from trying to parse test scripts, plans docs, and tooling as game assets:

`tests/.gdignore` — prevents GdUnit4 runner confusion with non-test files
`plans/.gdignore` — prevents Markdown files from generating import errors

Content of each `.gdignore` is simply an empty file:
```bash
touch tests/.gdignore
touch plans/.gdignore
```

## Why .gdignore Matters

Godot scans every file under `res://` that lacks a `.gdignore` in its directory. Markdown files, Python scripts, and JSON files outside the standard resource types generate warning spam in the editor. The `.gdignore` suppresses this entirely for the affected directory tree.

## Verify

After creating directories:
```bash
godot --headless --import
```

A clean import with no "file not found" or resource parse warnings confirms the structure is correct.
