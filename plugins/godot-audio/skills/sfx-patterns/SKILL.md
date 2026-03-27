---
name: sfx-patterns
description: Implement SFX playback — 3D positional audio, pitch randomization, one-shot pooling, and audio cue resources.
invocation: /sfx-patterns
---

Play sound effects correctly: positional 3D audio for world sounds, pooled one-shot players, and pitch variation for non-repetitive playback.

## AudioCue Resource

Define sound effects as `Resource` files for designer-friendly authoring:

```gdscript
class_name AudioCue
extends Resource

## Encapsulates an SFX definition with randomization settings.

@export var streams: Array[AudioStream] = []   # pick one randomly per play
@export var volume_db: float = 0.0
@export var pitch_min: float = 0.9
@export var pitch_max: float = 1.1
@export var bus: StringName = AudioBus.SFX
@export var max_distance: float = 20.0         # for 3D players

func pick_stream() -> AudioStream:
	if streams.is_empty():
		return null
	return streams[randi() % streams.size()]

func random_pitch() -> float:
	return randf_range(pitch_min, pitch_max)
```

Save as `.tres`: `res://assets/audio/cues/footstep_dirt.tres`

## SFX Manager Autoload

```gdscript
class_name SFXManager
extends Node

## Plays AudioCues via a pool of AudioStreamPlayer3D nodes.

const POOL_SIZE: int = 16

var _pool_3d: Array[AudioStreamPlayer3D] = []
var _pool_2d: Array[AudioStreamPlayer] = []
var _pool_index_3d: int = 0
var _pool_index_2d: int = 0

func _ready() -> void:
	for i: int in POOL_SIZE:
		var p3: AudioStreamPlayer3D = AudioStreamPlayer3D.new()
		add_child(p3)
		_pool_3d.append(p3)
		var p2: AudioStreamPlayer = AudioStreamPlayer.new()
		add_child(p2)
		_pool_2d.append(p2)

func play_3d(cue: AudioCue, position: Vector3) -> void:
	var stream: AudioStream = cue.pick_stream()
	if stream == null:
		return
	var p: AudioStreamPlayer3D = _pool_3d[_pool_index_3d % POOL_SIZE]
	_pool_index_3d += 1
	p.stream = stream
	p.volume_db = cue.volume_db
	p.pitch_scale = cue.random_pitch()
	p.bus = cue.bus
	p.max_distance = cue.max_distance
	p.global_position = position
	p.play()

func play_2d(cue: AudioCue) -> void:
	var stream: AudioStream = cue.pick_stream()
	if stream == null:
		return
	var p: AudioStreamPlayer = _pool_2d[_pool_index_2d % POOL_SIZE]
	_pool_index_2d += 1
	p.stream = stream
	p.volume_db = cue.volume_db
	p.pitch_scale = cue.random_pitch()
	p.bus = cue.bus
	p.play()
```

## Usage from Gameplay Code

```gdscript
@export var footstep_cue: AudioCue
@export var hit_cue: AudioCue

func _on_footstep_frame() -> void:
	SFXManager.play_3d(footstep_cue, global_position)

func take_damage(_amount: int) -> void:
	SFXManager.play_3d(hit_cue, global_position)
```

## Pitch Randomization Guide

Pitch variation eliminates the "machine gun" effect (same SFX repeated identically):

| Sound type | pitch_min | pitch_max |
|---|---|---|
| Footstep | 0.88 | 1.12 |
| Weapon swing | 0.92 | 1.08 |
| UI click | 0.97 | 1.03 |
| Explosion | 0.85 | 1.15 |
| Voice grunt | 0.90 | 1.10 |

## 3D Audio Attenuation

`AudioStreamPlayer3D` attenuates by distance. Key properties:

| Property | Description | Typical value |
|---|---|---|
| `max_distance` | Distance at which volume reaches `attenuation_filter_cutoff_hz` | 15–30 |
| `unit_size` | Distance at which volume = 100% | 1.0 |
| `attenuation_model` | INVERSE_DISTANCE (realistic) or LINEAR_DISTANCE (game-feel) | INVERSE_DISTANCE |
| `panning_strength` | How much L/R stereo panning | 1.0 |
