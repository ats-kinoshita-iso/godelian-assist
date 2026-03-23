## HealthComponent — reusable health/damage component.
##
## Drop onto any CharacterBody3D or StaticBody3D to give it health.
## Connect signals to HUD, GameManager, or respawn logic.
##
## Plugins used: godot-patterns/node-composition, gdscript-guide/typing-guide
class_name HealthComponent extends Node

## Emitted whenever current health changes (damage or heal).
signal health_changed(new_value: float)
## Emitted once when health reaches zero.
signal died

@export var max_health: float = 100.0
@export var invincibility_time: float = 0.2

var current_health: float
var is_dead: bool = false

## Tracks remaining invincibility frames in seconds.
var _invincible_timer: float = 0.0


func _ready() -> void:
    current_health = max_health


func _process(delta: float) -> void:
    if _invincible_timer > 0.0:
        _invincible_timer -= delta


## Apply damage. Ignores hits during invincibility window.
## Returns actual damage dealt (0 if blocked by i-frames).
func take_damage(amount: float) -> float:
    if is_dead: return 0.0
    if _invincible_timer > 0.0: return 0.0

    var actual: float = minf(amount, current_health)
    current_health -= actual
    _invincible_timer = invincibility_time
    health_changed.emit(current_health)

    if current_health <= 0.0:
        _die()

    return actual


## Restore health up to max. Safe to call on dead entities (does nothing).
func heal(amount: float) -> void:
    if is_dead: return
    current_health = minf(current_health + amount, max_health)
    health_changed.emit(current_health)


## Instantly kill regardless of invincibility or current health.
func kill() -> void:
    if is_dead: return
    current_health = 0.0
    health_changed.emit(0.0)
    _die()


## Returns health as a 0.0–1.0 fraction (for progress bars).
func get_fraction() -> float:
    if max_health <= 0.0: return 0.0
    return current_health / max_health


func _die() -> void:
    is_dead = true
    died.emit()
