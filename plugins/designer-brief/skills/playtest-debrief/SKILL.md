---
name: playtest-debrief
description: >-
  Structure playtest observations into a ranked list of issues that Claude can
  map to specific files and convert into an ordered task list.
---

## The debrief format

After a playtest session, use this template to capture observations:

```markdown
## Playtest: <date or description, e.g. "2026-03-27 — first run of dash feature">

### What worked (keep these)
- Dash distance feels right at 4 meters
- Dust particle timing is satisfying
- Cooldown indicator is readable

### What felt wrong (ranked Critical / High / Medium / Low)
- [Critical] Double-jump cancels the dash mid-air — unintended
- [High] Dash cooldown is 0.5s but feels more like 0.8s — laggy UI update?
- [Medium] Dust particle is too small at 1080p — hard to see
- [Low] Dash sound is slightly too loud compared to jump

### Bugs observed (exact reproduction steps)
- Jump → Dash → Jump again: second jump fires even during dash
  Repro: hold space, tap shift mid-air, tap space again — consistent

### Open questions (design decisions not yet made)
- Should dashing into a wall deal damage to the player?
- Should enemies be able to dodge dash?
```

All four sections are optional — fill what applies to the session.

## How Claude processes a debrief

1. **Reads each item** and categorizes it: feel / bug / performance / visual
2. **Maps each item** to the most likely file and function responsible
3. **Respects your ranking** — Critical items are addressed first, then High, Medium, Low.
   Claude does not reorder your priorities.
4. **Produces an ordered task list** in the format used by `iterate`:
   - Each item: what felt wrong, the responsible file/function, proposed diff
5. **Presents all diffs before applying any** — designer approves or skips each one

## Designer's responsibility in ranking

The designer must rank issues before Claude prioritizes — Claude does not reorder.
Use this guide:

| Rank | Meaning |
|---|---|
| Critical | Breaks the game — unplayable or corrupts save |
| High | Significantly hurts feel or progression — must fix before next playtest |
| Medium | Noticeable but manageable — fix in this sprint |
| Low | Polish — fix when Critical/High are clear |

## Bugs vs. feel issues

**Bugs** have exact reproduction steps. Claude treats these as correctness fixes:
reads the code, finds the logic error, proposes the fix, applies after approval.

**Feel issues** require judgment. Claude proposes a specific value change or behavior
change and explains the reasoning. The designer approves or adjusts the proposed direction.

## Converting a debrief to backlog items

After processing, unresolved open questions from the debrief automatically become
new `queued` items in `plans/game-backlog.json` via the `add-feature` skill.
Items that required architectural changes (not just tuning) become new briefs.
