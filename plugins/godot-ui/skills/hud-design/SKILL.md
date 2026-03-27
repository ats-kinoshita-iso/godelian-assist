---
name: hud-design
description: Design and implement a Godot 4.x HUD using CanvasLayer with typed signal-driven updates.
invocation: /hud-design
---

Build a HUD that overlays the 3D viewport, updates through EventBus signals, and never holds direct references to gameplay nodes.

## CanvasLayer Architecture

The HUD must live on a `CanvasLayer` node so it renders above the 3D world and stays fixed during camera movement. Never place HUD elements as children of 3D nodes.

```
CanvasLayer (layer = 1)   ← attach HUD.gd here
└── MarginContainer
    ├── TopBar (HBoxContainer)
    │   ├── HealthBar (TextureProgressBar)
    │   ├── StaminaBar (TextureProgressBar)
    │   └── GoldLabel (Label)
    └── BottomBar (HBoxContainer)
        ├── Hotbar (HBoxContainer — item slots)
        └── MinimapContainer
```

## HUD Controller Script

```gdscript
class_name HUD
extends CanvasLayer

## Signal-driven HUD. Connects to EventBus; never holds gameplay node references.

@onready var health_bar: TextureProgressBar = %HealthBar
@onready var stamina_bar: TextureProgressBar = %StaminaBar
@onready var gold_label: Label = %GoldLabel

func _ready() -> void:
	EventBus.health_changed.connect(_on_health_changed)
	EventBus.hud_update_requested.connect(_on_hud_update_requested)

func _on_health_changed(actor: Node, new_health: int, max_health: int) -> void:
	if not actor.is_in_group("player"):
		return
	health_bar.max_value = float(max_health)
	health_bar.value = float(new_health)

func _on_hud_update_requested() -> void:
	pass  # trigger full refresh from SaveManager / GameManager state
```

## TextureProgressBar Setup

`TextureProgressBar` uses three textures: under (background), progress (fill), over (frame border).

Key properties:
- `min_value`: 0.0
- `max_value`: player's max health (set from signal)
- `value`: current health
- `fill_mode`: 0 = left-to-right (standard for health bars)
- `nine_patch_stretch`: true when using resizable textures

## Damage Flash Effect

```gdscript
@onready var damage_flash: ColorRect = %DamageFlash

func show_damage_flash() -> void:
	damage_flash.visible = true
	var tween: Tween = create_tween()
	tween.tween_property(damage_flash, "modulate:a", 0.0, 0.3)
	tween.tween_callback(func() -> void: damage_flash.visible = false)
```

## HUD Design Rules

- **No direct gameplay references** — HUD reads from signals only
- **CanvasLayer.layer = 1** for gameplay HUD; reserve higher layers for menus (layer 2) and debug (layer 10)
- **All text in Label nodes** — never draw text via `_draw()`; use theme fonts instead
- **Use `%` unique names** for HUD element references — avoids fragile path strings
- **Animate changes, don't snap** — lerp health bar value over 0.15s for juice; snap only for stamina
