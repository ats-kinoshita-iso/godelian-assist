# designer-brief

Formal designer-to-programmer handoff workflow for Godot game development.

## Skills

| Skill | When to use |
|-------|-------------|
| `brief` | Describe a new mechanic or feature in plain language — Claude produces an implementation spec |
| `spec-review` | Review and approve/revise/reject Claude's spec before any code is written |
| `iterate` | After playtesting — propose and apply the minimal fix for a specific complaint |
| `playtest-debrief` | After a playtest session — rank observations and let Claude map them to files |
| `feature-complete` | When feel is approved — run quality gate, clean up, commit |

## The workflow

```
Designer → /brief → Claude produces spec
        → /spec-review → Designer approves
        → Claude implements (no further input needed)
        → Designer playtests
        → /playtest-debrief → Claude fixes issues
        → /feature-complete → committed and done
```

## Hooks

`hooks.json` adds a `PreToolUse` warning when Claude is about to create a `.gd`, `.tscn`,
or `.tres` file without an active approved spec. See `cookbook/hooks/designer-approval.md`
for the `check_spec.py` script to drop into your game project.
