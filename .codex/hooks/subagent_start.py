#!/usr/bin/env python3
"""Emit non-blocking context for every Codex subagent start."""

import json
import sys


def main() -> None:
    # Consume the event payload without making assumptions about its shape.
    sys.stdin.read()
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SubagentStart",
                    "additionalContext": (
                        "Read repository AGENTS.md and instruction.md before job work; "
                        "preserve truth boundaries; return paths, facts/assumptions, "
                        "validation performed, and unresolved blockers."
                    ),
                }
            }
        )
    )


if __name__ == "__main__":
    main()
