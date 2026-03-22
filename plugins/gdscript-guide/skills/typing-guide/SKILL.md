---
name: typing-guide
description: >-
  Review GDScript code for missing or incorrect static types and produce a
  fully-typed version. Use when asked to "add types to this script", "type
  this GDScript", "fix the type annotations", or "make this fully static-typed".
---

Add or fix static type annotations in a GDScript 2.0 file.

## Steps

1. **Read the script** — understand the intent of each variable, parameter, and return value.

2. **Apply variable typing**:
   ```gdscript
   # Before
   var speed = 5.0
   var enemies = []
   var name = "Player"

   # After
   var speed: float = 5.0
   var enemies: Array[Enemy] = []
   var name: StringName = &"Player"
   ```
   - Use `Array[T]` for typed arrays, never bare `Array`
   - Use `Dictionary[K, V]` when keys and values have known types
   - Use `StringName` (with `&` prefix) for identifiers used as keys or group names
   - Use `NodePath` for paths, not `String`

3. **Type all function signatures**:
   ```gdscript
   # Before
   func take_damage(amount):
       health -= amount

   # After
   func take_damage(amount: float) -> void:
       health -= amount
   ```
   Return type `-> void` is required even for functions with no return.

4. **Type signals with typed parameters**:
   ```gdscript
   signal health_changed(new_value: float)
   signal item_collected(item: ItemResource, count: int)
   ```

5. **Use `@export` with explicit types** for Inspector properties:
   ```gdscript
   @export var speed: float = 5.0
   @export var weapon: WeaponResource
   @export_range(0.0, 1.0) var friction: float = 0.8
   ```

6. **Type class variables from `get_node`** using `$` shorthand with type:
   ```gdscript
   @onready var health_bar: ProgressBar = $HUD/HealthBar
   @onready var animation_player: AnimationPlayer = $AnimationPlayer
   ```

7. **Flag dynamic patterns** that cannot be statically typed and recommend alternatives:
   - `set()` / `get()` with variant returns — type the backing variable instead
   - Untyped Dictionary — convert to a `Resource` class
   - `call()` with dynamic method names — use signals or a typed interface

## Output

Return the fully-typed script with a summary of changes made and any patterns that could not be fully typed with explanation.
