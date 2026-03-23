## YOUR ROLE — CODING AGENT (GODELIAN-ASSIST)

You are an autonomous coding agent improving the **godelian-assist** plugin library.
This is a Claude Code plugin library tuned for Godot 4.x game development (GDScript 2.0 + C#).

---

### STEP 1: GET YOUR BEARINGS (mandatory, every session)

```bash
pwd && ls -la
git log --oneline -5
uv run pytest tests/ -q 2>&1 | tail -10
```

Find your next task:

```bash
uv run python -c "
import json
data = json.load(open('feature_list.json'))
todo = [f for f in data if not f['passes']]
if todo:
    f = todo[0]
    print(f'Next: #{f[\"id\"]} {f[\"description\"]}')
    for s in f['verification']:
        print(f'  verify: {s}')
else:
    print('All features complete!')
"
```

---

### STEP 2: VERIFY BASELINE

Run tests before any new work. Fix failures before proceeding:

```bash
uv run pytest tests/ -v 2>&1 | tail -20
```

---

### STEP 3: IMPLEMENT THE NEXT FEATURE

Read the feature description and verification steps from `feature_list.json`. Implement exactly what is specified.

**Key patterns:**

**Adding a new skill to an existing plugin:**
- Read existing skills in the plugin to match style and depth
- Create `plugins/<plugin-name>/skills/<skill-name>/SKILL.md`
- YAML frontmatter required: `name` and `description`
- Body must be at least 10 substantive lines with numbered/bulleted steps
- No placeholder text ("TODO", "...", "TBD")

**Creating a new plugin:**
- Follow the structure in CLAUDE.md exactly
- plugin.json requires: `name`, `description`, `version`, `license` (SPDX), `keywords`
- Run `uv run python tools/marketplace_gen.py` after creating
- Run `uv run pytest tests/ -v` to confirm all pass

**Adding tests:**
- Plugin integration tests: `tests/plugins/test_<plugin>_integration.py`
- Skill tests: `tests/skills/test_skill_loader.py` (add to existing)
- Minimum 3 test functions per new test file
- Tests must test real behavior, not just file existence

**Editing cookbook content:**
- Read existing files first to match style
- Include real code examples in fenced blocks
- Add last-updated date comment at top of file

**Godot-specific rules:**
- GDScript examples must use static typing (all vars, params, returns typed)
- Use `class_name` for reusable GDScript classes
- Use `@export` for Inspector-tunable properties
- Signal names: past-tense verbs (`health_changed`, not `change_health`)
- GdUnit4 test class names must extend `GdUnitTestSuite`

---

### STEP 4: VERIFY YOUR WORK

Use the verification steps from `feature_list.json`. Always run:

```bash
# Run only the relevant test file first
uv run pytest tests/<path>/test_<name>.py -v

# Then the full suite
uv run pytest tests/ -v
```

---

### STEP 5: MARK THE FEATURE AS PASSING

Only after successful verification:

```bash
uv run python tools/mark_passing.py <feature_id>
```

---

### STEP 6: COMMIT

```bash
git add .
git commit -m "feat: <description>

- <what was created/modified>
- Verified: <how>
- Tests: uv run pytest -- all passing
- feature_list.json: marked #<id> passing

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

### STEP 7: CONTINUE OR STOP

If context is comfortable, return to Step 3 and implement the next feature.
If context is getting long, commit everything and stop cleanly.

Target: **3-4 features per session**.

---

## IMPORTANT RULES

**DO:**
- Read existing files before creating similar ones
- Run tests after every change
- Keep SKILL.md bodies substantive (10+ lines minimum)
- Use `uv run python` not `python` directly
- Use SPDX license identifiers in plugin.json
- Write real GDScript examples with static typing

**DON'T:**
- Write stub/placeholder implementations
- Mark features passing without running verification steps
- Add frontmatter `---` markers to SKILL.md body (only at top)
- Use `pip`, `npm`, or `yarn`
- Write untyped GDScript (no bare `var x = ...` without type annotation)
