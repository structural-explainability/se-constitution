"""Tests for repo requirements validation."""

from typing import cast

from se_constitution.types.cross_file import RepoRequirementsData
from se_constitution.types.primitives import TomlData
from se_constitution.validate.repo_requirements import validate_repo_requirements
from tests.fixture.data import make_valid_data


def get_repo_requirements() -> RepoRequirementsData:
    """Return a valid typed repo requirements artifact."""
    return cast(RepoRequirementsData, make_valid_data()["repo_requirements"])


def test_validate_repo_requirements_accepts_valid_data() -> None:
    """A valid repo requirements file should produce no errors."""
    data = get_repo_requirements()
    errors = validate_repo_requirements(data)
    assert errors == []


def test_validate_repo_requirements_requires_summary() -> None:
    """Each repo requirement must define a summary."""
    data = cast(TomlData, get_repo_requirements())
    data["repo"]["kernel"] = {}
    errors = validate_repo_requirements(cast(RepoRequirementsData, data))
    assert "repo-requirements.toml: [repo.kernel] must define summary." in errors
