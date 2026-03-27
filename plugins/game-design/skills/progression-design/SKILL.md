---
name: progression-design
description: Design player progression — XP curves using Curve resources, stat scaling, and unlock gates.
invocation: /progression-design
---
> **Godot version**: Godot 4.x (4.0+). All code examples use GDScript 2.0 and are not compatible with Godot 3.


Define the progression arc: XP per level, stat growth, skill unlocks, and how they feel in play.

## XP Curve with Curve Resource

Godot's `Curve` resource is the right tool for XP-to-level progression — it lets the designer tune the feel visually in the editor.

```gdscript
class_name ProgressionData
extends Resource

## XP required to reach each level, driven by a Curve resource.

@export var max_level: int = 30
@export var xp_curve: Curve  # X = normalized level (0–1), Y = XP required (0–1)
@export var xp_scale: float = 10000.0  # Multiplier: curve Y * xp_scale = actual XP

func xp_for_level(level: int) -> int:
	if level <= 1:
		return 0
	var t: float = float(level - 1) / float(max_level - 1)
	return int(xp_curve.sample(t) * xp_scale)

func level_for_xp(total_xp: int) -> int:
	for lvl: int in range(max_level, 0, -1):
		if total_xp >= xp_for_level(lvl):
			return lvl
	return 1
```

**Authoring**: Create the `Curve` in the Godot editor. Use an ease-in-ease-out curve — early levels fast, mid-game moderate, late-game steep. Export as `res://assets/data/progression.tres`.

## Stat Growth Schema

```gdscript
class_name StatGrowth
extends Resource

## Per-level stat multiplier, also driven by Curve resources.

@export var health_curve: Curve    # Base health at each level
@export var damage_curve: Curve    # Base damage at each level
@export var defense_curve: Curve
@export var health_base: int = 100
@export var damage_base: int = 10
@export var defense_base: int = 5
@export var health_scale: float = 500.0
@export var damage_scale: float = 50.0
@export var defense_scale: float = 30.0

func health_at_level(level: int) -> int:
	var t: float = float(level - 1) / float(30 - 1)
	return health_base + int(health_curve.sample(t) * health_scale)
```

## Unlock Gate Design

Track unlocks in a signal-driven unlock system:

```gdscript
class_name UnlockSystem
extends Node

signal ability_unlocked(ability_id: String, level: int)

const UNLOCK_TABLE: Dictionary = {
	5:  "double_jump",
	10: "dash",
	15: "parry",
	20: "charged_attack",
	25: "ultimate_ability",
}

func check_unlocks(new_level: int) -> void:
	if UNLOCK_TABLE.has(new_level):
		ability_unlocked.emit(UNLOCK_TABLE[new_level], new_level)
```

## Progression Design Worksheet

Work through this with the designer before authoring any Curve resources:

| Question | Guidance |
|---|---|
| How many levels? | 10–30 is typical for action games |
| Time per level (early) | 5–10 minutes feels rewarding |
| Time per level (late) | 30–60 minutes for endgame dedication |
| Curve shape | Ease-in (fast start) vs linear vs exponential |
| Stat growth feel | Doubling every 10 levels = power fantasy; 20% per 10 = grounded |
| Unlock pacing | Spread abilities evenly or cluster at milestone levels? |
| Soft cap | Does the curve flatten at max level for diminishing returns? |

## Common Pitfalls

- **Linear XP curves feel like a grind** after level 5 — use a curve that accelerates slowly
- **Stats that double every level** make early content trivial by mid-game — use `sqrt` or `log` scaling
- **Too many unlocks at once** overwhelm new players — space them 3–5 levels apart
- **No Curve resource means hardcoded tables** — always use Curve for designer-adjustable values
