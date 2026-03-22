---
name: quality-fix
description: >-
  Auto-fix all fixable Godot quality issues: reformat GDScript files, apply
  C# formatting, and report any remaining issues that require manual attention.
  Use when asked to "fix formatting", "auto-fix lint", "clean up code", or
  "fix quality issues".
---

Auto-fix all fixable quality issues in the Godot project.

## Steps

1. **Identify scope** — find all GDScript and C# files to process:
   ```
   find . -name "*.gd" -not -path "./.godot/*"
   find . -name "*.cs" -not -path "./.godot/*"
   ```

2. **Fix GDScript formatting** — reformat in place:
   ```
   gdformat $(find . -name "*.gd" -not -path "./.godot/*")
   ```
   Report which files were modified.

3. **Fix C# formatting** (if `.csproj` present):
   ```
   dotnet-csharpier .
   ```
   Report which files were modified.

4. **Re-run lint** to surface issues that cannot be auto-fixed:
   ```
   gdlint $(find . -name "*.gd" -not -path "./.godot/*")
   ```
   List every remaining lint error with file:line references.

5. **Summarize**:
   - Count of files reformatted (GDScript + C#)
   - Count of lint errors remaining after auto-fix
   - Explicit list of any errors that require manual changes

## Output Format

```
Auto-fix Results
================
GDScript format: 3 files reformatted
  - src/player/player.gd
  - src/enemies/goblin.gd
  - ui/hud.gd

C# format: 1 file reformatted
  - src/GameManager.cs

Remaining lint errors (manual fix required):
  src/player/player.gd:42 — max-line-length: line is 115 chars (max 100)
  src/enemies/goblin.gd:87 — function-name: "DoAttack" should be snake_case

Recommendation: 2 issues require manual attention before commit.
```

## Notes

- Only fix formatting — never change logic or variable names without explicit instruction.
- If `gdformat` is not installed, report installation command: `pip install gdtoolkit`.
- If `dotnet-csharpier` is not installed, skip and report: `dotnet tool install -g csharpier`.
- After auto-fix, always verify the project still parses: `godot --headless --check-only -s project.godot`.
