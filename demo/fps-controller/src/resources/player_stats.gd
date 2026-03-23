## PlayerStats — designer-tunable data resource for the FPS player.
##
## Usage: File > New Resource > PlayerStats in Godot editor.
## Assign the .tres file to Player's @export var stats field.
##
## Plugin used: godot-patterns/resource-patterns
class_name PlayerStats extends Resource

## Movement
@export_group("Movement")
@export var move_speed: float = 5.0
@export var sprint_speed: float = 9.0
@export var jump_velocity: float = 4.5
@export var air_control: float = 0.3        ## 0 = no control, 1 = full ground control
@export var gravity_scale: float = 1.0      ## multiplier on ProjectSettings gravity

## Mouse look
@export_group("Mouse Look")
@export_range(0.001, 0.01, 0.001) var mouse_sensitivity: float = 0.003
@export var pitch_limit_deg: float = 89.0   ## max up/down look angle

## Health
@export_group("Health")
@export var max_health: float = 100.0
@export var invincibility_time: float = 0.2 ## seconds of i-frames after hit

## Stamina
@export_group("Stamina")
@export var max_stamina: float = 100.0
@export var stamina_drain_rate: float = 20.0  ## per second while sprinting
@export var stamina_regen_rate: float = 10.0  ## per second while not sprinting
@export var stamina_regen_delay: float = 1.5  ## seconds before regen starts after depletion
@export var sprint_min_stamina: float = 10.0  ## minimum stamina to start sprinting
