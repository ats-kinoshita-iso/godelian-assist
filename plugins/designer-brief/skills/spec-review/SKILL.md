---
name: spec-review
description: >-
  Review Claude's implementation spec before any code is written. Approve,
  revise, or reject — then Claude proceeds only on explicit approval.
---

## The spec review step

After Claude generates a spec from a brief, it writes it to `plans/specs/<slug>.md` and
copies it to `plans/specs/ACTIVE_SPEC.md`. Implementation does not begin until the designer
signals approval. This is the single most important gate in the workflow.

## Reading the spec

The spec at `plans/specs/ACTIVE_SPEC.md` contains:

- **Node structure** — the scene tree Claude will create (node names and types)
- **Signal map** — every signal, its parameters, who emits it, who receives it
- **Resource subclasses** — any custom `extends Resource` classes with typed fields
- **Files to create** — exact `res://` paths of new `.gd` and `.tscn` files
- **Files to modify** — existing files Claude will change and what changes
- **GDScript skeletons** — typed stubs showing the public API of each class
- **Test plan** — what GdUnit4 tests will be written

Focus your review on: node structure (is the scene hierarchy right?), signals (does the
decoupling make sense?), and files to modify (are there any surprises?).

## Three review outcomes

**Approved** — reply with "approved" or "proceed":
Claude sets `ACTIVE_SPEC.md`, moves feature status to `in_progress` in the game backlog,
and begins implementation. No files are written before this confirmation.

**Revised** — mark specific sections inline with `[REVISE: your note]`:
```markdown
- Signal: `dash_ready()` emitted by DashComponent [REVISE: should be dash_cooldown_ended — clearer name]
- Files to modify: src/ui/hud.gd [REVISE: don't touch hud.gd — connect via EventBus instead]
```
Return the marked-up spec to Claude. Claude updates the spec and re-presents it for review.
This loops until approval.

**Rejected** — reply with "rejected" or "start over":
Claude discards the spec and asks for a new or revised brief. Use this when the
architectural approach is wrong, not just details. The feature stays `queued` in the backlog.

## Common revision patterns

- **Wrong node type**: "Use Area3D for the hitbox, not MeshInstance3D"
- **Scope creep caught early**: "The spec added inventory integration — that's out of scope, remove it"
- **Signal naming**: "Use past-tense signal names — `dash_started` not `on_dash`"
- **Missing @export**: "The dash_distance should be @export so I can tune it in the Inspector"
- **Wrong parent**: "DashComponent should be a child of CharacterBody3D, not a sibling"

## After approval

Claude will:
1. Write all `.gd` files (fully typed, with class_name and signals)
2. Write all `.tscn` files (text format, using scene-builder patterns)
3. Write `.tres` resource files if the spec includes custom Resources
4. Run `gdlint` on all new `.gd` files
5. Run type-check with `godot --headless --check-only`
6. Write GdUnit4 tests per the test plan
7. Report back: what was created, any issues found, what to check

The designer does not see code during implementation — only the report at the end.
