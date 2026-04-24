"""validate/naming_patterns.py - Validation for naming patterns data."""

from se_constitution.types.cross_file import NamingPatternsData


def validate_naming_patterns(data: NamingPatternsData) -> list[str]:
    """Validate naming patterns structure."""
    errors: list[str] = []

    if "global" not in data:
        errors.append("naming-patterns.toml: missing [global] section.")

    pattern_section = data["pattern"]

    if not pattern_section:
        errors.append(
            "naming-patterns.toml: [pattern] must define at least one pattern."
        )

    for pattern_name, pattern_def in pattern_section.items():
        if "format" not in pattern_def:
            errors.append(
                f"naming-patterns.toml: [pattern.{pattern_name}] must define format."
            )

    return errors
