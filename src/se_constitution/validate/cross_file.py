"""validate/cross_file.py - Cross-file validation for constitutional artifacts.

- DependencyRulesData is imported from types.dependency (artifact-specific),
  NOT from types.cross_file.

- Dependency rules have a stable, enforced internal structure:
    meta + dependency + allowed list semantics and are validated both:
    (1) in their own validator, and
    (2) here for cross-artifact consistency.

- Therefore:
    DependencyRulesData is treated as a FIRST-CLASS artifact type.

- In contrast:
    NamingPatternsData, ManifestSchemaData, RepoRequirementsData
    are currently only partially structured and primarily used for
    cross-file checks, so they remain in types.cross_file.

STANDARD:

- Full artifact with internal invariants gets its own module in types/
- Lightweight or partially enforced shape uses types.cross_file

DESIGN RATIONALE:

- Long-term schema stability
- Clear ownership of artifact structure
- Avoid duplicate or drifting type definitions
"""

from se_constitution.types.class_registry import ClassRegistryData
from se_constitution.types.cross_file import (
    NamingPatternsData,
)
from se_constitution.types.dependency import DependencyRulesData
from se_constitution.types.manifest_schema import ManifestSchemaData
from se_constitution.types.repo_requirements import RepoRequirementsData


def _defined_classes(class_registry: ClassRegistryData) -> set[str]:
    """Return the set of defined repo classes."""
    return set(class_registry["class"].keys())


def _classes_used_by_naming_patterns(
    naming_patterns: NamingPatternsData,
) -> set[str]:
    """Return classes referenced by naming patterns."""
    used: set[str] = set()
    for pattern_def in naming_patterns.get("pattern", {}).values():
        raw_class = pattern_def.get("class")
        if isinstance(raw_class, str):
            used.add(raw_class)
    return used


def validate_cross_file_consistency(
    *,
    class_registry: ClassRegistryData,
    naming_patterns: NamingPatternsData,
    dependency_rules: DependencyRulesData,
    manifest_schema: ManifestSchemaData,
    repo_requirements: RepoRequirementsData,
) -> tuple[list[str], list[str]]:
    """Validate consistency across constitutional files."""
    errors: list[str] = []
    warnings: list[str] = []

    known_classes = _defined_classes(class_registry)

    for pattern_name, pattern_def in naming_patterns.get("pattern", {}).items():
        raw_class = pattern_def.get("class")
        class_name: str | None = raw_class if isinstance(raw_class, str) else None
        if class_name is not None and class_name not in known_classes:
            errors.append(
                f"naming-patterns.toml: pattern '{pattern_name}' references unknown class '{class_name}'."
            )

    for class_name in dependency_rules["dependency"]:
        if class_name not in known_classes:
            errors.append(
                f"dependency-rules.toml: dependency rules reference unknown class '{class_name}'."
            )

    for class_name, class_def in dependency_rules["dependency"].items():
        for allowed_class in class_def["allowed"]:
            if allowed_class not in known_classes:
                errors.append(
                    f"dependency-rules.toml: class '{class_name}' allows unknown dependency class '{allowed_class}'."
                )

    for class_name in manifest_schema.get("class", {}):
        if class_name not in known_classes:
            errors.append(
                f"manifest-schema.toml: class requirements reference unknown class '{class_name}'."
            )

    for class_name in repo_requirements.get("repo", {}):
        if class_name not in known_classes:
            errors.append(
                f"repo-requirements.toml: repo requirements reference unknown class '{class_name}'."
            )

    named_classes = _classes_used_by_naming_patterns(naming_patterns)
    dependency_classes = set(dependency_rules["dependency"].keys())
    manifest_classes = set(manifest_schema.get("class", {}).keys())
    repo_requirement_classes = set(repo_requirements.get("repo", {}).keys())

    for class_name in sorted(known_classes - named_classes):
        errors.append(
            f"class-registry.toml: class '{class_name}' has no naming pattern."
        )

    for class_name in sorted(known_classes - dependency_classes):
        errors.append(
            f"class-registry.toml: class '{class_name}' has no dependency rule."
        )

    for class_name in sorted(known_classes - manifest_classes):
        errors.append(
            f"class-registry.toml: class '{class_name}' has no manifest-schema entry."
        )

    for class_name in sorted(known_classes - repo_requirement_classes):
        errors.append(
            f"class-registry.toml: class '{class_name}' has no repo-requirements entry."
        )

    if not known_classes:
        warnings.append("No repo classes are currently defined.")

    return errors, warnings
