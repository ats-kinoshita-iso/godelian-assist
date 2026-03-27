---
name: feature-complete
description: >-
  Mark a feature done after designer approval: run the full quality gate,
  clean up spec files, and commit.
---

## What "feature complete" means

A feature is complete when all three conditions hold:

1. **Designer approval** — the designer has confirmed the feature feels right
   (from either direct approval or a playtest-debrief session with no remaining Critical/High items).
2. **Quality gate passes** — gdlint, gdformat, GdUnit4 tests, and type-check all pass.
3. **No regressions** — previously passing tests still pass.

Do not call `/feature-complete` while any Critical or High playtest items are open.

## The completion checklist Claude runs

```bash
# 1. Style
gdlint src/<feature-files>.gd

# 2. Formatting
gdformat --check src/<feature-files>.gd

# 3. Type correctness
godot --headless --check-only -s src/<feature-files>.gd

# 4. Unit tests (feature-specific)
godot --headless -s addons/gdUnit4/bin/GdUnitCmdTool.gd -- --testpath tests/<feature>/

# 5. Full test suite (regression)
godot --headless -s addons/gdUnit4/bin/GdUnitCmdTool.gd -- --testpath tests/

# 6. Screenshot review (if GDAI MCP active)
#    play_scene → get_running_scene_screenshot → confirm visuals match spec
```

If any step fails, Claude fixes it before declaring the feature complete.
The designer is not asked to approve again for quality-gate-only fixes — only for feel changes.

## What to clean up

1. **Remove** `plans/specs/ACTIVE_SPEC.md` (or clear its contents)
2. **Move** `plans/specs/<slug>.md` to `plans/specs/done/<slug>.md`
3. **Update** `plans/game-backlog.json`: set feature status to `done`
4. **Remove** any `plans/pending-approval/` or `plans/pending-changes/` files for this feature

## Commit

```bash
git add src/<feature-files> scenes/<feature-files> tests/<feature-files>
git commit -m "feat(<slug>): <feature title>

- Implements: <one-line description from spec>
- Designer approved: <date>
- Tests: all passing
- Quality: gdlint PASS, gdformat PASS, GdUnit4 PASS

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

Commit only the feature files. Do not commit plans/, specs/, or backlog files in the
same commit — keep implementation history clean.

## After completion

Print the updated backlog status (next queued feature).
If the backlog is empty, report to the designer: "All queued features are done — ready for
your next design session."
