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


ManifestSchemaData = TypedDict(
    "ManifestSchemaData",
    {
        "class": dict[str, object],
    },
    total=False,
)
# WHY:
# - functional syntax required because "class" is a real TOML key
# - Python does not support inheriting functional TypedDicts from class-syntax TypedDicts
# - consequence: "meta" cannot be declared required here
# - validate_manifest_schema therefore retains the "meta" not in data check,
#   which IS reachable because meta is absent from this TypedDict
# TODO: revisit if TypedDict inheritance across syntaxes is resolved in a future Python version


class RepoRequirementsData(TypedDict):
    """Repository requirements artifact structure.

    Maps repo class to requirement definitions.
    Kept broad until structure is enforced by validation.
    """

    meta: ArtifactMeta
    repo: dict[str, object]
