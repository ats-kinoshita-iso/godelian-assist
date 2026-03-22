---
name: node-composition
description: >-
  Recommend a node composition strategy for a Godot 4.x feature, comparing
  inheritance vs. composition approaches. Use when asked "should I extend X or
  compose it?", "how do I add Y to multiple enemies?", or "what's the Godot
  way to share behavior between scenes?"
---

Recommend the right Godot 4.x node composition strategy for a feature.

## Context Gathering

Ask or infer:
- What behavior needs to be shared? (e.g., health, inventory, patrol AI)
- How many different entity types need this behavior?
- Does the behavior require its own state (variables), signals, or `_process`?

## Patterns to Consider

### 1. Child Node (Composition — preferred)
Add a dedicated child node that encapsulates the behavior.
```gdscript
# HealthComponent.gd — child of any entity that has health
class_name HealthComponent extends Node

@export var max_health: float = 100.0
var current_health: float

signal died
signal health_changed(new_value: float)

func take_damage(amount: float) -> void:
    current_health = maxf(0.0, current_health - amount)
    health_changed.emit(current_health)
    if current_health == 0.0:
        died.emit()
```
**When to use**: reusable behaviors (health, inventory, hitbox, patrol, loot drop).

### 2. Inheritance
Extend a base class that provides shared logic.
```gdscript
# Enemy.gd
class_name Enemy extends CharacterBody3D
func take_damage(amount: float) -> void: ...
```
**When to use**: a strict type hierarchy where IS-A is true (all enemies share identical interface). Keep chains shallow (max 2 levels).

### 3. Autoload + Signal Bus
Register events globally; entities subscribe and publish.
```gdscript
# EventBus.gd (Autoload)
signal enemy_died(enemy: Enemy)
```
**When to use**: communication between completely unrelated scenes; avoids tight coupling.

### 4. Resource-based Data
Separate data from behavior using `Resource` subclasses.
```gdscript
class_name CharacterStats extends Resource
@export var speed: float = 5.0
@export var attack: float = 10.0
```
**When to use**: entity configuration that designers should tune; stats, item definitions.

## Decision Matrix

| Need | Pattern |
|------|---------|
| Shared behavior, multiple types | Child component node |
| Shared interface, type safety | Shallow inheritance |
| Cross-scene events | Autoload signal bus |
| Designer-tunable data | Resource |
| One-off logic | Keep in the scene script |

## Output

Recommend a pattern with a short rationale, then provide a minimal code skeleton for the recommended approach.
