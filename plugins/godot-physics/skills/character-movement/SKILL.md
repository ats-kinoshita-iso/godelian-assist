---
name: character-movement
description: Implement polished CharacterBody3D movement with coyote time, jump buffering, and air acceleration.
invocation: /character-movement
---

Build a fully-featured 3D character controller using `CharacterBody3D` with the feel-good physics tricks that make movement satisfying.

## Core Concepts

| Technique | What it does | Typical value |
|---|---|---|
| **Coyote time** | Allows jumping for N frames after walking off a ledge | 6–12 frames |
| **Jump buffering** | Queues a jump press for N frames before landing | 8–15 frames |
| **Air acceleration** | Separate (lower) acceleration when airborne | 40–60% of ground accel |
| **Variable jump height** | Cuts vertical velocity when jump is released early | velocity.y *= 0.5 |
| **Gravity scale** | Faster fall when descending for snappier arc | 1.5–2.5× gravity |

## Complete Typed GDScript Example

```gdscript
class_name PlayerMovement
extends CharacterBody3D

## Polished 3D character controller with coyote time, jump buffering, and air acceleration.

@export_group("Movement")
@export var move_speed: float = 6.0
@export var ground_acceleration: float = 12.0
@export var air_acceleration: float = 5.0
@export var friction: float = 10.0

@export_group("Jump")
@export var jump_velocity: float = 6.5
@export var gravity_scale: float = 2.0
@export var fall_gravity_scale: float = 3.5
@export var coyote_frames: int = 8
@export var jump_buffer_frames: int = 12
@export var variable_jump_cut: float = 0.5

var _coyote_timer: int = 0
var _jump_buffer_timer: int = 0
var _was_on_floor: bool = false

const BASE_GRAVITY: float = ProjectSettings.get_setting("physics/3d/default_gravity")

func _physics_process(delta: float) -> void:
	_update_timers()
	_apply_gravity(delta)
	_handle_jump()
	_handle_horizontal(delta)
	move_and_slide()

func _update_timers() -> void:
	if is_on_floor():
		_coyote_timer = coyote_frames
		_was_on_floor = true
	else:
		if _was_on_floor:
			_was_on_floor = false
		_coyote_timer = max(0, _coyote_timer - 1)
	_jump_buffer_timer = max(0, _jump_buffer_timer - 1)
	if Input.is_action_just_pressed("jump"):
		_jump_buffer_timer = jump_buffer_frames

func _apply_gravity(delta: float) -> void:
	if is_on_floor():
		return
	var grav: float = BASE_GRAVITY * (gravity_scale if velocity.y >= 0.0 else fall_gravity_scale)
	velocity.y -= grav * delta

func _handle_jump() -> void:
	var can_jump: bool = _coyote_timer > 0
	var wants_jump: bool = _jump_buffer_timer > 0
	if can_jump and wants_jump:
		velocity.y = jump_velocity
		_coyote_timer = 0
		_jump_buffer_timer = 0
	if Input.is_action_just_released("jump") and velocity.y > 0.0:
		velocity.y *= variable_jump_cut

func _handle_horizontal(delta: float) -> void:
	var input_dir: Vector2 = Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	var direction: Vector3 = (transform.basis * Vector3(input_dir.x, 0.0, input_dir.y)).normalized()
	var accel: float = ground_acceleration if is_on_floor() else air_acceleration
	if direction.length() > 0.0:
		velocity.x = move_toward(velocity.x, direction.x * move_speed, accel * delta)
		velocity.z = move_toward(velocity.z, direction.z * move_speed, accel * delta)
	else:
		var fric: float = friction if is_on_floor() else friction * 0.3
		velocity.x = move_toward(velocity.x, 0.0, fric * delta)
		velocity.z = move_toward(velocity.z, 0.0, fric * delta)
```

## Tuning Guide

Start with defaults, then adjust in this order:
1. `move_speed` — does it feel fast enough for the level scale?
2. `jump_velocity` — does the peak height clear platforms comfortably?
3. `fall_gravity_scale` — higher = snappier, more control; lower = floatier
4. `coyote_frames` — 6 is subtle, 12 is generous; both feel fair
5. `jump_buffer_frames` — 12 frames (0.2s at 60fps) covers most player timing windows
6. `air_acceleration` — low values feel slippery; high values feel floaty but controllable

## Input Map Requirements

Ensure these actions exist in Project Settings → Input Map:
- `move_left`, `move_right`, `move_forward`, `move_back`
- `jump`

## Scene Structure

```
CharacterBody3D (PlayerMovement script)
├── CollisionShape3D (CapsuleShape3D)
└── Head (Node3D, at eye height)
    └── Camera3D
```
