---
name: configure-quality
description: Install and configure gdtoolkit, GdUnit4, and the pre-commit quality hook for a Godot project.
invocation: /configure-quality
---

Set up the complete GDScript quality gate: linting, formatting, and unit testing infrastructure.

## Install gdtoolkit

```bash
pip install gdtoolkit
```

Or with uv (preferred):
```bash
uv tool install gdtoolkit
```

Verify:
```bash
gdlint --version
gdformat --version
```

## .gdlintrc Configuration

Create `.gdlintrc` in the project root. Copy this file verbatim — it enforces godelian-assist conventions:

```yaml
# gdlintrc — GDScript linter configuration
rules:
  max-line-length: 100
  tab-characters: true
  function-arguments-number: 10

  # Naming conventions
  class-name: PascalCase
  function-name: snake_case
  variable-name: snake_case
  signal-name: snake_case
  constant-name: CONSTANT_CASE

  # Code quality
  no-elif-return: true
  no-unnecessary-pass: true

  # Static typing required
  disable:
    - function-preload-variable
```

## Install GdUnit4

1. Open the Godot editor
2. Go to AssetLib → search "GdUnit4" → install
3. Or download from https://github.com/MikeSchulze/gdUnit4 and drop into `addons/`

Enable in `project.godot`:
```ini
[editor_plugins]
enabled=PackedStringArray("res://addons/gdUnit4/plugin.cfg")
```

Verify: open Godot, run a test scene — GdUnit4 panel appears at the bottom.

## Quality Commands Reference

| Command | Purpose |
|---|---|
| `gdlint src/` | Lint all GDScript in src/ |
| `gdformat --check src/` | Check formatting without writing |
| `gdformat src/` | Auto-format (write) |
| `godot --headless --import` | Validate all .tscn/.tres files |
| `godot --headless -s addons/gdUnit4/bin/GdUnitCmdTool.gd` | Run GdUnit4 test suite headless |

## Pre-commit Quality Hook

Add to `.claude/settings.json` hooks section (or use the designer-brief plugin's hook as a model):

```json
{
  "event": "PreToolUse",
  "type": "command",
  "command": "gdlint ${file}",
  "matcher": {
    "tool_name": ["Write", "Edit"],
    "file_pattern": ".*\\.gd$"
  }
}
```

This runs gdlint on every `.gd` file before Claude writes it.

## Verify Setup

```bash
gdlint src/
gdformat --check src/
```

Both should exit 0 with no output on a fresh project. Any lint errors on your existing scripts should be fixed before beginning feature work.
