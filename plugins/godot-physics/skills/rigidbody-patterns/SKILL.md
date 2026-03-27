---
name: rigidbody-patterns
description: Correct patterns for RigidBody3D — applying forces, freeze modes, sleeping, and ragdoll switching.
invocation: /rigidbody-patterns
---

`RigidBody3D` is fully physics-driven. Follow these patterns to avoid the common mistakes that cause jitter, missed forces, and state corruption.

## Force Application Rules

**Never set `velocity` directly on a RigidBody3D.** It bypasses the physics solver and causes one-frame stutters.

| Intent | Wrong | Right |
|---|---|---|
| Push in direction | `velocity = dir * speed` | `apply_central_impulse(dir * speed)` |
| Continuous force | `velocity += force * delta` | `apply_central_force(force)` in `_integrate_forces` |
| Instant velocity set | `velocity = target` | `linear_velocity = target` (only in `_integrate_forces`) |
| Torque | `angular_velocity = ...` | `apply_torque_impulse(torque)` |

## _integrate_forces Callback

The only safe place to read or write physics state each frame:

```gdscript
class_name PhysicsObject
extends RigidBody3D

var _target_velocity: Vector3 = Vector3.ZERO
var _apply_impulse: bool = false
var _impulse_vector: Vector3 = Vector3.ZERO

func request_impulse(impulse: Vector3) -> void:
	_impulse_vector = impulse
	_apply_impulse = true

func _integrate_forces(state: PhysicsDirectBodyState3D) -> void:
	if _apply_impulse:
		state.apply_central_impulse(_impulse_vector)
		_apply_impulse = false
```

## Freeze Modes

| Mode | Behaviour | Use for |
|---|---|---|
| `FREEZE_MODE_STATIC` | Immovable, zero inertia | Doors mid-animation, kinematic platforms |
| `FREEZE_MODE_KINEMATIC` | Moves via `move_and_collide`, generates contacts | Elevators, moving platforms |

```gdscript
# Freeze while animating
freeze_mode = RigidBody3D.FREEZE_MODE_KINEMATIC
freeze = true

# Resume physics
freeze = false
```

## Sleeping

RigidBodies auto-sleep when below the linear/angular velocity threshold. Sleeping bodies use zero CPU. Do not disable `can_sleep` unless continuous processing is critical.

Wake a sleeping body:
```gdscript
sleeping = false   # directly wakes it
# or apply a small impulse — any force wakes it automatically
```

## Ragdoll Switching Pattern

Swap a `CharacterBody3D` character to ragdoll on death:

```gdscript
func activate_ragdoll() -> void:
	# 1. Disable character controller
	set_physics_process(false)

	# 2. For each RigidBody3D bone in the ragdoll skeleton:
	for bone: RigidBody3D in _ragdoll_bones:
		bone.freeze = false
		bone.collision_layer = CollisionLayer.RAGDOLL
		bone.linear_velocity = velocity  # inherit character velocity

	# 3. Hide the animated mesh, show the ragdoll mesh
	$Mesh.visible = false
	$RagdollMesh.visible = true
```

## Common Pitfalls

- **Applying forces outside `_integrate_forces`** — forces applied in `_physics_process` are queued, not immediate; for one-shot impulses use `apply_central_impulse()` directly
- **Scaling a RigidBody3D** — changes to `scale` corrupt the physics shape; scale the collision shape instead
- **Nesting RigidBody3D** — never parent one physics body inside another; use `RemoteTransform3D` to sync positions
- **Contact monitors off** — `contact_monitor = true` and `max_contacts_reported > 0` must both be set to receive `body_entered` signals
