---
name: add-node
description: Insert a new node into an existing .tscn file, preserving all existing structure.
invocation: /add-node
---

Add one or more nodes to an existing Godot `.tscn` file without disturbing existing content.

## Input

Provide:
- Target `.tscn` file path
- New node: name, type, parent path
- Optional: properties, sub_resource requirements

## Procedure

1. **Read the existing file** — identify all existing ext_resource, sub_resource, and node entries
2. **Find the correct insertion point** — nodes are ordered depth-first; insert new node after its parent and after all of its parent's existing children
3. **Assign IDs** — new ext_resource: next sequential integer; new sub_resource: `"ClassName_XXXXX"` with unique 5-char suffix from base-34 alphabet
4. **Update load_steps** — recalculate: `count(ext_resource) + count(sub_resource) + 1` and update the header
5. **Preserve path integrity** — all existing `parent=` paths remain unchanged; new node's `parent=` is the exact path string as provided

## Parent Path Preservation Rule

Never rewrite or normalize existing `parent=` values. Only the new node's `parent=` is computed. Existing node declarations are copied verbatim except for the header `load_steps` update.

## CollisionShape3D Rule

If the new node type is `CollisionShape3D`, a sub_resource must be provided or requested. Never insert a CollisionShape3D without `shape = SubResource("...")`.

## Output

Show a diff of the changes:
- Header line (load_steps updated)
- New sub_resource block (if any)
- New node block

Then emit the full updated file.

## Example

Adding a `MeshInstance3D` named `Mesh` as a child of root:

Before (header): `[gd_scene load_steps=2 format=3 uid="uid://cecaux1sm7mo0"]`
After (header):  `[gd_scene load_steps=2 format=3 uid="uid://cecaux1sm7mo0"]`

New node appended after existing root children:
```
[node name="Mesh" type="MeshInstance3D" parent="."]
```

## Sub-resource Addition Example

Adding an `Area3D` with a `SphereShape3D` collision:

```
[sub_resource type="SphereShape3D" id="SphereShape3D_ccccc"]
radius = 1.5

[node name="DetectionArea" type="Area3D" parent="."]

[node name="CollisionShape3D" type="CollisionShape3D" parent="DetectionArea"]
shape = SubResource("SphereShape3D_ccccc")
```

load_steps increases by 1 (one new sub_resource).
