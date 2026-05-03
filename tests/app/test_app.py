"""Tests for application orchestration."""

from pathlib import Path

from se_constitution.io.paths import DataPaths


def test_constitution_paths_from_repo_root_builds_expected_paths(
    tmp_path: Path,
) -> None:
    """Canonical data paths should be resolved from a repo root."""
    paths = DataPaths.from_repo_root(tmp_path)

    assert paths.repo_root == tmp_path
    assert paths.class_registry == tmp_path / "data" / "class" / "class-registry.toml"
    assert paths.naming_patterns == (
        tmp_path / "data" / "naming" / "naming-patterns.toml"
    )
    assert paths.dependency_rules == (
        tmp_path / "data" / "dependency" / "dependency-rules.toml"
    )
    assert paths.repo_requirements == (
        tmp_path / "data" / "repo" / "repo-requirements.toml"
    )
