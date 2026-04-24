"""tests/validate/test_examples.py - Tests for canonical valid and invalid example artifact sets.

Issue #4: Add canonical examples.

Valid set:   data/examples/valid/   - minimal 2-class ecosystem, zero errors expected.
Invalid set: data/examples/invalid/ - 3 deliberate violations, one per affected file.

Violations in invalid set:
  1. class-registry.toml:   [class.kernel] missing required 'summary'
  2. dependency-rules.toml: kernel's allowed list contains unknown class 'phantom'
  3. naming-patterns.toml:  [pattern.phantom] references unknown class 'phantom'
"""

from pathlib import Path
import tomllib
from typing import Any, cast

from se_constitution.types.class_registry import ClassRegistryData
from se_constitution.types.cross_file import (
    ManifestSchemaData,
    NamingPatternsData,
    RepoRequirementsData,
)
from se_constitution.types.dependency import DependencyRulesData
from se_constitution.validate.class_registry import validate_class_registry
from se_constitution.validate.cross_file import validate_cross_file_consistency
from tests.fixture.data import make_valid_data

# tests/validate/ -> tests/ -> project root -> data/examples/
EXAMPLES_DIR: Path = Path(__file__).parent.parent.parent / "data" / "examples"
VALID_DIR: Path = EXAMPLES_DIR / "valid"
INVALID_DIR: Path = EXAMPLES_DIR / "invalid"


def load_toml(path: Path) -> dict[str, Any]:
    """Load a TOML file as a typed dict."""
    with path.open("rb") as f:
        return tomllib.load(f)


# ---------------------------------------------------------------------------
# Valid set
# ---------------------------------------------------------------------------


class TestValidExamples:
    """Canonical valid artifact set must produce zero validation errors."""

    def test_valid_class_registry_passes(self) -> None:
        data = cast(
            ClassRegistryData, load_toml(VALID_DIR / "class" / "class-registry.toml")
        )
        errors = validate_class_registry(data)
        assert errors == [], f"Expected no errors; got: {errors}"

    def test_valid_cross_file_passes(self) -> None:
        errors, warnings = validate_cross_file_consistency(
            class_registry=cast(
                ClassRegistryData,
                load_toml(VALID_DIR / "class" / "class-registry.toml"),
            ),
            naming_patterns=cast(
                NamingPatternsData,
                load_toml(VALID_DIR / "naming" / "naming-patterns.toml"),
            ),
            dependency_rules=cast(
                DependencyRulesData,
                load_toml(VALID_DIR / "dependency" / "dependency-rules.toml"),
            ),
            manifest_schema=cast(
                ManifestSchemaData,
                load_toml(VALID_DIR / "manifest" / "manifest-schema.toml"),
            ),
            repo_requirements=cast(
                RepoRequirementsData,
                load_toml(VALID_DIR / "repo" / "repo-requirements.toml"),
            ),
        )
        assert errors == [], f"Expected no cross-file errors; got: {errors}"
        assert warnings == [], f"Expected no cross-file warnings; got: {warnings}"

    # Extend with one test per individual validator as they are tightened in issues #1-#2.


# ---------------------------------------------------------------------------
# Invalid set
# ---------------------------------------------------------------------------


class TestInvalidExamples:
    """Canonical invalid artifact set must produce exactly the expected violations."""

    def test_violation_1_class_registry_missing_summary(self) -> None:
        """[class.kernel] missing 'summary' triggers class-registry validator."""
        data = cast(
            ClassRegistryData, load_toml(INVALID_DIR / "class" / "class-registry.toml")
        )
        errors = validate_class_registry(data)
        assert len(errors) == 1, f"Expected 1 error; got {len(errors)}: {errors}"
        assert "kernel" in errors[0] and "summary" in errors[0], (
            f"Expected error naming 'kernel' and 'summary'; got: {errors[0]}"
        )

    def test_violations_2_and_3_cross_file_phantom_class(self) -> None:
        """kernel's allowed list and a naming pattern both reference unknown class 'phantom'."""
        errors, _warnings = validate_cross_file_consistency(
            class_registry=cast(
                ClassRegistryData,
                load_toml(VALID_DIR / "class" / "class-registry.toml"),
            ),
            naming_patterns=cast(
                NamingPatternsData,
                load_toml(INVALID_DIR / "naming" / "naming-patterns.toml"),
            ),
            dependency_rules=cast(
                DependencyRulesData,
                load_toml(INVALID_DIR / "dependency" / "dependency-rules.toml"),
            ),
            manifest_schema=cast(
                ManifestSchemaData,
                load_toml(VALID_DIR / "manifest" / "manifest-schema.toml"),
            ),
            repo_requirements=cast(
                RepoRequirementsData,
                load_toml(VALID_DIR / "repo" / "repo-requirements.toml"),
            ),
        )
        assert any("phantom" in e and "naming" in e for e in errors), (
            f"Expected naming pattern phantom error; got: {errors}"
        )
        assert any("phantom" in e and "dependency" in e for e in errors), (
            f"Expected dependency phantom error; got: {errors}"
        )

    def test_valid_and_invalid_class_registries_differ(self) -> None:
        """Sanity check: valid and invalid sets are not identical."""
        valid = load_toml(VALID_DIR / "class" / "class-registry.toml")
        invalid = load_toml(INVALID_DIR / "class" / "class-registry.toml")
        assert valid != invalid

    def test_violation_dependency_subject_class_unknown(self) -> None:
        """Dependency rules subject class not in class-registry triggers cross-file error."""
        data = cast(dict[str, Any], make_valid_data())
        data["dependency_rules"]["dependency"]["phantom"] = {"allowed": []}
        errors, _ = validate_cross_file_consistency(
            class_registry=cast(ClassRegistryData, data["class_registry"]),
            naming_patterns=cast(NamingPatternsData, data["naming_patterns"]),
            dependency_rules=cast(DependencyRulesData, data["dependency_rules"]),
            manifest_schema=cast(ManifestSchemaData, data["manifest_schema"]),
            repo_requirements=cast(RepoRequirementsData, data["repo_requirements"]),
        )
        assert (
            "dependency-rules.toml: dependency rules reference unknown class 'phantom'."
            in errors
        )

    def test_violation_manifest_schema_unknown_class(self) -> None:
        """Manifest schema class entry not in class-registry triggers cross-file error."""
        data = cast(dict[str, Any], make_valid_data())
        data["manifest_schema"]["class"]["phantom"] = {}
        errors, _ = validate_cross_file_consistency(
            class_registry=cast(ClassRegistryData, data["class_registry"]),
            naming_patterns=cast(NamingPatternsData, data["naming_patterns"]),
            dependency_rules=cast(DependencyRulesData, data["dependency_rules"]),
            manifest_schema=cast(ManifestSchemaData, data["manifest_schema"]),
            repo_requirements=cast(RepoRequirementsData, data["repo_requirements"]),
        )
        assert (
            "manifest-schema.toml: class requirements reference unknown class 'phantom'."
            in errors
        )

    def test_violation_repo_requirements_unknown_class(self) -> None:
        """Repo requirements entry not in class-registry triggers cross-file error."""
        data = cast(dict[str, Any], make_valid_data())
        data["repo_requirements"]["repo"]["phantom"] = {
            "summary": "Phantom requirements."
        }
        errors, _ = validate_cross_file_consistency(
            class_registry=cast(ClassRegistryData, data["class_registry"]),
            naming_patterns=cast(NamingPatternsData, data["naming_patterns"]),
            dependency_rules=cast(DependencyRulesData, data["dependency_rules"]),
            manifest_schema=cast(ManifestSchemaData, data["manifest_schema"]),
            repo_requirements=cast(RepoRequirementsData, data["repo_requirements"]),
        )
        assert (
            "repo-requirements.toml: repo requirements reference unknown class 'phantom'."
            in errors
        )

    def test_warning_no_classes_defined(self) -> None:
        """Empty class registry triggers no-classes warning."""
        data = cast(dict[str, Any], make_valid_data())
        data["class_registry"]["class"] = {}
        _, warnings = validate_cross_file_consistency(
            class_registry=cast(ClassRegistryData, data["class_registry"]),
            naming_patterns=cast(NamingPatternsData, data["naming_patterns"]),
            dependency_rules=cast(DependencyRulesData, data["dependency_rules"]),
            manifest_schema=cast(ManifestSchemaData, data["manifest_schema"]),
            repo_requirements=cast(RepoRequirementsData, data["repo_requirements"]),
        )
        assert "No repo classes are currently defined." in warnings
