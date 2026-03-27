# API Reference: Godot .tscn File Format

**Godot version**: 4.x (4.0 – 4.6+)
**format value**: `3` (constant across all 4.x minor versions)
**Source**: Verified against `resource_format_text.cpp`, `resource_uid.cpp`, official docs

---

## File Header

```
[gd_scene load_steps=N format=3 uid="uid://XXXXXXXXXXXXX"]
```

- `format=3` — always 3 for Godot 4.x
- `load_steps` — optional; equals `count(ext_resource) + count(sub_resource) + 1`; wrong value causes no error (only affects progress bar)
- `uid` — optional; omit freely; engine falls back to path-based loading when absent

**Minimal valid file** (no resources):
```
[gd_scene format=3]

[node name="Root" type="Node"]
```

---

## UID Format

**Character set**: `abcdefghijklmnopqrstuvwxy01234568`
Exactly 25 lowercase letters (`a`–`y`; `z` excluded) plus 9 digits (`0`–`8`; `9` excluded).
This is **base-34**, not base-62.

**Length**: 13 characters after `uid://`

**Examples**: `uid://cecaux1sm7mo0`, `uid://c4cp0al3ljsjv`

**Invalid characters**: `z` or `9` anywhere in the UID causes `text_to_id` to return `INVALID_ID` — treated as absent, no parse error.

```python
# Generate a valid UID
import random
CHARS = "abcdefghijklmnopqrstuvwxy01234568"
uid = "uid://" + "".join(random.choices(CHARS, k=13))
```

---

## ext_resource

External file references (scripts, textures, audio, other scenes).

**Syntax**:
```
[ext_resource type="Script" path="res://src/player/player.gd" id="1_aaaaa"]
```

**ID format**: `"<N>_<5chars>"` — sequential integer starting at 1, underscore, 5 chars from base-34 alphabet.
Simple IDs like `"1_aaaaa"` are fully valid. IDs must be unique within the ext_resource namespace.

**Reference in node properties**:
```
script = ExtResource("1_aaaaa")
```

**Common types**: `Script`, `Texture2D`, `AudioStream`, `PackedScene`, `Mesh`, `Material`

---

## sub_resource

Inline resource definitions (shapes, meshes, materials not worth externalizing).

**Syntax**:
```
[sub_resource type="CapsuleShape3D" id="CapsuleShape3D_aaaaa"]
radius = 0.4
height = 1.8
```

**ID format**: `"<ClassName>_<5chars>"` — class name prefix aids debugging; 5-char suffix from base-34.
Simple IDs like `"CapsuleShape3D_aaaaa"` are valid.

**Reference in node properties**:
```
shape = SubResource("CapsuleShape3D_aaaaa")
```

**Namespace**: ext_resource and sub_resource IDs are in **separate namespaces** — the same string can appear in both without conflict.

---

## Shape Sub-resource Defaults

Only non-default values are stored. Omit properties at their defaults.

| Shape | Property | Type | Default |
|---|---|---|---|
| CapsuleShape3D | radius | float | 0.5 |
| CapsuleShape3D | height | float | 2.0 |
| BoxShape3D | size | Vector3 | Vector3(1, 1, 1) |
| SphereShape3D | radius | float | 0.5 |
| CylinderShape3D | radius | float | 0.5 |
| CylinderShape3D | height | float | 2.0 |

Examples:
```
[sub_resource type="CapsuleShape3D" id="CapsuleShape3D_bbbbb"]
radius = 0.4
height = 1.8

[sub_resource type="BoxShape3D" id="BoxShape3D_ccccc"]
size = Vector3(2, 1, 2)

[sub_resource type="SphereShape3D" id="SphereShape3D_ddddd"]
# radius = 0.5 is default — omit entirely
```

---

## Node Declarations

```
[node name="NodeName" type="TypeName" parent="path/to/parent"]
property = value
```

### parent= Attribute Rules

| Node position | parent= value |
|---|---|
| Scene root | **Omitted** — no parent= attribute |
| Direct child of root | `parent="."` |
| Child of node "Arm" | `parent="Arm"` |
| Child of "Arm/Hand" | `parent="Arm/Hand"` |

No leading `./` in paths. Paths are relative to root, root name excluded.

### CollisionShape3D Rule

`CollisionShape3D` nodes **must** have a `shape` property assigned immediately after declaration. A bare CollisionShape3D without a shape causes a runtime warning and non-functional collision.

```
[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
shape = SubResource("CapsuleShape3D_bbbbb")
```

### Transform

```
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, x, y, z)
```

Identity rotation with translation `(x, y, z)`. Head pivot example at y=1.4:
```
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.4, 0)
```

---

## Signal Connections

Declared at the end of the file, after all nodes.

```
[connection signal="signal_name" from="SourceNode" to="TargetNode" method="_on_method"]
```

**Required fields**: `signal`, `from`, `to`, `method` — all four always present.

**Path convention**: Same as `parent=` — relative to root; `"."` for root itself.

**Optional fields** (omit when at default):
- `flags=<int>` — omit when flags == 2 (CONNECT_PERSIST, the editor default)
  - 1 = CONNECT_DEFERRED, 4 = CONNECT_ONE_SHOT, 8 = CONNECT_REFERENCE_COUNTED
- `unbinds=<int>` — omit when 0
- `binds=[v1, v2]` — omit when empty

```
[connection signal="health_changed" from="HealthComponent" to="." method="_on_health_changed"]
```

---

## Generation Order

When generating a .tscn file, write sections in this order:

1. `[gd_scene ...]` header
2. `[ext_resource ...]` entries (one per line, blank line between header and first)
3. `[sub_resource ...]` entries (blank line before each)
4. `[node ...]` entries (blank line before each; scene root first, then children in depth-first order)
5. `[connection ...]` entries (blank line before each)

---

## Headless Validation

```bash
godot --headless --import
```

Parses and imports all project resources. Parse errors appear in stdout. Use this for CI validation of .tscn files. (`--check-only` only validates GDScript, not .tscn.)

---

## Complete Reference Example

Player scene: CharacterBody3D with CapsuleShape3D, Head pivot, Camera3D, attached script.

```
[gd_scene load_steps=3 format=3 uid="uid://bcd12efgh3456a"]

[ext_resource type="Script" path="res://src/player/player.gd" id="1_aaaaa"]

[sub_resource type="CapsuleShape3D" id="CapsuleShape3D_bbbbb"]
radius = 0.4
height = 1.8

[node name="Player" type="CharacterBody3D"]
script = ExtResource("1_aaaaa")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
shape = SubResource("CapsuleShape3D_bbbbb")

[node name="Head" type="Node3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.4, 0)

[node name="Camera3D" type="Camera3D" parent="Head"]

[connection signal="health_changed" from="HealthComponent" to="." method="_on_health_changed"]
```

`load_steps = 1 ext + 1 sub + 1 = 3` ✓
