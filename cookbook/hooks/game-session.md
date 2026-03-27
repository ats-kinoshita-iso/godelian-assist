# Game Session Hooks — Recipe

<!-- last-updated: 2026-03-27 -->

This hook set bookends every Claude Code game development session with automatic
backlog orientation at start and a quality summary at the end.

---

## The hooks.json block

Add to your game project's `.claude/settings.json`:

```json
{
  "hooks": [
    {
      "event": "PostToolUse",
      "command": "python plans/session_start.py",
      "matcher": {
        "tool_name": ["Read"],
        "run_once_per_session": true
      }
    },
    {
      "event": "Stop",
      "command": "python plans/session_end.py"
    }
  ]
}
```

Stack with the designer-approval gate by merging the `hooks` arrays:

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
    },
    {
      "event": "PostToolUse",
      "command": "python plans/session_start.py",
      "matcher": {
        "tool_name": ["Read"],
        "run_once_per_session": true
      }
    },
    {
      "event": "Stop",
      "command": "python plans/session_end.py"
    }
  ]
}
```

---

## session_start.py

Drop into `plans/session_start.py`:

```python
"""Print backlog status at the start of a Claude Code session."""
from __future__ import annotations

import json
from pathlib import Path

BACKLOG = Path(__file__).parent / "game-backlog.json"

if not BACKLOG.exists():
    print("[game-session] No game-backlog.json found. Run /backlog-init to create one.")
else:
    data = json.loads(BACKLOG.read_text(encoding="utf-8"))
    features = data.get("features", [])
    in_progress = [f for f in features if f["status"] == "in_progress"]
    pending = [f for f in features if f["status"] == "pending_approval"]
    queued = [f for f in features if f["status"] == "queued"]
    done = [f for f in features if f["status"] == "done"]

    print(f"\n[game-session] {data.get('game_title', 'Game')} — Session Start")
    print(f"  Done: {len(done)}  |  In progress: {len(in_progress)}  |"
          f"  Pending approval: {len(pending)}  |  Queued: {len(queued)}")
    if in_progress:
        print(f"  Current: #{in_progress[0]['id']} {in_progress[0]['title']}")
    elif pending:
        print(f"  Awaiting approval: #{pending[0]['id']} {pending[0]['title']}")
    elif queued:
        print(f"  Next up: #{queued[0]['id']} {queued[0]['title']} — run /next-feature to begin")
    print()
```

---

## session_end.py

Drop into `plans/session_end.py`:

```python
"""Print a brief quality summary at the end of a Claude Code session."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

BACKLOG = Path(__file__).parent / "game-backlog.json"

print("\n[game-session] Session End")

# Backlog summary
if BACKLOG.exists():
    data = json.loads(BACKLOG.read_text(encoding="utf-8"))
    features = data.get("features", [])
    in_progress = [f for f in features if f["status"] == "in_progress"]
    if in_progress:
        print(f"  In progress: #{in_progress[0]['id']} {in_progress[0]['title']}")
        print("  Run /feature-complete when the designer approves, or commit WIP with 'wip:' prefix.")

# Quick gdlint pass on any modified .gd files
result = subprocess.run(
    ["git", "diff", "--name-only", "--diff-filter=AM"],
    capture_output=True, text=True
)
gd_files = [f for f in result.stdout.splitlines() if f.endswith(".gd")]
if gd_files:
    print(f"  Modified GDScript files this session: {len(gd_files)}")
    print("  Run 'gdlint <files>' before committing.")

print()
```

---

## Session protocol (add to your game project's CLAUDE.md)

```markdown
## Game Development Session Protocol

At the start of each session:
- Backlog status is printed automatically (game-session Start hook)
- If a feature is `in_progress`, continue it — do not start a new one
- If a feature is `pending_approval`, present the spec to the designer

During the session:
- Run /brief before creating any new .gd or .tscn files
- Run /spec-review to approve before implementation
- Run /iterate for targeted fixes after playtesting

At the end of each session:
- Run /feature-complete if the designer has approved the feature feel
- If not complete, commit with a `wip:` prefix commit message
- Clear ACTIVE_SPEC.md only when the feature is fully done
```

---

## See Also

- `cookbook/hooks/designer-approval.md` — PreToolUse spec gate
- `plugins/designer-brief/` — brief, spec-review, iterate, playtest-debrief, feature-complete
- `plugins/game-backlog/` — backlog-init, backlog-status, next-feature, add-feature
