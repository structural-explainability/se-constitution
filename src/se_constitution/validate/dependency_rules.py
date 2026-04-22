"""Validation for dependency rules data."""

from typing import Any

from se_constitution.types.dependency import DependencyRulesData


def validate_dependency_rules(data: DependencyRulesData) -> list[str]:
    """Validate dependency rules structure."""
    errors: list[str] = []

    dependency_section = data["dependency"]

    for class_name, class_def in dependency_section.items():
        allowed: Any | None = class_def.get("allowed")
        if not isinstance(allowed, list):
            errors.append(
                f"dependency-rules.toml: [dependency.{class_name}] must define allowed as a list."
            )

    return errors
