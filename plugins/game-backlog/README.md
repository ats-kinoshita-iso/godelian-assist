# game-backlog

Prioritized game feature backlog for the designer-programmer workflow.

## Skills

| Skill | When to use |
|-------|-------------|
| `backlog-init` | Once, at project start — seed the backlog from your GDD or concept |
| `backlog-status` | Any time — print the feature board as a priority table |
| `next-feature` | Advance the next queued feature to spec/approval |
| `add-feature` | Add a new feature mid-session with title, brief, and priority |

## Backlog file

Each game project maintains its own `plans/game-backlog.json`. This plugin defines
the schema and the skills for managing it — the file itself lives in the game project,
not in godelian-assist.

## Status flow

```
queued → pending_approval → in_progress → done
                ↑                ↑
           /next-feature     /spec-review (approved)
```
