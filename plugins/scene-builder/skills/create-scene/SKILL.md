---
name: create-scene
description: Generate a valid Godot .tscn file from a node list and properties.
invocation: /create-scene
---

Generate a Godot 4.x `.tscn` file that passes headless import validation.

## Input

Provide:
- Scene name (becomes the root node name and the filename stem)
- Root node type (e.g. `CharacterBody3D`, `Node3D`, `Area3D`)
- Child nodes with types and optional properties
- Optional: script path, signal connections

## Generation Algorithm

Follow this order strictly:

1. **Collect resources** — identify all ext_resource (scripts, textures) and sub_resource (shapes, meshes) references needed by any node property
2. **Assign IDs** — ext_resource IDs: `"1_aaaaa"`, `"2_bbbbb"`, ... incrementing; sub_resource IDs: `"ClassName_aaaaa"`, `"ClassName_bbbbb"`, ...
3. **Compute load_steps** — `count(ext_resource) + count(sub_resource) + 1`
4. **Generate UID** — 13 chars from `abcdefghijklmnopqrstuvwxy01234568` (base-34; no `z`, no `9`)
5. **Write header** — `[gd_scene load_steps=N format=3 uid="uid://XXXXXXXXXXXXX"]`
6. **Write ext_resource entries** — one per line, blank line after header
7. **Write sub_resource entries** — blank line before each; only non-default property values
8. **Write node entries** — root first (no `parent=`), children depth-first with correct `parent=` paths
9. **Write connections** — at end of file, one per line

## Parent Path Rules

| Node | parent= |
|---|---|
| Root | omitted |
| Direct child | `parent="."` |
| Child of "Arm" | `parent="Arm"` |
| Child of "Arm/Hand" | `parent="Arm/Hand"` |

No leading `./`. Paths are relative to root; root name excluded.

## CollisionShape3D Rule

Every `CollisionShape3D` node **must** have a `shape` sub_resource assigned. Never emit a bare CollisionShape3D — always pair it with a sub_resource entry and assign `shape = SubResource("...")`.

## Shape Defaults (omit if at default)

| Shape | Property | Default |
|---|---|---|
| CapsuleShape3D | radius | 0.5 |
| CapsuleShape3D | height | 2.0 |
| BoxShape3D | size | Vector3(1, 1, 1) |
| SphereShape3D | radius | 0.5 |

## Output

Emit the complete `.tscn` file. Then state:
- File path: `res://path/to/scene.tscn`
- load_steps breakdown: `N ext + M sub + 1 = load_steps`
- Any CollisionShape3D shape pairings made

## Validation

After writing, confirm with:
```bash
godot --headless --import
```
Any parse errors appear in stdout. Fix and regenerate if errors are found.

## Example

```
[gd_scene load_steps=3 format=3 uid="uid://c4cp0al3ljsjv"]

[ext_resource type="Script" path="res://src/enemy/enemy.gd" id="1_aaaaa"]

[sub_resource type="CapsuleShape3D" id="CapsuleShape3D_bbbbb"]
radius = 0.4
height = 1.8

[node name="Enemy" type="CharacterBody3D"]
script = ExtResource("1_aaaaa")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
shape = SubResource("CapsuleShape3D_bbbbb")

[node name="Sprite3D" type="Sprite3D" parent="."]
```
