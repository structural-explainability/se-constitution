"""Tests for naming patterns validation."""

from typing import cast

from se_constitution.types.cross_file import NamingPatternsData
from se_constitution.types.primitives import TomlData
from se_constitution.validate.naming_patterns import validate_naming_patterns
from tests.fixture.data import make_valid_data


def get_naming_patterns() -> NamingPatternsData:
    """Return a valid typed naming patterns artifact."""
    return cast(NamingPatternsData, make_valid_data()["naming_patterns"])


def test_validate_naming_patterns_accepts_valid_data() -> None:
    """A valid naming patterns file should produce no errors."""
    data = get_naming_patterns()
    errors = validate_naming_patterns(data)
    assert errors == []


def test_validate_naming_patterns_requires_format() -> None:
    """Each pattern must define a format."""
    data = cast(TomlData, get_naming_patterns())
    del data["pattern"]["schema"]["format"]
    errors = validate_naming_patterns(cast(NamingPatternsData, data))
    assert "naming-patterns.toml: [pattern.schema] must define format." in errors
