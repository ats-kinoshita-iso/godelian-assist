# Aiki-FPS: Game Design Document (MVP)

**Version**: 0.3.0-alpha
**Last Updated**: 2026-03-29
**Engine**: Godot 4.x (4.6.1+)
**Language**: GDScript 2.0

---

## 1. Vision Statement

A **first-person Sifu** where Aikido footwork replaces the third-person
camera's spatial awareness. In Sifu, you see enemies circling you and react
with crowd-aware positioning. In first-person, you lose that peripheral view —
so footwork (irimi to charge through, tenkan to pivot and reface) becomes your
eyes and your defense. Mastery comes from reading audio/visual tells, choosing
the right footwork response, and routing multi-enemy encounters efficiently.

**Elevator pitch**: Sifu's structure-break combat and route-optimization
endgame, translated to first-person through Aikido's footwork system.

### 1.1 Reference Games

| Reference | What We Take | Priority |
|-----------|-------------|----------|
| **Sifu** | Structure/posture system, takedowns, crowd management, arena replayability, death consequence, encounter design, combo system | **Primary** |
| **Sekiro** | Deflect timing feel, hit-stop weight, posture-break-as-kill-condition | Secondary |
| **ZZZ (Zenless Zone Zero)** | Evasive assist windows, auto-cinematic finishers, route optimization endgame | Secondary |
| **Ghostrunner / Cyberpunk 2077** | First-person melee camera feel, weapon-hand motion blur | Tertiary |
| **Bloodborne** | Aggressive play rewarded (rally-style HP recovery on finisher) | Tertiary |

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

**HP Recovery on Decisive Technique**: Completing a decisive technique restores
**15–25% of max HP** (tunable via Resource). This is critical for multi-enemy
sustain — like Sifu's takedown healing and Bloodborne's rally mechanic, it
rewards aggressive structure-breaking play with survivability. Without this,
multi-enemy encounters become attrition wars.

**Player Ki at 0**: Player enters a stumble state (~1 second), vulnerable to
a heavy hit. Not instant death, but very dangerous.

**Player Ki ↔ Health feedback**: Like Sifu, low health makes Ki recover more
slowly. This creates a death spiral that rewards clean play and punishes
taking hits — but the HP recovery on decisive techniques provides a way out.

**Player Death**: On death, a brief **death screen** displays (Sifu-style,
~2–3 seconds) showing:
- What attack killed you (e.g. "Defeated by: Men-uchi")
- Your Musubi accuracy for the attempt
- A retry prompt

This gives the player a moment to process what went wrong before the next
attempt — supporting the routing/optimization loop.

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
  **Best against**: vertical attacks (men-uchi, shomenuchi) — you step inside
  the arc before it develops.
- **Tenkan Musubi**: Pivot AWAY from attack line. Lower risk, lower reward.
  Perfect Musubi = player ends at enemy's flank.
  **Best against**: thrusts and horizontal attacks (tsuki, do-uchi) — you
  redirect the linear/sweeping force.

#### Directional Attack Matching (from Sifu)

Like Sifu's high/low avoid system, certain footwork is **preferred** against
certain attack directions. Using the wrong footwork doesn't guarantee failure,
but the Musubi window is tighter:

| Attack Direction | Preferred Footwork | Window Bonus | Wrong Footwork Penalty |
|------------------|--------------------|-------------|----------------------|
| **Vertical** (overhead) | Irimi (step inside arc) | +20ms window | -15ms window |
| **Horizontal** (sweep) | Tenkan (pivot away) | +20ms window | -15ms window |
| **Thrust** (linear) | Tenkan (redirect line) | +20ms window | -15ms window |
| **Low** (sweep kick) | Irimi (step over/past) | +20ms window | -15ms window |

This adds a **read-and-react** layer: you must identify the attack type from
the tell and choose the right footwork, not just time it correctly.

### 2.4 Weapon & Combo System (MVP: Katana only)

The katana maps to Aikido's natural hand positions. Strikes chain from
footwork, and specific input sequences produce distinct combo moves (like Sifu).

#### Footwork Chain Attacks

| Footwork → Strike | Attack Type | Damage | Speed | Ki Damage |
|-------------------|-------------|--------|-------|-----------|
| Irimi-omote → Shomenuchi | Overhead vertical cut | High | Medium | High |
| Irimi-ura → Tsuki | Forward thrust | Medium | Fast | Medium |
| Tenkan-omote → Yokomenuchi | Diagonal sweeping cut | Medium | Medium | Medium |
| Tenkan-ura → Kesa-giri | Reverse diagonal | Medium | Medium | Medium |

#### Neutral Combos (Sifu-style input sequences)

| Input Sequence | Move | Properties |
|----------------|------|-----------|
| LMB | Quick slash | Fast, low damage, combo starter |
| LMB → LMB → LMB | 3-hit chain | Standard combo, last hit has Ki bonus |
| LMB → LMB → hold LMB | Rising cut | Launcher/stagger, high Ki damage |
| LMB → pause → LMB | Delayed slash | Catches dodge-happy enemies, timing mix-up |
| Hold LMB | Charged cut | Slow, high damage, high Ki damage |
| LMB → LMB → LMB → hold LMB | Finisher combo | 4-hit string, last hit sweeps (crowd tool) |

#### Combo Design Philosophy

Following Sifu: combos are **not just damage strings** — each has tactical
purpose. The sweep finisher hits multiple enemies. The delayed slash is a
mix-up. The rising cut is your best structure damage. Players should use
different combos for different situations, not spam the same one.

**Input**: LMB = light attack, hold LMB = heavy attack. Footwork + LMB within
the chain window = footwork-specific strike. Specific LMB sequences with
timing variations = combo moves.

### 2.5 Ki Burst System (Focus attack analog)

Sifu rewards aggression with Focus attacks — unblockable specials earned by
landing hits. Our equivalent is the **Ki Burst** system.

**Ki Burst meter**: Builds by landing attacks on enemies (not by taking damage
or defending). Displayed as segmented pips near HP.

| Action | Meter Gain |
|--------|-----------|
| Landing a neutral combo hit | +3 per hit |
| Landing a footwork chain attack | +8 |
| Perfect Musubi | +15 |
| Good Musubi | +8 |
| Getting hit | -5 (punishment for sloppy play) |

**MVP Ki Burst techniques** (cost 1 segment each, **unblockable**):

| Technique | Effect | Tactical Role |
|-----------|--------|--------------|
| **Atemi** (当て身) | Sharp palm strike, high Ki damage to single target | Structure breaker vs tough enemies |
| **Irimi-nage** (入り身投げ) | Enter and throw, sends enemy into nearby enemies | Crowd control, environmental combo |
| **Kokyu-ho** (呼吸法) | Breath power — brief burst of speed, next footwork has extended Musubi window | Defensive reset, positioning tool |

Ki Bursts are your **trump card** — they bypass enemy guard and provide
guaranteed Ki damage or crowd control. They reward aggressive, accurate play.

### 2.6 Crowd Management (the FP Sifu problem)

Sifu is fundamentally about fighting 2–5 enemies simultaneously, with the
third-person camera giving spatial awareness. In first-person, **you can't see
behind you** — so the crowd management system must compensate.

#### Aggression Management (from Sifu)

Not all enemies attack at once. The system manages threat timing:

| Enemies Present | Actively Attacking | Circling / Threatening |
|----------------|--------------------|----------------------|
| 1 | 1 | 0 |
| 2 | 1–2 | 0–1 |
| 3 | 1–2 | 1–2 |
| 4–5 | 2 | 2–3 |

Circling enemies telegraph their intent to attack with audio cues (footsteps
closing in, weapon sounds, kiai shouts) before transitioning to active.

#### FP Spatial Awareness Compensations

Since you lose the third-person peripheral view, the game provides:

1. **Directional audio**: 3D positional audio for enemy footsteps, breathing,
   weapon readying. This is the PRIMARY spatial awareness tool.
2. **Threat indicator**: Subtle UI arrows at screen edges showing direction
   of nearby enemies (like FPS radar, but minimal — just directional pips).
3. **Footwork as repositioning**: Tenkan naturally rotates you to face new
   threats. Irimi lets you charge through a group to the other side.
   Footwork IS your crowd management tool.
4. **Peripheral flash**: Screen edge briefly flashes red from the direction
   of an incoming attack you can't see — gives ~0.3s warning to tenkan.
5. **Lock-on toggle**: Soft lock-on to current target. Tenkan breaks lock
   and snaps to nearest threat in the pivot direction.

#### Encounter Design (from Sifu)

MVP arena encounters should escalate:

- **Wave 1**: 1v1 (pure footwork/Musubi practice)
- **Wave 2**: 1v2 (introduce crowd management)
- **Wave 3**: 1v3 (requires footwork repositioning + combo sweeps)
- **Boss**: 1v1 Kendo Practitioner (full moveset, multi-phase)

### 2.7 Environmental Interaction

Even in MVP, the environment should be a combat tool (from Sifu):

| Interaction | Trigger | Effect |
|-------------|---------|--------|
| **Wall slam** | Irimi an enemy near a wall | Bonus Ki damage + brief stun |
| **Throw into enemy** | Ki Burst irimi-nage near other enemies | Knockdown on thrown enemy AND hit enemies |
| **Obstacle vault** | Footwork near low obstacle | Player vaults, gains height advantage |
| **Weapon pickup** | Walk over dropped weapon | Temporary weapon swap (post-MVP) |

Wall slams are the critical MVP interaction — they reward spatial awareness
and create another reason to use irimi aggressively.

### 2.8 Death Consequence System

A simple retry loop lacks the weight of Sifu's aging system. Our equivalent
uses **Composure** — a per-run resource that degrades with each death.

**Composure** (0–100, starts at 100):
- Each death costs composure: **-10 × death_count** in the current run
  (1st death = -10, 2nd = -20, 3rd = -30... accelerating like Sifu's aging)
- Composure affects gameplay:

| Composure | Effect |
|-----------|--------|
| 100–70 | Normal gameplay. Full HP, normal Ki regen. |
| 69–40 | **Focused**: -15% max HP, +15% Ki Burst gain. Getting sharper but fragile. |
| 39–10 | **Desperate**: -30% max HP, +30% Ki Burst gain, decisive techniques deal +25% damage. Glass cannon. |
| Below 10 | **Final Stand**: One more death = run over. Max Ki Burst gain, minimal HP. |
| 0 | **Run over**. Must restart the arena from Wave 1. |

**Composure recovery**: Performing a decisive technique recovers +5 composure
(in addition to HP recovery). Clean play digs you out of the death spiral.

This mirrors Sifu's aging arc: early deaths are cheap, but they compound.
Skilled players can complete a run at full composure. The glass-cannon effect
at low composure makes desperate runs exciting, not hopeless.

### 2.9 Camera & First-Person Feel

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

### 2.10 Enemy Design (MVP: One Type + Fodder)

Two enemy types for MVP: **Dojo Students** (fodder for crowd encounters) and
the **Kendo Practitioner** (boss).

#### Dojo Student (Fodder Enemy)

Basic fighters with simple, readable patterns. Designed to teach crowd
management. Low HP, low Ki, 1–2 attack patterns.

| Attack | Tell | Damage | Ki Damage |
|--------|------|--------|-----------|
| **Straight punch** | Pulls fist back, 0.4s windup | 10 | 5 |
| **Front kick** | Shifts weight back, 0.5s windup | 15 | 8 |

- Die to 2–3 combo hits or a single footwork chain attack
- Structure breaks after 2 successful Musubi deflects
- Serve as Ki Burst meter batteries — reward aggressive play
- In groups of 2–3, they test crowd management and spatial awareness

#### Kendo Practitioner (Boss)

A disciplined swordsman with readable but demanding attack patterns.

#### Boss Attack Patterns

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
                    ┌──────────────────────────────────────────┐
                    │        CROWD MANAGER (global)            │
                    │  Assigns ACTIVE/CIRCLING roles per enemy │
                    └───────┬──────────────────┬───────────────┘
                            ▼                  ▼
                      [ACTIVE slot]      [CIRCLING slot]
                            │                  │
IDLE → APPROACH → ATTACK_WINDUP → ATTACK_ACTIVE → RECOVERY → IDLE
                                                 ↓
                                            STAGGERED (Ki break)
                                                 ↓
                                            VULNERABLE (decisive technique)
```

The **Crowd Manager** is a global coordinator that assigns attack slots.
Only 1–2 enemies hold ACTIVE slots at any time. CIRCLING enemies move to
flank positions, play threatening audio, and occasionally feint — but don't
commit to attacks until given an ACTIVE slot.

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

A dojo courtyard arena with escalating wave-based encounters (like Sifu's
arena mode). Each run uses the Composure system — deaths cost composure,
and reaching 0 ends the run.

#### Wave Structure

| Wave | Enemies | Purpose |
|------|---------|---------|
| **1** | 2 Dojo Students | Warm-up, basic crowd management |
| **2** | 3 Dojo Students | Crowd pressure, footwork repositioning |
| **3** | 1 Dojo Student + Kendo Practitioner | Boss intro with distraction |
| **4** | Kendo Practitioner (Phase 2 unlocked) | Full boss, multi-phase |

#### Scoring

| Metric | Weight | Sifu Parallel |
|--------|--------|--------------|
| **Composure remaining** | 30% | Age at completion |
| **Musubi accuracy** (perfect/good/miss) | 25% | Parry precision |
| **Time** | 20% | Speed of completion |
| **Combo variety** | 15% | Combat diversity |
| **Damage taken** | 10% | Efficiency |

Leaderboard is local (MVP). The Sifu-style replayability loop: optimize your
route through waves, minimize deaths to preserve composure, master the boss
to finish with a high score. A perfect run (zero deaths, all perfect Musubi)
is the aspirational goal — like completing Sifu at age 20.

---

## 4. HUD & UI

### 4.1 In-Game HUD

```
┌─────────────────────────────────────────────┐
│  [Player Ki ████████░░]    [Enemy Ki ████░░] │
│                                              │
│            ◁ (threat pip)    ▷               │
│               (gameplay view)                │
│                                              │
│                                              │
│  [HP ██████░░]          ◆ MUSUBI INDICATOR   │
│  [Ki Burst ●●○]        Composure: 85        │
└─────────────────────────────────────────────┘
```

- **Ki gauges**: top of screen, opponent-style (like Sekiro)
- **HP**: bottom-left, minimal
- **Ki Burst pips**: segmented meter below HP (like Sifu's Focus)
- **Composure**: small number, bottom-right (like Sifu's age display)
- **Threat pips**: directional arrows at screen edges for off-screen enemies
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
│   │   ├── weapon_controller.gd   # NEW: katana strikes, combos, chains
│   │   ├── ki_burst_system.gd     # NEW: Focus attack analog
│   │   ├── combo_system.gd        # NEW: input sequence detection
│   │   └── camera_fx.gd           # NEW: procedural sway, FOV, hit-stop
│   ├── enemy/
│   │   ├── enemy_base.gd          # NEW: base class for all enemies
│   │   ├── dojo_student.gd        # NEW: fodder enemy
│   │   ├── kendo_practitioner.gd  # NEW: boss enemy
│   │   ├── enemy_ai.gd            # NEW: per-enemy AI state machine
│   │   ├── crowd_manager.gd       # NEW: global aggression slot manager
│   │   └── enemy_stats.gd         # NEW: Resource for enemy tuning
│   ├── combat/
│   │   ├── hitbox.gd              # NEW: Area3D-based hitbox
│   │   ├── hurtbox.gd             # NEW: Area3D-based hurtbox
│   │   ├── composure_system.gd    # NEW: death consequence tracking
│   │   └── environment_interact.gd # NEW: wall slams, throws
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
├── KiComponent (Node)             # NEW — structure gauge
├── KiBurstSystem (Node)           # NEW — Focus attack analog
├── FootworkSystem (Node)          # NEW — footwork state machine
├── MusubiSystem (Node)            # NEW — timing window detection
├── ComboSystem (Node)             # NEW — input sequence tracking
├── WeaponController (Node)        # NEW — strike execution
├── ThreatIndicator (Control)      # NEW — directional enemy pips on HUD
├── Hitbox (Area3D)                # NEW — player's weapon hitbox
├── Hurtbox (Area3D)               # NEW — player's vulnerable area
└── AudioStreamPlayer3D
```

#### Arena Scene Tree

```
Arena (Node3D)
├── Environment (Node3D)
│   ├── DojoCourtyard (MeshInstance3D or CSG)
│   ├── Walls (StaticBody3D)       # For wall-slam interactions
│   └── SpawnPoints (Node3D)
├── CrowdManager (Node)            # Global aggression slot manager
├── ComposureSystem (Node)         # Per-run death consequence
├── WaveManager (Node)             # Controls enemy spawn waves
├── EnemyContainer (Node3D)        # Parent for spawned enemies
├── UI (CanvasLayer)
│   ├── HUD
│   └── DeathScreen
└── AudioManager (Node)
```

### 6.3 Signal Flow

```
CrowdManager.assign_active_slot ──→ EnemyAI.set_role(ACTIVE/CIRCLING)
                                         │
Enemy.attack_started ──→ MusubiSystem.on_enemy_attack()
                              │
FootworkSystem.footwork_executed ──→ MusubiSystem.check_musubi_timing()
                                         │
                                    MusubiSystem.musubi_triggered(quality)
                                         │
                       ┌─────────┬───────┼──────────┬──────────┐
                       ▼         ▼       ▼          ▼          ▼
                 KiComponent  KiBurst  Weapon    CameraFX  ThreatIndicator
                 .add_ki()    .add()   .chain()  .play()   .update()
                       │
                 KiComponent.ki_depleted ──→ Enemy.on_ki_broken()
                       │                          │
                       │                   DecisiveTechnique (cinematic)
                       │                          │
                       │                   ├── HealthComponent.heal()
                       │                   └── ComposureSystem.recover()
                       │
                 Player.died ──→ ComposureSystem.on_death()
                                      │
                              ┌───────┴────────┐
                              ▼                ▼
                        DeathScreen      (composure > 0?)
                        .show()           ├── YES: respawn
                                          └── NO: run_over
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
| **Footwork** | | | |
| Irimi distance | PlayerStats | 3.0m | How far irimi moves you |
| Irimi duration | PlayerStats | 0.2s | Movement time |
| Tenkan arc | PlayerStats | 180° | Rotation amount |
| Tenkan duration | PlayerStats | 0.3s | Rotation time |
| Footwork cooldown | PlayerStats | 0.4s | Time between consecutive footwork |
| **Musubi** | | | |
| Musubi perfect window | PlayerStats | 50ms | ±25ms from sweet spot |
| Musubi good window | PlayerStats | 100ms | ±50ms from sweet spot |
| Directional match bonus | PlayerStats | 20ms | Extra window for correct footwork |
| Directional mismatch penalty | PlayerStats | 15ms | Reduced window for wrong footwork |
| **Ki** | | | |
| Ki drain on perfect Musubi | PlayerStats | 30 | Enemy Ki loss |
| Ki regen rate (player) | PlayerStats | 3/s | Passive recovery |
| Ki regen rate (enemy) | PlayerStats | 5/s | Enemy recovers faster |
| Low-HP Ki regen penalty | PlayerStats | 0.5x | Ki regen mult when HP < 30% |
| **Ki Burst** | | | |
| Ki Burst segments | PlayerStats | 3 | Max segments |
| Burst gain per hit | PlayerStats | 3 | Neutral combo hit |
| Burst gain per chain | PlayerStats | 8 | Footwork chain attack |
| Burst gain per perfect | PlayerStats | 15 | Perfect Musubi |
| **Weapon** | | | |
| Katana base damage | WeaponData | 20 | Neutral attack |
| Footwork chain damage mult | WeaponData | 1.5x | Bonus for chaining |
| Sweep finisher arc | WeaponData | 120° | Crowd hit angle |
| **Decisive Technique** | | | |
| HP recovery on finisher | PlayerStats | 20% | % of max HP restored |
| Composure recovery | PlayerStats | 5 | Composure restored per finisher |
| **Composure** | | | |
| Starting composure | ArenaConfig | 100 | Per-run starting value |
| Death cost multiplier | ArenaConfig | 10 | Cost = multiplier × death_count |
| **Enemies** | | | |
| Max active attackers | CrowdConfig | 2 | Simultaneous attack slots |
| Circling threat audio delay | CrowdConfig | 1.5s | Time before audio warning |
| Peripheral flash warning | CrowdConfig | 0.3s | Warning time for off-screen attacks |
| Enemy tell duration | EnemyStats | 0.3–0.6s | Per attack type |
| Wall slam bonus Ki damage | EnemyStats | 15 | Extra Ki damage on wall slam |

---

## 8. Implementation Phases

### Phase 0 — Foundation (~3 sessions)
- [ ] Extend PlayerStats with footwork, combat, Ki Burst parameters (remove stamina)
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
- [ ] Footwork cooldown system (cooldown-gated, not stamina-gated)

### Phase 2 — Combat Core (~5 sessions)
- [ ] Hitbox/Hurtbox Area3D system
- [ ] ComboSystem — input sequence detection (Sifu-style combos)
- [ ] WeaponController — katana strikes, chain from footwork
- [ ] MusubiSystem — timing window detection with directional matching
- [ ] Dojo Student enemy (fodder) — 2 attack patterns
- [ ] Ki break → stagger → auto-cinematic decisive technique
- [ ] HP recovery on decisive technique
- [ ] Hit-stop and screen shake via CameraFX
- [ ] Unit tests for MusubiSystem, ComboSystem, WeaponController

### Phase 3 — Multi-Enemy & Systems (~4 sessions)
- [ ] CrowdManager — global aggression slot system
- [ ] Enemy aggression roles (ACTIVE/CIRCLING with audio tells)
- [ ] ThreatIndicator — directional pips for off-screen enemies
- [ ] Peripheral flash warning for incoming off-screen attacks
- [ ] KiBurstSystem — meter build, 3 MVP techniques (atemi, irimi-nage, kokyu-ho)
- [ ] Environmental interaction — wall slams (irimi near wall = bonus Ki damage)
- [ ] Throw-into-enemy interaction (irimi-nage Ki Burst)
- [ ] ComposureSystem — death consequence with escalating cost
- [ ] Unit tests for CrowdManager, KiBurstSystem, ComposureSystem

### Phase 4 — Dojo Mode (~2 sessions)
- [ ] Dojo environment (simple box level with wooden floor)
- [ ] Training dummy (static target)
- [ ] Drill system — sequential tutorial steps
- [ ] 8 drills: movement, irimi, tenkan, omote/ura, musubi, combos, ki burst, free practice
- [ ] Drill completion detection

### Phase 5 — Boss & Arena (~3 sessions)
- [ ] Kendo Practitioner boss — 4 attack patterns, multi-phase (2 phases)
- [ ] Phase transitions on structure break (Sifu-style)
- [ ] WaveManager — 4-wave arena structure
- [ ] Scoring system (composure, accuracy, time, variety, damage)
- [ ] HUD — Ki gauges, HP, Ki Burst pips, composure, threat pips, Musubi indicator
- [ ] Death screen (Sifu-style: cause of death, Musubi accuracy, retry/run over)
- [ ] Main menu, pause menu, results screen
- [ ] Local leaderboard (save to user://)

### Phase 6 — Audio & Polish (~2 sessions)
- [ ] 3D positional audio for enemy spatial awareness (CRITICAL for FP)
- [ ] Footstep variation per footwork type
- [ ] Weapon sounds: katana swing, impact, deflect
- [ ] Musubi feedback: chime (perfect), click (good)
- [ ] Ki break sound, decisive technique audio
- [ ] Circling enemy audio tells (footsteps, weapon sounds, kiai)
- [ ] Wall slam impact sound
- [ ] Ambient: dojo creaks, courtyard wind

### Phase 7 — Playtest & Tune (~ongoing)
- [ ] Timing window tuning (Musubi feels right? Directional matching fair?)
- [ ] Camera comfort pass (no nausea during tenkan?)
- [ ] Ki economy balance (fights too long? too short?)
- [ ] Ki Burst economy (earned too fast? too slow? techniques impactful?)
- [ ] Composure pacing (death spiral too harsh? too lenient?)
- [ ] Crowd management feel (aggression slots natural? audio tells readable?)
- [ ] Enemy difficulty curve (tells readable? combos fair? boss phases balanced?)
- [ ] Footwork responsiveness (inputs feel snappy?)
- [ ] Death screen pacing (informative without breaking flow?)
- [ ] Wall slam positioning (consistent detection? satisfying feel?)

---

## 9. Design Decisions (Resolved)

1. **Decisive techniques**: Auto-cinematic (ZZZ chain attack / Sifu takedown
   style). Camera pulls to cinematic angle, player executes Aikido technique
   automatically. No QTE. Heals HP and restores composure.
2. **No stamina system**: Footwork is cooldown-gated, not stamina-gated.
   The gameplay loop is about routing and timing (Sifu / ZZZ), not resource
   management. StaminaComponent from the FPS demo is not used.
3. **Death mechanic**: Brief death screen (Sifu-style) with Composure system.
   Deaths have escalating cost. Run ends at composure 0. Mirrors Sifu's aging.
4. **Primary reference is Sifu**: The game is "first-person Sifu with Aikido
   footwork." Structure-break combat, crowd management, route optimization,
   combo variety, environmental interaction, and death consequences all come
   from Sifu. Footwork replaces the third-person camera's spatial awareness.
5. **Multi-enemy encounters in MVP**: Crowd management is core, not post-MVP.
   Dojo Students serve as fodder. CrowdManager controls aggression slots.
   Audio + threat indicators compensate for lost third-person perspective.
6. **Ki Burst system**: Rewards aggression with unblockable specials (like
   Sifu's Focus attacks). Builds by landing hits, spent on tactical techniques.

## 10. Open Questions

1. **Enemy variety post-MVP**: Naginata user (range), unarmed grappler
   (close range), archer (ranged pressure)?
2. **Mobile adaptation**: How do 6 footwork types map to touch? Swipe
   directions + tap timing? This is a future problem but worth noting.
3. **Decisive technique variety**: Should different Ki-break situations trigger
   different cinematic finishers, or one per weapon for MVP?
4. **Combo unlock progression**: Should combos be available from the start
   (like Sifu post-unlock) or gated behind an XP/mastery system?
5. **Lock-on behavior**: Soft lock-on that follows current target? Hard lock
   that requires manual break? How does tenkan interact with lock-on?
6. **Movement speed**: Without sprint, should base movement be faster? Or is
   footwork the primary way to close/create distance?
7. **Composure visual feedback**: Should the player model/hands visibly change
   at low composure (like Sifu's aging)? E.g., hand tremor, narrowed FOV?
