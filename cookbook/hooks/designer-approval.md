# Designer Approval Gate — Hook Recipe

<!-- last-updated: 2026-03-27 -->

This hook warns Claude when it is about to create or edit a Godot source file (`.gd`, `.tscn`,
`.tres`) without an active approved spec. It enforces the brief → spec → approve → implement
workflow from the `designer-brief` plugin.

---

## What it does

Before any `Write` or `Edit` tool call that targets a Godot source file, the hook runs
`plans/check_spec.py`. That script checks for `plans/specs/ACTIVE_SPEC.md`.

- If the file **exists**: the hook exits 0 silently — implementation proceeds.
- If the file **does not exist**: the hook prints a warning message and exits 0.

> The gate is a **warning, not a hard block** — Claude can still proceed if the context
> makes a spec unnecessary (e.g., rapid prototyping mode, or fixing a one-line typo).
> The warning ensures the omission is intentional, not accidental.

---

## Step 1: Add the hook to your game project's `.claude/settings.json`

```json
{
  "hooks": [
    {
      "event": "PreToolUse",
      "command": "python plans/check_spec.py",
      "matcher": {
        "tool_name": ["Write", "Edit"],
        "file_pattern": ".*\\.(gd|tscn|tres)$"
      }
    }
  ]
}
```

---

## Step 2: Create `plans/check_spec.py` in your game project

Drop this file into `plans/` — it is a standalone script with no dependencies:

```python
"""Pre-tool-use hook: warn if no approved spec is active before writing Godot files."""
from __future__ import annotations

import sys
from pathlib import Path

ACTIVE_SPEC = Path(__file__).parent / "specs" / "ACTIVE_SPEC.md"

if not ACTIVE_SPEC.exists():
    print(
        "\n[designer-brief] WARNING: No active spec found at plans/specs/ACTIVE_SPEC.md\n"
        "  Run /brief to generate a spec, then /spec-review to approve it before\n"
        "  creating or editing .gd / .tscn / .tres files.\n"
        "  To bypass: create an empty plans/specs/ACTIVE_SPEC.md for this session.\n",
        file=sys.stderr,
    )

# Always exit 0 — this is a warning, not a block.
sys.exit(0)
```

---

## Step 3: Create `plans/specs/` directory

```bash
mkdir -p plans/specs/done
mkdir -p plans/pending-approval
mkdir -p plans/pending-changes
```

---

## How ACTIVE_SPEC.md is managed

| Action | Effect on ACTIVE_SPEC.md |
|--------|--------------------------|
| Designer approves a spec | Claude writes the spec content to `ACTIVE_SPEC.md` |
| Feature marked complete | Claude clears / removes `ACTIVE_SPEC.md` |
| Designer rejects a spec | Claude clears `ACTIVE_SPEC.md`, feature stays queued |
| Rapid prototyping | Create empty `ACTIVE_SPEC.md` to silence the warning |

---

## Bypassing during rapid prototyping

When iterating quickly and you don't want to go through the full brief/spec cycle:

```bash
# Silence the gate for the session
echo "# Prototyping — spec waived" > plans/specs/ACTIVE_SPEC.md

# Remove it when done prototyping
rm plans/specs/ACTIVE_SPEC.md
```

---

## Integration with game-backlog

When a feature moves from `queued` → `in_progress` via `/next-feature`, Claude
automatically creates the spec file and sets `ACTIVE_SPEC.md`. The gate is
satisfied without any manual step.

---

## See Also

- `plugins/designer-brief/skills/brief/SKILL.md` — how to write a brief
- `plugins/designer-brief/skills/spec-review/SKILL.md` — how to review a spec
- `cookbook/hooks/game-session.md` — the full session hook set
