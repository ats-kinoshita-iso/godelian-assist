## StaminaComponent — reusable stamina/sprint resource manager.
##
## Drains while sprinting, regenerates after a cooldown.
## Player reads is_depleted to gate sprint input.
##
## Plugins used: godot-patterns/node-composition, gdscript-guide/idioms
class_name StaminaComponent extends Node

## Emitted each frame while stamina changes.
signal stamina_changed(new_value: float)
## Emitted once when stamina hits zero.
signal depleted
## Emitted once when stamina recovers above sprint_min_stamina after depletion.
signal recovered

@export var max_stamina: float = 100.0
@export var drain_rate: float = 20.0      ## units/second while active
@export var regen_rate: float = 10.0      ## units/second while inactive
@export var regen_delay: float = 1.5      ## seconds before regen after stopping drain
@export var sprint_min_stamina: float = 10.0

var current_stamina: float
var is_depleted: bool = false

var _draining: bool = false
var _regen_cooldown: float = 0.0


func _ready() -> void:
    current_stamina = max_stamina


func _process(delta: float) -> void:
    if _draining:
        _tick_drain(delta)
    else:
        _tick_regen(delta)


## Call every frame while the sprint input is held and movement speed > 0.
func start_drain() -> void:
    _draining = true
    _regen_cooldown = regen_delay


## Call when sprint input is released or player stops moving.
func stop_drain() -> void:
    _draining = false


## Returns stamina as a 0.0–1.0 fraction.
func get_fraction() -> float:
    if max_stamina <= 0.0: return 0.0
    return current_stamina / max_stamina


func _tick_drain(delta: float) -> void:
    if current_stamina <= 0.0:
        if not is_depleted:
            is_depleted = true
            depleted.emit()
        _draining = false
        return

    var prev: float = current_stamina
    current_stamina = maxf(0.0, current_stamina - drain_rate * delta)
    if not is_equal_approx(current_stamina, prev):
        stamina_changed.emit(current_stamina)


func _tick_regen(delta: float) -> void:
    if _regen_cooldown > 0.0:
        _regen_cooldown -= delta
        return
    if current_stamina >= max_stamina:
        return

    var prev: float = current_stamina
    current_stamina = minf(max_stamina, current_stamina + regen_rate * delta)
    if not is_equal_approx(current_stamina, prev):
        stamina_changed.emit(current_stamina)

    if is_depleted and current_stamina >= sprint_min_stamina:
        is_depleted = false
        recovered.emit()
