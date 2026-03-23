## Player — first-person character controller for Godot 4.x.
##
## Attach to a CharacterBody3D with:
##   - CollisionShape3D (CapsuleShape3D, height 1.8, radius 0.4)
##   - Head (Node3D, positioned at y=0.75)
##     - Camera3D
##   - HealthComponent
##   - StaminaComponent
##   - AudioStreamPlayer3D
##
## Plugins used: godot-patterns/scene-architecture, godot-patterns/state-machine,
##               gdscript-guide/typing-guide, gdscript-guide/idioms,
##               gdscript-guide/performance, godot-patterns/signal-design
class_name Player extends CharacterBody3D

# ---------------------------------------------------------------------------
# Signals  (signal-design skill: emitter owns declaration)
# ---------------------------------------------------------------------------

## Forwarded from HealthComponent for external listeners (HUD, GameManager).
signal health_changed(new_value: float)
signal died

# ---------------------------------------------------------------------------
# State machine  (state-machine skill: enum pattern)
# ---------------------------------------------------------------------------

enum State { IDLE, WALKING, SPRINTING, JUMPING, FALLING, DEAD }

var _state: State = State.IDLE

# ---------------------------------------------------------------------------
# Exports  (resource-patterns skill: designer-tunable via .tres)
# ---------------------------------------------------------------------------

@export var stats: PlayerStats

# ---------------------------------------------------------------------------
# Cached node references  (performance skill: @onready, never in _process)
# ---------------------------------------------------------------------------

@onready var _head: Node3D = $Head
@onready var _camera: Camera3D = $Head/Camera3D
@onready var _health: HealthComponent = $HealthComponent
@onready var _stamina: StaminaComponent = $StaminaComponent
@onready var _audio: AudioStreamPlayer3D = $AudioStreamPlayer3D

# ---------------------------------------------------------------------------
# Runtime state
# ---------------------------------------------------------------------------

var _gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")
var _wish_sprint: bool = false

# ---------------------------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------------------------

func _ready() -> void:
    assert(stats != null, "Player requires a PlayerStats resource assigned in the Inspector")
    Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

    _health.health_changed.connect(_on_health_changed)
    _health.died.connect(_on_died)
    _stamina.depleted.connect(_on_stamina_depleted)
    _stamina.recovered.connect(_on_stamina_recovered)


func _unhandled_input(event: InputEvent) -> void:
    # Guard: ignore input when dead
    if _state == State.DEAD: return

    # Mouse look  (idioms skill: guard clause, @onready already cached)
    if event is InputEventMouseMotion:
        var motion: InputEventMouseMotion = event as InputEventMouseMotion
        _rotate_camera(motion.relative)
        return

    # Capture toggle
    if event.is_action_pressed(&"ui_cancel"):
        var mode: Input.MouseMode = (
            Input.MOUSE_MODE_CAPTURED
            if Input.mouse_mode != Input.MOUSE_MODE_CAPTURED
            else Input.MOUSE_MODE_VISIBLE
        )
        Input.mouse_mode = mode


func _physics_process(delta: float) -> void:
    # Guard: no movement when dead
    if _state == State.DEAD: return

    _apply_gravity(delta)
    _handle_jump()
    _handle_move(delta)
    move_and_slide()
    _update_state()


# ---------------------------------------------------------------------------
# Private — movement
# ---------------------------------------------------------------------------

func _apply_gravity(delta: float) -> void:
    if not is_on_floor():
        velocity.y -= _gravity * stats.gravity_scale * delta


func _handle_jump() -> void:
    if Input.is_action_just_pressed(&"jump") and is_on_floor():
        velocity.y = stats.jump_velocity
        _transition(State.JUMPING)


func _handle_move(delta: float) -> void:
    var input_dir: Vector2 = Input.get_vector(
        &"move_left", &"move_right", &"move_forward", &"move_back"
    )
    var wish_dir: Vector3 = (
        transform.basis * Vector3(input_dir.x, 0.0, input_dir.y)
    ).normalized()

    _wish_sprint = Input.is_action_pressed(&"sprint") and input_dir != Vector2.ZERO

    var target_speed: float = _resolve_speed()
    var control: float = 1.0 if is_on_floor() else stats.air_control

    # Lerp horizontal velocity toward wish direction  (performance skill: no get_node calls)
    if wish_dir != Vector3.ZERO:
        velocity.x = lerpf(velocity.x, wish_dir.x * target_speed, control)
        velocity.z = lerpf(velocity.z, wish_dir.z * target_speed, control)
    else:
        velocity.x = lerpf(velocity.x, 0.0, control)
        velocity.z = lerpf(velocity.z, 0.0, control)

    # Drive stamina component
    if _wish_sprint and not _stamina.is_depleted and is_on_floor():
        _stamina.start_drain()
    else:
        _stamina.stop_drain()


func _resolve_speed() -> float:
    if _wish_sprint and not _stamina.is_depleted:
        return stats.sprint_speed
    return stats.move_speed


func _rotate_camera(mouse_delta: Vector2) -> void:
    # Horizontal: rotate the whole body
    rotate_y(-mouse_delta.x * stats.mouse_sensitivity)
    # Vertical: rotate only the head, clamped
    _head.rotate_x(-mouse_delta.y * stats.mouse_sensitivity)
    _head.rotation.x = clampf(
        _head.rotation.x,
        -deg_to_rad(stats.pitch_limit_deg),
        deg_to_rad(stats.pitch_limit_deg)
    )


# ---------------------------------------------------------------------------
# Private — state machine  (state-machine skill: explicit transitions)
# ---------------------------------------------------------------------------

func _update_state() -> void:
    # Infer state from physics each frame
    if _state == State.DEAD: return

    match true:
        _ when not is_on_floor() and velocity.y > 0.0:
            _transition(State.JUMPING)
        _ when not is_on_floor() and velocity.y <= 0.0:
            _transition(State.FALLING)
        _ when is_on_floor() and _wish_sprint and not _stamina.is_depleted:
            _transition(State.SPRINTING)
        _ when is_on_floor() and Vector2(velocity.x, velocity.z).length() > 0.1:
            _transition(State.WALKING)
        _:
            _transition(State.IDLE)


func _transition(new_state: State) -> void:
    if _state == new_state: return
    _state = new_state


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

## Apply damage to this player. Returns actual damage dealt.
func take_damage(amount: float) -> float:
    return _health.take_damage(amount)


## Returns current state as a readable StringName (for HUD or debug overlay).
func get_state_name() -> StringName:
    return StringName(State.keys()[_state])


# ---------------------------------------------------------------------------
# Signal handlers
# ---------------------------------------------------------------------------

func _on_health_changed(new_value: float) -> void:
    health_changed.emit(new_value)


func _on_died() -> void:
    _transition(State.DEAD)
    Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
    died.emit()


func _on_stamina_depleted() -> void:
    _stamina.stop_drain()


func _on_stamina_recovered() -> void:
    pass  # Sprint will automatically resume on next _handle_move if held
