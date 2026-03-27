---
name: screenshot-review
description: >-
  Use GDAI MCP's screenshot tools to visually verify that a scene or feature
  matches design intent after implementation, and integrate visual feedback
  into the quality loop.
---

> **Godot version**: Godot 4.6+ (GDScript 2.0). Never use Godot 3 syntax.
> Godot 3 → 4 quick-ref: `KinematicBody`→`CharacterBody3D`, `yield()`→`await`,
> `move_and_slide(vel, UP)`→`velocity` property + `move_and_slide()`,
> `connect("s", self, "cb")`→`signal.connect(callback)`, `Spatial`→`Node3D`,
> `onready var`→`@onready var`, `export var`→`@export var`.

## When to use screenshot review

Screenshot review answers questions that code inspection cannot:

- Does the character appear where expected in the scene?
- Is the UI layout correct (health bar top-left, minimap top-right)?
- Are collision debug shapes visible and sized correctly?
- Does the particle effect play and look as described?
- Is the camera framing correct for the level geometry?

Use it **after implementation and before marking a feature complete**.
Do NOT use it as a substitute for logic testing — bugs in damage calculation or
save/load won't appear in a screenshot.

## Prerequisites

- GDAI MCP installed and active (see `cookbook/mcp/gdai-mcp.md`)
- Godot editor open with the project loaded
- The GDAI MCP plugin enabled (Project → Project Settings → Plugins)

## Screenshot tool names (GDAI MCP)

```
get_editor_screenshot       — captures the full Godot editor window
get_running_scene_screenshot — captures the game viewport while a scene plays
```

> **Important**: the tools are named `get_editor_screenshot` and
> `get_running_scene_screenshot`. They are NOT named `capture_screenshot`,
> `take_screenshot`, or `screenshot`. Using the wrong name will return a tool-not-found error.

## The review workflow

1. **Run the scene** using GDAI MCP:
   ```
   use play_scene with path "res://scenes/player/player.tscn"
   ```

2. **Capture the viewport** once the scene is running:
   ```
   use get_running_scene_screenshot
   ```

3. **Compare to design intent** — describe what the screenshot shows and compare against
   the feature's accepted criteria from the spec in `plans/specs/ACTIVE_SPEC.md`.

4. **Capture the editor** to check scene tree layout or node placement:
   ```
   use get_editor_screenshot
   ```

5. **Stop the scene** when done:
   ```
   use stop_running_scene
   ```

## What to look for in a screenshot

**Scene/node placement:**
- Is the root node visible and positioned correctly?
- Do child nodes appear in the expected hierarchy (check editor screenshot)?
- Is nothing floating at the origin by accident?

**Collision shapes (enable debug in Godot: Debug → Visible Collision Shapes):**
- Do CollisionShape3D outlines match the visual mesh size?
- Are hitboxes and hurtboxes distinct and non-overlapping at rest?

**UI layout:**
- Are Control nodes anchored correctly (health bar hugs top-left, not centered)?
- Is text readable at 1080p?
- Does the HUD disappear behind 3D geometry (CanvasLayer required)?

**Particles and VFX:**
- Is the particle system visible and emitting in the right direction?
- Does the effect start and stop at the right time?

## Screenshot review is NOT a replacement for

- `gdlint` — style and formatting issues do not appear in screenshots
- GdUnit4 tests — gameplay logic correctness requires unit tests
- Debug output (`get_debug_output` via godot-mcp) — runtime errors are invisible in screenshots
- Playtesting — feel, responsiveness, and difficulty are not visually verifiable

## Integrating with the quality gate

The full verification sequence for a completed feature:

```
1. gdlint <files>                   → style
2. gdformat --check <files>         → formatting
3. godot --headless --check-only    → type errors (or LSP bridge)
4. GdUnit4 tests                    → logic correctness
5. play_scene + get_running_scene_screenshot → visual correctness
6. get_debug_output                 → runtime errors
```

All six steps should pass before calling `/feature-complete`.

## Without GDAI MCP (fallback)

If GDAI MCP is not installed, replace steps 5–6 with:
- `run_project` via godot-mcp + `get_debug_output` for runtime errors
- Manual visual check: ask the designer to open the scene in the editor and confirm placement
- Document in the feature commit: "visual verification: manual editor check by designer"
