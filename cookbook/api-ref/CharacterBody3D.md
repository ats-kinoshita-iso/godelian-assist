# API Reference: CharacterBody3D

**Godot 4.x** | `extends PhysicsBody3D → CollisionObject3D → Node3D → Node → Object`

---

## Purpose

`CharacterBody3D` is the correct base class for player characters and NPCs that need physics collision but direct movement control. Unlike `RigidBody3D`, you control velocity directly — the engine does not apply forces.

---

## Key Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `velocity` | `Vector3` | `Vector3.ZERO` | The body's current velocity. Set this each frame, then call `move_and_slide()`. |
| `up_direction` | `Vector3` | `Vector3.UP` | Defines what "floor" means. Change for wall-walking or zero-G. |
| `floor_max_angle` | `float` | `0.785` (45°) | Steeper angles are treated as walls, not floors. |
| `max_slides` | `int` | `4` | How many slide iterations per `move_and_slide()` call. |
| `motion_mode` | `MotionMode` | `MOTION_MODE_GROUNDED` | GROUNDED for platformers; FLOATING for top-down/swimming. |
| `slide_on_ceiling` | `bool` | `true` | If false, stops on ceiling contact instead of sliding. |

---

## Key Methods

### `move_and_slide() -> bool`

Moves the body by `velocity * delta` (delta is applied internally), sliding along collisions. Returns `true` if any collision occurred.

```gdscript
func _physics_process(_delta: float) -> void:
	velocity.y -= 9.8 * get_physics_process_delta_time()
	move_and_slide()
```

**Call once per `_physics_process`.** Do not call in `_process`.

### `is_on_floor() -> bool`

Returns `true` if the body is resting on a surface within `floor_max_angle`. Valid only after `move_and_slide()` has been called this frame.

### `is_on_ceiling() -> bool`

Returns `true` if the body contacted a ceiling-classified surface.

### `is_on_wall() -> bool`

Returns `true` if the body contacted a wall-classified surface.

### `get_floor_normal() -> Vector3`

Returns the normal of the floor the body is standing on. Useful for slope alignment.

### `get_slide_collision_count() -> int`

Number of slide collisions that occurred in the last `move_and_slide()`.

### `get_slide_collision(index: int) -> KinematicCollision3D`

Returns collision data for slide #N. Access via `collision.get_collider()`, `.get_normal()`.

---

## Typed GDScript Usage Example

```gdscript
class_name PlayerController
extends CharacterBody3D

@export var move_speed: float = 5.0
@export var jump_velocity: float = 6.0

const GRAVITY: float = ProjectSettings.get_setting("physics/3d/default_gravity")

func _physics_process(delta: float) -> void:
	# Apply gravity
	if not is_on_floor():
		velocity.y -= GRAVITY * delta

	# Jump
	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = jump_velocity

	# Horizontal movement
	var input_dir: Vector2 = Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	var direction: Vector3 = (transform.basis * Vector3(input_dir.x, 0.0, input_dir.y)).normalized()
	velocity.x = direction.x * move_speed
	velocity.z = direction.z * move_speed

	move_and_slide()
```

---

## Common Pitfalls

- **Never use `position +=` for movement** — bypasses collision detection entirely
- **`move_and_slide()` applies delta internally** — do not multiply `velocity` by `delta` before calling it
- **`is_on_floor()` is only valid after `move_and_slide()`** — reading it before the call returns stale data
- **Godot 3 had `move_and_slide(velocity, up_dir)`** — Godot 4 reads `velocity` as a property; no parameters

---

## CollisionShape3D Requirement

Every `CharacterBody3D` needs a `CollisionShape3D` child with a valid shape. Without it, no collision occurs and no error is raised.
