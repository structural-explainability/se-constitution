"""Typed representations for cross-file constitutional artifacts.

WHY-FILE:
    Cross-file validation consumes artifacts from multiple sources, including:
    - se-constitution TOML files
    - se-formal-contract JSON registries (via submodule)

    These TypedDicts define boundary shapes so validation logic can evolve
    without guessing artifact structure.

OWNS:
    - shared artifact shapes used in cross-file validation

DOES NOT OWN:
    - validation behavior
    - formal meanings of invariants
    - Lean definitions
"""

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


class FormalContractInvariantRegistryData(TypedDict):
    """Formal contract invariant registry structure.

    Loaded from se-formal-contract submodule.

    This represents the upstream formal contract authority.
    Used to validate dependency-rule principles
    against Lean-exported invariants.

    Invariants are canonical identifiers exported by the formal contract.

    They are used to validate that dependency-rule principles declared in
    se-constitution correspond to formally defined invariants.

    OBS:
    - se-constitution MUST NOT redefine invariant identifiers.
    - No class mapping exists at this layer; validation is name-based.
    """

    schema: str
    contract_version: str
    invariants: list[str]
