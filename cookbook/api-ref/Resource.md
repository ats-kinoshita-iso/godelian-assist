# API Reference: Resource

**Godot 4.x** | `extends RefCounted → Object`

---

## Purpose

`Resource` is the base class for all Godot data objects that can be saved to disk as `.tres` or `.res` files and referenced in `.tscn` scenes. Subclass it to create custom game data types (AttackData, ItemData, LevelConfig, etc.) that designers can author in the editor.

---

## Key Properties

| Property | Type | Description |
|---|---|---|
| `resource_path` | `String` | The `res://` or `user://` path where this resource is saved. Empty for unsaved resources. |
| `resource_name` | `String` | Optional human-readable name (shown in editor). |

---

## @export Annotation

Properties marked `@export` are serialized when the resource is saved and editable in the Godot Inspector.

```gdscript
class_name EnemyConfig
extends Resource

@export var display_name: String = ""
@export var max_health: int = 100
@export var move_speed: float = 3.5
@export var attack_damage: int = 10
@export var death_vfx: PackedScene
@export var loot_table: Array[ItemData] = []

@export_group("Detection")
@export var aggro_radius: float = 8.0
@export var sight_angle_degrees: float = 120.0

@export_subgroup("Combat")
@export var attack_cooldown: float = 1.2
@export var attack_range: float = 1.5
```

Supported export types: all primitives, `String`, `Vector2/3/4`, `Color`, `NodePath`, `Resource` subclasses, `Array[T]`, `Dictionary`, `PackedScene`, `AudioStream`, `Texture2D`, enums.

---

## Custom Subclass Pattern

```gdscript
# src/data/item_data.gd
class_name ItemData
extends Resource

enum ItemType { CONSUMABLE, EQUIPMENT, KEY_ITEM }

@export var item_id: String = ""
@export var display_name: String = ""
@export var item_type: ItemType = ItemType.CONSUMABLE
@export var icon: Texture2D
```

Save instances as `.tres` files: `res://assets/data/items/health_potion.tres`

---

## Key Methods

### `load(path: String) -> Variant` (global function)

Loads a resource from disk. Returns the cached version if already loaded.

```gdscript
var config: EnemyConfig = load("res://assets/data/enemies/slime.tres") as EnemyConfig
```

### `ResourceLoader.load(path: String, type_hint: String = "", cache_mode: CacheMode = CACHE_MODE_REUSE) -> Resource`

More control over caching. Use `CACHE_MODE_IGNORE` to force a fresh load.

### `save(path: String = "") -> Error` (via ResourceSaver)

```gdscript
var result: Error = ResourceSaver.save(my_resource, "user://save_slot_1.tres")
```

### `duplicate(subresources: bool = false) -> Resource`

Creates a copy. Without `subresources = true`, nested sub-resources are shared (not copied).

```gdscript
var config_copy: EnemyConfig = original_config.duplicate(true)
config_copy.max_health = 200   # does not affect original
```

### `emit_changed() -> void`

Signals that the resource has changed. Useful for editor tools and reactive systems.

---

## Signals

### `changed()`

Emitted when `emit_changed()` is called. Connect to refresh UI or recalculate derived data.

---

## Typed GDScript Usage Example

```gdscript
class_name LootTable
extends Resource

@export var entries: Array[LootEntry] = []
@export var guaranteed_drop: ItemData

func roll() -> ItemData:
	var roll_value: float = randf()
	var cumulative: float = 0.0
	for entry: LootEntry in entries:
		cumulative += entry.weight
		if roll_value <= cumulative:
			return entry.item
	return guaranteed_drop
```

---

## Common Pitfalls

- **Editing a loaded resource mutates the cached singleton** — always `duplicate()` before modifying a resource that was loaded from disk if you don't want the change to be global
- **`@export` on typed arrays requires Godot 4.1+** — `@export var items: Array[ItemData]` is not available in 4.0
- **`null` vs missing resource** — `load()` returns `null` if the path doesn't exist; always null-check the result
- **Godot 3 `preload()` inside a class** — use `load()` in `_ready()` instead; `preload()` works but only for compile-time constants
- **ResourceSaver vs FileAccess** — use `ResourceSaver.save()` for `.tres` files; use `FileAccess` + `JSON` for save game data
