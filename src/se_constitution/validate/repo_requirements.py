"""validate/repo_requirements.py - Validation for repo requirements data."""

from collections.abc import Mapping
from typing import Any, cast

from se_constitution.types.repo_requirements import RepoRequirementsData


def validate_repo_requirements(data: RepoRequirementsData) -> list[str]:
    """Validate repo requirements structure."""
    errors: list[str] = []

    repo_section = cast(dict[str, Any], data["repo"])

    if not repo_section:
        errors.append("repo-requirements.toml: [repo] must not be empty.")

    for repo_class, repo_def in repo_section.items():
        if not isinstance(repo_def, dict):
            errors.append(
                f"repo-requirements.toml: [repo.{repo_class}] must be a table."
            )
            continue

        repo_def_map = cast(Mapping[str, object], repo_def)
        summary = repo_def_map.get("summary")

        if not isinstance(summary, str) or not summary.strip():
            errors.append(
                f"repo-requirements.toml: [repo.{repo_class}] must define summary."
            )

    return errors
