---
name: projectile-system
description: Implement a pooled projectile system for bullets, arrows, and thrown objects in Godot 4.x.
invocation: /projectile-system
---

Build a reusable projectile system with object pooling to avoid per-shot instantiation overhead.

## Why Pool Projectiles

Instantiating and freeing `PackedScene` nodes every shot causes garbage collection spikes that manifest as frame hitches at high fire rates. A pool pre-instantiates N projectiles and recycles them — spawn cost drops to near zero.

## Projectile Node

```gdscript
class_name Projectile
extends Area3D

## Pooled projectile. Returned to pool on hit or lifetime expiry.

signal hit_target(target: Node3D, position: Vector3)
signal lifetime_expired()

@export var speed: float = 20.0
@export var lifetime: float = 3.0
@export var damage: int = 10

var _active: bool = false
var _direction: Vector3 = Vector3.FORWARD
var _elapsed: float = 0.0

func launch(origin: Vector3, direction: Vector3) -> void:
	global_position = origin
	_direction = direction.normalized()
	_elapsed = 0.0
	_active = true
	monitoring = true
	visible = true

func deactivate() -> void:
	_active = false
	monitoring = false
	visible = false

func _physics_process(delta: float) -> void:
	if not _active:
		return
	global_position += _direction * speed * delta
	_elapsed += delta
	if _elapsed >= lifetime:
		lifetime_expired.emit()
		deactivate()

func _on_body_entered(body: Node3D) -> void:
	if not _active:
		return
	hit_target.emit(body, global_position)
	deactivate()
```

## ProjectilePool Autoload (or Node)

```gdscript
class_name ProjectilePool
extends Node

## Object pool for a single projectile type. Pre-instantiates SIZE projectiles.

@export var projectile_scene: PackedScene
@export var pool_size: int = 30

var _pool: Array[Projectile] = []

func _ready() -> void:
	_pool.resize(pool_size)
	for i: int in pool_size:
		var p: Projectile = projectile_scene.instantiate() as Projectile
		p.deactivate()
		add_child(p)
		_pool[i] = p

func acquire() -> Projectile:
	for p: Projectile in _pool:
		if not p._active:
			return p
	# Pool exhausted — grow by one (emit warning)
	push_warning("ProjectilePool: pool exhausted, growing")
	var p: Projectile = projectile_scene.instantiate() as Projectile
	p.deactivate()
	add_child(p)
	_pool.append(p)
	return p

func fire(origin: Vector3, direction: Vector3) -> Projectile:
	var p: Projectile = acquire()
	p.launch(origin, direction)
	return p
```

## Usage at Fire Point

```gdscript
@onready var _pool: ProjectilePool = $ProjectilePool

func _fire() -> void:
	var p: Projectile = _pool.fire(
		$Muzzle.global_position,
		-$Muzzle.global_basis.z   # forward of muzzle node
	)
	p.hit_target.connect(_on_projectile_hit, CONNECT_ONE_SHOT)

func _on_projectile_hit(target: Node3D, _pos: Vector3) -> void:
	if target.has_method("take_damage"):
		target.take_damage(10)
```

## Pool Sizing Guide

| Fire rate | Lifetime | Recommended pool size |
|---|---|---|
| 2 shots/sec | 2 sec | 8 |
| 5 shots/sec | 3 sec | 20 |
| 10 shots/sec | 2 sec | 30 |
| 20 shots/sec | 1.5 sec | 40 |

Formula: `pool_size = ceil(fire_rate * lifetime * 1.5)` — the 1.5 factor gives headroom.

## Collision Setup

```gdscript
# In Projectile._ready()
collision_layer = CollisionLayer.PROJECTILE
collision_mask  = CollisionLayer.WORLD | CollisionLayer.HURTBOX
body_entered.connect(_on_body_entered)
```
