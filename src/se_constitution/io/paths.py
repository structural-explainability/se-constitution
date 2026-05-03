"""Path utilities for repo data files."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataPaths:
    """Canonical paths for repo data files."""

    repo_root: Path
    class_registry: Path
    naming_patterns: Path
    dependency_rules: Path
    repo_requirements: Path
    upstream_contract: Path

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> "DataPaths":
        """Construct canonical paths from the repository root."""
        root = repo_root or Path.cwd()
        data_dir = root / "data"

        return cls(
            repo_root=root,
            class_registry=data_dir / "class" / "class-registry.toml",
            naming_patterns=data_dir / "naming" / "naming-patterns.toml",
            dependency_rules=data_dir / "dependency" / "dependency-rules.toml",
            repo_requirements=data_dir / "repo" / "repo-requirements.toml",
            upstream_contract=root / "upstream" / "se-formal-contract" / "main",
        )
