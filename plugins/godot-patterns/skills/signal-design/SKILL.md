---
name: signal-design
description: >-
  Design the signal architecture for a Godot 4.x scene or system: identify
  what signals to emit, where to connect them, and whether to use direct
  connections or an event bus. Use when asked "how should signals work for X",
  "design the event system for Y", or "review my signal connections".
---

Design or review the signal architecture for a Godot 4.x system.

## Steps

1. **Map data flow** — identify events that need to cross scene boundaries:
   - Player takes damage → HUD updates
   - Enemy dies → Score increments, loot spawns
   - Door opens → Sound plays, animation triggers

2. **Choose connection strategy** for each signal:

   **Direct connection** (parent connects child's signal):
   ```gdscript
   # In Player.gd _ready():
   $HealthComponent.health_changed.connect(_on_health_changed)
   $HealthComponent.died.connect(_on_player_died)
   ```
   Use when: parent owns both sides; connection is 1-to-1.

   **Autoload EventBus** (decoupled publish/subscribe):
   ```gdscript
   # Emitting (in EnemyAI.gd):
   EventBus.enemy_died.emit(self)

   # Connecting (in ScoreManager.gd _ready()):
   EventBus.enemy_died.connect(_on_enemy_died)
   ```
   Use when: emitter and receiver are unrelated scenes; many-to-many.

   **Group broadcast**:
   ```gdscript
   get_tree().call_group("enemies", "alert", player.global_position)
   ```
   Use when: broadcasting a command to many nodes of the same type.

3. **Name signals** — use past-tense verbs for events (`health_changed`, `died`, `item_collected`), not imperatives (`change_health`, `kill`).

4. **Define signal parameters** — include only what listeners need:
   ```gdscript
   signal damage_taken(amount: float, source: Node)
   signal inventory_changed(item: ItemResource, delta: int)
   ```

5. **Avoid signal spaghetti** — flag if:
   - A signal chain is more than 3 hops deep
   - A node connects to signals from nodes it doesn't own (use EventBus instead)
   - Signals are used as function calls with return-value-style logic

6. **Produce a signal map** — table format:
   | Signal | Emitter | Receiver(s) | Parameters | Connection type |
   |--------|---------|-------------|------------|-----------------|

## Output

Signal map table + any anti-patterns flagged + recommended EventBus signals to add (if any).
