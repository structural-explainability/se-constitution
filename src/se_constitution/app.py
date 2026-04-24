"""app.py - Application orchestration for se_constitution."""

from typing import cast

from se_constitution.io.paths import DataPaths
from se_constitution.io.read import read_toml
from se_constitution.report.text import render_validation_report
from se_constitution.types.class_registry import ClassRegistryData
from se_constitution.types.cross_file import (
    ManifestSchemaData,
    NamingPatternsData,
    RepoRequirementsData,
)
from se_constitution.types.dependency import DependencyRulesData
from se_constitution.validate.class_registry import validate_class_registry
from se_constitution.validate.cross_file import validate_cross_file_consistency
from se_constitution.validate.dependency_rules import validate_dependency_rules
from se_constitution.validate.manifest_schema import validate_manifest_schema
from se_constitution.validate.naming_patterns import validate_naming_patterns
from se_constitution.validate.repo_requirements import validate_repo_requirements


def run_validate(*, strict: bool = False) -> int:
    """Validate all constitutional data and print a report."""
    paths = DataPaths.from_repo_root()

    # cast at the i/o boundary; internal code can use more specific types without worrying about parsing issues
    class_registry = cast(ClassRegistryData, read_toml(paths.class_registry))
    naming_patterns = cast(NamingPatternsData, read_toml(paths.naming_patterns))
    dependency_rules = cast(DependencyRulesData, read_toml(paths.dependency_rules))
    manifest_schema = cast(ManifestSchemaData, read_toml(paths.manifest_schema))
    repo_requirements = cast(RepoRequirementsData, read_toml(paths.repo_requirements))

    errors: list[str] = []
    warnings: list[str] = []

    errors.extend(validate_class_registry(class_registry))
    errors.extend(validate_naming_patterns(naming_patterns))
    errors.extend(validate_dependency_rules(dependency_rules))
    errors.extend(validate_manifest_schema(manifest_schema))
    errors.extend(validate_repo_requirements(repo_requirements))

    cross_errors, cross_warnings = validate_cross_file_consistency(
        class_registry=class_registry,
        naming_patterns=naming_patterns,
        dependency_rules=dependency_rules,
        manifest_schema=manifest_schema,
        repo_requirements=repo_requirements,
    )
    errors.extend(cross_errors)
    warnings.extend(cross_warnings)

    report = render_validation_report(errors=errors, warnings=warnings, strict=strict)
    print(report)

    if errors:
        return 1
    if strict and warnings:
        return 1
    return 0
