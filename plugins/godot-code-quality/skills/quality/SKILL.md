---
name: quality
description: >-
  Run the full Godot quality gate and report a numeric score with per-check
  breakdown covering GDScript lint, format, GdUnit4 tests, and C# checks.
  Use when asked to "check quality", "run all checks", "run the gate", or
  "what is the quality score".
---

Run the full Godot quality gate and produce a scored report.

## Steps

1. **GDScript lint** — run `gdlint` on all `.gd` files:
   ```
   gdlint $(find . -name "*.gd" -not -path "./.godot/*")
   ```
   Report each file with errors. Pass if zero lint errors.

2. **GDScript format check** — verify formatting without modifying files:
   ```
   gdformat --check $(find . -name "*.gd" -not -path "./.godot/*")
   ```
   Pass if no files need reformatting.

3. **GdUnit4 tests** — run the test suite headlessly:
   ```
   godot --headless -s addons/gdUnit4/bin/GdUnitCmdTool.gd --add res://tests
   ```
   Parse the output for pass/fail counts. Pass if all tests pass.

4. **C# checks** (if `.csproj` present):
   - Format: `dotnet-csharpier --check .`
   - Build + Roslyn: `dotnet build --no-restore -warnaserror`
   Pass if both succeed.

5. **Score** — compute `(checks_passed / total_checks) * 100`.

## Output Format

```
Quality Gate Results
====================
[PASS] GDScript lint      — 0 errors across N files
[PASS] GDScript format    — N files checked, 0 need reformatting
[FAIL] GdUnit4 tests      — 3 failed, 42 passed
[PASS] C# build           — 0 warnings, 0 errors
[PASS] C# format          — N files checked

Score: 80/100

Failed checks:
  GdUnit4: TestPlayerMovement.test_jump_height — AssertionError: expected 3.5, got 3.2
```

## Notes

- Skip C# checks entirely if no `.csproj` file is found in the project root.
- If GdUnit4 addon is not installed, report `[SKIP] GdUnit4 — addon not found` and exclude from score.
- Always run all checks even if one fails — show the full picture.
- A score of 100 means all applicable checks passed.
