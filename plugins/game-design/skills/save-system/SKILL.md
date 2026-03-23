---
name: save-system
description: >-
  Design a save/load system for a Godot 4.x game: what data to persist, choosing
  between ConfigFile vs JSON vs binary, the ISaveable interface pattern, auto-save
  triggers, and handling format version migration. Use when asked to "design the
  save system", "how do I save game progress?", or "implement save/load".
---

Design and implement a save/load system for a Godot 4.x action-RPG.

## What to Persist

Decide per-category:

| Category | Persist? | Format |
|----------|----------|--------|
| Player stats (HP, level, XP) | Yes | Save file |
| Inventory items + quantities | Yes | Save file |
| World state (doors, chests opened) | Yes | Save file |
| Quest progress | Yes | Save file |
| Settings (volume, graphics) | Yes | ConfigFile (separate) |
| Scene layout, enemy positions | No | Hardcoded in `.tscn` |
| NPC dialogue state | Situational | Save file if branching |

## Format Comparison

| Format | API | Best for |
|--------|-----|---------|
| `ConfigFile` | `config.set_value(section, key, val)` | Settings, simple key-value data |
| JSON | `JSON.stringify()` / `JSON.parse()` | Human-readable save data, modding support |
| Binary (Resource) | `ResourceSaver.save()` | Complex nested data, automatic type handling |

**Recommendation for action-RPGs**: JSON for saves (human-readable, easy to debug), ConfigFile for settings.

## ISaveable Interface Pattern

Define a standard interface so any node can opt into the save system:

```gdscript
# i_saveable.gd
class_name ISaveable extends Node

## Return a Dictionary of data to save. Keys must be stable across versions.
func save_data() -> Dictionary:
    return {}

## Restore state from previously saved Dictionary.
func load_data(data: Dictionary) -> void:
    pass

## Unique identifier for this saveable (used as dictionary key).
func save_id() -> StringName:
    return StringName(name)
```

## Save Manager (Autoload)

```gdscript
# save_manager.gd  — registered as Autoload "SaveManager"
class_name SaveManager extends Node

const SAVE_PATH: String = "user://save_game.json"
const SAVE_VERSION: int = 1

func save() -> void:
    var save_data: Dictionary[StringName, Dictionary] = {}
    for node: Node in get_tree().get_nodes_in_group("saveable"):
        if node is ISaveable:
            save_data[node.save_id()] = node.save_data()

    var envelope: Dictionary = {
        "version": SAVE_VERSION,
        "timestamp": Time.get_unix_time_from_system(),
        "data": save_data,
    }
    var file: FileAccess = FileAccess.open(SAVE_PATH, FileAccess.WRITE)
    file.store_string(JSON.stringify(envelope, "\t"))
    file.close()

func load_save() -> bool:
    if not FileAccess.file_exists(SAVE_PATH): return false
    var file: FileAccess = FileAccess.open(SAVE_PATH, FileAccess.READ)
    var envelope: Dictionary = JSON.parse_string(file.get_as_text())
    file.close()
    _migrate(envelope)
    var save_data: Dictionary = envelope.get("data", {})
    for node: Node in get_tree().get_nodes_in_group("saveable"):
        if node is ISaveable and save_data.has(node.save_id()):
            node.load_data(save_data[node.save_id()])
    return true
```

## Auto-Save Triggers

```gdscript
# Trigger save on: checkpoint reached, level exit, periodic timer
func _ready() -> void:
    EventBus.checkpoint_reached.connect(func(_pos: Vector3) -> void: SaveManager.save())
    EventBus.level_completed.connect(func(_id: StringName) -> void: SaveManager.save())
    $AutoSaveTimer.timeout.connect(SaveManager.save)  # every 5 minutes
```

## Version Migration

```gdscript
func _migrate(envelope: Dictionary) -> void:
    var version: int = envelope.get("version", 0)
    if version < 1:
        # v0 -> v1: rename "hp" key to "health"
        var data: Dictionary = envelope.get("data", {})
        for key: StringName in data:
            if data[key].has("hp"):
                data[key]["health"] = data[key]["hp"]
                data[key].erase("hp")
        envelope["version"] = 1
```

## Steps

1. Decide what data to persist using the category table above.
2. Add nodes that need saving to the `"saveable"` group; implement `ISaveable`.
3. Create `SaveManager` as an Autoload and implement `save()` / `load_save()`.
4. Identify auto-save trigger points (checkpoint, level exit, timer).
5. Add a `version` field from day one and write a migration function for each format bump.
6. Test: save mid-game, quit, reload — verify all state restored correctly.
