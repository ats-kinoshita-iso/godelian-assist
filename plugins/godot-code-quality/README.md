# godot-code-quality

Unified quality gate for Godot 4.x projects. Runs GDScript lint, GDScript format checks, GdUnit4 tests, and C# Roslyn checks as a single pass/fail gate.

## Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| `quality` | "check quality", "run the gate" | Full quality check with numeric score |
| `quality-fix` | "fix formatting", "auto-fix lint" | Auto-fix formatting issues, report remaining |

## Prerequisites

```bash
# GDScript tooling (gdlint + gdformat)
pip install gdtoolkit

# C# formatting (optional, only needed for C# projects)
dotnet tool install -g csharpier

# GdUnit4 — install via Godot Asset Library or:
# https://github.com/MikeSchulze/gdUnit4
```

## Hooks

- **PreToolUse (git commit)**: runs gdlint + gdformat check before every commit
- **Stop**: prints a brief quality summary at the end of each Claude session

## Checks and Scoring

| Check | Language | Fixable |
|-------|----------|---------|
| `gdlint` | GDScript | No (manual) |
| `gdformat` | GDScript | Yes (`quality-fix`) |
| GdUnit4 | GDScript/C# | No (manual) |
| `dotnet-csharpier` | C# | Yes (`quality-fix`) |
| `dotnet build -warnaserror` | C# | No (manual) |

Score = (passing checks / applicable checks) × 100.
