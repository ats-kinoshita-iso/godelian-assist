---
name: test-gen-godot
description: >-
  Generate GdUnit4 test stubs for a GDScript class: create a GdUnitTestSuite
  subclass with test_ methods covering each public method, signal emissions,
  and async behavior. Use when asked to "write tests for this GDScript",
  "generate GdUnit4 tests", or "add unit tests to this Godot class".
---

Generate GdUnit4 test stubs for a GDScript class.

## GdUnit4 Test Structure

```gdscript
# test_player.gd
class_name TestPlayer extends GdUnitTestSuite

# Subject under test
var _player: Player

func before_test() -> void:
    # Runs before each test_ method
    _player = auto_free(Player.new())

func after_test() -> void:
    # Runs after each test_ method (auto_free handles cleanup)
    pass
```

## Testing a Method

```gdscript
func test_take_damage_reduces_health() -> void:
    # Arrange
    _player.current_health = 100.0

    # Act
    _player.take_damage(25.0)

    # Assert
    assert_float(_player.current_health).is_equal(75.0)


func test_take_damage_does_not_go_below_zero() -> void:
    _player.current_health = 10.0
    _player.take_damage(50.0)
    assert_float(_player.current_health).is_greater_equal(0.0)
```

## Testing Signals

```gdscript
func test_take_damage_emits_health_changed() -> void:
    var monitor := monitor_signals(_player)

    _player.current_health = 100.0
    _player.take_damage(30.0)

    assert_signal(monitor).is_emitted("health_changed")


func test_take_damage_to_zero_emits_died() -> void:
    var monitor := monitor_signals(_player)

    _player.current_health = 10.0
    _player.take_damage(100.0)

    assert_signal(monitor).is_emitted("died")
```

## Testing Async / Awaitable Methods

```gdscript
func test_respawn_restores_health() -> void:
    _player.current_health = 0.0

    await _player.respawn()   # await async method

    assert_float(_player.current_health).is_equal(_player.max_health)
```

## Steps

1. Read the target GDScript class fully.
2. Identify every public method (not prefixed with `_`) and every signal.
3. Create `test_<class_name>.gd` in `tests/` extending `GdUnitTestSuite`.
4. Add `before_test()` to instantiate the subject; use `auto_free()` for nodes.
5. For each method: write at least one happy-path test and one edge-case test.
6. For each signal: write a test using `monitor_signals()` + `assert_signal()`.
7. For async methods: use `await` inside the test function.
8. Use descriptive test names: `test_<method>_<condition>_<expected_result>`.

## GdUnit4 Assertion Reference

| Type | Assertion |
|------|-----------|
| `float` | `assert_float(val).is_equal(expected)` |
| `int` | `assert_int(val).is_equal(expected)` |
| `bool` | `assert_bool(val).is_true()` / `.is_false()` |
| `String` | `assert_str(val).is_equal(expected)` |
| `Object/null` | `assert_object(val).is_not_null()` |
| Signal | `assert_signal(monitor).is_emitted("signal_name")` |

## Running Tests

```bash
godot --headless -s addons/gdUnit4/bin/GdUnitCmdTool.gd --add res://tests
```
