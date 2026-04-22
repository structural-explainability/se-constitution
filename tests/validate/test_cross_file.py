"""Tests for cross-file validation."""

from typing import Any, cast

from se_constitution.validate.cross_file import validate_cross_file_consistency
from tests.fixture.data import make_valid_data


def test_cross_file_validation_accepts_valid_data() -> None:
    """A valid constitutional dataset should produce no errors or warnings."""
    data = cast(dict[str, Any], make_valid_data())

    errors, warnings = validate_cross_file_consistency(
        class_registry=data["class_registry"],
        naming_patterns=data["naming_patterns"],
        dependency_rules=data["dependency_rules"],
        manifest_schema=data["manifest_schema"],
        repo_requirements=data["repo_requirements"],
    )

    assert errors == []
    assert warnings == []


def test_cross_file_validation_rejects_unknown_pattern_class() -> None:
    """Naming patterns may not reference unknown classes."""
    data = cast(dict[str, Any], make_valid_data())
    data["naming_patterns"]["pattern"]["schema"]["class"] = "unknown"

    errors, _warnings = validate_cross_file_consistency(
        class_registry=data["class_registry"],
        naming_patterns=data["naming_patterns"],
        dependency_rules=data["dependency_rules"],
        manifest_schema=data["manifest_schema"],
        repo_requirements=data["repo_requirements"],
    )

    assert (
        "naming-patterns.toml: pattern 'schema' references unknown class 'unknown'."
        in errors
    )


def test_cross_file_validation_rejects_unknown_allowed_dependency_class() -> None:
    """Dependency rules may not allow unknown classes."""
    data = cast(dict[str, Any], make_valid_data())
    data["dependency_rules"]["dependency"]["schema"]["allowed"].append("unknown")

    errors, _warnings = validate_cross_file_consistency(
        class_registry=data["class_registry"],
        naming_patterns=data["naming_patterns"],
        dependency_rules=data["dependency_rules"],
        manifest_schema=data["manifest_schema"],
        repo_requirements=data["repo_requirements"],
    )

    assert (
        "dependency-rules.toml: class 'schema' allows unknown dependency class 'unknown'."
        in errors
    )


def test_cross_file_validation_rejects_unknown_repo_requirement_class() -> None:
    """Repo requirements may not reference unknown classes."""
    data = cast(dict[str, Any], make_valid_data())
    data["repo_requirements"]["repo"]["unknown"] = {"summary": "Unknown requirements."}

    errors, _warnings = validate_cross_file_consistency(
        class_registry=data["class_registry"],
        naming_patterns=data["naming_patterns"],
        dependency_rules=data["dependency_rules"],
        manifest_schema=data["manifest_schema"],
        repo_requirements=data["repo_requirements"],
    )

    assert (
        "repo-requirements.toml: repo requirements reference unknown class 'unknown'."
        in errors
    )
