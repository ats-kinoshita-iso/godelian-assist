# Implementation Plan: godelian-assist v2 — Complete Godot Developer

**Created**: 2026-03-26
**Status**: Active
**Reference**: PROPOSAL.md (in repo root)
**Feature ID range**: 13–58 (append to feature_list.json)

---

## How to Use This Plan

1. This document is the authoritative breakdown of PROPOSAL.md into agent-executable features.
2. Each phase begins with a **Research Gate** — tasks that must be completed and documented before any code is written for that phase. Research findings go into `plans/research/`.
3. Implementation uses the same coding agent loop as Phase 1–3: read `feature_list.json`, implement next feature, run tests, mark passing.
4. Each phase ends with a **Validation Gate** — run `validation_prompt.md` against all features in the phase before starting the next.
5. Phases A → B → C → D are strictly sequential (each depends on the prior). Phase E, F, G can overlap with D once C is complete.

---

## Dependency Graph

```
A (Live Feedback) ──► B (Designer Workflow) ──► C (Scene Builder) ──► D (Bootstrap)
                                                                            │
                                     E (Game Systems) ◄───────────────────┤
                                     F (Version Guard + API Ref) ◄─────────┤
                                     G (Game Agent) ◄────────────────────────┘
                                     (E, F, G can run in parallel after D)
```

**Hard dependencies:**
- B requires A to be installed and tested (agent approval gate needs MCP to be real)
- C requires the `.tscn` format research (C.0) to produce correct output
- G requires B (backlog/spec format) and C (scene creation) to be complete

---

## Phase A: Live Feedback Infrastructure

**Goal**: Claude can run a Godot game, read debug output, and (when GDAI MCP is active) take a screenshot. These capabilities underpin every subsequent phase.

### A.0 — Research Gate (complete before any A.1+ work)

**Researcher reads and documents findings in `plans/research/phase-a-mcp.md`:**

1. **GDAI MCP installation on Windows 11**
   - Install `gdaimcp` npm package: `npm install -g gdaimcp` (verify exact package name)
   - Install the Godot plugin from the GDAI MCP site
   - Verify WebSocket connection between Claude Code and Godot editor
   - Document: exact `settings.json` MCP entry (name, command, args, env)
   - Document: which Godot plugin version is required (min Godot 4.x version)
   - Test: does `run_project` work headless? Does it require the editor open?

2. **godot-mcp minimal (Coding-Solo/godot-mcp)**
   - Install: `npm install -g godot-mcp`
   - Document: `settings.json` entry
   - Document: available tools (run_project, get_debug_output, list_projects)
   - Test: which tool captures stderr/stdout from Godot?

3. **GDScript LSP bridge**
   - Install `twaananen/claude-code-gdscript` or `Sods2/claude-code-gdscript-lsp`
   - Verify: `godot --lsp-port 6005` flag exists in Godot 4.6.1
   - Document: MCP config entry
   - Test: in a `.gd` file with a type error, does Claude Code see the diagnostic?

4. **Screenshot capability**
   - In GDAI MCP: what is the exact tool name for screenshots? (`capture_screenshot`? `take_screenshot`?)
   - What is the return format? (file path? base64 data URI?)
   - Does it capture the game viewport, the editor viewport, or both?
   - Test on Windows: are there display/path issues?

5. **Document findings** in `plans/research/phase-a-mcp.md` with exact commands and config snippets before proceeding.

**Gate**: Phase A implementation begins only when `plans/research/phase-a-mcp.md` exists and contains working config for at least one MCP server and the LSP bridge.

---

### A.1 — Feature 13: GDAI MCP Cookbook Recipe

**File**: `cookbook/mcp/gdai-mcp.md`

**Must contain:**
- One-line overview of GDAI MCP (what it does, why it's powerful)
- Prerequisites: Node.js, npm, Godot 4.x with text editor running
- Step-by-step installation: npm install command, Godot plugin install
- The exact `.claude/settings.json` MCP block (copy-paste ready)
- Available tool categories (scene tools, script tools, screenshot, debug output)
- A "first use" workflow: open Godot editor → run `/mcp status` → run a scene → capture output
- Windows-specific notes (path separators, PowerShell vs bash)
- Troubleshooting: WebSocket not connecting, port in use, Godot not found

**Verification:**
1. `cookbook/mcp/gdai-mcp.md` exists and is ≥ 40 lines
2. Contains a fenced JSON block with the `settings.json` MCP config
3. Mentions `capture_screenshot` (or the correct tool name from research)
4. `uv run pytest tests/ -v` — all pass

---

### A.2 — Feature 14: Minimal godot-mcp Cookbook Recipe

**File**: `cookbook/mcp/godot-mcp-minimal.md`

**Must contain:**
- When to use this instead of GDAI MCP (lighter, no editor plugin needed)
- npm install command
- `settings.json` MCP block
- Available tools (run_project, get_debug_output)
- Comparison table: godot-mcp vs GDAI MCP (capabilities, setup complexity)

**Verification:**
1. File exists ≥ 25 lines
2. Contains npm install command and JSON config block
3. Contains comparison table
4. All tests pass

---

### A.3 — Feature 15: GDScript LSP Bridge Cookbook Recipe

**File**: `cookbook/mcp/gdscript-lsp.md`

**Must contain:**
- What the LSP bridge provides (diagnostics, hover, go-to-definition in `.gd` files)
- How to start Godot's LSP server: `godot --lsp-port 6005 --headless`
- Install and config for the chosen bridge (from research)
- `settings.json` MCP block
- How to verify it's working (example: make a type error, see it in Claude Code)
- Limitation note: requires a running Godot instance

**Verification:**
1. File exists ≥ 30 lines
2. Contains `--lsp-port` in the guide
3. Contains `settings.json` config block
4. All tests pass

---

### A.4 — Feature 16: lsp-setup Skill

**File**: `plugins/godot-code-quality/skills/lsp-setup/SKILL.md`

**Must contain (≥ 15 body lines):**
- What the LSP setup gives Claude Code (real-time GDScript error detection)
- The three-component architecture: Godot editor → TCP LSP → bridge → Claude Code stdio
- Step-by-step setup referencing `cookbook/mcp/gdscript-lsp.md`
- How to test: write a script with a known type error, verify Claude sees it
- What errors the LSP catches that gdlint doesn't (and vice versa)
- How to restart if the bridge drops connection

**Verification:**
1. SKILL.md exists with valid YAML frontmatter
2. Body ≥ 15 non-blank lines
3. Mentions `--lsp-port` and the TCP/stdio bridge
4. All tests pass

---

### A.5 — Feature 17: screenshot-review Skill

**File**: `plugins/godot-code-quality/skills/screenshot-review/SKILL.md`

**Must contain (≥ 15 body lines):**
- When to use screenshot review (after scene changes, after physics implementation, after UI work)
- Prerequisites: GDAI MCP active and Godot editor/game running
- The review workflow: run scene → request screenshot → analyze → compare to design intent
- What to look for: node placement, collision shape visibility (in debug mode), UI layout, particle effects
- How to describe discrepancies back to the designer
- What screenshot review cannot catch (logic bugs, audio, feel) — use debug output instead
- The combined loop: screenshot + debug output + gdlint = full verification

**Verification:**
1. SKILL.md exists with valid YAML frontmatter
2. Body ≥ 15 non-blank lines
3. Mentions "screenshot" and "design intent" and "debug output"
4. Mentions GDAI MCP or the screenshot tool name
5. All tests pass

---

### A.testing — Feature 18: Phase A Integration Tests

**File**: `tests/plugins/test_godot_code_quality_phase_a.py`

**Must include (≥ 6 test functions):**
- `test_lsp_setup_skill_exists`
- `test_lsp_setup_skill_body_depth` (≥ 15 lines)
- `test_lsp_setup_mentions_lsp_port`
- `test_screenshot_review_skill_exists`
- `test_screenshot_review_skill_body_depth`
- `test_screenshot_review_mentions_design_intent`

**Cookbook tests** — `tests/cookbook/test_mcp_recipes.py`:
- `test_gdai_mcp_recipe_exists`
- `test_gdai_mcp_recipe_has_settings_json_block`
- `test_gdscript_lsp_recipe_exists`
- `test_gdscript_lsp_recipe_mentions_lsp_port`

**Verification**: `uv run pytest tests/ -v` — all pass, including new tests

---

### A.done — Phase A Definition of Done

- [ ] `cookbook/mcp/gdai-mcp.md` — copy-paste ready, Windows-tested config
- [ ] `cookbook/mcp/godot-mcp-minimal.md` — comparison table, npm install
- [ ] `cookbook/mcp/gdscript-lsp.md` — working LSP bridge config
- [ ] `plugins/godot-code-quality/skills/lsp-setup/SKILL.md` — 15+ body lines
- [ ] `plugins/godot-code-quality/skills/screenshot-review/SKILL.md` — 15+ body lines
- [ ] Integration tests added and passing
- [ ] `plans/research/phase-a-mcp.md` — research findings documented
- [ ] Validation agent run (`validation_prompt.md`) — VALIDATION: PASS

---

## Phase B: Designer-Programmer Workflow

**Goal**: Formal, enforced workflow for designer → spec → implementation → review. The user never has to describe what they want twice; Claude never implements without approval.

### B.0 — Research Gate

**Researcher documents findings in `plans/research/phase-b-workflow.md`:**

1. **Brief format design**
   - What is the minimum viable brief? (one sentence? a template?)
   - What fields are mandatory vs. optional? Proposed: title, intent, feel, constraints, out-of-scope
   - Should briefs be free-form prose or structured YAML? Decision: structured Markdown with a defined heading hierarchy
   - Example brief for "player dash with cooldown" — write it out fully

2. **Spec format design**
   - What does an approved spec contain? Proposed sections:
     - Summary (one sentence)
     - Node structure (scene tree diagram)
     - Signals (name, parameters, who emits, who connects)
     - Resources (custom Resource subclasses, fields)
     - GDScript skeletons (typed, with TODOs)
     - Files to create (exact paths)
     - Files to modify (exact paths + what changes)
     - Test plan (what GdUnit4 tests to write)
   - Format: Markdown file in `plans/specs/<feature-slug>.md`

3. **Approval gate hook design**
   - PreToolUse fires on `Write` and `Edit` tool calls
   - Check: does the file being written have an associated spec in `plans/specs/`?
   - How to associate? Convention: spec filename matches `src/` path convention
   - Alternative: the gate checks for a `plans/specs/ACTIVE_SPEC.md` symlink/file
   - Decision: gate checks for `plans/specs/ACTIVE_SPEC.md` — simpler, unambiguous
   - What does the gate do when no spec exists? Print a warning (not a hard block — agent can override)

4. **Game backlog schema design**
   - Extend the existing `feature_list.json` pattern or separate file?
   - Decision: separate `plans/game-backlog.json` in the game project (not in godelian-assist itself)
   - Schema v1 definition (write it out fully in research doc)

5. **Document in `plans/research/phase-b-workflow.md`** with all format decisions.

---

### B.1 — Feature 19: designer-brief Plugin (brief + spec-review)

**New plugin**: `plugins/designer-brief/`

**plugin.json** fields:
```json
{
  "name": "designer-brief",
  "description": "Formal designer → programmer handoff: brief, spec, approval, iterate.",
  "version": "1.0.0",
  "license": "MIT",
  "keywords": ["godot", "workflow", "designer", "spec", "game-design"]
}
```

**Skill: `brief`** (`plugins/designer-brief/skills/brief/SKILL.md`)

Must contain (≥ 20 body lines):
- Purpose: translate designer intent into a concrete implementation spec before touching code
- The brief template (exact Markdown structure with headings):
  ```
  ## Feature: <title>
  **Intent**: one sentence — what the mechanic does and why it exists in the game
  **Feel**: how it should feel to the player (visceral words: snappy, floaty, punchy, weighty)
  **Constraints**: hard limits (max nodes, performance budget, must reuse X)
  **Out of scope**: what this feature deliberately does NOT do
  **Designer acceptance**: I will approve this feature when ___
  ```
- How Claude responds to a brief: reads it, asks clarifying questions, then produces a spec
- The spec sections Claude must populate (from research doc)
- The approval handshake: Claude writes spec to `plans/specs/<slug>.md`, sets `plans/specs/ACTIVE_SPEC.md`, designer reviews
- Rule: no files are created until the designer explicitly says "approved" or "proceed"

**Skill: `spec-review`** (`plugins/designer-brief/skills/spec-review/SKILL.md`)

Must contain (≥ 15 body lines):
- How the designer reviews a spec: read `plans/specs/<slug>.md`, focus on node structure and signal map
- Three review outcomes: Approved (proceed), Revised (Claude updates spec and re-presents), Rejected (restart with new brief)
- What "Approved" triggers: Claude writes `ACTIVE_SPEC.md`, begins implementation
- How to revise: designer marks specific sections with `[REVISE: ...]` inline comments
- Common revision patterns: wrong node type, missing signal, scope creep caught early

**Verification:**
1. Both SKILL.md files exist with valid frontmatter
2. `brief` body ≥ 20 lines; `spec-review` body ≥ 15 lines
3. `brief` contains the brief template (all 5 heading fields)
4. `spec-review` mentions `ACTIVE_SPEC.md`
5. All tests pass

---

### B.2 — Feature 20: designer-brief Plugin (iterate + playtest-debrief + feature-complete)

**Skill: `iterate`** (`plugins/designer-brief/skills/iterate/SKILL.md`)

Must contain (≥ 15 body lines):
- When to use `iterate` vs. starting a new brief (it's an iteration when the system exists and needs tuning, not redesign)
- The iteration request format: describe what felt wrong, when it happens, what you expected
- How Claude responds: finds the responsible code, proposes the minimal diff, waits for approval
- Rule: never redesign in an iteration — scope to the specific complaint
- Example: "dash feels sluggish" → Claude finds tween duration → proposes changing 0.3 → 0.08

**Skill: `playtest-debrief`** (`plugins/designer-brief/skills/playtest-debrief/SKILL.md`)

Must contain (≥ 15 body lines):
- The debrief template:
  ```
  ## Playtest: <session date/description>
  **What worked** (keep these)
  **What felt wrong** (ranked: critical / medium / low)
  **Bugs observed** (exact reproduction steps)
  **Open questions** (design decisions not yet made)
  ```
- How Claude processes a debrief: sorts by severity, maps each item to a file/function, produces an ordered task list
- How the task list feeds back into the game backlog
- Rule: designer must rank issues before Claude prioritizes — Claude does not reorder the designer's priorities

**Skill: `feature-complete`** (`plugins/designer-brief/skills/feature-complete/SKILL.md`)

Must contain (≥ 12 body lines):
- What "feature complete" means: designer has approved the feel, all tests pass, quality gate passes
- The completion checklist Claude runs: gdlint, gdformat, GdUnit4, screenshot review
- How to mark complete: `uv run python tools/mark_passing.py <id>` for game features (or the game backlog equivalent)
- What to clean up: remove `ACTIVE_SPEC.md`, move spec to `plans/specs/done/`, commit

**Verification:**
1. All three SKILL.md files exist with valid frontmatter
2. Each body ≥ 12 lines
3. `iterate` mentions "minimal diff"
4. `playtest-debrief` contains the debrief template headings
5. `feature-complete` mentions gdlint and GdUnit4
6. All tests pass

---

### B.3 — Feature 21: Approval Gate Hook (hooks.json)

**File**: `plugins/designer-brief/hooks/hooks.json`

**Hook design**:
```json
{
  "hooks": [
    {
      "event": "PreToolUse",
      "command": "python plans/check_spec.py",
      "matcher": { "tool_name": ["Write", "Edit"], "file_pattern": "*.gd|*.tscn|*.tres" }
    }
  ]
}
```

The hook script `plans/check_spec.py` (template, to be created in the game project):
- Checks for `plans/specs/ACTIVE_SPEC.md`
- If missing: prints a warning message explaining what spec approval means
- Returns exit 0 always (warning, not block) — the agent can proceed but must acknowledge

**File**: `cookbook/hooks/designer-approval.md`

Must contain (≥ 20 lines):
- Explanation of the approval gate concept
- Copy-paste `hooks.json` entry
- The `check_spec.py` script (full, ready to drop into any game project's `plans/` directory)
- How to temporarily bypass during rapid prototyping (delete ACTIVE_SPEC.md check)
- How to integrate with game-backlog: spec is created automatically when a feature moves to `in_progress`

**Verification:**
1. `hooks.json` exists and is valid JSON with a PreToolUse entry
2. `cookbook/hooks/designer-approval.md` exists ≥ 20 lines
3. Contains the complete `check_spec.py` script
4. All tests pass

---

### B.4 — Feature 22: game-backlog Plugin (backlog-init + backlog-status)

**New plugin**: `plugins/game-backlog/`

**Skill: `backlog-init`** — Initialize `plans/game-backlog.json` from designer's initial game description

Must contain (≥ 15 body lines):
- The game-backlog schema v1:
  ```json
  {
    "game_title": "string",
    "genre": "string",
    "version": "1.0",
    "features": [
      {
        "id": 1,
        "title": "string",
        "brief": "one-sentence description",
        "status": "queued|in_progress|pending_approval|done",
        "priority": 1,
        "spec": "plans/specs/<slug>.md or null",
        "notes": "string or null"
      }
    ]
  }
  ```
- How to extract features from a GDD (Game Design Document) or a designer's free-form description
- The initial ordering: Claude should ask the designer to confirm priority before writing the file
- Where the file lives: `plans/game-backlog.json` in the game project root

**Skill: `backlog-status`** — Show current feature board

Must contain (≥ 12 body lines):
- How to display the backlog in a readable table format (Markdown table output)
- Status column meanings: queued (not started), in_progress (Claude is working), pending_approval (spec awaiting review), done
- How to identify the "current sprint" (in_progress features)
- Rule: only one feature should be `in_progress` at a time

**Verification:**
1. Both SKILL.md files exist with valid frontmatter
2. `backlog-init` body ≥ 15 lines and contains the full JSON schema
3. `backlog-status` body ≥ 12 lines
4. All tests pass

---

### B.5 — Feature 23: game-backlog Plugin (next-feature + add-feature)

**Skill: `next-feature`** — Advance backlog: pop next queued feature, generate its brief

Must contain (≥ 12 body lines):
- How to select the next feature: highest priority `queued` item
- What Claude does automatically: reads the feature's `brief`, generates a full brief using the `designer-brief/brief` skill format, writes to `plans/specs/<slug>.md`
- Sets feature status to `pending_approval`
- Outputs: the spec for designer review before proceeding

**Skill: `add-feature`** — Designer adds a new feature mid-session

Must contain (≥ 10 body lines):
- Input format: designer provides title, brief (one sentence), priority (1-5)
- Where it gets inserted in the backlog (by priority rank)
- How to handle priority conflicts (ask designer)
- When to use this vs. creating a new playtest-debrief entry

**Verification:**
1. Both SKILL.md files exist with valid frontmatter
2. `next-feature` body ≥ 12 lines, mentions `pending_approval`
3. `add-feature` body ≥ 10 lines, mentions priority
4. All tests pass

---

### B.6 — Feature 24: game-session Hook Recipe

**File**: `cookbook/hooks/game-session.md`

Must contain (≥ 25 lines):
- The full `hooks.json` block for a game development session:
  - **Start hook** (`PostToolUse` on session start or first tool use): print backlog status
  - **Stop hook**: run quality gate summary, print which features changed this session, prompt for commit
- Copy-paste `settings.json` additions for the hooks
- How to combine with the designer-approval hook (they stack)
- Session discipline rules for the CLAUDE.md section:
  - Start each session with `/backlog-status`
  - End each session with `/feature-complete` or a clear "where we left off" note
  - Never start a new feature if the current one is `pending_approval`

**Verification:**
1. File exists ≥ 25 lines
2. Contains a complete fenced JSON hooks block
3. Mentions both Start and Stop events
4. All tests pass

---

### B.testing — Feature 25: Phase B Integration Tests

**File**: `tests/plugins/test_designer_brief_integration.py` (≥ 8 test functions)
- `test_plugin_json_valid`
- `test_all_skills_exist` (brief, spec-review, iterate, playtest-debrief, feature-complete)
- `test_brief_skill_body_depth`
- `test_brief_skill_contains_template_headings` (Intent, Feel, Constraints)
- `test_spec_review_mentions_active_spec`
- `test_iterate_mentions_minimal_diff`
- `test_playtest_debrief_contains_template`
- `test_hooks_json_valid_json` and `test_hooks_json_has_pretooluse`

**File**: `tests/plugins/test_game_backlog_integration.py` (≥ 6 test functions)
- `test_plugin_json_valid`
- `test_all_skills_exist` (backlog-init, backlog-status, next-feature, add-feature)
- `test_backlog_init_contains_schema`
- `test_backlog_status_mentions_in_progress`
- `test_next_feature_mentions_pending_approval`
- `test_add_feature_mentions_priority`

**Verification**: `uv run pytest tests/ -v` — all pass

---

### B.done — Phase B Definition of Done

- [ ] `plugins/designer-brief/` — 5 skills, hooks.json, README.md
- [ ] `plugins/game-backlog/` — 4 skills, README.md
- [ ] `cookbook/hooks/designer-approval.md` — complete with check_spec.py
- [ ] `cookbook/hooks/game-session.md` — complete with hooks.json
- [ ] Integration tests: ≥ 14 total new test functions, all passing
- [ ] `plans/research/phase-b-workflow.md` — design decisions documented
- [ ] Validation agent: VALIDATION: PASS

---

## Phase C: Scene Builder

**Goal**: Claude can create and modify `.tscn` files directly — no editor required. This is the most technically demanding phase and the single biggest gap in the "sole programmer" model.

### C.0 — Research Gate (most critical gate in the project)

**Researcher documents findings in `plans/research/phase-c-tscn-format.md`:**

1. **Read the official .tscn format spec**
   - Source: `https://docs.godotengine.org/en/4.4/contributing/development/file_formats/tscn.html`
   - Document: the exact header format, all section types, property encoding

2. **UID format**
   - What is a valid UID? (e.g., `uid://abc123xyz` — what character set? what length?)
   - Are UIDs required? What happens in Godot if a scene has no UID?
   - Can Claude generate a valid UID without running Godot? (Random base62? Hash of path?)
   - Test: create a `.tscn` with a hand-written UID — does Godot accept it?

3. **Resource ID format**
   - ext_resource IDs: format `"1_HASH"` — what is HASH? Random? Based on path?
   - sub_resource IDs: same format
   - Are IDs stable across edits? (Does Godot re-generate them on save?)
   - Test: create a .tscn with simple sequential IDs like `"1_aaa"`, `"2_bbb"` — does Godot accept?

4. **load_steps calculation**
   - Rule: `load_steps = 1 + count(ext_resource) + count(sub_resource)`
   - Test: create a scene with wrong load_steps — does Godot error or silently correct?
   - If silently corrected: load_steps doesn't matter for correctness → just use `load_steps=2` and note this

5. **Signal connections in .tscn**
   - What is the exact syntax for the `[connection]` section?
   - Format: `[connection signal="signal_name" from="NodePath" to="NodePath" method="_on_method"]`
   - Test: hand-write a signal connection in .tscn — does it work in Godot?

6. **Sub-resource syntax**
   - CapsuleShape3D, BoxShape3D, SphereShape3D — what are their property names?
   - How are nested resources handled (a material inside a MeshInstance3D)?

7. **Validation via headless Godot**
   - Does `godot --headless --check-only -s <script.gd>` also validate .tscn syntax?
   - Is there a way to validate a .tscn without opening the editor? (`godot --headless --import`?)
   - If no headless validation: document this limitation explicitly

8. **Create a hand-crafted .tscn test file** and verify it opens correctly in Godot 4.6.1
   - Minimum: Player (CharacterBody3D) with CollisionShape3D (CapsuleShape3D) and a script
   - Add one signal connection
   - Save to `plans/research/test_generated_scene.tscn`

9. **Document all findings in `plans/research/phase-c-tscn-format.md`** before any implementation.

**Gate**: The `test_generated_scene.tscn` must open without errors in Godot 4.6.1 before Phase C implementation begins.

---

### C.1 — Feature 26: .tscn Format Reference

**File**: `cookbook/api-ref/tscn-format.md`

This is the canonical reference Claude loads when generating `.tscn` files. It is not a skill — it is a reference document.

Must contain (≥ 60 lines):
- Complete annotated example of a minimal valid `.tscn` (CharacterBody3D + CollisionShape3D + script)
- UID generation rule (from research: random base62 string of N chars, prefixed with `uid://`)
- Resource ID generation rule (sequential + short random suffix: `"1_abc"`, `"2_def"`)
- load_steps formula (or note that Godot corrects it)
- Complete list of common node types and their required child nodes (CharacterBody3D → CollisionShape3D, MeshInstance3D; Area3D → CollisionShape3D)
- Signal connection syntax with example
- sub_resource syntax for the 5 most common shapes (Capsule, Box, Sphere, Cylinder, Concave)
- ext_resource patterns (Script, PackedScene, Texture2D, AudioStream)
- The `format=3` requirement (Godot 4 text format)
- Common mistakes: wrong format number, missing CollisionShape, wrong parent path

**Verification:**
1. File exists ≥ 60 lines
2. Contains a complete `.tscn` example in a fenced code block
3. Contains `uid://` format documentation
4. Contains signal connection syntax
5. All tests pass

---

### C.2 — Feature 27: scene-builder Plugin (create-scene)

**New plugin**: `plugins/scene-builder/`

**Skill: `create-scene`** — Generate a complete valid `.tscn` file from a node spec

Must contain (≥ 25 body lines):
- When to use this skill: any time a new scene is needed (player, enemy, item, UI panel, level)
- The input spec format Claude expects from the designer (or generates from a brief):
  ```
  Root: Player (CharacterBody3D)
  ├── CollisionShape3D  [CapsuleShape: radius=0.4, height=1.8]
  ├── MeshInstance3D    [placeholder capsule mesh]
  ├── Head (Node3D)
  │   └── Camera3D
  └── HealthComponent (Node)
  Script: res://src/player/player.gd
  Signals to connect: [none — signals connected at runtime via EventBus]
  ```
- The generation algorithm (step by step):
  1. Count ext_resource entries (scripts, sub-scenes); assign sequential IDs
  2. Count sub_resource entries (shapes, materials); assign sequential IDs
  3. Generate UID: `uid://` + 10 random alphanumeric chars
  4. Set `load_steps = 1 + len(ext_resource) + len(sub_resource)`
  5. Write header
  6. Write ext_resource sections
  7. Write sub_resource sections
  8. Write root node
  9. Write child nodes (each with `parent="."` or nested path)
- The mandatory child rule: every CharacterBody3D, RigidBody3D, Area3D MUST have a CollisionShape3D child
- How to verify: `godot --headless --import res://path/to/scene.tscn` or visual check in editor
- Full worked example: the Player scene from above, fully rendered as `.tscn` text

**Verification:**
1. SKILL.md exists with valid frontmatter
2. Body ≥ 25 non-blank lines
3. Contains a complete `.tscn` output example in a fenced code block
4. Mentions UID generation
5. Mentions the CollisionShape3D mandatory child rule
6. All tests pass

---

### C.3 — Feature 28: scene-builder Plugin (add-node + wire-signals)

**Skill: `add-node`** — Add nodes to an existing `.tscn` without breaking existing paths

Must contain (≥ 18 body lines):
- Input: path to existing .tscn, node spec (type, parent, name, properties)
- The read-then-write pattern: always read the full file first, locate the parent node section, insert after
- Path preservation: node names in Godot are global within the scene; changing a name breaks all `get_node()` calls that reference it — never rename, only add
- How to update `load_steps` after adding sub_resources
- How to add a node to the root (parent=".") vs. a nested node (parent="Head")
- The null-safety check: verify the parent node exists in the .tscn before inserting
- Example: add an `AudioStreamPlayer3D` named "FootstepAudio" to the Player scene

**Skill: `wire-signals`** — Add signal connections to an existing `.tscn`

Must contain (≥ 15 body lines):
- The `[connection]` section syntax: `signal`, `from`, `to`, `method`, optional `flags`
- Validation steps before writing: verify source node path exists, verify signal name exists on that node type, verify target node path exists, verify target method name in the script
- When to use .tscn connections vs. `signal.connect()` in `_ready()`: .tscn for static/always-on connections; code for conditional or runtime connections
- Example: connect `HealthComponent`'s `health_changed` signal to the HUD's `_on_health_changed` method
- Common error: connecting from the wrong node path (use node NAME, not type)

**Verification:**
1. Both SKILL.md files exist with valid frontmatter
2. `add-node` body ≥ 18 lines, mentions path preservation
3. `wire-signals` body ≥ 15 lines, contains `[connection]` syntax example
4. All tests pass

---

### C.4 — Feature 29: scene-builder Plugin (scene-from-brief + scene-audit)

**Skill: `scene-from-brief`** — Most powerful skill: generate .tscn + all .gd scripts from a designer brief in one operation

Must contain (≥ 20 body lines):
- Input: the approved spec from `plans/specs/ACTIVE_SPEC.md`
- The generation order:
  1. Generate all `.gd` script skeletons (typed, with `class_name`, signals, @export vars)
  2. Generate the `.tscn` using `create-scene` patterns (scripts as ext_resources)
  3. Generate `.tres` resource files if the spec includes custom Resources
  4. Write all files
  5. Run `gdlint` on all generated .gd files
  6. Run `godot --headless --check-only -s <root_script.gd>` for type validation
- The mandatory typing pass: before writing any .gd, verify every var, param, and return type is annotated
- How to handle missing designer decisions (e.g., "what are the export properties?"): Claude invents reasonable defaults and documents them with `# DESIGNER: adjust this value`
- Full example: generate Player scene from the fps-controller brief

**Skill: `scene-audit`** — Read an existing .tscn and report problems

Must contain (≥ 15 body lines):
- What to check: orphaned scripts (script path doesn't exist), missing CollisionShape3D on physics bodies, nodes with untyped scripts, disconnected signals (signal exists in code but not in .tscn connections), misnamed nodes (name doesn't match class convention)
- Output format: structured report with ISSUE / SEVERITY / FIX for each problem
- How to use audit as a pre-commit check: add to the PreToolUse hook chain

**Verification:**
1. Both SKILL.md files exist with valid frontmatter
2. `scene-from-brief` body ≥ 20 lines, contains generation order steps
3. `scene-from-brief` mentions `ACTIVE_SPEC.md`
4. `scene-audit` body ≥ 15 lines, mentions orphaned scripts and CollisionShape3D
5. All tests pass

---

### C.testing — Feature 30: Phase C Integration Tests

**File**: `tests/plugins/test_scene_builder_integration.py` (≥ 10 test functions)

- `test_plugin_json_valid`
- `test_all_skills_exist` (create-scene, add-node, wire-signals, scene-from-brief, scene-audit)
- `test_create_scene_body_depth` (≥ 25 lines)
- `test_create_scene_has_tscn_example` (contains `[gd_scene`)
- `test_create_scene_mentions_uid`
- `test_create_scene_mentions_collision_rule`
- `test_add_node_mentions_path_preservation`
- `test_wire_signals_has_connection_syntax` (contains `[connection`)
- `test_scene_from_brief_mentions_active_spec`
- `test_scene_audit_mentions_orphaned_scripts`

**File**: `tests/cookbook/test_api_refs.py` (≥ 4 test functions)
- `test_tscn_format_ref_exists`
- `test_tscn_format_ref_has_uid_section`
- `test_tscn_format_ref_has_connection_section`
- `test_tscn_format_ref_has_example`

**Verification**: `uv run pytest tests/ -v` — all pass

---

### C.done — Phase C Definition of Done

- [ ] `cookbook/api-ref/tscn-format.md` — 60+ lines, working .tscn example verified in Godot 4.6.1
- [ ] `plugins/scene-builder/` — 5 skills, README.md, plugin.json
- [ ] A hand-generated test scene (`plans/research/test_generated_scene.tscn`) that opens in Godot
- [ ] Integration tests ≥ 14 new test functions, all passing
- [ ] `plans/research/phase-c-tscn-format.md` — UID format, ID format, load_steps, connections documented
- [ ] Validation agent: VALIDATION: PASS

---

## Phase D: Project Bootstrap

**Goal**: Claude can create a complete, correctly-configured Godot project from zero. The designer provides a one-sentence concept; Claude delivers a runnable project structure with all quality tooling pre-configured.

### D.0 — Research Gate

**Document findings in `plans/research/phase-d-bootstrap.md`:**

1. **project.godot settings for text format**
   - Exact setting key: `application/config/use_binary_format`? Test with Godot 4.6.1
   - Where does this go in `[application]` section?
   - Does Godot 4.6.1 have a project-wide "enforce static typing" setting, or only per-script?
   - What GDScript warning level settings exist? (`[gdscript]` section keys)

2. **Headless project creation**
   - Can `godot --headless --path /new/path --quit` create a project.godot?
   - Or does project.godot need to be hand-written?
   - What is the minimum content for a valid project.godot (just `[application]` section? config_version required?)
   - Test: write a minimal project.godot by hand, open in Godot 4.6.1 — does it work?

3. **gdlintrc format**
   - What is `.gdlintrc` format? YAML? JSON? INI?
   - What rules does godelian-assist's style require? (line_length, max_file_lines, etc.)
   - Document a complete `.gdlintrc` for the project conventions in CLAUDE.md

4. **Canonical autoload scripts**
   - What does the minimal `EventBus.gd` look like? (just a Node with typed signal declarations?)
   - What does the minimal `GameManager.gd` look like? (scene transitions, pause toggle)
   - What does the minimal `SaveManager.gd` look like? (ConfigFile-based facade)
   - Write these three scripts fully typed in the research doc

5. **Directory structure canonical form**
   - What goes in `src/`? (GDScript source by system: `src/player/`, `src/enemies/`, `src/ui/`)
   - What goes in `scenes/`? (`.tscn` files, mirroring `src/` structure)
   - What goes in `data/`? (`.tres` resource files)
   - What goes in `assets/`? (`sounds/`, `textures/`, `models/`, `fonts/`)
   - What goes in `tests/`? (GdUnit4 test files)

---

### D.1 — Feature 31: project-bootstrap Plugin (new-project)

**New plugin**: `plugins/project-bootstrap/`

**Skill: `new-project`** — Create a Godot project from a one-sentence concept

Must contain (≥ 25 body lines):
- Input: game concept (one sentence), project name (kebab-case), target Godot version
- What Claude creates:
  - `/project.godot` — with text format, GDScript typing settings (from research)
  - `/.gitignore` — standard Godot gitignore (`.godot/imported/`, `.godot/mono/`, etc.)
  - `/CLAUDE.md` — from `cookbook/claude-md/godot.md` template, substituting project name and version
  - `/plans/game-backlog.json` — from `game-backlog/backlog-init` skill, seeded with first features Claude infers from the concept
  - `/README.md` — one-paragraph project description
- The initialization sequence (order matters — project.godot before directories):
  1. Create project.godot
  2. Create .gitignore
  3. Create directory structure
  4. Create CLAUDE.md
  5. Create autoloads (next skill)
  6. Create initial game-backlog.json
  7. Report: project is ready, first feature is queued
- The design-inference step: Claude reads the concept and proposes 3-5 initial backlog features (not implemented yet — just queued)

**Verification:**
1. SKILL.md exists ≥ 25 body lines
2. Lists the 7 initialization steps
3. Mentions `game-backlog.json` creation
4. Mentions CLAUDE.md template
5. All tests pass

---

### D.2 — Feature 32: project-bootstrap Plugin (configure-quality + setup-autoloads)

**Skill: `configure-quality`** — Install and configure all quality tooling

Must contain (≥ 18 body lines):
- Install gdtoolkit: `pip install gdtoolkit` (or `uv tool install gdtoolkit`)
- The `.gdlintrc` content (from research — full copy-paste ready config)
- Add quality hooks to `.claude/settings.json` (reference `cookbook/hooks/godot-quality.md`)
- Verify installation: `gdlint --version`, `gdformat --version`
- GdUnit4 install note: must be done via Godot Asset Library in editor (document the steps)
- Optional C#: `dotnet tool install -g csharpier`
- How to run the full quality gate after setup: the `quality` skill command sequence

**Skill: `setup-autoloads`** — Create the three canonical autoload scripts and register them

Must contain (≥ 20 body lines):
- Create `src/autoloads/event_bus.gd` — the global signal bus (Node, no class_name, typed signals)
  - Include 5 example signals Claude writes as stubs: `signal player_died()`, `signal scene_changed(scene_path: String)`, etc.
- Create `src/autoloads/game_manager.gd` — scene transitions and pause
  - `change_scene_to_file(path: String) -> void`
  - `set_pause(paused: bool) -> void`
- Create `src/autoloads/save_manager.gd` — ConfigFile-based save/load
  - `save_game(data: Dictionary) -> void`
  - `load_game() -> Dictionary`
  - `has_save() -> bool`
- The project.godot autoload registration format:
  ```ini
  [autoload]
  EventBus="*res://src/autoloads/event_bus.gd"
  GameManager="*res://src/autoloads/game_manager.gd"
  SaveManager="*res://src/autoloads/save_manager.gd"
  ```
- All scripts must be fully statically typed

**Verification:**
1. Both SKILL.md files exist ≥ 18/20 lines
2. `configure-quality` contains the `.gdlintrc` content
3. `setup-autoloads` contains the three GDScript class skeletons
4. `setup-autoloads` contains the project.godot autoload registration block
5. All tests pass

---

### D.3 — Feature 33: project-bootstrap Plugin (setup-directories)

**Skill: `setup-directories`** — Create the canonical directory structure

Must contain (≥ 12 body lines):
- Complete directory tree with purpose of each (matching CLAUDE.md conventions)
- The `.gdignore` files in non-Godot directories (prevents Godot from importing Python/JSON files accidentally)
- How to extend the structure for specific game types (platformer adds `src/platforms/`, RPG adds `src/dialogue/`)
- Rule: `scenes/` mirrors `src/` structure exactly — one `.tscn` per `.gd` class where possible

**Verification:**
1. SKILL.md exists ≥ 12 lines
2. Mentions `.gdignore` usage
3. Mentions the `scenes/` mirrors `src/` rule
4. All tests pass

---

### D.testing — Feature 34: Phase D Integration Tests

**File**: `tests/plugins/test_project_bootstrap_integration.py` (≥ 8 test functions)

- `test_plugin_json_valid`
- `test_all_skills_exist` (new-project, configure-quality, setup-autoloads, setup-directories)
- `test_new_project_body_depth` (≥ 25 lines)
- `test_new_project_mentions_initialization_steps`
- `test_configure_quality_has_gdlintrc_content`
- `test_setup_autoloads_has_three_scripts`
- `test_setup_autoloads_has_autoload_registration_block`
- `test_setup_directories_mentions_gdignore`

**Verification**: `uv run pytest tests/ -v` — all pass

---

### D.done — Phase D Definition of Done

- [ ] `plugins/project-bootstrap/` — 4 skills, README.md, plugin.json
- [ ] Integration tests ≥ 8 new test functions, all passing
- [ ] `plans/research/phase-d-bootstrap.md` — project.godot settings, autoload scripts, directory structure documented
- [ ] Validation agent: VALIDATION: PASS

---

## Phase E: Game System Coverage

**Goal**: Broaden the skill library to cover physics, UI, audio, and 5 more game design systems. Phases A–D unlock the core workflow; Phase E makes Claude competent across the game types designers actually build.

### E.0 — Research Gate

**Document in `plans/research/phase-e-systems.md`:**

1. **Godot 4.6.1 API changes** from 4.3/4.4 for:
   - CharacterBody3D: `velocity` property, `move_and_slide()` signature, `get_floor_normal()`
   - RigidBody3D: `freeze` vs. old `mode`, `apply_central_impulse()` vs. old names
   - NavigationAgent3D: `target_position` vs. old `target_location`, `get_next_path_position()`
   - AudioStreamSynchronized: is it in 4.6.1? What's the API?
   - AudioStreamInteractive: is it in 4.6.1? State machine API?

2. **Dialogue system options in Godot 4.x**
   - Dialogic 2: current API, is it maintained in 2026?
   - Custom state machine approach: pros/cons vs. Dialogic 2
   - Decision: which one does the `dialogue-design` skill recommend as primary?

3. **Control node anchors in Godot 4.x**
   - How do anchor presets work programmatically? (`anchor_left`, `anchor_top`, etc.)
   - What changed from Godot 3 in the Control/Container system?

---

### E.1 — Feature 35: Expanded game-design Skills (combat + inventory)

**Skill: `combat-design`** — Full combat system spec

Must contain (≥ 20 body lines):
- Hitbox/hurtbox architecture: separate Area3D nodes (`HitboxArea3D`, `HurtboxArea3D`)
- The damage pipeline: attacker emits `hit_landed(damage: float, hit_position: Vector3)` → defender's hurtbox receives → applies to health
- Hit feedback checklist: screen shake (Camera3D.basis rotation), particle burst, audio (pitch-randomized SFX), hitstop (brief `Engine.time_scale` reduction)
- Invincibility frame pattern: timer-based `is_invincible: bool` flag, set on `_on_hurtbox_area_entered`
- Combo tracking: StringName array of inputs, matched against combo dictionary
- Resource schema: `AttackData` (damage: float, knockback: Vector3, hitstop: float, sfx: AudioStream)
- Typed GDScript skeleton for the hitbox component

**Skill: `inventory-design`** — Item and inventory system

Must contain (≥ 18 body lines):
- `ItemData` Resource subclass: id (StringName), display_name, icon (Texture2D), stackable (bool), max_stack (int), weight (float)
- Inventory container: `Array[ItemData]` with typed add/remove/has methods
- Hotbar vs. bag vs. equipment slot distinction
- Pickup signal chain: `Area3D.body_entered` → `pickup_requested(item: ItemData)` → inventory add → UI update
- Weight system: total_weight property, overencumbered signal
- Stacking logic: find existing stack, increment count, emit `inventory_changed`
- `ItemDB` autoload: Dictionary[StringName, ItemData] for looking up items by ID

**Verification:**
1. Both SKILL.md files exist ≥ 18/20 lines
2. `combat-design` contains `AttackData` resource schema
3. `inventory-design` contains `ItemData` resource schema
4. Both have typed GDScript examples
5. All tests pass

---

### E.2 — Feature 36: Expanded game-design Skills (dialogue + enemy + progression)

**Skill: `dialogue-design`** — Dialogue system

Must contain (≥ 18 body lines):
- Primary recommendation: Dialogic 2 for feature-rich dialogue; custom state machine for simple games
- `DialogueLine` Resource: speaker_name, text, portrait (Texture2D), choices (Array[DialogueChoice])
- `DialogueChoice` Resource: text, next_line_id (StringName), condition (StringName)
- Custom state machine approach: `DialogueState` enum, `DialogueManager` autoload, `dialogue_started/ended` signals
- Integration with Godot UI: RichTextLabel for BBCode formatting, AnimationPlayer for portrait transitions
- Saving dialogue state: which conversations are complete (Dictionary[StringName, bool])

**Skill: `enemy-design`** — Enemy AI architecture

Must contain (≥ 20 body lines):
- NavigationAgent3D setup: `target_position` set in `_physics_process`, `get_next_path_position()` for movement direction
- Sight detection: Area3D cone (custom CollisionShape3D approximation), `PhysicsDirectSpaceState3D` raycast for line-of-sight confirmation
- Hearing detection: Area3D sphere, `SoundEvent` emitted by player
- State machine: `EnemyState` enum (PATROL, ALERT, CHASE, ATTACK, FLEE, DEAD), typed transition methods
- Group-based squad behavior: `get_tree().get_nodes_in_group("enemies")` for alert propagation
- Typed `EnemyData` Resource: speed, sight_range, attack_range, attack_damage, patrol_radius

**Skill: `progression-design`** — XP, leveling, unlocks

Must contain (≥ 15 body lines):
- `PlayerStats` Resource: level (int), current_xp (int), xp_to_next_level (int), stat curves
- Curve-based XP thresholds: `Curve` resource with level on X axis, XP required on Y
- Stat scaling: `base_stat + (level - 1) * growth_per_level`
- Unlock gates: `Dictionary[StringName, bool]` of unlocked abilities/items
- Achievement signals: `achievement_unlocked(achievement_id: StringName)` emitted to EventBus
- Save/load integration: `PlayerStats` fields go to SaveManager

**Verification:**
1. All three SKILL.md files exist ≥ 15/18/20 lines
2. `enemy-design` mentions NavigationAgent3D and state machine
3. `dialogue-design` mentions Dialogic 2 and the custom alternative
4. `progression-design` mentions Curve resource
5. All tests pass

---

### E.3 — Feature 37: godot-physics Plugin (character-movement + collision-layers)

**New plugin**: `plugins/godot-physics/`

**Skill: `character-movement`** — CharacterBody3D movement patterns

Must contain (≥ 22 body lines):
- Ground detection: `is_on_floor()` — use this, not raycasting
- `velocity` as a property: `velocity.y -= gravity * delta` pattern
- Slope limit: `floor_max_angle` property
- Coyote time: `var coyote_timer: float = 0.0`; counts up when off floor; jump allowed within 0.15s
- Jump buffering: `var jump_buffer: float = 0.0`; set on jump input; consumed on next `is_on_floor()` frame
- Air acceleration: separate `air_acceleration` constant, lerp toward input direction
- The canonical `_physics_process` structure (annotated with what goes where)
- Typed GDScript example of a complete 3D character movement class

**Skill: `collision-layers`** — Layer/mask design

Must contain (≥ 15 body lines):
- The constants autoload pattern: `class_name CollisionLayer` with `const PLAYER = 1`, `const ENEMIES = 2`, etc.
- Layer vs. mask: layer = "I am on this layer"; mask = "I detect these layers"
- Standard layout for action-RPG: layer 1=world, 2=player, 3=enemies, 4=items, 5=hitboxes, 6=hurtboxes, 7=triggers
- How to set in `project.godot` (`layer_names/3d_physics/layer_1 = "world"`)
- Common mistake: confusing layer and mask (hitbox should be ON layer 5, have mask = 6)

**Verification:**
1. Both SKILL.md files exist ≥ 15/22 lines
2. `character-movement` mentions coyote time and jump buffering
3. `character-movement` has a complete typed GDScript example
4. `collision-layers` has the CollisionLayer constants class
5. All tests pass

---

### E.4 — Feature 38: godot-physics Plugin (area-detection + rigidbody + projectiles)

**Skill: `area-detection`** — Area3D patterns

Must contain (≥ 15 body lines):
- Hitbox vs. hurtbox vs. trigger zone — three distinct use cases, each with different layer/mask config
- `body_entered` vs. `area_entered`: when to use each
- Avoiding ghost frames: use `monitoring = true` only when active; disable between attacks
- Sight cone approximation: ConvexPolygonShape3D or a narrow CapsuleShape3D rotated
- Line-of-sight raycast: `PhysicsDirectSpaceState3D.intersect_ray()` pattern

**Skill: `rigidbody-patterns`** — RigidBody3D use cases

Must contain (≥ 12 body lines):
- When to use RigidBody3D vs. CharacterBody3D (physics puzzles, debris, ragdolls — not player controllers)
- `freeze` modes: STATIC (no movement), KINEMATIC (code-controlled), default (full physics)
- Applying forces correctly: `apply_central_impulse()` for instant, `apply_central_force()` for sustained
- Sleeping bodies: `can_sleep = true`, `sleeping` property
- Ragdoll pattern: skeleton with `BoneAttachment3D` children driving RigidBody3D nodes

**Skill: `projectile-system`** — Pooled projectile architecture

Must contain (≥ 18 body lines):
- Why pooling matters: `instantiate()` + `queue_free()` per shot causes frame spikes at high fire rates
- Pool implementation: `Array[Projectile]` in `ProjectileManager` autoload, reuse via `activate()`/`deactivate()`
- `move_and_collide()` vs. raycast: move_and_collide for slow projectiles; raycast for instant/hitscan
- Piercing: iterate all collisions via `move_and_collide` shape cast; apply damage to each
- Network-safe note: seed RNG for piercing logic to keep client/server in sync

**Verification:**
1. All three SKILL.md files exist at required depths
2. `projectile-system` mentions pooling
3. `area-detection` mentions ghost frames
4. `rigidbody-patterns` mentions `freeze` modes
5. All tests pass

---

### E.5 — Feature 39: godot-ui Plugin

**New plugin**: `plugins/godot-ui/`

**Skills**: `hud-design`, `menu-design`, `theme-system`, `ui-signals` (4 skills)

Each skill ≥ 15 body lines. Key content:

**`hud-design`**: CanvasLayer (layer 1), anchor presets, TextureProgressBar for health, SubViewport for minimap, `_on_health_changed(new_health: float, max_health: float)` signal receiver pattern

**`menu-design`**: Main menu scene (separate from game), pause menu as CanvasLayer in game scene with `get_tree().paused = true`, settings menu with `ConfigFile` persistence, FocusMode.ALL for controller nav, `grab_focus()` on first button in `_ready()`

**`theme-system`**: Theme Resource with StyleBoxFlat variants, font (LabelSettings), color constant names, applying themes programmatically vs. inspector, how to override per-Control without breaking global theme

**`ui-signals`**: "Game updates UI, UI emits input events" principle, signal flow diagram (game system → UI display; UI button → game system via EventBus), avoiding circular dependencies, typed signal parameters for all UI updates

**Verification:**
1. All 4 SKILL.md files exist ≥ 15 lines each
2. `hud-design` mentions CanvasLayer and TextureProgressBar
3. `menu-design` mentions `get_tree().paused` and FocusMode
4. All tests pass

---

### E.6 — Feature 40: godot-audio Plugin

**New plugin**: `plugins/godot-audio/`

**Skills**: `audio-architecture`, `adaptive-music`, `sfx-patterns` (3 skills)

Each skill ≥ 15 body lines. Key content:

**`audio-architecture`**: Bus structure (Master → Music, SFX, Voice, Ambient), AudioStreamPlayer for music (singleton pattern via GameManager), AudioStreamPlayer3D for positional SFX (parented to emitting node), `AudioStreamRandomizer` for variation, volume via `db_to_linear()` and `linear_to_db()`

**`adaptive-music`**: `AudioStreamSynchronized` for stems (verify API in Godot 4.6.1 from research), transition timing (cross-fade duration set to match BPM), state machine (EXPLORE, COMBAT, BOSS, MENU) with signal-driven transitions from EventBus

**`sfx-patterns`**: Pooled AudioStreamPlayer3D nodes, `AudioStreamRandomizer` for pitch/volume variation, impact sounds tied to `body_entered` velocity magnitude (`linear_velocity.length()`), footstep system (surface detection via RayCast3D + AudioStream Dictionary)

**Verification:**
1. All 3 SKILL.md files exist ≥ 15 lines each
2. `audio-architecture` mentions the bus structure
3. `adaptive-music` mentions state machine and transitions
4. All tests pass

---

### E.testing — Feature 41: Phase E Integration Tests

**File**: `tests/plugins/test_godot_physics_integration.py` (≥ 8 tests)
**File**: `tests/plugins/test_godot_ui_integration.py` (≥ 6 tests)
**File**: `tests/plugins/test_godot_audio_integration.py` (≥ 5 tests)
**File**: `tests/plugins/test_game_design_phase_e.py` (≥ 6 tests — for new game-design skills)

All following the same pattern as existing integration tests.

**Verification**: `uv run pytest tests/ -v` — all pass

---

### E.done — Phase E Definition of Done

- [ ] 5 new skills in `game-design` plugin (combat, inventory, dialogue, enemy, progression)
- [ ] `plugins/godot-physics/` — 5 skills, README.md, plugin.json
- [ ] `plugins/godot-ui/` — 4 skills, README.md, plugin.json
- [ ] `plugins/godot-audio/` — 3 skills, README.md, plugin.json
- [ ] Integration tests ≥ 25 new test functions, all passing
- [ ] `plans/research/phase-e-systems.md` — API changes and design decisions documented
- [ ] Validation agent: VALIDATION: PASS

---

## Phase F: Godot Version Guard and API Reference

**Goal**: Eliminate the #1 AI failure mode (Godot 3 syntax contamination) and provide an embedded API reference that prevents method/class hallucinations.

### F.0 — Research Gate

**Document in `plans/research/phase-f-version-guard.md`:**

1. **Compile the complete Godot 3 → 4 breaking API change list** (relevant to game code, not engine internals):
   - Node renames: KinematicBody→CharacterBody3D/2D, Spatial→Node3D, etc.
   - Method signature changes: `move_and_slide`, `move_and_collide`, `connect`, etc.
   - Keyword changes: `yield`→`await`, `onready`→`@onready`, `export`→`@export`, `setget`→property
   - Removed globals: `PoolStringArray`→`PackedStringArray`, etc.

2. **For each of the 8 priority classes**, read the Godot 4.6 official API docs and extract:
   - Class hierarchy (extends X)
   - Constructor or scene requirements
   - All properties used in game code (not engine internals)
   - All methods used in game code
   - All signals
   - Common mistakes / deprecated patterns

3. **Design the API fragment format** — should be:
   - Quick-reference, not full docs
   - Under 60 lines per class (Claude can read it all in one pass)
   - Prioritizes the methods/properties Claude hallucinates most often

---

### F.1 — Feature 42: Godot 4 Version Guard in All Existing SKILL.md Files

**Task**: Add the version guard header to every SKILL.md in the four Godot plugins that contains GDScript.

**Files to update** (check each for GDScript content):
- `plugins/godot-patterns/skills/*/SKILL.md` (5 skills)
- `plugins/gdscript-guide/skills/*/SKILL.md` (4 skills)
- `plugins/godot-code-quality/skills/*/SKILL.md` (2 skills + 2 new from Phase A)
- `plugins/game-design/skills/*/SKILL.md` (7 skills including Phase E additions)

**Guard format** (insert after the closing `---` of YAML frontmatter):

```
> **Godot version**: Godot 4.6+ (GDScript 2.0). Never use Godot 3 syntax.
> Godot 3 → 4 quick-ref: `KinematicBody`→`CharacterBody3D`, `yield()`→`await`,
> `move_and_slide(vel, UP)`→`velocity` property + `move_and_slide()`,
> `connect("s", self, "cb")`→`signal.connect(callback)`, `Spatial`→`Node3D`,
> `onready var`→`@onready var`, `export var`→`@export var`.
```

**New test** added to `tests/plugins/test_plugin_structure.py`:
```python
def test_godot_skills_have_version_guard(skill_path: Path) -> None:
    """All GDScript-containing skills must have the Godot version guard."""
    content = skill_path.read_text(encoding="utf-8")
    if "gdscript" in content.lower() or "CharacterBody" in content or "@export" in content:
        assert "Godot 4" in content and "Godot 3" in content, \
            f"{skill_path}: missing Godot version guard"
```

**Verification:**
1. All GDScript-containing skills updated
2. New test function added and passing
3. `uv run pytest tests/ -v` — all pass

---

### F.2 — Feature 43: API Reference Fragments (CharacterBody3D, RigidBody3D, Area3D)

**Files**:
- `cookbook/api-ref/CharacterBody3D.md`
- `cookbook/api-ref/RigidBody3D.md`
- `cookbook/api-ref/Area3D.md`

Each ≥ 25 lines, must contain:
- `extends` chain
- Key properties (with types)
- Key methods (with full typed signatures)
- Key signals
- Common mistakes / what NOT to do
- One minimal typed GDScript usage example

**Verification:**
1. All 3 files exist ≥ 25 lines
2. Each contains `extends` chain
3. Each contains a typed GDScript example
4. All tests pass

---

### F.3 — Feature 44: API Reference Fragments (AnimationPlayer, NavigationAgent3D, AudioStreamPlayer)

**Files**:
- `cookbook/api-ref/AnimationPlayer.md`
- `cookbook/api-ref/NavigationAgent3D.md`
- `cookbook/api-ref/AudioStreamPlayer.md`

Same requirements as F.2.

**Verification**: Same as F.2 (3 files, ≥ 25 lines each, extends + typed example)

---

### F.4 — Feature 45: API Reference Fragments (Resource, Signal patterns)

**Files**:
- `cookbook/api-ref/Resource.md` — Custom Resource subclasses, @export fields, load/save patterns, why not to use `new()` in _ready
- `cookbook/api-ref/Signal.md` — Signal declaration syntax (typed params), `signal.connect()` vs old `connect()`, `signal.emit()`, `is_connected()`, `disconnect()`, lambda connections

**Verification**: Same pattern

---

### F.5 — Feature 46: api-lookup Skill

**File**: `plugins/gdscript-guide/skills/api-lookup/SKILL.md`

Must contain (≥ 15 body lines):
- How to use the `cookbook/api-ref/` fragments: read the relevant class file before writing code that uses that class
- The "verify before write" rule: if unsure a method exists, check the fragment; if the method isn't in the fragment, check the official docs before using it
- How to add a new fragment when a class is missing from the library
- The hallucination red flag patterns: methods ending in `_node`, getting node by type (not name), Godot 3 method names
- Workflow integration: before implementing any skill that involves physics, UI, audio, or navigation — load the relevant fragment first

**Verification:**
1. SKILL.md exists ≥ 15 lines
2. Mentions `cookbook/api-ref/`
3. Mentions "verify before write"
4. All tests pass

---

### F.done — Phase F Definition of Done

- [ ] Version guard added to all GDScript-containing SKILL.md files
- [ ] `cookbook/api-ref/` — 8 class reference fragments, each ≥ 25 lines
- [ ] `plugins/gdscript-guide/skills/api-lookup/SKILL.md`
- [ ] New version guard test in `test_plugin_structure.py`
- [ ] `plans/research/phase-f-version-guard.md` — full Godot 3→4 change list + API class summaries
- [ ] `uv run pytest tests/ -v` — all pass
- [ ] Validation agent: VALIDATION: PASS

---

## Phase G: Autonomous Game Agent

**Goal**: An agent harness that takes a feature from the game backlog through to designer approval, handling all implementation, testing, and verification autonomously.

### G.0 — Research Gate

**Document in `plans/research/phase-g-agent.md`:**

1. **The approval pause problem**
   - Claude Code agent mode cannot "wait" for user input mid-run
   - Solution: the agent writes a proposal file and stops cleanly; designer reviews and re-runs the agent to continue
   - Design: `plans/pending-approval/<feature-slug>-spec.md` is the handoff point
   - When spec exists + status is `pending_approval`: agent reads spec, waits for the designer's `[APPROVED]` marker in the file

2. **GDAI MCP conditional usage**
   - Agent must detect whether GDAI MCP is active before calling screenshot tools
   - Detection: check if `mcp` servers list in settings includes `gdai-mcp` or similar
   - Fallback: if no MCP, run `godot --headless --check-only -s <script.gd>` for code validation only

3. **Game feature vs. plugin feature**
   - The existing `feature_list.json` tracks plugin development
   - Game features are tracked in `plans/game-backlog.json` (in the game project)
   - The agent must use a different backlog reader (a new tool script or inline Python)

4. **Session discipline**
   - Target: 1-2 features per agent session (game features are larger than plugin features)
   - Agent should commit after each complete feature (after designer approval)

---

### G.1 — Feature 47: implement_feature Agent Prompt

**File**: `agent/prompts-game/implement_feature.md`

This is the primary agent harness for autonomous gameplay implementation.

Must contain these sections (≥ 80 lines total):

**ROLE**: Autonomous Godot programmer implementing a single game feature. Takes design direction from the game backlog and approved spec. Never implements without an approved spec.

**STEP 1: GET BEARINGS**
```bash
pwd && git log --oneline -3
uv run pytest tests/ -q 2>&1 | tail -5  # plugin tests
# Read game backlog
python -c "import json; [print(f['status'], f['title']) for f in json.load(open('plans/game-backlog.json'))['features']]"
```

**STEP 2: FIND ACTIVE FEATURE**
- Find feature with status `in_progress` or `pending_approval`
- If `pending_approval`: read `plans/pending-approval/<slug>-spec.md` and check for `[APPROVED]` marker
- If `[APPROVED]`: proceed to implementation
- If no `[APPROVED]`: report "Waiting for designer approval of spec at plans/pending-approval/<slug>-spec.md" and STOP

**STEP 3: GENERATE SPEC (if no spec exists)**
- Read the feature's `brief` from game-backlog.json
- Generate a full spec using the `designer-brief/brief` skill format
- Write to `plans/pending-approval/<slug>-spec.md`
- Update feature status to `pending_approval`
- Commit the spec file
- Report: "Spec ready for review at plans/pending-approval/<slug>-spec.md" and STOP

**STEP 4: IMPLEMENT**
- Read the approved spec
- Generate all .gd files (typed, with class_name, signals, @export)
- Generate all .tscn files using `scene-builder/scene-from-brief` patterns
- Generate .tres resource files if spec includes custom Resources
- Run `gdlint` on all generated .gd files; fix any lint errors before proceeding
- Run `godot --headless --check-only -s <root_script.gd>` for type checking

**STEP 5: VERIFY**
- Run GdUnit4 tests if any exist for this feature
- If GDAI MCP active: run the relevant scene, capture debug output, take screenshot
- If no MCP: run `godot --headless --check-only` on all new scripts
- Report verification results clearly

**STEP 6: REPORT TO DESIGNER**
- What was implemented (file list)
- Screenshot if captured
- Any issues found and how they were resolved
- What the designer should check in the editor
- Instruction: "Run `/iterate` with specific feedback, or `/feature-complete` if satisfied"

**STEP 7: COMMIT**
- Only after implementation and verification pass (not after spec generation)
- git add specific files (not -A)
- Commit message format: `feat(<feature-slug>): <title>`

**IMPORTANT RULES** section:
- Never implement without `[APPROVED]` in the spec
- Never skip the lint check
- If a .tscn is needed, always use `scene-builder/create-scene` patterns (load cookbook/api-ref/tscn-format.md first)
- Always use Godot 4 syntax (load the version guard from any Godot SKILL.md as reminder)
- If uncertain about a Godot API method, check the relevant cookbook/api-ref/ fragment first

**Verification:**
1. File exists ≥ 80 lines
2. Contains all 7 steps
3. Contains the `[APPROVED]` marker check
4. Contains the GDAI MCP conditional check
5. Contains "Never implement without" rule

---

### G.2 — Feature 48: iterate_on_feedback Agent Prompt

**File**: `agent/prompts-game/iterate_on_feedback.md`

The agent that processes designer playtest feedback into targeted code changes.

Must contain (≥ 50 lines):

**ROLE**: Receives designer feedback, identifies the minimum change to address each complaint, proposes the diff, waits for approval, applies.

**STEP 1**: Read `plans/game-backlog.json` and the active feature's spec

**STEP 2**: Parse designer feedback (from the last playtest-debrief format):
- Categorize each complaint: feel / bug / performance / visual
- Map each complaint to the most likely responsible file and function
- Severity rank: critical (game-breaking) / medium / low

**STEP 3**: For each complaint (ordered by severity):
- Propose the minimal change: show the exact lines to change (before/after)
- Do NOT redesign — only change what is necessary
- Write proposed changes to `plans/pending-changes/<feature-slug>-iteration-N.md`
- Commit the proposal file

**STEP 4**: Report proposed changes to designer and STOP
- "Here are N proposed changes. Review plans/pending-changes/... and mark each [APPROVED] or [SKIP]"

**STEP 5** (next agent run): Apply all `[APPROVED]` changes, verify, report

**Verification:**
1. File exists ≥ 50 lines
2. Contains feel/bug/performance/visual categorization
3. Contains the `[APPROVED]` / `[SKIP]` marker workflow
4. Contains "minimal change" rule

---

### G.3 — Feature 49: game-session Hooks and CLAUDE.md Update

**File**: `cookbook/hooks/game-session.md`

The complete hooks recipe for a game development session. Must contain (≥ 30 lines):
- The hooks.json block (Start, Stop, PreToolUse)
- settings.json merge instructions
- Session protocol for the game CLAUDE.md section:
  - Every session: start with `/backlog-status`
  - Before any new file: confirm spec is approved
  - Before any commit: run `/quality`
  - End of session: run `/feature-complete` or leave a note in game-backlog.json

**Update `cookbook/claude-md/godot.md`**: Add a new section "## Game Development Session Protocol" (5-8 lines) linking to the game-session hooks recipe and the designer-brief workflow.

**Verification:**
1. `cookbook/hooks/game-session.md` exists ≥ 30 lines
2. Contains the full hooks.json block
3. `cookbook/claude-md/godot.md` has the new session protocol section
4. All tests pass

---

### G.done — Phase G Definition of Done

- [ ] `agent/prompts-game/implement_feature.md` — ≥ 80 lines, all 7 steps, approval gate
- [ ] `agent/prompts-game/iterate_on_feedback.md` — ≥ 50 lines, categorization + minimal change rule
- [ ] `cookbook/hooks/game-session.md` — ≥ 30 lines with complete hooks.json
- [ ] `cookbook/claude-md/godot.md` updated with session protocol
- [ ] `plans/research/phase-g-agent.md` — approval pause design, MCP conditional, backlog reader documented
- [ ] Validation agent: VALIDATION: PASS

---

## Complete feature_list.json Additions

Append these entries to `feature_list.json` (IDs 13–49). Set all `"passes": false`.

```json
  {"id": 13, "phase": "godot-p4", "description": "Create cookbook/mcp/gdai-mcp.md: complete GDAI MCP setup guide for Windows 11. Must be ≥40 lines, contain a fenced JSON settings.json block, mention capture_screenshot (or correct tool name from research), and include Windows-specific notes.", "verification": ["Step 1: cookbook/mcp/gdai-mcp.md exists ≥40 lines", "Step 2: contains fenced JSON settings.json MCP block", "Step 3: mentions screenshot tool name", "Step 4: uv run pytest tests/ -v -- all pass"], "passes": false},
  {"id": 14, "phase": "godot-p4", "description": "Create cookbook/mcp/godot-mcp-minimal.md: lighter godot-mcp alternative guide. Must be ≥25 lines, contain npm install command and JSON config block, and a comparison table vs GDAI MCP.", "verification": ["Step 1: file exists ≥25 lines", "Step 2: contains npm install command", "Step 3: contains comparison table", "Step 4: all tests pass"], "passes": false},
  {"id": 15, "phase": "godot-p4", "description": "Create cookbook/mcp/gdscript-lsp.md: GDScript LSP bridge setup guide. Must be ≥30 lines, contain --lsp-port in the guide and a settings.json config block.", "verification": ["Step 1: file exists ≥30 lines", "Step 2: contains '--lsp-port'", "Step 3: contains settings.json config block", "Step 4: all tests pass"], "passes": false},
  {"id": 16, "phase": "godot-p4", "description": "Add lsp-setup skill to godot-code-quality plugin. Body ≥15 lines. Must mention --lsp-port, the TCP/stdio bridge architecture, and how to verify the LSP is working.", "verification": ["Step 1: plugins/godot-code-quality/skills/lsp-setup/SKILL.md exists", "Step 2: body ≥15 non-blank lines", "Step 3: mentions '--lsp-port' and bridge", "Step 4: all tests pass"], "passes": false},
  {"id": 17, "phase": "godot-p4", "description": "Add screenshot-review skill to godot-code-quality plugin. Body ≥15 lines. Must mention GDAI MCP, 'design intent', and 'debug output'. Explain when screenshot review applies and its limitations.", "verification": ["Step 1: plugins/godot-code-quality/skills/screenshot-review/SKILL.md exists", "Step 2: body ≥15 non-blank lines", "Step 3: mentions GDAI MCP and design intent", "Step 4: all tests pass"], "passes": false},
  {"id": 18, "phase": "godot-p4", "description": "Create tests/plugins/test_godot_code_quality_phase_a.py with ≥6 test functions validating lsp-setup and screenshot-review skills and the new mcp cookbook recipes.", "verification": ["Step 1: test file exists with ≥6 test functions", "Step 2: uv run pytest tests/plugins/test_godot_code_quality_phase_a.py -v -- all pass", "Step 3: all tests pass"], "passes": false},

  {"id": 19, "phase": "godot-p5", "description": "Create designer-brief plugin with brief and spec-review skills. brief body ≥20 lines with full brief template (Intent, Feel, Constraints, Out of scope, Designer acceptance). spec-review body ≥15 lines mentioning ACTIVE_SPEC.md.", "verification": ["Step 1: plugins/designer-brief/.claude-plugin/plugin.json exists", "Step 2: skills/brief/SKILL.md body ≥20 lines with all 5 template headings", "Step 3: skills/spec-review/SKILL.md body ≥15 lines mentions ACTIVE_SPEC.md", "Step 4: all tests pass"], "passes": false},
  {"id": 20, "phase": "godot-p5", "description": "Add iterate, playtest-debrief, and feature-complete skills to designer-brief plugin. iterate ≥15 lines mentions 'minimal diff'. playtest-debrief ≥15 lines has full template. feature-complete ≥12 lines mentions gdlint and GdUnit4.", "verification": ["Step 1: all three SKILL.md files exist", "Step 2: iterate mentions 'minimal diff'", "Step 3: playtest-debrief has What worked/What felt wrong/Bugs/Questions headings", "Step 4: feature-complete mentions gdlint and GdUnit4", "Step 5: all tests pass"], "passes": false},
  {"id": 21, "phase": "godot-p5", "description": "Add hooks.json to designer-brief plugin (PreToolUse on Write/Edit for .gd/.tscn files) and create cookbook/hooks/designer-approval.md ≥20 lines with complete check_spec.py script.", "verification": ["Step 1: plugins/designer-brief/hooks/hooks.json is valid JSON with PreToolUse entry", "Step 2: cookbook/hooks/designer-approval.md exists ≥20 lines", "Step 3: contains complete check_spec.py script", "Step 4: all tests pass"], "passes": false},
  {"id": 22, "phase": "godot-p5", "description": "Create game-backlog plugin with backlog-init and backlog-status skills. backlog-init ≥15 lines contains full JSON schema (id, title, brief, status, priority, spec, notes). backlog-status ≥12 lines mentions in_progress.", "verification": ["Step 1: plugins/game-backlog/.claude-plugin/plugin.json exists", "Step 2: backlog-init body ≥15 lines with complete JSON schema", "Step 3: backlog-status body ≥12 lines mentions in_progress", "Step 4: all tests pass"], "passes": false},
  {"id": 23, "phase": "godot-p5", "description": "Add next-feature and add-feature skills to game-backlog plugin. next-feature ≥12 lines mentions pending_approval. add-feature ≥10 lines mentions priority.", "verification": ["Step 1: both SKILL.md files exist", "Step 2: next-feature mentions pending_approval", "Step 3: add-feature mentions priority", "Step 4: all tests pass"], "passes": false},
  {"id": 24, "phase": "godot-p5", "description": "Create cookbook/hooks/game-session.md ≥25 lines with complete hooks.json block (Start and Stop events) and session protocol rules.", "verification": ["Step 1: file exists ≥25 lines", "Step 2: contains fenced JSON with Start and Stop hooks", "Step 3: all tests pass"], "passes": false},
  {"id": 25, "phase": "godot-p5", "description": "Create integration tests for designer-brief (≥8 functions) and game-backlog (≥6 functions) plugins.", "verification": ["Step 1: tests/plugins/test_designer_brief_integration.py exists with ≥8 functions", "Step 2: tests/plugins/test_game_backlog_integration.py exists with ≥6 functions", "Step 3: uv run pytest tests/ -v -- all pass"], "passes": false},

  {"id": 26, "phase": "godot-p6", "description": "Create cookbook/api-ref/tscn-format.md ≥60 lines: complete annotated .tscn example, UID generation rule (uid:// + base62), resource ID format, load_steps formula, signal connection syntax, sub_resource types for 5 common shapes, common mistakes.", "verification": ["Step 1: file exists ≥60 lines", "Step 2: contains complete .tscn example in fenced code block", "Step 3: contains 'uid://' format documentation", "Step 4: contains '[connection' signal syntax", "Step 5: all tests pass"], "passes": false},
  {"id": 27, "phase": "godot-p6", "description": "Create scene-builder plugin with create-scene skill. Body ≥25 lines. Must contain the generation algorithm (5 steps), CollisionShape3D mandatory child rule, UID generation, and a complete .tscn output example.", "verification": ["Step 1: plugins/scene-builder/.claude-plugin/plugin.json exists", "Step 2: skills/create-scene/SKILL.md body ≥25 non-blank lines", "Step 3: contains complete .tscn output in fenced code block", "Step 4: mentions uid generation and CollisionShape rule", "Step 5: all tests pass"], "passes": false},
  {"id": 28, "phase": "godot-p6", "description": "Add add-node and wire-signals skills to scene-builder. add-node ≥18 lines mentions path preservation. wire-signals ≥15 lines contains [connection syntax and validation steps.", "verification": ["Step 1: both SKILL.md files exist", "Step 2: add-node mentions path preservation ≥18 lines", "Step 3: wire-signals contains '[connection' syntax example ≥15 lines", "Step 4: all tests pass"], "passes": false},
  {"id": 29, "phase": "godot-p6", "description": "Add scene-from-brief and scene-audit skills to scene-builder. scene-from-brief ≥20 lines mentions ACTIVE_SPEC.md and the 5-step generation order. scene-audit ≥15 lines mentions orphaned scripts and CollisionShape3D.", "verification": ["Step 1: both SKILL.md files exist", "Step 2: scene-from-brief ≥20 lines mentions ACTIVE_SPEC.md", "Step 3: scene-audit ≥15 lines mentions orphaned scripts", "Step 4: all tests pass"], "passes": false},
  {"id": 30, "phase": "godot-p6", "description": "Create integration tests for scene-builder (≥10 functions) and cookbook api-ref tests (≥4 functions for tscn-format.md).", "verification": ["Step 1: tests/plugins/test_scene_builder_integration.py ≥10 functions", "Step 2: tests/cookbook/test_api_refs.py ≥4 functions", "Step 3: uv run pytest tests/ -v -- all pass"], "passes": false},

  {"id": 31, "phase": "godot-p7", "description": "Create project-bootstrap plugin with new-project skill. Body ≥25 lines. Must list the 7 initialization steps (project.godot, .gitignore, directories, CLAUDE.md, autoloads, backlog). Mentions game-backlog.json creation.", "verification": ["Step 1: plugins/project-bootstrap/.claude-plugin/plugin.json exists", "Step 2: skills/new-project/SKILL.md body ≥25 lines", "Step 3: contains all 7 initialization steps", "Step 4: mentions game-backlog.json", "Step 5: all tests pass"], "passes": false},
  {"id": 32, "phase": "godot-p7", "description": "Add configure-quality skill to project-bootstrap. Body ≥18 lines. Must contain complete .gdlintrc content (copy-paste ready), gdtoolkit install command, and quality hooks reference.", "verification": ["Step 1: SKILL.md exists ≥18 lines", "Step 2: contains .gdlintrc content", "Step 3: mentions gdtoolkit install and GdUnit4", "Step 4: all tests pass"], "passes": false},
  {"id": 33, "phase": "godot-p7", "description": "Add setup-autoloads skill to project-bootstrap. Body ≥20 lines. Must contain three GDScript class skeletons (EventBus, GameManager, SaveManager — all fully statically typed) and the project.godot [autoload] registration block.", "verification": ["Step 1: SKILL.md exists ≥20 lines", "Step 2: contains three GDScript class skeletons", "Step 3: all skeletons use static typing", "Step 4: contains project.godot [autoload] block", "Step 5: all tests pass"], "passes": false},
  {"id": 34, "phase": "godot-p7", "description": "Add setup-directories skill to project-bootstrap and create integration tests (≥8 functions).", "verification": ["Step 1: setup-directories SKILL.md exists ≥12 lines mentioning .gdignore", "Step 2: tests/plugins/test_project_bootstrap_integration.py ≥8 functions", "Step 3: uv run pytest tests/ -v -- all pass"], "passes": false},

  {"id": 35, "phase": "godot-p8", "description": "Add combat-design and inventory-design skills to game-design plugin. combat-design ≥20 lines with AttackData resource schema and typed GDScript hitbox example. inventory-design ≥18 lines with ItemData resource schema.", "verification": ["Step 1: both SKILL.md files exist at required depths", "Step 2: combat-design contains AttackData schema", "Step 3: inventory-design contains ItemData schema", "Step 4: both have typed GDScript code", "Step 5: all tests pass"], "passes": false},
  {"id": 36, "phase": "godot-p8", "description": "Add dialogue-design, enemy-design, and progression-design skills to game-design plugin. Depths ≥18/20/15 lines respectively. enemy-design mentions NavigationAgent3D and state machine. progression-design mentions Curve resource.", "verification": ["Step 1: all three exist at required depths", "Step 2: enemy-design mentions NavigationAgent3D and state machine", "Step 3: progression-design mentions Curve resource", "Step 4: dialogue-design mentions Dialogic 2", "Step 5: all tests pass"], "passes": false},
  {"id": 37, "phase": "godot-p8", "description": "Create godot-physics plugin with character-movement skill (≥22 lines). Must mention coyote time, jump buffering, air acceleration, and contain a complete typed CharacterBody3D movement GDScript example.", "verification": ["Step 1: plugins/godot-physics/.claude-plugin/plugin.json exists", "Step 2: character-movement body ≥22 lines", "Step 3: mentions coyote time and jump buffering", "Step 4: contains typed GDScript movement example", "Step 5: all tests pass"], "passes": false},
  {"id": 38, "phase": "godot-p8", "description": "Add collision-layers, area-detection, rigidbody-patterns, and projectile-system skills to godot-physics. Each at required depths. projectile-system mentions pooling. area-detection mentions ghost frames.", "verification": ["Step 1: all four SKILL.md files exist at required depths", "Step 2: projectile-system mentions pooling", "Step 3: area-detection mentions ghost frames", "Step 4: collision-layers has CollisionLayer constants class", "Step 5: all tests pass"], "passes": false},
  {"id": 39, "phase": "godot-p8", "description": "Create godot-ui plugin with hud-design, menu-design, theme-system, and ui-signals skills. Each ≥15 lines. hud-design mentions CanvasLayer and TextureProgressBar. menu-design mentions get_tree().paused and FocusMode.", "verification": ["Step 1: plugins/godot-ui/.claude-plugin/plugin.json exists", "Step 2: all four SKILL.md files exist ≥15 lines", "Step 3: hud-design mentions CanvasLayer", "Step 4: menu-design mentions get_tree().paused", "Step 5: all tests pass"], "passes": false},
  {"id": 40, "phase": "godot-p8", "description": "Create godot-audio plugin with audio-architecture, adaptive-music, and sfx-patterns skills. Each ≥15 lines. audio-architecture mentions bus structure. adaptive-music mentions state machine and transitions.", "verification": ["Step 1: plugins/godot-audio/.claude-plugin/plugin.json exists", "Step 2: all three SKILL.md files exist ≥15 lines", "Step 3: audio-architecture mentions bus structure", "Step 4: adaptive-music mentions state machine", "Step 5: all tests pass"], "passes": false},
  {"id": 41, "phase": "godot-p8", "description": "Create integration tests for godot-physics (≥8 functions), godot-ui (≥6 functions), godot-audio (≥5 functions), and expanded game-design skills (≥6 functions).", "verification": ["Step 1: all four test files exist at required function counts", "Step 2: uv run pytest tests/ -v -- all pass"], "passes": false},

  {"id": 42, "phase": "godot-p9", "description": "Add Godot 4 version guard to all existing GDScript-containing SKILL.md files (godot-patterns, gdscript-guide, godot-code-quality, game-design plugins). Add test to test_plugin_structure.py verifying guard presence.", "verification": ["Step 1: all GDScript-containing SKILL.md files have 'Godot 4' and 'Godot 3' in content", "Step 2: new test test_godot_skills_have_version_guard exists and passes", "Step 3: uv run pytest tests/ -v -- all pass"], "passes": false},
  {"id": 43, "phase": "godot-p9", "description": "Create cookbook/api-ref/ fragments for CharacterBody3D, RigidBody3D, Area3D. Each ≥25 lines with extends chain, key properties/methods/signals, and a typed GDScript usage example.", "verification": ["Step 1: all three files exist ≥25 lines", "Step 2: each contains extends chain and typed example", "Step 3: all tests pass"], "passes": false},
  {"id": 44, "phase": "godot-p9", "description": "Create cookbook/api-ref/ fragments for AnimationPlayer, NavigationAgent3D, AudioStreamPlayer. Same requirements as feature 43.", "verification": ["Step 1: all three files exist ≥25 lines", "Step 2: each contains extends chain and typed example", "Step 3: all tests pass"], "passes": false},
  {"id": 45, "phase": "godot-p9", "description": "Create cookbook/api-ref/Resource.md and cookbook/api-ref/Signal.md. ≥25 lines each. Resource covers custom subclasses, @export, load/save. Signal covers typed declarations, connect(), emit(), disconnect().", "verification": ["Step 1: both files exist ≥25 lines", "Step 2: Resource.md mentions @export and custom subclass", "Step 3: Signal.md mentions connect() and emit()", "Step 4: all tests pass"], "passes": false},
  {"id": 46, "phase": "godot-p9", "description": "Add api-lookup skill to gdscript-guide plugin. Body ≥15 lines. Mentions cookbook/api-ref/, 'verify before write' rule, and hallucination red flag patterns.", "verification": ["Step 1: SKILL.md exists ≥15 lines", "Step 2: mentions cookbook/api-ref/", "Step 3: mentions 'verify before write'", "Step 4: all tests pass"], "passes": false},

  {"id": 47, "phase": "godot-p10", "description": "Create agent/prompts-game/implement_feature.md ≥80 lines. Must contain all 7 steps, the [APPROVED] marker check, GDAI MCP conditional, and 'Never implement without approved spec' rule.", "verification": ["Step 1: file exists ≥80 lines", "Step 2: contains all 7 steps (GET BEARINGS through COMMIT)", "Step 3: contains '[APPROVED]' marker check logic", "Step 4: contains GDAI MCP conditional usage", "Step 5: all tests pass"], "passes": false},
  {"id": 48, "phase": "godot-p10", "description": "Create agent/prompts-game/iterate_on_feedback.md ≥50 lines. Must contain feel/bug/performance/visual categorization, the [APPROVED]/[SKIP] marker workflow, and the 'minimal change' rule.", "verification": ["Step 1: file exists ≥50 lines", "Step 2: contains four complaint categories", "Step 3: contains [APPROVED] and [SKIP] markers", "Step 4: mentions 'minimal change'", "Step 5: all tests pass"], "passes": false},
  {"id": 49, "phase": "godot-p10", "description": "Create cookbook/hooks/game-session.md ≥30 lines with complete hooks.json block. Update cookbook/claude-md/godot.md with 5-8 line session protocol section referencing designer-brief and game-session hooks.", "verification": ["Step 1: cookbook/hooks/game-session.md exists ≥30 lines with hooks.json block", "Step 2: cookbook/claude-md/godot.md has new session protocol section", "Step 3: uv run pytest tests/ -v -- all pass"], "passes": false}
```

---

## Testing Strategy

### Existing test infrastructure (do not break)
- `tests/plugins/test_plugin_structure.py` — structural validation of all plugins (auto-detects new plugins)
- `tests/skills/test_skill_loader.py` — skill loading validation
- `tests/tools/` — tool tests

### New test files per phase
| Phase | Test file | Min functions |
|-------|-----------|--------------|
| A | `tests/plugins/test_godot_code_quality_phase_a.py` | 6 |
| A | `tests/cookbook/test_mcp_recipes.py` | 4 |
| B | `tests/plugins/test_designer_brief_integration.py` | 8 |
| B | `tests/plugins/test_game_backlog_integration.py` | 6 |
| C | `tests/plugins/test_scene_builder_integration.py` | 10 |
| C | `tests/cookbook/test_api_refs.py` | 4 |
| D | `tests/plugins/test_project_bootstrap_integration.py` | 8 |
| E | `tests/plugins/test_godot_physics_integration.py` | 8 |
| E | `tests/plugins/test_godot_ui_integration.py` | 6 |
| E | `tests/plugins/test_godot_audio_integration.py` | 5 |
| E | `tests/plugins/test_game_design_phase_e.py` | 6 |
| F | added to `tests/plugins/test_plugin_structure.py` | +1 |
| F | `tests/cookbook/test_api_refs.py` | +6 new classes |

**Total new test functions**: ≥ 72

### Validation gate (after each phase)
Run `validation_prompt.md` with the scope restricted to features in the completed phase. The validation agent must output `VALIDATION: PASS` before the next phase begins.

### Full regression rule
After every feature is marked passing, `uv run pytest tests/ -v` must show 0 failures. No partial passes.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| GDAI MCP doesn't work on Windows 11 without display server | Medium | High | Research gate A.0 must test this; fallback to godot-mcp-minimal (headless compatible) |
| `.tscn` UID format generates invalid UIDs | Medium | High | Research gate C.0 tests hand-crafted UIDs in real Godot; document working format before writing the skill |
| GDScript LSP bridge incompatible with Godot 4.6.1 `--lsp-port` | Low | Medium | Research gate A.0 verifies flag exists; fallback to static gdlint if bridge unavailable |
| `scene-from-brief` generates .tscn that Godot rejects silently | Medium | High | Add demo .tscn validation step in C.done (open file in Godot, report errors) |
| AudioStreamSynchronized/Interactive not available in 4.6.1 | Low | Low | Research gate E.0 verifies API; if missing, use alternative patterns in `adaptive-music` |
| Godot headless mode can't validate .tscn files | Medium | Medium | C.0 research determines this; document limitation in scene-builder skills; recommend visual check |
| Designer approval gate hook causes friction | Low | Low | Hook is a warning, not a block; explicitly designed to be bypassable |
| Phase E scope creep (too many skills, agent gets confused) | Low | Medium | Keep each feature to 2-3 skills max; split into more features if needed |

---

## Session Targets

Each coding agent session should complete 2-4 features. Recommended session boundaries:

| Session | Features | Phase |
|---------|----------|-------|
| 1 | Research A.0 → document `plans/research/phase-a-mcp.md` | A |
| 2 | 13, 14, 15 | A |
| 3 | 16, 17, 18 | A |
| 4 | Research B.0 → document `plans/research/phase-b-workflow.md` | B |
| 5 | 19, 20 | B |
| 6 | 21, 22, 23 | B |
| 7 | 24, 25 | B |
| 8 | Research C.0 → document + test_generated_scene.tscn verified | C |
| 9 | 26, 27 | C |
| 10 | 28, 29, 30 | C |
| 11 | Research D.0 + 31, 32 | D |
| 12 | 33, 34 | D |
| 13–16 | 35–41 (Phase E, 2 features/session) | E |
| 17 | 42 (version guard — touches many files) | F |
| 18 | 43, 44, 45, 46 | F |
| 19 | Research G.0 + 47 | G |
| 20 | 48, 49 | G |
