<!-- Last updated: 2026-03-22 -->

# Godot 4.x Project — CLAUDE.md Template

Copy this file to your Godot project root as `CLAUDE.md` and fill in the placeholders.

---

```markdown
# <Project Name>

A 3D action-RPG built with Godot 4.x.

## Target Environment

- **Engine**: Godot 4.x (4.6.1+)
- **Languages**: GDScript 2.0 and C# (.NET 8)
- **Testing**: GdUnit4
- **Platform**: <Windows / Linux / macOS / all>

## Commands

### Engine
- Run project: `godot --path .`
- Headless check: `godot --headless --check-only -s project.godot`
- Run GdUnit4 tests: `godot --headless -s addons/gdUnit4/bin/GdUnitCmdTool.gd --add res://tests`
- Export: `godot --headless --export-release "<preset>" build/<output>`

### GDScript quality
- Lint: `gdlint $(find . -name "*.gd" -not -path "./.godot/*")`
- Format: `gdformat $(find . -name "*.gd" -not -path "./.godot/*")`
- Format check (no write): `gdformat --check $(find . -name "*.gd" -not -path "./.godot/*")`

### C# quality
- Build: `dotnet build`
- Format check: `dotnet-csharpier --check .`
- Format apply: `dotnet-csharpier .`

## Directory Structure

```
project.godot           # Godot project file
addons/                 # Third-party addons (gdUnit4, etc.)
assets/                 # Art, audio, fonts — no code here
src/                    # GDScript and C# source
  player/               # Player scenes and scripts
  enemies/              # Enemy scenes and scripts
  ui/                   # UI scenes and scripts
  systems/              # Autoloads and system managers
  resources/            # Custom Resource subclasses (.gd only)
data/                   # .tres resource instances (stats, items, configs)
tests/                  # GdUnit4 test files
  test_<class>.gd       # One test file per class
scenes/                 # Godot scenes (.tscn)
  levels/               # Level scenes
  entities/             # Character/enemy/prop scenes
```

## GDScript Conventions

- **Static typing required** on all variables, parameters, and return types
- Use `class_name` for any script referenced from other scripts
- `snake_case` for variables and functions, `PascalCase` for class names
- Signals declared at top of class, past-tense names (`health_changed`, not `on_change_health`)
- `@export` for all Inspector-tunable properties with explicit types
- `@onready` for all node references — never call `get_node` in `_process`
- Maximum function length: 30 lines — extract helpers if longer
- Guard clauses over deep nesting

## C# Conventions

- `#nullable enable` at top of every file
- `partial` classes for all Godot node scripts
- `PascalCase` methods/properties, `_camelCase` private fields, `camelCase` locals
- `[Export]` for Inspector properties, `GetNode<T>()` in `_Ready()` for node refs
- XML doc comments on all public API

## Godot Architecture Rules

- **One scene per logical entity** — Player, Enemy, Door are separate `.tscn` files
- **Composition over inheritance** — use component child nodes for shared behavior
- **Signals over direct node references** — decouple with signals and EventBus Autoload
- **Resources for data** — stats, items, configs go in `Resource` subclasses, not dictionaries
- **No scene tree logic in `_process`** — `get_node`, `find_child`, `get_children` are cached at `_ready`
- **Autoloads sparingly** — only for truly global state (EventBus, GameManager, SaveSystem)

## Testing (GdUnit4)

- Test files live in `tests/`, named `test_<class_name>.gd`
- Every test class extends `GdUnitTestSuite`
- Use `before_test()` / `after_test()` for setup/teardown
- Use `auto_free()` for any node created in tests
- Test naming: `test_<method>_<condition>_<expected>`
- Run before every commit: `godot --headless -s addons/gdUnit4/bin/GdUnitCmdTool.gd --add res://tests`

## Commit Convention

- `feat:` new gameplay feature or mechanic
- `fix:` bug fix in game logic
- `asset:` new or updated art/audio asset
- `scene:` new or updated scene file
- `refactor:` code cleanup without behavior change
- `test:` new or updated GdUnit4 tests
- `chore:` build, tooling, dependency changes

## Proactiveness Rules

DO proactively:
- Add static types to GDScript when you see untyped vars while reading
- Suggest signal decoupling when direct `get_node("../../Other")` calls appear
- Run `gdlint` output after modifying GDScript files
- Note when a `.tscn` node name change would break existing `get_node` calls

DO NOT proactively:
- Modify `.godot/` generated files
- Rename nodes in scenes (breaks references project-wide)
- Remove `@tool` annotations without explicit instruction
- Refactor scenes not part of the current task

## Session Protocol

Every coding session follows the designer-brief workflow:

1. **Start**: Check `plans/game-backlog.json` for the current `in_progress` feature. Read its spec at `plans/specs/ACTIVE_SPEC.md`. If no approved spec exists, run `/brief` before writing any code.
2. **Implement**: Use `agent/prompts-game/implement_feature.md` as the implementation guide.
3. **Iterate**: After designer playtest, use `agent/prompts-game/iterate_on_feedback.md` to process feedback. Every change requires `[APPROVED]` or `[SKIP]` marker before implementation.
4. **Complete**: Run `/feature-complete` when all acceptance criteria are met.

Session hooks are configured in `cookbook/hooks/game-session.md` — the `designer-brief` plugin's `PreToolUse` hook warns when no active spec is set before writing `.gd`, `.tscn`, or `.tres` files.
```
