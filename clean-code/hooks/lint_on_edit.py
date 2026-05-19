#!/usr/bin/env python3
"""PostToolUse hook — lint a just-edited Python file with the PROJECT's ruff config.

Runs ruff on the edited `.py` file using whatever configuration the project
already defines (its pyproject.toml / ruff.toml). It deliberately imposes no
config of its own — it never overrides the project's ruff settings. Violations
are returned to Claude (exit 2) so it can fix them in-loop.

Whether the Clean Code Tier-1 rules are active is the project's choice: add them
to pyproject.toml via `extend-select` (see the plugin README).
"""
import json
import shutil
import subprocess
import sys


def _ruff_runner() -> list[str]:
    """Pick how to invoke ruff, preferring the project's uv-pinned version.

    `uv run ruff` uses the ruff version pinned in the project (so the hook
    matches CI). Falls back to a ruff already on PATH, then to `uvx ruff`.
    """
    if shutil.which("uv"):
        return ["uv", "run", "ruff"]
    if shutil.which("ruff"):
        return ["ruff"]
    return ["uvx", "ruff"]


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    file_path = (event.get("tool_input") or {}).get("file_path", "")
    if not file_path.endswith(".py"):
        return 0

    result = subprocess.run(
        [*_ruff_runner(), "check", file_path],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0 and (result.stdout or result.stderr):
        sys.stderr.write(result.stdout + result.stderr)
        return 2  # exit 2 — ruff's findings are returned to Claude to fix

    return 0


if __name__ == "__main__":
    sys.exit(main())
