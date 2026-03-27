---
name: idioms
description: >-
  Rewrite GDScript code to use idiomatic Godot 4.x patterns: match statements,
  lambdas, Callable, await, proper _process/_physics_process usage, and modern
  GDScript 2.0 syntax. Use when asked to "make this more idiomatic", "modernize
  this script", or "use better Godot patterns here".
---
> **Godot version**: Godot 4.x (4.0+). All code examples use GDScript 2.0 and are not compatible with Godot 3.


Rewrite a GDScript snippet or file to use idiomatic Godot 4.x patterns.

## Key GDScript 2.0 Idioms

### 1. `match` instead of `if/elif` chains
```gdscript
# Before
if state == "idle":
    _idle()
elif state == "walk":
    _walk()
elif state == "attack":
    _attack()

# After
match state:
    "idle": _idle()
    "walk": _walk()
    "attack": _attack()
    _: push_warning("Unknown state: %s" % state)
```

### 2. `await` for async operations
```gdscript
# Before — timer callback pattern
func _start_cooldown() -> void:
    $CooldownTimer.start()
func _on_cooldown_timer_timeout() -> void:
    can_attack = true

# After — inline await
func _start_cooldown() -> void:
    can_attack = false
    await get_tree().create_timer(cooldown_time).timeout
    can_attack = true
```

### 3. Lambdas for one-off signal connections
```gdscript
# Inline connection with lambda
button.pressed.connect(func() -> void:
    _handle_button_press(button_id)
)
```

### 4. `Callable.bind()` for parameterized connections
```gdscript
for i: int in range(inventory_size):
    slots[i].pressed.connect(_on_slot_pressed.bind(i))
```

### 5. `@onready` instead of `get_node` in `_ready`
```gdscript
# Before
var health_bar: ProgressBar
func _ready() -> void:
    health_bar = get_node("HUD/HealthBar")

# After
@onready var health_bar: ProgressBar = $HUD/HealthBar
```

### 6. String formatting with `%` or `str()`
```gdscript
# Use named format for readability
label.text = "HP: %d / %d" % [current_hp, max_hp]
# Or typed string
label.text = "Score: " + str(score)
```

### 7. Guard clauses over nesting
```gdscript
# Before
func interact() -> void:
    if can_interact:
        if target != null:
            target.interact()

# After
func interact() -> void:
    if not can_interact: return
    if target == null: return
    target.interact()
```

## Steps

1. Read the provided script.
2. Identify all non-idiomatic patterns from the list above.
3. Rewrite each section, preserving behavior exactly.
4. Note each change made with a one-line explanation.
5. If behavior cannot be preserved during rewrite, flag it explicitly.
