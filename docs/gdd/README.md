# Aiki-FPS: Game Design Document (MVP)

**Version**: 0.2.0-alpha
**Last Updated**: 2026-03-29
**Engine**: Godot 4.x (4.6.1+)
**Language**: GDScript 2.0

---

## 1. Vision Statement

A first-person melee combat game where Aikido footwork IS the combat system.
Instead of a single dodge button, players choose from distinct movement patterns
that determine positioning, timing, and counterattack opportunities. Mastery
comes from reading enemy attacks and selecting the right footwork response.

**Elevator pitch**: Sekiro's deflect system meets Aikido's 6 footwork patterns
in first-person, with Sifu's arena-mode replayability.

### 1.1 Reference Games

| Reference | What We Take |
|-----------|-------------|
| **Sekiro** | Posture/Ki system, deflect timing, hit-stop weight |
| **ZZZ (Zenless Zone Zero)** | Evasive assist windows, route optimization endgame |
| **Sifu** | Arena mode replayability, enemy encounter design |
| **Bloodborne** | Aggressive play rewarded (rally mechanic inspiration) |
| **Ghostrunner / Cyberpunk 2077** | First-person melee camera feel |

### 1.2 Target Platform

- **MVP**: PC (keyboard + mouse)
- **Future**: Mobile (touch controls, ZZZ-style)

---

## 2. Core Mechanics

### 2.1 Footwork System (the heart of the game)

Aikido defines 6 primary footwork patterns. Each produces a mechanically
distinct movement. Every footwork has two variants:

- **Omote** (表) — ends in front of opponent (aggressive, riskier)
- **Ura** (裏) — ends behind opponent (safer, better follow-up angles)

#### MVP Footwork (Phase 1)

| Footwork | Movement | Combat Role | KB+M Input |
|----------|----------|-------------|------------|
| **Irimi** (入り身) | Direct forward entry | Close distance, pressure | W + Shift (step) |
| **Tenkan** (転換) | 180° pivot on front foot | Redirect force, flank | Shift + mouse flick direction |

**Omote/Ura selection**: Hold RMB during footwork = ura variant; tap without
RMB = omote variant.

#### Post-MVP Footwork (Phase 4+)

| Footwork | Movement | Combat Role |
|----------|----------|-------------|
| **Irimi-tenkan** (入り身転換) | Enter then pivot | Gap close + immediate reposition |
| **Tenshin** (転身) | 45° diagonal evasion | Dodge off-line, counter angle |
| **Kaiten** (回転) | Full body rotation | Sweeping attacks, break encirclement |
| **Tsugi-ashi** (継ぎ足) | Shuffle step | Micro-spacing, feints, neutral game |

### 2.2 Ki Flow System (posture analog)

Both player and enemies have a **Ki gauge** (0–100). Ki represents
balance, composure, and martial readiness.

#### Ki Economy

| Action | Player Ki | Enemy Ki |
|--------|-----------|----------|
| Successful footwork into Musubi | +15 | — |
| Correct Musubi deflect | +10 | -20 |
| Landing a strike after Musubi | +5 | -15 |
| Getting hit | -25 | — |
| Mistimed footwork | -10 | — |
| Enemy attack blocked by player | — | -5 |
| Enemy whiffs (player evades) | — | -10 |
| Idle / no combat | Regen +3/s | Regen +5/s |

**Ki Break**: When enemy Ki reaches 0, they enter a **stagger** state
(~2 seconds). An **auto-cinematic decisive technique** triggers — the camera
pulls to a cinematic angle as the player executes a finishing Aikido technique
(ikkyo, shihonage, kotegaeshi, etc.) similar to ZZZ's chain attacks or Sifu's
takedowns. This is the primary kill condition — like Sekiro's deathblow after
posture break, but presented as an automatic cinematic rather than a QTE.

**Player Ki at 0**: Player enters a stumble state (~1 second), vulnerable to
a heavy hit. Not instant death, but very dangerous.

**Player Death**: On death, a brief **death screen** displays (Sifu-style)
showing what killed the player and a prompt to retry. This gives the player
a moment to process what went wrong before the next attempt — supporting the
routing/optimization loop rather than brute-force retries.

### 2.3 Musubi System (the timing window)

**Musubi** (結び, "connection/blending") is the core parry/deflect mechanic.
When the player executes footwork with correct timing relative to an incoming
attack, they enter a Musubi state.

#### Musubi Windows

| Timing | Result | Ki Reward |
|--------|--------|-----------|
| **Perfect** (±3 frames / ~50ms) | Full deflect, enemy staggers briefly, free counter | +25 player, -30 enemy |
| **Good** (±6 frames / ~100ms) | Partial deflect, reduced damage, slight advantage | +10 player, -15 enemy |
| **Miss** | Footwork executes but no deflect, vulnerable during recovery | -10 player |

The Musubi window opens when the player's footwork movement intersects the
enemy's attack timing. Different footwork types have different Musubi
characteristics:

- **Irimi Musubi**: Must enter INTO the attack line. High risk, high reward.
  Perfect Musubi = player ends at point-blank range for immediate counter.
- **Tenkan Musubi**: Pivot AWAY from attack line. Lower risk, lower reward.
  Perfect Musubi = player ends at enemy's flank.

### 2.4 Weapon System (MVP: Katana only)

The katana maps to Aikido's natural hand positions. Strikes chain from
footwork:

| Footwork → Strike | Attack Type | Damage | Speed |
|-------------------|-------------|--------|-------|
| Irimi-omote → Shomenuchi | Overhead vertical cut | High | Medium |
| Irimi-ura → Tsuki | Forward thrust | Medium | Fast |
| Tenkan-omote → Yokomenuchi | Diagonal sweeping cut | Medium | Medium |
| Tenkan-ura → Kesa-giri | Reverse diagonal | Medium | Medium |
| Neutral → Light attack | Quick slash | Low | Fast |
| Neutral → Heavy attack | Charged cut | High | Slow |

**Input**: LMB = light attack, hold LMB = heavy attack. Footwork + LMB within
the chain window = footwork-specific strike.

### 2.5 Camera & First-Person Feel

The biggest challenge: making rotational footwork feel good in first-person
without causing nausea.

#### Camera Rules

1. **Procedural head sway** tied to footwork type:
   - Irimi: forward momentum bob (subtle head dip then rise)
   - Tenkan: smooth rotational pan (camera follows body rotation)
2. **FOV shifts**: +5° during fast movement, -3° on parry (focus effect)
3. **Motion blur**: weapon/hands only, NOT world geometry
4. **Horizon lock**: camera roll stays level during all footwork (critical
   for comfort)
5. **Hit-stop**: 40–80ms freeze on weapon impact (heavier hits = longer stop)
6. **Screen shake**: very subtle, directional (toward impact point)
7. **Tenkan camera solution**: during tenkan, the camera rotates smoothly
   over ~0.3s with a slight ease-in-ease-out curve. The player maintains
   mouse control during the rotation — their mouse input is ADDED to the
   procedural rotation, not overridden.

### 2.6 Enemy Design (MVP: One Type)

**Kendo Practitioner** — a disciplined swordsman with readable attack patterns.

#### Attack Patterns

| Attack | Tell | Window | Damage |
|--------|------|--------|--------|
| **Men-uchi** (head strike) | Raises shinai overhead, 0.5s windup | Irimi or tenkan Musubi | 30 |
| **Kote-uchi** (wrist strike) | Steps forward, drops tip, 0.3s windup | Tenkan Musubi preferred | 20 |
| **Do-uchi** (body strike) | Rotates hips, 0.4s windup | Irimi Musubi preferred | 25 |
| **Tsuki** (thrust) | Pulls back, 0.6s windup | Tenkan Musubi only | 35 |

Each attack has a clear visual and audio tell. The enemy cycles through
patterns with increasing complexity:

- **Phase 1** (Ki 100–60): Single attacks, long recovery
- **Phase 2** (Ki 60–30): 2-hit combos, shorter recovery
- **Phase 3** (Ki 30–0): 3-hit combos, feints, shorter tells

#### Enemy AI State Machine

```
IDLE → APPROACH → ATTACK_WINDUP → ATTACK_ACTIVE → RECOVERY → IDLE
                                                 ↓
                                            STAGGERED (Ki break)
                                                 ↓
                                            VULNERABLE (deathblow window)
```

---

## 3. Game Modes (MVP)

### 3.1 Dojo Mode (Tutorial)

A traditional wooden dojo environment. The sensei (NPC voice) guides the player
through:

1. **Movement basics** — WASD, mouse look, camera orientation
2. **Irimi drill** — practice forward entry against a wooden dummy
3. **Tenkan drill** — practice pivot against a wooden dummy
4. **Omote vs Ura** — explanation and practice of both variants
5. **Musubi timing** — the dummy attacks, player practices deflect timing
6. **Ki system** — explanation of Ki gauge, practice breaking dummy's Ki
7. **Putting it together** — free practice against a sparring partner
   (the Kendo Practitioner at reduced difficulty)

Each drill has a completion condition and the player can repeat any drill
at will. The dojo is always accessible from the main menu.

### 3.2 Arena Mode (Core Gameplay)

A single arena (dojo courtyard) where the player faces the Kendo Practitioner.
Scoring based on:

- **Time to Ki-break**
- **Musubi accuracy** (perfect/good/miss ratio)
- **Damage taken**
- **Footwork variety** (using both irimi and tenkan)

Leaderboard is local (MVP). This is the Sifu-style replayability loop:
optimize your route, improve your timing, get a better score.

---

## 4. HUD & UI

### 4.1 In-Game HUD

```
┌─────────────────────────────────────────────┐
│  [Player Ki ████████░░]    [Enemy Ki ████░░] │
│                                              │
│                                              │
│               (gameplay view)                │
│                                              │
│                                              │
│  [HP ██████░░]          ◆ MUSUBI INDICATOR   │
└─────────────────────────────────────────────┘
```

- **Ki gauges**: top of screen, opponent-style (like Sekiro)
- **HP**: bottom-left, minimal
- **Musubi indicator**: center-bottom diamond that flashes on successful
  Musubi timing. Color-coded: gold = perfect, white = good, red = miss

### 4.2 Menus

- **Main Menu**: Start (→ Arena), Dojo (→ Tutorial), Settings, Quit
- **Pause Menu**: Resume, Restart, Dojo, Settings, Quit to Menu
- **Results Screen**: Score breakdown after arena completion

---

## 5. Audio Design

### 5.1 MVP Audio

- **Footstep variation**: different sounds per footwork type (sliding for
  tenkan, sharp step for irimi)
- **Weapon sounds**: katana swing (light/heavy), impact on flesh, impact on
  blade (deflect)
- **Musubi feedback**: distinct chime for perfect timing, subtle click for good
- **Ki break**: satisfying crack/shatter sound
- **Ambient**: wooden dojo creaks, outdoor courtyard wind

---

## 6. Technical Architecture

### 6.1 Extending the Existing FPS Demo

The MVP builds on the existing `demo/fps-controller/` codebase:

```
demo/fps-controller/
├── src/
│   ├── player/
│   │   ├── player.gd              # Extend State enum, add footwork states
│   │   ├── health_component.gd    # Reuse as-is
│   │   ├── footwork_system.gd     # NEW: footwork state machine & movement
│   │   ├── ki_component.gd        # NEW: Ki gauge (parallel to health)
│   │   ├── musubi_system.gd       # NEW: timing window detection
│   │   ├── weapon_controller.gd   # NEW: katana strikes, chains from footwork
│   │   └── camera_fx.gd           # NEW: procedural sway, FOV, hit-stop
│   ├── enemy/
│   │   ├── enemy.gd               # NEW: Kendo Practitioner base
│   │   ├── enemy_ai.gd            # NEW: AI state machine
│   │   └── enemy_stats.gd         # NEW: Resource for enemy tuning
│   ├── combat/
│   │   ├── hitbox.gd              # NEW: Area3D-based hitbox
│   │   └── hurtbox.gd             # NEW: Area3D-based hurtbox
│   ├── ui/
│   │   ├── hud.gd                 # NEW: Ki gauges, HP, Musubi indicator
│   │   ├── main_menu.gd           # NEW
│   │   ├── results_screen.gd      # NEW
│   │   └── death_screen.gd        # NEW: Sifu-style death screen
│   ├── dojo/
│   │   ├── dojo_manager.gd        # NEW: tutorial flow controller
│   │   ├── training_dummy.gd      # NEW: static target for drills
│   │   └── drill.gd               # NEW: base class for drill sequences
│   └── resources/
│       ├── player_stats.gd        # Extend with footwork/Ki/combat params
│       ├── weapon_data.gd         # NEW: katana stats Resource
│       ├── decisive_technique.gd  # NEW: Resource for cinematic finisher data
│       └── default_player_stats.tres
├── scenes/
│   ├── player.tscn                # Extend with new child nodes
│   ├── enemy.tscn                 # NEW
│   ├── dojo.tscn                  # NEW: tutorial environment
│   ├── arena.tscn                 # NEW: combat arena
│   └── ui/
│       ├── hud.tscn               # NEW
│       └── main_menu.tscn         # NEW
└── tests/
    ├── test_health_component.gd   # Existing
    ├── test_ki_component.gd       # NEW
    ├── test_footwork_system.gd    # NEW
    ├── test_musubi_system.gd      # NEW
    └── test_weapon_controller.gd  # NEW
```

### 6.2 Node Composition (player scene tree)

```
Player (CharacterBody3D)
├── CollisionShape3D (CapsuleShape3D)
├── Head (Node3D)
│   ├── Camera3D
│   │   └── CameraFX (Node — procedural effects script)
│   └── WeaponMount (Node3D)
│       └── KatanaModel (MeshInstance3D or placeholder)
├── HealthComponent (Node)
├── KiComponent (Node)             # NEW
├── FootworkSystem (Node)          # NEW
├── MusubiSystem (Node)            # NEW
├── WeaponController (Node)        # NEW
├── Hitbox (Area3D)                # NEW — player's weapon hitbox
├── Hurtbox (Area3D)               # NEW — player's vulnerable area
└── AudioStreamPlayer3D
```

### 6.3 Signal Flow

```
Enemy.attack_started ──→ MusubiSystem.on_enemy_attack()
                              │
FootworkSystem.footwork_executed ──→ MusubiSystem.check_musubi_timing()
                                         │
                                    MusubiSystem.musubi_triggered(quality)
                                         │
                           ┌─────────────┼─────────────┐
                           ▼             ▼             ▼
                    KiComponent    WeaponController  CameraFX
                    .add_ki()      .enable_chain()   .play_musubi_fx()
                           │
                    KiComponent.ki_depleted ──→ Enemy.on_ki_broken()
```

### 6.4 State Machine Extensions

The Player's state enum expands:

```gdscript
enum State {
    IDLE, WALKING, JUMPING, FALLING, DEAD,  # existing (SPRINTING removed — no stamina)
    IRIMI_OMOTE, IRIMI_URA,                 # new — footwork
    TENKAN_OMOTE, TENKAN_URA,               # new — footwork
    FOOTWORK_RECOVERY,                       # new — brief vulnerability after footwork
    ATTACKING,                               # new — weapon strike active
    STUMBLE,                                 # new — Ki depleted, vulnerable
    DECISIVE_TECHNIQUE,                      # new — auto-cinematic finisher playing
}
```

---

## 7. Tuning & Balance Levers

All values are exposed via Resource files for rapid iteration:

| Parameter | Location | Default | Notes |
|-----------|----------|---------|-------|
| Irimi distance | PlayerStats | 3.0m | How far irimi moves you |
| Irimi duration | PlayerStats | 0.2s | Movement time |
| Tenkan arc | PlayerStats | 180° | Rotation amount |
| Tenkan duration | PlayerStats | 0.3s | Rotation time |
| Musubi perfect window | PlayerStats | 50ms | ±25ms from sweet spot |
| Musubi good window | PlayerStats | 100ms | ±50ms from sweet spot |
| Ki drain on perfect Musubi | PlayerStats | 30 | Enemy Ki loss |
| Ki regen rate (player) | PlayerStats | 3/s | Passive recovery |
| Ki regen rate (enemy) | PlayerStats | 5/s | Enemy recovers faster |
| Katana base damage | WeaponData | 20 | Neutral attack |
| Footwork chain damage mult | WeaponData | 1.5x | Bonus for chaining |
| Enemy tell duration | EnemyStats | 0.3–0.6s | Per attack type |

---

## 8. Implementation Phases

### Phase 0 — Foundation (~3 sessions)
- [ ] Extend PlayerStats with footwork and combat parameters (remove stamina)
- [ ] Create KiComponent (mirror HealthComponent pattern)
- [ ] Create FootworkSystem node with irimi/tenkan state machine
- [ ] Input mapping for footwork (Shift + direction, RMB for ura)
- [ ] Unit tests for KiComponent and FootworkSystem

### Phase 1 — Core Footwork (~3 sessions)
- [ ] Irimi movement (linear interpolation, omote/ura variants)
- [ ] Tenkan movement (rotational interpolation, omote/ura variants)
- [ ] CameraFX — procedural sway per footwork type
- [ ] FOV shifts during footwork
- [ ] State machine integration with Player (remove SPRINTING state)
- [ ] Footwork cooldown system (Ki-gated, not stamina-gated)

### Phase 2 — Combat Loop (~4 sessions)
- [ ] Hitbox/Hurtbox Area3D system
- [ ] WeaponController — katana strikes, chain from footwork
- [ ] MusubiSystem — timing window detection
- [ ] Enemy base class with AI state machine
- [ ] Kendo Practitioner — 4 attack patterns with tells
- [ ] Ki break → stagger → auto-cinematic decisive technique
- [ ] Decisive technique camera system (cinematic angle, ZZZ/Sifu style)
- [ ] Hit-stop and screen shake via CameraFX
- [ ] Unit tests for MusubiSystem and WeaponController

### Phase 3 — Dojo Mode (~2 sessions)
- [ ] Dojo environment (simple box level with wooden floor)
- [ ] Training dummy (static target)
- [ ] Drill system — sequential tutorial steps
- [ ] 7 drills: movement, irimi, tenkan, omote/ura, musubi, ki, free practice
- [ ] Drill completion detection

### Phase 4 — Arena & Polish (~2 sessions)
- [ ] Arena environment (dojo courtyard)
- [ ] Scoring system (time, accuracy, damage, variety)
- [ ] HUD — Ki gauges, HP, Musubi indicator
- [ ] Death screen (Sifu-style: show cause of death, retry prompt)
- [ ] Main menu, pause menu, results screen
- [ ] Audio: footsteps, weapon sounds, Musubi chimes, Ki break
- [ ] Local leaderboard (save to user:// )

### Phase 5 — Playtest & Tune (~ongoing)
- [ ] Timing window tuning (Musubi feels right?)
- [ ] Camera comfort pass (no nausea during tenkan?)
- [ ] Ki economy balance (fights too long? too short?)
- [ ] Enemy difficulty curve (tells readable? combos fair?)
- [ ] Footwork responsiveness (inputs feel snappy?)
- [ ] Death screen pacing (informative without breaking flow?)

---

## 9. Design Decisions (Resolved)

1. **Decisive techniques**: Auto-cinematic (ZZZ chain attack / Sifu takedown
   style). Camera pulls to cinematic angle, player executes Aikido technique
   automatically. No QTE.
2. **No stamina system**: Footwork is Ki-gated and cooldown-gated, not
   stamina-gated. The gameplay loop is about routing and timing (Ghostrunner /
   ZZZ / Sifu), not resource management. StaminaComponent from the FPS demo
   is not used.
3. **Death mechanic**: Brief death screen (Sifu-style). Shows what killed you,
   gives a moment to process, then retry. Supports the route-optimization loop.

## 10. Open Questions

1. **Enemy variety post-MVP**: Naginata user (range), unarmed grappler
   (close range), archer (ranged pressure)?
2. **Mobile adaptation**: How do 6 footwork types map to touch? Swipe
   directions + tap timing? This is a future problem but worth noting.
3. **Decisive technique variety**: Should different Ki-break situations trigger
   different cinematic finishers, or one per weapon for MVP?
4. **Footwork cooldown tuning**: How long between consecutive footwork? Too
   short = spam, too long = sluggish. Needs playtesting.
5. **Movement speed**: Without sprint, should base movement be faster? Or is
   footwork the primary way to close/create distance?
