---
name: iterate
description: >-
  Propose and apply the minimal code change to address a specific gameplay
  complaint, without redesigning the surrounding system.
---

## When to use iterate vs. a new brief

Use `iterate` when a **system already exists** and needs targeted tuning:
- "The dash feels too slow" → tune a constant
- "The coyote time window is too generous" → change a timer value
- "The particle effect fires too late" → adjust an emit delay
- "The health bar doesn't update when damage is blocked" → fix a signal connection

Use a **new brief** when the system's architecture needs to change:
- "The dash should be directional, not just forward" → new design
- "The health system needs a shield layer" → new component

The distinction: if the fix touches the approach, use a brief. If it touches the values or
a missing edge case, use iterate.

## The iteration request format

Describe what felt wrong, when it happens, and what you expected:

```
What felt wrong: The dash covers the distance too slowly — feels like a slide, not a snap.
When it happens: Every time I press the dash button.
What I expected: Instant position change, or so fast it looks instant (≤0.1s).
Priority: Critical — breaks the game feel entirely.
```

Short form is also fine:
```
Dash speed: too slow. Should feel instant. High priority.
```

## How Claude responds to an iteration request

1. **Locates the responsible code** — reads the relevant file(s) and finds the specific
   variable, function, or signal that controls the complained behavior.
2. **Proposes the minimal diff** — shows exactly what will change (before/after),
   with no other modifications to the file:
   ```
   # src/player/dash_component.gd  line 14
   # BEFORE:
   var dash_duration: float = 0.3
   # AFTER:
   var dash_duration: float = 0.08
   ```
3. **Waits for approval** before making any change.
4. **Applies the approved diff**, runs `gdlint`, runs relevant GdUnit4 tests.
5. **Reports**: what changed, test result, what to check in the editor.

## The minimal diff rule

Claude makes only the change needed to address the specific complaint.
It does not clean up surrounding code, rename variables, refactor functions,
or improve anything not directly related to the iteration request.

If Claude notices a separate issue while reading the file, it will mention it
as an aside — but not fix it unless the designer adds it to the iteration request.

## Stacking iterations

Multiple iteration requests can be batched in one `playtest-debrief` session.
Claude processes them in priority order (Critical → High → Medium → Low) and
presents all proposed diffs before applying any of them.

## What iterate does NOT do

- Does not redesign the system
- Does not move nodes in the scene tree
- Does not change signal names or parameters (that would break other connections)
- Does not add new features — use a new brief for that
