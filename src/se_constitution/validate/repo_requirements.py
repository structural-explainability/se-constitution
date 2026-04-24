"""validate/repo_requirements.py - Validation for repo requirements data."""

from se_constitution.types.cross_file import RepoRequirementsData


def validate_repo_requirements(data: RepoRequirementsData) -> list[str]:
    """Validate repo requirements structure."""
    errors: list[str] = []

    if "meta" not in data:
        errors.append("repo-requirements.toml: missing [meta] section.")

    repo_section = data["repo"]

    for repo_class, repo_def in repo_section.items():
        if not isinstance(repo_def, dict):
            errors.append(
                f"repo-requirements.toml: [repo.{repo_class}] must be a table."
            )
            continue

        if "summary" not in repo_def:
            errors.append(
                f"repo-requirements.toml: [repo.{repo_class}] must define summary."
            )

    return errors
