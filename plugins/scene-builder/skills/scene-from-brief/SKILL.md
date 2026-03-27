---
name: scene-from-brief
description: Generate a complete .tscn scene from the approved ACTIVE_SPEC.md designer brief.
invocation: /scene-from-brief
---

Read the active designer spec and produce a complete, valid `.tscn` file for the specified scene.

## Prerequisite

Requires an approved spec at `plans/specs/ACTIVE_SPEC.md`. If no spec is active, stop and say:
> "No active spec found. Run /brief to create one, then /spec-review to approve it."

## Procedure

### Step 1 — Read the Spec
Read `plans/specs/ACTIVE_SPEC.md`. Extract:
- Scene name and purpose (from Intent section)
- Required node types (from Constraints or implementation notes)
- Required scripts (ext_resource)
- Required collision shapes and gameplay volumes
- Signal connections described in the spec

### Step 2 — Plan the Node Hierarchy
Design the tree before writing any file:
- Root node type appropriate to the scene's role (CharacterBody3D for characters, Node3D for environment, Area3D for triggers)
- Group related nodes under pivot nodes (e.g. Head as a Node3D holding Camera3D)
- Every CharacterBody3D or Area3D needs a matching CollisionShape3D child
- List all sub_resources needed (one per CollisionShape3D or other inline resource)

State the planned hierarchy as a tree diagram and ask for confirmation if any choices are ambiguous.

### Step 3 — Generate the .tscn

Follow the generation algorithm from `cookbook/api-ref/tscn-format.md`:

1. Count ext_resource and sub_resource to set `load_steps`
2. Generate a 13-char base-34 UID (chars: `abcdefghijklmnopqrstuvwxy01234568`)
3. Write header, ext_resource, sub_resource, nodes, connections — in that order
4. Apply CollisionShape3D rule: always assign `shape`; never emit bare CollisionShape3D
5. Omit shape properties that are at their defaults

### Step 4 — Report

After writing the file:
- State the output path: `res://path/to/scene.tscn`
- Show load_steps breakdown: `N ext + M sub + 1 = load_steps`
- List every node in the generated tree with its type
- List every signal connection wired
- Flag any spec requirements that could not be satisfied in .tscn alone (e.g. gameplay logic that needs GDScript)

## Scene Type Templates

**Character (CharacterBody3D)**:
```
Root: CharacterBody3D
├── CollisionShape3D (+ CapsuleShape3D sub_resource)
├── MeshInstance3D (optional visual)
└── Head: Node3D (at y = eye height)
    └── Camera3D
```

**Trigger Volume (Area3D)**:
```
Root: Area3D
└── CollisionShape3D (+ SphereShape3D or BoxShape3D sub_resource)
```

**Environment Object (StaticBody3D)**:
```
Root: StaticBody3D
├── MeshInstance3D
└── CollisionShape3D (+ BoxShape3D or ConcavePolygonShape3D sub_resource)
```

## Scope Boundary

This skill writes the `.tscn` file only. GDScript logic, export variables, and shader parameters are separate tasks. Note any that the spec requires but that cannot be expressed in the scene file.
