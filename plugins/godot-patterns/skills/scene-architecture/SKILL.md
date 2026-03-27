---
name: scene-architecture
description: >-
  Design or review a Godot 4.x scene hierarchy for a game entity or system.
  Produces a node tree diagram, explains ownership and responsibility of each
  node, and flags anti-patterns. Use when asked to "design the scene for X",
  "review my scene structure", or "how should I structure X in Godot".
---
> **Godot version**: Godot 4.x (4.0+). All code examples use GDScript 2.0 and are not compatible with Godot 3.


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

## CharacterBody3D FPS Controller — Correct Node Layout

The two most common mistakes when hand-building an FPS scene are wrong
`CollisionShape3D` offset and wrong `Head` (camera) height:

```
CharacterBody3D          ← origin = feet (y=0 in world = floor contact point)
├── CollisionShape3D     ← offset y = capsule_height / 2  (e.g. y=0.9 for 1.8 m capsule)
│     CapsuleShape3D(height=1.8, radius=0.4)
├── Head (Node3D)        ← offset y ≈ 1.6  (eye height above feet, NOT y=0.75)
│   └── Camera3D
├── HealthComponent
├── StaminaComponent
└── AudioStreamPlayer3D
```

| Node | Required Y offset | Consequence if wrong |
|------|-------------------|----------------------|
| `CollisionShape3D` | `capsule_height / 2` (0.9 m) | Capsule floats or sinks into floor |
| `Head` | ~1.6 m from feet | Camera inside body (y=0) or below capsule center (y=0.75) |

## Hand-Authoring .tscn Files Outside the Editor

Godot reports **"missing dependencies"** for files that physically exist when
the `[gd_scene]` header or `[ext_resource]` blocks contain invalid or fake UIDs.

```ini
# CORRECT — omit uid= entirely; Godot assigns real UIDs on first open
[gd_scene load_steps=3 format=3]

# ext_resource requires: type, path, id — uid= is optional, omit if hand-writing
[ext_resource type="Script" path="res://src/player/player.gd" id="1_player"]
[ext_resource type="PackedScene" path="res://scenes/hud.tscn" id="2_hud"]

# sub_resource: only type and id in header; properties follow
[sub_resource type="CapsuleShape3D" id="CapsuleShape3D_1"]
radius = 0.4
height = 1.8

# Root node: NO parent= attribute
[node name="Player" type="CharacterBody3D"]
script = ExtResource("1_player")

# All other nodes: parent= required
[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.9, 0)
shape = SubResource("CapsuleShape3D_1")
```

| Mistake | Fix |
|---------|-----|
| `uid="uid://my_fake_name"` on `[gd_scene]` | Omit `uid=` entirely |
| `uid="uid://my_fake_name"` on `[ext_resource]` | Omit `uid=` — Godot resolves by `path=` |
| Root `[node]` has `parent="."` | Root must have **no** `parent=` attribute |

## Output Format

Produce the node tree, then a table of signals, then the anti-pattern review.
End with a recommended next step (e.g., "Extract the weapon slot into its own scene").
