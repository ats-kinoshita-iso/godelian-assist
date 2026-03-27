# Phase C Research: Godot .tscn Format Specification

**Date**: 2026-03-27
**Status**: Complete — verified against Godot engine source (resource_format_text.cpp, resource_uid.cpp, resource.cpp) and official docs
**Gate**: Findings documented; test scene to be verified in Godot 4.6.1

---

## 1. UID Format

**Character set**: `[a-y][0-8]` — 25 lowercase letters (a through y; `z` excluded) and 9 digits (0 through 8; `9` excluded). This is **base-34**, NOT base-62.

**Length**: 1–13 characters after `uid://`. All real Godot-generated UIDs use the full 13 characters.

**Examples**: `uid://cecaux1sm7mo0`, `uid://c4cp0al3ljsjv`, `uid://bcd12efgh3456`

**Required?**: No. The engine falls back to path-based loading when omitted. No parse error.

**Invalid characters**: If `z` or `9` appears in the UID, `text_to_id` returns `INVALID_ID` — treated as absent.

**For generation by Claude**: Pick 13 random characters from `abcdefghijklmnopqrstuvwxy01234568`. Do not use z or 9.

```python
# Reference: generate a valid UID string
import random
CHARS = "abcdefghijklmnopqrstuvwxy01234568"
uid = "uid://" + "".join(random.choices(CHARS, k=13))
```

---

## 2. ext_resource ID Format

**Format**: `"<N>_<5chars>"` where N is a sequential integer starting at 1, and the 5-char suffix is from the same base-34 alphabet.

**Examples**: `"1_7bt6s"`, `"2_eorut"`, `"1_r3bjq"`

**Parser behaviour**: Treats the ID as an opaque quoted string. Simple IDs like `"1_aaaaa"` are valid. IDs must be unique within the ext_resource namespace.

**Reference syntax**:
```
[ext_resource type="Script" path="res://src/player/player.gd" id="1_aaaaa"]
...
script = ExtResource("1_aaaaa")
```

---

## 3. sub_resource ID Format

**Format**: `"<ClassName>_<5chars>"` — the class name prefix aids debugging.

**Examples**: `"CapsuleShape3D_fdxgg"`, `"SphereShape3D_tj6p1"`, `"SphereMesh_4w3ye"`

**Parser behaviour**: Same as ext_resource — opaque string. Simple IDs like `"CapsuleShape3D_aaaaa"` work.

**ext_resource and sub_resource IDs are in separate namespaces** — the same string can appear in both without conflict (they are referenced differently: `ExtResource("x")` vs `SubResource("x")`).

**Reference syntax**:
```
[sub_resource type="CapsuleShape3D" id="CapsuleShape3D_aaaaa"]
radius = 0.4
height = 1.8
...
shape = SubResource("CapsuleShape3D_aaaaa")
```

---

## 4. load_steps

**Formula**: `load_steps = count(ext_resource) + count(sub_resource) + 1`

**Wrong value**: No parse error. Value only affects loading progress bars. Omitting `load_steps` entirely also causes no error.

**Omit when**: No ext_resource or sub_resource entries exist (the header shrinks to just `[gd_scene format=3]`).

---

## 5. Node Parent Paths

| Node position | parent= attribute |
|---|---|
| Scene root | **Omitted entirely** — no parent= attribute at all |
| Direct child of root | `parent="."` |
| Grandchild (child of "Arm") | `parent="Arm"` |
| Great-grandchild (child of "Arm/Hand") | `parent="Arm/Hand"` |

**No leading `./`** in paths (not `parent="./Arm"`). Paths are relative to root, root name excluded.

---

## 6. Signal Connection Syntax

**Required fields**: `signal`, `from`, `to`, `method` — all four always present.

```
[connection signal="health_changed" from="HealthComponent" to="." method="_on_health_changed"]
```

**Optional fields** (omit when default):
- `flags=<int>` — omitted when flags == 2 (CONNECT_PERSIST, the default for editor connections)
  - 1 = CONNECT_DEFERRED, 4 = CONNECT_ONE_SHOT, 8 = CONNECT_REFERENCE_COUNTED
- `unbinds=<int>` — omitted when 0
- `binds= [v1, v2]` — omitted when empty

**from/to paths**: Same convention as parent= — relative to root, use `"."` for root itself.

---

## 7. Shape Sub-resource Properties

Default values are **never stored** — only non-default values appear.

| Shape | Property | Type | Default |
|---|---|---|---|
| CapsuleShape3D | radius | float | 0.5 |
| CapsuleShape3D | height | float | 2.0 |
| BoxShape3D | size | Vector3 | Vector3(1,1,1) |
| SphereShape3D | radius | float | 0.5 |
| CylinderShape3D | radius | float | 0.5 |
| CylinderShape3D | height | float | 2.0 |

**Examples**:
```
[sub_resource type="CapsuleShape3D" id="CapsuleShape3D_aaaaa"]
radius = 0.4
height = 1.8

[sub_resource type="BoxShape3D" id="BoxShape3D_bbbbb"]
size = Vector3(2, 1, 2)

[sub_resource type="SphereShape3D" id="SphereShape3D_ccccc"]
radius = 1.2
```

---

## 8. format Version

`format=3` for all Godot 4.x (4.0 through 4.6+). No variation by minor version.

---

## 9. Minimum Valid .tscn

```
[gd_scene format=3]

[node name="Root" type="Node"]
```

Three lines. No uid, no load_steps needed when no resources.

---

## 10. Headless Validation

```bash
godot --headless --import
```

Parses and imports all resources in the project. Parse errors appear in stdout. Does NOT need `--quit` (handles exit automatically). This is the canonical CI validation command.

`--check-only` is for GDScript only — does NOT validate .tscn files.

---

## Complete Reference .tscn (Player scene)

A CharacterBody3D player with CapsuleShape3D, Camera3D under a Head pivot, and an attached script — fully valid for Godot 4.6.1:

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

load_steps = 1 ext + 1 sub + 1 = 3 ✓
