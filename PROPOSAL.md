# godelian-assist v2: Complete Godot Developer — Proposal

**Date**: 2026-03-26
**Status**: Proposed
**Goal**: Transform godelian-assist from a knowledge/advice library into an autonomous Godot programmer that creates and iterates on gameplay, taking design direction from the user and handling all implementation independently.

---

## 1. Current State Assessment

### What godelian-assist does well today

All 12 Phase 1–3 features are passing. The library provides Claude with:

- **Knowledge**: scene patterns, GDScript idioms, quality gates, game design frameworks
- **Advice**: skills that guide decisions (scene architecture, signal design, state machines)
- **Standards**: hooks that enforce code quality at commit time

### The fundamental gap

godelian-assist makes Claude a knowledgeable *consultant*. The target is Claude as a *programmer*. The distinction:

| Consultant (current) | Programmer (target) |
|----------------------|---------------------|
| Explains how to structure a scene | Creates the `.tscn` file |
| Describes signal patterns | Writes the signal bus and connects it |
| Suggests a save system design | Implements and tests the save system |
| Tells you what to fix | Runs the game, reads the error, fixes it |
| Gives you a spec | Takes a spec, delivers working gameplay |

### What exists in the broader ecosystem that we're missing

From research across 30+ projects (godogen, GDAI MCP, Claude-Code-Game-Studios, Ziva, twaananen/claude-code-gdscript, etc.):

| Capability | Ecosystem solution | godelian-assist today |
|-----------|-------------------|----------------------|
| Live editor control (read/write scenes, run game) | GDAI MCP (95+ tools) | Not integrated |
| GDScript LSP diagnostics in Claude Code | claude-code-gdscript LSP bridge | Not integrated |
| Visual feedback (screenshots of running game) | GDAI MCP / Ziva | Not integrated |
| Create `.tscn` files from scratch | Godogen, GDAI MCP | No skill exists |
| Designer → programmer handoff workflow | Claude-Code-Game-Studios | No formal workflow |
| Godot API reference embedded in context | Godogen (850+ classes) | Not embedded |
| New project bootstrapping | Godogen | No skill exists |
| Debug output → fix loop | GDAI MCP | Not integrated |
| Gameplay iteration agent | Godogen, GDAI MCP | Not implemented |

---

## 2. Research Findings (Key Insights)

### 2a. The #1 failure mode: Godot 3 vs. Godot 4 contamination

Every LLM tested defaults to Godot 3 syntax unless explicitly constrained. Common wrong outputs:

```gdscript
# Godot 3 (wrong) — LLM default
move_and_slide(velocity, Vector2.UP)
yield(get_tree(), "idle_frame")
connect("signal", self, "_callback")

# Godot 4 (correct) — what we must enforce
move_and_slide()  # velocity is a property now
await get_tree().process_frame
signal_name.connect(_callback)
```

**Solution**: Embed a Godot 4.x version guard in every skill and add a dedicated Godot 3→4 migration reference to the context.

### 2b. The scene file gap is the biggest usability blocker

Claude can write GDScript but cannot create a `.tscn` file — the primary Godot artifact. Without scene files, every feature requires the user to manually set up the scene tree, which breaks the "sole programmer" model.

The `.tscn` text format is fully AI-readable and writable:

```
[gd_scene load_steps=3 format=3 uid="uid://xxx"]
[ext_resource type="Script" path="res://player.gd" id="1_abc"]
[node name="Player" type="CharacterBody3D"]
script = ExtResource("1_abc")
[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
shape = CapsuleShape3D(...)
```

A skill teaching Claude to generate this format unlocks the most critical capability gap.

### 2c. MCP is the path to live editor control

The GDAI MCP server (gdaimcp.com) + Godot plugin combo provides 95+ tools including:
- Read/write scene nodes and properties
- Run the game and capture debug output
- Take editor/viewport screenshots
- GDScript LSP diagnostics
- DAP debugger integration

Integrating this as a cookbook recipe (and eventually a plugin) makes Claude's feedback loop close: write code → run → screenshot → fix → repeat.

### 2d. The designer-programmer collaboration model is underserved

Claude-Code-Game-Studios (48 agents) is the closest existing art but is too complex to set up. What's needed is a lightweight, opinionated workflow:

1. Designer writes a brief (what mechanic, what feel, what constraints)
2. Claude produces a spec (nodes, signals, resources, GDScript skeletons)
3. Designer approves or revises the spec
4. Claude implements (creates files, runs tests)
5. Claude verifies (runs game, reads output, takes screenshot if MCP available)
6. Designer reviews and gives feedback (feels right / fix X / try Y instead)
7. Repeat from 4

This loop does not currently exist anywhere in godelian-assist.

### 2e. Text formats must be enforced from day one

Setting Godot to save `.tscn` / `.tres` as text (not binary) is a prerequisite for AI edit access. This must be enforced in the project bootstrap, not discovered later.

---

## 3. Proposal: Phased Implementation Plan

### Vision Statement

> godelian-assist becomes a complete Godot programmer. The user describes the game they want to build — the feel, the mechanics, the progression. Claude designs the architecture, writes every file, runs the game, sees the result, and iterates until it's right. The user never touches GDScript.

---

### Phase A — Live Feedback Infrastructure (Highest Priority)

These changes unlock the feedback loop that makes autonomous implementation possible. Nothing else in this proposal delivers full value without them.

#### A1. GDAI MCP Cookbook Recipe

**What**: A `cookbook/mcp/gdai-mcp.md` recipe that walks through installing and configuring the GDAI MCP server + Godot plugin. Includes the `settings.json` snippet for Claude Code.

**Why this first**: 95+ tools — run game, capture output, screenshot, read/write scene nodes — this is the foundation of the autonomous loop.

**Deliverables**:
- `cookbook/mcp/gdai-mcp.md` — Setup guide and `settings.json` config
- `cookbook/mcp/godot-mcp-minimal.md` — Alternative for the lighter Coding-Solo/godot-mcp (npm installable, run/capture only)
- Update `cookbook/claude-md/godot.md` — Add MCP usage section

**Verification**: Claude can launch Godot, run a scene, and receive debug output.

---

#### A2. GDScript LSP Bridge Cookbook Recipe

**What**: A `cookbook/mcp/gdscript-lsp.md` recipe for installing `twaananen/claude-code-gdscript` or `Sods2/claude-code-gdscript-lsp`, which bridge Godot's TCP-based LSP to Claude Code's stdio.

**Why**: Real-time GDScript diagnostics in the Claude Code session. Claude sees type errors, missing methods, and undefined variables the moment it writes code — not after running the game.

**Deliverables**:
- `cookbook/mcp/gdscript-lsp.md` — Install guide for both bridges, comparison table
- New `plugins/godot-code-quality/skills/lsp-setup/SKILL.md` — How to configure and verify LSP is working

**Verification**: Claude Code gets GDScript completions and diagnostics in the terminal session.

---

#### A3. `screenshot-review` skill in `godot-code-quality`

**What**: A skill that, when GDAI MCP is active, instructs Claude to take a screenshot after running the game and analyze whether the visual output matches the design intent.

**Why**: Closes the visual feedback loop. "Does the character jump correctly?" cannot be answered from code alone.

**Deliverables**:
- `plugins/godot-code-quality/skills/screenshot-review/SKILL.md`
- Update `cookbook/hooks/godot-quality.md` — Add a Stop hook that triggers screenshot if MCP is active

---

### Phase B — Designer-Programmer Workflow (Core Differentiator)

This is what makes godelian-assist genuinely unique. No existing project has a clean, lightweight designer → programmer loop.

#### B1. New plugin: `designer-brief`

**Purpose**: Formal handoff from designer intent to Claude implementation. The single plugin that governs how user and Claude collaborate.

**Skills**:

| Skill | Description |
|-------|-------------|
| `brief` | Designer describes a mechanic or feature in natural language. Claude outputs: what it understood, the implementation spec (nodes, signals, resources), and what questions need answering before coding begins. |
| `spec-review` | Designer reviews Claude's spec and marks it approved or revised. Claude updates the spec and confirms before touching any files. |
| `iterate` | Designer describes what felt wrong after playtesting (too fast, wrong collision, animation stutter). Claude proposes the specific code change without redesigning the whole system. |
| `playtest-debrief` | Structured format for designer feedback: what worked, what didn't, priority of fixes. Claude converts this into an ordered task list. |
| `feature-complete` | Designer marks a feature done. Claude runs the full quality gate, commits, and moves to the next backlog item. |

**Hook**: A `PreToolUse` hook on file creation that checks whether the spec was approved. If no spec exists for the files being created, Claude pauses and generates one first.

---

#### B2. New plugin: `game-backlog`

**Purpose**: Maintain a prioritized, persistent list of features from the designer's perspective. Not a code issue tracker — a game design feature board.

**Skills**:

| Skill | Description |
|-------|-------------|
| `backlog-init` | Create `plans/game-backlog.json` with the initial feature list from the designer's brief. |
| `backlog-status` | Show what's done, in-progress, and queued. Current feature highlighted. |
| `next-feature` | Pop the highest-priority feature and generate its implementation brief. |
| `add-feature` | Designer adds a new feature mid-session with priority placement. |

**Format** (`plans/game-backlog.json`):
```json
{
  "features": [
    {
      "id": 1,
      "title": "Player double-jump",
      "brief": "Player can jump a second time mid-air. Second jump has 80% of first jump height.",
      "status": "done",
      "spec": "plans/specs/player-double-jump.md"
    },
    {
      "id": 2,
      "title": "Coyote time",
      "brief": "Player can jump 0.15s after walking off a ledge.",
      "status": "in_progress",
      "spec": "plans/specs/coyote-time.md"
    }
  ]
}
```

---

#### B3. New hook: Designer Approval Gate

**What**: A `hooks.json` entry that fires before any new `.gd` or `.tscn` file is written without an associated spec in `plans/specs/`.

**Why**: Prevents Claude from implementing things the designer hasn't approved. The spec review step is not optional — it's enforced by the tooling.

**Deliverables**:
- `plugins/designer-brief/hooks/hooks.json`
- `cookbook/hooks/designer-approval.md` — Explanation and copy-paste config

---

### Phase C — Scene Builder (Closes the Sole-Programmer Gap)

#### C1. New plugin: `scene-builder`

**Purpose**: Claude can create and modify `.tscn` files directly, without requiring the user to touch the Godot editor.

This is the most technically demanding addition and the most important for the "sole programmer" model.

**Skills**:

| Skill | Description |
|-------|-------------|
| `create-scene` | Given a node tree spec, generate a complete valid `.tscn` text file. Includes proper UID generation, ext_resource references, and sub-resource inline definitions. |
| `add-node` | Add one or more nodes to an existing `.tscn` without breaking existing node paths or external references. |
| `wire-signals` | Add signal connections to a `.tscn` (the `connections` section). Validates that source node, signal name, and target method all exist. |
| `scene-from-brief` | Given a designer brief, produce both the `.tscn` and all required `.gd` scripts in one operation. The most powerful skill in the system. |
| `scene-audit` | Read an existing `.tscn` and report: orphaned scripts, missing CollisionShapes, nodes with no type annotation in their script, disconnected signals. |

**Critical technical constraint**: All generated `.tscn` files must use the text format (not binary). The skill must enforce `format=3` and real UID strings.

**`.tscn` generation pattern the skill will teach**:
```
[gd_scene load_steps=N format=3 uid="uid://GENERATED"]

; External resources (scripts, sub-scenes, audio, etc.)
[ext_resource type="Script" path="res://src/player/player.gd" id="1_HASH"]

; Sub-resources (inline shapes, materials, etc.)
[sub_resource type="CapsuleShape3D" id="CapsuleShape3D_HASH"]
radius = 0.4
height = 1.8

; Root node
[node name="Player" type="CharacterBody3D"]
script = ExtResource("1_HASH")

; Child nodes
[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
shape = SubResource("CapsuleShape3D_HASH")
```

---

### Phase D — Project Bootstrap (New Game from Zero)

#### D1. New plugin: `project-bootstrap`

**Purpose**: Start a new Godot project from scratch with all conventions pre-configured. The designer gives a one-sentence game concept; Claude sets up the entire project structure.

**Skills**:

| Skill | Description |
|-------|-------------|
| `new-project` | Create directory structure, initial `project.godot` with text format enabled and static typing enforced, `CLAUDE.md` from cookbook template, `plans/game-backlog.json` from designer brief. |
| `configure-quality` | Install gdtoolkit, set up `.gdlintrc`, configure GdUnit4 addon path, add quality gate hooks to `.claude/settings.json`. |
| `setup-autoloads` | Create the standard autoload set: `EventBus.gd` (global signal bus), `GameManager.gd` (scene transitions, pause), `SaveManager.gd` (save/load facade). |
| `setup-directories` | Create the canonical directory structure: `src/`, `scenes/`, `data/`, `assets/sounds/`, `assets/textures/`, `tests/`. |

**`project.godot` settings the skill enforces**:
```ini
[application]
config/use_binary_format=false          ; text .tscn/.tres always

[gdscript]
warnings/untyped_declaration=2          ; error on untyped var
warnings/inferred_declaration=0         ; allow := inference
warnings/return_value_discarded=1       ; warn on discarded return

[rendering]
textures/canvas_textures/default_texture_repeat=0
```

---

### Phase E — Expanded Game System Coverage

The current `game-design` plugin covers the 3D action-RPG use case well. The following additions broaden coverage to common Godot game types and fill missing mechanics.

#### E1. Expanded `game-design` plugin skills

| New Skill | Description |
|-----------|-------------|
| `combat-design` | Full combat system spec: hitboxes (Area3D), hurtboxes, damage pipeline, hit feedback (screen shake, particles, audio), combo tracking, invincibility frames. Produces Resource schema for damage types + GDScript skeleton. |
| `inventory-design` | Item system: `ItemData` Resource, inventory container (Array[ItemData]), hotbar, equipment slots. Pickup signals, weight system, stacking. |
| `dialogue-design` | Dialogue system options in Godot 4.x: Dialogic 2, custom state machine approach. Resource-based dialogue trees, portrait display, branching. |
| `enemy-design` | Enemy AI pattern: NavigationAgent3D pathfinding, sight/hearing detection with Area3D, state machine (patrol → alert → chase → attack → flee), group-based squad behavior. |
| `progression-design` | XP and leveling: `PlayerStats` Resource, curve-based XP thresholds (`Curve` resource), stat scaling, unlock gates, achievement triggers via signals. |

#### E2. New plugin: `godot-physics`

**Purpose**: Movement, collision, and physics patterns — the #1 source of "feels wrong" gameplay bugs.

| Skill | Description |
|-------|-------------|
| `character-movement` | CharacterBody3D movement patterns: ground detection, slope limit, step height, coyote time, jump buffering, air acceleration. Typed GDScript with `move_and_slide()`. |
| `collision-layers` | Collision layer/mask design for a game with multiple entity types. Produces a layer map table and the GDScript constants autoload. |
| `area-detection` | Area3D patterns: hitboxes, hurtboxes, trigger zones, sight cones. Body entered/exited signal architecture. Avoiding detection ghost frames. |
| `rigidbody-patterns` | RigidBody3D use cases: destructible objects, physics-based puzzles, ragdolls. When to use `freeze` mode, applying forces correctly, sleeping bodies. |
| `projectile-system` | Projectile architecture: pooling (avoid instantiate/free per shot), `move_and_collide` vs raycast vs area, piercing, penetration depth, network-friendly patterns. |

#### E3. New plugin: `godot-ui`

**Purpose**: Control node hierarchy, theming, and responsive layout — another top source of designer-programmer friction.

| Skill | Description |
|-------|-------------|
| `hud-design` | In-game HUD layout with Control nodes: anchors and offsets, CanvasLayer stacking, health bar (TextureProgressBar), minimap (SubViewport), cooldown icons. Signal-driven updates from game systems. |
| `menu-design` | Menu scene architecture: main menu, pause menu (process mode), settings menu, confirmation dialogs. FocusMode for controller navigation. Transition animations. |
| `theme-system` | Godot 4 Theme resource: defining StyleBox variants, fonts, color palettes. Programmatic theme application vs inspector. Responsive to accessibility settings. |
| `ui-signals` | UI signal architecture: when UI emits signals to game vs when game updates UI. Separating input handling from display. Controller-friendly focus chains. |

#### E4. New plugin: `godot-audio`

**Purpose**: Audio architecture for games — frequently left to end and then hard to retrofit.

| Skill | Description |
|-------|-------------|
| `audio-architecture` | Bus structure (Master → Music → SFX → Voice → Ambient), AudioStreamPlayer vs AudioStreamPlayer2D/3D, AudioStreamRandomizer for variation, polyphony. |
| `adaptive-music` | Dynamic music: `AudioStreamSynchronized` for stems, transition timing to musical bars, `AudioStreamInteractive` state machine for combat/exploration music. |
| `sfx-patterns` | Sound effect patterns: pooled players, randomized pitch/volume, positional falloff tuning, impact sounds tied to physics collision magnitude. |

---

### Phase F — Godot Version Lock and API Reference

#### F1. Godot 4 Version Guard in every skill

Every SKILL.md that contains GDScript must include a version guard header:

```
> Target: Godot 4.4+ (GDScript 2.0). Do NOT use Godot 3 syntax.
> Key Godot 3 → 4 breaks: KinematicBody→CharacterBody3D, yield→await,
> move_and_slide(vel, UP)→velocity property + move_and_slide(),
> Spatial→Node3D, connect("s",self,"cb")→signal.connect(cb).
```

This header must be validated by the test suite (integration test checks for the guard string).

#### F2. Lazy-loaded API reference fragments

**What**: A `cookbook/api-ref/` directory of Godot 4.x class reference fragments, one file per class, loaded into context on demand.

**Inspired by**: godogen's approach of embedding 850+ class docs to prevent hallucinations.

**Initial set** (the classes most frequently hallucinated):
- `CharacterBody3D` — velocity, move_and_slide, is_on_floor
- `RigidBody3D` — apply_force, apply_impulse, freeze
- `Area3D` — body_entered, body_exited, monitoring
- `AnimationPlayer` — play, stop, is_playing, animation_finished
- `NavigationAgent3D` — target_position, get_next_path_position, distance_to_target
- `AudioStreamPlayer` — play, stop, bus, volume_db
- `Resource` — @export fields, save/load patterns
- `Signal` — connect, disconnect, emit, is_connected

**New skill**: `plugins/gdscript-guide/skills/api-lookup/SKILL.md` — How to use the cookbook API fragments to verify a method exists before writing code.

---

### Phase G — Autonomous Implementation Agent (Completing the Loop)

This phase creates the agent harness for gameplay implementation — analogous to the existing `agent/prompts-godot/coding_prompt.md` but targeting game features, not plugin development.

#### G1. `agent/prompts-game/` directory

Two new agent prompts:

**`implement_feature.md`** — The autonomous game feature implementer:
1. Read the current backlog (`plans/game-backlog.json`) and find the `in_progress` feature
2. Read the feature's spec (`plans/specs/<feature>.md`)
3. Verify baseline passes (all existing tests, gdlint, gdformat)
4. Plan the implementation (which files to create/modify — list them, do not start yet)
5. Implement: write GDScript files, create `.tscn` files, update autoloads
6. Run GdUnit4 tests; if any fail, fix them before proceeding
7. If GDAI MCP is available: run the specific scene, capture output, screenshot
8. Report result to designer: what was implemented, screenshot (if available), what to test
9. Mark feature `done` in backlog if designer approves, or add revision notes if not

**`iterate_on_feedback.md`** — The gameplay feedback integrator:
1. Read the designer's playtest debrief
2. Parse it into specific issues (feel, bug, performance, visual)
3. For each issue: identify the responsible file and function
4. Propose the change (do not implement yet — show designer the diff)
5. On designer approval: implement, run, verify, report

#### G2. `cookbook/hooks/game-session.md`

A hooks recipe for a full game development session:

- **Start hook**: Print current backlog status and the active feature
- **Stop hook**: Run full quality gate, print summary, ask if designer wants to commit progress
- **PreToolUse (Write)**: Check spec approval status before creating new files

---

## 4. Implementation Priority Order

| Priority | Item | Effort | Impact |
|----------|------|--------|--------|
| 1 | GDAI MCP cookbook recipe (A1) | Low | Critical — unlocks live feedback |
| 2 | GDScript LSP bridge recipe (A2) | Low | High — real-time diagnostics |
| 3 | `designer-brief` plugin (B1) | Medium | Critical — defines the collaboration model |
| 4 | `scene-builder` plugin (C1) | High | Critical — sole programmer gap |
| 5 | `game-backlog` plugin (B2) | Low | High — persistent feature tracking |
| 6 | `project-bootstrap` plugin (D1) | Medium | High — new game from zero |
| 7 | Godot 4 version guard in all skills (F1) | Low | High — prevents #1 failure mode |
| 8 | `godot-physics` plugin (E2) | Medium | High — most common gameplay bugs |
| 9 | Expanded `game-design` skills (E1) | Medium | Medium |
| 10 | `screenshot-review` skill (A3) | Low | Medium — depends on A1 |
| 11 | `game-session` hooks (G2) | Low | Medium |
| 12 | `implement_feature.md` agent (G1) | Medium | High — closes autonomous loop |
| 13 | API reference fragments (F2) | Medium | Medium |
| 14 | `godot-ui` plugin (E3) | Medium | Medium |
| 15 | `godot-audio` plugin (E4) | Low | Medium |
| 16 | Designer approval gate hook (B3) | Low | Medium |
| 17 | `iterate_on_feedback.md` agent (G1) | Low | High — depends on G1 agent |

---

## 5. New Directory Structure

```
godelian-assist/
├── plugins/
│   ├── godot-patterns/            # existing — add version guards
│   ├── gdscript-guide/            # existing — add api-lookup skill
│   ├── godot-code-quality/        # existing — add lsp-setup, screenshot-review
│   ├── game-design/               # existing — add combat, inventory, dialogue, enemy, progression
│   ├── designer-brief/            # NEW — brief, spec-review, iterate, playtest-debrief
│   ├── game-backlog/              # NEW — backlog-init, status, next-feature, add-feature
│   ├── scene-builder/             # NEW — create-scene, add-node, wire-signals, scene-from-brief
│   ├── project-bootstrap/         # NEW — new-project, configure-quality, setup-autoloads
│   ├── godot-physics/             # NEW — character-movement, collision-layers, area-detection
│   ├── godot-ui/                  # NEW — hud-design, menu-design, theme-system
│   ├── godot-audio/               # NEW — audio-architecture, adaptive-music, sfx-patterns
│   └── [existing general plugins unchanged]
├── agent/
│   ├── prompts-godot/             # existing (plugin development agent)
│   └── prompts-game/              # NEW — implement_feature.md, iterate_on_feedback.md
├── cookbook/
│   ├── claude-md/
│   │   └── godot.md               # existing — add MCP, LSP, designer-brief sections
│   ├── hooks/
│   │   ├── godot-quality.md       # existing
│   │   ├── designer-approval.md   # NEW
│   │   └── game-session.md        # NEW
│   ├── mcp/
│   │   ├── gdai-mcp.md            # NEW — full GDAI MCP setup
│   │   ├── godot-mcp-minimal.md   # NEW — lighter alternative
│   │   └── gdscript-lsp.md        # NEW — LSP bridge setup
│   └── api-ref/                   # NEW — per-class API fragments
│       ├── CharacterBody3D.md
│       ├── RigidBody3D.md
│       └── [8+ classes]
└── plans/
    ├── game-backlog.json           # per-game (not in this repo — in game project)
    └── specs/                     # per-feature specs (not in this repo — in game project)
```

---

## 6. Success Criteria

The proposal is complete when these end-to-end flows work without the user touching GDScript or the Godot editor:

### Flow 1: New feature from brief
1. Designer: "I want the player to be able to dash forward, with a 0.5s cooldown and a dust particle effect"
2. Claude: Outputs spec — `PlayerDash` component node, `dash_ready` signal, `DashTrail` particle scene, `PlayerStats` resource field for dash distance
3. Designer: "Approved, make the cooldown configurable in the Inspector"
4. Claude: Creates `player_dash.gd`, `player_dash.tscn`, updates `player.tscn`, runs GdUnit4 tests, runs the scene, screenshots
5. Claude: "Feature implemented. Screenshot shows the dash particle. Cooldown is @export. Tests passing."
6. Designer: Reviews screenshot, approves, Claude marks feature done and commits

### Flow 2: Playtest feedback integration
1. Designer: "The dash feels sluggish, it should be instant. Also the particle stays on after the dash ends."
2. Claude: Reads `player_dash.gd`, identifies `tween.tween_property` duration, proposes changing it to 0.08s; reads `player_dash.tscn`, finds particle node, proposes setting `one_shot = true`
3. Designer: "Yes to both"
4. Claude: Makes both changes, runs game, screenshots, reports

### Flow 3: New project from zero
1. Designer: "Start a 2D platformer project called 'echo-drift'"
2. Claude: Creates directory structure, `project.godot` with text format + static typing, canonical autoloads (`EventBus`, `GameManager`, `SaveManager`), initial `CLAUDE.md`, empty `plans/game-backlog.json`
3. Claude: Reports project is ready, asks for first feature brief

---

## 7. Feature List Entries (next `feature_list.json` additions)

These map the proposal to the autonomous agent format:

```
Phase: godot-p4 (infrastructure)
- A1: cookbook/mcp/gdai-mcp.md + cookbook/mcp/godot-mcp-minimal.md
- A2: cookbook/mcp/gdscript-lsp.md + lsp-setup skill
- A3: screenshot-review skill in godot-code-quality
- F1: Godot 4 version guard added to all existing GDScript SKILL.md files (verified by test)

Phase: godot-p5 (designer workflow)
- B1a: designer-brief plugin — brief + spec-review skills
- B1b: designer-brief plugin — iterate + playtest-debrief + feature-complete skills
- B2: game-backlog plugin — all 4 skills
- B3: designer-approval hook recipe

Phase: godot-p6 (scene builder)
- C1a: scene-builder plugin — create-scene + add-node skills
- C1b: scene-builder plugin — wire-signals + scene-from-brief + scene-audit skills

Phase: godot-p7 (project bootstrap)
- D1: project-bootstrap plugin — all 4 skills

Phase: godot-p8 (game system coverage)
- E1: expanded game-design skills (combat, inventory, dialogue, enemy, progression)
- E2: godot-physics plugin — all 5 skills
- E3: godot-ui plugin — all 4 skills
- E4: godot-audio plugin — all 3 skills

Phase: godot-p9 (autonomous agent)
- F2: cookbook/api-ref/ — 8 class reference fragments + api-lookup skill
- G1: agent/prompts-game/implement_feature.md
- G2: agent/prompts-game/iterate_on_feedback.md + game-session hooks
```

---

## 8. What This Proposal Does NOT Include

Deliberate exclusions to stay focused:

- **Asset generation** (images, models, audio): Out of scope. Claude Code is a programmer, not an artist. The designer provides assets; Claude integrates them.
- **Godot export/publishing**: Out of scope for the programmer role.
- **Multiplayer/networking**: Deferred to a later proposal — high complexity, niche use case.
- **C# as primary language**: GDScript is the default. The existing `gdscript-to-csharp` skill handles conversion when needed.
- **In-editor plugin for Godot**: godelian-assist remains a Claude Code plugin, not a Godot editor plugin. The GDAI MCP cookbook recipe handles the editor integration layer.
- **Visual scripting**: Not supported by the AI-assistance model.
