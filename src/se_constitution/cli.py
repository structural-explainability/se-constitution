"""cli.py - Command-line interface."""

import argparse

from se_constitution.app import run_validate


def build_parser() -> argparse.ArgumentParser:
    """Build and return the command-line parser."""
    parser = argparse.ArgumentParser(
        prog="se_constitution",
        description="Validate Structural Explainability constitutional data.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate constitutional data files and cross-file consistency.",
    )
    validate_parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as validation failures.",
    )

    return parser


def main() -> int:
    """Run the command-line interface."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "validate":
        return run_validate(strict=args.strict)

    parser.error(f"Unknown command: {args.command}")
    return 2
