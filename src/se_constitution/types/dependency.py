"""Shared dependency type definitions."""

from typing import TypedDict

from se_constitution.types.primitives import ArtifactMeta


class DependencyEntry(TypedDict):
    """Dependency rule entry structure.

    Defines the allowed upstream dependency classes for one repo class.
    Kept minimal because current validation reads only this field.
    """

    allowed: list[str]


class PrincipleSection(TypedDict, total=False):
    """Principle flags for dependency rules."""

    no_cycles: bool
    no_reverse_foundation_dependencies: bool
    constitution_is_foundational: bool
    formal_contract_is_root: bool


class DependencyRulesData(TypedDict, total=False):
    """Dependency rules artifact structure.

    Represents the dependency-rules artifact as loaded from TOML.
    Kept in its own file because dependency rules are a distinct
    constitutional artifact with a stable repeated entry shape.
    """

    meta: ArtifactMeta
    principle: PrincipleSection
    dependency: dict[str, DependencyEntry]
