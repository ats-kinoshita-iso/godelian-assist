<!-- Last updated: 2026-03-22 -->

# Hook Recipe: Godot Quality Gate

Run GDScript lint and format checks automatically before commits and at session end.

## Available

### Pre-commit quality gate

Runs `gdlint` and `gdformat --check` before every `git commit`. Blocks the commit if either fails.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash(git commit*)",
        "hooks": [
          {
            "type": "command",
            "command": "echo '=== Godot Quality Gate ===' && gdlint $(find . -name '*.gd' -not -path './.godot/*' 2>/dev/null) && gdformat --check $(find . -name '*.gd' -not -path './.godot/*' 2>/dev/null) && echo 'PASS: GDScript quality checks passed'"
          }
        ]
      }
    ]
  }
}
```

**Setup**: Add to `.claude/settings.json` in your Godot project root.

**Requires**: `pip install gdtoolkit`

---

### Session-end quality summary

Prints a brief quality summary each time Claude stops, without blocking.

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '\\n=== Session Quality Summary ===' && echo -n 'GDScript lint errors: ' && (gdlint $(find . -name '*.gd' -not -path './.godot/*' 2>/dev/null) 2>&1 | grep -c 'error' || echo '0') && echo 'Run /quality for a full scored report.' 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

---

### Auto-format GDScript on Write

Automatically runs `gdformat` after Claude writes or edits any `.gd` file.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path // .tool_response.filePath // empty' | { read -r f; echo \"$f\" | grep -q '\\.gd$' && gdformat \"$f\" && echo \"Formatted: $f\" || true; } 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

**Note**: `gdformat` modifies files in place. The hook is silent on non-GDScript files.
