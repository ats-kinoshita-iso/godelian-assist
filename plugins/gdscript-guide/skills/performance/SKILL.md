---
name: performance
description: >-
  Profile and optimize a GDScript file or system for Godot 4.x performance:
  identify hot loops, unnecessary allocations, physics/rendering bottlenecks,
  and suggest targeted fixes. Use when asked to "optimize this script",
  "why is this lagging?", or "make this more performant".
---
> **Godot version**: Godot 4.x (4.0+). All code examples use GDScript 2.0 and are not compatible with Godot 3.


Review and optimize GDScript for Godot 4.x performance.

## Common GDScript Performance Patterns

### 1. Cache `get_node` calls — never call in `_process`
```gdscript
# BAD — allocates every frame
func _process(delta: float) -> void:
    $HUD/HealthBar.value = health  # get_node called each frame

# GOOD — cached at ready
@onready var health_bar: ProgressBar = $HUD/HealthBar
func _process(delta: float) -> void:
    health_bar.value = health
```

### 2. Use `_physics_process` only for physics; `_process` for visuals
- Move `velocity`, collision checks, `move_and_slide()` → `_physics_process`
- Animations, UI updates, non-physics interpolation → `_process`
- Avoid heavy logic (pathfinding, sorting) in either — defer to async or timers

### 3. Prefer `is_instance_valid()` over try/catch
```gdscript
if is_instance_valid(target) and target.is_inside_tree():
    target.take_damage(damage)
```

### 4. Pool objects instead of instancing in hot paths
```gdscript
# Use a pool for frequently spawned objects (bullets, particles)
class_name BulletPool extends Node
var _pool: Array[Bullet] = []

func get_bullet() -> Bullet:
    if _pool.is_empty():
        return Bullet.instantiate()
    return _pool.pop_back()

func return_bullet(b: Bullet) -> void:
    b.visible = false
    _pool.push_back(b)
```

### 5. Avoid `find_children` / `get_children` in `_process`
Cache results in `_ready`. Use groups for dynamic queries:
```gdscript
var enemies: Array[Node] = get_tree().get_nodes_in_group("enemies")
```

### 6. Use `PackedByteArray` / `PackedFloat32Array` for bulk data
When working with arrays of primitives (positions, colors), typed packed arrays are 10-100× faster than `Array[float]`.

### 7. Limit `print` in release builds
```gdscript
# Debug only
if OS.is_debug_build():
    print("state: ", state)
```

## Steps

1. Read the script and identify loops, signal connections, and node access patterns.
2. Classify issues by severity: **critical** (allocations/lookups in `_process`), **moderate** (unoptimized data structures), **minor** (style).
3. Provide fixed code for each critical and moderate issue.
4. Estimate impact: "removes ~N allocations per frame" where measurable.
5. Suggest any Godot profiler checkpoints: `Performance.get_monitor()`, `VisualServer` metrics, or the built-in profiler tabs to verify improvement.
