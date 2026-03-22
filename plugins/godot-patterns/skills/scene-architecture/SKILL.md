---
name: scene-architecture
description: >-
  Design or review a Godot 4.x scene hierarchy for a game entity or system.
  Produces a node tree diagram, explains ownership and responsibility of each
  node, and flags anti-patterns. Use when asked to "design the scene for X",
  "review my scene structure", or "how should I structure X in Godot".
---

Design or review a Godot 4.x scene hierarchy.

## Steps

1. **Clarify the entity** — identify what the scene represents (player, enemy, UI, level, etc.) and its primary responsibilities.

2. **Propose a node tree** — output a tree diagram using Godot node type names:
   ```
   CharacterBody3D (Player)
   ├── CollisionShape3D
   ├── MeshInstance3D
   ├── Camera3D
   ├── AnimationPlayer
   ├── AudioStreamPlayer3D (footsteps)
   └── Area3D (interaction_range)
       └── CollisionShape3D
   ```

3. **Explain each node** — one line per node: type choice rationale, signal connections, and `@export` variables it exposes.

4. **Identify sub-scenes** — call out nodes that should be extracted into their own `.tscn` files (reused entities, complex sub-trees with their own logic).

5. **Signal map** — list the signals this scene emits and which signals it listens to from children or the event bus.

6. **Anti-pattern check** — flag any of these if present:
   - Deep inheritance chains (prefer composition)
   - Direct `get_node("../../OtherEntity")` calls upward or sideways
   - Logic in scene root that belongs in a child node
   - Missing `CollisionShape` on physics bodies
   - Camera or UI nodes embedded in entity scenes (should be separate)

7. **Export variables** — list all `@export` properties the scene exposes for tuning in the Inspector, with suggested default values.

## Output Format

Produce the node tree, then a table of signals, then the anti-pattern review.
End with a recommended next step (e.g., "Extract the weapon slot into its own scene").
