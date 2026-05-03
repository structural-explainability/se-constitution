"""cli.py - Command-line interface for se-constitution.

Parses arguments and dispatches to validate.py or sync.py.
Owns nothing except argument parsing and error handling.

Entry points:
  uv run python -m se_constitution validate
  uv run python -m se_constitution validate --strict
  uv run python -m se_constitution validate --require-tag
  uv run python -m se_constitution sync

Call chain:
  __main__.py -> cli.main()
              -> validate.run_validate()  (sync_all called internally)
              -> sync.sync_all()          (sync only, no validation)
"""

import argparse

from se_constitution.sync import sync_all
from se_constitution.validate import run_validate


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog="se-constitution",
        description="Sync and validate the SE constitution artifacts.",
    )
    subparsers = parser.add_subparsers(dest="command")

    validate_parser = subparsers.add_parser(
        "validate",
        help="Sync and validate all constitutional artifacts.",
    )
    validate_parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors.",
    )
    validate_parser.add_argument(
        "--require-tag",
        action="store_true",
        help="Require contract_version to match the current exact git tag.",
    )

    subparsers.add_parser(
        "sync",
        help="Sync CITATION.cff and pyproject.toml from SE_MANIFEST.toml version.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the command-line interface."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "validate":
            return run_validate(
                strict=args.strict,
                require_tag=args.require_tag,
            )
        if args.command == "sync":
            sync_all()
            return 0

    except (ValueError, FileNotFoundError, RuntimeError) as e:
        print(f"Error: {e}")
        return 1

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
