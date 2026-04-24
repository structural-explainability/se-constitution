"""types/repo_requirements.py - Repository requirements artifact structure.

Represents the repository requirements artifact as loaded from TOML.
Uses functional TypedDict syntax because "class" is a real TOML key.
Kept in its own file because repository requirements is a distinct constitutional
artifact with a stable repeated entry shape.
"""

from typing import TypedDict

from se_constitution.types.primitives import ArtifactMeta


class RepoRequirementEntry(TypedDict, total=False):
    """Repository requirement definition for one repo class."""

    summary: str
    required_root_files: list[str]
    required_root_directories: list[str]
    required_docs: list[str]
    recommended_docs: list[str]
    required_data: list[str]
    required_capabilities: list[str]
    forbidden_capabilities: list[str]
    require_ci: bool
    require_manifest_validation: bool
    require_data_validation: bool


class RepoRequirementsData(TypedDict):
    """Repository requirements artifact structure."""

    meta: ArtifactMeta
    repo: dict[str, RepoRequirementEntry]
