---
name: wire-signals
description: Add signal connections to an existing .tscn file using correct [connection] syntax.
invocation: /wire-signals
---

Append `[connection]` entries to a Godot `.tscn` file.

## Input

Provide:
- Target `.tscn` file path
- One or more connections, each with: signal name, from node, to node, method name
- Optional: flags, binds, unbinds

## [connection] Syntax

```
[connection signal="signal_name" from="SourcePath" to="TargetPath" method="_on_method_name"]
```

**Required fields**: `signal`, `from`, `to`, `method` — all four always present, in this order.

**Path convention**: Same as `parent=` paths — relative to root, no leading `./`:
- Root node itself: `"."`
- Direct child named "Health": `"Health"`
- Grandchild "Head/Camera3D": `"Head/Camera3D"`

## Optional Fields

Include only when non-default:

| Field | Omit when | Values |
|---|---|---|
| `flags` | flags == 2 (editor default, CONNECT_PERSIST) | 1=DEFERRED, 4=ONE_SHOT, 8=REF_COUNTED |
| `unbinds` | unbinds == 0 | integer |
| `binds` | empty | `[value1, value2, ...]` |

## Procedure

1. **Read the existing file** — note where the last node or existing connection entry ends
2. **Verify nodes exist** — confirm `from` and `to` paths correspond to declared nodes in the file; warn if not found
3. **Check for duplicates** — if an identical connection already exists, skip and report
4. **Append connections** — add after all node entries, one per line, blank line before each new connection block

## Output

Show each new `[connection]` line that will be added. Then emit or diff the updated file.

## Examples

Basic signal connection (health component → player HUD):
```
[connection signal="health_changed" from="HealthComponent" to="." method="_on_health_changed"]
```

Deferred signal with args:
```
[connection signal="area_entered" from="DetectionArea" to="." method="_on_detection" flags=1 binds=[1]]
```

One-shot signal:
```
[connection signal="animation_finished" from="AnimationPlayer" to="." method="_on_intro_done" flags=4]
```

## Common Signal Names by Node Type

| Node | Common signals |
|---|---|
| Area3D | `body_entered`, `body_exited`, `area_entered` |
| AnimationPlayer | `animation_finished`, `animation_started` |
| Timer | `timeout` |
| Button | `pressed`, `toggled` |
| CharacterBody3D | (custom signals via script) |
