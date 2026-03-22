---
name: balance-design
description: >-
  Design or tune balance parameters for a 3D action-RPG system: combat numbers,
  enemy difficulty, progression curves, and economy. Produces concrete numeric
  targets and a Godot Resource schema to expose them. Use when asked to "balance
  the combat", "tune the numbers", "how fast should the player level?", or
  "design the stat system".
---

Design or tune balance parameters for a 3D action-RPG system.

## Balance Domains

### Combat Math
Core formula: time-to-kill (TTK) is the primary lever.

```
TTK = enemy_health / (player_dps × hit_rate)
player_dps = weapon_damage × attack_speed × crit_multiplier
```

Target TTKs by encounter type:
| Encounter | Target TTK | Reason |
|-----------|-----------|--------|
| Trash enemy | 2–4 seconds | Quick, satisfying, keeps pace |
| Elite enemy | 15–30 seconds | Enough time to use abilities |
| Boss | 60–180 seconds | Multi-phase, memorable |

### Progression Curve
Use an exponential curve for XP/stats — feels earned, prevents trivial early content.

```gdscript
# XP required for level N
func xp_for_level(n: int) -> float:
    return base_xp * pow(growth_factor, n - 1)  # e.g., base=100, growth=1.4
```

Typical RPG parameters:
- `base_xp = 100`, `growth_factor = 1.4` → level 10 requires ~2,900 XP
- Stat gains: +5% HP, +3% damage per level (compound, not additive)

### Economy
- Drop rate for common items: 40–60% per encounter
- Rare item drop rate: 2–8% (feels lucky when it drops)
- Gold-per-hour target: enough to buy one upgrade every 15 minutes of play
- Avoid "gold sinks that feel mandatory" — upgrades should feel like choices

### Difficulty Scaling
Simple enemy stat scaling by zone:
```gdscript
class_name EnemyStats extends Resource
@export var base_health: float = 50.0
@export var base_damage: float = 10.0
@export var level_scale: float = 1.25  # multiply per zone level
```

## Steps

1. **Identify the system to balance** (combat, economy, progression, difficulty).
2. **State current numbers** (if tuning existing) or **propose initial numbers** (if designing new).
3. **Apply target TTK or curve** formula from the relevant domain above.
4. **Produce a `Resource` schema** with `@export` fields so designers can tune in Inspector:
   ```gdscript
   class_name CombatBalance extends Resource
   @export var player_base_damage: float = 15.0
   @export var player_attack_speed: float = 1.5  # attacks/sec
   @export var crit_chance: float = 0.1
   @export var crit_multiplier: float = 2.0
   ```
5. **Flag balance traps** — rubber-banding, death spirals, power cliffs, trivialized content.
6. **Propose one test scenario** to validate the numbers: "Spawn 10 trash enemies at level 5 — player should clear in under 90 seconds."
