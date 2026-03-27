# Agent Prompt: Iterate on Designer Feedback

**Purpose**: Process playtest feedback and apply minimal targeted changes to an existing feature.
**Prerequisite**: A playtest debrief has been captured (via `/playtest-debrief`). Changes must be designer-approved before implementation.
**Rule**: Every change requires an `[APPROVED]` marker. Every skip requires a `[SKIP]` marker. No unmarked items are acted on.

---

## Input Format

The designer provides feedback as a list of observations. Each item is categorized and then marked before implementation begins.

### Feedback Categories

| Category | Description | Action |
|---|---|---|
| **Feel** | Movement, timing, weight, responsiveness | Tune exported variables first; code change only if tuning is insufficient |
| **Bug** | Incorrect behaviour, crash, missing feature | Fix immediately; no designer markup needed for true bugs |
| **Performance** | Framerate, hitching, loading | Profile before fixing; do not optimize prematurely |
| **Visual** | Wrong appearance, missing effect, UI issue | Scene or theme change; may require screenshot confirmation |

---

## Step 1 — CATEGORIZE FEEDBACK

Read the playtest debrief and produce a categorized list:

```
FEEL:
  [ ] Jump feels floaty — peak height too high
  [ ] Enemy hits feel weightless — no hitstop or screenshake

BUG:
  [ ] Pickup item sometimes not collected on first touch
  [ ] Health bar doesn't update when receiving >50 damage

PERFORMANCE:
  [ ] FPS drops when >10 enemies are on screen

VISUAL:
  [ ] Health bar fill color is wrong (blue instead of red)
  [ ] Attack animation clips through terrain
```

Present this list to the designer for prioritization. Do not begin any changes yet.

---

## Step 2 — DESIGNER MARKUP

The designer marks each item before any implementation:

```
FEEL:
  [APPROVED] Jump feels floaty — reduce jump_velocity by 0.8, increase fall_gravity_scale to 3.5
  [SKIP] Enemy hits feel weightless — out of scope for this iteration

BUG:
  [APPROVED] Pickup item sometimes not collected — ghost frame fix in DetectionZone
  [APPROVED] Health bar doesn't update — fix signal connection in HUD._ready()

PERFORMANCE:
  [SKIP] FPS drops — not blocking, track in backlog

VISUAL:
  [APPROVED] Health bar fill color — change fill_color in game_theme.tres
  [SKIP] Attack animation clips — needs animation rework, not this iteration
```

**Stop here until the designer has marked every item.** Do not implement anything with an unmarked status.

---

## Step 3 — APPLY THE MINIMAL CHANGE RULE

For each `[APPROVED]` item, apply the smallest possible change that addresses it:

- **Feel / tuning**: Change only the exported variable value. Do not refactor surrounding code.
- **Bug / logic**: Fix only the faulty branch. Do not clean up nearby code.
- **Visual**: Change only the property that is wrong. Do not redesign the layout.

**Explicitly do not**:
- Rename variables or functions that were not part of the bug
- Restructure functions to be "cleaner" while fixing them
- Add error handling or validation to code paths not involved in the issue
- Move files or reorganize directories
- Add features not mentioned in the approved feedback

If a fix requires more than a minimal change, flag it and ask the designer before proceeding.

---

## Step 4 — WRITE CHANGES

For each `[APPROVED]` item, read the affected file first, then apply only the approved change.

After each change, state:
```
Changed: src/player/player_movement.gd:42
  jump_velocity: 6.5 → 5.7
  fall_gravity_scale: 2.5 → 3.5
Reason: [APPROVED] Jump feels floaty
```

---

## Step 5 — RUN QUALITY GATE

```bash
gdlint src/
gdformat --check src/
godot --headless --import
godot --headless -s addons/gdUnit4/bin/GdUnitCmdTool.gd --add tests/
```

All must pass. If a test breaks due to a value change, update the test to match the new approved value (not the other way around — the test is wrong, not the change).

---

## Step 6 — SCREENSHOT CONFIRMATION (if GDAI MCP available)

For `[APPROVED]` Visual items:
```
1. get_editor_screenshot — confirm the property change is reflected in the editor
2. Play scene → get_running_scene_screenshot — confirm runtime appearance
3. Report the before/after comparison
```

---

## Step 7 — REPORT AND COMMIT

Produce a summary before committing:

```
APPLIED:
  ✓ jump_velocity 6.5 → 5.7, fall_gravity_scale 2.5 → 3.5
  ✓ DetectionZone ghost frame fix (body tracking Dictionary)
  ✓ HUD health_changed connection moved to _ready()
  ✓ Health bar fill_color: Color.BLUE → Color.RED

SKIPPED:
  ✗ Enemy hit feel — [SKIP] by designer
  ✗ FPS optimization — [SKIP] by designer
  ✗ Attack animation — [SKIP] by designer

Quality gate: lint ✓ format ✓ import ✓ tests ✓
```

Commit with:
```bash
git commit -m "fix: apply playtest feedback — jump feel, pickup ghost frame, HUD health signal

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

Do not bundle [SKIP] items into the commit message. Only committed changes appear.
