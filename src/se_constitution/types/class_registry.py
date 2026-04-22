"""Data types for class registry artifacts."""

from typing import TypedDict


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
        "meta": dict[str, str],
        "class": dict[str, ClassDef],
    },
)
"""Class registry artifact structure.

Represents the class-registry artifact as loaded from TOML.
Uses functional TypedDict syntax because "class" is a real TOML key.
Kept in its own file because class registry is a distinct constitutional
artifact with a stable repeated entry shape.
"""
