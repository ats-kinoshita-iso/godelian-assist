---
name: scene-audit
description: Audit an existing .tscn file for format correctness, completeness, and spec compliance.
invocation: /scene-audit
---

Inspect a `.tscn` file and report all format errors, warnings, and spec compliance issues.

## Input

Provide:
- Path to the `.tscn` file
- Optional: path to the spec to check against (defaults to `plans/specs/ACTIVE_SPEC.md`)

## Audit Checks

### Format Correctness

| Check | Pass condition |
|---|---|
| Header present | First line is `[gd_scene format=3 ...]` |
| format value | `format=3` |
| UID validity | 13 chars from `[a-y][0-8]` only; no `z` or `9` |
| load_steps accuracy | equals `count(ext_resource) + count(sub_resource) + 1` |
| ext_resource ID format | matches `"N_XXXXX"` pattern |
| sub_resource ID format | matches `"ClassName_XXXXX"` pattern |
| ID uniqueness | no duplicate IDs within ext_resource namespace; no duplicates within sub_resource namespace |
| Root node parent | root has no `parent=` attribute |
| Child parent paths | no leading `./`; paths are relative to root |
| ExtResource references | every `ExtResource("id")` has a matching `[ext_resource ... id="id"]` |
| SubResource references | every `SubResource("id")` has a matching `[sub_resource ... id="id"]` |
| Dangling resources | every declared ext_resource and sub_resource is referenced by at least one node |

### Completeness

| Check | Pass condition |
|---|---|
| CollisionShape3D paired | every CollisionShape3D node has `shape = SubResource(...)` |
| Connection nodes exist | `from` and `to` paths in `[connection]` entries resolve to declared nodes |
| Connection required fields | every `[connection]` has `signal`, `from`, `to`, and `method` |

### Spec Compliance (when spec provided)

- Required node types from spec are present
- Required scripts are referenced as ext_resource
- Required signal connections are wired
- Scene root type matches spec intent (CharacterBody3D for characters, etc.)

## Output Format

```
AUDIT: res://path/to/scene.tscn
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ERRORS (must fix before import):
  [line N] Missing shape on CollisionShape3D "CollisionShape3D"
  [header] load_steps=4 but actual count is 3

WARNINGS (will not prevent import but may cause runtime issues):
  [connection] from="Ghost" — node not declared in scene
  [sub_resource] "Mesh_aaaaa" declared but never referenced

SPEC GAPS (required by ACTIVE_SPEC.md but missing):
  - Camera3D not found; spec requires first-person camera

PASS: 14/17 checks passed
```

## Severity Levels

- **ERROR** — will cause parse failure or import error; blocks use
- **WARNING** — imports but causes runtime warnings or broken gameplay
- **SPEC GAP** — technically valid but incomplete relative to approved design

## Fix Guidance

For each error, suggest the exact correction:
- Wrong load_steps: show the corrected header line
- Missing shape: show the sub_resource block and shape assignment to add
- Dangling reference: show either the missing declaration or the removal of the unused ID
- Invalid UID char: show a corrected UID with valid characters only
