---
name: audio-architecture
description: Design the Godot 4.x audio bus structure — master, music, SFX, voice, and ambient buses with send routing.
invocation: /audio-architecture
---

Set up the audio bus structure in Godot's Audio panel before writing a single line of audio code.

## Standard Bus Structure

Configure in **Project → Audio** (or the Audio panel at the bottom of the editor):

```
Master (bus 0)
├── Music     (bus 1) → Master
├── SFX       (bus 2) → Master
│   ├── Combat    (bus 3) → SFX
│   └── Footstep  (bus 4) → SFX
├── Voice     (bus 5) → Master
└── Ambient   (bus 6) → Master
```

Each child bus has `send = "ParentBusName"`. Master has no send (outputs to hardware).

## Bus Constants Class

```gdscript
class_name AudioBus

## Named constants for all audio buses.
## Must match the names in Project → Audio exactly (case-sensitive).

const MASTER:   StringName = &"Master"
const MUSIC:    StringName = &"Music"
const SFX:      StringName = &"SFX"
const COMBAT:   StringName = &"Combat"
const FOOTSTEP: StringName = &"Footstep"
const VOICE:    StringName = &"Voice"
const AMBIENT:  StringName = &"Ambient"
```

## AudioStreamPlayer Bus Assignment

Always set the `bus` property to the correct named bus:

```gdscript
# 2D/3D players in scene:
$MusicPlayer.bus = AudioBus.MUSIC
$FootstepPlayer.bus = AudioBus.FOOTSTEP
$WeaponSfx.bus = AudioBus.COMBAT
$DialoguePlayer.bus = AudioBus.VOICE
$WindAmbient.bus = AudioBus.AMBIENT
```

## Volume Control

Volume is in decibels (dB). Convert from 0–1 linear to dB:

```gdscript
func set_music_volume(linear: float) -> void:
	var db: float = linear_to_db(clampf(linear, 0.0, 1.0))
	AudioServer.set_bus_volume_db(AudioServer.get_bus_index(AudioBus.MUSIC), db)

func set_sfx_volume(linear: float) -> void:
	var db: float = linear_to_db(clampf(linear, 0.0, 1.0))
	AudioServer.set_bus_volume_db(AudioServer.get_bus_index(AudioBus.SFX), db)
```

Save volume settings to `user://settings.cfg` (not save files).

## Bus Effects

Add effects to buses in the Audio panel:

| Bus | Recommended effects |
|---|---|
| Music | Reverb (room = 0.3), Limiter |
| Combat SFX | Distortion (very light, drive = 0.05), Compressor |
| Footstep | EQ (high-pass at 80 Hz) |
| Voice | Compressor, EQ (presence boost at 3 kHz) |
| Ambient | Reverb (room = 0.7, wet = 0.4) |

## Mute/Unmute

```gdscript
func mute_bus(bus_name: StringName, muted: bool) -> void:
	AudioServer.set_bus_mute(AudioServer.get_bus_index(bus_name), muted)
```

Use mute (not volume = 0) for reversible silencing — volume 0 loses the original value.
