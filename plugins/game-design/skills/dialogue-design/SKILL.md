---
name: dialogue-design
description: Design dialogue and narrative flow using Dialogic 2 conventions for Godot 4.x.
invocation: /dialogue-design
---
> **Godot version**: Godot 4.x (4.0+). All code examples use GDScript 2.0 and are not compatible with Godot 3.


Structure branching dialogue and in-game narrative using Dialogic 2, the standard Godot 4.x dialogue plugin.

## Dialogic 2 Overview

**Plugin**: Dialogic 2 — install via AssetLib or from https://github.com/dialogic-godot/dialogic
**File type**: `.dtl` (Dialogic timeline files in `res://dialogues/`)
**GDScript API**: `Dialogic.start("timeline_name")` — starts a timeline from GDScript

Enable in `project.godot`:
```ini
[editor_plugins]
enabled=PackedStringArray("res://addons/dialogic/plugin.cfg")
```

## Timeline File Structure (.dtl)

Dialogic uses a visual editor but timelines can also be authored as text:

```
character Aria: Hello, traveller. [pause=0.5] What brings you here?
- [I'm looking for the artifact.] => branch_artifact
- [Just passing through.] => branch_passing

label branch_artifact
character Aria: Hmm. [expression=suspicious] That is... dangerous knowledge.
=> end

label branch_passing
character Aria: Safe travels. [animation=wave]
=> end
```

## Character Definition

Create characters in `res://dialogues/characters/` via Dialogic editor:
- Display name
- Portrait variants (normal, happy, suspicious, hurt)
- Portrait position (left/right/center)
- Voice audio bus

## Integration Pattern

Trigger dialogue from GDScript on interaction:

```gdscript
class_name NPCInteraction
extends Area3D

@export var timeline_name: String = ""

func _on_body_entered(body: Node3D) -> void:
	if body.is_in_group("player") and Input.is_action_just_pressed("interact"):
		_start_dialogue()

func _start_dialogue() -> void:
	if timeline_name.is_empty():
		return
	var dialogue: Node = Dialogic.start(timeline_name)
	dialogue.timeline_ended.connect(_on_dialogue_ended)

func _on_dialogue_ended() -> void:
	# Resume gameplay, update quest state, etc.
	EventBus.scene_transition_finished.emit()
```

## Dialogue Design Checklist

For each NPC or dialogue moment, specify:

| Field | Description |
|---|---|
| Trigger | How does dialogue start? (proximity, interaction key, cutscene) |
| Characters | Who speaks? Which portraits? |
| Branching | Are there player choices? What are the outcomes? |
| State gates | Conditions (quest stage, item owned) that alter dialogue |
| Consequences | What changes after dialogue? (quest update, item given, door unlocked) |
| Repeat behaviour | Can dialogue be replayed? Different text on repeat? |

## Conditional Dialogue

Use Dialogic conditions to branch on game state:

```
if {GameManager.current_quest_stage} >= 2:
  character Aria: You've come far. The vault is ahead.
else:
  character Aria: I can't help you yet. Return when you're ready.
```

## Voice-Over Placeholder Convention

Mark lines requiring VO recording with `[VO_NEEDED]` tag during authoring:
```
character Aria: [VO_NEEDED] The artifact was stolen three moons ago.
```
Strip tags for release build.
