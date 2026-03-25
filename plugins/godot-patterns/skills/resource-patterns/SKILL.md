---
name: resource-patterns
description: >-
  Design and implement Godot 4.x Resource subclasses for game data: character
  stats, item definitions, weapon configs, level configs. Covers when to use
  Resource vs Node, loading/saving .tres files, and sharing Resources across
  scenes. Use when asked to "design the data model for X", "should this be a
  Resource?", or "how do I share config data between scenes?"
---

Design and implement Godot 4.x Resource subclasses for game data.

## Resource vs Node — Decision Rule

Use a **Resource** when:
- Data is purely declarative (no `_process`, no scene tree presence needed)
- The same data is shared across multiple scenes (item definitions, stat blocks)
- Designers need to create/edit instances in the Inspector
- You want to serialize to `.tres` / `.res` files

Use a **Node** when:
- The entity needs lifecycle callbacks (`_ready`, `_process`)
- The entity must exist in the scene tree (visible, collidable, audible)
- The entity holds scene-local state that changes at runtime

## Defining a Custom Resource

```gdscript
# weapon_resource.gd
class_name WeaponResource extends Resource

@export var weapon_name: StringName = &"Sword"
@export var damage: float = 15.0
@export var attack_speed: float = 1.5       # attacks per second
@export var range: float = 1.8              # meters
@export_range(0.0, 1.0) var crit_chance: float = 0.1
@export var attack_animation: StringName = &"attack_slash"
@export var hit_sound: AudioStream
@export var icon: Texture2D
```

## Sharing Resources Across Scenes

Resources in Godot are **reference-counted and shared by default**. Assign the same `.tres` file
to multiple scenes — they all read from the same object.

```gdscript
# enemy.gd
class_name Enemy extends CharacterBody3D

@export var stats: CharacterStats   # assign sword_stats.tres in Inspector

func _ready() -> void:
    health = stats.max_health       # reads shared resource
```

**Caution**: if you modify a shared resource at runtime, all scenes using it see the change.
Use `stats.duplicate()` to get a per-instance copy when you need independent state.

## Loading Resources at Runtime

```gdscript
# Preload at script parse time (for known paths)
const PLAYER_STATS: CharacterStats = preload("res://data/player_stats.tres")

# Load at runtime (for dynamic paths)
func load_item(item_id: StringName) -> ItemResource:
    var path: String = "res://data/items/%s.tres" % item_id
    return load(path) as ItemResource
```

## Nested Resources

Resources can contain other Resources, enabling composition:

```gdscript
class_name CharacterStats extends Resource

@export var base_stats: BaseStats           # another Resource
@export var equipment_slots: Array[EquipmentSlot] = []
@export var abilities: Array[AbilityResource] = []
```

## Saving at Runtime (User Data)

```gdscript
func save_progress(path: String, data: SaveData) -> void:
    ResourceSaver.save(data, path)         # writes .tres or .res

func load_progress(path: String) -> SaveData:
    if not ResourceLoader.exists(path):
        return SaveData.new()
    return ResourceLoader.load(path) as SaveData
```

## Hand-Authoring .tres Files Outside the Editor

When writing `.tres` files by hand (e.g. committing baseline assets to source control),
the header format is **different** from what you might expect:

```ini
# CORRECT — type= must be the built-in base class, not your script class
[gd_resource type="Resource" script_class="PlayerStats" load_steps=2 format=3]

[ext_resource type="Script" path="res://src/resources/player_stats.gd" id="1_script"]

[resource]
script = ExtResource("1_script")   # REQUIRED — binds the object to your class
move_speed = 5.0
max_health = 100.0
```

**Common mistakes that cause "missing dependencies" / load failure:**

| Mistake | Correct |
|---------|---------|
| `type="PlayerStats"` | `type="Resource"` — `type=` is the C++ base class, not your script class |
| Missing `[ext_resource]` for the `.gd` | Declare the script as an ext_resource |
| Missing `script = ExtResource(...)` in `[resource]` | First property must bind the script |
| `load_steps` not counting the script ext_resource | `load_steps = <ext_resource count> + 1` |

**Rule:** always create `.tres` files via **File > New Resource** in the Godot editor;
hand-author only when the editor-generated file needs source-control-friendly edits.

## Steps

1. Identify what data needs to be shared or designed in the Inspector.
2. Create a `class_name MyResource extends Resource` file.
3. Add `@export` fields with explicit types and sensible defaults.
4. Create `.tres` instances via **File > New Resource** in the Godot editor — let
   the editor write the header; never set `type=` to your script class name.
5. Assign `.tres` files to scenes via `@export var` fields.
6. Use `resource.duplicate()` where per-instance mutable copies are needed.
