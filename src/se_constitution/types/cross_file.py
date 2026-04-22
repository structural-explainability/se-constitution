"""Typed representations for cross-file constitutional artifacts."""

from typing import TypedDict

from se_constitution.types.dependency import DependencyEntry

NamingPatternEntry = TypedDict(
    "NamingPatternEntry",
    {
        "class": str,
        "format": str,
    },
    total=False,
)
# WHY:
# - functional syntax required because "class" is a real TOML key
# - lightweight shared entry across validators


class NamingPatternsData(TypedDict):
    """Naming patterns artifact structure.

    Maps pattern identifiers to naming definitions.
    """

    pattern: dict[str, NamingPatternEntry]


class DependencyRulesData(TypedDict):
    """Dependency rules artifact structure.

    Reuses canonical dependency entry definitions.
    """

    dependency: dict[str, DependencyEntry]


ManifestSchemaData = TypedDict(
    "ManifestSchemaData",
    {
        "class": dict[str, object],
    },
    total=False,
)
# WHY:
# - functional syntax required because "class" is a real TOML key
# - only class mapping used in cross-file validation today


class RepoRequirementsData(TypedDict):
    """Repository requirements artifact structure.

    Maps repo class to requirement definitions.
    Kept broad until structure is enforced by validation.
    """

    repo: dict[str, object]
