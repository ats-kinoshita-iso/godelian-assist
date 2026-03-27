"""Pre-tool-use hook: warn if no approved spec is active before writing Godot files.

Drop this file into your game project's plans/ directory.
See cookbook/hooks/designer-approval.md for setup instructions.
"""
from __future__ import annotations

import sys
from pathlib import Path

ACTIVE_SPEC = Path(__file__).parent / "specs" / "ACTIVE_SPEC.md"

if not ACTIVE_SPEC.exists():
    print(
        "\n[designer-brief] WARNING: No active spec found at plans/specs/ACTIVE_SPEC.md\n"
        "  Run /brief to generate a spec, then /spec-review to approve it before\n"
        "  creating or editing .gd / .tscn / .tres files.\n"
        "  To bypass: create an empty plans/specs/ACTIVE_SPEC.md for this session.\n",
        file=sys.stderr,
    )

# Always exit 0 — this is a warning, not a block.
sys.exit(0)
