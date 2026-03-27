# API Reference: Area3D

**Godot 4.x** | `extends CollisionObject3D → Node3D → Node → Object`

---

## Purpose

`Area3D` detects when physics bodies or other areas overlap its collision shape. Use it for: trigger zones, pickup volumes, aggro ranges, damage zones, and hitbox/hurtbox pairs. It does **not** apply physics forces — it only detects.

---

## Key Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `monitoring` | `bool` | `true` | Whether this area detects overlapping bodies/areas. |
| `monitorable` | `bool` | `true` | Whether other areas can detect this area. |
| `priority` | `float` | `0.0` | Order of processing when multiple areas overlap. Higher = processed first. |
| `gravity_space_override` | `SpaceOverride` | `SPACE_OVERRIDE_DISABLED` | Override gravity inside this area. |
| `gravity` | `float` | `9.8` | Gravity magnitude when `gravity_space_override` is active. |
| `linear_damp_space_override` | `SpaceOverride` | `SPACE_OVERRIDE_DISABLED` | Override linear damping inside this area. |
| `audio_bus_override` | `bool` | `false` | Override the audio bus for sounds inside this area. |

---

## Key Methods

### `get_overlapping_bodies() -> Array[Node3D]`

Returns all `PhysicsBody3D` nodes currently overlapping this area. Safe to call from `_process`.

```gdscript
func _process(_delta: float) -> void:
	for body: Node3D in get_overlapping_bodies():
		if body.is_in_group("player"):
			_apply_damage_tick(body)
```

### `get_overlapping_areas() -> Array[Area3D]`

Returns all `Area3D` nodes currently overlapping this area.

### `has_overlapping_bodies() -> bool`

Returns `true` if any physics body is currently overlapping. Cheaper than `get_overlapping_bodies().is_empty()`.

### `overlaps_body(body: Node3D) -> bool`

Returns `true` if the specific body is overlapping.

### `overlaps_area(area: Area3D) -> bool`

Returns `true` if the specific area is overlapping.

---

## Signals

### `body_entered(body: Node3D)`

Emitted when a `PhysicsBody3D` enters the area. Fires during the physics step — use `CONNECT_DEFERRED` if the handler changes the scene tree.

### `body_exited(body: Node3D)`

Emitted when a `PhysicsBody3D` exits the area.

### `area_entered(area: Area3D)`

Emitted when another `Area3D` enters this area. Used for hitbox/hurtbox detection.

### `area_exited(area: Area3D)`

Emitted when another `Area3D` exits this area.

---

## Typed GDScript Usage Example

```gdscript
class_name DamageZone
extends Area3D

## Deals damage per second to all players inside.

@export var damage_per_second: float = 10.0

var _bodies_inside: Dictionary = {}   # ghost frame mitigation

func _ready() -> void:
	collision_layer = CollisionLayer.TRIGGER
	collision_mask  = CollisionLayer.PLAYER
	body_entered.connect(_on_body_entered, CONNECT_DEFERRED)
	body_exited.connect(_on_body_exited, CONNECT_DEFERRED)

func _physics_process(delta: float) -> void:
	for body: Node3D in _bodies_inside.keys():
		if is_instance_valid(body) and body.has_method("take_damage"):
			body.take_damage(int(damage_per_second * delta))

func _on_body_entered(body: Node3D) -> void:
	_bodies_inside[body] = true

func _on_body_exited(body: Node3D) -> void:
	_bodies_inside.erase(body)
```

---

## Common Pitfalls

- **Ghost frames**: body_entered fires but body_exited never fires when entry and exit happen in one physics step. Track overlapping bodies in a `Dictionary`, not a counter.
- **`monitoring = false` after free**: accessing `get_overlapping_bodies()` on a freed area crashes. Disable monitoring first.
- **Godot 3 `connect("body_entered", self, "_on_body_entered")`** — Godot 4 uses `body_entered.connect(_on_body_entered)`; string-based connect is removed.
- **Area3D does not block movement** — it only detects. For physical barriers use `StaticBody3D`.
- **`body_entered` fires in physics step** — mutating the scene tree inside the handler causes errors; always use `CONNECT_DEFERRED` for handlers that free nodes or change scenes.
