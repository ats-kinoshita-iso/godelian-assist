---
name: systems-design
description: >-
  Design a game system for a 3D action-RPG: specify data model, state machine,
  interactions with other systems, and produce a Godot 4.x implementation
  skeleton. Use when asked to "design the X system", "how should Y work?", or
  "spec out the combat/inventory/dialogue system".
---

Design a game system for a 3D action-RPG and produce a Godot 4.x implementation plan.

## Steps

1. **Define the system** — one sentence: what does it do, who owns it, and when does it run?

2. **Identify data** — what information does the system need to store and read?
   - Static data (defined at design time): use `Resource` subclasses (`.tres`)
   - Dynamic state (changes at runtime): use node variables or an Autoload manager
   Example for a Combat System:
   ```
   Static:  WeaponResource { damage, range, attack_speed, animations[] }
   Dynamic: float current_stamina, bool is_attacking, Node target
   ```

3. **State machine** — draw the state transitions if the system has modes:
   ```
   IDLE -> ATTACKING (attack_pressed and has_stamina)
   ATTACKING -> RECOVERING (animation_finished)
   RECOVERING -> IDLE (recovery_time elapsed)
   IDLE -> DODGING (dodge_pressed)
   DODGING -> IDLE (dodge_animation_finished)
   ```

4. **System interfaces** — what signals does it emit and what does it consume from other systems?
   | Signal/Input | Direction | Purpose |
   |---|---|---|
   | `damage_dealt(target, amount)` | Emit | Notify health/stats systems |
   | `stamina_changed(value)` | Emit | Update HUD |
   | `enemy_died(enemy)` | Listen | Interrupt attacks |

5. **Godot implementation sketch** — node structure and key code patterns:
   ```gdscript
   class_name CombatComponent extends Node

   signal damage_dealt(target: Node, amount: float)
   signal attack_started
   signal attack_finished

   @export var weapon: WeaponResource
   @export var stamina_cost: float = 20.0

   var _state: StringName = &"idle"
   @onready var _animation_player: AnimationPlayer = $"../AnimationPlayer"

   func try_attack(target: Node) -> bool:
       if _state != &"idle": return false
       if not _has_stamina(): return false
       _enter_attacking(target)
       return true
   ```

6. **Edge cases and constraints** — enumerate at least 3 failure modes and how the system handles them:
   - What if the target is destroyed mid-attack?
   - What if two systems try to trigger the same state simultaneously?
   - What happens on scene reload/level transition?

7. **Next step** — identify the first Godot scene/script to create to begin implementation.
