# API Reference: AnimationPlayer

**Godot 4.x** | `extends Node → Object`

---

## Purpose

`AnimationPlayer` plays keyframe animations stored in an `AnimationLibrary`. Use it for: character animation, UI transitions, scene cinematics, and property tweening that is too complex for `Tween`. One `AnimationPlayer` can hold multiple `AnimationLibrary` resources.

---

## Key Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `current_animation` | `String` | `""` | Name of the currently playing animation. Read-only at runtime (use `play()`). |
| `current_animation_length` | `float` | `0.0` | Duration of current animation in seconds. Read-only. |
| `current_animation_position` | `float` | `0.0` | Playback position in seconds. Read-only. |
| `speed_scale` | `float` | `1.0` | Playback speed multiplier. 2.0 = double speed, -1.0 = reverse. |
| `autoplay` | `String` | `""` | Animation to play automatically when the node enters the scene tree. |
| `playback_default_blend_time` | `float` | `0.0` | Default blend duration when switching animations. |
| `root_node` | `NodePath` | `".."` | Root of the node tree that animations target. |

---

## Key Methods

### `play(name: StringName = &"", custom_blend: float = -1, custom_speed: float = 1.0, from_end: bool = false) -> void`

Plays an animation by name. Blends from the current animation over `custom_blend` seconds.

```gdscript
$AnimationPlayer.play("walk")
$AnimationPlayer.play("attack", 0.1)   # 0.1s blend from current
```

### `play_backwards(name: StringName = &"", custom_blend: float = -1) -> void`

Plays an animation in reverse (from end to start).

### `stop(keep_state: bool = false) -> void`

Stops playback. If `keep_state = true`, retains the last frame's values.

### `pause() -> void`

Pauses at the current position.

### `is_playing() -> bool`

Returns `true` if an animation is currently playing.

### `get_animation(name: StringName) -> Animation`

Returns the `Animation` resource by name. Use to read keyframe data.

### `get_animation_list() -> PackedStringArray`

Returns all animation names in the library.

### `queue(name: StringName) -> void`

Queues an animation to play after the current one finishes.

---

## Signals

### `animation_finished(anim_name: StringName)`

Emitted when an animation completes (not emitted for looping animations mid-loop).

### `animation_started(anim_name: StringName)`

Emitted when an animation begins playing.

### `animation_changed(old_name: StringName, new_name: StringName)`

Emitted when switching from one animation to another.

---

## AnimationLibrary

In Godot 4.x, animations are organized into libraries. The default library has an empty string name `""`. Named libraries use `"LibraryName/AnimationName"` syntax.

```gdscript
# Access animations in the default library:
anim_player.play("idle")

# Access animations in a named library:
anim_player.play("combat/attack_01")
```

---

## Typed GDScript Usage Example

```gdscript
class_name CharacterAnimator
extends Node

@onready var anim: AnimationPlayer = $AnimationPlayer

var _current_state: String = ""

func play_state(state: String, blend: float = 0.15) -> void:
	if _current_state == state:
		return
	_current_state = state
	anim.play(state, blend)

func play_one_shot(anim_name: String, then_state: String) -> void:
	anim.play(anim_name, 0.1)
	await anim.animation_finished
	play_state(then_state)
```

---

## Common Pitfalls

- **`play()` with a non-existent animation name** — prints an error and does nothing; always verify the name with `get_animation_list()`
- **Godot 3 `playback_speed`** — renamed to `speed_scale` in Godot 4
- **`AnimationTreePlayer`** — removed in Godot 4; use `AnimationTree` + `AnimationStateMachine` instead
- **Modifying `current_animation` directly** — it is read-only; always use `play()`
- **`await animation_finished` without checking which animation** — if another `play()` interrupts, the signal fires with the new animation name
