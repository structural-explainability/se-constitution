"""types/class_registry.py - Class registry artifact structure.

Represents the class-registry artifact as loaded from TOML.
Uses functional TypedDict syntax because "class" is a real TOML key.
Kept in its own file because class registry is a distinct constitutional
artifact with a stable repeated entry shape.
"""

from typing import TypedDict

from se_constitution.types.primitives import ArtifactMeta


class ClassDef(TypedDict, total=False):
    """Class definition structure.

    Represents one class entry from the class registry.
    Fields are optional here because validation is responsible for
    checking required semantic content such as summary or description.
    """

    summary: str
    description: str
    stable: bool


ClassRegistryData = TypedDict(
    "ClassRegistryData",
    {
        "meta": ArtifactMeta,
        "class": dict[str, ClassDef],
    },
)
