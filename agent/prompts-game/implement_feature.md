# Agent Prompt: Implement Feature

**Purpose**: Drive a complete feature implementation cycle for a Godot 4.x game project.
**Prerequisite**: An approved spec must exist at `plans/specs/ACTIVE_SPEC.md` with the `[APPROVED]` marker.
**Invocation**: Paste this prompt into a Claude Code session, or reference it via the `/feature-complete` skill.

---

## Step 1 — GET BEARINGS

Read the project state before touching any code:

```
1. Read CLAUDE.md — note Godot path, quality commands, autoload names, style rules
2. Read plans/specs/ACTIVE_SPEC.md — confirm [APPROVED] marker is present
3. Read plans/game-backlog.json — find the in_progress feature entry
4. Skim the relevant src/ directory — understand what already exists
5. Run: godot --headless --import — confirm project parses cleanly before changes
```

**If `[APPROVED]` is not in ACTIVE_SPEC.md, stop immediately.**

> "No approved spec found. The spec at `plans/specs/ACTIVE_SPEC.md` does not contain the `[APPROVED]` marker. Run `/spec-review` to get designer approval before implementing."

Never implement without an approved spec. This rule has no exceptions.

---

## Step 2 — PLAN THE IMPLEMENTATION

Before writing any file, produce a written implementation plan:

```
Files to create:
  - src/<system>/<name>.gd         (GDScript class)
  - scenes/<name>.tscn             (scene, if needed)
  - tests/<name>_test.gd           (GdUnit4 tests)

Files to modify:
  - src/autoloads/event_bus.gd     (add signals if needed)
  - project.godot                  (register autoloads if needed)

Signals to add to EventBus: [list]
Nodes required in scene: [list with types]
Collision layer assignments: [list]
```

Show this plan to the designer and wait for confirmation if any choices are ambiguous.

---

## Step 3 — CHECK GDAI MCP (OPTIONAL)

If GDAI MCP is configured in `.claude/settings.json`:

```
1. get_editor_screenshot — confirm the editor is open and on the right scene
2. Use available MCP tools to inspect existing nodes before creating new ones
3. After implementation: get_running_scene_screenshot — visual confirmation
```

If GDAI MCP is not configured, proceed without it. All implementation must work headlessly — never require the editor to be open for code generation.

---

## Step 4 — WRITE CODE

Write all files per the implementation plan. Enforce these rules on every file:

**GDScript rules**:
- `class_name` on every script — no anonymous scripts
- Static typing on every variable, parameter, and return type — no untyped declarations
- `@export` for all designer-facing properties
- Signals declared with typed parameters
- `snake_case` for functions, variables, signals; `PascalCase` for class names; `CONSTANT_CASE` for constants
- Max line length: 100 characters

**Scene rules** (when writing .tscn):
- Follow `cookbook/api-ref/tscn-format.md` exactly
- UID: 13 chars from base-34 alphabet `abcdefghijklmnopqrstuvwxy01234568`
- Every `CollisionShape3D` must have a `shape` assigned
- `load_steps = count(ext_resource) + count(sub_resource) + 1`
- No bare `CollisionShape3D` nodes

**API rules**:
- Look up every Godot class in `cookbook/api-ref/` before using it
- Use `signal_name.connect(method)` not string-based connect
- Use `await` not `yield`
- Never use `set("property", value)` for known properties — use direct assignment

---

## Step 5 — RUN QUALITY GATE

Run all checks in sequence. Do not proceed past a failure without fixing it.

```bash
# 1. Lint
gdlint src/

# 2. Format check
gdformat --check src/

# 3. Import validation
godot --headless --import

# 4. Feature tests
godot --headless -s addons/gdUnit4/bin/GdUnitCmdTool.gd --add tests/<feature>/

# 5. Full test suite
godot --headless -s addons/gdUnit4/bin/GdUnitCmdTool.gd --add tests/
```

If any step fails:
- Fix the issue
- Re-run that step and all subsequent steps
- Do not mark the feature complete until all 5 pass

---

## Step 6 — SCREENSHOT REVIEW (if GDAI MCP available)

```
1. Open the scene in the Godot editor
2. get_editor_screenshot — capture the scene layout
3. Play the scene: use run_scene tool or manual play
4. get_running_scene_screenshot — capture runtime state
5. Compare against spec's "Designer acceptance" criteria
6. Report: what matches, what differs, what requires designer playtest
```

If GDAI MCP is not available, skip to Step 7.

---

## Step 7 — COMMIT

```bash
git add src/ scenes/ tests/ plans/
git status   # confirm only expected files are staged
git commit -m "feat: <feature title from ACTIVE_SPEC.md>

Implements: <one-line description>
Quality gate: lint ✓ format ✓ import ✓ tests ✓

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

After commit:
- Update `plans/game-backlog.json`: set feature status to `"pending_approval"`
- Remove `ACTIVE_SPEC.md` (or mark it `[PENDING_REVIEW]`)
- Report to the designer: "Feature implemented. Awaiting your playtest."

---

## Quality Checklist (run mentally before committing)

- [ ] All new GDScript files have `class_name`
- [ ] All variables and parameters are statically typed
- [ ] All new signals have typed parameters
- [ ] No `yield`, no string-based `connect()`
- [ ] No `CollisionShape3D` without a `shape`
- [ ] EventBus signals are in `event_bus.gd`, not scattered in scripts
- [ ] `game-backlog.json` updated to `pending_approval`
- [ ] All 5 quality gate steps passed
