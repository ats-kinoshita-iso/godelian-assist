---
name: enemy-design
description: Design enemy archetypes — behaviour state machines, NavigationAgent3D pathfinding, and data schemas for Godot 4.x.
invocation: /enemy-design
---
> **Godot version**: Godot 4.x (4.0+). All code examples use GDScript 2.0 and are not compatible with Godot 3.


Define enemy archetypes, their state machine behaviours, navigation setup, and data schemas ready for typed GDScript implementation.

## EnemyData Resource Schema

```gdscript
class_name EnemyData
extends Resource

@export var enemy_name: String = ""
@export var max_health: int = 50
@export var move_speed: float = 3.5
@export var detection_radius: float = 8.0
@export var attack_range: float = 1.5
@export var attack_cooldown: float = 1.2
@export var attack_data: AttackData
@export var patrol_points: Array[Vector3] = []
@export var loot_table: Array[ItemData] = []
@export var xp_reward: int = 10
@export var death_vfx: PackedScene
```

## State Machine Architecture

Every enemy runs a simple state machine with four core states. Expand per archetype.

```gdscript
class_name EnemyStateMachine
extends Node

enum State { IDLE, PATROL, CHASE, ATTACK, STUNNED, DEAD }

var current_state: State = State.IDLE
var target: Node3D = null

func _physics_process(delta: float) -> void:
	match current_state:
		State.IDLE:    _tick_idle(delta)
		State.PATROL:  _tick_patrol(delta)
		State.CHASE:   _tick_chase(delta)
		State.ATTACK:  _tick_attack(delta)
		State.STUNNED: _tick_stunned(delta)

func transition_to(new_state: State) -> void:
	current_state = new_state
```

## NavigationAgent3D Setup

Every enemy that moves uses `NavigationAgent3D` for pathfinding. Place as a child of the enemy root.

```gdscript
@onready var nav_agent: NavigationAgent3D = $NavigationAgent3D

func _ready() -> void:
	nav_agent.path_desired_distance = 0.5
	nav_agent.target_desired_distance = 0.5

func _tick_chase(delta: float) -> void:
	if target == null:
		transition_to(State.PATROL)
		return
	nav_agent.target_position = target.global_position
	var direction: Vector3 = nav_agent.get_next_path_position() - global_position
	direction = direction.normalized()
	velocity = direction * data.move_speed
	move_and_slide()
```

**NavigationRegion3D required in level scene** — bake a NavMesh for every level where enemies navigate.

## Enemy Scene Structure

```
CharacterBody3D (Enemy)
├── CollisionShape3D          (body collider)
├── NavigationAgent3D         (pathfinding)
├── AnimationPlayer
├── AnimationTree             (blend states for walk/attack/hurt/die)
├── EnemyStateMachine (Node)
├── HealthComponent (Node)
├── HurtboxComponent (Area3D)
│   └── CollisionShape3D
├── HitboxComponent (Area3D)  (enabled during attack animation)
│   └── CollisionShape3D
└── DetectionArea (Area3D)    (sphere for aggro range)
    └── CollisionShape3D (SphereShape3D, radius = detection_radius)
```

## Archetype Design Template

Define each enemy type before implementation:

| Field | Description |
|---|---|
| Role | Tank, Skirmisher, Ranged, Elite, Boss |
| States | Which states does this archetype use? |
| Detection | Sight radius, sound triggers, alert behaviour |
| Attack pattern | Single hit, combo, AoE, projectile |
| Stagger threshold | How many hits before entering STUNNED |
| Group behaviour | Solo, pack (alert neighbours), guard (fixed position) |
| Special ability | Optional unique mechanic |

## Common Patrol Pattern

```gdscript
var _patrol_index: int = 0

func _tick_patrol(delta: float) -> void:
	if data.patrol_points.is_empty():
		transition_to(State.IDLE)
		return
	var target_pos: Vector3 = data.patrol_points[_patrol_index]
	nav_agent.target_position = target_pos
	if nav_agent.is_navigation_finished():
		_patrol_index = (_patrol_index + 1) % data.patrol_points.size()
```
