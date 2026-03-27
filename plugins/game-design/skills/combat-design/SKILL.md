---
name: combat-design
description: Design a combat system — attack data schemas, hitbox logic, and damage pipeline — ready for typed GDScript implementation.
invocation: /combat-design
---
> **Godot version**: Godot 4.x (4.0+). All code examples use GDScript 2.0 and are not compatible with Godot 3.


Define the data model and hitbox architecture for a 3D action combat system. Produces a spec that maps directly to typed GDScript resources and scene structures.

## AttackData Resource Schema

Every attack in the game is represented as a `Resource` so it can be authored in the Godot editor and referenced by scene files.

```gdscript
class_name AttackData
extends Resource

## Exported resource representing a single attack definition.

@export var attack_name: String = ""
@export var damage: int = 10
@export var knockback_force: float = 5.0
@export var hitstun_frames: int = 8
@export var hitbox_size: Vector3 = Vector3(1.0, 1.0, 1.0)
@export var hitbox_offset: Vector3 = Vector3.ZERO
@export var hit_sfx: AudioStream
@export var hit_vfx: PackedScene
@export var applies_status: bool = false
@export var status_effect: String = ""
@export var status_duration: float = 0.0
@export var attack_type: AttackType = AttackType.MELEE

enum AttackType { MELEE, RANGED, AOE, DOT }
```

Save attack definitions as `.tres` files: `res://assets/data/attacks/sword_slash.tres`

## Hitbox Scene Architecture

Each attack spawns or enables a hitbox node. Use `Area3D` with a `CollisionShape3D`:

```gdscript
class_name HitboxComponent
extends Area3D

## Typed hitbox that carries AttackData and emits hit signals.

@export var attack_data: AttackData

signal hit_landed(target: Node3D, data: AttackData)

func _ready() -> void:
	body_entered.connect(_on_body_entered)
	monitoring = false  # disabled until attack animation triggers it

func enable_hitbox() -> void:
	monitoring = true

func disable_hitbox() -> void:
	monitoring = false

func _on_body_entered(body: Node3D) -> void:
	if body.has_method("take_damage"):
		hit_landed.emit(body, attack_data)
		disable_hitbox()
```

## Damage Pipeline

```
AnimationPlayer (frame event)
  └── enable_hitbox()
      └── HitboxComponent.body_entered
          └── HurtboxComponent.receive_hit(AttackData)
              └── HealthComponent.apply_damage(int)
                  └── EventBus.health_changed.emit(actor, new_health, max_health)
```

No direct node references cross scene boundaries — everything flows through signals and EventBus.

## Design Variables to Specify

Work through these with the designer before implementation:

| Variable | Description | Typical Range |
|---|---|---|
| Base damage | Minimum attack damage | 5–30 |
| Hitstun frames | Frames target is stunned | 4–20 |
| Knockback force | Physics impulse on hit | 2–15 |
| Hitbox active frames | Animation frames where hitbox is live | 2–6 |
| Hit confirm window | Frames after hit before next attack | 8–24 |
| Invincibility frames | I-frames after being hit | 12–30 |

## Scene Structure for Melee Character

```
CharacterBody3D (Player/Enemy)
├── CollisionShape3D          (character body)
├── AnimationPlayer
├── HealthComponent (Node)
├── HurtboxComponent (Area3D) (receives incoming damage)
│   └── CollisionShape3D
└── AttackPivot (Node3D)      (positioned at hand/weapon)
    └── HitboxComponent (Area3D)
        └── CollisionShape3D
```
