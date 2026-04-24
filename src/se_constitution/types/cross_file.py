"""types/cross_file.py - Typed representations for cross-file constitutional artifacts."""

from typing import TypedDict

from se_constitution.types.primitives import ArtifactMeta

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
# - entry-level type; meta belongs at the artifact level in NamingPatternsData


class NamingPatternsData(TypedDict):
    """Naming patterns artifact structure.

    Maps pattern identifiers to naming definitions.
    """

    meta: ArtifactMeta
    pattern: dict[str, NamingPatternEntry]
