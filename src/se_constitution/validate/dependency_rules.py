"""validate/dependency_rules.py - Validation for dependency rules data."""

from typing import Any

from se_constitution.types.dependency import DependencyRulesData


def validate_formal_contract_root(data: DependencyRulesData) -> list[str]:
    """Validate formal_contract root dependency constraints."""
    errors: list[str] = []

    principles = data.get("principle")
    dependencies = data.get("dependency")

    if principles is None or principles.get("formal_contract_is_root") is not True:
        errors.append(
            "dependency-rules.toml: principle.formal_contract_is_root must be true."
        )

    if dependencies is None:
        errors.append("dependency-rules.toml: [dependency] section is required.")
        return errors

    formal_contract = dependencies.get("formal_contract")
    if formal_contract is None:
        errors.append(
            "dependency-rules.toml: [dependency.formal_contract] is required."
        )
        return errors

    allowed = formal_contract.get("allowed")
    if allowed != []:
        errors.append(
            "dependency-rules.toml: [dependency.formal_contract].allowed must be []."
        )

    return errors


def validate_dependency_rules(data: DependencyRulesData) -> list[str]:
    """Validate dependency rules structure."""
    errors: list[str] = []

    dependency_section = data.get("dependency")
    if dependency_section is None:
        errors.append("dependency-rules.toml: [dependency] section is required.")
        return errors

    for class_name, class_def in dependency_section.items():
        allowed: Any | None = class_def.get("allowed")
        if not isinstance(allowed, list):
            errors.append(
                f"dependency-rules.toml: [dependency.{class_name}] must define allowed as a list."
            )

    errors.extend(validate_formal_contract_root(data))
    return errors
