# godot-patterns

Architectural patterns and design guidance for Godot 4.x game development.

## Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| `scene-architecture` | "design the scene for X", "review my scene" | Node tree design with signals, exports, anti-pattern check |
| `node-composition` | "should I extend or compose?", "how to share behavior" | Inheritance vs. composition pattern selection |
| `signal-design` | "how should signals work?", "review my signal connections" | Signal architecture with connection strategy and map |

## Design Philosophy

- **Composition over inheritance** — prefer component child nodes over deep class hierarchies
- **Signals over direct references** — decouple scenes with signals and EventBus
- **Scenes as contracts** — each scene exposes a clear `@export` interface; internals are private
- **Resources for data** — separate designer-tunable data from logic using `Resource` subclasses
