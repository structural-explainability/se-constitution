"""Module entry point for se-constitution.

Enables `uv run python -m se_constitution`.
Delegates immediately to the CLI entry point.
All logic lives in cli.py, validate.py, sync.py, and load.py.
"""

from se_constitution.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
