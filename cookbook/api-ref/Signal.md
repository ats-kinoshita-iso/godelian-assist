# API Reference: Signal (GDScript)

**Godot 4.x** — Signals are first-class typed objects in GDScript 2.0

---

## Purpose

Signals implement the Observer pattern in Godot — a node announces an event without knowing who is listening. This decouples emitters from receivers, which is essential for cross-scene communication and the EventBus pattern.

---

## Declaring Signals

```gdscript
# Untyped (no parameters)
signal player_died()

# Typed parameters — always use typed declarations
signal health_changed(actor: Node, new_health: int, max_health: int)
signal item_collected(item: ItemData, position: Vector3)
signal animation_completed(anim_name: String)
```

**Always use typed signal declarations.** Untyped parameters (`signal foo(a, b)`) bypass the GDScript type checker.

---

## Emitting

```gdscript
# Emit with no arguments
player_died.emit()

# Emit with typed arguments
health_changed.emit(self, current_health, max_health)
item_collected.emit(item_data, global_position)
```

---

## Connecting

### Basic connection

```gdscript
# Connect in _ready()
some_node.health_changed.connect(_on_health_changed)

func _on_health_changed(actor: Node, new_health: int, max_health: int) -> void:
	pass
```

### Connection flags

```gdscript
# CONNECT_DEFERRED — handler runs at the end of the frame (safe for scene tree mutation)
body_entered.connect(_on_body_entered, CONNECT_DEFERRED)

# CONNECT_ONE_SHOT — auto-disconnects after first emission
anim_player.animation_finished.connect(_on_intro_done, CONNECT_ONE_SHOT)

# CONNECT_REFERENCE_COUNTED — allows multiple connects; disconnect N times to remove
signal_name.connect(handler, CONNECT_REFERENCE_COUNTED)

# Combine flags with bitwise OR
signal_name.connect(handler, CONNECT_DEFERRED | CONNECT_ONE_SHOT)
```

### Lambda / Callable connection

```gdscript
button.pressed.connect(func() -> void: GameManager.change_scene("res://scenes/ui/menu.tscn"))

# With capture — be careful: captured variables are evaluated at connection time
var level_id: int = current_level
button.pressed.connect(func() -> void: GameManager.load_level(level_id))
```

---

## Disconnecting

```gdscript
func _exit_tree() -> void:
	EventBus.health_changed.disconnect(_on_health_changed)
```

Always disconnect in `_exit_tree()` when:
- The receiver node is freed before the emitter
- The connection was made across scene boundaries

Failure to disconnect when the receiver is freed causes `Object was freed` errors.

---

## Checking Connections

```gdscript
if EventBus.health_changed.is_connected(_on_health_changed):
	EventBus.health_changed.disconnect(_on_health_changed)

# Get all connections:
var connections: Array[Dictionary] = EventBus.health_changed.get_connections()
```

---

## await with Signals

```gdscript
# Suspend until the signal fires — returns signal arguments
await get_tree().create_timer(2.0).timeout

# With typed return
var result: String = await anim_player.animation_finished
print("Animation completed: ", result)

# One-shot pattern with await
func play_death_sequence() -> void:
	anim_player.play("die")
	await anim_player.animation_finished
	queue_free()
```

---

## Typed GDScript Usage Example

```gdscript
class_name HealthComponent
extends Node

signal health_changed(actor: Node, new_health: int, max_health: int)
signal actor_died(actor: Node)

@export var max_health: int = 100
var current_health: int = 100

func _ready() -> void:
	current_health = max_health

func apply_damage(amount: int) -> void:
	current_health = clampi(current_health - amount, 0, max_health)
	health_changed.emit(get_parent(), current_health, max_health)
	EventBus.health_changed.emit(get_parent(), current_health, max_health)
	if current_health == 0:
		actor_died.emit(get_parent())

func heal(amount: int) -> void:
	current_health = clampi(current_health + amount, 0, max_health)
	health_changed.emit(get_parent(), current_health, max_health)
```

---

## Common Pitfalls

- **Godot 3 string-based connect** — `connect("signal_name", self, "_method")` is removed in Godot 4; use `signal_name.connect(method_reference)`
- **Godot 3 `yield`** — replaced by `await` in Godot 4
- **Connecting to a freed object** — if the emitter is freed before disconnect, signal connections dangle; use `CONNECT_ONE_SHOT` or `is_instance_valid()` checks
- **Forgetting `()` in emit** — `health_changed.emit` (no parens) is a no-op; always call `health_changed.emit(...)`
- **Untyped parameters silently accept wrong types** — always declare typed parameters to catch argument mismatches at parse time
