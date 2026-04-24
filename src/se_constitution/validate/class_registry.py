"""validate/class_registry.py - Validation for class registry data."""

from se_constitution.types.class_registry import ClassRegistryData


def validate_class_registry(data: ClassRegistryData) -> list[str]:
    """Validate class registry structure."""
    errors: list[str] = []

    class_section = data["class"]

    if not class_section:
        errors.append("class-registry.toml: [class] must define at least one class.")

    for class_name, class_def in class_section.items():
        if "summary" not in class_def and "description" not in class_def:
            errors.append(
                f"class-registry.toml: [class.{class_name}] must define summary or description."
            )

    return errors
