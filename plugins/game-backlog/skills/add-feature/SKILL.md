---
name: add-feature
description: >-
  Add a new feature to the game backlog mid-session with a title, one-sentence
  brief, and priority placement.
---

## When to use

- During a playtest debrief when a new design decision emerges
- When the designer thinks of a feature not in the original GDD
- When a feature is split into smaller pieces during spec review
- When a previously out-of-scope feature is re-scoped in

Do NOT use to track bugs — bugs found during playtesting are handled by
`/playtest-debrief` and then by `/iterate`.

## Input format

Provide at minimum a title and brief. Priority is optional — Claude will ask if omitted.

```
Title: Weapon swap
Brief: Player can carry two weapons and switch between them with Q key.
Priority: 3
```

Or as a natural sentence:
```
Add "weapon swap" — player switches between two weapons with Q. Make it priority 3.
```

## What Claude does

1. Reads `plans/game-backlog.json` to find the current highest ID.
2. Assigns the new feature `id = current_max_id + 1`, status `queued`.
3. Inserts the feature at the requested priority position, shifting lower-priority
   features down by 1.
4. If the requested priority conflicts with an `in_progress` or `pending_approval`
   feature, Claude will ask: "Priority 2 is currently in-progress. Do you want to
   insert above it (making this the next feature after current) or below it?"
5. Writes the updated `plans/game-backlog.json`.
6. Prints the updated `/backlog-status` table so you can confirm placement.

## Priority rules

- Priority 1 = implement next after the current `in_progress` feature completes.
- If no priority is given, Claude places the feature at the bottom of the queue
  (lowest priority among `queued` features) and asks if that's correct.
- Priorities are relative — Claude does not enforce gaps or rebalance the whole list.
  If you have features at 1, 2, 5 and add one at priority 3, it goes between 2 and 5.
