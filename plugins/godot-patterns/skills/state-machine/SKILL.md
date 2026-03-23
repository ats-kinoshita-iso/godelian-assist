---
name: state-machine
description: >-
  Implement a state machine in Godot 4.x: enum-based states, the Node-per-state
  pattern, state transitions, and connecting state changes to AnimationPlayer.
  Use when asked to "implement a state machine", "design the AI states for X",
  "how do I manage player states?", or "refactor this if/elif chain into states".
---

Implement a state machine for a Godot 4.x entity.

## When to Use a State Machine

Use when an entity has mutually exclusive modes of behavior that each run their own
`_process` / `_physics_process` logic. Typical cases: player movement, enemy AI, door/trap mechanics.

## Pattern 1 — Enum State Machine (Simple)

Best for 3–5 states with minimal per-state logic.

```gdscript
class_name PlayerController extends CharacterBody3D

enum State { IDLE, WALKING, JUMPING, ATTACKING, DEAD }

var _state: State = State.IDLE

@onready var _anim: AnimationPlayer = $AnimationPlayer

func _physics_process(delta: float) -> void:
    match _state:
        State.IDLE:      _tick_idle(delta)
        State.WALKING:   _tick_walking(delta)
        State.JUMPING:   _tick_jumping(delta)
        State.ATTACKING: _tick_attacking(delta)
        State.DEAD:      pass  # no tick in dead state

func _transition(new_state: State) -> void:
    if _state == new_state: return
    _exit_state(_state)
    _state = new_state
    _enter_state(_state)

func _enter_state(state: State) -> void:
    match state:
        State.IDLE:      _anim.play("idle")
        State.WALKING:   _anim.play("walk")
        State.JUMPING:   _anim.play("jump")
        State.ATTACKING: _anim.play("attack"); _start_attack_timer()
        State.DEAD:      _anim.play("die")

func _exit_state(state: State) -> void:
    match state:
        State.ATTACKING: _cancel_attack()
        _: pass
```

## Pattern 2 — Node-per-State (Scalable)

Best for 6+ states or when each state has complex logic. Each state is a child Node.

```
CharacterBody3D (Enemy)
└── StateMachine (Node)
    ├── IdleState (EnemyState)
    ├── PatrolState (EnemyState)
    ├── ChaseState (EnemyState)
    └── AttackState (EnemyState)
```

```gdscript
# enemy_state.gd — base class
class_name EnemyState extends Node

signal transition_requested(new_state: StringName)

func enter(_prev_state: StringName) -> void: pass
func exit() -> void: pass
func tick(delta: float) -> void: pass
func physics_tick(delta: float) -> void: pass


# state_machine.gd
class_name StateMachine extends Node

@export var initial_state: StringName = &"Idle"
var _current: EnemyState
var _states: Dictionary[StringName, EnemyState] = {}

func _ready() -> void:
    for child: Node in get_children():
        if child is EnemyState:
            _states[StringName(child.name)] = child
            child.transition_requested.connect(_on_transition_requested)
    _transition(initial_state)

func _process(delta: float) -> void:
    if _current: _current.tick(delta)

func _physics_process(delta: float) -> void:
    if _current: _current.physics_tick(delta)

func _transition(new_state: StringName) -> void:
    if _current: _current.exit()
    _current = _states.get(new_state)
    if _current: _current.enter(initial_state)

func _on_transition_requested(new_state: StringName) -> void:
    _transition(new_state)
```

## Connecting to AnimationPlayer

From within each state's `enter()`:

```gdscript
# patrol_state.gd
class_name PatrolState extends EnemyState

@onready var _anim: AnimationPlayer = $"../../AnimationPlayer"

func enter(_prev: StringName) -> void:
    _anim.play("walk")

func physics_tick(delta: float) -> void:
    # move along patrol path...
    if _sees_player():
        transition_requested.emit(&"Chase")
```

## Steps

1. Identify all states the entity can be in — draw a transition diagram.
2. Choose Pattern 1 (enum) for ≤5 simple states, Pattern 2 (Node-per-state) for more complex needs.
3. Implement `_enter_state` / `enter()` to trigger animation and start state-specific timers.
4. Implement `_exit_state` / `exit()` to clean up timers, reset flags.
5. Wire transition conditions inside each state's tick — keep transitions explicit.
6. Connect to `AnimationPlayer` from within state enter/exit, not from game logic.
