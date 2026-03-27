---
name: backlog-status
description: >-
  Display the current game feature board as a prioritized table showing what
  is done, in progress, and queued.
---

## What it shows

Claude reads `plans/game-backlog.json` and outputs a Markdown table sorted by priority:

```
## Game Backlog — My Game

| # | Priority | Title | Status | Notes |
|---|----------|-------|--------|-------|
| 1 | 1 | Player movement | ✅ done | |
| 2 | 2 | Player dash | 🔄 in_progress | spec at plans/specs/player-dash.md |
| 3 | 3 | Double-jump | ⏳ pending_approval | awaiting designer review |
| 4 | 4 | Enemy patrol AI | 📋 queued | |
| 5 | 5 | Health system | 📋 queued | |
| 6 | 6 | Save/load | 📋 queued | |

Current sprint: Player dash (#2)
Next up: Double-jump (#3) — pending your approval of the spec.
```

## Status meanings

| Status | Icon | Meaning |
|---|---|---|
| `queued` | 📋 | Not started — waiting for its turn |
| `in_progress` | 🔄 | Claude is actively implementing |
| `pending_approval` | ⏳ | Spec written — awaiting designer approval |
| `done` | ✅ | Implemented, tested, and designer-approved |

## The one-at-a-time rule

Only one feature should be `in_progress` at a time. If `/backlog-status` shows
multiple `in_progress` features, something went wrong — Claude will flag it and
ask which to continue and which to pause.

`pending_approval` features may stack: it is fine to have one `in_progress` and
one `pending_approval` simultaneously (e.g., Claude is implementing feature 2 while
feature 3's spec is waiting for designer review).

## When to run

- At the start of every session (or automatically via the `game-session` Start hook)
- After completing a feature (`/feature-complete` runs it automatically)
- When the designer adds a feature (`/add-feature` runs it automatically)
- Any time you want a quick orientation
