---
name: area-detection
description: Implement Area3D-based detection zones with correct ghost frame handling and one-frame delay avoidance.
invocation: /area-detection
---

Use `Area3D` for detection volumes (aggro ranges, pickups, damage triggers) with the correct signal flow and ghost frame mitigation.

## Ghost Frames Problem

When a body enters and exits an `Area3D` in the same physics frame (e.g. fast projectile, instant teleport), `body_entered` fires but `body_exited` never fires. This leaves the body in the area's overlap set permanently — a **ghost frame**.

**Mitigation**: Always track overlapping bodies in a `Dictionary` keyed by body, not a simple counter. On `body_exited`, remove from the dict. Check membership with `.has()`, not a boolean flag.

```gdscript
var _overlapping: Dictionary = {}   # body -> true

func _on_body_entered(body: Node3D) -> void:
	_overlapping[body] = true
	_process_entry(body)

func _on_body_exited(body: Node3D) -> void:
	_overlapping.erase(body)

func is_body_inside(body: Node3D) -> bool:
	return _overlapping.has(body)
```

## Detection Zone Component

```gdscript
class_name DetectionZone
extends Area3D

## Reusable detection zone. Emits typed signals on enter/exit.
## Set collision_layer = CollisionLayer.TRIGGER
## Set collision_mask  = CollisionLayer.PLAYER (or ENEMY, etc.)

signal target_entered(target: Node3D)
signal target_exited(target: Node3D)

@export var target_group: String = "player"

var _overlapping: Dictionary = {}

func _ready() -> void:
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)

func _on_body_entered(body: Node3D) -> void:
	if not body.is_in_group(target_group):
		return
	_overlapping[body] = true
	target_entered.emit(body)

func _on_body_exited(body: Node3D) -> void:
	if _overlapping.erase(body):
		target_exited.emit(body)

func get_targets() -> Array[Node3D]:
	return Array(_overlapping.keys(), TYPE_OBJECT, "Node3D", null)

func has_target() -> bool:
	return not _overlapping.is_empty()
```

## Deferred Signal Warning

`body_entered` fires during the physics step. If you change scene state (free a node, change scene) inside the signal handler, you risk a mid-step modification crash.

**Fix**: Always use `call_deferred` or connect with `CONNECT_DEFERRED` when the handler changes the scene tree:

```gdscript
body_entered.connect(_on_body_entered, CONNECT_DEFERRED)
```

## Common Detection Zone Types

| Use case | Shape | collision_mask |
|---|---|---|
| Enemy aggro range | SphereShape3D | PLAYER |
| Pickup collection | SphereShape3D | PLAYER |
| Level exit trigger | BoxShape3D | PLAYER |
| Damage zone (lava) | BoxShape3D | PLAYER \| ENEMY |
| Interactable prompt | SphereShape3D (small) | PLAYER |

## Scene Placement

```
EnemyRoot (CharacterBody3D)
└── DetectionZone (Area3D — DetectionZone script)
    └── CollisionShape3D (SphereShape3D, radius = detection_radius)
```

Wire in enemy `_ready()`:
```gdscript
$DetectionZone.target_entered.connect(_on_player_detected)
$DetectionZone.target_exited.connect(_on_player_lost)
```
