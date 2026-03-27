---
name: theme-system
description: Create and apply a Godot 4.x Theme resource to unify UI fonts, colors, and control styles project-wide.
invocation: /theme-system
---

Define a single `Theme` resource that all UI controls inherit, eliminating per-node style overrides.

## Theme Resource Setup

Create `res://assets/ui/game_theme.tres` in the Godot editor:

1. Create a new `Theme` resource
2. Set it as the theme on the root `Control` node of each UI scene
3. All child controls inherit it automatically

In `project.godot`, set the custom theme globally:
```ini
[gui]
theme/custom="res://assets/ui/game_theme.tres"
```

This applies the theme to every Control node in the entire project.

## Theme Structure

A Theme stores overrides per control type. Key entries to define:

| Control type | Properties to set |
|---|---|
| Label | font, font_size, font_color |
| Button | normal/hover/pressed/focus StyleBoxFlat, font, font_color |
| ProgressBar | background_color, fill_color, StyleBoxFlat |
| LineEdit | font, caret_color, StyleBoxFlat |
| PanelContainer | panel StyleBoxFlat |

## StyleBoxFlat Quick Reference

`StyleBoxFlat` is the main style primitive:

```gdscript
# Create a rounded button style programmatically (also doable in editor):
var style: StyleBoxFlat = StyleBoxFlat.new()
style.bg_color = Color("1a1a2e")
style.border_color = Color("e94560")
style.border_width_left = 2
style.border_width_right = 2
style.border_width_top = 2
style.border_width_bottom = 2
style.corner_radius_top_left = 6
style.corner_radius_top_right = 6
style.corner_radius_bottom_left = 6
style.corner_radius_bottom_right = 6
```

## Font Setup

Load a custom font from a `.ttf` file:

```gdscript
var font: FontFile = load("res://assets/fonts/press_start_2p.ttf")
theme.set_font("font", "Label", font)
theme.set_font_size("font_size", "Label", 14)
```

Define a font size hierarchy:
- **Body**: 14px — labels, menu items
- **Heading**: 22px — section titles
- **HUD**: 18px — health numbers, counters
- **Small**: 11px — tooltips, fine print

## Applying Theme Overrides Per Scene

For one-off overrides (don't break the global theme):

```gdscript
# In code — override just this label's color:
my_label.add_theme_color_override("font_color", Color.RED)

# Remove the override to revert to theme:
my_label.remove_theme_color_override("font_color")
```

Never use `add_theme_*_override` for baseline styles — put those in the Theme resource.

## Color Palette Convention

Define palette colors as constants in a dedicated class:

```gdscript
class_name UIColors

const BACKGROUND: Color = Color("0f0e17")
const SURFACE:    Color = Color("1a1a2e")
const PRIMARY:    Color = Color("e94560")
const SECONDARY:  Color = Color("16213e")
const TEXT:       Color = Color("fffffe")
const TEXT_DIM:   Color = Color("a7a9be")
const SUCCESS:    Color = Color("2dc653")
const DANGER:     Color = Color("e94560")
```
