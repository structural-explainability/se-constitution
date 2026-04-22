"""Shared dependency type definitions."""

from typing import TypedDict


class DependencyEntry(TypedDict):
    """Dependency rule entry structure.

    Defines the allowed upstream dependency classes for one repo class.
    Kept minimal because current validation reads only this field.
    """

    allowed: list[str]


class DependencyRulesData(TypedDict):
    """Dependency rules artifact structure.

    Represents the dependency-rules artifact as loaded from TOML.
    Kept in its own file because dependency rules are a distinct
    constitutional artifact with a stable repeated entry shape.
    """

    meta: dict[str, str]
    dependency: dict[str, DependencyEntry]
