---
name: ui-signals
description: Wire UI controls to gameplay through EventBus signals — no direct node references across scene boundaries.
invocation: /ui-signals
---

Connect UI controls to gameplay systems using EventBus signals and local button.pressed signals, following the one-directional data flow rule.

## Signal Flow Rule

```
Gameplay → EventBus.emit() → UI updates
UI input  → EventBus.emit() → Gameplay reacts
```

UI nodes never hold references to gameplay nodes. Gameplay nodes never hold references to UI nodes. Everything crosses scene boundaries through EventBus.

## EventBus Signals for UI

Declare UI-related signals on EventBus (`src/autoloads/event_bus.gd`):

```gdscript
# UI update signals (gameplay → UI)
signal health_changed(actor: Node, new_health: int, max_health: int)
signal stamina_changed(actor: Node, new_stamina: float, max_stamina: float)
signal gold_changed(new_amount: int)
signal item_added_to_hotbar(item: ItemData, slot_index: int)
signal dialogue_started()
signal dialogue_ended()

# UI action signals (UI → gameplay)
signal pause_requested()
signal resume_requested()
signal inventory_open_requested()
signal inventory_close_requested()
```

## Button Connection Pattern

Connect `pressed` locally in `_ready()`. Emit to EventBus — do not call gameplay directly:

```gdscript
func _ready() -> void:
	%PauseButton.pressed.connect(_on_pause_pressed)
	%InventoryButton.pressed.connect(_on_inventory_pressed)

func _on_pause_pressed() -> void:
	EventBus.pause_requested.emit()

func _on_inventory_pressed() -> void:
	EventBus.inventory_open_requested.emit()
```

## Receiving Updates in UI

```gdscript
func _ready() -> void:
	EventBus.health_changed.connect(_on_health_changed)
	EventBus.gold_changed.connect(_on_gold_changed)

func _on_health_changed(actor: Node, new_health: int, max_health: int) -> void:
	if not actor.is_in_group("player"):
		return
	%HealthBar.value = float(new_health)

func _on_gold_changed(new_amount: int) -> void:
	%GoldLabel.text = str(new_amount)
```

## AnimationPlayer for UI Transitions

Use `AnimationPlayer` for show/hide transitions — not `Tween` for multi-property animations:

```gdscript
@onready var anim: AnimationPlayer = $AnimationPlayer

func show_panel() -> void:
	anim.play("slide_in")

func hide_panel() -> void:
	anim.play_backwards("slide_in")
	await anim.animation_finished
	hide()
```

Define animations in the editor. Name convention: `slide_in`, `fade_in`, `bounce_in`.

## Signal Cleanup

Disconnect signals when a UI node is removed from the tree to avoid dangling connections:

```gdscript
func _exit_tree() -> void:
	EventBus.health_changed.disconnect(_on_health_changed)
	EventBus.gold_changed.disconnect(_on_gold_changed)
```

Or use `CONNECT_ONE_SHOT` for connections that should auto-disconnect after one fire.

## Debugging Signal Flow

If a UI element stops updating, check:
1. Is the EventBus signal being emitted? (`print` inside the emitting code)
2. Is the connection established? (`EventBus.health_changed.get_connections()`)
3. Is `_ready()` running? (check node is in the tree when scene loads)
