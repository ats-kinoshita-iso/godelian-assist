# API Reference: AudioStreamPlayer / AudioStreamPlayer2D / AudioStreamPlayer3D

**Godot 4.x** | `extends Node → Object` (AudioStreamPlayer) / `extends Node2D` / `extends Node3D`

---

## Three Variants

| Class | Use for |
|---|---|
| `AudioStreamPlayer` | Non-positional audio: music, UI sounds, narration |
| `AudioStreamPlayer2D` | 2D positional audio (panned by screen position) |
| `AudioStreamPlayer3D` | 3D positional audio with distance attenuation (world SFX) |

---

## Key Properties (all variants)

| Property | Type | Default | Description |
|---|---|---|---|
| `stream` | `AudioStream` | `null` | The audio resource to play. Assign an `.ogg`, `.wav`, or `.mp3` resource. |
| `volume_db` | `float` | `0.0` | Playback volume in decibels. 0 = full, -6 ≈ half power, -inf = silent. |
| `pitch_scale` | `float` | `1.0` | Playback speed / pitch multiplier. 2.0 = one octave up. |
| `playing` | `bool` | `false` | Read-only. True while audio is playing. |
| `autoplay` | `bool` | `false` | Play automatically when node enters the scene tree. |
| `stream_paused` | `bool` | `false` | Pauses without losing position. Resume by setting to `false`. |
| `bus` | `StringName` | `&"Master"` | Target audio bus. Use `AudioBus` constants class. |
| `mix_target` | `MixTarget` | `MIX_TARGET_STEREO` | (AudioStreamPlayer only) Output channel routing. |

## 3D-Only Properties (AudioStreamPlayer3D)

| Property | Type | Default | Description |
|---|---|---|---|
| `max_distance` | `float` | `0.0` | Distance at which volume reaches `attenuation_filter_cutoff_hz`. 0 = infinite. |
| `unit_size` | `float` | `10.0` | Reference distance for volume calculations. |
| `attenuation_model` | `AttenuationModel` | `ATTENUATION_INVERSE_DISTANCE` | How volume decreases with distance. |
| `panning_strength` | `float` | `1.0` | Stereo panning intensity from position. |

---

## Key Methods

### `play(from_position: float = 0.0) -> void`

Starts playback from `from_position` seconds. If already playing, restarts.

```gdscript
$MusicPlayer.play()
$SfxPlayer.play(0.5)   # start halfway through
```

### `stop() -> void`

Stops playback and resets position to 0.

### `seek(to_position: float) -> void`

Jumps to `to_position` seconds without stopping.

### `get_playback_position() -> float`

Returns current position in seconds.

---

## Signals

### `finished()`

Emitted when a non-looping stream reaches the end. Not emitted for looping streams.

---

## Typed GDScript Usage Example

```gdscript
class_name MusicController
extends Node

@onready var player: AudioStreamPlayer = $AudioStreamPlayer

@export var music_tracks: Array[AudioStream] = []
var _track_index: int = 0

func _ready() -> void:
	player.bus = AudioBus.MUSIC
	player.finished.connect(_on_track_finished)
	_play_current_track()

func _play_current_track() -> void:
	if music_tracks.is_empty():
		return
	player.stream = music_tracks[_track_index]
	player.play()

func _on_track_finished() -> void:
	_track_index = (_track_index + 1) % music_tracks.size()
	_play_current_track()

func set_volume(linear: float) -> void:
	player.volume_db = linear_to_db(clampf(linear, 0.0, 1.0))
```

---

## Common Pitfalls

- **Playing a null stream** — `play()` on a player with `stream = null` does nothing and prints an error; always check `stream != null`
- **Godot 3 `AudioStreamPlayer.play(offset)`** — renamed to `play(from_position)` in Godot 4
- **Volume 0 vs mute** — setting `volume_db = -80` approximates silence but is not the same as `bus` mute; use `AudioServer.set_bus_mute()` for actual muting
- **`finished` not emitted for looping streams** — if `AudioStream` has `loop = true`, `finished` never fires
- **`AudioStreamPlayer2D/3D` do not follow their node** — 3D position is read from `global_position` automatically each frame; no manual update needed
- **Import format matters** — Ogg Vorbis (`.ogg`) for music (smaller), WAV for SFX (no decode delay), MP3 also supported
