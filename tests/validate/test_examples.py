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
from se_constitution.types.cross_file import NamingPatternsData
from se_constitution.types.dependency import DependencyRulesData
from se_constitution.types.manifest_schema import ManifestSchemaData
from se_constitution.types.repo_requirements import RepoRequirementsData
from se_constitution.validate.class_registry import validate_class_registry
from se_constitution.validate.cross_file import validate_cross_file_consistency
from se_constitution.validate.dependency_rules import validate_dependency_rules
from se_constitution.validate.manifest_schema import validate_manifest_schema
from se_constitution.validate.naming_patterns import validate_naming_patterns
from se_constitution.validate.repo_requirements import validate_repo_requirements
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
# Valid set - one test per individual validator
# ---------------------------------------------------------------------------


class TestValidExamples:
    """Canonical valid artifact set must produce zero validation errors."""

    def test_valid_class_registry_passes(self) -> None:
        data = cast(
            ClassRegistryData, load_toml(VALID_DIR / "class" / "class-registry.toml")
        )
        errors = validate_class_registry(data)
        assert errors == [], f"Expected no errors; got: {errors}"

    def test_valid_naming_patterns_passes(self) -> None:
        data = cast(
            NamingPatternsData, load_toml(VALID_DIR / "naming" / "naming-patterns.toml")
        )
        errors = validate_naming_patterns(data)
        assert errors == [], f"Expected no errors; got: {errors}"

    def test_valid_dependency_rules_passes(self) -> None:
        data = cast(
            DependencyRulesData,
            load_toml(VALID_DIR / "dependency" / "dependency-rules.toml"),
        )
        errors = validate_dependency_rules(data)
        assert errors == [], f"Expected no errors; got: {errors}"

    def test_valid_manifest_schema_passes(self) -> None:
        data = cast(
            ManifestSchemaData,
            load_toml(VALID_DIR / "manifest" / "manifest-schema.toml"),
        )
        errors = validate_manifest_schema(data)
        assert errors == [], f"Expected no errors; got: {errors}"

    def test_valid_repo_requirements_passes(self) -> None:
        data = cast(
            RepoRequirementsData,
            load_toml(VALID_DIR / "repo" / "repo-requirements.toml"),
        )
        errors = validate_repo_requirements(data)
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


# ---------------------------------------------------------------------------
# Invalid set - example file violations plus targeted uncovered-line tests
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

    # --- targeted tests for uncovered validator lines ---

    def test_class_registry_rejects_empty_class_section(self) -> None:
        """Empty [class] section must be reported."""
        data = cast(dict[str, Any], make_valid_data())
        data["class_registry"]["class"] = {}
        errors = validate_class_registry(
            cast(ClassRegistryData, data["class_registry"])
        )
        assert "class-registry.toml: [class] must define at least one class." in errors

    def test_dependency_rules_rejects_allowed_not_a_list(self) -> None:
        """[dependency.{class}].allowed must be a list."""
        data = cast(dict[str, Any], make_valid_data())
        data["dependency_rules"]["dependency"]["kernel"]["allowed"] = "constitution"
        errors = validate_dependency_rules(
            cast(DependencyRulesData, data["dependency_rules"])
        )
        assert (
            "dependency-rules.toml: [dependency.kernel] must define allowed as a list."
            in errors
        )

    def test_manifest_schema_rejects_missing_meta(self) -> None:
        """Missing [meta] section must be reported."""
        data: dict[str, Any] = {"section": {}, "field": {}}
        errors = validate_manifest_schema(cast(ManifestSchemaData, data))
        assert "manifest-schema.toml: missing [meta] section." in errors

    def test_naming_patterns_rejects_missing_global(self) -> None:
        """Missing [global] section must be reported."""
        data = cast(dict[str, Any], make_valid_data())
        del data["naming_patterns"]["global"]
        errors = validate_naming_patterns(
            cast(NamingPatternsData, data["naming_patterns"])
        )
        assert "naming-patterns.toml: missing [global] section." in errors

    def test_naming_patterns_rejects_empty_pattern_section(self) -> None:
        """Empty [pattern] section must be reported."""
        data = cast(dict[str, Any], make_valid_data())
        data["naming_patterns"]["pattern"] = {}
        errors = validate_naming_patterns(
            cast(NamingPatternsData, data["naming_patterns"])
        )
        assert (
            "naming-patterns.toml: [pattern] must define at least one pattern."
            in errors
        )

    def test_repo_requirements_rejects_missing_summary(self) -> None:
        """[repo.{class}] missing summary must be reported."""
        data = cast(dict[str, Any], make_valid_data())
        del data["repo_requirements"]["repo"]["kernel"]["summary"]
        errors = validate_repo_requirements(
            cast(RepoRequirementsData, data["repo_requirements"])
        )
        assert "repo-requirements.toml: [repo.kernel] must define summary." in errors

    def test_repo_requirements_rejects_non_table_entry(self) -> None:
        """[repo.{class}] must be a table, not a scalar."""
        data = cast(dict[str, Any], make_valid_data())
        data["repo_requirements"]["repo"]["kernel"] = "not-a-table"
        errors = validate_repo_requirements(
            cast(RepoRequirementsData, data["repo_requirements"])
        )
        assert "repo-requirements.toml: [repo.kernel] must be a table." in errors
