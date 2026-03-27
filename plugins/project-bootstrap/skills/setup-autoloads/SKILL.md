---
name: setup-autoloads
description: Create the three core autoload singletons and register them in project.godot.
invocation: /setup-autoloads
---

Create EventBus, GameManager, and SaveManager singletons — the three autoloads required by the godelian-assist architecture — and register them in `project.godot`.

## Why These Three

- **EventBus** — decoupled signal bus; all cross-system events go through here, avoiding direct node references
- **GameManager** — global game state machine (menus, paused, playing, game-over); owns scene transitions
- **SaveManager** — serializes/deserializes game state to/from user://save.json; single source of truth for persistence

## GDScript Class Skeletons

Write these files exactly as shown. All properties and parameters are statically typed.

### src/autoloads/event_bus.gd

```gdscript
class_name EventBus
extends Node

## Central signal bus. All cross-system events are emitted and connected here.
## Usage: EventBus.health_changed.emit(actor, new_value)

# --- Player signals ---
signal player_died()
signal player_respawned(position: Vector3)

# --- Health signals ---
signal health_changed(actor: Node, new_health: int, max_health: int)
signal actor_died(actor: Node)

# --- UI signals ---
signal hud_update_requested()
signal scene_transition_started(scene_path: String)
signal scene_transition_finished()

# --- Game state signals ---
signal game_paused()
signal game_resumed()
signal save_requested()
signal load_requested()
```

### src/autoloads/game_manager.gd

```gdscript
class_name GameManager
extends Node

## Global game state machine. Owns scene transitions and pause control.

enum State { BOOT, MENU, PLAYING, PAUSED, GAME_OVER }

var current_state: State = State.BOOT
var current_scene_path: String = ""

func _ready() -> void:
	EventBus.scene_transition_started.connect(_on_scene_transition_started)

func change_scene(path: String) -> void:
	EventBus.scene_transition_started.emit(path)
	await get_tree().create_timer(0.3).timeout
	get_tree().change_scene_to_file(path)
	current_scene_path = path
	EventBus.scene_transition_finished.emit()

func set_state(new_state: State) -> void:
	current_state = new_state
	get_tree().paused = (new_state == State.PAUSED)
	if new_state == State.PAUSED:
		EventBus.game_paused.emit()
	elif new_state == State.PLAYING:
		EventBus.game_resumed.emit()

func _on_scene_transition_started(_path: String) -> void:
	pass
```

### src/autoloads/save_manager.gd

```gdscript
class_name SaveManager
extends Node

## Serializes and deserializes game state to user://save.json.

const SAVE_PATH: String = "user://save.json"

var _data: Dictionary = {}

func save() -> void:
	var file: FileAccess = FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file == null:
		push_error("SaveManager: cannot open save file for writing")
		return
	file.store_string(JSON.stringify(_data, "\t"))
	file.close()

func load_save() -> bool:
	if not FileAccess.file_exists(SAVE_PATH):
		return false
	var file: FileAccess = FileAccess.open(SAVE_PATH, FileAccess.READ)
	if file == null:
		return false
	var result: Variant = JSON.parse_string(file.get_as_text())
	file.close()
	if result is Dictionary:
		_data = result
		return true
	return false

func get_value(key: String, default_value: Variant = null) -> Variant:
	return _data.get(key, default_value)

func set_value(key: String, value: Variant) -> void:
	_data[key] = value
```

## project.godot [autoload] Registration

Add this block to `project.godot` (or update the existing `[autoload]` section):

```ini
[autoload]
EventBus="*res://src/autoloads/event_bus.gd"
GameManager="*res://src/autoloads/game_manager.gd"
SaveManager="*res://src/autoloads/save_manager.gd"
```

The `*` prefix means "instantiate as node" (required for autoloads in Godot 4.x).

## Verify

After writing files and updating `project.godot`:
```bash
godot --headless --import
```

No errors = autoloads registered correctly. All three will be accessible as global singletons at runtime.
