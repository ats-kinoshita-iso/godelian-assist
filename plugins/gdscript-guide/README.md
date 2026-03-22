# gdscript-guide

GDScript 2.0 idioms, static typing, performance, and style guidance for Godot 4.x.

## Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| `typing-guide` | "add types to this script", "type this GDScript" | Full static type annotation review and rewrite |
| `idioms` | "make this more idiomatic", "modernize this script" | Rewrite to idiomatic GDScript 2.0 patterns |
| `performance` | "optimize this script", "why is this lagging?" | Profile and fix GDScript performance issues |

## Key Principles

- All variables, parameters, and return types must be statically typed
- Use `match` over `if/elif` chains for state machines
- Use `await` for async patterns instead of callback functions
- Cache `get_node` calls in `@onready` — never in `_process`
- Guard clauses over deep nesting
