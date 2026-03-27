# godelian-assist

An autonomous Godot 4.x game development assistant — plugin library and agent harness for Claude Code.

## Target Environment

- **Engine**: Godot 4.x (4.6.1+)
- **Languages**: GDScript 2.0 and C# (.NET 8)
- **Testing**: GdUnit4
- **Platform**: Windows / Linux / macOS

## Stack

- **Python tooling**: managed with `uv`
- **JS/TS**: managed with `bun` (if needed)
- **Godot**: use `godot --headless` for CLI operations

## Commands

### Python tooling
- Install deps: `uv sync`
- Run tests: `uv run pytest`
- Lint: `uv run ruff check .`
- Format: `uv run ruff format .`
- Type check: `uv run mypy .`
- Regenerate marketplace: `uv run python tools/marketplace_gen.py`

### Godot (when working in a game repo)
- **Godot executable**: `"/c/Users/akino/Desktop/Godot_v4.6.1-stable_win64.exe"` (add to PATH or use full path)
- Validate GDScript: `godot --headless --check-only -s <script.gd>`
- Run GdUnit4 tests: `godot --headless -s addons/gdUnit4/bin/GdUnitCmdTool.gd`
- Format GDScript: `gdformat <file.gd>` (requires gdtoolkit)
- Lint GDScript: `gdlint <file.gd>` (requires gdtoolkit)
- Format C#: `dotnet-csharpier .`
- Lint C#: `dotnet build` (Roslyn analyzers)

## Directory Structure

```
.claude-plugin/       # Marketplace manifest (auto-generated)
plugins/              # Claude Code plugins for Godot development
  godot-patterns/     #   Scene/node/signal architecture patterns
  gdscript-guide/     #   GDScript idioms, typing, best practices
  godot-code-quality/ #   Quality gate: gdlint, gdformat, GdUnit4, C# checks
  game-design/        #   Game systems, loop design, balance
  memory-manager/     #   Persistent memory across sessions
  context-sync/       #   Context log synchronization
  plan-manager/       #   Plan auditing and registry
  eval-framework/     #   Evaluation criteria and scoring
  observability/      #   Logging, tracing, instrumentation
  agent-patterns/     #   Reusable agent prompt patterns
  planning/           #   Planning skills
  test-quality/       #   Test quality and coverage
  workspace-clean/    #   Workspace hygiene
cookbook/             # Golden baseline configs
  claude-md/          #   CLAUDE.md templates
  hooks/              #   Hook recipes (including Godot hooks)
  mcp/                #   MCP server configs
tools/                # Development and validation tooling
tests/                # Plugin and tool test suite
docs/                 # Architecture and usage documentation
plans/                # Agent planning documents
  active/             #   In-progress plans
  validation-reports/ #   Per-phase validation reports
```

## Generated Files

`.claude-plugin/marketplace.json` is **auto-generated** — never edit it by hand.
Run `uv run python tools/marketplace_gen.py` to regenerate.

## Plugin Format

```
plugins/<name>/
├── .claude-plugin/
│   └── plugin.json         # Required: name, description, version, keywords, license
├── skills/
│   └── <skill-name>/
│       └── SKILL.md        # YAML frontmatter (name, description) + body ≥10 lines
├── hooks/                  # Optional
│   └── hooks.json
└── README.md
```

## Code Style

### Python
- Type annotations required on all function and method signatures
- Docstrings required on all public functions and classes
- Max line length: 100 characters
- Naming: `snake_case` functions/vars, `PascalCase` classes, `SCREAMING_SNAKE_CASE` constants
- Mypy strict mode — no untyped code

### GDScript
- Static typing on all variables, parameters, and return types
- Use `class_name` for reusable classes
- Signals declared at top of class
- `snake_case` for functions/variables, `PascalCase` for classes/nodes
- Maximum function length: 30 lines — extract helpers if longer
- Prefer composition (child nodes) over inheritance

### C#
- Use nullable reference types (`#nullable enable`)
- `PascalCase` for methods/properties, `camelCase` for local variables
- XML doc comments on public API
- Use `partial` classes for generated Godot code separation

## Godot Conventions

- **Scene composition**: one scene per logical entity; expose config via `@export`
- **Signals over direct references**: decouple nodes with signals where possible
- **Autoloads sparingly**: use for truly global state (GameManager, EventBus)
- **Resource files**: extract reusable data into `.tres`/`.res` Resources
- **GdUnit4**: all GDScript tests in `tests/` directory; C# tests in `tests/csharp/`
- **Version control**: commit `.godot/` only for imported resource metadata; never commit local overrides

## Proactiveness Rules

DO:
- Fix obvious type errors or missing static types in GDScript spotted while reading
- Suggest signal-based decoupling when direct `get_node` chains appear
- Run GdUnit4 tests after modifying game scripts
- Check `gdlint` output before committing GDScript changes

DO NOT:
- Modify `.godot/` generated files unless explicitly asked
- Change node names in scenes (breaks `get_node` calls project-wide)
- Remove `@tool` annotations without confirming intent
- Refactor scenes not part of the current task
