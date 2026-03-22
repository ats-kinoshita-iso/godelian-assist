# godelian-assist

An autonomous Godot 4.x game development assistant — plugin library and agent harness for Claude Code.

Built on top of [agent-workshop](https://github.com/ats-kinoshita-iso/agent-workshop), tuned for GDScript 2.0, C#, and 3D action-RPG development.

## Plugins

### Godot-Specific

| Plugin | Description |
|--------|-------------|
| `godot-patterns` | Scene/node composition, signal architecture, Autoload patterns |
| `gdscript-guide` | GDScript 2.0 typing, idioms, performance optimization |
| `godot-code-quality` | Quality gate: gdlint, gdformat, GdUnit4, C# Roslyn checks |
| `game-design` | Systems design, core loop analysis, balance tuning |

### General Purpose (ported from agent-workshop)

| Plugin | Description |
|--------|-------------|
| `memory-manager` | Persistent memory across Claude sessions |
| `context-sync` | Session context log synchronization |
| `plan-manager` | Plan auditing and registry |
| `eval-framework` | Evaluation criteria and scoring rubrics |
| `observability` | Logging, tracing, instrumentation |
| `agent-patterns` | Reusable agent prompt patterns |
| `planning` | Planning and decomposition skills |
| `test-quality` | Test quality and GdUnit4 coverage |
| `workspace-clean` | Workspace hygiene and cleanup |

## Setup

```bash
# Clone
git clone https://github.com/ats-kinoshita-iso/godelian-assist
cd godelian-assist

# Install Python tooling
uv sync

# Install GDScript tooling (in your Godot project)
pip install gdtoolkit

# Optional: C# formatting
dotnet tool install -g csharpier

# Run tests
uv run pytest
```

## Using Plugins in Your Godot Project

Add godelian-assist as a marketplace source in your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "godelian-assist": {
      "source": {
        "source": "directory",
        "path": "/path/to/godelian-assist"
      }
    }
  }
}
```

Then enable plugins via `/plugins` in Claude Code.

## Development

```bash
# Run all tests
uv run pytest

# Regenerate marketplace.json after adding/removing plugins
uv run python tools/marketplace_gen.py

# Lint
uv run ruff check .

# Type check
uv run mypy .
```

## Project Structure

```
.claude-plugin/       # marketplace.json (auto-generated)
plugins/              # Claude Code plugins
cookbook/             # Hook recipes, CLAUDE.md templates, MCP configs
tools/                # marketplace_gen, skill_loader, hook_validator, plan_manager
tests/                # 183+ tests validating plugin structure and tooling
docs/                 # Architecture documentation
plans/                # Agent planning documents
```

## Target Stack

- **Engine**: Godot 4.x (4.6.1+)
- **Languages**: GDScript 2.0 + C# (.NET 8)
- **Testing**: GdUnit4
- **Quality**: gdlint, gdformat, dotnet-csharpier, Roslyn
