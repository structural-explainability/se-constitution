"""types/naming_patterns.py - Type definitions for naming patterns artifact.

Defines the TypedDict structure for the naming-patterns artifact as loaded
from data/naming/naming-patterns.toml.
"""

from typing import TypedDict

from se_constitution.types.primitives import ArtifactMeta


class PatternEntry(TypedDict, total=False):
    """A single naming pattern entry."""

    class_: str  # maps to 'class' key in TOML
    format: str


class GlobalNamingRules(TypedDict, total=False):
    """Global naming constraints applied to all patterns."""

    required_prefix: str
    separator: str
    ascii_only: bool
    lowercase_only: bool
    allow_underscore: bool
    allow_space: bool


class NamingPatternsData(TypedDict, total=False):
    """Naming patterns artifact structure.

    Represents the naming-patterns artifact as loaded from TOML.
    """

    meta: ArtifactMeta
    global_: GlobalNamingRules  # maps to 'global' key in TOML
    pattern: dict[str, dict[str, object]]
