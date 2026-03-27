# scene-builder

Generate and audit Godot 4.x `.tscn` scene files directly from Claude Code.

## Skills

| Skill | Invocation | Description |
|---|---|---|
| create-scene | `/create-scene` | Generate a new `.tscn` from a node list |
| add-node | `/add-node` | Insert a node into an existing `.tscn` |
| wire-signals | `/wire-signals` | Append `[connection]` entries to a scene |
| scene-from-brief | `/scene-from-brief` | Build a scene from the active designer spec |
| scene-audit | `/scene-audit` | Validate format correctness and spec compliance |

## Reference

See `cookbook/api-ref/tscn-format.md` for the full `.tscn` format specification including UID charset, ID formats, load_steps formula, and parent path rules.
