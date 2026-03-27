---
name: adaptive-music
description: Implement an adaptive music system with a state machine and crossfade transitions between music layers.
invocation: /adaptive-music
---

Build an adaptive music system that transitions between states (exploration, combat, boss, victory) with crossfaded stems.

## State Machine Architecture

The music system is a state machine. Each state maps to a set of active stems. Transitions crossfade between states.

```gdscript
class_name AdaptiveMusicSystem
extends Node

## Adaptive music state machine with crossfaded stem transitions.
## Place as an autoload or child of GameManager.

enum MusicState { SILENT, EXPLORATION, COMBAT, BOSS, VICTORY, DEFEAT }

@export var fade_duration: float = 1.5
@export var stems: Dictionary = {}   # MusicState -> AudioStream

var _current_state: MusicState = MusicState.SILENT
var _players: Array[AudioStreamPlayer] = []
var _active_player_index: int = 0

func _ready() -> void:
	_players.resize(2)
	for i: int in 2:
		var p: AudioStreamPlayer = AudioStreamPlayer.new()
		p.bus = AudioBus.MUSIC
		add_child(p)
		_players[i] = p
	EventBus.player_died.connect(_on_player_died)

func transition_to(new_state: MusicState) -> void:
	if new_state == _current_state:
		return
	_current_state = new_state
	_crossfade_to(stems.get(new_state, null))

func _crossfade_to(new_stream: AudioStream) -> void:
	if new_stream == null:
		_fade_out_all()
		return
	var next_index: int = (_active_player_index + 1) % 2
	var outgoing: AudioStreamPlayer = _players[_active_player_index]
	var incoming: AudioStreamPlayer = _players[next_index]
	incoming.stream = new_stream
	incoming.volume_db = linear_to_db(0.0)
	incoming.play()
	_active_player_index = next_index
	var tween: Tween = create_tween().set_parallel()
	tween.tween_property(incoming, "volume_db", linear_to_db(1.0), fade_duration)
	tween.tween_property(outgoing, "volume_db", linear_to_db(0.0), fade_duration)
	await tween.finished
	outgoing.stop()

func _fade_out_all() -> void:
	for p: AudioStreamPlayer in _players:
		var tween: Tween = create_tween()
		tween.tween_property(p, "volume_db", linear_to_db(0.0), fade_duration)
		await tween.finished
		p.stop()

func _on_player_died() -> void:
	transition_to(MusicState.DEFEAT)
```

## State Trigger Wiring

Wire state transitions to EventBus signals:

```gdscript
# In AdaptiveMusicSystem._ready():
EventBus.player_died.connect(func() -> void: transition_to(MusicState.DEFEAT))

# In EnemyStateMachine — when player detected:
func _on_player_detected() -> void:
	EventBus.combat_started.emit()

# Somewhere that receives combat_started:
EventBus.combat_started.connect(
	func() -> void: music_system.transition_to(AdaptiveMusicSystem.MusicState.COMBAT)
)
```

## Stem Strategy

Two common approaches:

**Horizontal re-sequencing** — swap between different tracks per state (simplest):
```
EXPLORATION → calm_exploration.ogg
COMBAT      → intense_combat.ogg
BOSS        → boss_theme.ogg
```

**Vertical layering** — all stems play simultaneously, mute/unmute per state (more complex but smoother):
```
Base stem always playing (low-level drums + bass)
Melody stem: unmute in EXPLORATION
Tension stem: unmute in COMBAT
All stems: full volume in BOSS
```

For vertical layering, use one `AudioStreamPlayer` per stem all playing the same-length looping track, and control volume per stem rather than switching streams.

## Transition Timing

- **Exploration → Combat**: 0.5–1.0s crossfade (fast for urgency)
- **Combat → Exploration**: 3.0–5.0s crossfade (slow, tension release)
- **Any → Victory/Defeat**: 0.3s (near-instant, dramatic)
- **Level load → Exploration**: 2.0s fade-in (gentle start)
