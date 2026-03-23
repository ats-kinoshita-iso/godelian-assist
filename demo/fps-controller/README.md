# FPS Character Controller — godelian-assist Demo

Demonstrates every godelian-assist plugin in a complete, working Godot 4.x FPS controller.

## Plugin Usage Map

| File | Plugins Applied |
|------|----------------|
| Scene hierarchy below | `godot-patterns/scene-architecture` |
| HealthComponent, StaminaComponent | `godot-patterns/node-composition` |
| Signal connections | `godot-patterns/signal-design` |
| All .gd files | `gdscript-guide/typing-guide`, `gdscript-guide/idioms` |
| player.gd `_physics_process` | `gdscript-guide/performance` |
| player_stats.gd | `godot-patterns/resource-patterns` |
| State machine in player.gd | `godot-patterns/state-machine` |
| test_*.gd | `test-quality/test-gen-godot` |
| Quality gate commands | `godot-code-quality/quality` |

## Scene Hierarchy  (`scene-architecture` skill output)

```
Player (CharacterBody3D)          ← owns movement physics
├── CollisionShape3D              ← capsule, 1.8m tall, 0.4m radius
├── MeshInstance3D                ← body mesh (hidden in first-person)
├── Head (Node3D)                 ← pivots up/down for mouse look
│   ├── Camera3D                  ← first-person view
│   └── WeaponMount (Node3D)      ← weapon scenes attach here
├── HealthComponent (Node)        ← emits health_changed, died
├── StaminaComponent (Node)       ← emits stamina_changed, depleted
└── AudioStreamPlayer3D           ← footstep/jump sounds
```

**Design decisions** (`node-composition` skill):
- Health and stamina are **child component nodes** (not base class fields) — they can be dropped
  onto any entity (enemies, destructibles) without code changes
- Camera lives under `Head` so vertical mouse look only rotates `Head`, horizontal rotates the
  whole `Player` body — keeps physics and camera separated
- `WeaponMount` is a dedicated `Node3D` so weapon scenes attach without modifying player code

**Signal map** (`signal-design` skill):

| Signal | Emitter | Receiver | Parameters |
|--------|---------|----------|------------|
| `health_changed` | HealthComponent | HUD, GameManager | `new_value: float` |
| `died` | HealthComponent | GameManager, respawn | — |
| `stamina_changed` | StaminaComponent | HUD | `new_value: float` |
| `stamina_depleted` | StaminaComponent | Player (blocks sprint) | — |
| `stamina_recovered` | StaminaComponent | Player (re-enables sprint) | — |

## How to Use in Godot

1. Copy `src/` into your Godot project's `src/player/` directory
2. Copy `src/resources/` into your project's `data/` directory
3. Create a scene with `CharacterBody3D` as root, attach `player.gd`
4. Add child nodes per the hierarchy above; assign exported properties
5. Create a `PlayerStats` resource (`.tres`) and assign to `@export var stats`
6. Copy `tests/` into your project's `tests/` directory
7. Run quality gate: `gdlint src/player/ && gdformat --check src/player/`

## Quality Gate (`godot-code-quality/quality` skill)

```bash
# GDScript lint
gdlint src/player/player.gd src/player/health_component.gd src/player/stamina_component.gd

# Format check
gdformat --check src/player/

# GdUnit4 tests
godot --headless -s addons/gdUnit4/bin/GdUnitCmdTool.gd --add res://tests
```
