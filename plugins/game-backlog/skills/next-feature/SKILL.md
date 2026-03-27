---
name: next-feature
description: >-
  Advance the highest-priority queued feature to pending_approval: generate its
  implementation spec and present it for designer review.
---

## What it does

1. Reads `plans/game-backlog.json` and finds the highest-priority feature with `status: queued`.
2. Sets its status to `pending_approval`.
3. Generates a full implementation spec using the `designer-brief/brief` skill format:
   - Node structure
   - Signal map
   - Custom Resource subclasses
   - Files to create and modify
   - GDScript skeletons (typed)
   - Test plan
4. Writes the spec to `plans/specs/<feature-slug>.md`.
5. Copies/links to `plans/specs/ACTIVE_SPEC.md` (satisfies the designer-approval gate).
6. Presents the spec to the designer with: "Review this spec and reply 'approved' to proceed,
   or mark sections with [REVISE: ...] to request changes."

Implementation does not begin until the designer explicitly approves.

## Feature slug convention

The slug is the feature title lowercased, spaces replaced with hyphens, punctuation removed:
- "Player double-jump" → `player-double-jump`
- "Enemy patrol AI" → `enemy-patrol-ai`
- "Save/load system" → `saveload-system`

## When there are no queued features

Claude reports: "No queued features found. Use `/add-feature` to add new features,
or `/backlog-status` to review the current state."

## One-at-a-time discipline

If a feature is already `in_progress` when `/next-feature` is called, Claude will:
- Show the current `in_progress` feature
- Ask: "There is already an in-progress feature. Do you want to pause it and start
  the next one, or complete the current one first?"

Do not advance to the next feature while one is actively being implemented.
Spec generation (`pending_approval`) is acceptable to queue ahead.
