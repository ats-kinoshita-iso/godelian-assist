---
name: game-loop
description: >-
  Design or review the core game loop for a 3D action-RPG: the moment-to-moment
  gameplay rhythm, feedback cycles, player motivation drivers, and how they map
  to Godot 4.x scene and system architecture. Use when asked to "design the
  core loop", "what's the game loop?", or "how does the player progress?".
---
> **Godot version**: Godot 4.x (4.0+). All code examples use GDScript 2.0 and are not compatible with Godot 3.


Design or review the core game loop for a 3D action-RPG.

## Framework: Three Loop Levels

### Micro loop (seconds — moment-to-moment)
The immediate combat/interaction feel.
- Input → response latency target: < 100ms for attacks, < 50ms for dodge
- Hit feedback: screen shake, sound, hitstop, particle burst
- Death/failure state: clear, immediate, unambiguous
- Key question: *Is every input satisfying?*

### Meso loop (minutes — per-encounter)
What the player does between micro interactions.
- Encounter structure: waves, rooms, boss phases
- Resource pressure: health, stamina, consumables depleted and restored when?
- Risk/reward moments: optional hard encounter for extra loot
- Key question: *Does each encounter feel different from the last?*

### Macro loop (hours — session-to-session)
What keeps the player returning.
- Progression axis: character stats, gear, abilities, world map
- Session goal: what can the player accomplish in 30 minutes?
- Unlock gating: what gates progression — time, skill, or content?
- Key question: *What did I gain this session that I didn't have before?*

## Steps

1. **State the current loop** (if reviewing) or **propose a loop** (if designing) at all three levels.

2. **Identify friction points** — where does player motivation stall?
   - Repetitive encounters with no variation (micro)
   - Unclear objectives or dead ends (meso)
   - Slow progression / no session payoff (macro)

3. **Map loops to Godot systems**:
   | Loop Level | Godot System |
   |------------|-------------|
   | Micro | CharacterBody3D, AnimationPlayer, hitbox Area3D |
   | Meso | LevelManager, EnemySpawner, LootSystem |
   | Macro | SaveSystem, StatProgression, WorldMap |

4. **Propose one concrete improvement** per loop level with implementation notes.

5. **Juiciness checklist** — assess feedback quality:
   - [ ] Attack lands: sound + particle + hitstop (even 2 frames)
   - [ ] Enemy death: ragdoll or death animation + loot spawn
   - [ ] Level up / stat gain: fanfare + visual indicator
   - [ ] Damage numbers: visible, color-coded (normal/crit/miss)
   - [ ] Stamina depletion: visual warning before hitting zero

## Output

Three-paragraph loop description (one per level) + friction points + improvement proposals + juiciness score (0-5 items checked).
