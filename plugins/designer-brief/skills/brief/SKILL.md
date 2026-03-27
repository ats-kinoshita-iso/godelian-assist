---
name: brief
description: >-
  Translate designer intent into a concrete implementation spec before any code
  is written. Produces a structured spec for designer approval.
---

## Purpose

The brief is the foundation of the designer-programmer handoff. Before Claude writes a single
line of GDScript or creates a single `.tscn` file, the designer's intent must be captured in
a structured format and turned into an implementation spec — then reviewed and approved.

This prevents the most common failure mode in AI game development: Claude implements
something technically correct but wrong for the game's feel and vision.

## The brief format

When describing a feature, use this structure:

```markdown
## Feature: <title>

**Intent**: One sentence — what this mechanic does and why it exists in the game.
**Feel**: How it should feel to the player (use visceral, player-perspective words:
  snappy, floaty, punchy, weighty, forgiving, tight, satisfying, scary).
**Constraints**: Hard limits — performance budget, must reuse existing nodes,
  max complexity, dependencies on other systems that must stay intact.
**Out of scope**: What this feature deliberately does NOT do. Prevents scope creep.
**Designer acceptance**: I will approve this feature when ___.
  (Be specific: "the dash covers 3 meters in 0.1 seconds with a visible dust particle.")
```

You do not have to fill every field in complete sentences — bullet points are fine.
The more specific the "Feel" and "Designer acceptance" fields, the better the spec.

## How Claude responds to a brief

1. **Reads and confirms understanding** — paraphrases the feature back in one sentence.
2. **Asks at most two clarifying questions** — only for genuinely ambiguous decisions that
   would change the architecture (e.g., "should the dash be cancelled by damage?").
3. **Produces the implementation spec** covering:
   - Node structure (scene tree with node types and names)
   - Signal map (name, parameters, emitter, receiver)
   - Custom Resource subclasses (fields and types)
   - Files to create (exact `res://` paths)
   - Files to modify (exact paths and what changes)
   - GDScript skeletons (class_name, signals, @export fields, method stubs — fully typed)
   - Test plan (what GdUnit4 tests will verify this feature)
4. **Writes spec to** `plans/specs/<feature-slug>.md`
5. **Sets** `plans/specs/ACTIVE_SPEC.md` to point to the new spec (or copies it there)
6. **Reports to designer**: "Spec ready at plans/specs/<slug>.md — review and reply 'approved' to proceed."

## The approval rule

**No files are created until the designer explicitly approves the spec.**

Claude does not begin writing `.gd` or `.tscn` files the moment a brief is given.
The spec review step is mandatory. This is enforced by the designer-approval hook
(see `cookbook/hooks/designer-approval.md`).

## Example

**Designer brief:**
```
## Feature: Player dash
**Intent**: Player dashes forward instantly, covering 4 meters, with a 0.5s cooldown.
**Feel**: Snappy and committed — once started, can't be cancelled. Feels powerful.
**Constraints**: Must not break existing jump/coyote time logic. No new autoloads.
**Out of scope**: No directional dash (forward only). No dash through walls.
**Designer acceptance**: Dash covers 4m in ≤0.1s; cooldown shown on HUD; dust particle plays.
```

**Claude produces:**
- Node: `DashComponent` (Node, child of Player) with `@export var dash_distance: float = 4.0` and `@export var cooldown: float = 0.5`
- Signal: `dash_started()`, `dash_ready()` (emitted by DashComponent, HUD connects to dash_ready)
- Files to create: `src/player/dash_component.gd`, `scenes/player/dash_trail.tscn`
- Files to modify: `scenes/player/player.tscn` (add DashComponent child), `src/ui/hud.gd` (connect dash_ready)
- Test plan: test dash distance, test cooldown prevents double-dash, test signal fires
