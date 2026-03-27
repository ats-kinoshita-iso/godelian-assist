# API Reference: NavigationAgent3D

**Godot 4.x** | `extends Node → Object`

---

## Purpose

`NavigationAgent3D` computes navigation paths for `Node3D` owners on a baked `NavigationMesh`. Attach it as a child of any moving character node. It handles pathfinding queries to the navigation server and provides the next waypoint each frame.

---

## Prerequisites

1. A `NavigationRegion3D` with a baked `NavigationMesh` must exist in the level scene
2. The agent's owner node must be inside (or near) the navigation region
3. Call `NavigationServer3D.process()` implicitly — it runs automatically in `_physics_process`

---

## Key Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `target_position` | `Vector3` | `Vector3.ZERO` | Set this to the destination. Triggers a new path query. |
| `path_desired_distance` | `float` | `1.0` | Distance from a path point at which the agent considers it reached. |
| `target_desired_distance` | `float` | `1.0` | Distance from the final target at which the agent considers arrival. |
| `max_speed` | `float` | `10.0` | Maximum speed used for avoidance calculations (informational only — you move the node). |
| `navigation_layers` | `int` | `1` | Bitmask of navigation layers this agent uses. |
| `avoidance_enabled` | `bool` | `false` | Enables RVO obstacle avoidance. |
| `radius` | `float` | `0.5` | Agent radius for avoidance. |
| `path_postprocessing` | `PathPostProcessing` | `CORRIDORFUNNEL` | Algorithm for smoothing the raw path. |

---

## Key Methods

### `get_next_path_position() -> Vector3`

Returns the next waypoint in the computed path. Move the owner toward this position each physics frame.

```gdscript
var next_pos: Vector3 = nav_agent.get_next_path_position()
var direction: Vector3 = (next_pos - global_position).normalized()
velocity = direction * move_speed
```

### `is_navigation_finished() -> bool`

Returns `true` when the agent has reached `target_desired_distance` of `target_position`. Check this to know when to stop moving or switch states.

### `distance_to_target() -> float`

Returns straight-line distance to `target_position` (not path distance).

### `get_current_navigation_path() -> PackedVector3Array`

Returns the full computed path as an array of world positions.

### `set_velocity(velocity: Vector3) -> void`

Used with avoidance — provides the agent's intended velocity; it returns a safe avoidance velocity via `velocity_computed` signal.

---

## Signals

### `target_reached()`

Emitted when `is_navigation_finished()` becomes true.

### `velocity_computed(safe_velocity: Vector3)`

Only emitted when `avoidance_enabled = true`. Use `safe_velocity` as the actual movement velocity to avoid other agents.

### `path_changed()`

Emitted when the navigation path is recalculated.

---

## Typed GDScript Usage Example

```gdscript
class_name EnemyNavigation
extends CharacterBody3D

@export var move_speed: float = 3.5
@onready var nav_agent: NavigationAgent3D = $NavigationAgent3D

func _ready() -> void:
	nav_agent.path_desired_distance = 0.5
	nav_agent.target_desired_distance = 0.8
	nav_agent.target_reached.connect(_on_target_reached)

func navigate_to(destination: Vector3) -> void:
	nav_agent.target_position = destination

func _physics_process(_delta: float) -> void:
	if nav_agent.is_navigation_finished():
		return
	var next_point: Vector3 = nav_agent.get_next_path_position()
	var direction: Vector3 = (next_point - global_position).normalized()
	velocity = direction * move_speed
	move_and_slide()

func _on_target_reached() -> void:
	velocity = Vector3.ZERO
```

---

## Common Pitfalls

- **No `NavigationRegion3D` in the scene** — `target_position` is accepted but `get_next_path_position()` returns the agent's own position; the agent never moves
- **NavMesh not baked** — same symptom as above; bake in editor or at runtime with `NavigationRegion3D.bake_navigation_mesh()`
- **Reading `get_next_path_position()` before setting `target_position`** — returns `Vector3.ZERO`
- **Godot 3 `Navigation` node** — removed in Godot 4; use `NavigationServer3D` and `NavigationRegion3D`
- **Avoidance adds one-frame latency** — velocity set in `_physics_process` is computed asynchronously; use `velocity_computed` signal instead of `get_next_path_position` when avoidance is on
