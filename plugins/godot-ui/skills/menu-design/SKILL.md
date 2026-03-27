---
name: menu-design
description: Implement pause, main, and settings menus with correct tree pause handling and keyboard/gamepad focus.
invocation: /menu-design
---

Build menus that correctly pause the game, handle focus navigation, and layer over the HUD without disrupting gameplay state.

## Pause Menu Pattern

```gdscript
class_name PauseMenu
extends CanvasLayer

## Pause menu. Pauses the scene tree on open; resumes on close.
## CanvasLayer.layer = 2  (above HUD at layer 1)

@onready var resume_button: Button = %ResumeButton
@onready var settings_button: Button = %SettingsButton
@onready var quit_button: Button = %QuitButton

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS  # runs even when tree is paused
	hide()
	resume_button.pressed.connect(close_menu)
	quit_button.pressed.connect(_on_quit_pressed)
	EventBus.game_paused.connect(open_menu)
	EventBus.game_resumed.connect(close_menu)

func open_menu() -> void:
	get_tree().paused = true
	show()
	resume_button.grab_focus()  # keyboard/gamepad entry point

func close_menu() -> void:
	get_tree().paused = false
	hide()

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_just_pressed("ui_cancel"):
		close_menu()

func _on_quit_pressed() -> void:
	get_tree().paused = false
	GameManager.change_scene("res://scenes/ui/main_menu.tscn")
```

## get_tree().paused Rules

- Setting `paused = true` stops `_process` and `_physics_process` on all nodes with default `PROCESS_MODE_INHERIT`
- Nodes that must run while paused (menus, HUD animations) need `process_mode = PROCESS_MODE_ALWAYS`
- Set this in `_ready()`, not in the scene file — keeps it explicit and searchable

## FocusMode and Keyboard Navigation

Every interactive menu element must be focusable for gamepad/keyboard play:

```gdscript
# In _ready() of any menu:
resume_button.focus_mode = Control.FOCUS_ALL
settings_button.focus_mode = Control.FOCUS_ALL
quit_button.focus_mode = Control.FOCUS_ALL

# Set focus neighbours for directional navigation:
resume_button.focus_neighbor_bottom = settings_button.get_path()
settings_button.focus_neighbor_top = resume_button.get_path()
settings_button.focus_neighbor_bottom = quit_button.get_path()
quit_button.focus_neighbor_top = settings_button.get_path()
```

## Menu Layer Stack

| CanvasLayer layer | Content |
|---|---|
| 1 | HUD (health, stamina, hotbar) |
| 2 | Pause menu |
| 3 | Settings overlay |
| 5 | Dialogue box |
| 10 | Debug overlay |

Higher layer number = renders on top.

## Main Menu (Non-Pausing)

The main menu is a full scene — no CanvasLayer needed:

```gdscript
class_name MainMenu
extends Control

func _ready() -> void:
	$PlayButton.pressed.connect(_on_play_pressed)
	$PlayButton.grab_focus()

func _on_play_pressed() -> void:
	GameManager.change_scene("res://scenes/levels/level_01.tscn")
```

## Settings Menu Pattern

Settings menus use `OptionButton` and `HSlider` nodes. Always save settings to `ConfigFile` at `user://settings.cfg`, not to `SaveManager` (settings persist independently of save files).
