---
name: gdscript-to-csharp
description: >-
  Convert a GDScript file to idiomatic C# for Godot 4.x. Maps GDScript types,
  signals, @export, @onready, and lifecycle methods to their C# equivalents.
  Use when asked to "convert this to C#", "port this script to C#", or
  "what is the C# equivalent of this GDScript?"
---
> **Godot version**: Godot 4.x (4.0+). All code examples use GDScript 2.0 and are not compatible with Godot 3.


Convert a GDScript 2.0 file to idiomatic C# for Godot 4.x.

## Type Mapping

| GDScript | C# |
|----------|----|
| `int` | `int` (or `long` for large values) |
| `float` | `float` (or `double`) |
| `bool` | `bool` |
| `String` | `string` |
| `StringName` | `StringName` |
| `Vector2`, `Vector3` | `Vector2`, `Vector3` |
| `Array[T]` | `Godot.Collections.Array<T>` |
| `Dictionary[K,V]` | `Godot.Collections.Dictionary<K,V>` |
| `Node` subclass | Same class name |
| `Variant` | `Variant` |

## Signal Conversion

```gdscript
# GDScript
signal health_changed(new_value: float)
signal died

func _ready() -> void:
    health_changed.emit(current_health)
```

```csharp
// C#
[Signal] public delegate void HealthChangedEventHandler(float newValue);
[Signal] public delegate void DiedEventHandler();

public override void _Ready()
{
    EmitSignal(SignalName.HealthChanged, CurrentHealth);
}
```

## Export and OnReady

```gdscript
# GDScript
@export var speed: float = 5.0
@export var weapon: WeaponResource
@onready var health_bar: ProgressBar = $HUD/HealthBar
```

```csharp
// C#
[Export] public float Speed { get; set; } = 5.0f;
[Export] public WeaponResource Weapon { get; set; }

private ProgressBar _healthBar;

public override void _Ready()
{
    _healthBar = GetNode<ProgressBar>("HUD/HealthBar");
}
```

## Lifecycle Methods

| GDScript | C# |
|----------|----|
| `_ready()` | `public override void _Ready()` |
| `_process(delta)` | `public override void _Process(double delta)` |
| `_physics_process(delta)` | `public override void _PhysicsProcess(double delta)` |
| `_input(event)` | `public override void _Input(InputEvent @event)` |
| `_unhandled_input(event)` | `public override void _UnhandledInput(InputEvent @event)` |

## Class Declaration

```gdscript
# GDScript
class_name Player extends CharacterBody3D

const MAX_SPEED: float = 10.0
var current_health: float
```

```csharp
// C#
using Godot;

public partial class Player : CharacterBody3D
{
    private const float MaxSpeed = 10.0f;
    private float _currentHealth;
}
```

## Steps

1. Read the GDScript file fully.
2. Map each `class_name` → `public partial class`.
3. Convert all signals with `[Signal]` delegate pattern.
4. Convert `@export` → `[Export]` property, `@onready` → `_Ready()` `GetNode<T>()` call.
5. Convert all method signatures using the lifecycle table above.
6. Map all types using the type table above.
7. Note any patterns with no direct equivalent (e.g., `match` → `switch`, `await` → `async/await`).
8. Output the full C# file followed by a summary of non-trivial conversions.
