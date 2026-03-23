---
name: debug-tools
description: >-
  Set up debugging and observability tools for a Godot 4.x project: built-in
  profiler usage, structured logging, Performance monitors, DebugDraw overlays,
  and an in-game debug overlay scene. Use when asked to "add debug tools",
  "how do I profile this?", "why is my game slow?", or "add logging to X".
---

Set up debugging and observability for a Godot 4.x project.

## Built-in Profiler

Open the Godot editor profiler: **Debugger > Profiler tab** while running in the editor.

Key metrics to watch:
- `physics_process` — should be < 16 ms at 60 Hz physics
- `_process` — visual update budget; spikes indicate frame-rate issues
- `render/draw_calls_in_frame` — high counts hurt GPU; merge meshes or use MultiMesh

```gdscript
# Read profiler data at runtime
func _process(_delta: float) -> void:
    var fps: float = Performance.get_monitor(Performance.TIME_FPS)
    var draw_calls: float = Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME)
    var physics_ms: float = Performance.get_monitor(Performance.TIME_PHYSICS_PROCESS) * 1000.0
    if OS.is_debug_build():
        _debug_overlay.update_stats(fps, draw_calls, physics_ms)
```

## Structured Logging

Use a lightweight logger Autoload instead of bare `print()`:

```gdscript
# logger.gd — Autoload "Logger"
class_name Logger extends Node

enum Level { DEBUG, INFO, WARN, ERROR }

@export var min_level: Level = Level.DEBUG

func debug(category: StringName, msg: String) -> void:
    _log(Level.DEBUG, category, msg)

func info(category: StringName, msg: String) -> void:
    _log(Level.INFO, category, msg)

func warn(category: StringName, msg: String) -> void:
    _log(Level.WARN, category, msg)

func error(category: StringName, msg: String) -> void:
    _log(Level.ERROR, category, msg)
    push_error("[%s] %s" % [category, msg])

func _log(level: Level, category: StringName, msg: String) -> void:
    if level < min_level: return
    var label: String = Level.keys()[level]
    print("[%s][%s] %s" % [label, category, msg])
```

Usage:
```gdscript
Logger.debug(&"CombatSystem", "Player attacked enemy: %s, damage: %.1f" % [enemy.name, dmg])
Logger.warn(&"SaveSystem", "Save file version mismatch: expected %d, got %d" % [expected, got])
```

## Performance Monitors

```gdscript
# Custom performance monitor — register before reading
func _ready() -> void:
    Performance.add_custom_monitor("game/active_enemies",
        Callable(self, "_get_enemy_count"))
    Performance.add_custom_monitor("game/projectiles_alive",
        Callable(self, "_get_projectile_count"))

func _get_enemy_count() -> int:
    return get_tree().get_nodes_in_group("enemies").size()
```

View custom monitors in **Debugger > Monitors** alongside built-in metrics.

## DebugDraw Overlays

Use `DebugDraw3D` (third-party addon) or Godot's built-in `RenderingServer` for visual debugging:

```gdscript
# Draw a sphere at a position — useful for hitbox/range debugging
func _process(_delta: float) -> void:
    if OS.is_debug_build():
        DebugDraw3D.draw_sphere(global_position, attack_range, Color.RED)
        DebugDraw3D.draw_line(global_position, _target.global_position, Color.YELLOW)
```

Without DebugDraw3D addon, use `ImmediateMesh` or `draw_line` on a `MeshInstance3D`.

## In-Game Debug Overlay Scene

Create `ui/debug_overlay.tscn` — a `CanvasLayer` with `Label` nodes, visible only in debug builds:

```gdscript
# debug_overlay.gd
class_name DebugOverlay extends CanvasLayer

@onready var _fps_label: Label = $VBox/FPS
@onready var _enemies_label: Label = $VBox/Enemies

func _ready() -> void:
    visible = OS.is_debug_build()

func _process(_delta: float) -> void:
    if not visible: return
    _fps_label.text = "FPS: %.0f" % Performance.get_monitor(Performance.TIME_FPS)
    _enemies_label.text = "Enemies: %d" % get_tree().get_nodes_in_group("enemies").size()

func update_stats(fps: float, draw_calls: float, physics_ms: float) -> void:
    _fps_label.text = "FPS: %.0f  DC: %.0f  Physics: %.1fms" % [fps, draw_calls, physics_ms]
```

## Steps

1. Add `Logger` Autoload for structured logging; replace bare `print()` calls.
2. Register custom `Performance` monitors for game-specific metrics.
3. Install DebugDraw3D addon (or use ImmediateMesh) for runtime visual debugging.
4. Create a `DebugOverlay` CanvasLayer scene; add to your main scene with `visible = OS.is_debug_build()`.
5. Use the editor Profiler tab to identify hot spots — look for spikes > 16 ms.
6. Strip all `OS.is_debug_build()` guards from release exports via export presets.
