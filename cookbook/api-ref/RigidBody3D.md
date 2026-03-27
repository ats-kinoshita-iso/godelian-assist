# API Reference: RigidBody3D

**Godot 4.x** | `extends PhysicsBody3D → CollisionObject3D → Node3D → Node → Object`

---

## Purpose

`RigidBody3D` is fully physics-simulated. The engine applies gravity, forces, and collisions automatically. Use it for throwable objects, barrels, debris, and ragdoll bones. Do **not** use it for player controllers — use `CharacterBody3D` instead.

---

## Key Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `mass` | `float` | `1.0` | Mass in kg. Affects force response and collision momentum. |
| `linear_velocity` | `Vector3` | `Vector3.ZERO` | Read-only outside `_integrate_forces`. Set in `_integrate_forces` only. |
| `angular_velocity` | `Vector3` | `Vector3.ZERO` | Rotation speed. Same read/write rules as `linear_velocity`. |
| `gravity_scale` | `float` | `1.0` | Multiplier for gravity. 0.0 = zero-G, 2.0 = double gravity. |
| `freeze` | `bool` | `false` | When true, body is immovable. See `freeze_mode`. |
| `freeze_mode` | `FreezeMode` | `FREEZE_MODE_STATIC` | STATIC = zero inertia; KINEMATIC = moves via transform. |
| `can_sleep` | `bool` | `true` | Bodies auto-sleep when below velocity threshold. Keep true. |
| `sleeping` | `bool` | (auto) | Set to `false` to wake. Wakes automatically on force application. |
| `contact_monitor` | `bool` | `false` | Must be `true` to receive `body_entered`/`body_exited` signals. |
| `max_contacts_reported` | `int` | `0` | Must be > 0 alongside `contact_monitor` for contact signals. |
| `linear_damp` | `float` | `-1.0` | Air resistance for linear motion. -1.0 uses project default. |
| `angular_damp` | `float` | `-1.0` | Air resistance for rotation. |

---

## Key Methods

### `apply_central_impulse(impulse: Vector3) -> void`

Applies an instant velocity change. Use for explosions, knockback, jump pads.

```gdscript
apply_central_impulse(Vector3.UP * 10.0)   # launch upward
```

### `apply_central_force(force: Vector3) -> void`

Applies a continuous force (accumulates over the frame). Call inside `_integrate_forces`.

### `apply_torque_impulse(impulse: Vector3) -> void`

Applies instant angular velocity — makes the body spin.

### `apply_impulse(impulse: Vector3, position: Vector3) -> void`

Applies impulse at a world-space offset from center. Creates rotation if offset is non-zero.

### `_integrate_forces(state: PhysicsDirectBodyState3D) -> void`

Called every physics step when the body is active. The **only** safe place to read/write `linear_velocity` and `angular_velocity` directly.

```gdscript
func _integrate_forces(state: PhysicsDirectBodyState3D) -> void:
	if _should_set_velocity:
		state.linear_velocity = _target_velocity
		_should_set_velocity = false
```

---

## Typed GDScript Usage Example

```gdscript
class_name ThrowableBarrel
extends RigidBody3D

var _launch_pending: bool = false
var _launch_vector: Vector3 = Vector3.ZERO

func _ready() -> void:
	contact_monitor = true
	max_contacts_reported = 4
	body_entered.connect(_on_body_entered)

func throw(direction: Vector3, force: float) -> void:
	_launch_vector = direction.normalized() * force
	_launch_pending = true

func _integrate_forces(state: PhysicsDirectBodyState3D) -> void:
	if _launch_pending:
		state.apply_central_impulse(_launch_vector)
		_launch_pending = false

func _on_body_entered(body: Node) -> void:
	if body.is_in_group("enemy"):
		body.take_damage(20)
```

---

## Common Pitfalls

- **Setting `velocity` directly** — `linear_velocity` is read-only outside `_integrate_forces`; use `apply_central_impulse` instead
- **Scaling a RigidBody3D** — changes to `scale` corrupt the physics shape; scale the collision shape resource instead
- **Nesting RigidBody3D inside another physics body** — not supported; use `RemoteTransform3D` to sync positions
- **Forgetting `contact_monitor = true`** — body_entered/body_exited signals never fire without this
- **Godot 3 `add_central_force`** — renamed to `apply_central_force` in Godot 4
