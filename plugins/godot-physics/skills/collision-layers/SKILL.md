---
name: collision-layers
description: Set up Godot 4.x collision layers and masks using a typed constants class.
invocation: /collision-layers
---

Define all project collision layers in one constants class, then configure each node's `collision_layer` and `collision_mask` from code — never guess bit values again.

## The Problem with Raw Bit Values

`collision_layer = 4` and `collision_mask = 6` are unreadable. One wrong bit causes silent, hard-to-debug physics failures. Always use named constants.

## CollisionLayer Constants Class

Create `src/utils/collision_layers.gd`:

```gdscript
class_name CollisionLayer

## Bit constants for every physics layer in the project.
## Layer N = bit (1 << (N-1)).
## Keep in sync with Project Settings → Layer Names → 3D Physics.

const WORLD:        int = 1        # layer 1 — static terrain and geometry
const PLAYER:       int = 2        # layer 2 — player character body
const ENEMY:        int = 4        # layer 3 — enemy character bodies
const PROJECTILE:   int = 8        # layer 4 — bullets, arrows, thrown objects
const TRIGGER:      int = 16       # layer 5 — Area3D triggers (checkpoints, pickups)
const HITBOX:       int = 32       # layer 6 — melee hitbox volumes
const HURTBOX:      int = 64       # layer 7 — hurtbox volumes (receive damage)
const INTERACTABLE: int = 128      # layer 8 — objects player can interact with
const RAGDOLL:      int = 256      # layer 9 — ragdoll physics bodies (post-death)
const CAMERA:       int = 512      # layer 10 — camera obstacle detection

## Preset masks — combine with bitwise OR
const PLAYER_MASK: int    = WORLD | ENEMY | TRIGGER | HURTBOX | INTERACTABLE
const ENEMY_MASK: int     = WORLD | PLAYER | HITBOX
const PROJECTILE_MASK: int = WORLD | ENEMY | HURTBOX
const HITBOX_MASK: int    = HURTBOX
const HURTBOX_MASK: int   = HITBOX
```

## Project Settings Layer Names

In **Project Settings → Layer Names → 3D Physics**, name each layer to match:
```
Layer 1:  World
Layer 2:  Player
Layer 3:  Enemy
Layer 4:  Projectile
Layer 5:  Trigger
Layer 6:  Hitbox
Layer 7:  Hurtbox
Layer 8:  Interactable
Layer 9:  Ragdoll
Layer 10: Camera
```

## Applying in Code

```gdscript
# In _ready() of each node type:

# Player CharacterBody3D
collision_layer = CollisionLayer.PLAYER
collision_mask  = CollisionLayer.PLAYER_MASK

# Enemy CharacterBody3D
collision_layer = CollisionLayer.ENEMY
collision_mask  = CollisionLayer.ENEMY_MASK

# HitboxComponent (Area3D)
collision_layer = CollisionLayer.HITBOX
collision_mask  = CollisionLayer.HURTBOX

# Pickup trigger (Area3D)
collision_layer = CollisionLayer.TRIGGER
collision_mask  = CollisionLayer.PLAYER
```

## Applying in .tscn

You can also set layers in the scene file. Each layer bit maps to a 1 in the integer:
```
# 4 layers set: WORLD(1) + ENEMY(4) + TRIGGER(16) + HURTBOX(64) = 85
collision_mask = 85
```
Using the code approach (in `_ready`) is preferred — it stays in sync with the constants class automatically.

## Layer Design Rules

1. **One responsibility per layer** — don't reuse a layer for two different physics roles
2. **Hitbox and Hurtbox are always separate layers** — hitbox only detects hurtbox and vice versa
3. **Projectiles never share a layer with characters** — prevents self-collision on spawn
4. **Triggers (Area3D) use a dedicated layer** — never combine trigger and body detection
