# godelian-assist Autonomous Agent

The autonomous coding agent for improving the godelian-assist plugin library.

## How It Works

1. Reads `feature_list.json` in the project root to find the next incomplete feature
2. Sends the coding prompt (`prompts-godot/coding_prompt.md`) to Claude
3. Claude reads, implements, and verifies the feature, then marks it passing
4. Loop continues until all features are complete

## Running the Agent

The agent harness requires the `claude_code_sdk` which is installed in the
`claude-quickstarts/autonomous-coding` virtualenv:

```bash
cd C:/Users/akino/claude-quickstarts/autonomous-coding
source .venv/Scripts/activate   # Windows: .venv/Scripts/activate.bat

# Run until all features complete
python run_godot_agent.py

# Limit sessions for testing
python run_godot_agent.py --max-iterations 2

# Use a different model
python run_godot_agent.py --model claude-opus-4-6
```

## Feature Phases

| Phase | Description | Features |
|-------|-------------|---------|
| `godot-p1` | New skills for existing plugins | #1–4 |
| `godot-p2` | Integration tests for Godot plugins | #5–8 |
| `godot-p3` | Content depth (cookbook, more skills) | #9–12 |

## Prompts

- `prompts-godot/coding_prompt.md` — main coding agent instructions
- `prompts-godot/validation_prompt.md` — validator instructions (for manual or automated validation runs)

## Adding Features

Add entries to `feature_list.json` in the project root. Each entry needs:

```json
{
  "id": 13,
  "phase": "godot-p4",
  "description": "...",
  "verification": ["Step 1: ...", "Step 2: ..."],
  "passes": false
}
```

Then run the agent — it will pick up the new features automatically.
