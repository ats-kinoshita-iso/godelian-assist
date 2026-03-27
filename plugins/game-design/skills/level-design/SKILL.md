---
name: level-design
description: >-
  Design a 3D level for a Godot 4.x action-RPG: layout principles, encounter
  pacing, navigation flow, implementing geometry with GridMap or CSGMesh,
  marking spawn/trigger zones with Area3D, and wiring level events to game
  systems via signals. Use when asked to "design a level", "lay out this area",
  or "how should I structure level scenes in Godot?"
---
> **Godot version**: Godot 4.x (4.0+). All code examples use GDScript 2.0 and are not compatible with Godot 3.


Design a 3D level for a Godot 4.x action-RPG.

## Layout Principles

A well-paced action-RPG level follows a rhythm of **tension → release → tension**:

1. **Entry zone** — safe, establishes visual language and orientation
2. **Encounter zone A** — small group of weak enemies; teaches core mechanic
3. **Resource node** — health/mana pickup, rewarding exploration
4. **Encounter zone B** — harder group or elite; pressure builds
5. **Shortcut or optional branch** — rewards thorough players
6. **Boss room or objective** — climax; clear visual framing (lighting, scale)
7. **Exit / checkpoint** — release of tension, save point

## Godot Scene Structure for a Level

```
Level_Forest_01 (Node3D)
├── Environment (WorldEnvironment + DirectionalLight3D)
├── Geometry (Node3D)
│   ├── Terrain (GridMap or MeshInstance3D)
│   ├── Props (Node3D — rocks, trees, barrels)
│   └── Architecture (CSGCombiner3D for prototyping)
├── Navigation (NavigationRegion3D)
│   └── NavigationMesh
├── Triggers (Node3D)
│   ├── SpawnZone_A (Area3D + CollisionShape3D)
│   ├── SpawnZone_B (Area3D + CollisionShape3D)
│   ├── Checkpoint (Area3D + CollisionShape3D)
│   └── LevelExit (Area3D + CollisionShape3D)
└── Spawners (Node3D)
    ├── EnemySpawner_A (EnemySpawner)
    └── EnemySpawner_B (EnemySpawner)
```

## Prototyping with CSGMesh

Use CSG (Constructive Solid Geometry) for fast blockout. Replace with proper meshes before shipping.

```gdscript
# In editor: Add CSGBox3D, CSGCylinder3D, CSGCombiner3D
# Set material to a solid color for readability during blockout
# CSG nodes: use CSGCombiner3D > CSGBox3D with operation = OPERATION_SUBTRACTION for doorways
```

## Spawn Zones with Area3D

```gdscript
# spawn_zone.gd
class_name SpawnZone extends Area3D

@export var enemies_to_spawn: Array[PackedScene] = []
@export var spawn_once: bool = true

signal zone_cleared

var _spawned: bool = false
var _alive_count: int = 0

func _ready() -> void:
    body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node3D) -> void:
    if _spawned and spawn_once: return
    if not body.is_in_group("player"): return
    _spawn_enemies()
    _spawned = true

func _spawn_enemies() -> void:
    for scene: PackedScene in enemies_to_spawn:
        var enemy: Node3D = scene.instantiate()
        add_child(enemy)
        _alive_count += 1
        enemy.tree_exited.connect(_on_enemy_died)

func _on_enemy_died() -> void:
    _alive_count -= 1
    if _alive_count <= 0:
        zone_cleared.emit()
```

## Navigation Mesh Setup

1. Add `NavigationRegion3D` to the level root.
2. Set `NavigationMesh` resource; bake after geometry is placed.
3. Enemy agents use `NavigationAgent3D` as a child node.
4. Rebake after moving large geometry: `NavigationServer3D.bake_from_source_geometry_data()`.

## Connecting Level Events to Game Systems

```gdscript
# level_manager.gd
func _ready() -> void:
    $Triggers/Checkpoint.body_entered.connect(_on_checkpoint_reached)
    $Triggers/LevelExit.body_entered.connect(_on_exit_reached)
    for zone: SpawnZone in $Triggers.get_children():
        zone.zone_cleared.connect(_on_zone_cleared.bind(zone))

func _on_checkpoint_reached(body: Node3D) -> void:
    if body.is_in_group("player"):
        EventBus.checkpoint_reached.emit(global_position)

func _on_exit_reached(body: Node3D) -> void:
    if body.is_in_group("player"):
        EventBus.level_completed.emit(level_id)
```

## Platform Height Budget (Jump Physics)

When placing platforms, calculate reachable height from the player's jump stats:

```
max_jump_height = jump_velocity² / (2 × gravity)

# Default Godot gravity = 9.8 m/s²
# jump_velocity = 4.5  →  max_jump_height ≈ 1.03 m
# jump_velocity = 6.0  →  max_jump_height ≈ 1.84 m
```

Use this to space platforms so each step is reachable with a running jump,
and mark "intended shortcut" platforms ~10 % above max height (barely missable).

| Jump velocity | Max height | Comfortable step | Challenge step |
|---------------|-----------|-----------------|----------------|
| 4.5 m/s | 1.03 m | 0.7–0.8 m | 0.9–1.0 m |
| 6.0 m/s | 1.84 m | 1.2–1.4 m | 1.6–1.8 m |

## Steps

1. Sketch the layout on paper first — identify entry, encounters, branching, exit.
2. Calculate the player's max jump height from `jump_velocity` in their stats resource.
3. Build the scene hierarchy as shown above.
4. Prototype geometry with CSGMesh; place spawn zones and trigger volumes.
5. Set up NavigationRegion3D and bake the nav mesh.
6. Wire Area3D signals to the level manager.
7. Playtest pacing: time-to-first-encounter, downtime between fights, overall duration.
