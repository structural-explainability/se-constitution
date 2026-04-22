"""Readers for machine-readable project files."""

from pathlib import Path
import tomllib
from typing import Any


def read_toml(path: Path) -> dict[str, Any]:
    """Read a TOML file and return its parsed content."""
    with path.open("rb") as infile:
        return tomllib.load(infile)
