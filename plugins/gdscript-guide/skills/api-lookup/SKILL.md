---
name: api-lookup
description: Look up Godot 4.x class APIs from the local cookbook/api-ref/ fragments before writing any GDScript.
invocation: /api-lookup
---

Before writing code that uses a Godot class, method, or signal — look it up. Do not rely on training-data memory for Godot API details; the API has breaking changes between minor versions and hallucinated method names cause runtime errors.

## Verify Before Write Rule

**Never write a Godot API call from memory.** Always:

1. Check `cookbook/api-ref/<ClassName>.md` in this repository
2. If not present, read the official docs or use the Godot editor's built-in help
3. Only then write the code

This rule exists because hallucinated Godot API names are the single most common source of bugs in Claude-generated GDScript. A method that "should exist" but doesn't causes a nil call error at runtime that can be hard to trace.

## Available API Reference Fragments

Located at `cookbook/api-ref/`:

| File | Covers |
|---|---|
| `tscn-format.md` | .tscn file format, UIDs, ext_resource, sub_resource, signals |
| `CharacterBody3D.md` | move_and_slide, is_on_floor, velocity, collision response |
| `RigidBody3D.md` | apply_central_impulse, _integrate_forces, freeze modes |
| `Area3D.md` | body_entered/exited, monitoring, overlapping bodies |
| `AnimationPlayer.md` | play, play_backwards, animation_finished, AnimationLibrary |
| `NavigationAgent3D.md` | target_position, get_next_path_position, is_navigation_finished |
| `AudioStreamPlayer.md` | play, stop, bus, volume_db, pitch_scale, finished |
| `Resource.md` | @export, load(), save(), custom subclasses, duplicate() |
| `Signal.md` | typed declarations, connect(), emit(), disconnect(), CONNECT_* flags |

## Hallucination Red Flag Patterns

Stop and verify when you catch yourself writing:
- `node.call("method_name")` — if you're not sure the method exists
- `$NodePath.some_method()` — if you haven't confirmed `some_method` is in the API ref
- Any method ending in `_v2`, `_ex`, `_new` — Godot 4 rarely uses these suffixes
- `set("property_name", value)` — use direct assignment; `set()` is for dynamic property access only
- `connect("signal_name", callable)` — Godot 4 uses `signal_name.connect(callable)`, not string-based connect
- `yield(...)` — this is Godot 3 only; use `await` in Godot 4

## How to Request a Lookup

Say: `/api-lookup CharacterBody3D.move_and_slide`

Claude will:
1. Read `cookbook/api-ref/CharacterBody3D.md` if it exists
2. Otherwise state "not in api-ref" and use the Godot docs URL format to retrieve it
3. Return the signature, parameters, return type, and a typed usage example

## Adding to api-ref

If you use a class not yet in `cookbook/api-ref/`, add a fragment:
- Minimum 25 non-blank lines
- Extends chain, key properties, key methods with signatures, key signals, typed example
- Follow the format of existing fragments
