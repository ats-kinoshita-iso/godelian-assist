---
name: backlog-init
description: >-
  Initialize plans/game-backlog.json from the designer's game description or
  GDD, seeding it with an initial prioritized feature list.
---

## When to use

Run once when starting a new game project, after `/new-project` (project-bootstrap).
Also run when onboarding an existing project that doesn't yet have a backlog.

## The game-backlog.json schema (v1)

Claude creates `plans/game-backlog.json` with this structure:

```json
{
  "game_title": "My Game",
  "genre": "3D action-platformer",
  "version": "1.0",
  "features": [
    {
      "id": 1,
      "title": "Player movement",
      "brief": "CharacterBody3D movement with jump, coyote time, and jump buffering.",
      "status": "queued",
      "priority": 1,
      "spec": null,
      "notes": null
    },
    {
      "id": 2,
      "title": "Player dash",
      "brief": "Forward dash covering 4m in 0.1s, 0.5s cooldown, dust particle.",
      "status": "queued",
      "priority": 2,
      "spec": null,
      "notes": null
    }
  ]
}
```

### Field reference

| Field | Type | Meaning |
|---|---|---|
| `id` | int | Unique, auto-incrementing |
| `title` | string | Short feature name (3-5 words) |
| `brief` | string | One sentence: what it does and why |
| `status` | string | `queued` / `in_progress` / `pending_approval` / `done` |
| `priority` | int | 1 = highest; lower number = do first |
| `spec` | string or null | Path to `plans/specs/<slug>.md` once created |
| `notes` | string or null | Designer notes, revision history |

## How Claude generates the initial feature list

1. **Reads the designer's input** — a GDD, a concept document, or a free-form description.
2. **Extracts features** — identifies discrete, implementable mechanics (not systems in the abstract).
   A "player controller" is too large; "player double-jump" is right-sized.
3. **Writes initial briefs** — one sentence per feature describing what it does.
4. **Assigns initial priorities** — core movement and systems first, polish and
   optional content last.
5. **Presents the list** — before writing the file, Claude shows the proposed feature list
   to the designer for priority confirmation.
6. **Writes `plans/game-backlog.json`** only after designer confirms the list and order.

## After initialization

- Run `/backlog-status` to see the board.
- Run `/next-feature` to advance the highest-priority queued feature to `pending_approval`
  and generate its implementation spec.
- Add features at any time with `/add-feature`.
