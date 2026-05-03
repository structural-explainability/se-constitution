"""orchestrate.py - Validation orchestrator for se-constitution.

Owns run_validate(). Called by cli.py. Always syncs before validating.
This is the only file in this package that knows the full validation order.

Validation order:
  1. validate_tag()                - contract_version matches git tag (--require-tag only)
  2. validate_schema_internal()    - manifest-schema.toml is self-consistent
  3. validate_manifest()           - SE_MANIFEST.toml conforms to the schema
  4. validate_cross_file()         - constitutional artifacts are mutually consistent

Consumers in other repos should not call run_validate().
They should call the specific validation function they need.
"""

from typing import cast

from se_manifest_schema.load import load_manifest
from se_manifest_schema.validate_contract import validate_tag

from se_constitution.io.paths import DataPaths
from se_constitution.load import load_toml
from se_constitution.types.class_registry import ClassRegistryData
from se_constitution.types.dependency import DependencyRulesData
from se_constitution.types.naming_patterns import NamingPatternsData
from se_constitution.types.repo_requirements import RepoRequirementsData
from se_constitution.validate.class_registry import validate_class_registry
from se_constitution.validate.cross_file import validate_cross_file_consistency
from se_constitution.validate.dependency_rules import validate_dependency_rules
from se_constitution.validate.repo_requirements import validate_repo_requirements

_paths = DataPaths.from_repo_root()


def load_constitution_artifacts() -> tuple[
    ClassRegistryData,
    NamingPatternsData,
    DependencyRulesData,
    RepoRequirementsData,
]:
    """Load constitutional artifacts from TOML files.

    Returns:
        A tuple containing (ClassRegistryData, NamingPatternsData, DependencyRulesData, RepoRequirementsData).
    """
    return (
        cast(ClassRegistryData, load_toml(_paths.class_registry)),
        cast(NamingPatternsData, load_toml(_paths.naming_patterns)),
        cast(DependencyRulesData, load_toml(_paths.dependency_rules)),
        cast(RepoRequirementsData, load_toml(_paths.repo_requirements)),
    )


def run_validate(*, require_tag: bool = False, strict: bool = False) -> int:
    """Sync and validate the se-constitution repository.

    Args:
        require_tag: If True, verify contract_version matches current git tag.
        strict: If True, treat warnings as errors.

    Returns:
        0 on success, 1 on failure.
    """
    errors: list[str] = []
    warnings: list[str] = []

    try:
        manifest = load_manifest()
        class_registry, naming_patterns, dependency_rules, repo_requirements = (
            load_constitution_artifacts()
        )
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        return 1

    print("[validate] SE_MANIFEST.toml")
    print("[validate] constitutional artifacts")

    if require_tag:
        errors.extend(validate_tag(manifest))

    errors.extend(validate_class_registry(class_registry))
    errors.extend(validate_dependency_rules(dependency_rules))
    errors.extend(validate_repo_requirements(repo_requirements))

    cross_errors, cross_warnings = validate_cross_file_consistency(
        class_registry=class_registry,
        naming_patterns=naming_patterns,
        dependency_rules=dependency_rules,
        repo_requirements=repo_requirements,
    )
    errors.extend(cross_errors)
    warnings.extend(cross_warnings)

    for e in errors:
        print(f"ERROR: {e}")
    for w in warnings:
        print(f"WARNING: {w}")

    if errors:
        return 1
    if strict and warnings:
        return 1

    print("Constitution validation passed.")
    return 0
